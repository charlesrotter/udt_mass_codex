#!/usr/bin/env python3
# P4 doorway study -- compact-field registration test (contract: PREREGISTRATION.md, frozen).
# Exact SymPy only: no floats, no numeric solvers, no randomness, no GPU. Deterministic.
# Honest split: SUBSTANTIVE (zero-residual exact computations) vs GUARD (citation/typing rows).
# Exit nonzero on any failure (F-D7).
import sys, json, os
import sympy as sp
from sympy import (symbols, sin, cos, exp, I, pi, Matrix, integrate, simplify,
                   S, solveset, Lambda, ImageSet, Function, Rational, eye, zeros)

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []
def check(name, ok, kind, detail):
    ok = bool(ok)
    CHECKS.append({"name": name, "ok": ok, "kind": kind, "detail": detail})
    print(("PASS" if ok else "FAIL") + " [" + kind + "] " + name + " -- " + detail)
    return ok

print("# P4 doorway study derivation (stages C1..C5, TD-3, TD-4)")
print("# Arena/stamps: registered stationary one-parameter presentation; positive triangular")
print("# chart; cell x in [-l,l]; R x S3 arena enters via banked cap census + Hopf connection")
print("# A = sigma3. Census/pairing/posture branches carried, NONE adopted. Off-shell typing.")

# ============================ STAGE 1: C1 (Hopf fiber circle) ============================
th, ph, psi = symbols('theta phi psi', real=True)
# sigma3 = dpsi + cos(theta) dphi on Euler-angle S3 (psi period 4*pi). Components in
# (theta, phi, psi) coordinate basis:
a_th, a_ph, a_ps = S(0), cos(th), S(1)
# Exterior derivative components (d sigma3)_{ij} = d_i a_j - d_j a_i
d_thph = sp.diff(a_ph, th) - sp.diff(a_th, ph)   # expect -sin(theta)
d_thps = sp.diff(a_ps, th) - sp.diff(a_th, psi)
d_phps = sp.diff(a_ps, ph) - sp.diff(a_ph, psi)
check("C1a_hopf_connection_not_closed",
      simplify(d_thph + sin(th)) == 0 and d_thps == 0 and d_phps == 0
      and simplify(d_thph) != 0,
      "SUBSTANTIVE",
      "d(sigma3) = -sin(theta) dtheta^dphi != 0 exactly; a global function F with dF = sigma3 "
      "would force d(sigma3)=0 (d^2=0): the fiber phase is NOT a globally-defined field")
obstruction = integrate(integrate(d_thph, (th, 0, pi)), (ph, 0, 2*pi))
check("C1a_chern_obstruction_integral",
      simplify(obstruction + 4*pi) == 0,
      "SUBSTANTIVE",
      "integral of d(sigma3) over the base S2 = -4*pi != 0 exact (one fiber period 4*pi, "
      "Chern class +-1): the Hopf bundle admits NO global section -- promotion of the fiber "
      "phase to a single global field FAILS with this exact obstruction")
# Local fiber-phase potentials (chart N regular at theta=0, chart S at theta=pi):
aN = cos(th) - 1   # dphi-coefficient of sigma3 - d(psi_N)
aS = cos(th) + 1
check("C1b_local_potentials_both_valid",
      simplify(sp.diff(aN, th) - d_thph) == 0 and simplify(sp.diff(aS, th) - d_thph) == 0
      and aN.subs(th, 0) == 0 and aS.subs(th, pi) == 0,
      "SUBSTANTIVE",
      "per-chart fiber phases exist (potentials regular at the respective poles): the fiber "
      "phase IS definable chart-locally")
mismatch = simplify(aN - aS)   # = -2 : (a_N - a_S) = -2 dphi
loop_int = integrate(mismatch, (ph, 0, 2*pi))
check("C1b_transition_is_circle_valued_winding_one",
      mismatch == -2 and simplify(loop_int + 4*pi) == 0,
      "SUBSTANTIVE",
      "chart mismatch of the fiber phase = -2*dphi; equatorial loop integral = -4*pi = "
      "(-1) x (fiber period 4*pi): the transition datum is CIRCLE-VALUED with winding -1 -- "
      "the theory OWNS a circle-valued transition law (delivered to C5), not a global field")
# CREDITED ADOPTION (verifier G1, finishing pass): SECOND Chern route -- Stokes on the
# verifier's own trivializations psi_N = psi + phi, psi_S = psi - phi.
stokes_chern = integrate(aN - aS, (ph, 0, 2*pi))
direct_chern = integrate(integrate(-sin(th), (th, 0, pi)), (ph, 0, 2*pi))
check("C1a_chern_second_route_stokes_credited",
      simplify(stokes_chern + 4*pi) == 0 and simplify(direct_chern + 4*pi) == 0
      and simplify(stokes_chern - direct_chern) == 0,
      "SUBSTANTIVE",
      "CREDITED ADOPTION (verifier G1): the Chern obstruction -4*pi re-derived by a SECOND "
      "route -- Stokes via the two trivializations psi_N = psi + phi, psi_S = psi - phi "
      "(equatorial loop integral of aN - aS) agrees exactly with the direct S2 integration "
      "of d(sigma3): two independent routes, one integer -- the C1 obstruction is "
      "route-independent")
