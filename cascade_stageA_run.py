"""stageA_run.py -- execute the Stage A survey in priority order, budget-ledgered.
Per (family, Z): coarse scan -> brackets -> refine up to 3 below-stuck roots
(farthest-first) -> two-method verify each -> dense diagnostic shot -> JSON."""
import sys, json, time
import numpy as np
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from stageA_lib import (miss_at, SHOTS, precheck, coarse_grid, scan, find_brackets,
                        refine_root, verify_root, diagnose_root)
from scipy.optimize import brentq

BUDGET_STOP_NEW_COMBO = 520   # do not START a new combo past this many shots
OUT = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad/stageA_results.json"

COMBOS = [  # (family, Z, stuck, label) in prompt priority order
    (("A1", 3.0), 8.0, 1.5,        "A1 m=3 Z=8"),
    (("A1", 3.0), 1.0, 1.5,        "A1 m=3 Z=1"),
    (("A2", 1.0), 8.0, 2.0,        "A2 k=1 Z=8"),
    (("A3",),     8.0, 1.0,        "A3 Z=8"),
    (("A1", 4.0), 8.0, 2.0,        "A1 m=4 Z=8"),
    (("A2", 3.0), 8.0, 2.0 / 3.0,  "A2 k=3 Z=8"),
    (("A1", 1.0), 8.0, 0.5,        "A1 m=1 Z=8"),
    (("A2", 1.0), 1.0, 2.0,        "A2 k=1 Z=1"),
    (("A3",),     1.0, 1.0,        "A3 Z=1"),
    (("A1", 4.0), 1.0, 2.0,        "A1 m=4 Z=1"),
    (("A2", 3.0), 1.0, 2.0 / 3.0,  "A2 k=3 Z=1"),
    (("A1", 1.0), 1.0, 0.5,        "A1 m=1 Z=1"),
]

results = {"combos": {}, "cut": [], "shot_ledger": {}}
t_all = time.time()

for family, Z, stuck, label in COMBOS:
    if SHOTS["n"] > BUDGET_STOP_NEW_COMBO:
        results["cut"].append(label)
        continue
    t0, s0 = time.time(), SHOTS["n"]
    rec = {"family": list(family), "Z": Z, "stuck": stuck,
           "precheck": precheck(family, stuck)}

    above = (0.0015, 0.004, 0.012, 0.035, 0.1, 0.3, 1.0) if family[0] == "A3" \
            else (0.0015, 0.004, 0.012, 0.035, 0.1)
    grid = coarse_grid(stuck, above=above)
    rows = scan(family, Z, grid)
    rec["scan"] = rows
    br, trans = find_brackets(rows)
    rec["status_transitions"] = trans

    below = sorted([b for b in br if 0.5 * (b[0] + b[1]) < stuck],
                   key=lambda b: abs(0.5 * (b[0] + b[1]) - stuck), reverse=True)
    above_br = [b for b in br if 0.5 * (b[0] + b[1]) >= stuck]
    rec["brackets_below"] = below
    rec["brackets_above_unrefined"] = above_br

    roots = []
    for lo, hi in below[:3]:
        p_star, ncalls = refine_root(family, Z, lo, hi, xtol=1e-10)
        if p_star is None:
            roots.append({"bracket": [lo, hi], "FAILED": ncalls}); continue
        ver = verify_root(family, Z, p_star, stuck)
        f, o = miss_at(family, Z, p_star, dense=True)
        diag = diagnose_root(o, Z) if o["status"] == "seal" else {"status": o["status"]}
        roots.append({"p_star": p_star, "brentq_calls": ncalls,
                      "one_minus_p_over_stuck": 1.0 - p_star / stuck,
                      "verify": ver, "diag": diag})
    rec["roots"] = roots
    rec["shots_used"] = SHOTS["n"] - s0
    rec["wall_s"] = round(time.time() - t0, 2)
    results["combos"][label] = rec
    results["shot_ledger"][label] = rec["shots_used"]
    print(f"[{label}] shots={rec['shots_used']} total={SHOTS['n']} "
          f"brackets_below={len(below)} refined={len(roots)} "
          f"({rec['wall_s']}s)", flush=True)
    with open(OUT, "w") as fh:
        json.dump(results, fh, indent=1, default=float)

results["total_shots"] = SHOTS["n"]
results["total_wall_s"] = round(time.time() - t_all, 1)
with open(OUT, "w") as fh:
    json.dump(results, fh, indent=1, default=float)
print("DONE total shots:", SHOTS["n"], " wall:", results["total_wall_s"], "s")
print("cut (throughput/budget-limited):", results["cut"])
