"""Final batch:
(1) gamma=0 control on the a- extension: does the positive mode persist
    with NO interface delta? (-> core artifact vs weld binding)
(2) Independent BC-a no-root check for the PHYSICAL cell (Friedrichs):
    F(W) = L_I(W) - gamma - D_ext(sqrt(W)) sign-definite on (0,50]?
    L_I via exact I_nu start at x0=-8 (stable direction).
(3) Closed-form q-scan: margin(q,lam) = 2q - L0(q,lam) < 0 on (0,1/2)?
    best margin at q->1/2, lam=2 (claim -0.4820).
(4) lam=6 BC-c a- root: convergence sequence x0=-8,-10,-12.
"""
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import kv, iv

mp.mp.dps = 30
q = 1/3; s = q*(1-q)/2
mu = np.sqrt(1+4*q*(1-q))/2
GAM = 2/3

def branch_data(lam, x0, kind):
    tau0 = (2*np.sqrt(lam)/q)*np.exp(q*x0/2)
    n = mp.sqrt(17)
    if kind == 'K':
        F = mp.besselk(n, tau0)
        Fp = -(mp.besselk(n-1, tau0) + mp.besselk(n+1, tau0))/2
    else:
        F = mp.besseli(n, tau0)
        Fp = (mp.besseli(n-1, tau0) + mp.besseli(n+1, tau0))/2
    pref = mp.e**(-(1-2*mp.mpf(1)/3)*x0/2)
    u0 = float(pref*F)
    up0 = float(pref*(-(1-2*mp.mpf(1)/3)/2*F + Fp*tau0*mp.mpf(1)/(3*2)*1))
    # note: dtau/dx = tau*q/2 -> Fp*tau0*q/2; q=1/3 -> tau0/6
    up0 = float(pref*(-(1-2*q)/2*F + Fp*tau0*q/2))
    return u0, up0

def Lbranch(W, lam, x0=-8.0, kind='K', rtol=1e-13):
    u0, up0 = branch_data(lam, x0, kind)
    def rhs(x, y):
        return [y[1], -(1-2*q)*y[1] + (lam*np.exp(q*x)+4*s
                                       + W*np.exp((2+2*q)*x))*y[0]]
    sol = solve_ivp(rhs, [x0, 0.0], [u0, up0], rtol=rtol, atol=1e-300,
                    method='DOP853')
    return sol.y[1,-1]/sol.y[0,-1]

print("(1) a- extension, gamma = 0 (NO delta), BC u'(R)=0: root of Lm(W)=0?")
for lam in (2.0, 6.0):
    f = lambda W: Lbranch(W, lam, x0=-10.0)
    g = np.geomspace(1e-3, 30, 60); v=[f(w) for w in g]; rt=[]
    for i in range(len(g)-1):
        if np.sign(v[i]) != np.sign(v[i+1]):
            rt.append(brentq(f, g[i], g[i+1], xtol=1e-10))
    print(f"   lam={lam:g}: roots of Lm(W)=0: {['%.6f' % x for x in rt]}")

print()
print("(2) PHYSICAL cell, BC-a, Friedrichs: F(W)=L_I(W)-2/3-D_ext on (0,50]")
def D_ext(w, ell):
    n_ = ell + 0.5
    kp = -0.5*(kv(n_-1, w) + kv(n_+1, w))
    return -0.5 + w*kp/kv(n_, w)
for lam, ell in ((2.0,1),(6.0,2)):
    Ws = np.geomspace(1e-3, 50.0, 40)
    F = [Lbranch(w, lam, kind='I') - GAM - D_ext(np.sqrt(w), ell) for w in Ws]
    print(f"   lam={lam:g}: min F = {min(F):+.4f} (>0 => no root, no mode); "
          f"F(0+)={F[0]:+.4f}, F(50)={F[-1]:+.4f}")
# also check L_I(0) from this start matches closed form 1.33835
print(f"   sanity L_I(W=0,lam=2) = {Lbranch(0.0, 2.0, kind='I'):+.8f} "
      f"(closed form +1.33835009)")
# BC-c physical: root of L_I(W)=2/3 should be NEGATIVE (the -3.4668);
# confirm no positive root:
for lam in (2.0, 6.0):
    Ws = np.geomspace(1e-3, 50.0, 40)
    F = [Lbranch(w, lam, kind='I') - GAM for w in Ws]
    print(f"   BC-c physical lam={lam:g}: min(L_I - 2/3) on (0,50] = "
          f"{min(F):+.4f} (>0 => no positive mode)")

print()
print("(3) closed-form margin scan 2q - L0(q,lam):")
def L0_cf(qv, lam):
    qv = mp.mpf(qv); lam = mp.mpf(lam)
    nuv = mp.sqrt(1+4*qv*(1-qv))/qv
    t0 = 2*mp.sqrt(lam)/qv
    Ip = (mp.besseli(nuv-1, t0) + mp.besseli(nuv+1, t0))/2
    return -(1-2*qv)/2 + (qv*t0/2)*Ip/mp.besseli(nuv, t0)
worst = -np.inf; argw = None
for qv in [0.02,0.05,0.1,0.15,0.2,0.25,0.3,1/3,0.35,0.4,0.45,0.49,0.4999]:
    margins = [float(2*mp.mpf(qv) - L0_cf(qv, lam)) for lam in (2,6,12)]
    if margins[0] > worst: worst, argw = margins[0], qv
    flag = all(m < 0 for m in margins)
    print(f"   q={qv:7.4f}: lam=2 {margins[0]:+.5f}  lam=6 {margins[1]:+.5f} "
          f" lam=12 {margins[2]:+.5f}  all<0: {flag}")
print(f"   best BC-c margin: {worst:+.5f} at q={argw} (claim -0.4820 at q->1/2)")
# BC-a margin = 2q - L0 - (ell+1) <= margin_c - 2 < 0 always. theorem-level.

print()
print("(4) lam=6 BC-c a- root convergence:")
for x0 in (-8.0, -10.0, -12.0):
    f = lambda W: Lbranch(W, 6.0, x0=x0) - GAM
    try:
        rt = brentq(f, 1e-4, 0.05, xtol=1e-11)
        print(f"   x0={x0}: root = {rt:.7f}")
    except ValueError as e:
        print(f"   x0={x0}: bracket failed ({e})")