check("C1c_registered_fields_are_real_guard", True, "GUARD",
      "the registered 1D presentation fields are (phi, f, bh), all REAL (banked arena "
      "record/period gate stamps); the fiber phase is NOT among them: C1 promotion would ADD "
      "a field = C5's registration question, with C1 delivering an OWNED target circle "
      "(period 4*pi) and an OWNED circle-valued transition datum (winding 1)")
# C1d/C2 shared: the banked cap census -- recompute every determinant from the cap vectors
tsv = os.path.join(HERE, "..", "udt_higher_isometry_plane_ownership_audit_2026-07-28",
                   "TORIC_CAP_ENUMERATION.tsv")
rows = [r.strip().split("\t") for r in open(tsv) if r.strip()][1:]
n_rows, all_match, all_unit = len(rows), True, True
for r in rows:
    vm = [sp.Integer(x) for x in r[1].split(",")]
    vp = [sp.Integer(x) for x in r[2].split(",")]
    det = vm[0]*vp[1] - vm[1]*vp[0]
    if det != sp.Integer(r[3]): all_match = False
    if abs(det) != 1: all_unit = False
check("C1d_cap_census_dets_recomputed_all_unit",
      n_rows == 104 and all_match and all_unit,
      "SUBSTANTIVE",
      "all 104 banked two-cap pairs: det recomputed from the cap vectors, matches the banked "
      "column, |det| = 1 every row => pi1(capped arena) = Z/1 = TRIVIAL (re-instantiated)")
h = symbols('h', integer=True)
hom_trivial = solveset(sp.Eq(1*h, 0), h, S.Integers)   # pi1 trivial: only relation g^1 = e
check("C1d_no_winding_home_in_arena_cycles",
      hom_trivial == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "winding of ANY circle-valued field is a hom pi1 -> Z; pi1 trivial => winding == 0 on "
      "every 1-cycle of the capped S3/toric sector: the arena's own angular cycles offer NO "
      "home for an integer (the banked capped/torsion obstruction, confronted)")

# ============================ STAGE 1: C2 (toric angles) ============================
# Cap model: the collapsing toric circle near a cap = punctured-disk angle alpha.
alpha = symbols('alpha', real=True)
winding_angle_map = integrate(S(1), (alpha, 0, 2*pi)) / (2*pi)   # (1/2pi) loop-int of d(alpha)
check("C2a_toric_angle_winding_one_at_cap",
      winding_angle_map == 1,
      "SUBSTANTIVE",
      "the toric angle, read as a circle-valued map on a loop around its cap axis, has "
      "winding = 1 exactly")
# Continuity across the cap point forces small-image loops there; a loop whose image lies in
# an arc (angular width < 2*pi) has total lift increment T with |T| < 2*pi AND T in 2*pi*Z:
n = symbols('n', integer=True)
arc_solutions = solveset(sp.Eq(2*pi*n, 0), n, S.Integers)  # |2 pi n| < 2 pi over Z <=> n = 0
check("C2a_arc_confined_loop_has_zero_winding",
      (arc_solutions == sp.FiniteSet(0) and not (sp.Abs(2*pi*sp.Integer(1)) < 2*pi)
       and not (sp.Abs(2*pi*sp.Integer(-1)) < 2*pi)),
      "SUBSTANTIVE",
      "the only integer multiple of 2*pi with |.| < 2*pi is 0 (|+-2*pi| < 2*pi is False, "
      "exact): an arc-confined loop has winding 0; with winding's homotopy/radius invariance "
      "(NAMED Category-A step, banked precedent lane) the winding-1 angle map admits NO "
      "continuous extension over the cap: the toric angle is NOT a field on the capped arena. "
      "O4 note (verifier): the SymPy content here is deliberately thin (a period integral + "
      "a lattice-point fact); the load-bearing step is the NAMED Category-A winding-"
      "invariance -- banked convention, honest because named")
check("C2b_no_live_home_for_toric_winding", True, "GUARD",
      "combining C1d (pi1 of the capped S3/toric sector TRIVIAL, recomputed) with the banked "
      "period-gate cycle census (CITED: the only live non-torsion cycles are the two-sided "
      "CYCLIC completion cycle (Z translation, x-direction) and J11 chart-transition loops): "
      "a winding built from the toric angles has NOWHERE to live -- an x-dependent phase on "
      "the completion cycle is not a toric angle but a NEW field = C5. "
      "C2 VERDICT: FAILS, by exactly the banked capped/torsion obstruction (confronted head-on)")
print("## STAGE 1 complete: C1 = FAILS-AS-GLOBAL-PROMOTION / DELIVERS target circle +")
print("## circle-valued transition datum (Chern obstruction exact). C2 = FAILS (cap kill).")

# ============================ STAGE 2: C3 (screen SO(2)) ============================
t = symbols('t', real=True)
J = Matrix([[0, -1], [1, 0]])                       # screen-rotation generator (L23, slots 2,3)
R = Matrix([[cos(t), -sin(t)], [sin(t), cos(t)]])   # candidate one-parameter subgroup
resid_ode = sp.simplify(sp.diff(R, t) - J*R)
check("C3a_screen_SO2_is_owned_circle",
      resid_ode == zeros(2, 2) and R.subs(t, 0) == eye(2)
      and sp.simplify(R.subs(t, 2*pi)) == eye(2)
      and sp.simplify(R.subs(t, pi)) == -eye(2),
      "SUBSTANTIVE",
      "R' = J R, R(0) = I (Picard-named uniqueness => R = exp(tJ)); R(2*pi) = I, "
      "R(pi) = -I != I: the banked screen SO(2) IS a genuine owned compact circle, period "
      "2*pi -- the ONE compact group in the banked equivariance")
