"""d2c_part1_mixing.py -- D2c PART 1: discharge the Z=8/Route-B mixing-term tension (CAS).

Task (microphysics_D2_two_regime_MAP.md, gate (a)): the live solvers carry Z_phi=8 ("route-B
value") while Route B's action carries a FORCED mixing term 2 sqrt(h) e^phi K phi' that the
current EOMs omit (f_rtheta_free_field_MAP.md:116-121; native_geometric_action_results.md:74-78,
123-126: "Z_phi=8 and D=2 are an INSEPARABLE package").

This script DERIVES, in the round-static reduction (h = rho(r)^2 Omega, static, diagonal --
inherited CHOSE x3), the mixing term's contribution to:
  (a) the bulk EOMs of both branches (does it vanish identically in round-static? NO -- exact
      residuals computed);
  (b) the fold pins of the banked universe cell (even fold r_c, odd fold r_s -- do the banked
      pins survive? YES, exactly);
  (c) the junction conditions at a G|P seal (JC1/JC2 become COUPLED; corrected forms derived);
  (d) the conserved Hamiltonian / transversality closure (E_ang(core)=2 survives Route B).

Conventions (all cited):
  Native action  S = INT c sqrt(h) [ (Z/2) phi'^2 + R2 + W K2 ]   (native_geometric_action:13)
  K_AB = (1/2) e^{-phi} d_r h_AB ;  K2 = K_AB K^AB - K^2 ;  W = e^{2phi} (G) / 1 (P)
  Route B: kinetic block -> sqrt(h) [ 4 phi'^2 + 2 e^phi K phi' ]  (Z=8, D=2; line 74)
  Round reduction per 4pi steradian (Step-0 V2, f2d_virial_step0_results.md:34-38):
    Lbar_P^A = (Z/2) rho^2 phi'^2 + 2 - 2 e^{-2phi} rho'^2   (+ matter)
    Lbar_G^A = (Z/2) rho^2 phi'^2 + 2 - 2 rho'^2
Run: python3 d2c_part1_mixing.py   (prints PASS/FAIL per check; all symbolic, seconds)
"""
import sympy as sp

r, th, lam = sp.symbols('r theta lambda', real=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)

checks = []
def check(name, cond):
    ok = bool(cond)
    checks.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name)

# ---------------------------------------------------------------- M1: round reduction of the mixing term
# h_AB = rho^2 * diag(1, sin^2 th);  K_AB = (1/2) e^{-phi} h_AB'
h = sp.Matrix([[rho**2, 0], [0, rho**2*sp.sin(th)**2]])
hp = h.diff(r)
hinv = h.inv()
K_AB = sp.Rational(1, 2)*sp.exp(-phi)*hp
Kmix = (hinv*K_AB).trace()                      # K = h^{AB} K_AB
K2 = ((hinv*K_AB*hinv*K_AB).trace() - Kmix**2)  # K_AB K^AB - K^2
sqrth = sp.sqrt(h.det())                        # rho^2 sin th  (th in (0,pi))
sqrth = sp.simplify(sp.refine(sqrth, sp.Q.positive(sp.sin(th))))

check('M1a: K = 2 e^{-phi} rho\'/rho (round)',
      sp.simplify(Kmix - 2*sp.exp(-phi)*rho.diff(r)/rho) == 0)
check('M1b: K2 = -2 e^{-2phi} rho\'^2/rho^2 (round)',
      sp.simplify(K2 + 2*sp.exp(-2*phi)*rho.diff(r)**2/rho**2) == 0)
check('M1c: (sqrt h)\' = sqrt(h) e^phi K  (the banked IBP identity, line 74)',
      sp.simplify(sqrth.diff(r) - sqrth*sp.exp(phi)*Kmix) == 0)
mixing_red = sp.simplify(2*sqrth*sp.exp(phi)*Kmix*phi.diff(r))
check('M1d: mixing term 2 sqrt(h) e^phi K phi\' = 4 rho rho\' phi\' * sin th',
      sp.simplify(mixing_red - 4*rho*rho.diff(r)*phi.diff(r)*sp.sin(th)) == 0)

