"""Finite exact checks for the PEA1 A conformal-clock protocol, no solver."""
import hashlib
import json
import platform
from pathlib import Path

import sympy as s

root = Path(__file__).resolve().parent
out = root / "CHECK_RESULT.json"
if out.exists():
    raise RuntimeError("REFUSE_OVERWRITE")

t, r, theta, phi = s.symbols("t r theta phi", real=True)
m = s.symbols("m", positive=True)
omega = s.Function("Omega", positive=True)(t, r)
x = [t, r, theta, phi]
f = 1 - 2*m/r
g = s.diag(-omega**2*f, omega**2/f, omega**2*r**2,
           omega**2*r**2*s.sin(theta)**2)
gi = g.inv()
gamma = [[[s.simplify(sum(gi[a, d]*(s.diff(g[d, c], x[b])
              + s.diff(g[d, b], x[c])-s.diff(g[b, c], x[d]))
              for d in range(4))/2)
           for c in range(4)] for b in range(4)] for a in range(4)]

checks = {}
def zero(name, expression):
    residual = s.simplify(expression)
    checks[name] = {"pass": residual == 0, "residual": str(residual)}

def acceleration(v):
    return [s.simplify(sum(v[b]*s.diff(v[a], x[b]) for b in range(4))
          + sum(gamma[a][b][c]*v[b]*v[c]
                for b in range(4) for c in range(4))) for a in range(4)]

u = s.Matrix([1/(omega*s.sqrt(f)), 0, 0, 0])
zero("held_clock_unit", (u.T*g*u)[0] + 1)
acc = acceleration(u)
expected_acc_r = m/(omega**2*r**2) + f*s.diff(omega, r)/omega**3
for a in range(4):
    zero(f"held_clock_acceleration_{a}", acc[a] - (expected_acc_r if a == 1 else 0))

for direction in [-1, 1]:
    k = s.Matrix([1/(omega**2*f), direction/omega**2, 0, 0])
    zero(f"radial_null_{direction}", (k.T*g*k)[0])
    for a, residual in enumerate(acceleration(k)):
        zero(f"radial_affine_geodesic_{direction}_{a}", residual)
    frequency = -(u.T*g*k)[0]
    zero(f"held_frequency_{direction}", frequency - 1/(omega*s.sqrt(f)))

h, beta, ell, xa = s.symbols("H beta L x_A", real=True)
fa, fb = s.symbols("f_A f_B", positive=True)
ea, eb = s.exp(h*t+beta*xa), s.exp(h*(t+ell)+beta*(xa+ell))
ear = s.exp(h*(t+2*ell)+beta*xa)
zout = eb*s.sqrt(fb)/(ea*s.sqrt(fa))
zin = ear*s.sqrt(fa)/(eb*s.sqrt(fb))
q = s.simplify(zout*zin)
zero("echo_product", q-s.exp(2*h*ell))
zero("outbound_contrast", zout/s.sqrt(fb/fa)-s.exp((h+beta)*ell))
zero("return_contrast", zin/s.sqrt(fa/fb)-s.exp((h-beta)*ell))

# Independent clock-history differentiation: h is nonzero only for this
# antiderivative; the direct lapse expression and continuous h=0 limit remain.
tau_a = s.sqrt(fa)*s.exp(beta*xa)*s.exp(h*t)/h
q_history = s.simplify(s.diff(tau_a.subs(t, t+2*ell), t)/s.diff(tau_a, t))
zero("echo_from_proper_clock_history", q_history-q)
i0 = s.symbols("I0", nonzero=True)
ie, ir = i0/ea**4, i0/ear**4
zero("echo_tide_identity", q**4*ir-ie)

# A transparent false-positive witness: H=1, beta=2, L=1 is an exact
# dimensionless control, not a measured/fitted physical scale.
false_positive = {
    "echo": str(q.subs({h: 1, beta: 2, ell: 1})),
    "outbound_contrast": str(s.exp((h+beta)*ell).subs({h: 1, beta: 2, ell: 1})),
    "return_contrast": str(s.exp((h-beta)*ell).subs({h: 1, beta: 2, ell: 1})),
    "interpretation": "echo>1 but return contrast<1; exact exponential signs",
}

data = {
    "status": "PASS" if all(v["pass"] for v in checks.values()) else "FAIL",
    "scope": "Exact symbolic identities for arbitrary positive Omega(t,r), Schwarzschild exterior r>2m>0, regular angular chart; no Ricci-flat-anchor reconstruction checked here.",
    "versions": {"python": platform.python_version(), "sympy": s.__version__},
    "input_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), root / "OPERATIONAL_PROBE_PLAN.md", root / "COMPUTE_PLAN.md"]},
    "coordinate_order": [str(v) for v in x],
    "metric_shape": [4, 4], "christoffel_shape": [4, 4, 4],
    "held_acceleration_r": str(expected_acc_r),
    "checks": checks,
    "count": len(checks),
    "false_positive": false_positive,
    "omissions": ["No instrument errors or empirical recovery bound", "No full curvature contraction or CVA uniqueness check", "Symbolic regression supports but does not replace analytic proof", "No global/horizon/asymptotic claim"],
}
out.write_text(json.dumps(data, indent=2)+"\n")
print(json.dumps(data, indent=2))
raise SystemExit(0 if data["status"] == "PASS" else 1)
