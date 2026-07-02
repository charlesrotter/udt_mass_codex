"""Q3 part 2: fine scan near a=1 (map structure, count sign changes) + brentq the roots
to high precision. Then stability: a* vs rtol and vs method."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_risefall_slice, shoot

def miss(a, Z, rtol=1e-11, method='DOP853'):
    U, Up, _ = make_risefall_slice(a)
    o = shoot(U, Up, Z, rtol=rtol, atol=rtol*1e-2, r_max=60000.0, method=method)
    return o

print("== fine scan a in [0.984, 1.006] ==")
for Z in (1.0, 8.0):
    print(f" Z={Z}:")
    for a in np.arange(0.984, 1.0061, 0.002):
        if abs(a - 1.0) < 1e-9: continue
        o = miss(a, Z)
        if o['status'] == 'seal':
            print(f"  a={a:8.5f}: miss={o['miss']:+.6g}  rho_s={o['y_s'][2]:.6g} "
                  f"r_s={o['r_s']:.6g}")
        else:
            print(f"  a={a:8.5f}: {o['status']}")

print("\n== extra-fine scan a in [0.9950, 0.9998] (hunt multiple crossings) ==")
for Z in (1.0, 8.0):
    print(f" Z={Z}:")
    prev = None
    for a in np.arange(0.995, 0.99981, 0.0004):
        o = miss(a, Z)
        s = np.sign(o['miss']) if o['status'] == 'seal' else 0
        mark = ' <-- SIGN CHANGE' if (prev is not None and s != 0 and prev != 0 and s != prev) else ''
        print(f"  a={a:8.5f}: miss={o['miss']:+.6g} rho_s={o['y_s'][2]:.6g}{mark}")
        prev = s