# ---------------------------------------------------------------- M2: shift-invariance (branch-blind)
# Under phi -> phi + lam (Branch-G depth-shift): K -> e^{-lam} K, e^phi -> e^{lam} e^phi, phi' inv.
K_AB_sh = sp.Rational(1, 2)*sp.exp(-(phi+lam))*hp
K_sh = (hinv*K_AB_sh).trace()
mix_sh = 2*sqrth*sp.exp(phi+lam)*K_sh*(phi+lam).diff(r)
check('M2: e^phi K phi\' is EXACTLY shift-invariant -> the mixing term needs NO W_chi'
      ' compensator; its form is BRANCH-BLIND',
      sp.simplify(mix_sh - mixing_red) == 0)

# ---------------------------------------------------------------- reduced Lagrangians (per 4pi)
rp_, pp_ = rho.diff(r), phi.diff(r)
Lmix = 4*rho*rp_*pp_                              # M1d, per 4pi
LP_A = (Z/2)*rho**2*pp_**2 + 2 - 2*sp.exp(-2*phi)*rp_**2        # Route-A P (Step-0 V2, vacuum)
LG_A = (Z/2)*rho**2*pp_**2 + 2 - 2*rp_**2                        # Route-A G
LP_B = LP_A.subs(Z, 8) + Lmix                                    # Route-B P
LG_B = LG_A.subs(Z, 8) + Lmix                                    # Route-B G

def EL(L, q):
    return sp.simplify(sp.diff(L, q) - sp.diff(sp.diff(L, q.diff(r)), r))

# ---------------------------------------------------------------- M3: Route-B P bulk EOMs + non-vanishing
ELphi_PB = EL(LP_B, phi)   # = 4 e^{-2phi} rho'^2 - d/dr(8 rho^2 phi' + 4 rho rho')
ELrho_PB = EL(LP_B, rho)
# claimed forms:
claim_phi_PB = 4*sp.exp(-2*phi)*rp_**2 - sp.diff(8*rho**2*pp_ + 4*rho*rp_, r)
claim_rho_PB = 8*rho*pp_**2 + 4*sp.exp(-2*phi)*rp_*pp_*0 \
    - 4*rho*phi.diff(r, 2) + 4*sp.diff(sp.exp(-2*phi)*rp_, r) + 8*rho*pp_**2*0
check('M3a: Route-B P phi-EOM  ==  4 e^{-2phi} rho\'^2 - (8 rho^2 phi\' + 4 rho rho\')\' = 0',
      sp.simplify(ELphi_PB - claim_phi_PB) == 0)
# mixing contribution to each EL (Route B minus Route A at Z=8):
dphi = sp.simplify(EL(LP_B, phi) - EL(LP_A.subs(Z, 8), phi))
drho = sp.simplify(EL(LP_B, rho) - EL(LP_A.subs(Z, 8), rho))
check('M3b: mixing adds  -4(rho rho\')\'  to the phi-EL (NOT identically zero in round-static)',
      sp.simplify(dphi + 4*sp.diff(rho*rp_, r)) == 0 and dphi != 0)
check('M3c: mixing adds  -4 rho phi\'\'  to the rho-EL (NOT identically zero)',
      sp.simplify(drho + 4*rho*phi.diff(r, 2)) == 0 and drho != 0)
# solved Route-B P system (vacuum):  from ELphi=0, ELrho=0
rho2 = sp.Function('varrho')(r)  # scratch
sol = sp.solve([ELphi_PB, ELrho_PB], [phi.diff(r, 2), rho.diff(r, 2)], dict=True)[0]
check('M3d: Route-B P rho-EOM solves to  rho\'\' = 2 phi\' rho\' + e^{2phi} rho (phi\'\' - 2 phi\'^2)'
      '  [checked as the coupled solved system]',
      sp.simplify(sol[rho.diff(r, 2)]
                  - (2*pp_*rp_ + sp.exp(2*phi)*rho*(sol[phi.diff(r, 2)] - 2*pp_**2))) == 0)

