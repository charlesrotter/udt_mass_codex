"""Sanity + timing: reproduce banked m=2 roots' miss~0; time typical shots."""
import time, numpy as np
import sys
sys.path.insert(0, "/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad")
from stageA_lib import miss_at, SHOTS, precheck

# banked (universe_cell_T3_closure_results.md): A1 m=2 == risefall m=2
for Z, a_star in ((1.0, 0.9961216584397), (8.0, 0.9860738233466)):
    t0 = time.time()
    f, o = miss_at(("A1", 2.0), Z, a_star)
    print(f"[banked m=2 Z={Z:g}] a*={a_star} status={o['status']} miss={f:+.3e} "
          f"rho_s={o.get('rho_s')} r_s={o.get('r_s')} q={o.get('q')}  ({time.time()-t0:.2f}s)")

# timing: far-from-stuck seal, near-stuck, and a no-seal probe
for lab, fam, Z, p in (("far", ("A1", 3.0), 8.0, 1.1),
                       ("near-stuck", ("A1", 3.0), 8.0, 1.497),
                       ("above", ("A1", 3.0), 8.0, 1.55),
                       ("A3 mid", ("A3",), 8.0, 0.7),
                       ("A2k1 far", ("A2", 1.0), 8.0, 1.6)):
    t0 = time.time()
    f, o = miss_at(fam, Z, p)
    print(f"[{lab}] p={p} status={o['status']} miss={f} rho_s={o.get('rho_s')} "
          f"r_s={o.get('r_s', o.get('r_coll'))}  ({time.time()-t0:.2f}s)")

print("prechecks:")
for fam, s in ((("A1", 1.0), 0.5), (("A1", 3.0), 1.5), (("A1", 4.0), 2.0),
               (("A2", 1.0), 2.0), (("A2", 3.0), 2.0 / 3.0), (("A3",), 1.0)):
    print(fam, "stuck=", s, precheck(fam, s))
print("shots used:", SHOTS["n"])
