import json, time, numpy as np, sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from bv7_core import *

Z = 8.0

def F_A2(a):
    U, Up = make_A2_slice(a)          # my own slice: 2 rho^2 exp(-a(rho^3-1)), stuck 2/3
    o = shoot(Z, Up); o["U"] = U
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o

def F_A3(b):
    U, Up = make_A3_slice(b)          # my own slice: 2 rho^2 (1+b)/(1+b rho^4), stuck 1
    o = shoot(Z, Up); o["U"] = U
    return (o["rhop_s"] if o["status"] == "seal" else np.nan), o

def d_to_p(fam, d):
    return (2.0 / 3.0) * (1.0 - d) if fam == "A2" else 1.0 - d

def p_to_d(fam, p):
    return 1.0 - p / (2.0 / 3.0) if fam == "A2" else 1.0 - p

def hunt(fam, F, d_grid):
    print(f"--- {fam} scan ---")
    pts = []
    for d in d_grid:
        p = d_to_p(fam, d)
        f, o = F(p)
        pts.append((d, p, f))
        print(f"  d={d:.6e} p={p:.9f} [{o['status']:8s}] rhop_s={f:+.6e} "
              f"rho_s={o.get('rho_s', float('nan')):.6f} r_s={o.get('r_s', float('nan')):.2f}")
    brs = []
    for (d1, p1, f1), (d2, p2, f2) in zip(pts, pts[1:]):
        if np.isfinite(f1) and np.isfinite(f2) and f1 * f2 < 0:
            brs.append((p2, p1, f2, f1))   # p decreases as d increases
            print(f"  SIGN CHANGE: d in [{d1:.5e}, {d2:.5e}]")
    return brs

def refine(fam, F, br):
    p_lo, p_hi, f_lo, f_hi = br
    n0 = SHOTS["n"]
    p_star, f_star, o_star, its, conv = bracket_root(F, p_lo, p_hi, f_lo, f_hi,
                                                     xtol=1e-10, maxiter=22)
    d_star = p_to_d(fam, p_star)
    diag = diagnose(o_star, Z, o_star["U"])
    print(fmt_root(f"{fam} ROOT", p_star, d_star, diag)
          + f"  [iters={its} conv={conv} shots={SHOTS['n']-n0}]")
    print(f"    Nd ladder(100k): {diag['Nd_ladder_100k']}")
    print(f"    Np ladder(100k): {diag['Np_ladder_100k']}")
    return p_star, d_star, diag

t0 = time.time()
res = {}

# A2: hints d~6.2e-3 (N=7), 5.9e-3 (N=8)
brs = hunt("A2", F_A2, np.array([5.75, 5.85, 5.95, 6.05, 6.15, 6.25, 6.35, 6.45]) * 1e-3)
for br in brs:
    p, d, diag = refine("A2", F_A2, br)
    res.setdefault("A2", []).append((p, d, diag))

# A3: hints d~8.3e-3 (N=7), 7.8e-3 (N=8)
brs = hunt("A3", F_A3, np.array([7.55, 7.70, 7.85, 8.00, 8.15, 8.30, 8.45, 8.60]) * 1e-3)
for br in brs:
    p, d, diag = refine("A3", F_A3, br)
    res.setdefault("A3", []).append((p, d, diag))

print(f"\nT2 shots this script={SHOTS['n']}  {time.time()-t0:.1f}s")

# cross-family spread using T1 (A1 m=2) values, read from file
t1 = json.load(open("bv7_t1_roots.json"))
a1 = {}
for r in t1:
    n = r["Nd"][1] if isinstance(r["Nd"], list) else r["Nd"]
    a1[n] = r["rho_s"]
summary = {"A1m2": a1}
for fam in ("A2", "A3"):
    for p, d, diag in res.get(fam, []):
        n = diag["Nd_100k"][1]
        summary.setdefault(fam, {})[n] = diag["rho_s"]
print("rho_s by family/N:", json.dumps({k: {str(n): v for n, v in vv.items()}
                                        for k, vv in summary.items()}, indent=1))
for N in (7, 8):
    vals = [summary[f][N] for f in ("A1m2", "A2", "A3") if N in summary.get(f, {})]
    if len(vals) == 3:
        spread = (max(vals) - min(vals)) / np.mean(vals)
        print(f"N={N}: rho_s = {[f'{v:.9f}' for v in vals]}  spread (max-min)/mean = {spread:.6e}")
    else:
        print(f"N={N}: INCOMPLETE ({len(vals)}/3 families)")
