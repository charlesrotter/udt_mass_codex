"""C4: the big-N root in A3 (Z=8) near b~0.99916. Own scan of [0.9985,0.9995], own
bisection of the sign-change subinterval nearest 0.99916, then zero counts of delta=rho-1
and rho' at 300k AND 600k samples, plus 10x zoom recount of the densest cluster and a
Rolle/interleave audit (adjacent same-type zeros = missed-zero indicator)."""
import numpy as np, json
from bv5_common import make_A3, miss_bv5, shoot_bv5, bisect_root, eval_dense, count_zeros, SHOTS

Z = 8.0
grid = [0.9985, 0.9987, 0.9989, 0.9991, 0.9993, 0.9995]
rows = []
for b in grid:
    U, Up = make_A3(b)
    f, o = miss_bv5(Z, Up)
    rows.append((b, f, o["status"], o.get("r_s", np.nan)))
    print(f"b={b:.6f}  rho'_s={f:+.5e}  [{o['status']}]  r_s={o.get('r_s', float('nan')):.6g}")

# sign-change subintervals
brackets = [(b1, b2, f1, f2) for (b1, f1, s1, _), (b2, f2, s2, _) in zip(rows, rows[1:])
            if s1 == s2 == "seal" and np.isfinite(f1) and np.isfinite(f2) and f1*f2 < 0]
print("sign-change subintervals:", [(b1, b2) for b1, b2, *_ in brackets])
# pick the one nearest 0.99916
tgt = 0.99916
b1, b2, f1, f2 = min(brackets, key=lambda t: abs(0.5*(t[0]+t[1]) - tgt))
p_star, o_mid, st = bisect_root(lambda p: make_A3(p), Z, b1, b2, f1, f2, tol=1e-10, itmax=32)
print(f"bisection [{b1},{b2}] -> b* = {p_star:.12f} ({st})")

U, Up = make_A3(p_star)
f_x, _ = miss_bv5(Z, U if False else Up, rtol=3e-9, atol=1e-11)
print(f"tolerance cross-check rtol=3e-9: rho'(r_s) = {f_x:+.3e}")

o = shoot_bv5(Z, Up, keep_segments=True)
assert o["status"] == "seal"
r_s, segs = o["r_s"], o["segments"]
print(f"ROOT: b*={p_star:.12f}  q={o['q']:.10f}  rho_s={o['rho_s']:.10f}  r_s={r_s:.6f}"
      f"  resid rho'_s={o['rhop_s']:+.2e}")

res = {"b_star": p_star, "r_s": r_s, "rho_s": o["rho_s"], "q": o["q"],
       "rhop_s_resid": o["rhop_s"], "f_crosscheck": float(f_x)}
for N in (300_000, 600_000):
    rr = np.linspace(0.0, r_s, N)
    y = eval_dense(segs, rr)
    delta, rhop = y[2] - 1.0, y[3]
    fl_d = max(1e-12, 1e-8*np.max(np.abs(delta)))
    fl_p = max(1e-12, 1e-8*np.max(np.abs(rhop)), 3.0*abs(o["rhop_s"]))
    nd, pos_d, lobe_d = count_zeros(rr, delta, fl_d)
    np_, pos_p, lobe_p = count_zeros(rr, rhop, fl_p)
    print(f"[{N} samples] N_delta={nd}  N_rhop={np_}  floors=({fl_d:.2e},{fl_p:.2e})"
          f"  min_lobes=({lobe_d:.3e},{lobe_p:.3e})")
    res[f"N{N}"] = {"N_delta": nd, "N_rhop": np_, "floor_delta": fl_d, "floor_rhop": fl_p,
                    "min_lobe_delta": lobe_d, "min_lobe_rhop": lobe_p,
                    "pos_delta": pos_d.tolist(), "pos_rhop": pos_p.tolist()}
    # interleave / Rolle audit
    merged = sorted([(x, "d") for x in pos_d] + [(x, "p") for x in pos_p])
    pat = "".join(t for _, t in merged)
    dd = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "d")
    pp = sum(1 for a, b in zip(pat, pat[1:]) if a == b == "p")
    print(f"    interleave: len={len(pat)} adjacent-dd={dd} adjacent-pp={pp}"
          f"  head='{pat[:40]}' tail='{pat[-40:]}'")
    res[f"N{N}"]["pattern_head"] = pat[:80]; res[f"N{N}"]["adj_dd"] = dd
    res[f"N{N}"]["adj_pp"] = pp
    if N == 300_000:
        # densest-cluster 10x zoom recount
        allz = np.sort(np.concatenate([pos_d, pos_p]))
        gaps = np.diff(allz); i = int(np.argmin(gaps)); g = max(gaps[i], 1e-6)
        w0, w1 = max(0.0, allz[i]-5*g), min(r_s, allz[i+1]+5*g)
        # also zoom the last 2% before the seal (densest physical clustering region)
        for wlab, (a0, a1) in (("min-gap", (w0, w1)), ("near-seal", (0.98*r_s, r_s))):
            local_base = max(256, int(N*(a1-a0)/r_s))
            rz = np.linspace(a0, a1, 10*local_base)
            yz = eval_dense(segs, rz)
            ndz, pdz, _ = count_zeros(rz, yz[2]-1.0, fl_d)
            npz, ppz, _ = count_zeros(rz, yz[3], fl_p)
            base_d = sum(1 for x in pos_d if a0 <= x <= a1)
            base_p = sum(1 for x in pos_p if a0 <= x <= a1)
            print(f"    zoom[{wlab}] r in [{a0:.4f},{a1:.4f}] 10x: N_delta {base_d}->{ndz},"
                  f" N_rhop {base_p}->{npz}")
            res[f"zoom_{wlab}"] = {"window": [float(a0), float(a1)], "base": [base_d, base_p],
                                   "zoom10x": [ndz, npz]}
        # gap statistics
        print(f"    zero-gap stats (all zeros merged): min={gaps.min():.4f}"
              f" median={np.median(gaps):.4f} max={gaps.max():.4f}"
              f" @300k sample spacing={r_s/N:.4f}")

with open("bv5_c4_bigN.json", "w") as fh:
    json.dump(res, fh, indent=1)
print(f"SHOTS used this run: {SHOTS['n']}")
