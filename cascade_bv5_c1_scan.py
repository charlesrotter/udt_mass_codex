"""C1 stage 1: scan miss = rho'(r_s) vs slice parameter, 10 pts concentrating toward stuck
(below side), per family x Z. Own integrator (DOP853, own event location)."""
import numpy as np, json
from bv5_common import make_A1, make_A3, make_A2, miss_bv5, SHOTS

# fractional offsets below the stuck point (concentrate toward stuck)
XS = np.array([0.10, 0.06, 0.035, 0.02, 0.012, 0.007, 0.004, 0.0022, 0.0012, 0.0006])

combos = [
    ("A1_m3_Z8", 8.0, 1.5,     lambda p: make_A1(3.0, p)),
    ("A1_m3_Z1", 1.0, 1.5,     lambda p: make_A1(3.0, p)),
    ("A3_Z8",    8.0, 1.0,     lambda p: make_A3(p)),
    ("A2_k3_Z8", 8.0, 2.0/3.0, lambda p: make_A2(3.0, p)),
]

results = {}
for lab, Z, stuck, mk in combos:
    print(f"\n===== {lab} (stuck={stuck:.10g}) =====")
    rows = []
    for x in XS:
        p = stuck * (1.0 - x)
        U, Up = mk(p)
        f, o = miss_bv5(Z, Up)
        rows.append((float(p), float(f) if np.isfinite(f) else None, o["status"],
                     float(o.get("r_s", np.nan)), float(o.get("rho_s", np.nan)),
                     float(o.get("q", np.nan))))
        fs = f"{f:+12.5e}" if np.isfinite(f) else "     nan    "
        print(f"  p={p:.10f} (x={x:.4f})  rho'_s={fs}  [{o['status']}]"
              f"  r_s={o.get('r_s', float('nan')):10.4g} rho_s={o.get('rho_s', float('nan')):8.5g}")
    # count sign changes among seal rows (in scan order = away->toward stuck)
    fs = [r[1] for r in rows if r[2] == "seal" and r[1] is not None]
    sc = sum(1 for f1, f2 in zip(fs, fs[1:]) if f1*f2 < 0)
    print(f"  seal-reaching: {len(fs)}/{len(rows)};  sign changes along scan: {sc}")
    results[lab] = {"stuck": stuck, "rows": rows, "sign_changes": sc}

with open("bv5_c1_scan.json", "w") as fh:
    json.dump(results, fh, indent=1)
print(f"\nSHOTS used this run: {SHOTS['n']}")
