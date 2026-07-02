import time, numpy as np, sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from bv7_core import *

Z = 1.0
STUCK = 1.5

def F(a):
    U, Up, _ = make_risefall_slice(a, m=3.0)   # reused slice, m=3
    o = shoot(Z, Up); o["U"] = U
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o

t0 = time.time()
d_grid = np.array([1.30, 1.34, 1.38, 1.42, 1.46, 1.50]) * 1e-3
pts = []
for d in d_grid:
    a = STUCK * (1.0 - d)
    f, o = F(a)
    pts.append((d, a, f))
    print(f"  d={d:.6e} a={a:.9f} [{o['status']:8s}] rhop_s={f:+.6e} "
          f"rho_s={o.get('rho_s', float('nan')):.6f} r_s={o.get('r_s', float('nan')):.2f}")

brs = []
for (d1, a1, f1), (d2, a2, f2) in zip(pts, pts[1:]):
    if np.isfinite(f1) and np.isfinite(f2) and f1 * f2 < 0:
        brs.append((a2, a1, f2, f1))
        print(f"  SIGN CHANGE: d in [{d1:.5e}, {d2:.5e}]")

for br in brs:
    a_lo, a_hi, f_lo, f_hi = br
    n0 = SHOTS["n"]
    a_star, f_star, o_star, its, conv = bracket_root(F, a_lo, a_hi, f_lo, f_hi,
                                                     xtol=1e-10, maxiter=22)
    d_star = 1.0 - a_star / STUCK
    diag = diagnose(o_star, Z, o_star["U"])
    print(fmt_root("T3 ROOT", a_star, d_star, diag)
          + f"  [iters={its} conv={conv} shots={SHOTS['n']-n0}]")
    print(f"    Nd ladder(100k): {diag['Nd_ladder_100k']}")
    print(f"    Np ladder(100k): {diag['Np_ladder_100k']}")
    print(f"    identity: Dphi_carried - ln(1101) = {diag['Dphi_carried'] - LN1101:+.3e}")
    print(f"    identity: 2m/rho(seal) - 1        = {diag['ms_seal'] - 1.0:+.3e}")

print(f"\nT3 shots this script={SHOTS['n']}  {time.time()-t0:.1f}s")