# ---------------------------------------------------------------- M4: Route-B G EOMs + the flat test
ELphi_GB = EL(LG_B, phi)
ELrho_GB = EL(LG_B, rho)
check('M4a: Route-B G phi-EOM = -(8 rho^2 phi\' + 4 rho rho\')\' = 0  (conserved Phi_B)',
      sp.simplify(ELphi_GB + sp.diff(8*rho**2*pp_ + 4*rho*rp_, r)) == 0)
# FLAT SPACE TEST: rho = r, phi = const is NOT a Route-B G solution:
flat = {phi: sp.Integer(0), rho: r}
res_flat = ELphi_GB.subs({phi.diff(r, 2): 0, pp_: 0, rho.diff(r, 2): 0, rp_: 1, rho: r})
check('M4b: FLAT (rho=r, phi=const) FAILS the Route-B G phi-EOM (residual -4, not 0):'
      ' the mixing term SOURCES phi on flat angular geometry',
      sp.simplify(res_flat + 4) == 0)
# the Route-B G "flat-analog" family: rho = a r + b (rho''=0), phi = phi0 - (1/2) ln rho
a_, b_, phi0 = sp.symbols('a b phi_0', real=True)
rho_f = a_*r + b_
phi_f = phi0 - sp.Rational(1, 2)*sp.log(rho_f)
subs_f = {phi.diff(r, 2): phi_f.diff(r, 2), phi.diff(r): phi_f.diff(r), phi: phi_f,
          rho.diff(r, 2): rho_f.diff(r, 2), rho.diff(r): rho_f.diff(r), rho: rho_f}
check('M4c: Route-B G admits  rho = a r + b,  phi = phi0 - (1/2) ln rho  (both EOMs): the'
      ' Route-B vacuum is DEFORMED (phi not constant on areal slices)',
      sp.simplify(ELphi_GB.subs(subs_f)) == 0 and sp.simplify(ELrho_GB.subs(subs_f)) == 0)

# ---------------------------------------------------------------- M5: field redefinition phi~ = phi + (1/2) ln rho
phit = sp.Function('phitilde')(r)
Lkin_B = 8*rho**2*pp_**2/2 + Lmix        # 4 rho^2 phi'^2 + 4 rho rho' phi'
subs_t = {phi.diff(r): phit.diff(r) - rp_/(2*rho), phi: phit - sp.log(rho)/2}
check('M5: Route-B kinetic block == 4 rho^2 phitilde\'^2 - rho\'^2  with phitilde = phi + (1/2)ln rho'
      ' (Route B = Z=8 Route-A kinetic in the SHIFTED field, minus an extra rho\'^2 gradient term)',
      sp.simplify(Lkin_B.subs(subs_t) - (4*rho**2*phit.diff(r)**2 - rp_**2)) == 0)

# ---------------------------------------------------------------- M6: even-fold natural BCs under Route B
pP, rP = sp.symbols("phip rhop", real=True)   # phi'(r_c), rho'(r_c)
Pi_phi_B = 8*rho**2*pP + 4*rho*rP             # dLbar_P^B/dphi'
pi_rho_B = -4*sp.exp(-2*phi)*rP + 4*rho*pP    # dLbar_P^B/drho'
solBC = sp.solve([Pi_phi_B, pi_rho_B], [pP, rP], dict=True)
check('M6: Route-B even-fold natural BCs (pi_phi = pi_rho = 0) STILL force phi\'=rho\'=0'
      ' uniquely (the 2x2 momentum map is nondegenerate: det = -32 rho^2 e^{-2phi} - 16 rho^2 != 0)',
      solBC == [{pP: 0, rP: 0}])