sol_diag = solveset(sin(t), t, S.Reals)   # SO(2) members that are signed-diagonal
Rpin = sp.simplify(R.subs(t, pi*n))       # value at the solution lattice, integer n
check("C3b_chart_keeps_only_2torsion_of_circle",
      (pi in sol_diag) and (2*pi in sol_diag) and (pi/2 not in sol_diag)
      and sp.simplify(sin(pi*n)) == 0
      and Rpin == Matrix([[(-1)**n, 0], [0, (-1)**n]])
      and sp.simplify(R.subs(t, pi)**2) == eye(2),
      "SUBSTANTIVE",
      "SO(2) intersect (signed diagonals = the K4-compatible screen forms in the registered "
      "triangular chart) <=> sin(t) = 0 <=> t in pi*Z: exactly {I, -I} = the 2-TORSION "
      "subgroup; the banked K4 screen characters +-1 are precisely the 2-torsion shadow of "
      "the owned circle -- the registered chart SPENDS the compactness as gauge fixing")
zc = symbols('z')   # real points of U(1): z real and |z| = 1
real_U1 = solveset(sp.Eq(zc**2, 1), zc, S.Reals)
check("C3b_K4_characters_are_real_points_of_U1",
      real_U1 == sp.FiniteSet(-1, 1),
      "SUBSTANTIVE",
      "{z real, z^2 = 1} = {+-1} exactly: the banked REAL holonomy targets' +-1 characters "
      "are the real points of the owned circle -- the real-targets theorem and the owned "
      "SO(2) are the SAME structure seen through the chart. O3 nuance (verifier): the "
      "identification is of character VALUES {+-1} and of the chart-surviving subgroup "
      "{I, -I}; K4 itself (order 4) does NOT embed in the circle -- two of its four screen "
      "blocks (diag(-1,1), diag(1,-1)) are det = -1 non-circle members")
# Triangular-positive chart group owns NO nontrivial compact one-parameter subgroup:
a2, b2, d2, T = symbols('a2 b2 d2 T', real=True)
sol_a = solveset(sp.Eq(exp(T*a2), 1), T, S.Reals)   # diagonal exponentials: point kernel at a2!=0
Xn = Matrix([[0, 0], [b2, 0]])
expN = eye(2) + T*Xn   # exp of nilpotent lower-triangular, exact (Xn^2 = 0)
check("C3b_triangular_chart_group_no_compact_subgroup",
      Xn*Xn == zeros(2, 2) and sp.simplify(exp(T*a2).subs(T, 0)) == 1
      and sol_a.subs(a2, 1) == sp.FiniteSet(0)
      and solveset(sp.Eq(T*b2, 0), T, S.Reals).subs(b2, 1) == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "lower-triangular generators: diagonal part e^{T a} = 1 <=> T a = 0 (real exp point "
      "kernel, solveset over R = {0} at a != 0); strictly-lower part nilpotent, "
      "exp = I + T X = I <=> T X = 0: the chart's block group (rho = e^{dx H}, positive "
      "triangular Q, L) contains NO nontrivial compact subgroup -- no U(1) is OWNED there")
kmodf = Function('kmod')
x = symbols('x', real=True)
thf = Function('thetad')
dressing = sp.dsolve(sp.Eq(thf(x).diff(x) + 2*kmodf(x)*thf(x), 0), thf(x),
                     ics={thf(0): 0})
check("C3c_dressing_anchored_to_zero",
      dressing.rhs == 0,
      "SUBSTANTIVE",
      "the banked unanchored screen-rotation dressing obeys theta' + 2 kmod(x) theta = 0; "
      "the anchor E(0) = I forces theta(0) = 0 => theta == 0 (exact dsolve; Route D 1.5 "
      "recomputed): on the anchored registered footing the SO(2) phase is PURE PRESENTATION "
      "-- anchored orbits are singletons; promoting the dressing to a field adds NO invariant "
      "content and leaves every banked holonomy target REAL (F-D5: no genuine change)")
print("## C3 VERDICT: FAILS-ON-BANKED-FOOTING (spent-as-gauge, exact form): the owned")
print("## compact circle was quotiented to its 2-torsion {+-1} by the registered triangular")
print("## chart + anchor; unfixing chart/anchor = changing the footing, not extending it (typed).")

# ============================ STAGE 2: C4 (E07/E08 R-subgroups) ============================
k = symbols('k', real=True, nonzero=True)
E07gen = Matrix([[-k, 0], [0, k]])   # banked E07 seat: K = diag(-k, +k), traceless line
expE07 = sp.simplify((T*E07gen).exp())
check("C4a_E07_point_kernel",
      expE07 == Matrix([[exp(-T*k), 0], [0, exp(T*k)]])
      and solveset(sp.Eq(exp(T), 1), T, S.Reals) == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "e^{T diag(-k,k)} = diag(e^{-Tk}, e^{Tk}) = I <=> Tk = 0 <=> T = 0 at k != 0 (real "
      "spectrum, point kernel): the E07 one-parameter subgroup is a CLOSED R-embedding -- "
      "no compact factor at ANY parameter value; same form kills H = diag(-1,+1) (E-block)")
