"""Independent CES1 source-first algebra anchors; not a smooth-bump proof.

Question: does the frozen interior reciprocal probe change the physical clock
contrast when preparation rapidity and proper separation are fixed?
Exact SymPy arithmetic, one CPU, no mesh, no GPU, <=60 s/512 MiB via capture.py.
No producer candidate/code/output or other review is used. B0 and B1 encode
analytic compact smooth-bump moments; existence and support are proved in prose.
"""
import json
import platform
import sympy as S

s, L, v, B0, B1, eps, f, r, theta = S.symbols(
    "s L v B0 B1 eps f r theta", real=True
)
checks = []


def zero(name, expr):
    simplified = S.factor(S.simplify(expr))
    passed = (all(x == 0 for x in simplified) if isinstance(simplified, S.MatrixBase)
              else simplified == 0)
    assert passed, (name, simplified)
    checks.append({"name": name, "kind": "exact identity", "pass": True})


def reject(name, residual):
    simplified = S.factor(S.simplify(residual))
    assert simplified != 0, (name, simplified)
    checks.append({"name": name, "kind": "wrong formula rejected", "pass": True,
                   "nonzero_residual": str(simplified)})


# Integrating the first-order null ODE across the shell yields this delay.
delay = 2 * (s * B0 + B1)
A0 = (s + L) / (1 - v)
zero("baseline moving intersection", A0 - s - (L + v * A0))

# Solve the linearized moving-arrival equation rather than holding its radius.
dA = S.solve(S.Eq(S.Symbol("dA"), v * S.Symbol("dA") + delay),
             S.Symbol("dA"))[0]
zero("moving arrival perturbation", dA - delay / (1 - v))
zero("log tick perturbation", S.diff(dA, s) / S.diff(A0, s) - 2 * B0)
reject("omit moving receiver intersection", delay - v * delay - delay)

# Rational boost eta=log(2), an exact non-comoving normalization anchor.
boost_v = S.Rational(3, 5)
proper_rate = S.Rational(4, 5)
Z0 = proper_rate * S.diff(A0, s).subs(v, boost_v)
zero("physical rapidity baseline Z=e^eta", Z0 - 2)
reject("coordinate arrival slope is proper tick ratio",
       S.diff(A0, s).subs(v, boost_v) - Z0)

# Reconstruct FCV1 from an affine baseline ray of spatial length R=A0-s.
R = S.factor(A0 - s)
ray_integral = R * delay
normalization_denominator = R * (1 - v)  # N_o omega_o
zero("FCV1 affine arrival cross-check", ray_integral / normalization_denominator - dA)
zero("endpoint motion denominator cancellation",
     S.diff(ray_integral / normalization_denominator, s) / S.diff(A0, s) - 2 * B0)

# Reciprocal admissibility in orthonormal t/r coordinates at the baseline.
metric = S.diag(-S.exp(-2 * eps * f), S.exp(2 * eps * f), 1, 1)
zero("exact full determinant", metric.det() + 1)
h = metric.diff(eps).subs(eps, 0)
zero("factor-two reciprocal tangent", h - S.diag(2*f, 2*f, 0, 0))
zero("trace-free tangent", S.trace(S.diag(-1, 1, 1, 1) * h))
zero("future radial null slope", -S.exp(-2*eps*f)*S.exp(2*eps*f)**2 + S.exp(2*eps*f))

print(json.dumps({
    "python": platform.python_version(), "sympy": S.__version__,
    "scope": "Exact algebra anchors for independent analytic source-first argument",
    "checks": checks, "passed": len(checks),
    "not_claimed": ["smooth bump support proved by this script", "formal proof",
                    "different model/library", "physical field solution", "locality theorem"]
}, indent=2))
