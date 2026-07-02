"""Q3 part 1: scan miss(a) = rho'(r_s) for risefall m=2, a in [0.80, 0.999] + a>1 side,
Z in {1, 8}. Look for sign changes vs asymptotic approach to 0 at a->1."""
import sys, numpy as np
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_risefall_slice, shoot

grids = {
    'main [0.8,1)': [0.80, 0.84, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 0.99, 0.995, 0.999],
    'low  [0,0.8)': [0.0, 0.2, 0.4, 0.6, 0.7],
    'high (1,1.2]': [1.001, 1.01, 1.05, 1.1, 1.2],
}
for Z in (1.0, 8.0):
    print(f"===== Z={Z} =====")
    for gname, grid in grids.items():
        print(f" -- {gname} --")
        for a in grid:
            U, Up, tag = make_risefall_slice(a)
            o = shoot(U, Up, Z, rtol=1e-11, atol=1e-13, r_max=20000.0)
            if o['status'] == 'seal':
                print(f"  a={a:7.4f}: seal r_s={o['r_s']:12.6g} miss={o['miss']:+.9g} "
                      f"rho_s={o['y_s'][2]:.9g} phi'_s={o['y_s'][1]:+.6g} Hd={o['Hdrift']:.0e}")
            else:
                ye = o['y_end']
                print(f"  a={a:7.4f}: {o['status']:8s} r_end={o['r_end']:.6g} "
                      f"phi_end={ye[0]:+.5g} rho_end={ye[2]:.6g} rho'_end={ye[3]:+.4g}")
