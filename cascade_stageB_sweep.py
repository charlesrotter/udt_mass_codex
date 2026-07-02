"""Stage B fine sweep, A1 m=3 Z=8, below-stuck side.
Geometric grid in d = 1 - a/1.5, d from 2e-2 down to 2e-4, 80 points.
Records miss f = rho'(r_s) per point; brackets = consecutive seal-seal sign changes.
One local refinement pass (4x subdivision) wherever two brackets are adjacent or
separated by one grid interval ("crowding"), plus around any non-seal statuses.
Shot counter kept. Output: stageB_sweep.json
"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss

Z, M = 8.0, 3.0
SHOTS = 0

def f_of_d(d, **kw):
    global SHOTS
    a = 1.5 * (1.0 - d)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0, **kw)
    return f, o["status"]

t0 = time.time()
# ---- pass 1: 80-point geometric grid, d descending from 2e-2 to 2e-4
d_grid = list(np.geomspace(2e-2, 2e-4, 80))
rows = []           # (d, f, status)
for d in d_grid:
    f, s = f_of_d(d)
    rows.append((float(d), float(f) if np.isfinite(f) else None, s))
    print(f"d={d:.6e}  a={1.5*(1-d):.8f}  f={f if np.isfinite(f) else float('nan'):+.4e}  [{s}]")

def find_brackets(rows):
    br = []
    for (d1, f1, s1), (d2, f2, s2) in zip(rows, rows[1:]):
        if s1 == s2 == "seal" and f1 is not None and f2 is not None and f1 * f2 < 0:
            br.append((d1, d2))
    return br

br1 = find_brackets(rows)
print(f"\npass1 brackets: {len(br1)}, shots={SHOTS}")
for b in br1: print(f"  ({b[0]:.6e}, {b[1]:.6e})")

# ---- refinement: subdivide 4x any grid interval that (a) holds a bracket AND has a
# neighboring interval that also holds a bracket within 1 step (crowding), or (b) borders
# a non-seal status. Also subdivide the last few intervals near d=2e-4 (accumulation end) 4x
# to look for crowding there.
rows_sorted = sorted(rows, key=lambda r: -r[0])   # d descending
crowd_idx = set()
br_idx = [i for i in range(len(rows_sorted)-1)
          if rows_sorted[i][2] == rows_sorted[i+1][2] == "seal"
          and rows_sorted[i][1] is not None and rows_sorted[i+1][1] is not None
          and rows_sorted[i][1]*rows_sorted[i+1][1] < 0]
for i, j in zip(br_idx, br_idx[1:]):
    if j - i <= 2:
        for k in range(i, j+1): crowd_idx.add(k)
for i, r in enumerate(rows_sorted):
    if r[2] != "seal":
        for k in (i-1, i):
            if 0 <= k < len(rows_sorted)-1: crowd_idx.add(k)
# accumulation tail: last 8 intervals
for k in range(max(0, len(rows_sorted)-9), len(rows_sorted)-1): crowd_idx.add(k)

new_rows = []
for k in sorted(crowd_idx):
    dhi, dlo = rows_sorted[k][0], rows_sorted[k+1][0]
    for d in np.geomspace(dhi, dlo, 6)[1:-1]:   # 4 interior points
        f, s = f_of_d(float(d))
        new_rows.append((float(d), float(f) if np.isfinite(f) else None, s))
print(f"refinement: {len(crowd_idx)} intervals subdivided, +{len(new_rows)} shots, total shots={SHOTS}")

all_rows = sorted(rows_sorted + new_rows, key=lambda r: -r[0])
br2 = find_brackets(all_rows)
print(f"\nfinal brackets: {len(br2)}")
for b in br2: print(f"  d in ({b[0]:.6e}, {b[1]:.6e})  a in ({1.5*(1-b[0]):.8f}, {1.5*(1-b[1]):.8f})")

json.dump({"rows": all_rows, "brackets": br2, "shots": SHOTS,
           "pass1_grid": [float(x) for x in d_grid],
           "wall_s": time.time()-t0},
          open("/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad/stageB_sweep.json","w"), indent=1)
print(f"\nshots={SHOTS} wall={time.time()-t0:.1f}s -> stageB_sweep.json")