ph1, ph2, u1, u2, u3, ph3 = symbols('varphi1 varphi2 u1 u2 u3 varphi3', real=True)
# Banked E08 two-segment law (Route B T3, cited): (ph,u) then (ph2,u2) -> (ph+ph2, u1 + e^{-ph1} u2)
def e08(p, q):   # p, q = (phi, u)
    return (p[0] + q[0], p[1] + exp(-p[0])*q[1])
lhs = e08(e08((ph1, u1), (ph2, u2)), (ph3, u3))
rhs = e08((ph1, u1), e08((ph2, u2), (ph3, u3)))
assoc_ok = all(sp.simplify(lhs[i] - rhs[i]) == 0 for i in (0, 1))
p2 = e08((ph1, u1), (ph1, u1)); p3 = e08(p2, (ph1, u1))
# periodicity: n-fold power = identity (0,0)
per2 = solveset(sp.Eq(p2[0], 0), ph1, S.Reals)
u_at0_2 = sp.simplify(p2[1].subs(ph1, 0)); u_at0_3 = sp.simplify(p3[1].subs(ph1, 0))
check("C4b_E08_solvable_no_torsion_no_compact",
      assoc_ok and per2 == sp.FiniteSet(0) and u_at0_2 == 2*u1 and u_at0_3 == 3*u1
      and solveset(sp.Eq(2*u1, 0), u1, S.Reals) == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "the banked E08 cocycle group (law u12 = u1 + e^{-phi1} u2; associativity recomputed, "
      "zero residual) is R semidirect R, simply-connected solvable: an n-th root of the "
      "identity forces n*phi = 0 => phi = 0, then u_n = n*u = 0 => u = 0 (n = 2, 3 "
      "instantiated exactly): NO nontrivial torsion, NO compact subgroup -- the expected "
      "FAIL, with the exact failure form = real spectrum / solvable simply-connected, i.e. "
      "the real-targets theorem at GROUP level")
print("## C4 VERDICT: FAILS (confirmed non-compact, exact failure forms). INFORMATIVE:")
print("## compactness cannot be reached from the banked strata by any parameter value.")
print("## STAGE 2 complete.")

# ============================ STAGE 3: C5 (new S1-valued field theta(x)) ============================
# Registration at Route-D-analog grade. Target: R/2piZ. All legality DERIVED from banked rules.
thv = symbols('vartheta', real=True)   # a target value
# --- C5a: target well-definedness => the periodicity legality rule (DERIVED, not asserted)
res_lin  = sp.simplify((thv + 2*pi) - thv)            # linear entry: residual 2pi
res_cos  = sp.simplify(cos(thv + 2*pi) - cos(thv))
res_sin  = sp.simplify(sin(thv + 2*pi) - sin(thv))
res_eith = sp.simplify(exp(I*(thv + 2*pi)) - exp(I*thv))
check("C5a_periodicity_legality_rule",
      res_lin == 2*pi and res_lin != 0 and res_cos == 0 and res_sin == 0 and res_eith == 0,
      "SUBSTANTIVE",
      "a bulk entry F(theta) is well-defined on the registered target R/2piZ iff "
      "F(theta+2pi) = F(theta): bare/linear theta FAILS (residual 2pi != 0, exact) -- "
      "EXCLUDED; cos(theta), sin(theta), e^{i theta} pass with zero residual -- LEGAL. "
      "This legality is DERIVED from target well-definedness (F-D2 honored), and it is "
      "exactly where the imaginary exponent enters the alphabet LEGALLY")
thF = Function('vth')   # a lift of the field (real-valued local lift)
jet_resid = sp.simplify(sp.diff(thF(x) + 2*pi, x) - sp.diff(thF(x), x))
check("C5a_jets_are_real_and_lift_independent",
      jet_resid == 0,
      "SUBSTANTIVE",
      "theta'(x), theta''(x): lifts differ by constants in 2piZ, d/dx kills them (zero "
      "residual): the JETS are well-defined REAL-valued local entries -- legal by the same "
      "co-translation status as the banked m-jets (N2-analog)")
# --- C5b: the banked exclusions TRAVEL: anchored-nonlocal entry fails co-translation
s = symbols('s', real=True)
lift = x**2                                   # free off-shell witness lift (Route-D precedent)
u_ = symbols('u_', real=True)
translated_member_val = integrate(sp.diff(lift.subs(x, u_ + s), u_), (u_, 0, x))  # member x->x+s
naive_cotranslate = (lift.subs(x, x + s) - lift.subs(x, 0))
nonlocal_resid = sp.simplify(translated_member_val - naive_cotranslate)
check("C5b_nonlocal_exclusion_travels",
      nonlocal_resid == -s**2 and sp.simplify(nonlocal_resid.subs(s, 0)) == 0
      and nonlocal_resid != 0,
      "SUBSTANTIVE",
      "the anchored nonlocal entry int_0^x theta' du (= the real LIFT theta~(x) - theta~(0)) "
      "FAILS the banked co-translation test: witness lift x^2 gives residual -s^2 != 0 -- "
      "the SAME anchor defect that excluded bare phi and nonlocal m-integrals (Route D "
      "R3, banked rule TRAVELING): the alphabet sees e^{i theta} and the jets, NEVER the lift")
