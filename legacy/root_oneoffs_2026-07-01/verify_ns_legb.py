"""AXIS 2: does LEG (b) -- the fate polynomial 'motion never sources shape'
-- survive the sign fix?  Independent rederivation.
AXIS 4: high-k growth test under the CORRECTED hyperbolic operator.
Agent ns-verify 2026-06-13."""
import numpy as np, sympy as sp

print("="*70); print("AXIS 2: FATE POLYNOMIAL, independent rederivation"); print("="*70)
# Off-diagonal Class-B metric block M=[[-f,a,b],[a,1/f,q],[b,q,A]], areal.
# The eliminated L* = -(c/8) sqrt(B) R/(f sqrt(f D2)), R = fP + D2 vT^2.
# Shape stationarity in (q, w) with A=r^2 W1^2.  Is the joint fate f_T-free?
f,r,W1 = sp.symbols('f r W1', positive=True)
q = sp.Symbol('q', real=True)
vT,vr,vh = sp.symbols('vT vr vh', real=True)  # vT = f_T, vr=f_r, vh=f_theta
A = sp.Symbol('A', positive=True)
D2 = A/f - q**2
Pp = A*vr**2 - 2*q*vr*vh + vh**2/f
R = f*Pp + D2*vT**2
# q-stationarity of R/sqrt(D2): numerator 2 R_q D2 - R D2_q
E1 = sp.expand(2*sp.diff(R,q)*D2 - R*sp.diff(D2,q))
# solve E1 for A (degree 1), substitute into the w-bracket
g = f*vr**2 - vT**2/f
polA = sp.Poly(E1, A)
print("E1 degree in A:", polA.degree())
Aq = sp.solve(E1, A)[0]
h = f*vr**2 + vT**2/f
brackA = sp.expand(-R*f*D2 + 2*A*h*f*D2 - A*R)   # w-stationarity bracket
fate = sp.together(brackA.subs(A, Aq))
num = sp.factor(sp.numer(fate))
print("FATE numerator (factored):", num)
print("FATE numerator has vT (=f_T)?:", sp.expand(sp.numer(fate)).has(vT))
target = -2*f*q*vh*(f*q*vr - vh)**3
# compare numerator to target up to a vT-free denominator factor
ratio = sp.cancel(sp.together(sp.numer(fate)/target))
print("numer/target =", sp.factor(ratio), " has vT?:", sp.factor(ratio).has(vT))

print("\n=> LEG (b) verdict: fate numerator vT-free?",
      not sp.expand(sp.numer(fate)).has(vT))

print("\n"+"="*70)
print("AXIS 4: HIGH-K GROWTH under the CORRECTED hyperbolic operator")
print("="*70)
# Spherical corrected operator: e^{2phi}phi_TT - e^{-2phi}(phi_rr+(2/r)phi_r
#  -2phi_r^2) = 0.  Linearize about phi0=const background ->
# e^{2p0}u_TT = e^{-2p0}(u_rr + (2/r)u_r).  Wave speed c^2=e^{-4p0}>0.
# Seed high-k modes u=sin(k r); dispersion omega^2 = c^2 k^2 (REAL) =>
# bounded oscillation. If it were elliptic (v_a3 sign), omega^2=-c^2 k^2 =>
# growth e^{|c|k t}: UNBOUNDED in k.  Test BOTH numerically.
def march(sign, k, p0=0.0, Nr=4000, rmax=20.0, steps=400):
    # sign=+1 hyperbolic (correct): u_TT = c2(u_rr); sign=-1 elliptic(v_a3)
    rr = np.linspace(0.5, rmax, Nr); dr = rr[1]-rr[0]
    c2 = np.exp(-4*p0)
    dt = 0.2*dr/np.sqrt(c2)
    u = np.sin(k*rr)*np.exp(-((rr-10)/3)**2)
    uprev = u.copy(); maxes=[]
    for n in range(steps):
        lap = np.zeros_like(u)
        lap[1:-1] = (u[2:]-2*u[1:-1]+u[:-2])/dr**2
        unew = 2*u - uprev + sign*c2*dt**2*lap
        unew[0]=unew[1]; unew[-1]=unew[-2]
        uprev=u; u=unew; maxes.append(np.max(np.abs(u)))
    return maxes[-1], np.max(maxes)

for k in [1.0, 5.0, 20.0, 50.0]:
    fin_h, mx_h = march(+1, k)
    fin_e, mx_e = march(-1, k)
    print(f" k={k:5.1f}  HYPERBOLIC(correct) maxabs={mx_h:.3e}   "
          f"ELLIPTIC(v_a3 sign) maxabs={mx_e:.3e}")
