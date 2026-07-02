"""C4 refine: hunt the claimed b~0.99916 root inside (0.9991, 0.9993) where my coarse grid
saw f>0 at both ends (possible missed root PAIR). 8-point scan + bisection + counts."""
import numpy as np, json
from bv5_common import make_A3, miss_bv5, shoot_bv5, bisect_root, eval_dense, count_zeros, SHOTS

Z = 8.0
grid = np.linspace(0.99910, 0.99925, 8)
rows = []
for b in grid:
    U, Up = make_A3(b)
    f, o = miss_bv5(Z, Up)
    rows.append((float(b), float(f), o["status"], float(o.get("r_s", np.nan))))
    print(f"b={b:.6f}  rho'_s={f:+.5e}  [{o['status']}]  r_s={o.get('r_s', float('nan')):.6g}")

brackets = [(b1, b2, f1, f2) for (b1, f1, s1, _), (b2, f2, s2, _) in zip(rows, rows[1:])
            if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1*f2 < 0]
print("sign-change subintervals:", [(round(b1, 7), round(b2, 7)) for b1, b2, *_ in brackets])

res = {"scan": rows, "brackets": [(b1, b2) for b1, b2, *_ in brackets]}
if brackets:
    b1, b2, f1, f2 = min(brackets, key=lambda t: abs(0.5*(t[0]+t[1]) - 0.99916))
    p_star, o_mid, st = bisect_root(lambda p: make_A3(p), Z, b1, b2, f1, f2, tol=1e-9, itmax=24)
    print(f"bisection [{b1:.7f},{b2:.7f}] -> b* = {p_star:.12f} ({st})")
    U, Up = make_A3(p_star)
    o = shoot_bv5(Z, Up, keep_segments=True)
    assert o["status"] == "seal"
    r_s, segs = o["r_s"], o["segments"]
    print(f"ROOT: b*={p_star:.12f}  q={o['q']:.10f}  rho_s={o['rho_s']:.10f}  r_s={r_s:.6f}"
          f"  resid rho'_s={o['rhop_s']:+.2e}")
    res.update(b_star=p_star, r_s=r_s, rho_s=o["rho_s"], q=o["q"], resid=o["rhop_s"])
    for N in (300_000, 600_000):
        rr = np.linspace(0.0, r_s, N)
        y = eval_dense(segs, rr)
        delta, rhop = y[2] - 1.0, y[3]
        fl_d = max(1e-12, 1e-8*np.max(np.abs(delta)))
        fl_p = max(1e-12, 1e-8*np.max(np.abs(rhop)), 3.0*abs(o["rhop_s"]))
        nd, pos_d, lobe_d = count_zeros(rr, delta, fl_d)
        np_, pos_p, lobe_p = count_zeros(rr, rhop, fl_p)
        merged = sorted([(x, "d") for x in pos_d] + [(x, "p") for x in pos_p])
        pat = "".join(t for _, t in merged)
        dd = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "d")
        pp = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "p")
        print(f"[{N} samples] N_delta={nd}  N_rhop={np_}  floors=({fl_d:.2e},{fl_p:.2e})"
              f"  min_lobes=({lobe_d:.3e},{lobe_p:.3e})  adj-dd={dd} adj-pp={pp}")
        res[f"N{N}"] = {"N_delta": nd, "N_rhop": np_, "floor_delta": fl_d,
                        "floor_rhop": fl_p, "min_lobe_delta": lobe_d,
                        "min_lobe_rhop": lobe_p, "adj_dd": dd, "adj_pp": pp}
        if N == 300_000:
            allz = np.sort(np.concatenate([pos_d, pos_p]))
            gaps = np.diff(allz)
            i = int(np.argmin(gaps)); g = max(gaps[i], 1e-6)
            for wlab, (a0, a1) in (("min-gap", (max(0, allz[i]-5*g), min(r_s, allz[i+1]+5*g))),
                                    ("near-seal", (0.98*r_s, r_s))):
                local_base = max(256, int(N*(a1-a0)/r_s))
                rz = np.linspace(a0, a1, 10*local_base)
                yz = eval_dense(segs, rz)
                ndz, _, _ = count_zeros(rz, yz[2]-1.0, fl_d)
                npz, _, _ = count_zeros(rz, yz[3], fl_p)
                base_d = sum(1 for x in pos_d if a0 <= x <= a1)
                base_p = sum(1 for x in pos_p if a0 <= x <= a1)
                print(f"    zoom[{wlab}] [{a0:.2f},{a1:.2f}] 10x: N_delta {base_d}->{ndz},"
                      f" N_rhop {base_p}->{npz}")
            print(f"    gap stats: min={gaps.min():.4f} median={np.median(gaps):.4f}"
                  f" @300k spacing={r_s/N:.4f}")
else:
    print("NO sign change found in (0.9991, 0.9993) at this resolution -- claimed root NOT"
          " reproduced at Db=2.1e-5.")

with open("bv5_c4_refine.json", "w") as fh:
    json.dump(res, fh, indent=1)
print(f"SHOTS used this run: {SHOTS['n']}")