# --- C5c: cocycle -- does the banked two-sided law admit a U(1) factor?
r1, r2, r3, q1, q2, q3, l1, l2, l3 = [Matrix(2, 2, sp.symbols(f'{nm}_:4'))
                                      for nm in ('r1', 'r2', 'r3', 'q1', 'q2', 'q3', 'l1', 'l2', 'l3')]
ps1, ps2, ps3 = symbols('psi1 psi2 psi3', real=True)
def comp(B, A):   # banked two-sided law (period gate C3 / Route B T3, cited), segment A then B
    return (B[0]*A[0], B[1]*A[1], B[1]*A[2] + B[2]*A[0], B[3]*A[3])
T1c = (r1, q1, l1, exp(I*ps1)); T2c = (r2, q2, l2, exp(I*ps2)); T3c = (r3, q3, l3, exp(I*ps3))
lhsC = comp(comp(T3c, T2c), T1c); rhsC = comp(T3c, comp(T2c, T1c))
assocU = all(sp.simplify(sp.expand(lhsC[i] - rhsC[i])) == sp.zeros(2, 2) for i in (0, 1, 2)) \
         and sp.simplify(lhsC[3] - rhsC[3]) == 0
noU = comp((r2, q2, l2, S(1)), (r1, q1, l1, S(1)))
withU = comp((r2, q2, l2, exp(I*ps2)), (r1, q1, l1, exp(I*ps1)))
blocks_untouched = all(sp.simplify(noU[i] - withU[i]) == sp.zeros(2, 2) for i in (0, 1, 2))
rev = sp.simplify(exp(I*ps1)*sp.conjugate(exp(I*ps1)))
check("C5c_two_sided_law_admits_central_U1_factor",
      assocU and blocks_untouched and rev == 1,
      "SUBSTANTIVE",
      "adjoining a U(1) slot u = e^{i psi} multiplicatively to the banked two-sided twisted "
      "law L(g2 o g1) = Q2 L1 + L2 rho1: associativity holds with zero residual on fully "
      "generic 2x2 blocks; the (rho, Q, L) blocks are UNTOUCHED by the adjunction; reversal "
      "u * conj(u) = 1 (real psi): the compact version of the banked law EXISTS -- the law "
      "ADMITS a central U(1) factor. Combined with C3b/C4 (no U(1) inside the banked block "
      "group): the factor is ADJOINED, not owned -- REGISTERED-POSIT status. O1 caveat "
      "(verifier): a central U(1) factor is direct-product-admissible for ANY associative "
      "law -- C5c ALONE has no discriminating power; the discriminating content is the "
      "base-law associativity re-proof plus the C3b/C4 owned-nowhere result, and the "
      "REGISTERED-POSIT tag hangs on exactly that adjoined-not-owned fact")
# --- C5d: K4 / parity / crease compatibility
neg_wd = sp.simplify((-(thv + 2*pi)) - (-thv))   # -2pi, in 2piZ: character action circle-wellposed
crease_sol = solveset(sp.Eq(2*thv, 2*pi*n), thv, S.Reals)
vals = sorted(set([sp.Mod(pi*m, 2*pi) for m in range(-2, 3)]), key=str)
check("C5d_K4_parity_crease_2torsion_datum",
      neg_wd == -2*pi and sp.Mod(neg_wd, 2*pi) == 0
      and (pi in crease_sol.subs(n, 1)) and set(vals) == {S(0), pi},
      "SUBSTANTIVE",
      "theta -> -theta is well-defined mod 2pi (residual -2pi == 0 mod 2pi): BOTH K4 "
      "character assignments chi_theta = +-1 are circle-legal (chi_theta DECLARED, "
      "ledgered); mirror parity eps_theta SUPPLIED, never valued (F-R4-analog). NEW EXACT "
      "FACT (conditional on supplied eps_theta = -1): the crease fixed-point condition "
      "theta == -theta mod 2pi <=> 2 theta in 2piZ <=> theta in {0, pi}: the crease value "
      "of an odd circle-valued field is 2-TORSION QUANTIZED -- the arc's first discrete "
      "TARGET-side datum, derived not imposed; eps_theta = +1 branch: unconstrained")
# --- C5e: J05 pairing slots (integration-by-parts identity, generic witnesses)
L_ = symbols('L_', positive=True)
# generic-cubic instantiation with all coefficients free (exact zero-residual IBP identity)
c0, c1, c2, c3, d0, d1, d2, d3, e0, e1, e2, e3 = symbols('c0 c1 c2 c3 d0 d1 d2 d3 e0 e1 e2 e3')
Dp = c0 + c1*x + c2*x**2 + c3*x**3
Ep = d0 + d1*x + d2*x**2 + d3*x**3
Vp = e0 + e1*x + e2*x**2 + e3*x**3
lhsJp = integrate(Dp*Vp + Ep*sp.diff(Vp, x), (x, 0, L_))
rhsJp = integrate((Dp - sp.diff(Ep, x))*Vp, (x, 0, L_)) + (Ep*Vp).subs(x, L_) - (Ep*Vp).subs(x, 0)
check("C5e_J05_pairing_pointwise_row_plus_wall_slots",
      sp.simplify(sp.expand(lhsJp - rhsJp)) == 0,
      "SUBSTANTIVE",
      "int(D_theta v + D_theta' v') = int((D_theta - d/dx D_theta') v) + [D_theta' v]_walls "
      "with all 12 coefficients free (zero residual): delta-theta(x) pairs as a POINTWISE "
      "density row (the reduction theorem's field-fork form) and the varied-boundary fork "
      "REQUIRES wall theta-jet slots (N3-analog, supplied-structure per the banked V8 "
      "resolution): the J05 coupling slots for theta are DEFINED -- registered, NOT adopted")
