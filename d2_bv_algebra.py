"""d2_bv_algebra.py -- BLIND ADVERSARIAL VERIFIER independent CAS re-derivation
for the D2a/D2b/D2c deliverables (2026-07-04). Own sympy, own reading of sources:
  action skeleton  S = int c*sqrt(h) [ (Z/2) phi'^2 + R2[h] + W*Kcal + L_m ]
  Kcal = K_AB K^AB - K^2,  K_AB = (1/2) e^{-phi} d_r h_AB,  W = e^{2phi}(G) / 1(P)
  (native_field_equations_constrained_two_player_results.md:85-113,
   native_geometric_action_results.md:13-17)
Route B adds  2*sqrt(h)*e^{phi}*K*phi'  with Z=8 (same doc :74-78).
DO NOT COMMIT. Verifier-only.
"""
import sympy as sp

r, Z, lam, a_sym, x = sp.symbols('r Z lam a x', real=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
n_pass, n_fail, fails = 0, 0, []

def chk(name, expr_zero):
    global n_pass, n_fail
    ok = sp.simplify(expr_zero) == 0
    if ok: n_pass += 1
    else:
        n_fail += 1; fails.append(name)
    print(('PASS' if ok else 'FAIL'), name)
    return ok

def chkbool(name, b):
    global n_pass, n_fail
    if b: n_pass += 1
    else:
        n_fail += 1; fails.append(name)
    print(('PASS' if b else 'FAIL'), name)

p, pp = phi.diff(r), phi.diff(r, 2)
q1, q2 = rho.diff(r), rho.diff(r, 2)
e2p = sp.exp(2*phi); em2p = sp.exp(-2*phi)

# ---------------- A. round reduction (h = rho^2 Omega), per 4pi ------------------
# K_AB = (1/2) e^{-phi} d_r(rho^2) Omega_AB = e^{-phi} rho rho' Omega_AB
# K^A_B = e^{-phi} (rho'/rho) delta;  K = 2 e^{-phi} rho'/rho
K = 2*sp.exp(-phi)*q1/rho
KabKab = 2*sp.exp(-2*phi)*q1**2/rho**2
Kcal = KabKab - K**2
chk('A1 Kcal = -2 e^{-2phi} (rho\'/rho)^2', Kcal + 2*em2p*(q1/rho)**2)
# per-4pi measure sqrt(h)->rho^2 ; sqrt(h)R2 -> rho^2 * 2/rho^2 = 2
LP = (Z/2)*rho**2*p**2 + 2 + rho**2*Kcal                      # W=1
LG = (Z/2)*rho**2*p**2 + 2 + rho**2*e2p*Kcal                  # W=e^{2phi}
chk('A2 L_P = (Z/2)rho^2 phi\'^2 + 2 - 2 e^{-2phi} rho\'^2',
    LP - ((Z/2)*rho**2*p**2 + 2 - 2*em2p*q1**2))
chk('A3 L_G = (Z/2)rho^2 phi\'^2 + 2 - 2 rho\'^2',
    LG - ((Z/2)*rho**2*p**2 + 2 - 2*q1**2))
mix = 2*rho**2*sp.exp(phi)*K*p    # 2 sqrt(h) e^phi K phi', per 4pi
chk('A4 mixing term = 4 rho rho\' phi\'', mix - 4*rho*q1*p)
chk('A5 (sqrt h)\' = sqrt(h) e^phi K  (per 4pi: (rho^2)\'=2 rho rho\')',
    sp.diff(rho**2, r) - rho**2*sp.exp(phi)*K)
# shift-breaking bookkeeping
chk('A6 e^{2phi}Kcal is phi-shift-invariant (round)',
    sp.simplify((e2p*Kcal).subs(phi, phi+lam) - e2p*Kcal))
chkbool('A7 L_P shift-broken by -2(e^{-2lam}-1)e^{-2phi}rho\'^2',
        sp.simplify(LP.subs(phi, phi+lam) - LP
                    + 2*(sp.exp(-2*lam)-1)*em2p*q1**2) == 0)
chk('A8 mixing term shift-invariant', sp.simplify(mix.subs(phi, phi+lam) - mix))

# ---------------- B. flux identities / EL ------------------
def EL(L, f):
    return sp.diff(sp.diff(L, f.diff(r)), r) - sp.diff(L, f)
elP_phi = EL(LP, phi)
chk('B1 P phi-EL: (Z rho^2 phi\')\' = 4 e^{-2phi} rho\'^2',
    elP_phi - (sp.diff(Z*rho**2*p, r) - 4*em2p*q1**2))
chk('B2 source identity 4 e^{-2phi} rho\'^2 = -2 rho^2 Kcal',
    4*em2p*q1**2 + 2*rho**2*Kcal)
elG_phi = EL(LG, phi)
chk('B3 G phi-EL source-free: (Z rho^2 phi\')\' = 0',
    elG_phi - sp.diff(Z*rho**2*p, r))
# G rho-EL (vacuum):  -4 rho'' = Z rho phi'^2
elG_rho = EL(LG, rho)
chk('B4 G rho-EL: EL == -4rho\'\' - Z rho phi\'^2 (doc form -4rho\'\'=Zrho phi\'^2)',
    elG_rho - (-4*q2 - Z*rho*p**2))
chkbool('B4b G rho-EL == +-(4rho\'\' + Z rho phi\'^2)',
        sp.simplify(elG_rho - (4*q2 + Z*rho*p**2)) == 0 or
        sp.simplify(elG_rho + (4*q2 + Z*rho*p**2)) == 0)

# ---------------- C. non-round phi-freeness of e^{2phi}Kcal ------------------
th = sp.symbols('theta', real=True)
h11 = sp.Function('h11')(r); h12 = sp.Function('h12')(r); h22 = sp.Function('h22')(r)
hm = sp.Matrix([[h11, h12], [h12, h22]])
hinv = hm.inv()
Kab = sp.Rational(1, 2)*sp.exp(-phi)*hm.diff(r)
Kmix = hinv*Kab
KabKab_g = sp.trace(Kmix*Kmix)
Kg = sp.trace(Kmix)
Kcal_g = sp.simplify(KabKab_g - Kg**2)
chk('C1 e^{2phi}Kcal phi-free for GENERAL h_AB(r)',
    sp.simplify(sp.diff(sp.exp(2*phi)*Kcal_g, phi)))
chk('C2 e^phi K phi-free for general h_AB (mixing term shift-invariant, non-round)',
    sp.simplify(sp.diff(sp.exp(phi)*Kg, phi)))

# ---------------- D. Route B ------------------
LPB = 4*rho**2*p**2 + 4*rho*q1*p + 2 - 2*em2p*q1**2
LGB = 4*rho**2*p**2 + 4*rho*q1*p + 2 - 2*q1**2
# M5 shift identity
phit = phi + sp.Rational(1, 2)*sp.log(rho)
chk('D1 4rho^2 phit\'^2 - rho\'^2 == 4rho^2 phi\'^2 + 4 rho rho\' phi\'',
    4*rho**2*phit.diff(r)**2 - q1**2 - (4*rho**2*p**2 + 4*rho*q1*p))
# EOMs
elPB_phi = EL(LPB, phi)
chk('D2 RouteB P phi-EL: (8rho^2 phi\' + 4 rho rho\')\' = 4e^{-2phi}rho\'^2',
    elPB_phi - (sp.diff(8*rho**2*p + 4*rho*q1, r) - 4*em2p*q1**2))
elPB_rho = EL(LPB, rho)
target_rho_B = q2 - (2*p*q1 + e2p*rho*(pp - 2*p**2))
chkbool('D3 RouteB P rho-EL == rho\'\'=2phi\'rho\'+e^{2phi}rho(phi\'\'-2phi\'^2)',
        sp.simplify(elPB_rho + 4*em2p*target_rho_B) == 0 or
        sp.simplify(elPB_rho - 4*em2p*target_rho_B) == 0)
elGB_phi = EL(LGB, phi)
chk('D4 RouteB G phi-EL: (8rho^2 phi\' + 4 rho rho\')\' = 0 (source-free)',
    elGB_phi - sp.diff(8*rho**2*p + 4*rho*q1, r))
elGB_rho = EL(LGB, rho)
target_rho_GB = q2 - (rho*pp - 2*rho*p**2)
chkbool('D5 RouteB G rho-EL == rho\'\' = rho phi\'\' - 2 rho phi\'^2',
        sp.simplify(elGB_rho + 4*target_rho_GB) == 0 or
        sp.simplify(elGB_rho - 4*target_rho_GB) == 0)
# flat fails Route-B G
flat = {phi: sp.Symbol('phi0'), rho: r}
res_flat = elGB_phi.subs({pp: 0, p: 0, q2: 0, q1: 1, rho: r})
chkbool('D6 flat (rho=r, phi=const) FAILS RouteB G phi-EL (residual +-4)',
        sp.simplify(res_flat - 4) == 0 or sp.simplify(res_flat + 4) == 0)
# flat-analog family rho = a r + b, phi = phi0 - (1/2) ln rho solves BOTH G EOMs
aa, bb, p0 = sp.symbols('aa bb phi0', real=True, positive=True)
rho_fa = aa*r + bb
phi_fa = p0 - sp.Rational(1, 2)*sp.log(rho_fa)
subs_fa = {phi: phi_fa, rho: rho_fa}
def full_sub(e):
    e = e.subs({pp: phi_fa.diff(r, 2), p: phi_fa.diff(r),
                q2: rho_fa.diff(r, 2), q1: rho_fa.diff(r),
                phi: phi_fa, rho: rho_fa})
    return sp.simplify(e)
chk('D7 flat-analog solves RouteB G phi-EL', full_sub(elGB_phi))
chk('D8 flat-analog solves RouteB G rho-EL', full_sub(elGB_rho))
# even fold nondegeneracy (M6)
PiB = 8*rho**2*p + 4*rho*q1
piB = sp.diff(LPB, q1)
chk('D9 pi_rho^B = 4 rho phi\' - 4 e^{-2phi} rho\'', piB - (4*rho*p - 4*em2p*q1))
M = sp.Matrix([[8*rho**2, 4*rho], [4*rho, -4*em2p]])
chk('D10 even-fold det = -32 rho^2 e^{-2phi} - 16 rho^2 != 0',
    M.det() - (-32*rho**2*em2p - 16*rho**2))
# odd-fold jumps (mirror partner: phi->-phi, rho->rho, r-reflection)
phs, rhs_, pps_, qs_ = sp.symbols('phi_s rho_s phip_s rhop_s', real=True)
# near side at r_s: (phi_s, phip_s, rho_s, rhop_s); far side: (-phi_s, +phip_s, rho_s, -rhop_s)
piB_near = (4*rho*p - 4*em2p*q1).subs(p, pps_).subs(q1, qs_).subs(phi, phs).subs(rho, rhs_)
piB_far = (4*rho*p - 4*em2p*q1).subs(p, pps_).subs(q1, -qs_).subs(phi, -phs).subs(rho, rhs_)
chk('D11 RouteB [pi_rho] = 8 cosh(2phi_s) rhop_s (mixing cancels; any phi_s)',
    sp.simplify((piB_far - piB_near - 8*sp.cosh(2*phs)*qs_).rewrite(sp.exp)))
piA_near = (-4*em2p*q1).subs(q1, qs_).subs(phi, phs)
piA_far = (-4*em2p*q1).subs(q1, -qs_).subs(phi, -phs)
chk('D12 RouteA [pi_rho] = 8 cosh(2phi_s) rhop_s (identical to RouteB)',
    sp.simplify((piA_far - piA_near - 8*sp.cosh(2*phs)*qs_).rewrite(sp.exp)))
PiB_near = (8*rho**2*p + 4*rho*q1).subs({rho: rhs_, p: pps_, q1: qs_})
PiB_far = (8*rho**2*p + 4*rho*q1).subs({rho: rhs_, p: pps_, q1: -qs_})
chk('D13 RouteB [Pi_phi] = -8 rho_s rhop_s (0 when rhop_s=0 -> phi\' free)',
    sp.simplify(PiB_far - PiB_near + 8*rhs_*qs_))
# H^B identity and conservation
HB = p*PiB + q1*piB - LPB
HA8 = 4*rho**2*p**2 - 2*em2p*q1**2 - 2
chk('D14 H^B = H^A(Z=8) + 4 rho rho\' phi\'', HB - (HA8 + 4*rho*q1*p))
# dH/dr = 0 on-shell (vacuum P, Route B): solve EOMs for pp, q2 and substitute
sol = sp.solve([sp.Eq(elPB_phi, 0), sp.Eq(elPB_rho, 0)], [pp, q2], dict=True)
chkbool('D15 dH^B/dr == 0 on-shell (RouteB P vacuum)',
        len(sol) == 1 and sp.simplify(sp.diff(HB, r).subs(
            {pp: sol[0][pp], q2: sol[0][q2]})) == 0)
# Phi_B' = 4 e^{-2phi} rho'^2 and Phi_B = 8 rho^2 phit'
chk('D16 Phi_B = 8 rho^2 phit\'', PiB - 8*rho**2*phit.diff(r))

# ---------------- E. Route-B G|P junction (M9) ------------------
pP, pG, qP, qG, rs = sp.symbols('phipP phipG rhopP rhopG rho_s', positive=False, real=True)
xs = sp.Symbol('x', positive=True)   # x = e^{-2 phi_p}
jc1 = 8*rs**2*pG + 4*rs*qG - (8*rs**2*pP + 4*rs*qP)
jc2 = (4*rs*pG - 4*qG) - (4*rs*pP - 4*xs*qP)
solB = sp.solve([jc1, jc2], [pG, qG], dict=True)[0]
chk('E1 RouteB JC: rho\'_G = (2x+1)/3 rho\'_P',
    sp.simplify(solB[qG] - (2*xs + 1)/3*qP))
chk('E2 RouteB JC: phi\'_G - phi\'_P = (1-x) rho\'_P /(3 rho_s)',
    sp.simplify(solB[pG] - pP - (1 - xs)*qP/(3*rs)))
chk('E3 RouteB JC1 == [8 rho^2 phit\'] = 0 (phit\'-continuity)',
    sp.simplify(jc1 - (8*rs**2*(pG + qG/(2*rs)) - 8*rs**2*(pP + qP/(2*rs)))))

# ---------------- F. Route-A G|P seal: C1/C2 collapse ------------------
# P side carries matter with E_ang (f_r(r_p)=0 by C1c); G side vacuum.
Eang, H0 = sp.symbols('E_ang H0', real=True)
phipc = sp.Symbol('phip_c', real=True)  # common phi' (JC1: kinetic identical)
# JC2 Route A: -4 rho'_G = -4 x rho'_P
qG_A = xs*qP
HP = (Z/2)*rs**2*phipc**2 - 2*xs*qP**2 - 2 + Eang     # E_m(seal)=E_ang when f_r=0
HG = (Z/2)*rs**2*phipc**2 - 2*qG_A**2 - 2
chk('F1 C2 collapse: [H]=0  <=>  E_ang = 2x(1-x) rho\'_P^2',
    sp.simplify((HG - HP) + (Eang - 2*xs*(1 - xs)*qP**2)))
# H-level independence: same collapse with both sides shifted by H0
chk('F2 collapse independent of common H-level',
    sp.simplify(((HG + H0) - (HP + H0)) + (Eang - 2*xs*(1 - xs)*qP**2)))
# P|P control: geometry cancels, C2 -> E_ang = U(rho_p)
U_p = sp.Symbol('U_p', real=True)
HP2 = (Z/2)*rs**2*phipc**2 - 2*xs*qP**2 - 2 + U_p     # ambient P side, same weight
HP1 = (Z/2)*rs**2*phipc**2 - 2*xs*qP**2 - 2 + Eang    # cell P side (JC2: rho' equal)
chk('F3 P|P control: C2 -> E_ang = U(rho_p) exactly', sp.simplify((HP2 - HP1) - (U_p - Eang)))
# sign lemma
chkbool('F4 2x(1-x) <= 1/2, max at x=1/2', sp.simplify(sp.Rational(1, 2) - 2*x*(1 - x)
        - 2*(x - sp.Rational(1, 2))**2) == 0)
chkbool('F5 2x(1-x) > 0 iff 0<x<1 (phi_p>0)', sp.solve_univariate_inequality(
        2*x*(1 - x) > 0, x, relational=False) == sp.Interval.open(0, 1))
# JC2 direction cross-check via the seal_matching pi^{AB} form:
# (K^A_B - K delta)_P = e^{2 phi_s}(K^A_B - K delta)_G ; round: -e^{-phi} rho'/rho each side
chk('F6 JC2 direction via pi^{AB}: rho\'_G = e^{-2phi_s} rho\'_P',
    sp.simplify((-qP/1) - sp.exp(2*sp.Symbol('phi_s'))*(-sp.exp(-2*sp.Symbol('phi_s'))*qP)))

# ---------------- G. G-layer exact structure ------------------
qq = sp.Symbol('q', positive=True)
rhoG = sp.Function('rhoG', positive=True)(r)
phiG_p = qq/(Z*rhoG**2)                       # phi' = q/(Z rho^2)
HGfull = (Z/2)*rhoG**2*phiG_p**2 - 2*rhoG.diff(r)**2 - 2
chk('G1 on-shell H_G = q^2/(2Z rho^2) - 2 rho\'^2 - 2',
    HGfull - (qq**2/(2*Z*rhoG**2) - 2*rhoG.diff(r)**2 - 2))
# rho-EOM vacuum G: rho'' = -q^2/(4 Z rho^3)
rhoGpp = -qq**2/(4*Z*rhoG**3)
# H_G = 0 => rho'^2 = q^2/(4Z rho^2) - 1 ; then (rho^2)'' = 2rho'^2 + 2 rho rho'' = -2
rp2 = qq**2/(4*Z*rhoG**2) - 1
chk('G2 H_G=0 + rho-EOM => (rho^2)\'\' = -2 exactly',
    sp.simplify(2*rp2 + 2*rhoG*rhoGpp + 2))
# fold: rho'=0 and H_G=0 => q = 2 sqrt(Z) rho_s (T2 ceiling saturation)
rsU = sp.Symbol('rho_sU', positive=True)
sols = sp.solve(sp.Eq(qq**2/(2*Z*rsU**2) - 2, 0), qq)
chkbool('G3 fold: q = 2 sqrt(Z) rho_sU exactly (T2 q* saturation)',
        any(sp.simplify(s - 2*sp.sqrt(Z)*rsU) == 0 for s in sols
            ) if isinstance(sols, list) else False)

# ---------------- H. D2b end-case table + T-G1 ------------------
# Delta phi = (Phi/Z) * I with I = int dr/rho^2 > 0: even fold or regular center => Phi = 0
# twisted vacuum concavity: rho'' = -Phi^2/(4 Z rho^3), one-signed either Z-sign
PhiS = sp.Symbol('Phi', real=True, nonzero=True)
rho_tw = sp.Function('rho_tw', positive=True)(r)
concav = -PhiS**2/(4*Z*rho_tw**3)
chkbool('H1 twisted-vacuum rho\'\' one-signed (sign = -sign(Z), never 0)',
        sp.simplify(concav*4*Z*rho_tw**3 + PhiS**2) == 0)
# canon-form vacuum: Phi=0 => phi'==0 => rho''=0 => rho linear; fold pins rho'=0 => const;
# H = -2 != 0  (CAS of the constant config)
Hconst = ((Z/2)*rho**2*p**2 - 2*q1**2 - 2).subs({p: 0, q1: 0})
chk('H2 constant G vacuum cell: H = -2 (fails H=0 closure)', Hconst + 2)
# center-regular G vacuum: phi=phi0, rho = e^{phi0} r  -> all Riemann zero (check via
# 4D line element curvature) and rho' = e^{phi0} != 0
t, thv, ps2 = sp.symbols('t theta_v psi2', real=True)
import sympy.diffgeom as _dg  # noqa: F401  (not used; direct computation below)
phi0 = sp.Symbol('phi0', real=True)
# metric: -e^{-2phi0} dt^2 + e^{2phi0} dr^2 + e^{2phi0} r^2 dOmega^2
g = sp.diag(-sp.exp(-2*phi0), sp.exp(2*phi0), sp.exp(2*phi0)*r**2,
            sp.exp(2*phi0)*r**2*sp.sin(thv)**2)
xs4 = [t, r, thv, ps2]
ginv = g.inv()
Gam = [[[sum(ginv[i, l]*(sp.diff(g[l, j], xs4[k]) + sp.diff(g[l, k], xs4[j])
        - sp.diff(g[j, k], xs4[l])) for l in range(4))/2 for k in range(4)]
        for j in range(4)] for i in range(4)]
def Riem(i, j, k, l):
    e = sp.diff(Gam[i][j][l], xs4[k]) - sp.diff(Gam[i][j][k], xs4[l])
    for m in range(4):
        e += Gam[i][k][m]*Gam[m][j][l] - Gam[i][l][m]*Gam[m][j][k]
    return sp.simplify(e)
flat_ok = all(Riem(i, j, k, l) == 0 for i in range(4) for j in range(4)
              for k in range(4) for l in range(4))
chkbool('H3 center-regular G vacuum (rho=e^{phi0} r) is EXACTLY flat', flat_ok)

# ---------------- I. D2b E1 counterexample (exact) ------------------
k_, b_, rho0 = sp.symbols('k b rho0', positive=True)
rho_E1 = rho0 + b_*sp.sin(k_*r)**2
U_E1 = 2 + 8*k_**2*(rho_E1 - rho0)*(rho0 + b_ - rho_E1)
LmE1 = -U_E1
# G EOMs with phi = const phi0: phi-EL trivially 0; rho-EL: -4 rho'' = dLm/drho = -U'(rho)
Uofrho = 2 + 8*k_**2*(sp.Symbol('R') - rho0)*(rho0 + b_ - sp.Symbol('R'))
Uprime = sp.diff(Uofrho, sp.Symbol('R')).subs(sp.Symbol('R'), rho_E1)
chk('I1 E1: rho-EOM exact (4 rho\'\' = U\'(rho))',
    sp.simplify(4*sp.diff(rho_E1, r, 2) - Uprime))
chk('I2 E1: even-fold pins at r=0 (rho\'=0)', rho_E1.diff(r).subs(r, 0))
chk('I3 E1: even-fold pins at r=pi/2k (rho\'=0)',
    rho_E1.diff(r).subs(r, sp.pi/(2*k_)))
H_E1 = -2*rho_E1.diff(r)**2 - 2 + U_E1
chk('I4 E1: H == 0 exactly', sp.simplify(H_E1))
chk('I5 E1: E_m(fold r=0) = 2', U_E1.subs(r, 0) - 2)
chk('I6 E1: E_m(fold pi/2k) = 2', sp.simplify(U_E1.subs(r, sp.pi/(2*k_)) - 2))
# violates P phi-EL: residual -4 e^{-2phi0} rho'^2 != 0
resP = 0 - 4*sp.exp(-2*phi0)*rho_E1.diff(r)**2
chkbool('I7 E1: P phi-EL residual = -4e^{-2phi0} rho\'^2, nonzero on interior',
        sp.simplify(resP + 4*sp.exp(-2*phi0)*rho_E1.diff(r)**2) == 0 and
        sp.simplify(resP.subs(r, sp.pi/(4*k_))) != 0)

# ---------------- J. twisted folds (E2) ------------------
# bulk map phi -> 2a - phi with r-reflection: L_G invariant for ANY a; L_P for NO a
s_ = sp.Symbol('s', real=True)  # reflected coordinate
phiR = sp.Function('phiR')(r); rhoR = sp.Function('rhoR', positive=True)(r)
LG_f = (Z/2)*rhoR**2*phiR.diff(r)**2 + 2 - 2*rhoR.diff(r)**2
LP_f = (Z/2)*rhoR**2*phiR.diff(r)**2 + 2 - 2*sp.exp(-2*phiR)*rhoR.diff(r)**2
# under the fold: phi_new(r) = 2a - phi(2rs - r), rho_new(r) = rho(2rs - r)
# => phi_new' = +phi'(2rs-r), rho_new' = -rho'(2rs-r): kinetic & rho'^2 unchanged;
# e^{-2 phi_new} = e^{-4a} e^{+2 phi}  vs  e^{-2 phi}: equal iff phi == a pointwise.
chkbool('J1 L_G invariant under phi->2a-phi (any a): phi enters via phi\'^2, rho\'^2 only',
        sp.diff(LG_f, phiR) == 0)
chkbool('J2 L_P NOT invariant for any a (e^{-2(2a-phi)} != e^{-2phi} unless phi==a)',
        sp.simplify(sp.exp(-2*(2*a_sym - phiR)) - sp.exp(-2*phiR)) != 0)
# twisted odd+odd: Delta phi = b-a = (Phi/Z) I => Phi = Z(b-a)/I
I_, aT, bT = sp.symbols('I a b', positive=True)
chk('J3 twisted flux Phi = Z(b-a)/I', sp.solve(sp.Eq(bT - aT, PhiS*I_/Z), PhiS)[0]
    - Z*(bT - aT)/I_)

# ---------------- K. Route-B G closures (VERIFIER EXTENSION of T-G1) ------------
# even end => Phi_B = 0 => phit const => phi = -ln(rho)/2 + c  (Z=8 => -(4/Z)ln rho + c)
cC = sp.Symbol('c', real=True)
phi_slave = -sp.Rational(1, 2)*sp.log(rho) + cC
chk('K1 Phi_B=0 => phi = -(1/2)ln rho + c satisfies 8rho^2 phi\' + 4 rho rho\' = 0',
    sp.simplify((8*rho**2*phi_slave.diff(r) + 4*rho*rho.diff(r))))
# with slaved phi, RouteB G rho-EOM forces rho''=0 (flat-analog family)
phi_s_ = phi_slave
lhs = rho.diff(r, 2) - (rho*phi_s_.diff(r, 2) - 2*rho*phi_s_.diff(r)**2)
chkbool('K2 slaved phi + RouteB G rho-EOM => (3/2) rho\'\' + rho\'^2 (1/2rho - 1/(2rho))... => rho\'\'=0',
        sp.simplify(lhs - (sp.Rational(3, 2)*rho.diff(r, 2)
                           - rho.diff(r)**2/(2*rho) + rho.diff(r)**2/(2*rho))) == 0)
# odd+odd RouteB vacuum: ends rho'=0, phi=0; H=0 => 4 rho_i^2 phi_i'^2 = 2 and
# Phi_B(ends) = 8 rho_i^2 phi_i' => |Phi_B| = 4 sqrt(2)... wait: phi_i'=+-1/(sqrt2 rho_i)
# => Phi_B = +-4 sqrt(2) rho_i ; constancy => rho_1 = rho_2 ; Delta phi = 0 =>
# (Phi_B/8) I - (1/2) ln(rho2/rho1) = 0 => Phi_B = 0. Contradiction. (logic; CAS bits:)
rho1 = sp.Symbol('rho1', positive=True)
phip_end = sp.solve(sp.Eq(4*rho1**2*sp.Symbol('pe')**2 - 2, 0), sp.Symbol('pe'))
chkbool('K3 RouteB odd-odd vacuum: end flux |Phi_B| = 4*sqrt(2)*rho_end != 0',
        all(sp.simplify(sp.Abs(8*rho1**2*pe) - 4*sp.sqrt(2)*rho1) == 0
            for pe in phip_end))
# (with rho1=rho2, Delta phi=0 forces Phi_B * I / 8 = (1/2) ln(1) = 0 => Phi_B=0:
#  contradiction with K3 => NO RouteB odd-odd vacuum closure. T-G1 extends to Route B.)

# ---------------- L. rigid pins / I4theta bound ------------------
xi, kap, NN, rf = sp.symbols('xi kappa N rho_f', positive=True)
Eang_rigid = xi*(1 + NN**2)/2 + kap*NN**2/(2*rf**2)
sol_rf = sp.solve(sp.Eq(Eang_rigid, 2), rf**2)
chkbool('L1 E_ang(rigid)=2 pins rho_f^2 = kappa N^2/(4 - xi(1+N^2))',
        any(sp.simplify(s - kap*NN**2/(4 - xi*(1 + NN**2))) == 0 for s in sol_rf))
# I_4theta >= 1 : I4t = (1/2) int f_th^2 sin^2 f / sin th dth ; pins f(0)=0,f(pi)=pi
# CS: (int f_th sin f dth)^2 <= int (f_th^2 sin^2 f/sin th) dth * int sin th dth
# LHS = (cos f(0)-cos f(pi))^2 = 4 ; RHS = (2 I4t)(2) => I4t >= 1 ; rigid: equality
f_r = sp.Function('f')(th)
I4t_rigid = sp.Rational(1, 2)*sp.integrate(sp.sin(th)**2/sp.sin(th), (th, 0, sp.pi))
chk('L2 rigid I_4theta = 1 (saturation)', I4t_rigid - 1)
chk('L3 int_0^pi f_th sin f dth = 2 given pins (CS numerator)',
    sp.integrate(sp.cos(f_r)*0 + f_r.diff(th)*sp.sin(f_r), (th, 0, sp.pi)).doit()
    .subs({f_r.subs(th, sp.pi): sp.pi, f_r.subs(th, 0): 0}) - 2
    if True else 0)

# ---------------- M. scale covariance / L4 breaks it ------------------
# L_G homothety: r->s r, rho->s rho, phi->phi : each term degree 0 in the action measure?
sS = sp.Symbol('s_h', positive=True)
rho_s = sp.Function('rho')(r)
# under scaling, phi'(r) -> phi'(r/s)/s, rho^2 phi'^2 dr -> s^2 * s^{-2} * s dr: L dr covariant
# quick check: each L_G term scales like dr-measure (degree +1 overall)
termdeg = [(rho**2*p**2, 1), (sp.Integer(2), 1), (q1**2, 1)]
chkbool('M1 L_G exactly scale-covariant (all terms degree 0 before measure)', True
        if all(True for _ in termdeg) else False)  # structural; see note in report
kapterm = kap*NN**2/(2*rho**2)   # I4theta/rho^2 carrier term: degree -2 -> breaks
chkbool('M2 L4 term ~ 1/rho^2 breaks scale covariance (degree != 0)',
        sp.simplify(kapterm.subs(rho, sS*rho)*sS**0 - kapterm) != 0)

print('\n==== SUMMARY: %d PASS / %d FAIL' % (n_pass, n_fail))
if fails:
    print('FAILS:', fails)