# ---------------------------------------------------------------- M7: odd-fold pins under Route B
# Mirror-image partner across r_s (universe_cell_fold_jc_sigma_results.md D1, odd canon phi->-phi):
#   phi~(r) = -phi(2 r_s - r)  => at the fold: phi~ = -phi_s (continuity => phi_s = 0 as banked),
#   phi~' = +phi'_s ;  rho~(r) = rho(2 r_s - r) => rho~' = -rho'_s.
ps, rs_, rhos, phis = sp.symbols("phis_p rhos_p rho_s phi_s", real=True)
pi_rho_side = lambda w, rpv, ppv: -4*w*rpv + 4*rhos*ppv     # w = e^{-2phi} weight on that side
jump_rho = sp.simplify(pi_rho_side(sp.exp(+2*phis), -rs_, ps) - pi_rho_side(sp.exp(-2*phis), rs_, ps))
check('M7a: Route-B odd-fold [pi_rho] = 8 cosh(2 phi_s) rho\'_s  -- the MIXING CONTRIBUTIONS'
      ' CANCEL IN THE JUMP; the banked pin rho\'(r_s)=0 survives Route B for ANY phi_s',
      sp.simplify(jump_rho - 8*sp.cosh(2*phis)*rs_) == 0)
Pi_side = lambda rpv, ppv: 8*rhos**2*ppv + 4*rhos*rpv
jump_phi = sp.simplify(Pi_side(-rs_, ps) - Pi_side(rs_, ps))
check('M7b: Route-B odd-fold [Pi_phi] = -8 rho_s rho\'_s -> vanishes IDENTICALLY once rho\'_s=0:'
      ' phi\'(r_s) stays FREE; fold flux Phi_B(r_s) = 8 rho_s^2 phi\'_s (Route-A Z=8 form) =>'
      ' "fold VALUES unchanged" (universe doc L70-71) CONFIRMED',
      sp.simplify(jump_phi + 8*rhos*rs_) == 0 and sp.simplify(Pi_side(0, ps) - 8*rhos**2*ps) == 0)

# ---------------------------------------------------------------- M8: Hamiltonian + conservation + flux law
H_A = sp.simplify(pp_*sp.diff(LP_A.subs(Z, 8), pp_) + rp_*sp.diff(LP_A.subs(Z, 8), rp_) - LP_A.subs(Z, 8))
H_B = sp.simplify(pp_*sp.diff(LP_B, pp_) + rp_*sp.diff(LP_B, rp_) - LP_B)
check('M8a: H^B = H^A(Z=8) + 4 rho rho\' phi\'  (the mixing survives INTO H off the folds;'
      ' at any fold point rho\'=0 the correction vanishes)',
      sp.simplify(H_B - H_A - 4*rho*rp_*pp_) == 0)
# conservation on-shell (Route-B P vacuum):
onshell = {phi.diff(r, 2): sol[phi.diff(r, 2)], rho.diff(r, 2): sol[rho.diff(r, 2)]}
check('M8b: dH^B/dr = 0 on the Route-B P EOMs (autonomy -> H-machinery intact)',
      sp.simplify(H_B.diff(r).subs(onshell)) == 0)
# Route-B flux law: Phi_B' = 4 e^{-2phi} rho'^2  (from the phi-EOM directly)
PhiB = 8*rho**2*pp_ + 4*rho*rp_
check('M8c: Route-B P flux law  Phi_B\' = 4 e^{-2phi} rho\'^2 >= 0  with Phi_B = 8 rho^2 phitilde\';'
      ' MONOTONICITY MIGRATES from phi to phitilde = phi + (1/2) ln rho',
      sp.simplify((PhiB.diff(r) - 4*sp.exp(-2*phi)*rp_**2).subs(onshell)) == 0)
check('M8d: even-fold H^B value = E_ang - 2 (geometry part -> -2 at phi\'=rho\'=0):'
      ' transversality H=0 STILL closes to E_ang(core) = 2 under Route B',
      sp.simplify(H_B.subs({pp_: 0, rp_: 0})) == -2)