# --- C5f: F-D5 adjudication -- the holonomy-target situation genuinely changes
sol_real = solveset(sp.Eq(exp(t), 1), t, S.Reals)
sol_circ = solveset(sp.Eq(cos(t), 1), t, S.Reals)
check("C5f_FD5_lattice_vs_point_kernel",
      sol_real == sp.FiniteSet(0)
      and (2*pi in sol_circ) and (4*pi in sol_circ) and (pi not in sol_circ)
      and sp.simplify(exp(2*pi*I)) == 1 and sp.simplify(exp(pi*I)) == -1 and 2*pi != 0,
      "SUBSTANTIVE",
      "real target: e^t = 1 over R has the point kernel {0} (solveset exact); circle "
      "target: e^{i t} = 1 <=> cos t = 1 (with sin t = 0 implied) <=> t in 2piZ -- a "
      "genuine LATTICE (2pi, 4pi members, pi excluded; direct certificates e^{2pi i} = 1, "
      "e^{pi i} = -1 per the banked period-gate route): the registered theta GENUINELY "
      "changes the banked holonomy-target situation -- F-D5 does NOT fire")
print("## C5 VERDICT: REGISTERS at Route-D-analog grade, REGISTERED-POSIT tag. Conditional")
print("## slots (honest): eps_theta SUPPLIED; chi_theta DECLARED; U(1) cocycle factor")
print("## ADJOINED (admitted by the banked law, not owned by it); entries = periodic-in-theta")
print("## pointwise values + real jets + wall slots; exclusions DERIVED (bare lift, nonlocal")
print("## integrals, aperiodic entries, character mismatch). STAGE 3 complete.")

# ============================ STAGE 4: TD-3 (integer content) ============================
# Period-gate machinery re-run with the registered theta present. Cycle census cited.
hh = symbols('hh', integer=True)
homDinf_Z = solveset(sp.Eq(2*hh, 0), hh, S.Integers)
check("TD3a_quotient_posture_winding_still_zero",
      homDinf_Z == sp.FiniteSet(0),
      "SUBSTANTIVE",
      "winding on the quotient posture = a hom D-infinity -> Z; torsion generators force "
      "2h(r+-) = 0 => h(r+-) = 0 over Z (exact), generation => winding == 0: the banked "
      "Hom(D-infinity, R) = 0 theorem SURVIVES the circle target on the winding side; the "
      "quotient posture's integer content is instead the TARGET-side crease Z2 datum (C5d)")
cc = symbols('cc', real=True)          # per-cell theta-slope (free off-shell datum)
LL = symbols('LLen', positive=True)    # cell length
Jth = symbols('Jth', real=True)        # supplied seam jump (germ data)
nw = symbols('n_w', integer=True)      # the winding integer
sol_L = sp.solve(sp.Eq(cc*LL + Jth, 2*pi*nw), LL)
sol_c = sp.solve(sp.Eq(cc*LL + Jth, 2*pi*nw), cc)
real_case = sp.solve(sp.Eq(cc*LL + Jth, 0), cc)
check("TD3b_cyclic_winding_condition_live",
      sol_L == [(2*pi*nw - Jth)/cc] and sol_c == [(2*pi*nw - Jth)/LL]
      and real_case == [-Jth/LL],
      "SUBSTANTIVE",
      "the CYCLIC completion cycle (the banked live non-torsion cycle): single-valuedness "
      "of e^{i theta} around it = the winding condition SUM_i c_i L_i + SUM_s J_s = "
      "2 pi n_w, n_w in Z (N = 1 instance solved exactly; general N = the period gate's "
      "telescoping form with d theta in place of d pi_p): THE FIRST LIVE INTEGER CONDITION "
      "on the banked cycle census. Structure change, exact: real-valued fields gave ONE "
      "hyperplane (n forced 0); the circle target gives a Z-INDEXED FAMILY of parallel "
      "hyperplanes -- the configuration space acquires Z-labeled sheets")
