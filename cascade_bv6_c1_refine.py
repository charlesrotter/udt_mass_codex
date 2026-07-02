import sys, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
from bv6_lib import g_of_a, illinois, diagnose, SHOTS

sw = json.load(open("bv6_c1_sweep.json"))
rows = sw["rows"]
brackets = []
for r1, r2 in zip(rows, rows[1:]):
    g1, g2 = r1["g"], r2["g"]
    if np.isfinite(g1) and np.isfinite(g2) and g1 * g2 < 0:
        brackets.append((r1["a"], r2["a"], g1, g2))

print(f"{len(brackets)} brackets to refine")
out = []
t0 = time.time()
for (a1, a2, g1, g2) in brackets:
    astar, gstar, width, obest, nev = illinois(a1, a2, g1, g2, xtol=1e-11)
    d = diagnose(obest)
    d.update(a_star=astar, g_star=gstar, bracket_width=width, n_evals=nev,
             d_val=1.0 - astar / 1.5)
    d.pop("counts_raw", None)
    out.append(d)
    c1, c2 = d["counts"]["1x"], d["counts"]["2x"]
    print(f"a*={astar:.11f} d={d['d_val']:.6e} |g*|={gstar:.2e} w={width:.1e} nev={nev}")
    print(f"   N_delta: 1x={c1['N_delta']} 2x={c2['N_delta']}  ladders {c1['N_delta_counts']} | {c2['N_delta_counts']}")
    print(f"   N_rhop : 1x={c1['N_rhop']} 2x={c2['N_rhop']}  ladders {c1['N_rhop_counts']} | {c2['N_rhop_counts']}")
    print(f"   rho_s={d['rho_s']:.8f} q={d['q']:.8f} r_s={d['r_s']:.6f} L={d['L_proper']:.6f} chi={d['chi']:.6f}")
    print(f"   dphi_dev={d['dphi_dev']:+.3e} 2m/rho-1={d['two_m_over_rho_dev']:+.3e} H_drift={d['H_drift']:.3e}")

print(f"\ntime {time.time()-t0:.1f}s shots(this proc)={SHOTS['n']}")


def clean(o):
    return {k: v for k, v in o.items() if k != "sols"}


json.dump({"roots": [{k: (v if not isinstance(v, np.ndarray) else v.tolist())
                      for k, v in r.items()} for r in out],
           "shots_this_proc": SHOTS["n"]},
          open("bv6_c1_roots.json", "w"), indent=1, default=str)
