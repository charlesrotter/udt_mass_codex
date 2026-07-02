"""Q4: profile readings (8pi*eps, 8pi*p_r, U) along the first-root solutions.
Q5: homothety test rho_c=3 at the Z=1 first root.
Plus: Z=8 first a>1 root (correct bracket) and hand-rolled RK4 sign check at a*+-1e-5."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, '/tmp/claude-1000/-home-udt-admin-udt-mass-codex/749e82df-e440-4596-af14-d52dfbde5fed/scratchpad')
from bv4_shoot import make_risefall_slice, shoot, rk4_shoot

ASTAR = {1.0: 0.9961216584397, 8.0: 0.9860738233466}

print("== Q4: profiles at the first roots ==")
for Z in (1.0, 8.0):
    a = ASTAR[Z]
    U, Up, _ = make_risefall_slice(a)
    o = shoot(U, Up, Z, rtol=1e-12, atol=1e-14, r_max=60000.0)
    sol, rs = o['sol'], o['r_s']
    rr = np.linspace(0.0, rs, 4001)
    phi, phip, rho, rhop = sol.sol(rr)
    e2m = np.exp(-2.0*phi)
    eps8 = 1.0/rho**2 - e2m*(rhop**2/rho**2 + 2.0*phip*rhop/rho) + 0.5*Z*phip**2 \
           - Up(rho)/(2.0*rho)          # 2 e^{-2phi} sigma / rho = U'/(2 rho)
    pr8  = e2m*(rhop**2/rho**2 - 2.0*phip*rhop/rho) - 1.0/rho**2
    Uv   = U(rho)
    sgn = np.sign(eps8); ncross = int(np.sum(sgn[1:]*sgn[:-1] < 0))
    print(f" Z={Z} a*={a}:")
    print(f"  8pi*eps: at core={eps8[0]:+.9g}  at seal={eps8[-1]:+.9g}  "
          f"min={eps8.min():+.9g}@r={rr[eps8.argmin()]:.4g}  max={eps8.max():+.9g}@r={rr[eps8.argmax()]:.4g}  sign-changes={ncross}")
    if ncross:
        idx = np.where(sgn[1:]*sgn[:-1] < 0)[0]
        print(f"   eps=0 crossings at r ~ {[f'{rr[i]:.5g}' for i in idx]}  (r_s={rs:.5g})")
    print(f"  8pi*p_r: at core={pr8[0]:+.9g}  at seal={pr8[-1]:+.9g}  "
          f"min={pr8.min():+.9g}  max={pr8.max():+.9g}")
    print(f"  U: min={Uv.min():.9g}  max={Uv.max():.9g}  (>0 everywhere: {bool(Uv.min()>0)})")
    # a few sample rows
    for frac in (0.0, 0.5, 0.9, 0.99, 1.0):
        i = int(frac*4000)
        print(f"   r={rr[i]:9.3f} phi={phi[i]:+8.4f} rho={rho[i]:7.4f} "
              f"8pi*eps={eps8[i]:+.6g} 8pi*p_r={pr8[i]:+.6g} U={Uv[i]:.6g}")

print("\n== Z=8 first a>1 root (bracket 1.001,1.002) ==")
def missval(a, Z, rho_c=1.0, rtol=1e-11):
    U, Up, _ = make_risefall_slice(a, rho_c=rho_c)
    o = shoot(U, Up, Z, rho_c=rho_c, rtol=rtol, atol=rtol*1e-2, r_max=60000.0)
    if o['status'] != 'seal': raise RuntimeError(o['status'])
    return o['miss']
try:
    astar = brentq(missval, 1.001, 1.002, args=(8.0,), xtol=1e-12)
    U, Up, _ = make_risefall_slice(astar)
    o = shoot(U, Up, 8.0, rtol=1e-12, atol=1e-14, r_max=60000.0)
    print(f" Z=8 first a>1: a*={astar:.10f} rho_s={o['y_s'][2]:.6f} r_s={o['r_s']:.4f} "
          f"q={8.0*o['y_s'][2]**2*o['y_s'][1]:.6f}")
except ValueError:
    print(" no sign change in (1.001,1.002)")

print("\n== RK4 independent sign check at a* +- 1e-5 (Z=1) ==")
for da in (-1e-5, +1e-5):
    a = ASTAR[1.0] + da
    U, Up, _ = make_risefall_slice(a)
    o = rk4_shoot(U, Up, 1.0, h=0.02, r_max=2000.0)
    print(f" a=a*{da:+.0e}: status={o['status']} miss={o['miss']:+.6e}")

print("\n== Q5: homothety rho_c=3, Z=1 (re-bisect a*, compare scaled r_s, rho_s, q) ==")
astar3 = brentq(missval, 0.9958, 0.9963, args=(1.0, 3.0), xtol=1e-13, rtol=8.9e-16)
U, Up, _ = make_risefall_slice(astar3, rho_c=3.0)
o = shoot(U, Up, 1.0, rho_c=3.0, rtol=1e-13, atol=1e-15, r_max=60000.0)
rho_s, phip_s = o['y_s'][2], o['y_s'][1]
q = 1.0*rho_s**2*phip_s
print(f" a*(rho_c=3) = {astar3:.13f}   vs a*(rho_c=1) = {ASTAR[1.0]:.13f}  "
      f"diff={astar3-ASTAR[1.0]:+.2e}")
print(f" r_s = {o['r_s']:.8f}   3x ref = {3*753.10691222:.8f}   ratio/3 = {o['r_s']/(3*753.10691222):.12f}")
print(f" rho_s = {rho_s:.10f}  3x ref = {3*1.3674805352:.10f}  ratio = {rho_s/(3*1.3674805352):.12f}")
print(f" q = {q:.10f}  3x ref = {3*1.2649417698:.10f}  ratio = {q/(3*1.2649417698):.12f}")
print(f" Hdrift={o['Hdrift']:.1e}  (H0={o['H0']:+.1e}, checks U(rho_c)=2 renormalization)")