# ---------------------------------------------------------------- M9: Route-B G|P junction conditions (coupled)
# P inside / G outside at seal s; phi, rho continuous (posture CHOSE-cited).  Unknowns: G-side slopes.
pPv, rPv, pGv, rGv = sp.symbols("phiP rhoP phiG rhoG", real=True)   # phi'_P, rho'_P, phi'_G, rho'_G
JC1B = sp.Eq(8*rhos**2*pPv + 4*rhos*rPv, 8*rhos**2*pGv + 4*rhos*rGv)          # [Pi_phi]=0
JC2B = sp.Eq(-4*sp.exp(-2*phis)*rPv + 4*rhos*pPv, -4*rGv + 4*rhos*pGv)        # [pi_rho]=0
solJ = sp.solve([JC1B, JC2B], [pGv, rGv], dict=True)[0]
check('M9a: Route-B G|P JCs are COUPLED but uniquely solvable:  rho\'_G = (2 e^{-2phi_s} + 1)/3 * rho\'_P',
      sp.simplify(solJ[rGv] - (2*sp.exp(-2*phis) + 1)/3*rPv) == 0)
check('M9b: phi\' JUMPS under Route B:  phi\'_G - phi\'_P = (1 - e^{-2phi_s}) rho\'_P / (3 rho_s)'
      ' (Route A had phi\' continuous; the jump vanishes iff phi_s = 0 or rho\'_P = 0)',
      sp.simplify(solJ[pGv] - pPv - (1 - sp.exp(-2*phis))*rPv/(3*rhos)) == 0)
check('M9c: JC1 in tilde variables = [8 rho^2 phitilde\'] = 0 (phitilde\' CONTINUOUS: the Route-B'
      ' dilation flux is the SHIFTED-field flux)',
      sp.simplify((solJ[pGv] + solJ[rGv]/(2*rhos)) - (pPv + rPv/(2*rhos))) == 0)

# ---------------------------------------------------------------- M10: Route-B C2 (H-balance) collapse at G|P
Eang = sp.symbols('E_ang', positive=True)
H_B_P_seal = 8*rhos**2*pPv**2/2 + 4*rhos*rPv*pPv - 2*sp.exp(-2*phis)*rPv**2 - 2 + Eang  # f_r=0: H_m=E_ang
H_B_G_seal = 8*rhos**2*pGv**2/2 + 4*rhos*rGv*pGv - 2*rGv**2 - 2
C2B = sp.simplify((H_B_P_seal - H_B_G_seal).subs({pGv: solJ[pGv], rGv: solJ[rGv]}))
x = sp.symbols('x', positive=True)   # x = e^{-2 phi_s}
C2B_x = sp.simplify(C2B.subs(sp.exp(-2*phis), x))
claim = Eang - sp.Rational(2, 3)*(1 + 2*x)*(1 - x)*rPv**2
check('M10a: Route-B C2 collapses to  E_ang(r_p) = (2/3)(1 + 2x)(1 - x) rho\'_P^2 ,  x = e^{-2 phi_p}'
      ' (the geometry does NOT cancel at a G|P seal; the residue is the W_chi weight-jump)',
      sp.simplify(C2B_x - claim) == 0)
check('M10b: SIGN: RHS > 0  iff  x < 1  iff  phi_p > 0  -- the SAME sign condition as Route A'
      ' (see part 2 G3); Route-blind at the seal, but Route B relaxes the phi<=0 monotonicity chain',
      sp.simplify((sp.Rational(2, 3)*(1 + 2*x)*(1 - x)).subs(x, 1)) == 0
      and (sp.Rational(2, 3)*(1 + 2*1.5)*(1 - 1.5)) < 0
      and (sp.Rational(2, 3)*(1 + 2*sp.Rational(1, 2))*(1 - sp.Rational(1, 2))) > 0)

# ----------------------------------------------------------------
n_ok = sum(1 for _, ok in checks if ok)
print(f"\n{n_ok}/{len(checks)} checks PASS")
if n_ok != len(checks):
    raise SystemExit(1)
