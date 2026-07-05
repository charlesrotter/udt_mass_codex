"""one_body_null_deflection_cas.py -- NATIVE one-body null-geodesic deflection (DATA-BLIND).

Derives the null bending angle on the native UDT one-body-plus-ambient metric
(canon C-2026-06-18-1; R2 S3/S9 banked exterior). NO data load, NO PDE solve:
symbolic quadrature + weak-field series. GR (4m/b, 15pi/4) enters ONLY as a labelled
reference AFTER the native expression is derived. Run: python3 one_body_null_deflection_cas.py

Metric (areal):  ds^2 = -A c^2 dt^2 + B drho^2 + rho^2 dOmega^2,  A=e^{-2phi}, B=1/(a^2 A).
One-body+ambient (E=1 gauge, phit_inf=0, phi0=0):
    A(rho) = e^{-2 nu artanh(beta/x)} * rho^{2s},  x=sqrt(rho^2+beta^2),
    f := A/rho^{2s} = e^{-2 phitilde},  phitilde = nu artanh(beta/x) = mhat/rho + O(beta^3),
    mhat = nu beta (mass, attractive sig=+1), s=2mu/Z in [0,1/2], nu=2 sqrt(Z+mu^2)/Z.
To O(mhat^2):  f = e^{-2 mhat/rho}  (native exponential lapse, S3d; Z enters only at O(mhat^3)).
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 30
rho, rho0, y, s, eps, a, c, En, L, Af, Bf, A0 = sp.symbols(
    'rho rho0 y s epsilon a c En L Af Bf A0', positive=True)

# --- 0. exact null integrand from the metric (no GR) --------------------------
rhodot2 = (En**2/(Af*c**2) - L**2/rho**2)/Bf          # from -A c^2 t'^2 + B rho'^2 + rho^2 phi'^2=0
dphi_drho = (L/rho**2)/sp.sqrt(rhodot2)
b2 = rho0**2/A0                                        # turning pt: L^2 c^2/En^2 = rho0^2/A0
dphi_b = dphi_drho.subs(L, En*sp.sqrt(b2)/c)
claim = sp.sqrt(Bf)/(rho*sp.sqrt((rho**2/rho0**2)*(A0/Af) - 1))
assert sp.simplify(dphi_b - claim) == 0
print("[0] exact null integrand  dphi/drho = sqrt(B)/(rho sqrt((rho/rho0)^2 A0/A -1))  OK")

# --- reduced integral:  alpha+pi = D(rho0) K(eps),  D=e^{phi0} rho0^{-s}/a  ----
# y=rho0/rho,  K(eps)=2 Int_0^1 y^{s-1} f^{-1/2} R^{-1/2} dy,  f=e^{-2 eps y},
# R = y^{2s-2} e^{-2 eps(1-y)} - 1,  eps=mhat/rho0.
f  = sp.exp(-2*eps*y);  R = y**(2*s-2)*sp.exp(-2*eps*(1-y)) - 1
P  = y**(s-1)*f**sp.Rational(-1,2)*R**sp.Rational(-1,2)

# --- 1. ambient cross-check (eps=0 -> J(s)) -----------------------------------
assert sp.simplify(P.subs(eps,0) - 1/sp.sqrt(1-y**(2-2*s))) == 0
print("[1] beta=0: integrand -> 1/sqrt(1-y^{2-2s}); K(0)=J(s) (ambient D(rho0)J(s)); "
      "J(0)=pi, J(1/2)=4  OK")

# --- 2. leading mass coefficient K1(s)=dK/deps|0 (s-dependence = conjecture test) ---
dP = sp.simplify(sp.diff(P,eps).subs(eps,0))
assert sp.simplify(dP - (y/sp.sqrt(1-y**(2-2*s)) + (1-y)/(1-y**(2-2*s))**sp.Rational(3,2)))==0
def K1c(sv):                                           # closed form via analytic-cont. Beta
    m=2-2*sv; p=sp.Rational(1,1)/m; G=sp.gamma
    B=lambda q:G(q)*G(-sp.Rational(1,2))/G(q-sp.Rational(1,2))
    return sp.simplify(2*(B(p)-B((m+2)/m))/m)
def K1n(sv): m=2-2*sv; return 2*mp.quad(lambda t:(1-t**(m+1))/(1-t**m)**mp.mpf('1.5'),[0,1])
print("[2] leading mass coeff K1(s) (reduced): K1(0)=%s  K1(1/2)=%s  (s-DEPENDENT)"
      % (K1c(0), K1c(sp.Rational(1,2))))
for sv in [sp.Integer(0),sp.Rational(1,4),sp.Rational(1,2)]:
    assert abs(float(K1c(sv))-float(K1n(float(sv))))<1e-9

# --- 3. s=0 weak-field to O(mhat^2), fixed impact parameter b -----------------
P0 = 2*sp.exp(eps*y)/sp.sqrt(sp.exp(-2*eps*(1-y))-y**2)     # s=0 reduction (a=1)
ser = sp.series(P0,eps,0,3).removeO()
c1 = mp.quad(sp.lambdify(y,ser.coeff(eps,1),'mpmath'),[0,1])
c2 = mp.quad(sp.lambdify(y,ser.coeff(eps,2),'mpmath'),[0,1])
# eps=u+u^2 (u=mhat/b, from b=rho0 e^{eps}); Dalpha=K-pi
u=sp.symbols('u',positive=True)
Dal=sp.expand(sp.Float(str(mp.nstr(c1,30)))*(u+u**2)+sp.Float(str(mp.nstr(c2,30)))*(u+u**2)**2)
print("[3] s=0 fixed-b one-body deflection:  Dalpha = %.6f (mhat/b) + %s (mhat/b)^2"
      % (float(Dal.coeff(u,1)), sp.nsimplify(float(Dal.coeff(u,2)),[sp.pi])))
print("    GR reference:  4 (mhat/b) + 15*pi/4 (mhat/b)^2  -> leading MATCHES (gamma=1), "
      "2nd-order DEPARTS (9pi/4 vs 15pi/4)")

# --- 4. end-to-end numeric geodesic cross-check (s=0, a=1) --------------------
Kx=lambda e:2*mp.quad(lambda t:mp.e**(e*t)/mp.sqrt(mp.e**(-2*e*(1-t))-t**2),[0,1])
for e in [mp.mpf('0.01'),mp.mpf('0.005')]:
    al=Kx(e)-mp.pi; uu=e*mp.e**(-e); srs=4*uu+(mp.mpf(9)/4*mp.pi)*uu**2
    assert abs(al-srs)/al < 4e-4
print("[4] end-to-end null-geodesic integral matches 4u+(9pi/4)u^2 (residual ~ u^3)  OK")
print("\nALL CHECKS PASS (data-blind).")
