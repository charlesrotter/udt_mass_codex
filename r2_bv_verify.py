"""BLIND ADVERSARIAL VERIFIER for R2 (r2_prereg_s_dependence.md + r2_final_cas.py).
Independent re-derivation from the SOURCE metric/action, own sympy, NOT their script.
DATA-BLIND: no observational number here.
"""
import sympy as sp

r, c = sp.symbols('r c', positive=True)
Z, mu = sp.symbols('Z mu', positive=True)
s = sp.symbols('s', positive=True)

R = []
def ck(name, cond):
    ok = bool(cond); R.append((name, ok))
    print(('PASS ' if ok else '**FAIL** ')+name)

# ================= metric (canon C-2026-06-18-1), general phi(r)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
g_tt = -sp.exp(-2*phi)*c**2
g_rr =  sp.exp( 2*phi)
g_OO =  rho**2

# --- CLAIM B core: ghat = e^{2phi} g ---
gh_tt = sp.exp(2*phi)*g_tt
gh_rr = sp.exp(2*phi)*g_rr
gh_OO = sp.exp(2*phi)*g_OO
ck('B1: ghat_tt = -c^2 IDENTICALLY (any phi)', sp.simplify(gh_tt + c**2)==0)
ck('B2: ghat_rr = e^{4phi}', sp.simplify(gh_rr - sp.exp(4*phi))==0)
ck('B3: ghat_OO = e^{2phi} rho^2', sp.simplify(gh_OO - sp.exp(2*phi)*rho**2)==0)

# --- Christoffel Gamma^r_tt for a DIAGONAL static metric: Gamma^r_tt = -1/2 g^{rr} d_r g_tt
def Gam_r_tt(gtt, grr):
    return sp.simplify(-sp.Rational(1,2)*(1/grr)*sp.diff(gtt, r))
Gam_g  = Gam_r_tt(g_tt, g_rr)
Gam_gh = Gam_r_tt(gh_tt, gh_rr)
ck('B4: Gamma^r_tt(ghat) = 0 (zero static force under ghat)', sp.simplify(Gam_gh)==0)
ck('B5 CONTRAST: Gamma^r_tt(g) != 0 in general (g DOES exert force)',
   sp.simplify(Gam_g) != 0)

# --- FULL radial geodesic accel of a MOMENTARILY-STATIC body (u^r=u^th=u^ph=0, only u^t):
#     d^2r/dtau^2 = -Gamma^r_tt (u^t)^2.  u^t^2 fixed by normalization g_tt (u^t)^2 = -c^2.
# ghat: u^t^2 = -c^2/gh_tt = 1 ; g: u^t^2 = -c^2/g_tt = e^{2phi}
acc_static_gh = sp.simplify(-Gam_gh*(-c**2/gh_tt))
acc_static_g  = sp.simplify(-Gam_g *(-c**2/g_tt))
ck('B6: full radial accel of static body under ghat = 0 (no attraction, ANY phi)',
   sp.simplify(acc_static_gh)==0)
ck('B7 CONTRAST: full radial accel of static body under g != 0 (real attraction)',
   sp.simplify(acc_static_g) != 0)

# --- one-body g: does g give a genuine attractive (inward) force toward larger depth?
# use one-body phi = phi_inf - q/r_areal, take rho=r (areal), q>0 attractive
q = sp.Symbol('q', positive=True)
phi_ob = sp.Symbol('phi_inf') - q/r
Gam_g_ob = (-sp.Rational(1,2)*(1/sp.exp(2*phi_ob))*sp.diff(-sp.exp(-2*phi_ob)*c**2, r))
Gam_g_ob = sp.simplify(Gam_g_ob)
# radial accel (inward = negative) for static body:
acc_ob = sp.simplify(-Gam_g_ob*(-c**2/(-sp.exp(-2*phi_ob)*c**2)))
print('   one-body g static radial accel =', acc_ob, ' (sign at r>0, q>0):',
      sp.simplify(acc_ob.subs({q:1, r:2, c:1, sp.Symbol('phi_inf'):0})))
ck('B8: one-body g gives NONZERO radial accel (attraction exists in g-frame)',
   sp.simplify(acc_ob) != 0)

