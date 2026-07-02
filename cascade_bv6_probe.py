import time, sys, json
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
import numpy as np
from bv6_lib import shoot, g_of_a, SHOTS, diagnose

for a in (1.4903, 1.4955, 1.50555):
    t0 = time.time()
    g, o = g_of_a(a, keep_sols=True)
    dt = time.time() - t0
    print(f"a={a}: status={o['status']}", end=" ")
    if o["status"] == "seal":
        phi_s, phip_s, rho_s, rhop_s = o["y_s"]
        print(f"r_s={o['r_s']:.6g} rho_s={rho_s:.6g} rhop_s={rhop_s:+.4e} "
              f"phip_s={phip_s:.4e} phi_s={phi_s:+.2e} t={dt:.2f}s nchunks={len(o['sols'])}")
    else:
        print(f"t={dt:.2f}s")
print("shots:", SHOTS["n"])
