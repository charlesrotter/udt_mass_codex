"""C1/C2/C3: bisect the FIRST root (farthest from stuck) per family x Z, own bisection;
then count interior zeros of delta=rho-1 and rho' on dense output (100k + 200k), with
noise floors, interleaving pattern, and a 10x zoom recount of the densest rho'-zero cluster.
Also: one far-side check shot (x=0.2 below stuck) per family to guard the 'first root' label."""
import numpy as np, json
from bv5_common import (make_A1, make_A3, make_A2, miss_bv5, shoot_bv5, bisect_root,
                        eval_dense, count_zeros, SHOTS)

COMBOS = [
    # label, Z, stuck, make_slice, bracket (p_lo, p_hi) and f values from the scan
    ("A1_m3_Z8", 8.0, 1.5,     lambda p: make_A1(3.0, p),
     1.4700000000, 1.4820000000, +1.78549e+00, -3.52293e-01, 1.2),
    ("A1_m3_Z1", 1.0, 1.5,     lambda p: make_A1(3.0, p),
     1.4940000000, 1.4967000000, +1.74675e-01, -1.42741e-01, 1.2),
    ("A3_Z8",    8.0, 1.0,     lambda p: make_A3(p),
     0.9650000000, 0.9800000000, +1.18824e+00, -1.08546e+00, 0.8),
    ("A2_k3_Z8", 8.0, 2.0/3.0, lambda p: make_A2(3.0, p),
     0.6533333333, 0.6586666667, +3.15366e-01, -2.68959e+00, 2.0/3.0*0.8),
]


def analyze_root(lab, Z, mk, p_star, n_base):
    """Final shot at p* with kept segments; zero counts at n_base and 2*n_base samples."""
    U, Up = mk(p_star)
    o = shoot_bv5(Z, Up, keep_segments=True)
    assert o["status"] == "seal", o["status"]
    r_s, segs = o["r_s"], o["segments"]
    res = {"p_star": p_star, "r_s": r_s, "rho_s": o["rho_s"], "q": o["q"],
           "rhop_s_resid": o["rhop_s"]}
    for N in (n_base, 2*n_base):
        rr = np.linspace(0.0, r_s, N)
        y = eval_dense(segs, rr)
        delta, rhop = y[2] - 1.0, y[3]
        fl_d = max(1e-12, 1e-8*np.max(np.abs(delta)))
        fl_p = max(1e-12, 1e-8*np.max(np.abs(rhop)), 3.0*abs(o["rhop_s"]))
        nd, pos_d, lobe_d = count_zeros(rr, delta, fl_d)
        np_, pos_p, lobe_p = count_zeros(rr, rhop, fl_p)
        res[f"N{N}"] = {"N_delta": nd, "N_rhop": np_,
                        "floor_delta": fl_d, "floor_rhop": fl_p,
                        "min_lobe_delta": lobe_d, "min_lobe_rhop": lobe_p,
                        "pos_delta": pos_d.tolist(), "pos_rhop": pos_p.tolist()}
        if N == n_base:
            # monotonicity of rho (C3): most-negative rho' in the interior
            res["min_rhop_interior"] = float(np.min(rhop[1:-1]))
            res["max_rhop_interior"] = float(np.max(rhop[1:-1]))
            res["rho_min"] = float(np.min(y[2])); res["rho_max"] = float(np.max(y[2]))
            # 10x zoom on densest rho'-zero cluster (if >=2 zeros) else zoom near seal
            allz = np.sort(np.concatenate([pos_p, pos_d]))
            if allz.size >= 2:
                gaps = np.diff(allz); i = int(np.argmin(gaps)); g = gaps[i]
                w0, w1 = max(0.0, allz[i]-2*g), min(r_s, allz[i+1]+2*g)
            else:
                w0, w1 = 0.9*r_s, r_s
            local_base = max(64, int(n_base*(w1-w0)/r_s))
            rz = np.linspace(w0, w1, 10*local_base)
            yz = eval_dense(segs, rz)
            ndz, _, _ = count_zeros(rz, yz[2]-1.0, fl_d)
            npz, _, _ = count_zeros(rz, yz[3], fl_p)
            in_w = lambda pos: sum(1 for x in pos if w0 <= x <= w1)
            res["zoom"] = {"window": [float(w0), float(w1)],
                           "N_delta_zoom": ndz, "N_rhop_zoom": npz,
                           "N_delta_base_in_window": in_w(pos_d),
                           "N_rhop_base_in_window": in_w(pos_p)}
    # interleaving pattern at base sampling
    pd = res[f"N{n_base}"]["pos_delta"]; pp = res[f"N{n_base}"]["pos_rhop"]
    merged = sorted([(x, "d") for x in pd] + [(x, "p") for x in pp])
    res["interleave"] = "".join(t for _, t in merged)
    return res


out = {}
for lab, Z, stuck, mk, p_lo, p_hi, f_lo, f_hi, p_far in COMBOS:
    print(f"\n===== {lab} =====")
    # far-side guard shot
    U, Up = mk(p_far)
    f_far, o_far = miss_bv5(Z, Up)
    print(f"  far-side p={p_far:.6f}: rho'_s={f_far:+.4e} [{o_far['status']}]")
    p_star, o_mid, st = bisect_root(mk, Z, p_lo, p_hi, f_lo, f_hi, tol=1e-9, itmax=32)
    print(f"  bisection [{p_lo}, {p_hi}] -> p* = {p_star:.12f} ({st})")
    # tolerance cross-check at looser rtol
    U, Up = mk(p_star)
    f_x, _ = miss_bv5(Z, Up, rtol=3e-9, atol=1e-11)
    print(f"  tolerance cross-check rtol=3e-9: rho'(r_s) = {f_x:+.3e}")
    res = analyze_root(lab, Z, mk, p_star, 100_000)
    res["far_side"] = {"p": p_far, "f": float(f_far) if np.isfinite(f_far) else None,
                       "status": o_far["status"]}
    res["f_crosscheck_rtol3e-9"] = float(f_x)
    out[lab] = res
    print(f"  ROOT: p*={p_star:.12f}  q={res['q']:.10f}  rho_s={res['rho_s']:.10f}"
          f"  r_s={res['r_s']:.6f}  resid rho'_s={res['rhop_s_resid']:+.2e}")
    for N in (100_000, 200_000):
        d = res[f"N{N}"]
        print(f"  [{N:>7d} samples] N_delta={d['N_delta']}  N_rhop={d['N_rhop']}"
              f"  floors=({d['floor_delta']:.2e},{d['floor_rhop']:.2e})"
              f"  min_lobes=({d['min_lobe_delta']:.3g},{d['min_lobe_rhop']:.3g})")
    print(f"  monotonicity: min rho' interior = {res['min_rhop_interior']:+.4e},"
          f" max rho' = {res['max_rhop_interior']:+.4e}, rho in [{res['rho_min']:.6f},"
          f" {res['rho_max']:.6f}]")
    print(f"  zoom: {res['zoom']}")
    print(f"  interleave pattern (d=delta zero, p=rho' zero): '{res['interleave']}'")

with open("bv5_roots_first.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(f"\nSHOTS used this run: {SHOTS['n']}")