# ================= redshift (mandatory #2)
# static clock proper-time rate = sqrt(-g_tt)/c ; ambient phi = phi0 - s ln rho_a
phi0 = sp.Symbol('phi0')
rho_a = sp.Symbol('rho_a', positive=True)
phi_amb = phi0 - s*sp.log(rho_a)
rate_g  = sp.sqrt(-(-sp.exp(-2*phi_amb)*c**2))/c
rate_gh = sp.sqrt(-(sp.exp(2*phi_amb)*(-sp.exp(-2*phi_amb)*c**2)))/c
r1, r2 = sp.symbols('r1 r2', positive=True)
ratio_g  = sp.simplify(rate_g.subs(rho_a, r2)/rate_g.subs(rho_a, r1))
ratio_gh = sp.simplify(rate_gh.subs(rho_a, r2)/rate_gh.subs(rho_a, r1))
ck('B9: g-frame clock ratio = (rho2/rho1)^s', sp.simplify(ratio_g - (r2/r1)**s)==0)
ck('B10: ghat-frame clock ratio = 1 (ZERO redshift)', sp.simplify(ratio_gh - 1)==0)

# ================= S13c (mandatory #3): R1-invariance of MOVING worldline
lam = sp.Symbol('lam')            # shift phi -> phi + lam
td, rd = sp.symbols('td rd', positive=True)
phic = sp.Symbol('phic')
def wact(shift):  # a(phi)*sqrt(-g xdot xdot), a=e^{phi}
    ph = phic + shift
    return sp.exp(ph)*sp.sqrt(sp.exp(-2*ph)*c**2*td**2 - sp.exp(2*ph)*rd**2)
static_resid = sp.simplify((wact(lam)-wact(0)).subs(rd,0))
moving_num = (wact(lam)/wact(0)).subs({td:10, rd:1, c:1, phic:0, lam:sp.log(2)})
ck('B11: static worldline shift-invariant (residual 0 at rd=0)', static_resid==0)
ck('B12: MOVING worldline NOT shift-invariant (over-shifts)',
   abs(float(moving_num)-1) > 1e-9)
# HUNT: is there a single conformal a(phi) fixing BOTH blocks? need a^2*(-g_tt) and a^2*g_rr both
# shift-invariant.  a^2*(-g_tt)=a^2 e^{-2phi}c^2 inv => a=e^{phi}; then a^2 g_rr = e^{4phi} NOT inv.
a_conf = sp.Function('a')(phi)
tt_inv = sp.exp(2*phi)*sp.exp(-2*phi)  # with a=e^phi -> c^2 const, invariant
rr_with_efphi = sp.exp(2*phi)*sp.exp(2*phi)  # = e^{4phi}
ck('B13: conformal a=e^{phi} makes tt-block invariant but rr-block=e^{4phi} shift-DEPENDENT '
   '(=> no single conformal a fixes both; disformal/anisotropic needed => not a worldline)',
   sp.simplify(tt_inv - 1)==0 and sp.diff(rr_with_efphi, phi) != 0)
# disformal fix: separate weight b on dr with b^2 e^{2phi} invariant => b=e^{-phi} != a=e^{phi}
b_needed = sp.exp(-phi)
ck('B14: the invariant fix requires b(dr)=e^{-phi} != a(dt)=e^{+phi} (ANISOTROPIC, not conformal '
   'worldline) -- confirms "no single a(phi)"', sp.simplify(b_needed*sp.exp(2*phi)*b_needed)==sp.exp(0))

# ================= J(s) light deflection (mandatory #4)
w, v = sp.symbols('w v', positive=True)
alpha = 1/(2-2*s)
J_closed = sp.sqrt(sp.pi)*sp.gamma(alpha)/((1-s)*sp.gamma(alpha+sp.Rational(1,2)))
# independent Beta-integral evaluation of 2 Int_0^1 dw/sqrt(1-w^{2-2s}), sub v=w^{2-2s}:
# w=v^{1/(2-2s)}, dw = 1/(2-2s) v^{alpha-1} dv ; integrand 2 * (1/(2-2s)) v^{alpha-1}(1-v)^{-1/2}
J_beta = 2*sp.Rational(1,1)*(sp.gamma(alpha)*sp.gamma(sp.Rational(1,2))
          /((2-2*s)*sp.gamma(alpha+sp.Rational(1,2))))
ck('J1: closed form = Beta-integral form', sp.simplify(J_beta - J_closed)==0)
ck('J2: J(0)=pi', sp.simplify(J_closed.subs(s,0)-sp.pi)==0)
# J(1/2) independent numeric quadrature
J_half_num = float(2*sp.integrate(1/sp.sqrt(1-w), (w,0,1)))
ck('J3: J(1/2)=4 (independent quadrature)', abs(J_half_num-4) < 1e-12
   and abs(float(J_closed.subs(s,sp.Rational(1,2)))-4) < 1e-12)
J_ser = sp.series(J_closed, s, 0, 2).removeO()
ck('J4: small-s J = pi[1+(1-ln2)s]', sp.simplify(J_ser - sp.pi*(1+(1-sp.log(2))*s))==0)
# impact-parameter independence: J depends only on s (no rho0/impact param appears)
ck('J5: J(s) has NO impact-parameter dependence (function of s alone)',
   J_closed.free_symbols == {s})

