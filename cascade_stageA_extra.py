"""(1) zero-counter sanity on one root: list actual zero POSITIONS of delta=rho-1
and rho' (must be distinct, interlacing sets -- guards against a counting bug).
(2) reduced A1 m=1 Z=8: scan + FIRST root only (full verify), rest cut (budget)."""
import sys, json
import numpy as np
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from stageA_lib import (miss_at, SHOTS, precheck, coarse_grid, scan, find_brackets,
                        refine_root, verify_root, diagnose_root)

SHOTS["n"] = 544  # carry ledger forward (537 run + 7 sanity)

# ---- (1) zero-position sanity at A1 m=3 Z=8 root1 (Nd=Nrp=5 reported)
p1 = 1.4928689011
f, o = miss_at(("A1", 3.0), 8.0, p1, dense=True)
rr = np.linspace(o["r_s"] * 1e-6, o["r_s"] * (1 - 1e-6), 60001)
phi, phip, rho, rhop = o["sol"].sol(rr)
def zero_pos(v):
    amp = np.max(np.abs(v)); tau = 1e-8 * amp
    mask = np.abs(v) > tau
    r, vv = rr[mask], v[mask]
    s = np.sign(vv)
    idx = np.where(s[1:] != s[:-1])[0]
    return r[idx]
zd, zp = zero_pos(rho - 1.0), zero_pos(rhop)
print("delta zeros :", np.round(zd, 2))
print("rho'  zeros :", np.round(zp, 2))
merged = sorted([(z, 'd') for z in zd] + [(z, 'p') for z in zp])
print("interleave  :", "".join(t for _, t in merged))

# ---- (2) reduced A1 m=1 Z=8
family, Z, stuck, label = ("A1", 1.0), 8.0, 0.5, "A1 m=1 Z=8 (REDUCED)"
rec = {"family": list(family), "Z": Z, "stuck": stuck, "precheck": precheck(family, stuck)}
grid = coarse_grid(stuck)
rows = scan(family, Z, grid)
rec["scan"] = rows
br, trans = find_brackets(rows)
below = sorted([b for b in br if 0.5 * (b[0] + b[1]) < stuck],
               key=lambda b: abs(0.5 * (b[0] + b[1]) - stuck), reverse=True)
rec["brackets_below"] = below
rec["brackets_above_unrefined"] = [b for b in br if 0.5 * (b[0] + b[1]) >= stuck]
rec["status_transitions"] = trans
roots = []
if below:
    lo, hi = below[0]
    p_star, ncalls = refine_root(family, Z, lo, hi, xtol=1e-10)
    if p_star is not None:
        ver = verify_root(family, Z, p_star, stuck)
        f, o = miss_at(family, Z, p_star, dense=True)
        diag = diagnose_root(o, Z) if o["status"] == "seal" else {"status": o["status"]}
        roots.append({"p_star": p_star, "brentq_calls": ncalls,
                      "one_minus_p_over_stuck": 1.0 - p_star / stuck,
                      "verify": ver, "diag": diag})
rec["roots"] = roots
rec["roots_cut_note"] = "roots 2..N unrefined -- shot-budget-limited"

res = json.load(open("stageA_results.json"))
res["combos"][label] = rec
res["shot_ledger"][label] = None
res["total_shots_final"] = SHOTS["n"]
json.dump(res, open("stageA_results.json", "w"), indent=1, default=float)
print("\n[m=1 Z=8] brackets_below:", below)
print("above:", rec["brackets_above_unrefined"], "transitions:", trans)
for rt in roots:
    d, v = rt["diag"], rt["verify"]
    print(f"root0: p*={rt['p_star']:.10f} conf={v['confirmed']} rel={v['rel_diffs']}")
    print(f"  q={d['q']:.8g} rho_s={d['rho_s']:.8g} r_s={d['r_s']:.6g} L={d['L_proper']:.6g} "
          f"chi={d['chi']:.5g} Nd={d['N_delta']} Nrp={d['N_rhop']} Hdrift={d['H_drift_max']:.2e}")
print("TOTAL SHOTS (incl. prior 544):", SHOTS["n"])
