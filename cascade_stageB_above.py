"""Stage B above-stuck side: coarse pass a in (1.5, 1.52], geometric in d' = a/1.5 - 1
from 1.3333e-2 down to 2e-4 (30 pts); bisect the first 3 brackets (largest d' first);
same per-rung characterization. Output: stageB_above.json"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from stageB_common import characterize   # reuse the graded counter/characterizer

Z, M = 8.0, 3.0
SCR = "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad"
SHOTS = 0

def f_of_dp(dp):
    global SHOTS
    a = 1.5 * (1.0 + dp)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0)
    return f, o, U

t0 = time.time()
dp_grid = np.geomspace(2.0/1.5*1e-2, 2e-4, 30)   # a from 1.52 down toward 1.5003
rows = []
for dp in dp_grid:
    f, o, _ = f_of_dp(float(dp))
    rows.append((float(dp), float(f) if np.isfinite(f) else None, o["status"]))
    print(f"d'={dp:.6e}  a={1.5*(1+dp):.8f}  f={f if np.isfinite(f) else float('nan'):+.4e}  [{o['status']}]")

br = []
for (d1, f1, s1), (d2, f2, s2) in zip(rows, rows[1:]):
    if s1 == s2 == "seal" and f1 is not None and f2 is not None and f1 * f2 < 0:
        br.append((d1, d2))
print(f"\nabove-stuck brackets found: {len(br)}")
for b in br: print(f"  d' in ({b[0]:.6e}, {b[1]:.6e})  a in ({1.5*(1+b[0]):.8f}, {1.5*(1+b[1]):.8f})")

rowmap = {r[0]: r[1] for r in rows}
rungs = []
for bi, (dp_hi, dp_lo) in enumerate(br[:3]):
    fhi = rowmap[dp_hi]
    lo, hi = dp_lo, dp_hi
    steps = 0
    while (hi - lo) > 1.0e-8 and steps < 18:
        mid = 0.5 * (lo + hi)
        fm, om, Um = f_of_dp(mid)
        steps += 1
        if not np.isfinite(fm): break
        if fhi * fm < 0: lo = mid
        else: hi, fhi = mid, fm
    dp_star = 0.5 * (lo + hi)
    fm, om, Um = f_of_dp(dp_star); steps += 1
    a_star = 1.5 * (1.0 + dp_star)
    if om["status"] == "seal":
        ch = characterize(om, Um)
        ch2 = characterize(om, Um, npts=200001)
        ch["N_delta_recheck200k"] = ch2["N_delta"]; ch["N_rhop_recheck200k"] = ch2["N_rhop"]
    else:
        ch = {"status": om["status"]}
    rung = {"bracket_index": bi, "dp_bracket": [dp_hi, dp_lo], "dp_star": dp_star,
            "a_star": a_star, "bisect_steps": steps, **ch}
    rungs.append(rung)
    print(f"[above {bi}] a*={a_star:.10f} d'={dp_star:.6e} steps={steps} "
          f"N_delta={ch.get('N_delta')} N_rhop={ch.get('N_rhop')} "
          f"(200k: {ch.get('N_delta_recheck200k')},{ch.get('N_rhop_recheck200k')}) "
          f"q={ch.get('q', float('nan')):.5f} rho_s={ch.get('rho_s', float('nan')):.5f} "
          f"L={ch.get('L_proper', float('nan')):.4f} chi={ch.get('chi', float('nan')):.4f} "
          f"Hd={ch.get('H_drift', float('nan')):.1e} dphi={ch.get('dphi_carried', float('nan')):.6f} "
          f"ms={ch.get('ms_seal_2m_over_rho', float('nan')):.6f}")

json.dump({"rows": rows, "brackets": br,
           "rungs": [{k: v for k, v in r.items() if 'profile' not in k} for r in rungs],
           "shots_this_script": SHOTS},
          open(f"{SCR}/stageB_above.json", "w"), indent=1)
print(f"\nshots this script = {SHOTS}, wall = {time.time()-t0:.1f}s")