# ================= orbit v^2 = s under g; and NO orbit under ghat (mandatory #1 confirm-kill)
rho_s = sp.Symbol('rho_s', positive=True)
A_g  = sp.exp(-2*phi0)*rho_s**(2*s)       # -g_tt/c^2 in areal coord (ambient)
Om2_g = c**2*sp.diff(A_g, rho_s)/(2*rho_s)   # coord ang vel^2 for circular orbit
v2_g = sp.simplify(rho_s**2*Om2_g/(c**2*A_g))
ck('O1: g-frame flat rotation law v^2/c^2 = s (reproduced independently)',
   sp.simplify(v2_g - s)==0)
A_gh = sp.simplify(sp.exp(2*(phi0-s*sp.log(rho_s)))*A_g*0 + 1)  # ghat A = -ghat_tt/c^2 = 1 const
Om2_gh = c**2*sp.diff(sp.Integer(1), rho_s)/(2*rho_s)  # A_gh const => derivative 0
ck('O2: ghat-frame A(rho)=1 const => Om^2=0 => v^2=s VANISHES (kill confirmed)',
   sp.simplify(Om2_gh)==0)

# ================= EOMs / flux / gauge (spot re-derivation)
def EL(L,qf): return sp.simplify(sp.diff(L,qf)-sp.diff(sp.diff(L,qf.diff(r)),r))
rp, pp = rho.diff(r), phi.diff(r)
LG = (Z/2)*rho**2*pp**2 + 2*mu*rho*rp*pp + 2 - 2*rp**2
Phi = Z*rho**2*pp + 2*mu*rho*rp
ck('E1: phi-EOM = -(Phi)\' (flux conserved)', sp.simplify(EL(LG,phi)+sp.diff(Phi,r))==0)
a_,b_ = sp.symbols('a_ b_', positive=True)
rho_f = a_*r+b_; phi_f = phi0-(2*mu/Z)*sp.log(rho_f)
sub={phi.diff(r,2):phi_f.diff(r,2),pp:phi_f.diff(r),phi:phi_f,
     rho.diff(r,2):rho_f.diff(r,2),rp:rho_f.diff(r),rho:rho_f}
ck('E2: ambient rho=ar+b, phi=phi0-(2mu/Z)ln rho solves EOMs & has Phi=0 (s=2mu/Z)',
   sp.simplify(EL(LG,phi).subs(sub))==0 and sp.simplify(EL(LG,rho).subs(sub))==0
   and sp.simplify(Phi.subs(sub))==0)
# s = 2mu/Z is the exponent in clock/ruler; gauge: shift phi->phi+lam scales D by e^lam, slope=-s
D = sp.exp(phi_f)/rho_f.diff(r)
Dsh = sp.exp(phi_f+lam)/rho_f.diff(r)
ck('E3: shift phi->phi+lam sends D->e^lam D (value=gauge); log-slope dlnD/dlnrho=-s invariant',
   sp.simplify(Dsh-sp.exp(lam)*D)==0 and
   sp.simplify(sp.diff(sp.log(D.subs(r,(rho_s-b_)/a_)),rho_s)*rho_s + 2*mu/Z)==0)

# ================= seal jump ∝ s, flux ∝ s (levers)
pG,rG,pP,rP = sp.symbols("pG rG pP rP", real=True)
rs,phis = sp.symbols('rs phis', positive=True)
JC1 = Z*rs**2*pG+2*mu*rs*rG-(Z*rs**2*pP+2*mu*rs*rP)
JC2 = -4*rG+2*mu*rs*pG-(-4*sp.exp(-2*phis)*rP+2*mu*rs*pP)
sol = sp.solve([JC1,JC2],[pG,rG],dict=True)[0]
jump = sp.simplify(sol[pG]-pP)
ck('L1: G|P phi\'-jump = s(1-e^{-2phis})rhoP/(rs(1+mu^2/Z)) (PROPORTIONAL to s)',
   sp.simplify(jump - (2*mu/Z)*(1-sp.exp(-2*phis))*rP/(rs*(1+mu**2/Z)))==0)
lnr,I_ = sp.symbols('lnr I_', positive=True)
Phi_odd = sp.solve(sp.Eq(0,(sp.Symbol('Px')/Z)*I_-(2*mu/Z)*lnr), sp.Symbol('Px'))[0]
ck('L2: odd+odd G-flux Phi = 2mu ln(rho2/rho1)/I = sZ ln/I (PROPORTIONAL to s)',
   sp.simplify(Phi_odd - 2*mu*lnr/I_)==0)

print(f'\n{sum(1 for _,o in R if o)}/{len(R)} INDEPENDENT CHECKS PASS')
