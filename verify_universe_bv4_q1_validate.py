"""Q1: validate my shooter. Test case: risefall m=2 a=0.9, Z=1 and Z=8.
Checks: H-drift; rtol sensitivity (1e-8/1e-11/1e-13); method DOP853 vs Radau vs RK4;
r_max sensitivity (does the answer depend on the box?)."""
import sys, numpy as np
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_risefall_slice, shoot, rk4_shoot, Hfun

for Z in (1.0, 8.0):
    U, Up, tag = make_risefall_slice(0.9)
    print(f"=== {tag}  Z={Z} ===")
    for rtol in (1e-8, 1e-11, 1e-13):
        o = shoot(U, Up, Z, rtol=rtol, atol=rtol*1e-2)
        print(f" DOP853 rtol={rtol:.0e}: status={o['status']:8s} r_s={o.get('r_s'):.10g} "
              f"miss=rho'_s={o['miss']:+.12g} rho_s={o['y_s'][2]:.10g} "
              f"phi'_s={o['y_s'][1]:+.10g} Hdrift={o['Hdrift']:.2e}")
    o = shoot(U, Up, Z, rtol=1e-11, atol=1e-13, method='Radau')
    print(f" Radau  rtol=1e-11 : status={o['status']:8s} r_s={o.get('r_s'):.10g} "
          f"miss={o['miss']:+.12g} rho_s={o['y_s'][2]:.10g} Hdrift={o['Hdrift']:.2e}")
    # r_max sensitivity: seal is an event, so r_max should be irrelevant once past r_s
    for rmax in (200.0, 1000.0, 5000.0):
        o = shoot(U, Up, Z, r_max=rmax, rtol=1e-11, atol=1e-13)
        print(f" r_max={rmax:6g}    : status={o['status']:8s} r_s={o.get('r_s'):.10g} "
              f"miss={o['miss']:+.12g}")
    # hand-rolled RK4
    o = rk4_shoot(U, Up, Z, h=0.005)
    print(f" RK4 h=0.005      : status={o['status']:8s} r_s={o.get('r_s'):.10g} "
          f"miss={o['miss']:+.12g} Hdrift={o.get('Hdrift', np.nan):.2e}")