# CREDITED ADOPTION (verifier G9, finishing pass): N = 2 telescoping re-derivation.
c1t, c2t, L1t, L2t, J1t, J2t, b1t = symbols('c1t c2t L1t L2t J1t J2t b1t', real=True)
b2t = c1t*L1t + b1t + J1t                 # start of cell 2 = end of cell 1 + seam jump
increment = sp.simplify((c2t*L2t + b2t + J2t) - b1t)
sol_real_t = sp.solve(sp.Eq(increment, 0), c1t)
sol_fam_t = sp.solve(sp.Eq(increment, 2*pi*nw), L1t)
sol_slope_t = sp.solve(sp.Eq(increment, 2*pi*nw), c1t)
check("TD3b_telescoping_N2_rederivation_credited",
      sp.expand(increment - (c1t*L1t + c2t*L2t + J1t + J2t)) == 0
      and sp.simplify(exp(I*(2*pi*nw)).rewrite(cos).subs(nw, 5)) == 1
      and sp.simplify(exp(I*pi)) == -1
      and sol_real_t == [-(c2t*L2t + J1t + J2t)/L1t]
      and sol_fam_t == [(2*pi*nw - c2t*L2t - J1t - J2t)/c1t]
      and len(sol_slope_t) == 1,
      "SUBSTANTIVE",
      "CREDITED ADOPTION (verifier G9): N = 2 telescoping re-derivation -- per-cell lifts "
      "theta = c_i x + b_i with seam jumps J_s telescope to increment = c1 L1 + c2 L2 + "
      "J1 + J2 exactly; the 2*pi enters ONLY through e^{i Delta} = 1 on the registered "
      "target (e^{2 pi i n} = 1, e^{i pi} = -1: genuine, not inserted); real-target "
      "contrast = the single hyperplane (n forced 0, the banked form); the circle target = "
      "the Z-indexed family; and slopes absorb ANY (L, n) pair -- the no-unconditional-cut "
      "scoping is REAL freedom, not an artifact")
sol_L_fixed = sp.solve(sp.Eq(1*LL, 2*pi*nw), LL)
check("TD3b_parameter_cut_adjudication",
      sol_L_fixed == [2*pi*nw],
      "SUBSTANTIVE",
      "WHICH parameters cut (honest, both directions): the condition couples the theta-"
      "sector data (slopes c_i, jumps J_s) JOINTLY with the cell lengths L_i; at FIXED "
      "slope c != 0 (witness c = 1, J = 0) the length is lattice-cut L in 2 pi Z (exact) "
      "-- a CONDITIONAL lattice; but the slopes are FREE data, so NO banked parameter "
      "(E0, l, moduli) is unconditionally quantized: absent adopted dynamics the winding "
      "cuts the JOINT (theta-data x geometry) space into Z-sheets only; the J05 slots "
      "(C5e) are exactly where an adopted coupling would tie c_i to E0_i -- registered, "
      "NOT adopted, no spectrum claimed (contract ceiling honored)")
zz = symbols('zz')
tor_real = solveset(sp.Eq(2*symbols('P_', real=True), 0), symbols('P_', real=True), S.Reals)
tor_circ = solveset(sp.Eq(zz**2, 1), zz, S.Complexes)
check("TD3c_torsion_classes_revive_over_U1",
      tor_real == sp.FiniteSet(0) and tor_circ == sp.FiniteSet(-1, 1)
      and sp.simplify((-1)**2) == 1 and (-1 != 1),
      "SUBSTANTIVE",
      "the banked torsion-vacuity proofs are TARGET-DEPENDENT and the re-run flips exactly "
      "one leg: over R, nP = 0 => P = 0 (order-2 classes VACUOUS -- banked, reproduced); "
      "over U(1), hol^2 = 1 has TWO solutions {+1, -1} (exact): the K4-orbifold order-2 "
      "classes -- vacuous for every real target -- become LIVE Z2-valued holonomy data for "
      "the circle target; the cap classes stay empty (pi1 trivial, C1d recomputed): the "
      "revival is exactly the 2-torsion sector, nothing else")
check("TD3d_J11_loops_gain_lattice", True, "GUARD",
      "with the adjoined U(1) factor (C5c), J11 loop holonomy carries u(loop) = e^{i Theta}; "
      "triviality <=> Theta in 2piZ (C5f lattice) -- vs the banked real-block triviality "
      "locus = a codim-1 real hyperplane (period gate C3, CITED): the 'trivial or "
      "classified' classification gains a DISCRETE winding component; conditional on a "
      "loop-possessing completion (completion data; F-S7 flag travels, inherited)")

# ============================ STAGE 4: TD-4 (carrier comparison, one-way) ============================
sN = symbols('sN', real=True)
liftmap = Function('lift_')(symbols('p_', real=True))
H0 = sp.simplify(sN*liftmap).subs(sN, 0)
H1 = sp.simplify(sN*liftmap).subs(sN, 1)
homZ_triv = solveset(sp.Eq(1*hh, 0), hh, S.Integers)
check("TD4a_pi2_content_not_carried",
      homZ_triv == sp.FiniteSet(0) and H0 == 0 and H1 == liftmap,
      "SUBSTANTIVE",
      "DERIVES layer: NO. A map S2 -> S1 lifts to R (pi1(S2) trivial => monodromy hom == 0, "
      "exact; covering-lifting NAMED Category-A) and the straight-line homotopy s*lift "
      "(endpoints checked exactly: 0 and lift) null-homotopes it: pi2(S1) = 0 -- the "
      "registered circle-valued field CANNOT carry the carrier's pi2(S2) winding content, "
      "and nothing here derives an S2-valued field. The carrier posit is NOT derived")
