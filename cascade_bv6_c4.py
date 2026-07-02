import sys, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
from bv6_lib import g_of_a, illinois, diagnose, SHOTS

t0 = time.time()
# --- twin-rung hunt: d' in [3.3e-3, 4.0e-3], a = 1.5*(1+d')
dp_grid = np.linspace(3.3e-3, 4.0e-3, 13)
gs = []
print("--- above-side scan d' in [3.3e-3, 4.0e-3] (13 pts, Delta a = %.2e)" %
      (1.5 * (dp_grid[1] - dp_grid[0])))
for dp in dp_grid:
    a = 1.5 * (1.0 + dp)
    g, o = g_of_a(a)
    gs.append(g)
    print(f"  d'={dp:.5e} a={a:.8f} status={o['status']:8s} g={g:+.6e}"
          + (f" rho_s={float(o['y_s'][2]):.5f}" if o["status"] == "seal" else ""))

roots = []
for i in range(len(dp_grid) - 1):
    if np.isfinite(gs[i]) and np.isfinite(gs[i + 1]) and gs[i] * gs[i + 1] < 0:
        a1, a2 = 1.5 * (1 + dp_grid[i]), 1.5 * (1 + dp_grid[i + 1])
        astar, gstar, w, obest, nev = illinois(a1, a2, gs[i], gs[i + 1], xtol=1e-11)
        d = diagnose(obest, nsamp=40001)
        d.update(a_star=astar, g_star=gstar, bracket_width=w, n_evals=nev,
                 dp_val=astar / 1.5 - 1.0)
        roots.append(d)
        c1, c2 = d["counts"]["1x"], d["counts"]["2x"]
        print(f"  ROOT a*={astar:.11f} d'={d['dp_val']:.6e} |g*|={gstar:.2e} w={w:.1e} nev={nev}")
        print(f"     N_delta 1x/2x = {c1['N_delta']}/{c2['N_delta']}  ladders {c1['N_delta_counts']} | {c2['N_delta_counts']}")
        print(f"     N_rhop  1x/2x = {c1['N_rhop']}/{c2['N_rhop']}  ladders {c1['N_rhop_counts']} | {c2['N_rhop_counts']}")
        print(f"     rho_s={d['rho_s']:.8f} q={d['q']:.8f} r_s={d['r_s']:.6f} L={d['L_proper']:.6f} chi={d['chi']:.6f}")
        print(f"     dphi_dev={d['dphi_dev']:+.3e} 2m/rho-1={d['two_m_over_rho_dev']:+.3e} H_drift={d['H_drift']:.3e}")

# --- far probe: d' in (8e-3, 1.4e-2], 14 log pts (ratio ~4.4%)
print("\n--- far probe d' in (8e-3, 1.4e-2], 14 log pts")
far = np.exp(np.linspace(np.log(8.0e-3), np.log(1.4e-2), 14))[1:]  # 13 pts strictly > 8e-3
far = np.exp(np.linspace(np.log(8.2e-3), np.log(1.4e-2), 13))
signs = []
for dp in far:
    a = 1.5 * (1.0 + dp)
    g, o = g_of_a(a)
    signs.append(g)
    print(f"  d'={dp:.5e} a={a:.8f} status={o['status']:8s} g={g:+.6e}"
          + (f" rho_s={float(o['y_s'][2]):.5f}" if o["status"] == "seal" else ""))
sc = sum(1 for x, y in zip(signs, signs[1:])
         if np.isfinite(x) and np.isfinite(y) and x * y < 0)
print(f"far-probe sign changes: {sc}")

print(f"\ntime {time.time()-t0:.1f}s shots(this proc)={SHOTS['n']}")
json.dump({"twin_roots": [{k: (v.tolist() if isinstance(v, np.ndarray) else v)
                           for k, v in r.items() if k != "sols"} for r in roots],
           "far_probe": [{"dp": float(dp), "g": float(g)} for dp, g in zip(far, signs)],
           "shots_this_proc": SHOTS["n"]},
          open("bv6_c4.json", "w"), indent=1, default=str)
