"""Stage D SURVEY sweep — pass 1 scan. Family A1 m=3, Z=8, rho_c=1 gauge, below-stuck side.
Window: d in (1.30e-3, 2.30e-3), d = 1 - a/1.5 (Stage-B family coordinate).
Dense geometric grid (Delta d/d ~ 0.05%), miss f = rho'(r_s) per point.
Brackets = consecutive seal-seal sign changes. Dip detector: local |f| minima WITHOUT a sign
change whose |f| is anomalously small vs neighbors (possible even-multiplicity pair / aliased
cluster) -> flagged for subdivision in the refine pass. Failed/no-seal points recorded verbatim.
SINGLE process, bounded. Output: stageD_scan_pass1.json (repo dir).
"""
import sys, json, time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice, miss

Z, M = 8.0, 3.0
D_HI, D_LO = 2.30e-3, 1.30e-3
NPTS = 1201                      # Delta d/d ~ 0.0476% per step (CHOSE, conditioning)
SHOTS = 0

def f_of_d(d):
    global SHOTS
    a = 1.5 * (1.0 - d)
    U, Up, _ = make_risefall_slice(a, m=M)
    SHOTS += 1
    f, o = miss(Z, U, Up, 1.0)
    return (float(f) if np.isfinite(f) else None), o["status"]

t0 = time.time()
d_grid = np.geomspace(D_HI, D_LO, NPTS)      # descending in d
rows = []
for i, d in enumerate(d_grid):
    f, s = f_of_d(float(d))
    rows.append((float(d), f, s))
    if i % 200 == 0:
        print(f"  [{i:4d}/{NPTS}] d={d:.6e} f={f if f is not None else float('nan'):+.4e} [{s}] "
              f"shots={SHOTS} wall={time.time()-t0:.1f}s", flush=True)

# ---- brackets (seal-seal sign changes)
brackets = []
for (d1, f1, s1), (d2, f2, s2) in zip(rows, rows[1:]):
    if s1 == s2 == "seal" and f1 is not None and f2 is not None and f1 * f2 < 0:
        brackets.append((d1, d2))

# ---- failures / non-seal statuses
fails = [(d, s) for (d, f, s) in rows if s != "seal"]

# ---- dip detector: interior |f| local minima with NO sign change against neighbors,
#      where the dip is deep (min|f| < 0.05 * geometric mean of flanking local maxima)
fa = np.array([r[1] if r[1] is not None else np.nan for r in rows])
dd = np.array([r[0] for r in rows])
dips = []
for i in range(2, len(fa) - 2):
    window = fa[i-2:i+3]
    if np.any(~np.isfinite(window)):
        continue
    if abs(fa[i]) < abs(fa[i-1]) and abs(fa[i]) < abs(fa[i+1]):
        # same sign across the local window (no bracket already found here)
        if np.all(np.sign(window) == np.sign(fa[i])):
            flank = max(abs(fa[i-2]), abs(fa[i+2]))
            if abs(fa[i]) < 0.05 * flank:
                dips.append((float(dd[i]), float(fa[i]), float(flank)))

print(f"\npass1: {len(brackets)} brackets, {len(fails)} non-seal points, {len(dips)} deep dips "
      f"(no-sign-change), shots={SHOTS}, wall={time.time()-t0:.1f}s")
for b in brackets:
    print(f"  bracket d in ({b[0]:.8e}, {b[1]:.8e})")
for d, s in fails:
    print(f"  NON-SEAL d={d:.8e} status={s}")
for d, fmin, flank in dips:
    print(f"  DIP d={d:.8e} |f|min={fmin:.3e} flank={flank:.3e}")

json.dump({"rows": rows, "brackets": brackets, "fails": fails, "dips": dips,
           "grid": [float(x) for x in d_grid], "shots": SHOTS,
           "window": [D_HI, D_LO], "npts": NPTS, "wall_s": time.time() - t0},
          open("/home/udt-admin/udt_mass_codex/stageD_scan_pass1.json", "w"), indent=1)
print("-> stageD_scan_pass1.json")