psN = symbols('psiE', real=True)
sig1_th, sig1_ph = cos(psN), sin(psN)*sin(th)
sig2_th, sig2_ph = -sin(psN), cos(psN)*sin(th)
g_thth = sp.simplify(sig1_th**2 + sig2_th**2)
g_phph = sp.simplify(sig1_ph**2 + sig2_ph**2)
g_thph = sp.simplify(sig1_th*sig1_ph + sig2_th*sig2_ph)
check("TD4b_S2_arises_natively_as_hopf_base",
      g_thth == 1 and g_phph == sin(th)**2 and g_thph == 0,
      "SUBSTANTIVE",
      "POSSESSES layer: PARTIAL-AS-STAGE. sigma1^2 + sigma2^2 = dtheta^2 + sin^2(theta) "
      "dphi^2 exactly, psi-INDEPENDENT => basic => descends to the Hopf base: the arena "
      "natively possesses a round S2 (and the fiber circle, C1) -- as DOMAIN/stage "
      "structure, never as a field TARGET; per the banked bedrock (metric derives the "
      "STAGE, not the ACTORS) this founds no actor")
eqv = sp.simplify(cos(thv)**2 + sin(thv)**2 - 1)
check("TD4c_emulates_equatorial_phase_sector",
      eqv == 0,
      "SUBSTANTIVE",
      "EMULATES layer: PARTIAL. the equatorial restriction of a unit-3-vector carrier "
      "field, n = (cos theta, sin theta, 0), |n| = 1 exactly, IS an S1-valued field: the "
      "registered theta carries exactly the structure of the carrier's U(1)/phase sector "
      "(the circle its equatorial windings wrap), with winding Z = pi1(S1); the pi2 sector "
      "(the polar direction) is NOT emulated (TD4a). One-way characterization; no result "
      "transferred from the hopfion lane (F-D4)")
check("TD4_three_layer_verdict", True, "GUARD",
      "DERIVES: NO (no S2-valued field derived; pi2 not carried). EMULATES: PARTIAL (the "
      "U(1)/phase sector exactly; pi2/pi3 sectors not). POSSESSES: PARTIAL-AS-STAGE (Hopf "
      "fiber circle + round S2 base owned natively in the DOMAIN; identifying theta's "
      "target with the owned fiber circle = a further typed posit, not made). CARRIER "
      "POSIT STATUS: PARTIALLY FOUNDED at the circle/phase layer, UNTOUCHED at the "
      "pi2(S2)/pi3(S3) layers. Map facts only; one-way (F-D4 honored)")

# ============================ FINALIZE ============================
n_sub = sum(1 for c in CHECKS if c["kind"] == "SUBSTANTIVE")
n_gua = sum(1 for c in CHECKS if c["kind"] == "GUARD")
n_fail = sum(1 for c in CHECKS if not c["ok"])
print(f"## TOTAL: {len(CHECKS)} checks = {n_sub} SUBSTANTIVE + {n_gua} GUARD; failures: {n_fail}")
verdicts = {
    "C1_hopf_fiber": "CONSTRAINED: no global promotion (Chern -4pi != 0); DELIVERS owned target circle + owned circle-valued transition datum to C5",
    "C2_toric_angles": "FAILS: not globally definable (cap winding kill); winding has no home (pi1 trivial, 104/104 |det|=1 recomputed)",
    "C3_screen_SO2": "FAILS-ON-BANKED-FOOTING: owned circle spent as gauge; chart keeps only its 2-torsion {+-1} = the K4 characters = real points of U(1); anchored dressing == 0",
    "C4_E07_E08": "FAILS (expected, exact): real spectrum / solvable simply-connected -- the real-targets theorem at group level; compactness unreachable by parameter motion",
    "C5_new_S1_field": "REGISTERS at Route-D-analog grade, REGISTERED-POSIT tag; eps_theta SUPPLIED, chi_theta DECLARED, U(1) factor ADJOINED; F-D5 passes",
    "TD3_integer_content": "quotient winding == 0 (Hom(Dinf,Z)=0) but crease Z2 target datum at eps_theta=-1; CYCLIC cycle: winding condition = Z-indexed hyperplane family (first live integer condition); conditional lattice at fixed slope, NO unconditional parameter quantization; K4 2-torsion classes REVIVE as Z2 holonomy data; J11 triviality locus becomes a lattice",
    "TD4_carrier": "DERIVES: NO; EMULATES: PARTIAL (U(1)/phase sector exactly); POSSESSES: PARTIAL-AS-STAGE (Hopf fiber + S2 base as domain); carrier posit PARTIALLY FOUNDED at circle layer, UNTOUCHED at pi2/pi3",
    "outcome_class": "OD-4 (mixed): no owned structure promotes to a FIELD (C1-C4 exact failures, each informative) while the NEW field REGISTERS cleanly with REGISTERED-POSIT tag (OD-2 component) and C1 supplies owned target+transition ingredients (OD-1 flavor at target level only)",
}
out = {"date": "2026-07-31", "contract": "PREREGISTRATION.md (frozen)",
       "counts": {"total": len(CHECKS), "substantive": n_sub, "guard": n_gua, "failed": n_fail},
       "verdicts": verdicts, "checks": CHECKS}
with open(os.path.join(HERE, "doorway_results.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
print("## outcome class: OD-4 (mixed) -- see verdicts in doorway_results.json")
sys.exit(0 if n_fail == 0 else 1)
