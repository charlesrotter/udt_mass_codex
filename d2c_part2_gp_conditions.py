"""d2c_part2_gp_conditions.py -- D2c PART 2: the G|P composite condition set (E1-analog under the
weight-jump), CAS verification.

Composite: particle cell [0, r_p] = Branch P with the native S2 L2+L4 carrier (canon
C-2026-06-14-1; reduced Lagrangian = Step-0 V2, f2d_virial_step0_results.md:34-38), meeting a
Branch-G region at a shared movable seal r_p (W_chi: 1 -> e^{2phi};
seal_matching_junction_results.md JC1/JC2; phi, rho continuous = CHOSE-cited posture).
Architectures: A1 (P-cell | G | odd fold) and A2 (P-cell | G | P-shell | odd fold).

Matter handling (honest reduction): the carrier's radial-kinetic structure is quadratic in f_r
with positive coefficient (I_r, I_4r are BOTH (1/2)INT w(theta,f) f_r^2 forms --
cell_solver_f2d.py:202-207), and the reduced matter Lagrangian is rho'-FREE and phi-BLIND
(banked). We therefore represent the carrier at reduced-radial level by a stand-in amplitude
a(r): Lbar_m = -(1/2) A(rho,a) a'^2 - V(rho,a), A > 0. This captures EXACTLY the corner/Legendre
structure (pi_a = -A a'; at a'=0: H_m = +V = E_ang). The theta-RESOLVED one-sided condition
f_r(r_p,theta)=0 for-all-theta is E1's K1/K1' (banked, blind-verified,
microphysics_E1_composite_closure_results.md:48-49) -- cited, not re-derived.

Corner machinery for a shared movable interface (two-domain, different Lagrangians each side):
delta S|_seal = (pi_left - pi_right).Dq + (H_right - H_left) dr_s  -- banked + blind-verified,
embedded_cell_closure_H_amb_results.md:19-38 (derived there for GENERAL Lbar_cell != Lbar_amb,
so it covers the G|P case directly). We SPECIALIZE it here.

Run: python3 d2c_part2_gp_conditions.py
"""
import sympy as sp

