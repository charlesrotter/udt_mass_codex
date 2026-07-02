import time, numpy as np
import sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from bv7_core import *

# 1) own root-finder vs analytic root of cos(x)-x (no IVP shots)
F = lambda x: (np.cos(x) - x, None)
x, f, _, it, conv = bracket_root(F, 0.0, 1.5, F(0.0)[0], F(1.5)[0], xtol=1e-13)
print(f"[rootfinder] x*={x:.15f} (exact 0.739085133215161) f={f:.2e} iters={it} conv={conv}")

# 2) null: U=const => sigma=0 => phi frozen at -ln(1101) => must be no-seal
t0 = time.time()
out = shoot(8.0, lambda rho: 0.0 * rho, r_cap=2.0e3)
print(f"[null U=const] status={out['status']} (expect no-seal)  {time.time()-t0:.1f}s")

# 3) timed probe: A1 m=2, Z=8, d=5.0e-3 (a=0.995)
U, Up, _ = make_risefall_slice(0.995, m=2.0)
t0 = time.time()
out = shoot(8.0, Up)
dt = time.time() - t0
print(f"[probe d=5e-3] status={out['status']}", end=" ")
if out["status"] == "seal":
    print(f"r_s={out['r_s']:.4f} rho_s={out['rho_s']:.7f} rhop_s={out['rhop_s']:+.4e} q={out['q']:.5f}", end=" ")
print(f" {dt:.1f}s  shots={SHOTS['n']}")
