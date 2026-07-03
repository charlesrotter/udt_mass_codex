"""bv11 V1/V2 part 1: 19-shot geometric bracket scan of d' in [0.0060, ~0.00718]."""
import json
import numpy as np
import bv11_lib as L

dps = 0.0060 * 1.01 ** np.arange(19)
rows = []
for dp in dps:
    f, o = L.miss_dp(dp, keep=True)
    row = {"dprime": float(dp), "a": 1.5 * (1 + dp), "status": o["status"],
           "miss": float(f) if np.isfinite(f) else None}
    if o["status"] == "seal":
        rr = np.linspace(0, o["r_s"], 100001)
        phi, phip, rho, rhop = L.eval_traj(o["sols"], rr)
        Nd, _ = L.graded_count((rho - 1.0)[1:-1])
        Np, _ = L.graded_count(rhop[1:-1])
        row.update(rho_s=float(o["y_s"][2]), r_s=o["r_s"],
                   q=float(L.Z * o["y_s"][2] ** 2 * o["y_s"][1]),
                   N_delta=Nd, N_rhop=Np)
    rows.append(row)
    print(row, flush=True)

print("\nSIGN CHANGES (seal-to-seal):")
brs = []
for r1, r2 in zip(rows, rows[1:]):
    if r1["status"] == r2["status"] == "seal" and r1["miss"] * r2["miss"] < 0:
        brs.append((r1["dprime"], r2["dprime"], r1["N_delta"], r2["N_delta"]))
        print(f"  bracket d'=({r1['dprime']:.7f},{r2['dprime']:.7f}) "
              f"N_delta endpoints=({r1['N_delta']},{r2['N_delta']})")
json.dump({"rows": rows, "brackets": brs, "shots": L.SHOTS["n"]},
          open("bv11_scan.json", "w"), indent=1)
print("shots:", L.SHOTS["n"])
