"""Q2: pure powers U=2 rho^n, n in {-2,-1,-0.1,0.1,1,2} (+ n=+-0.01 for the n->0 limit),
Z in {1,8}. Record rho'(r_s) sign, rho_s; compare to null-orbit values rho_c*exp(+-sqrt(Z)/2)."""
import sys, numpy as np
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_power_slice, shoot

for Z in (1.0, 8.0):
    rp, rm = np.exp(np.sqrt(Z)/2), np.exp(-np.sqrt(Z)/2)
    print(f"=== Z={Z}  null-orbit refs: e^{{+sqrtZ/2}}={rp:.9f}  e^{{-sqrtZ/2}}={rm:.9f} ===")
    for n in (-2.0, -1.0, -0.1, -0.01, 0.01, 0.1, 1.0, 2.0):
        U, Up, tag = make_power_slice(n)
        o = shoot(U, Up, Z, rtol=1e-11, atol=1e-13)
        if o['status'] == 'seal':
            rho_s, miss = o['y_s'][2], o['miss']
            ref = rp if miss > 0 else rm
            print(f" n={n:+6.2f}: seal r_s={o['r_s']:12.6g} rho'_s={miss:+.9g} "
                  f"rho_s={rho_s:.9f}  rho_s/ref={rho_s/ref:.9f}  Hdrift={o['Hdrift']:.1e}")
        else:
            print(f" n={n:+6.2f}: {o['status']} at r={o['r_s']:.6g} "
                  f"y_end(phi,rho)=({o['y_end'][0]:+.4g},{o['y_end'][2]:.4g}) "
                  f"Hdrift={o['Hdrift']:.1e}")
