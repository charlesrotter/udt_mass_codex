"""Q3 part 3: brentq the FIRST root (smallest-a sign change) per Z, plus one later root
(cascade member) and the first a>1 root. Then: smoothness table around a*, stability of a*
vs rtol and method. Full seal diagnostics at each root."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_risefall_slice, shoot

NEV = {'n': 0}
def missval(a, Z, rtol=1e-11, method='DOP853'):
    NEV['n'] += 1
    U, Up, _ = make_risefall_slice(a)
    o = shoot(U, Up, Z, rtol=rtol, atol=rtol*1e-2, r_max=60000.0, method=method)
    if o['status'] != 'seal':
        raise RuntimeError(f"a={a}: {o['status']}")
    return o['miss']

def diagnose(a, Z, rtol=1e-13):
    U, Up, tag = make_risefall_slice(a)
    o = shoot(U, Up, Z, rtol=rtol, atol=1e-15, r_max=60000.0)
    phi_s, phip_s, rho_s, rhop_s = o['y_s']
    q = Z * rho_s**2 * phip_s
    m_c = 0.5 * 1.0 * (1.0 - np.exp(-2*(-np.log(1101.0))) * 0.0**2)   # rho'=0 at core
    m_s = 0.5 * rho_s * (1.0 - np.exp(-2*phi_s) * rhop_s**2)
    print(f"  a*={a:.12f} Z={Z}: r_s={o['r_s']:.8f} rho_s={rho_s:.10f} "
          f"phi'_s={phip_s:+.10f}")
    print(f"    miss(rho'_s)={rhop_s:+.3e}  q={q:.10f}  2*rho_s*sqrtZ={2*rho_s*np.sqrt(Z):.10f}"
          f"  q/(2 rho_s sqrtZ)={q/(2*rho_s*np.sqrt(Z)):.6f}")
    print(f"    U(rho_s)={U(rho_s):.10f}  H-check q^2/(2Z rho_s^2)+U-2="
          f"{q**2/(2*Z*rho_s**2) + U(rho_s) - 2:+.2e}  Hdrift={o['Hdrift']:.1e}")
    print(f"    2m/rho core={2*m_c/1.0:.12f}  seal={2*m_s/rho_s:.12f}")
    return o

roots = {}
for Z, brk in ((1.0, (0.9958, 0.9963)), (8.0, (0.986, 0.988))):
    NEV['n'] = 0
    astar = brentq(missval, *brk, args=(Z,), xtol=1e-13, rtol=8.9e-16)
    roots[Z] = astar
    print(f"== Z={Z} FIRST root: a* = {astar:.13f}  ({NEV['n']} evals) ==")
    diagnose(astar, Z)

print("\n== later cascade roots (existence demo, moderate precision) ==")
for Z, brk, label in ((1.0, (0.9982, 0.9986), '2nd-ish a<1'),
                      (1.0, (1.001, 1.002),  'first a>1'),
                      (8.0, (0.9950, 0.9954), 'later a<1'),
                      (8.0, (1.002, 1.004),  'first a>1 bracket')):
    try:
        astar = brentq(missval, *brk, args=(Z,), xtol=1e-12)
        U, Up, _ = make_risefall_slice(astar)
        o = shoot(U, Up, Z, rtol=1e-12, atol=1e-14, r_max=60000.0)
        print(f" Z={Z} {label:18s}: a*={astar:.10f} rho_s={o['y_s'][2]:.6f} "
              f"r_s={o['r_s']:.4f} q={Z*o['y_s'][2]**2*o['y_s'][1]:.6f}")
    except ValueError as e:
        print(f" Z={Z} {label:18s}: no sign change in bracket ({e})")

print("\n== smoothness: miss(a) around the first roots ==")
for Z in (1.0, 8.0):
    astar = roots[Z]
    for d in (-3e-4, -1e-4, -3e-5, -1e-5, 0.0, 1e-5, 3e-5, 1e-4, 3e-4):
        m = missval(astar + d, Z)
        print(f" Z={Z} a*-a={-d:+.1e}: miss={m:+.9e}")

print("\n== stability of a* vs rtol and method (re-bisect) ==")
for Z, brk in ((1.0, (0.9958, 0.9963)), (8.0, (0.986, 0.988))):
    for rtol, meth in ((1e-8, 'DOP853'), (1e-10, 'DOP853'), (1e-12, 'DOP853'),
                       (1e-11, 'Radau')):
        astar = brentq(missval, *brk, args=(Z, rtol, meth), xtol=1e-13, rtol=8.9e-16)
        print(f" Z={Z} {meth} rtol={rtol:.0e}: a* = {astar:.13f}")
