import sys, json, time
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
from bv6_lib import g_of_a, SHOTS

# my own grid: log-spaced in d over [4.0e-3, 7.0e-3], ratio <= 1.01 -> Delta d/d <= 1%
nd = 58
d_grid = np.exp(np.linspace(np.log(7.0e-3), np.log(4.0e-3), nd))  # descending d = ascending a
ratio = np.exp(np.log(7.0e-3 / 4.0e-3) / (nd - 1))
print(f"grid: {nd} pts, d from {d_grid[0]:.4e} to {d_grid[-1]:.4e}, ratio={ratio:.6f} "
      f"(Delta d/d = {ratio-1:.4%})")

rows = []
t0 = time.time()
for d in d_grid:
    a = 1.5 * (1.0 - d)
    g, o = g_of_a(a)
    row = {"d": float(d), "a": float(a), "g": g, "status": o["status"]}
    if o["status"] == "seal":
        phi_s, phip_s, rho_s, rhop_s = [float(v) for v in o["y_s"]]
        row.update(r_s=o["r_s"], rho_s=rho_s, q=8.0 * rho_s ** 2 * phip_s)
    rows.append(row)
    print(f"d={d:.5e} a={a:.8f} status={o['status']:8s} g={g:+.6e}" +
          (f" rho_s={row['rho_s']:.5f}" if o['status'] == 'seal' else ""))

print(f"time {time.time()-t0:.1f}s shots={SHOTS['n']}")
json.dump({"rows": rows, "shots": SHOTS["n"], "grid_ratio": ratio},
          open("bv6_c1_sweep.json", "w"), indent=1)

# sign changes + |g| dip detector (local minima of |g| much smaller than neighbors, no sign change)
gs = [r["g"] for r in rows]
print("\nsign changes (brackets):")
for i in range(len(rows) - 1):
    g1, g2 = gs[i], gs[i + 1]
    if np.isfinite(g1) and np.isfinite(g2) and g1 * g2 < 0:
        print(f"  [{rows[i]['a']:.8f}, {rows[i+1]['a']:.8f}]  d~[{rows[i+1]['d']:.4e},{rows[i]['d']:.4e}] g: {g1:+.3e} -> {g2:+.3e}")
print("\n|g| dip candidates (no sign change, |g| < 0.2 * both neighbors):")
for i in range(1, len(rows) - 1):
    if all(np.isfinite(v) for v in (gs[i-1], gs[i], gs[i+1])):
        if abs(gs[i]) < 0.2 * abs(gs[i-1]) and abs(gs[i]) < 0.2 * abs(gs[i+1]) \
           and gs[i-1] * gs[i] > 0 and gs[i] * gs[i+1] > 0:
            print(f"  dip at a={rows[i]['a']:.8f} d={rows[i]['d']:.4e} |g|={abs(gs[i]):.3e} "
                  f"(nbrs {abs(gs[i-1]):.3e}, {abs(gs[i+1]):.3e})")
