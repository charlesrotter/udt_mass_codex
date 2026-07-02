"""T3 exploration driver: numerics robustness + rise-fall slice scan. Bounded, single process."""
import sys, numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import (make_power_slice, make_risefall_slice, shoot, miss,
                                     diagnose, LN1101)

# --- 1. numerics robustness: same point, tightened tolerance + bigger r_max ---
U, Up, _ = make_power_slice(1.0)
for (rt, at, rm) in [(1e-10, 1e-12, 5e7), (1e-12, 1e-14, 5e8)]:
    o = shoot(8.0, U, Up, 1.0, r_max=rm, rtol=rt, atol=at)
    print(f"[robust n=+1 Z=8 rtol={rt:g}] status={o['status']}"
          + (f" rho'_s={o['rhop_s']:.8e} q={o['q']:.8e} r_s={o['r_s']:.6e}" if o["status"] == "seal" else ""))

# --- 2. n->0+ limit probe (branch structure near the vacuum point) ---
for Z in (1.0, 8.0):
    for n in (0.01, 0.05, 0.1):
        U, Up, _ = make_power_slice(n)
        f, o = miss(Z, U, Up, 1.0, r_max=5e8)
        print(f"[n->0+ Z={Z:g}] n={n:.2f} status={o['status']}"
              + (f" rho'_s={f:+.4e} rho_s={o['rho_s']:.4f} q={o['q']:.4g}" if o["status"] == "seal" else ""))

# --- 3. rise-fall slice scan (m=2, a grid), both Z ---
for Z in (1.0, 8.0):
    print(f"\n===== risefall m=2, Z={Z:g} =====")
    rows = []
    for a in np.linspace(0.0, 3.0, 25):
        U, Up, lab = make_risefall_slice(a)
        f, o = miss(Z, U, Up, 1.0)
        rows.append((a, f, o["status"]))
        print(f"  a={a:6.3f}  rho'_s={f if np.isfinite(f) else float('nan'):+12.4e}  [{o['status']}]"
              + (f"  q={o['q']:9.4g} rho_s={o['rho_s']:9.4g}" if o["status"] == "seal" else ""))
    # bisect any sign change on seal-reaching pairs
    for (a1, f1, s1), (a2, f2, s2) in zip(rows, rows[1:]):
        if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1 * f2 < 0:
            lo, hi, flo = a1, a2, f1
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                U, Up, _ = make_risefall_slice(mid)
                fm, om = miss(Z, U, Up, 1.0)
                if not np.isfinite(fm): break
                if flo * fm <= 0: hi = mid
                else: lo, flo = mid, fm
            a_star = 0.5 * (lo + hi)
            U, Up, _ = make_risefall_slice(a_star)
            fm, om = miss(Z, U, Up, 1.0)
            if om["status"] == "seal":
                print(f"  ROOT a*={a_star:.8f}  (rho'_s={fm:+.2e})")
                d = diagnose(om, Z, U)
                for k, v in d.items(): print(f"      {k:22s} = {v}")
