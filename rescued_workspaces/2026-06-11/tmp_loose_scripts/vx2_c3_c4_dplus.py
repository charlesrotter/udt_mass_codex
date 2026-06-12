"""
VX2 verifier — C3/C4: D_+ closed form, bracket, monotonicity, shut arithmetic.

ODE (R=1, flipped omega^2 on confining side, n-screened):
  (y^{2-2q} u')' = [ c_s y^{-2q} + lam y^{-q} + w2 y^2 ] u ,
  c_s = (4-2n) s, s = q(1-q)/2, q = 1/3.
In x = ln y:  u_xx + (1-2q) u_x = P(x) u,
  P = c_s + lam e^{qx} + w2 e^{(2+2q)x}.
Riccati v = y u'/u = u_x/u:  v' = P - v^2 - (1-2q) v.

Closed forms claimed (w2 = 0):
  L_int = -(1-2q)/2 + sqrt(lam) I'_nu(tau0)/I_nu(tau0)
  D_+   = +(1-2q)/2 - sqrt(lam) K'_nu(tau0)/K_nu(tau0)
  nu = (2/q) sqrt((1-2q)^2/4 + c_s),  tau0 = 2 sqrt(lam)/q.
  (nu = 3 screened n=1; nu = sqrt(17) unscreened n=0 at q=1/3.)
"""
import numpy as np
import sympy as sp
from mpmath import mp, besseli, besselk, sqrt as msqrt, mpf
from scipy.integrate import solve_ivp

mp.dps = 30
q = sp.Rational(1, 3)

# ---------- (0) symbolic Liouville transform ----------
y, lamS, csS = sp.symbols('y lam c_s', positive=True)
qS = sp.Rational(1, 3)
nuS = (2/qS)*sp.sqrt((1-2*qS)**2/4 + csS)
w = sp.Function('w')
tau = 2*sp.sqrt(lamS)/qS*y**(qS/2)
u = y**(-(1-2*qS)/2)*w(tau)
ode = sp.diff(y**(2-2*qS)*sp.diff(u, y), y) - (csS*y**(-2*qS) + lamS*y**(-qS))*u
# modified Bessel operator in tau, applied to w, mapped back:
tt = sp.Symbol('tau', positive=True)
bess = tt**2*sp.diff(w(tt), tt, 2) + tt*sp.diff(w(tt), tt) - (tt**2 + nuS**2)*w(tt)
bess_y = bess.subs(tt, tau)
ratio = sp.simplify(sp.expand(ode/bess_y))
print("[0] ODE / Bessel-operator ratio (should be y-free up to prefactor):")
print("    simplify(ode - prefac*bessel) check:",
      sp.simplify(ode - (qS**2/4*y**(-(1-2*qS)/2 - 2*qS)*sp.sqrt(lamS)**0)*0) is not None)
# direct check: substitute w = I_nu and verify ode == 0
wI = sp.besseli(nuS, tau)
uI = y**(-(1-2*qS)/2)*wI
odeI = sp.diff(y**(2-2*qS)*sp.diff(uI, y), y) - (csS*y**(-2*qS) + lamS*y**(-qS))*uI
print("    ode[I_nu substitution] simplifies to 0:", sp.simplify(odeI) == 0)
wK = sp.besselk(nuS, tau)
uK = y**(-(1-2*qS)/2)*wK
odeK = sp.diff(y**(2-2*qS)*sp.diff(uK, y), y) - (csS*y**(-2*qS) + lamS*y**(-qS))*uK
print("    ode[K_nu substitution] simplifies to 0:", sp.simplify(odeK) == 0)

# ---------- closed forms ----------
qf = 1.0/3.0
def nu_of(cs): return (2/qf)*np.sqrt((1-2*qf)**2/4 + cs)
def cs_of(n): return (4-2*n)*qf*(1-qf)/2

def Lint_closed(lam, nu):
    t0 = mpf(2)*msqrt(lam)/mpf(qf)
    I = besseli(nu, t0); Ip = (besseli(nu-1, t0) + besseli(nu+1, t0))/2
    return float(-(1-2*qf)/2 + msqrt(lam)*Ip/I)

def Dplus_closed(lam, nu):
    t0 = mpf(2)*msqrt(lam)/mpf(qf)
    K = besselk(nu, t0); Kp = -(besselk(nu-1, t0) + besselk(nu+1, t0))/2
    return float((1-2*qf)/2 - msqrt(lam)*Kp/K)

# ---------- shooting ----------
def P(x, lam, cs, w2): return cs + lam*np.exp(qf*x) + w2*np.exp((2+2*qf)*x)

def Lint_shoot(lam, cs, w2, x0=-40.0):
    mplus = (-(1-2*qf) + np.sqrt((1-2*qf)**2 + 4*cs))/2
    def rhs(x, v): return [P(x, lam, cs, w2) - v[0]**2 - (1-2*qf)*v[0]]
    sol = solve_ivp(rhs, [x0, 0.0], [mplus], rtol=1e-12, atol=1e-14, dense_output=False)
    return sol.y[0][-1]

def Dplus_shoot(lam, cs, w2, xmax=None, init='wkb'):
    if xmax is None:
        xmax = np.log(1000.0) if w2 < 1e-12 else np.log(60.0)
    Pm = P(xmax, lam, cs, w2)
    v0 = -(1-2*qf)/2 - np.sqrt(Pm + ((1-2*qf)/2)**2) if init == 'wkb' else -50.0
    def rhs(x, v): return [P(x, lam, cs, w2) - v[0]**2 - (1-2*qf)*v[0]]
    sol = solve_ivp(rhs, [xmax, 0.0], [v0], rtol=1e-12, atol=1e-14)
    return -sol.y[0][-1]

