"""C4 (gamma=0 census + slope identity) and C5 (f>=1 structure, piercing,
seal thinness)."""
import numpy as np
from el_core import run_flow, classify, threshold, SQ3

# ---------- C4: gamma = 0 census ----------
print("C4 census, gamma = 0 (claim: every c>0 TERM, minF ~ 0.970):")
for c in [1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.3, 1.0]:
    lab, sol = classify(0.0, c, Tmax=120.0)
    F = sol.y[0]
    print(f"  c={c:<8g} {lab:4s} t_end={sol.t[-1]:8.3f}  minF={F.min():.6f}  "
          f"Fbar_end={F[-1]:.4f}")

# slope identity numeric check: d f_min/d(1-y)|_1 = gamma - sqrt(3) c
# f_min(y) = F - sqrt(3) a  (a>0);  d/d(1-y) = -d/dy; at t=0:
#   -(F' - sqrt3 a')|_{y=1} = gamma - sqrt3 c.  Numeric: small-t expansion.
for gamma, c in [(0.0, 0.1), (1/3, 0.05), (1/3, 0.3), (0.7, 0.1)]:
    sol, _ = run_flow(gamma, c, Tmax=0.01, t_eval=np.linspace(0, 0.01, 11))
    fmin = sol.y[0] - SQ3*sol.y[2]
    # 1-y = 1-e^-t ~ t for small t
    one_my = 1 - np.exp(-sol.t)
    slope = (fmin[1]-fmin[0])/(one_my[1]-one_my[0])
    print(f"  slope check g={gamma:.4f} c={c}: numeric={slope:+.6f} "
          f"claimed g-sqrt3*c={gamma-SQ3*c:+.6f}")

# ---------- C5 ----------
print("\nC5:")
gamma = 1/3
cstar = threshold(gamma, 0.02, 0.06, tol_rel=1e-6, Tmax=80.0)
print(f"  c*(1/3) = {cstar:.6f}")

def profile(gamma, c, Tmax=80.0, n=40001):
    sol, sealed = run_flow(gamma, c, Tmax=Tmax, dense=True)
    tend = sol.t[-1]
    ts = np.linspace(0, tend, n)
    u = sol.sol(ts)
    F, A = u[0], u[2]
    k = SQ3*A/F
    fmin = F*(1-k)        # south pole f
    fmax = F*(1+k)
    return ts, F, A, k, fmin, sealed

# (a) clean band c < gamma/sqrt3: F >= 1 everywhere? fmin behavior?
for c in [cstar+1e-3, 0.1, gamma/SQ3*0.98]:
    ts, F, A, k, fmin, sealed = profile(gamma, c)
    # find first crossing fmin < 1
    idx = np.where(fmin < 1.0)[0]
    tc = ts[idx[0]] if len(idx) else None
    print(f"  g=1/3 c={c:.6f} sealed={sealed} t_seal={ts[-1]:.4f} minF={F.min():.6f} "
          f"min_fmin={fmin.min():.4g} first fmin<1 at t={tc if tc is None else round(tc,4)} "
          f"shellfrac={(ts[-1]-tc)/ts[-1] if tc is not None else float('nan'):.5f}")

# (b) piercing above band: c > gamma/sqrt3 -> fmin < 1 immediately inside
for c in [gamma/SQ3*1.02, gamma/SQ3*1.5]:
    ts, F, A, k, fmin, sealed = profile(gamma, c, Tmax=80.0)
    early = fmin[ts < 0.05]
    print(f"  g=1/3 c={c:.6f} (>g/sqrt3={gamma/SQ3:.6f}): fmin just inside "
          f"(t<0.05): min={early.min():.6f}  (pierced={early.min()<1})")

# below band: fmin should rise initially
c = gamma/SQ3*0.9
ts, F, A, k, fmin, sealed = profile(gamma, c)
early = fmin[ts < 0.05]
print(f"  g=1/3 c={c:.6f} (<g/sqrt3): fmin just inside min={early.min():.8f} "
      f"(should be >=1: {early.min()>=1.0})")

# (c) seal thinness at c = c* + 1e-3 (claim ~0.4% of log-depth)
c = cstar + 1e-3
ts, F, A, k, fmin, sealed = profile(gamma, c, n=400001)
idx = np.where(fmin < 1.0)[0]
tc = ts[idx[0]]
print(f"  seal shell at c=c*+1e-3: t_seal={ts[-1]:.5f}, fmin<1 from t={tc:.5f}; "
      f"fraction of log-depth = {(ts[-1]-tc)/ts[-1]*100:.3f}%  (claim ~0.4%)")
print(f"  fmin at seal -> {fmin[-1]:.4g} (claim -> 0); F at seal = {F[-1]:.4f}")

# (d) momentum-only: f = 1 pointwise ON interface (a(1)=0, F(1)=1) - trivial;
# maintained slightly inside? f(theta) = F + sqrt3 a cos(theta): at t=eps,
# a ~ c*eps != 0 so NOT pointwise 1 inside. Quantify:
sol, _ = run_flow(gamma, 0.1, Tmax=0.001, t_eval=[0, 0.001])
print(f"  a at t=0: {sol.y[2][0]:.2e}; at t=1e-3: {sol.y[2][1]:.4e} "
      f"(pointwise f=1 NOT maintained inside; interface-sphere-only statement)")
