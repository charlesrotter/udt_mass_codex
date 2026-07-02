import sys, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
from bv6_lib import g_of_a, illinois, diagnose, SHOTS

results = {}
t0 = time.time()
for label, (alo, ahi), npts in (("N13", (1.4953, 1.4956), 9),
                                ("N20", (1.4965, 1.4967), 9)):
    print(f"--- bracket {label}: [{alo},{ahi}] scan {npts} pts")
    grid = np.linspace(alo, ahi, npts)
    gs = []
    for a in grid:
        g, o = g_of_a(a)
        gs.append(g)
        print(f"  a={a:.8f} status={o['status']:8s} g={g:+.6e}"
              + (f" rho_s={float(o['y_s'][2]):.5f}" if o["status"] == "seal" else ""))
    roots = []
    for i in range(npts - 1):
        if np.isfinite(gs[i]) and np.isfinite(gs[i + 1]) and gs[i] * gs[i + 1] < 0:
            astar, gstar, w, obest, nev = illinois(grid[i], grid[i + 1], gs[i], gs[i + 1],
                                                   xtol=1e-11)
            d = diagnose(obest, nsamp=40001)
            d.update(a_star=astar, g_star=gstar, bracket_width=w, n_evals=nev,
                     d_val=1.0 - astar / 1.5)
            roots.append(d)
            c1, c2 = d["counts"]["1x"], d["counts"]["2x"]
            print(f"  ROOT a*={astar:.11f} d={d['d_val']:.6e} |g*|={gstar:.2e} w={w:.1e} nev={nev}")
            print(f"     N_delta 1x/2x = {c1['N_delta']}/{c2['N_delta']}  ladders {c1['N_delta_counts']} | {c2['N_delta_counts']}")
            print(f"     N_rhop  1x/2x = {c1['N_rhop']}/{c2['N_rhop']}  ladders {c1['N_rhop_counts']} | {c2['N_rhop_counts']}")
            print(f"     rho_s={d['rho_s']:.8f} q={d['q']:.8f} r_s={d['r_s']:.6f} L={d['L_proper']:.6f} chi={d['chi']:.6f}")
            print(f"     dphi_dev={d['dphi_dev']:+.3e} 2m/rho-1={d['two_m_over_rho_dev']:+.3e} H_drift={d['H_drift']:.3e}")
    results[label] = roots

print(f"\ntime {time.time()-t0:.1f}s shots(this proc)={SHOTS['n']}")
json.dump({k: [{kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv)
                for kk, vv in r.items() if kk != "sols"} for r in v]
           for k, v in results.items()} | {"shots_this_proc": SHOTS["n"]},
          open("bv6_c2_roots.json", "w"), indent=1, default=str)