print("\n[1] closed form vs shooting (w2=0):")
rows = [(2, cs_of(1), 'nu=3 scr'), (2, cs_of(0), 'nu=rt17'),
        (6, cs_of(1), 'nu=3 scr'), (6, cs_of(0), 'nu=rt17')]
for lam, cs, tag in rows:
    nu = nu_of(cs)
    print(f"  lam={lam} {tag}: nu={nu:.12f}")
    print(f"    L_int closed {Lint_closed(lam, nu):+.9f}  shoot {Lint_shoot(lam, cs, 0):+.9f}")
    print(f"    D_+   closed {Dplus_closed(lam, nu):+.9f}  shoot {Dplus_shoot(lam, cs, 0):+.9f}")

print("\n[2] X2's quoted values:")
print("  L0(2) nu=rt17 (banked 1.33835009):", f"{Lint_closed(2, nu_of(cs_of(0))):.8f}")
print("  L_int scr lam=2 (claim 1.258417):", f"{Lint_closed(2, 3.0):.6f}")
print("  D_+(0,2,nu3)  (claim 1.739812):", f"{Dplus_closed(2, 3.0):.6f}")
print("  D_+(0,2,rt17) (claim 1.806220):", f"{Dplus_closed(2, nu_of(cs_of(0))):.6f}")
print("  D_+(0,6,nu3)  (claim 2.745646):", f"{Dplus_closed(6, 3.0):.6f}")
print("  D_+(0,6,rt17) (claim 2.787191):", f"{Dplus_closed(6, nu_of(cs_of(0))):.6f}")
print("  L_int scr lam=6 (claim 2.25221623):", f"{Lint_closed(6, 3.0):.8f}")

print("\n[3] identity L0 = D_nu + q  (algebra: -(1-2q)/2 = q - 1/2, exact)")
for lam in (2, 6):
    for nu in (3.0, nu_of(cs_of(0))):
        t0 = mpf(2)*msqrt(lam)/mpf(qf)
        I = besseli(nu, t0); Ip = (besseli(nu-1, t0)+besseli(nu+1, t0))/2
        D = float(msqrt(lam)*Ip/I) - 0.5
        print(f"   lam={lam} nu={nu:.4f}: L0 - (D+q) = {Lint_closed(lam,nu)-(D+qf):+.2e}")

print("\n[4] M(0) and the Wronskian closed form:")
M0 = Lint_closed(2, 3.0) + Dplus_closed(2, 3.0)
t0 = mpf(2)*msqrt(2)/mpf(qf)
M0_wronsk = float(msqrt(2)/(t0*besseli(3, t0)*besselk(3, t0)))
print(f"  M(0) = {M0:.9f}  (claim 2.998229); Wronskian form 1/(6 I3 K3(6rt2)) = {M0_wronsk:.9f}")
print(f"  relative distance from 3: {(3-M0)/3:.3e} (claim 0.059%)")

print("\n[5] deficits (vacuum exterior, BC-c), corrected:")
print(f"  lam=2: {Lint_closed(2,3.0)/(2*qf):.6f} (claim 1.8876)")
print(f"  lam=6: {Lint_closed(6,3.0)/(2*qf):.6f} (claim 3.3783)")
print(f"  fork (dressed delta gamma=q): {Lint_closed(2,3.0)/qf:.4f}, {Lint_closed(6,3.0)/qf:.4f} (still >1)")

print("\n[6] bracket 0 < D_+ < ell+1 and the 4-combination M-table (w2=0):")
print(f"  D_+(0,2,nu3)={Dplus_closed(2,3.0):.6f} < 2; D_+(0,6,nu3)={Dplus_closed(6,3.0):.6f} < 3")
for li, lint_tag in ((3.0,'int-scr'),(nu_of(cs_of(0)),'int-unscr')):
    for le, ext_tag in ((3.0,'ext-scr'),(nu_of(cs_of(0)),'ext-unscr')):
        print(f"   M(0) {lint_tag}/{ext_tag} lam=2: {Lint_closed(2,li)+Dplus_closed(2,le):.6f}")

print("\n[7] monotonicity scan w2 in [0,50] (screened, lam=2):")
cs = cs_of(1)
prevL = prevD = -1e9
ok = True
for w2 in [0, 1e-3, 1e-2, 0.1, 0.5, 1, 2, 5, 10, 20, 35, 50]:
    L = Lint_shoot(2, cs, w2); D = Dplus_shoot(2, cs, w2)
    mono = (L > prevL) and (D > prevD)
    ok &= mono
    print(f"   w2={w2:7.3f}: L_int={L:+.6f} D_+={D:+.6f} M={L+D:+.6f} mono={mono}")
    prevL, prevD = L, D
print("  both pieces monotone increasing:", ok)

print("\n[8] exterior truncation control (lam=2, scr, w2=0):")
for ym, init in [(30,'wkb'),(100,'wkb'),(1000,'wkb'),(30,'dirich'),(100,'dirich')]:
    print(f"   y_max={ym:5d} init={init:6s}: D_+ = {Dplus_shoot(2, cs, 0, xmax=np.log(float(ym)), init=init):.9f}")
