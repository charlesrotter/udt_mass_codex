import sympy as sp
# Symmetric parametrization: a=h_thth, bt=h_pspsi/sin^2(th).  Background a0=bt0=r^2.
# sqrt(h) K = w0 * ell , ell = -1/2 sin(th) a' bt' / sqrt(a bt)   (w0=e^{-2phi0})
r, th = sp.symbols('r theta', positive=True)
S=sp.sin(th)
a=sp.Function('a'); bt=sp.Function('bt')
A=a(r); B=bt(r); Ap=sp.diff(A,r); Bp=sp.diff(B,r)
ell = -sp.Rational(1,2)*S*Ap*Bp/sp.sqrt(A*B)
def EL(L,f):
    return sp.diff(L,f)-sp.diff(sp.diff(L,sp.diff(f,r)),r)
Ea=EL(ell,A); Eb=EL(ell,B)
a0=r**2; b0=r**2
eps=sp.symbols('epsilon'); al=sp.Function('alpha'); be=sp.Function('beta')
def lin(expr):
    e2=expr.subs({A:a0+eps*al(r),B:b0+eps*be(r)})
    return sp.simplify(sp.diff(sp.series(e2,eps,0,2).removeO(),eps).subs(eps,0))
LEa=sp.simplify(lin(Ea)); LEb=sp.simplify(lin(Eb))
print("E_a linearized =",LEa)
print("E_b linearized =",LEb)
# Expect each ~ Lbare[beta or alpha]/(sym).  Lbare[f]=r^2 f''-2 r f'+2 f
Lb_beta=(r**2*sp.diff(be(r),r,2)-2*r*sp.diff(be(r),r)+2*be(r))
Lb_alpha=(r**2*sp.diff(al(r),r,2)-2*r*sp.diff(al(r),r)+2*al(r))
print("\nE_a / (Lbare[beta]) =", sp.simplify(LEa/ (Lb_beta)))
print("E_b / (Lbare[alpha]) =", sp.simplify(LEb/ (Lb_alpha)))

# ---- ROUND self-check: a pure breathing (ell=0) deformation a=bt=r^2 e^{2u(r)} ----
# Compute sqrt(h)K exactly and compare to -1/2 e^{-2phi} a' bt'/... to make sure our ell reproduces
# the round monopole source 4 e^{-2phi}. Set a=bt=A2, ell_round = -1/2 sin th (A2')^2/A2
A2=sp.Function('A2')(r)
ell_round=(-sp.Rational(1,2)*S*sp.diff(A2,r)**2/A2)
# surface integral over th,psi of w0*ell_round:  int sin dth dpsi = ... times (A2'/...)
# For round with A2=r^2: ell_round = -1/2 sin (2r)^2 / r^2 = -2 sin  -> int dth dpsi = -8 pi. matches -2 e^{-2phi} area? ok.
print("\nround ell (A2=r^2):", sp.simplify(ell_round.subs(A2,r**2)))