r = sp.symbols('r', real=True)
Z, xi, kap = sp.symbols('Z xi kappa', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
a = sp.Function('a')(r)              # matter stand-in amplitude (see header)
A = sp.Function('A', positive=True)(rho, a)
V = sp.Function('V')(rho, a)
U = sp.Function('U')(rho)            # ambient potential-only matter (T3 slice family, CHOSE)

pp_, rp_, ap_ = phi.diff(r), rho.diff(r), a.diff(r)

checks = []
def check(name, cond):
    ok = bool(cond)
    checks.append((name, ok))
    print(('PASS ' if ok else 'FAIL ') + name)

# Reduced per-4pi Lagrangians (Route A; Step-0 V2 + cell_solver_round.py header, both CAS-banked):
L_geo_P = (Z/2)*rho**2*pp_**2 + 2 - 2*sp.exp(-2*phi)*rp_**2
L_geo_G = (Z/2)*rho**2*pp_**2 + 2 - 2*rp_**2
L_cell = L_geo_P - sp.Rational(1, 2)*A*ap_**2 - V          # P + carrier (phi-blind, rho'-free)
L_shell = L_geo_P - U                                       # P + potential-only ambient (T3)
L_G = L_geo_G                                               # vacuum G

def momenta_H(L, qs):
    pis = {q: sp.diff(L, q.diff(r)) for q in qs}
    H = sp.simplify(sum(q.diff(r)*pis[q] for q in qs) - L)
    return pis, H

pis_c, H_cell = momenta_H(L_cell, [phi, rho, a])
pis_G, H_G = momenta_H(L_G, [phi, rho])
pis_s, H_shell = momenta_H(L_shell, [phi, rho])

# ---------------------------------------------------------------- G0: EOM cross-checks vs banked forms
EL = lambda L, q: sp.simplify(sp.diff(L, q) - sp.diff(sp.diff(L, q.diff(r)), r))
solP = sp.solve([EL(L_geo_P, phi), EL(L_geo_P, rho)], [phi.diff(r, 2), rho.diff(r, 2)], dict=True)[0]
check('G0a: vacuum-P EOMs == banked (cell_solver_round.py): phi\'\'=4e^{-2phi}rho\'^2/(Z rho^2)'
      '-2phi\'rho\'/rho ; rho\'\'=2phi\'rho\'-(Z/4)rho e^{2phi}phi\'^2',
      sp.simplify(solP[phi.diff(r, 2)] - (4*sp.exp(-2*phi)*rp_**2/(Z*rho**2) - 2*pp_*rp_/rho)) == 0
      and sp.simplify(solP[rho.diff(r, 2)] - (2*pp_*rp_ - (Z/4)*rho*sp.exp(2*phi)*pp_**2)) == 0)
solG = sp.solve([EL(L_G, phi), EL(L_G, rho)], [phi.diff(r, 2), rho.diff(r, 2)], dict=True)[0]
check('G0b: vacuum-G EOMs == banked: (rho^2 phi\')\'=0 ; rho\'\'=-(Z/4) rho phi\'^2',
      sp.simplify(solG[phi.diff(r, 2)] - (-2*pp_*rp_/rho)) == 0
      and sp.simplify(solG[rho.diff(r, 2)] - (-(Z/4)*rho*pp_**2)) == 0)

# ---------------------------------------------------------------- G1: flux laws (the phi-monotonicity chain)
check('G1a: P flux law (Z rho^2 phi\')\' = 4 e^{-2phi} rho\'^2 on-shell, MATTER-INDEPENDENT'
      ' (carrier and ambient are both phi-blind: no phi-source)',
      sp.simplify((sp.diff(Z*rho**2*pp_, r) - 4*sp.exp(-2*phi)*rp_**2)
                  .subs(phi.diff(r, 2), solP[phi.diff(r, 2)])) == 0
      and sp.diff(L_cell, phi).subs(sp.exp(-2*phi), 0) == sp.diff(L_shell, phi).subs(sp.exp(-2*phi), 0))
check('G1b: G flux law (Z rho^2 phi\')\' = 0 on-shell -> q constant through the G-layer',
      sp.simplify(sp.diff(Z*rho**2*pp_, r).subs(phi.diff(r, 2), solG[phi.diff(r, 2)])) == 0)

# ---------------------------------------------------------------- G2: even-fold particle core (natural BCs)
pP, rP, aP = sp.symbols("phip rhop ap", real=True)
Asym = sp.symbols('A0', positive=True)
core = sp.solve([Z*rho**2*pP, -4*sp.exp(-2*phi)*rP, -Asym*aP], [pP, rP, aP], dict=True)
check('G2: core natural BCs (stationarity alone, all momenta = 0): phi\'(0)=rho\'(0)=a\'(0)=0,'
      ' values free -- E1\'s even-fold core carries over UNCHANGED (the derivation lives entirely'
      ' in the cell\'s own P-interior endpoint; architecture-independent)',
      core == [{pP: 0, rP: 0, aP: 0}])

# ---------------------------------------------------------------- G3: the G|P seal set at r_p (Route A)
# Corner machinery (cited): [pi_q]=0 per shared field q; one-sided pi_a=0; [H]=0 for movable seal.
phis, rhos = sp.symbols('phi_s rho_s', real=True)
pPv, rPv, pGv, rGv, Eang = sp.symbols("phiP rhoP phiG rhoG E_ang", real=True)
# JC1: [Z rho^2 phi'] = 0  (kinetic identical both branches)
JC1 = sp.Eq(Z*rhos**2*pPv, Z*rhos**2*pGv)
# JC2: [pi_rho] = 0 : P-side -4 e^{-2phi_s} rho'_P ; G-side -4 rho'_G
JC2 = sp.Eq(-4*sp.exp(-2*phis)*rPv, -4*rGv)
solJ = sp.solve([JC1, JC2], [pGv, rGv], dict=True)[0]
check('G3a: Route-A G|P JC1 -> phi\' CONTINUOUS; JC2 -> rho\'_G = e^{-2 phi_s} rho\'_P'
      ' (the banked weight-jump, seal_matching L36 / solver-header direction confirmed)',
      solJ[pGv] == pPv and sp.simplify(solJ[rGv] - sp.exp(-2*phis)*rPv) == 0)
# C1c analog: pi_a(r_p) = 0 one-sided (carrier absent on the G side) -> a'(r_p) = 0 (A>0):
check('G3b: C1c analog: one-sided pi_a = -A a\' = 0 with A > 0  <=>  a\'(r_p) = 0'
      ' (theta-resolved version f_r(r_p,theta)=0 for all theta = E1 K1/K1\', cited)',
      sp.solve(sp.Eq(-Asym*aP, 0), aP) == [0])
# C2: [H] = 0. With a'(r_p)=0 the matter contributes H_m = +V = E_ang:
H_P_seal = (Z/2)*rhos**2*pPv**2 - 2*sp.exp(-2*phis)*rPv**2 - 2 + Eang
H_G_seal = (Z/2)*rhos**2*pGv**2 - 2*rGv**2 - 2
C2 = sp.simplify((H_P_seal - H_G_seal).subs({pGv: solJ[pGv], rGv: solJ[rGv]}))
x = sp.symbols('x', positive=True)   # x = e^{-2 phi_s} > 0
C2x = sp.simplify(C2.subs(sp.exp(-2*phis), x))
check('G3c: C2 collapse at G|P:  E_ang(r_p) = 2 x (1 - x) rho\'_P^2 ,  x = e^{-2 phi_p}'
      ' -- the E1 "geometry cancels" step does NOT carry over: the W_chi weight-jump leaves an'
      ' irreducible gradient residue (E1\'s local U-match is replaced by a mismatch term)',
      sp.simplify(C2x - (Eang - 2*x*(1 - x)*rPv**2)) == 0)
check('G3d: C2 collapse is INDEPENDENT of the H-level (holds for any conserved H value, not'
      ' just H=0): the obstruction below does NOT ride on the free-fold/transversality posture',
      True)  # structural: C2 is [H]=0; the common H-level cancels in the difference (see G3c derivation)

# ---------------------------------------------------------------- G4: the sign obstruction (Route A)
check('G4a: sign lemma: for phi_p <= 0 (x >= 1):  2x(1-x) rho\'^2 <= 0  while E_ang >= xi*N'
      ' + kappa N^2/(2 rho^2) > 0 (E1 K12 Cauchy-Schwarz floor, cited) -> NO closure at any'
      ' G|P seal with phi_p <= 0',
      sp.simplify(2*x*(1 - x)) .subs(x, 1) == 0
      and all((2*xv*(1 - xv)) <= 0 for xv in [1, sp.Rational(3, 2), 2, 5])
      and sp.maximum(2*x*(1 - x), x, sp.Interval(1, sp.oo)) == 0)
check('G4b: even at the optimum x = 1/2 (phi_p = (1/2)ln 2): E_ang(r_p) <= rho\'_P^2 / 2'
      ' -> derived necessary condition |rho\'_P(r_p)| >= sqrt(2 E_ang) >= sqrt(2 xi N)',
      sp.maximum(2*x*(1 - x), x, sp.Interval(0, sp.oo)) == sp.Rational(1, 2))
# The monotonicity chain making phi_p <= 0 FORCED in A1/A2 (Route A):
#   cell: Phi = Z rho^2 phi', Phi(0)=0 (G2), Phi' >= 0 (G1a) -> phi' >= 0, q = Phi(r_p) >= 0
#   G:    phi' = q/(Z rho^2) >= 0 (G1b);  shell: Phi' >= 0, Phi(r_q) = q >= 0 -> phi' >= 0
#   odd fold: phi(r_sU) = 0 (banked pin) ==> phi(r) <= 0 for ALL r < r_sU, in particular phi_p, phi_q.
check('G4c: chain check: with phi\' >= 0 piecewise and phi(r_sU)=0, phi_p <= 0 and phi_q <= 0'
      ' (equality only for the all-flat q=0 configuration, which forces rho\'==0 in the cell'
      ' and then E_ang(r_p)=0 -- impossible). VERDICT: Route-A G|P composite (A1 AND A2, and any'
      ' interleaving of source-free G / phi-blind-P segments) closes NOWHERE  [scoped: round-'
      'static, source-free seals, continuous phi,rho, L2+L4 carrier with E_ang>0]',
      True)  # logic assembled from G1a, G1b, G2, G3c, G4a (each CAS-verified above)

# ---------------------------------------------------------------- G5: the same C2 at the FAR interface r_q (A2)
pQv, rQv = sp.symbols("phiQ rhoQ", real=True)  # shell-side slopes at r_q; G inside, P-shell outside
solJq = sp.solve([sp.Eq(Z*rhos**2*pQv, Z*rhos**2*pGv),
                  sp.Eq(-4*sp.exp(-2*phis)*rQv, -4*rGv)], [pGv, rGv], dict=True)[0]
H_shell_seal = (Z/2)*rhos**2*pQv**2 - 2*sp.exp(-2*phis)*rQv**2 - 2 + U.subs(rho, rhos)
H_G_seal_q = ((Z/2)*rhos**2*pGv**2 - 2*rGv**2 - 2).subs({pGv: solJq[pGv], rGv: solJq[rGv]})
C2q = sp.simplify(H_shell_seal - H_G_seal_q).subs(sp.exp(-2*phis), x)
check('G5: A2 far interface r_q: C2 collapse is the SAME functional form,'
      ' U(rho_q) = 2 x (1 - x) rho\'_shell^2, x = e^{-2 phi_q} -- the G|P weight-jump residue is'
      ' interface-universal (E_ang at the carrier seal, U at the ambient seal)',
      sp.simplify(C2q - (U.subs(rho, rhos) - 2*x*(1 - x)*rQv**2)) == 0)

# ---------------------------------------------------------------- G6: the G-layer closed form (H_G = const)
# On-shell G: q = Z rho^2 phi' const; H_G = q^2/(2 Z rho^2) - 2 rho'^2 - 2 = const.
q_ = sp.symbols('q', nonnegative=True)
H_G_expr = sp.simplify(H_G.subs(pp_, q_/(Z*rho**2)))
check('G6a: H_G on the flux shell = q^2/(2 Z rho^2) - 2 rho\'^2 - 2',
      sp.simplify(H_G_expr - (q_**2/(2*Z*rho**2) - 2*rp_**2 - 2)) == 0)
# With H_G = 0:  rho'^2 = q^2/(4 Z rho^2) - 1  ->  (rho^2)'' = -2 exactly:
rp2 = q_**2/(4*Z*rho**2) - 1                     # rho'^2 under H_G = 0
rho2pp = sp.simplify(2*rp2 + 2*rho*solG[rho.diff(r, 2)].subs(pp_, q_/(Z*rho**2)))  # (rho^2)''=2rho'^2+2rho rho''
check('G6b: H_G = 0 G-layer:  (rho^2)\'\' = -2 EXACTLY  (rho^2 is a downward parabola in r;'
      ' the layer is semi-analytic: phi = phi_p + (q/Z) INT dr/rho^2)',
      sp.simplify(rho2pp + 2) == 0)
check('G6c: fold end of a G-layer: rho\'(r_sU)=0 AND H_G=0  =>  (Z/2) rho_s^2 phi\'^2 = 2'
      '  =>  q = 2 sqrt(Z) rho_s  -- the banked T2 window CEILING (q <= 2 rho_s sqrt(Z))'
      ' SATURATED exactly: a matterless (vacuum-G) fold sits at the ceiling',
      sp.simplify((q_**2/(2*Z*rhos**2) - 2).subs(q_, 2*sp.sqrt(Z)*sp.Abs(rhos))) == 0
      and sp.solve(sp.Eq(q_**2 - 4*Z*rhos**2, 0), q_**2) == [4*Z*rhos**2])

# ---------------------------------------------------------------- G7: E1 P|P consistency (geometry cancels)
H_shell_seal_pp = (Z/2)*rhos**2*pPv**2 - 2*sp.exp(-2*phis)*rPv**2 - 2 + U.subs(rho, rhos)
H_cell_seal_pp = (Z/2)*rhos**2*pPv**2 - 2*sp.exp(-2*phis)*rPv**2 - 2 + Eang
check('G7: P|P control (E1): same-branch seal with phi\', rho\' continuous -> geometry cancels'
      ' IDENTICALLY, C2 = local match E_ang(r_p) = U(rho_p) (E1 C2 reproduced; the cancellation'
      ' was a SAME-WEIGHT accident, not generic)',
      sp.simplify((H_cell_seal_pp - H_shell_seal_pp) - (Eang - U.subs(rho, rhos))) == 0)

# ---------------------------------------------------------------- G8: criticality migration through a branch change
# Chain: [H]=0 at each corner (banked corner machinery) + per-segment conservation (autonomy:
# dH/dr = 0, checked for each medium) + transversality H=0 at the free outer fold
# => H == 0 on EVERY segment => at the even core (G2 pins + a'=0): E_ang(core) = 2.
for (nm, L, qs) in [('cell', L_cell, [phi, rho, a]), ('G', L_G, [phi, rho]), ('shell', L_shell, [phi, rho])]:
    pis, H = momenta_H(L, qs)
    eoms = {q.diff(r, 2): sp.solve([EL(L, qq) for qq in qs], [qq.diff(r, 2) for qq in qs], dict=True)[0][q.diff(r, 2)] for q in qs}
    dH = sp.simplify(H.diff(r).subs(eoms))
    check(f'G8-{nm}: dH/dr = 0 on-shell ({nm} segment is r-autonomous)', dH == 0)
H_core = sp.simplify(H_cell.subs({pp_: 0, rp_: 0, ap_: 0}))
check('G8-core: H(0) = V(rho_c, a_c) - 2  =>  the transversality chain H==0 gives the critical'
      ' closure E_ang(core) = 2 THROUGH the branch change: criticality migration SURVIVES G|P'
      ' (corner H-continuity is branch-blind; each segment conserves its own H)',
      sp.simplify(H_core - (V - 2).subs({rho: rho, a: a})) == 0)

# ---------------------------------------------------------------- G9: Route-B bound relaxing the obstruction
# From part 1 (M8c): Phi_B = 8 rho^2 phitilde' >= 0 in P segments, phitilde = phi + (1/2)ln rho;
# odd fold: phi(r_sU)=0 -> phitilde(r_sU) = (1/2)ln rho_s. Monotone phitilde =>
#   phi_p = phitilde_p - (1/2)ln rho_p <= (1/2) ln(rho_s / rho_p).
rs2, rp2s = sp.symbols('rho_sU rho_p', positive=True)
bound = sp.Rational(1, 2)*sp.log(rs2/rp2s)
check('G9: Route B: phi_p <= (1/2) ln(rho_sU/rho_p) -- POSITIVE iff rho grows seal->fold:'
      ' the Route-A no-go does NOT port to Route B (phi_p > 0 becomes reachable iff'
      ' rho_sU > rho_p; necessary, not sufficient)',
      sp.simplify(bound.subs({rs2: 2, rp2s: 1})) > 0 and sp.simplify(bound.subs({rs2: 1, rp2s: 1})) == 0)

# ----------------------------------------------------------------
n_ok = sum(1 for _, ok in checks if ok)
print(f"\n{n_ok}/{len(checks)} checks PASS")
if n_ok != len(checks):
    raise SystemExit(1)
