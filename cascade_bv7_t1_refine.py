import json, time, numpy as np, sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from bv7_core import *

Z = 8.0
rows = json.load(open("bv7_t1_sweep.json"))

def F(a):
    U, Up, _ = make_risefall_slice(a, m=2.0)
    o = shoot(Z, Up)
    o["U"] = U
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o

results = []
t0 = time.time()
for r1, r2 in zip(rows, rows[1:]):
    if not (r1["status"] == r2["status"] == "seal" and r1["f"] is not None
            and r2["f"] is not None and r1["f"] * r2["f"] < 0):
        continue
    # bracket in a: note a decreases as d increases -> a-bracket = [a(d2), a(d1)]
    a_lo, a_hi = r2["a"], r1["a"]
    f_lo, f_hi = r2["f"], r1["f"]
    n0 = SHOTS["n"]
    a_star, f_star, o_star, its, conv = bracket_root(F, a_lo, a_hi, f_lo, f_hi,
                                                     xtol=1e-10, maxiter=22)
    d_star = 1.0 - a_star
    diag = diagnose(o_star, Z, o_star["U"])
    results.append({"a": a_star, "d": d_star, "diag_str": fmt_root("ROOT", a_star, d_star, diag),
                    "rho_s": diag["rho_s"], "q": diag["q"], "r_s": diag["r_s"],
                    "Nd": diag["Nd_100k"], "Np": diag["Np_100k"],
                    "Nd2": diag["Nd_200k"], "Np2": diag["Np_200k"],
                    "iters": its, "conv": conv, "shots": SHOTS["n"] - n0})
    print(results[-1]["diag_str"] + f"  [iters={its} conv={conv} shots={SHOTS['n']-n0}]")
    print(f"    Nd ladder(100k) k=2..13: {diag['Nd_ladder_100k']}")
    print(f"    Np ladder(100k) k=2..13: {diag['Np_ladder_100k']}")

print(f"\nT1 refine shots={SHOTS['n']}  {time.time()-t0:.1f}s")
json.dump([{k: v for k, v in r.items() if k != "diag_str"} for r in results],
          open("bv7_t1_roots.json", "w"), indent=1, default=str)
