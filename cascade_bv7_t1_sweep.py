import json, time, numpy as np, sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from bv7_core import *

Z = 8.0
NPTS = 53
dgrid = 3.8e-3 * (7.0e-3 / 3.8e-3) ** (np.arange(NPTS) / (NPTS - 1))
print(f"T1 sweep: A1 m=2 Z=8, {NPTS} pts, d in [{dgrid[0]:.4e},{dgrid[-1]:.4e}], "
      f"step ratio {dgrid[1]/dgrid[0]-1:.5%}")

rows = []
t0 = time.time()
for d in dgrid:
    a = 1.0 - d
    U, Up, _ = make_risefall_slice(a, m=2.0)
    o = shoot(Z, Up)
    f = o["rhop_s"] if o["status"] == "seal" else np.nan
    rows.append({"d": float(d), "a": float(a), "status": o["status"],
                 "f": float(f) if np.isfinite(f) else None,
                 "rho_s": o.get("rho_s"), "q": o.get("q"), "r_s": o.get("r_s")})
    print(f"  d={d:.6e} a={a:.8f} [{o['status']:8s}] rhop_s={f:+.6e} "
          f"rho_s={o.get('rho_s', float('nan')):.6f} r_s={o.get('r_s', float('nan')):.2f}")

sc = 0
for r1, r2 in zip(rows, rows[1:]):
    if (r1["status"] == r2["status"] == "seal" and r1["f"] is not None
            and r2["f"] is not None and r1["f"] * r2["f"] < 0):
        sc += 1
        print(f"SIGN CHANGE #{sc}: d in [{r1['d']:.6e}, {r2['d']:.6e}]")
print(f"total sign changes: {sc}  shots={SHOTS['n']}  {time.time()-t0:.1f}s")
json.dump(rows, open("bv7_t1_sweep.json", "w"), indent=1)
