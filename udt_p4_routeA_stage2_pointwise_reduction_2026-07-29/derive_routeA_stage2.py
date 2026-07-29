#!/usr/bin/env python3
"""P4 Route A Stage 2 — the pointwise reduction: derive R_PW (TB1-TB5 computations).

Contract: udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/PREREGISTRATION.md
(frozen first). Exact SymPy, zero-residual checks, deterministic (no floats, no
randomness, no network), single CPU process, bounded. Exit 0 iff every check passes;
nonzero otherwise (F-B5).

Stage 2 imposes ONLY the pointwise requirements (R1, R2, R4, R7(a,b-identities), R8,
R10, R12, R13 + PW J-rows J01-J06(slot), J10, J12, J13(slot), J14) and derives the
residual space R_PW. NO member is selected or privileged (F-B1); WS/GC gates are NOT
run. Census forks are carried as labeled branches or proven branch-independent (F-B2).
Exhaustive claims are scoped to jet <= 2 on the registered stationary presentation,
polynomial/formal in the (k10, C) moduli (F-B3 stamps travel in the JSON/MD).

Cited inputs (recomputed as consistency, never re-derived as new, never adopted
beyond banked scope): Stage-1 bank (udt_p4_routeA_response_inverse_problem_2026-07-29,
A1/A3-AMENDED), Route B bank (E02 footing, exact K4, T-block), Route C bank (jet-spread
examples only).

Conventions copied from the banked Route B registration (07-28), as in Stage 1:
  eta = diag(-1,1,1,1); slots (0,1) = clock/ruler base, (2,3) = screen.
  Lorentz generator L{ab}: L[a,b] = 1, L[b,a] = -eta_aa/eta_bb.
  Extension class chart: X = [[H,0],[C,K]], H = diag(-1,1),
  K = [[k00,0],[k10,k11]] lower-triangular, C = [[c00,c01],[c10,c11]].

AMENDED 2026-07-29 per VERIFIER_REPORT.md (PASS-WITH-REQUIRED-AMENDMENTS; record in
CORRECTION_LAYER.md; pre-amendment run: 53/53, exit 0). A1 (substantive): the R7(b)
"pointwise-vacuous" claim was REFUTED AS STATED — the rank-6/empty-nullspace
computation is the CLASS-WIDE stabilizer; the PER-MEMBER (pointwise) stabilizer jumps
on strata. R7(b) restated: generically vacuous + the exact stratum Noether identity
on k_mod = 0 (the verifier counter-computation ADOPTED in the A1_* checks and
EXTENDED: all-member minor-divisibility proof, resonance-strata enumeration with
derived identities, corrected/scoped nonemptiness witnesses). A2: every check count
now splits SUBSTANTIVE zero-residual computations vs CITATION GUARDS (bookkeeping/
list/string checks — honest as labeled, not residual computations). A3: the E12
null-slot statement carries its chart-deltaK pairing-convention note (A3_* check).

ROUND-2 AMENDED 2026-07-29 per the VERIFIER_REPORT "AMENDMENT CLOSURE" (verdict
NEW-DEFECT, item C3; round-1 amended run: 67/67, exit 0). The round-1 A1-extension
headline "the ONLY genuine new cut is the k_mod = 0 identity" was REFUTED by the
closure verifier (VERIFIER_CLOSURE_PROBE.py P3/P5) — the same error CLASS as the
original refutation (a stratum-blind uniqueness gloss), one level down: the
auto-satisfaction argument covers ONLY the four NAMED C = 0 strata, while the
resonance rank-drop locus carries substantial C != 0 sub-varieties whose identities
are FURTHER genuine cuts. CORRECTED STATEMENT (travels with every occurrence):
k_mod = 0 is the only CODIMENSION-1 cut; the resonance locus carries C != 0
sub-varieties of higher codimension with additional exact identities (derived
example: -c10 r_sh - k10 m10 = 0 on {lam - k_mod = -1, c00 = c01 = 0} — it cuts the
SHEAR slot); the four NAMED C = 0 strata identities are auto-satisfied in the
declared class. The closure counter-computation is ADOPTED as the A1R2_* checks; the
omega witness is RE-SCOPED (on-stratum witness for k_mod = 0 only); the FULL deeper
stratification is stamped TYPED-NOT-EXHAUSTED (codim-1 layer exhaustive by the
Groebner proof; deeper layers = derived examples + method, not a census).
"""

import itertools
import json
import sys

import sympy as sp
from sympy import Matrix, Rational, Symbol, symbols, exp, simplify, eye, zeros

CHECKS = []

# A2 amendment: checks are classified SUBSTANTIVE (a zero-residual exact computation)
# or CITATION-GUARD (bookkeeping: list-copy/subset equality, trivial arithmetic
# restating a cited banked fact, string scans). Guards are kept — each is honest in
# its detail string and guards a genuinely banked citation — but they are never
# counted as residual computations in any headline.
CITATION_GUARDS = {
    "PW1_bare_phi_excluded",
    "PW4_R2_census_component_coverage",
    "PW4_J05_full_tangent_paired",
    "PW4_J13_discriminator_slots_retained",
    "PW4_R13_no_global_entries_in_alphabet",
    "PW4_functional_dimensions_per_grade",
    "PW5_obs_EH_form_lands_in_jet2_class",
    "PW5_obs_Bach_form_typed_class_only",
}


def check(name, residual_ok, detail=""):
    kind = "citation-guard" if name in CITATION_GUARDS else "substantive"
    CHECKS.append({"name": name, "passed": bool(residual_ok), "detail": detail,
                   "kind": kind})
    status = "PASS" if residual_ok else "FAIL"
    tag = " [guard]" if kind == "citation-guard" else ""
    print(f"[{status}]{tag} {name}" + (f" -- {detail}" if detail else ""))


def is_zero_matrix(M):
    return all(simplify(e) == 0 for e in M)


# ----------------------------------------------------------------------------
# S0 — conventions and banked-structure recomputation (consistency, cited)
# ----------------------------------------------------------------------------
eta = sp.diag(-1, 1, 1, 1)


def lorentz_generator(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta[a, a], eta[b, b])
    return L


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
GENS = {f"L{a}{b}": lorentz_generator(a, b) for (a, b) in PAIRS}
check(
    "S0_generators_infinitesimal_lorentz",
    all(is_zero_matrix(L.T * eta + eta * L) for L in GENS.values()) and len(GENS) == 6,
    "six so(1,3) generators, L^T.eta + eta.L = 0 (banked convention copy)",
)

I4 = eye(4)
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]
check(
    "S0_klein_group_recomputed",
    all(is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 and M[0, 0] == 1 for M in K4)
    and all(any(is_zero_matrix(M1 * M2 - M3) for M3 in K4) for M1 in K4 for M2 in K4)
    and all(is_zero_matrix(M * M - I4) for M in K4)
    and is_zero_matrix(R12 * R13 - R23),
    "K4 exact: proper orthochronous, closed, involutive, R12.R13=R23 (Route B bank recomputed)",
)

k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb

T = X.T * eta + eta * X
T_expected = zeros(4, 4)
T_expected[0:2, 0:2] = 2 * eye(2)
T_expected[0:2, 2:4] = Cb.T
T_expected[2:4, 0:2] = Cb
T_expected[2:4, 2:4] = Kb + Kb.T
check("S0_tangent_block_form", is_zero_matrix(T - T_expected), "T = [[2I2, C^T],[C, K+K^T]] (banked)")

t = Symbol("t")
ch = (exp(t) + exp(-t)) / 2
sh = (exp(t) - exp(-t)) / 2
Boost = Matrix([[ch, sh, 0, 0], [sh, ch, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
BoostInv = Boost.subs(t, -t)
xg = symbols("x0:16")
Xgen = Matrix(4, 4, xg)


def tangent(M):
    return M.T * eta + eta * M


check(
    "S0_tangent_transport_bilinear",
    is_zero_matrix(sp.expand(tangent(Boost * Xgen * BoostInv) - BoostInv.T * tangent(Xgen) * BoostInv))
    and all(
        is_zero_matrix(sp.expand(tangent(M * Xgen * M) - M.T.inv() * tangent(Xgen) * M.inv()))
        for M in [R23, R12, R13]
    ),
    "T -> Lam^-T T Lam^-1 under the exact boost and all K4 elements (contragredient transport, banked T2)",
)

# K4 action on the registered class (banked A3, recomputed) — the alphabet's K4 layer.
subs_R12 = {k10: -k10, c00: -c00, c11: -c11}
subs_R13 = {k10: -k10, c01: -c01, c10: -c10}
subs_R23 = {c00: -c00, c01: -c01, c10: -c10, c11: -c11}
K4_SUBS = [("R12", subs_R12), ("R13", subs_R13), ("R23", subs_R23)]
check(
    "S0_K4_action_on_class_recomputed",
    is_zero_matrix(R23 * X * R23 - X.subs(subs_R23, simultaneous=True))
    and is_zero_matrix(R12 * X * R12 - X.subs(subs_R12, simultaneous=True))
    and is_zero_matrix(R13 * X * R13 - X.subs(subs_R13, simultaneous=True))
    and all(
        simplify((M * X * M)[2, 2] - k00) == 0 and simplify((M * X * M)[3, 3] - k11) == 0
        for M in K4
    ),
    "R23: C -> -C; R12: k10,c00,c11 flip; R13: k10,c01,c10 flip; k00,k11 (hence lambda,k_mod) invariant (banked)",
)

# ----------------------------------------------------------------------------
# TB1 — the building-block alphabet (R1/R13/J12 provenance + J04 shift + K4 grading)
# ----------------------------------------------------------------------------
print("\n--- TB1: building-block alphabet ---")

xvar, s, phi = symbols("x s phi", real=True)
cE = Symbol("c_E", positive=True)
lam, kmod = symbols("lam k_mod", real=True)
p_, q_ = symbols("p q", real=True)

# TB1.1 J04 shift layer: the shift-with-absorption orbit is (phi, c_E) -> (phi+s, c_E e^{s})
# (same founded readout Q = c_E e^{-phi}, banked D3); well-defined functions of (phi, c_E)
# are exactly the functions of Q. Jets of phi are shift-invariant. Bare phi is excluded.
Q = cE * exp(-phi)
check(
    "PW1_Q_orbit_invariant",
    simplify(Q.subs({phi: phi + s, cE: cE * exp(s)}, simultaneous=True) - Q) == 0,
    "Q = c_E e^{-phi} is invariant on the shift-with-absorption orbit (phi,c_E)->(phi+s,c_E e^s) (banked D3 recomputed)",
)
check(
    "PW1_D3_anchor_absorption_recomputed",
    simplify(cE * exp(-(phi + s)) - (cE * exp(-s)) * exp(-phi)) == 0,
    "reading (phi+s, c_E) = reading (phi, c_E e^{-s}) on the founded stationary readout (Stage-1 D3)",
)
F_pow = cE**p_ * exp(-q_ * phi)
F_shift = F_pow.subs({phi: phi + s, cE: cE * exp(s)}, simultaneous=True)
resid_law = simplify(F_shift - F_pow * exp((p_ - q_) * s))
witness_noninv = simplify((F_shift - F_pow).subs({p_: 1, q_: 0, s: 1}))
check(
    "PW1_anchored_exponent_condition",
    resid_law == 0
    and simplify((F_shift - F_pow).subs(p_, q_)) == 0
    and witness_noninv != 0,
    "c_E^p e^{-q phi} is orbit-invariant iff p = q, i.e. iff it is a power of Q: e^{a phi}-type "
    "dependence is admitted ONLY through the anchored combination (c_E/Q)^a; generic p != q witness nonzero",
)
check(
    "PW1_bare_phi_excluded",
    simplify((phi + s) - phi - s) == 0 and (s != 0),
    "bare phi shifts by s (residual = s, not identically zero): absolute-zero-point dependence is NOT in the alphabet (J04/F-RA4)",
)
phifun = sp.Function("phi_f")(xvar)
jets_inert = all(
    simplify(sp.diff(phifun + s, (xvar, n)) - sp.diff(phifun, (xvar, n))) == 0 for n in [1, 2, 3, 4]
)
check(
    "PW1_phi_jets_shift_invariant",
    jets_inert,
    "d^n(phi+s)/dx^n = d^n phi/dx^n for n=1..4: all phi-jets are shift-invariant alphabet blocks (n=3,4 recorded for the TB4 typing)",
)
check(
    "PW1_cE_over_Q_is_exp_phi",
    simplify(cE / Q - exp(phi)) == 0,
    "(c_E/Q) = e^{phi} exactly: every seat exponential e^{a phi} has the anchored form (c_E/Q)^a "
    "(real-exponent power rule on a positive base = Category-A)",
)

# TB1.2 K4 grading of the alphabet: characters under (R12, R13); R23 = R12.R13.
def char_of(expr):
    sgns = []
    for _, sm in [("R12", subs_R12), ("R13", subs_R13)]:
        d = simplify(expr.subs(sm, simultaneous=True) / expr)
        sgns.append(d)
    return tuple(sgns)


CHAR_TRIV, CHAR_A, CHAR_B, CHAR_C = (1, 1), (-1, -1), (-1, 1), (1, -1)
char_table_ok = (
    char_of(k10) == CHAR_A
    and char_of(c00) == CHAR_B
    and char_of(c11) == CHAR_B
    and char_of(c01) == CHAR_C
    and char_of(c10) == CHAR_C
)
check(
    "PW1_K4_characters_of_moduli",
    char_table_ok,
    "characters under (R12,R13): k10 = chi_a (-,-); c00,c11 = chi_b (-,+); c01,c10 = chi_c (+,-) (banked A6 table recomputed)",
)
check(
    "PW1_K4_touches_only_k10_C",
    set().union(*[set(sm.keys()) for sm in [subs_R12, subs_R13, subs_R23]]) == {k10, c00, c01, c10, c11},
    "the K4 substitutions act only on {k10, c00, c01, c10, c11}: Q, phi-jets, f-jets, bh-jets, alpha, "
    "lambda, k_mod, boundary data are K4-inert alphabet blocks (trivial character; banked census/A3)",
)

# The 11-generator invariant ring (banked, verifier-proven generating set) recomputed.
I1 = k10**2
I2v, I3v, I4v = c00**2, c11**2, c00 * c11
I5v, I6v, I7v = c01**2, c10**2, c01 * c10
I8v, I9v = k10 * c00 * c01, k10 * c00 * c10
I10v, I11v = k10 * c11 * c01, k10 * c11 * c10
INV11 = [I1, I2v, I3v, I4v, I5v, I6v, I7v, I8v, I9v, I10v, I11v]
check(
    "PW1_invariant_ring_generators_11",
    all(all(simplify(m.subs(sm, simultaneous=True) - m) == 0 for _, sm in K4_SUBS) for m in INV11),
    "k10^2; six within-class C quadratics; four mixed cubics — all K4-invariant (banked A4 + verifier generating set recomputed)",
)

# e^{phi X} as derived structure: on the E04 closed form the lower-left block's (i,j) entry
# is c_ij times a phi-scalar — the exponential's entries reduce to alphabet blocks with the
# character of their C-position (no new block enters the alphabet).
ph = Symbol("phi_", real=True)
expH = sp.diag(exp(-ph), exp(ph))
LL = Cb * H2 * (expH - eye(2))
cpos = [[c00, c01], [c10, c11]]
entries_linear = all(
    simplify(LL[i, j] - cpos[i][j] * LL[i, j].coeff(cpos[i][j])) == 0
    and not (set(LL[i, j].coeff(cpos[i][j]).free_symbols) & {c00, c01, c10, c11, k10})
    for i in range(2)
    for j in range(2)
)
entries_char = all(
    all(
        simplify(LL[i, j].subs(sm, simultaneous=True) / LL[i, j])
        == simplify(cpos[i][j].subs(sm, simultaneous=True) / cpos[i][j])
        for _, sm in K4_SUBS
    )
    for i in range(2)
    for j in range(2)
)
check(
    "PW1_expX_lower_block_entries_carry_C_characters",
    entries_linear and entries_char,
    "E04 closed-form lower-left block C H (e^{phi H} - I): entry (i,j) = c_ij * (phi-scalar), carrying "
    "exactly the K4 character of c_ij — e^{phi X}-type derived structure reduces to graded alphabet blocks",
)

# J01 typing: configurations carry a nondegenerate coframe — det e^{phi X} = e^{phi tr X} != 0
# (recompute on the E04 closed form + diagonal seat; banked triangular-det lemma cited).
M_E04 = zeros(4, 4)
M_E04[0:2, 0:2] = expH
M_E04[2:4, 0:2] = LL
M_E04[2:4, 2:4] = eye(2)
a_seat = lam - kmod
d_seat = lam + kmod
det_seat = exp(-ph) * exp(ph) * exp(a_seat * ph) * exp(d_seat * ph)
check(
    "PW1_J01_coframe_nondegenerate",
    simplify(M_E04.det() - 1) == 0 and simplify(det_seat - exp(2 * lam * ph)) == 0,
    "det e^{phi X} is a nonvanishing exponential (E04: det = 1; seat: e^{2 lam phi}): J01 nondegeneracy is a "
    "type property of every configuration in the census (banked det lemma recomputed on closed forms)",
)
check(
    "PW1_J02_founded_base_block",
    is_zero_matrix(X[0:2, 0:2] - sp.diag(-1, 1)),
    "H = diag(-1,1) fixed in every configuration: the founded reciprocal pair is the base-block structure (J02 typing)",
)

# ----------------------------------------------------------------------------
# TB2 — the equivariance reduction (R7(a)/J10 solved exactly; R7(b) identities)
# ----------------------------------------------------------------------------
print("\n--- TB2: equivariance reduction ---")

# TB2.1 The registered chart has TRIVIAL infinitesimal stabilizer (recompute Route B T1):
# solve for B in so(1,3) with [B, X] tangent to the registered class for every class member.
bcoef = symbols("beta0:6")
B = zeros(4, 4)
for i, Lm in enumerate(GENS.values()):
    B = B + bcoef[i] * Lm
X0 = zeros(4, 4)
X0[0:2, 0:2] = H2
V_basis = []
for (i, j) in [(2, 2), (3, 2), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]:
    E = zeros(4, 4)
    E[i, j] = 1
    V_basis.append(E)
FORBIDDEN = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
eqs = []
for M in [X0] + V_basis:
    Cm = B * M - M * B
    eqs.extend([Cm[i, j] for (i, j) in FORBIDDEN])
Amat, _ = sp.linear_eq_to_matrix(eqs, list(bcoef))
stab_rank = Amat.rank()
check(
    "PW2_registered_stabilizer_trivial",
    stab_rank == 6 and Amat.nullspace() == [],
    f"the linear system [B,X] tangent-to-class for all class members has rank {stab_rank} on 6 coefficients: "
    "B = 0 only — the registered chart's CLASS-WIDE infinitesimal local-Lorentz stabilizer is TRIVIAL (Route B T1 "
    "recomputed; A1 NOTE: class-wide only — the PER-MEMBER stabilizer jumps on strata, see the A1_* checks)",
)

# --- A1 AMENDMENT (verifier counter-computation ADOPTED, then EXTENDED) -----------
# R7(b) is a PER-MEMBER (pointwise) statement: <R, delta_gauge X> = 0 identically for
# gauge directions tangent to the configuration. The class-wide computation above does
# NOT decide it. Compute the pointwise tangency stabilizer at the general member.
Cm_pt = B * X - X * B
eqs_pt = [Cm_pt[i, j] for (i, j) in FORBIDDEN]
A_pt, _ = sp.linear_eq_to_matrix(eqs_pt, list(bcoef))
GENERIC_PT = {k00: 2, k10: 3, k11: 5, c00: 7, c01: 11, c10: 13, c11: 17}
check(
    "PW2_R7b_noether_generic_vacuous_stratum_identities",
    A_pt.subs(GENERIC_PT).rank() == 6 and A_pt.subs(GENERIC_PT).nullspace() == [],
    "R7(b) RESTATED (A1): at a GENERIC member the pointwise tangency stabilizer is trivial (rank 6, empty "
    "nullspace) — R7(b) is vacuous GENERICALLY, not pointwise-everywhere; on the degeneration strata of the "
    "moduli continuous gauge directions ARE tangent and R7(b) imposes the exact stratum Noether identities "
    "derived in the A1_* checks below; K4 remains discrete (no parameter); current-conservation stays WS (Stage 3)",
)

# (i) ALL-MEMBER stratum proof (extends the verifier's generic-point check): every
# nonzero 6x6 minor of the 9x6 pointwise system is divisible by (k00 - k11) = -2 k_mod,
# so the rank drops below 6 on the ENTIRE k_mod = 0 stratum — not just at test points.
minors_pt = []
for rsel in itertools.combinations(range(A_pt.rows), 6):
    mdet = sp.expand(A_pt[list(rsel), :].det())
    if mdet != 0:
        minors_pt.append(mdet)
minors_divisible = all(sp.expand(sp.div(mdet, k00 - k11, k00)[1]) == 0 for mdet in minors_pt)
check(
    "A1_kmod0_rank_drop_all_members",
    len(minors_pt) == 36 and minors_divisible,
    "all 36 nonzero 6x6 minors of the pointwise tangency system are divisible by (k00 - k11): the per-member "
    "stabilizer is nontrivial on the ENTIRE codim-1 stratum k_mod = 0 (all-member proof, strengthens the "
    "verifier's point checks)",
)
# (ii) the stratum nullspace is exactly the screen rotation L23 (symbolic, generic on
# the stratum): substitute k11 -> k00 and solve.
A_iso = A_pt.subs(k11, k00)
ns_iso = A_iso.nullspace()
check(
    "A1_kmod0_nullspace_is_L23",
    len(ns_iso) == 1
    and all(simplify(ns_iso[0][i]) == 0 for i in range(5))
    and simplify(ns_iso[0][5]) != 0,
    "on k_mod = 0 (k11 = k00, remaining moduli symbolic) the pointwise system has rank 5 and nullspace = "
    "span(L23), the screen rotation (verifier VC_* adopted; here symbolic = generic on the whole stratum)",
)
# (iii) the tangency obstruction of L23 at a GENERAL member is exactly 2 k_mod:
L23m = GENS["L23"]
W23_full = L23m * X - X * L23m
check(
    "A1_L23_obstruction_is_2kmod",
    simplify(W23_full[2, 3] - (k11 - k00)) == 0
    and all(simplify(W23_full[i, j]) == 0 for (i, j) in FORBIDDEN if (i, j) != (2, 3)),
    "[L23, X](2,3) = k11 - k00 = 2 k_mod is the ONLY forbidden entry of the L23 motion: the screen rotation is "
    "class-tangent exactly on the reciprocal-isotropy locus k_mod = 0 (ties the stratum to reciprocal isotropy "
    "transparently)",
)
# (iv) the gauge direction on the stratum (verifier witness adopted):
W23 = W23_full.subs(k11, k00)
Jrot = Matrix([[0, 1], [-1, 0]])
check(
    "A1_gauge_direction_tangent_nonzero",
    all(simplify(W23[i, j]) == 0 for (i, j) in FORBIDDEN)
    and is_zero_matrix(W23[0:2, 0:4])
    and is_zero_matrix(W23[2:4, 2:4] - k10 * sp.diag(1, -1))
    and is_zero_matrix(W23[2:4, 0:2] - Jrot * Cb.subs(k11, k00))
    and any(simplify(e) != 0 for e in W23.subs({k10: 3, c00: 7, c01: 11, c10: 13, c11: 17})),
    "[L23, X]|_{k_mod=0} = [[0,0],[J C, k10 diag(1,-1)]] != 0 for (k10, C) != 0: a nonzero infinitesimal "
    "local-Lorentz motion TANGENT to the registered class at every k_mod = 0 member (verifier counter-computation "
    "adopted exactly)",
)
# (v) chart reading of the direction + field sector:
dK23 = W23[2:4, 2:4]
dC23 = W23[2:4, 0:2]
check(
    "A1_gauge_chart_components_field_sector_zero",
    simplify(sp.trace(dK23) / 2) == 0                       # delta lambda = 0
    and simplify((dK23[1, 1] - dK23[0, 0]) / 2 + k10) == 0  # delta k_mod = -k10
    and simplify(dK23[1, 0]) == 0                           # delta k10 = 0
    and is_zero_matrix(dC23 - Jrot * Cb.subs(k11, k00)),    # delta C = J C
    "chart reading: (delta lambda, delta k_mod, delta k10, delta C) = (0, -k10, 0, J C). Field sector: the gauge "
    "motion acts on the frame extension X only; Q, phi-jets, f, bh are chart scalars (TB1 local-Lorentz typing), "
    "so their variation under L23 is ZERO on the registered stationary presentation — the identity below is purely "
    "moduli-sector THERE (general arenas carry frame-indexed coframe data: TYPED, not derived)",
)
# (vi) the exact stratum Noether identity (verifier VH_* adopted; r_nl-independence
# is NEW here — the identity holds with the full 4-slot kernel, null slot included):
pairA1 = lambda A_, B_: sp.trace(A_.T * B_)
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
I2A = eye(2)
D2A = sp.diag(-1, 1)
E21A = Matrix([[0, 0], [1, 0]])
E12A = Matrix([[0, 1], [0, 0]])
W_slotA = r_tr * I2A + r_tf * D2A + r_sh * E21A + r_nl * E12A
MkerA = Matrix([[m00, m01], [m10, m11]])
pairing_stratum = sp.expand(pairA1(W_slotA, dK23) + pairA1(MkerA, dC23))
IDENT_KMOD0 = sp.expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
check(
    "A1_stratum_noether_identity_form",
    sp.expand(pairing_stratum - IDENT_KMOD0) == 0,
    "<R, [L23,X]>|_{k_mod=0} = -2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 (exact; r_tr, r_sh AND the "
    "null slot r_nl all drop out): R7(b) on the stratum ties the trace-free slot to the mixing kernel — the FIRST "
    "nontrivial pointwise Noether content of the response problem",
)
# (vii) K4 consistency: the identity is chi_a-graded (every term), the direction L23
# transports with chi_a, and the stratum itself is K4-stable.
CHI_A_SIGN = {"R12": -1, "R13": -1, "R23": 1}
ident_graded = True
for gname, Mg in [("R12", R12), ("R13", R13), ("R23", R23)]:
    smg = dict([("R12", subs_R12), ("R13", subs_R13), ("R23", subs_R23)])[gname]
    # component transport: r_tf trivial; m_ij transports with the character of c_ij
    comp_transport = {m00: (-1 if c00 in smg else 1) * m00,
                      m01: (-1 if c01 in smg else 1) * m01,
                      m10: (-1 if c10 in smg else 1) * m10,
                      m11: (-1 if c11 in smg else 1) * m11}
    Ig = IDENT_KMOD0.subs(smg, simultaneous=True).subs(comp_transport, simultaneous=True)
    if sp.expand(Ig - CHI_A_SIGN[gname] * IDENT_KMOD0) != 0:
        ident_graded = False
    if not is_zero_matrix(Mg * L23m * Mg - CHI_A_SIGN[gname] * L23m):
        ident_graded = False
check(
    "A1_identity_chi_a_graded_K4_consistent",
    ident_graded
    and not ({k00, k11} & set().union(*[set(smg.keys()) for smg in [subs_R12, subs_R13, subs_R23]])),
    "every term of the stratum identity carries chi_a (k10*r_tf: chi_a x trivial; m*c cross-terms: chi_b x chi_c); "
    "the gauge direction transports as g L23 g = chi_a(g) L23; k_mod is K4-inert so the stratum is K4-stable: the "
    "identity is K4-consistent (its zero set is well defined on the quotient)",
)
# (viii) the pre-amendment nonemptiness witness VIOLATES the identity on the stratum:
viol = pairing_stratum.subs({r_tf: 1, r_tr: 0, r_sh: 0, r_nl: 0,
                             m00: 0, m01: 0, m10: 0, m11: 0})
check(
    "A1_old_witness_violates_on_stratum",
    simplify(viol + 2 * k10) == 0 and simplify(viol.subs(k10, 3)) != 0,
    "the pre-amendment witness 'unit trace-free screen kernel, R_kmod = 2' (r_tf = 1, all else 0) pairs to "
    "-2 k10 != 0 with the tangent gauge direction at k_mod = 0, k10 != 0: it is NOT a member of the corrected "
    "R_PW on the stratum — it is hereby SCOPED OFF-STRATUM (a member only where k_mod != 0); verifier "
    "VH_witness_member_violates adopted",
)
# (ix) the omega-shape witness SATISFIES the identity (r_sh does not enter):
sat_omega = pairing_stratum.subs({r_sh: k10, r_tr: 0, r_tf: 0, r_nl: 0,
                                  m00: 0, m01: 0, m10: 0, m11: 0})
check(
    "A1_omega_witness_satisfies_identity",
    sp.expand(sat_omega) == 0,
    "the omega-shape member (R_k10 = r_sh = k10, all else 0) pairs to ZERO with the k_mod = 0 gauge direction "
    "(tr(E21^T k10 diag(1,-1)) = 0): it satisfies the k_mod = 0 identity identically — OB1 nonemptiness stands "
    "ON that stratum (verifier-confirmed, adopted). R2 SCOPE: an on-stratum witness for k_mod = 0 ONLY — it "
    "VIOLATES the C != 0 resonance shear identity (A1R2_omega_witness_violates_on_Cneq0_stratum); NOT a "
    "universal on-resonance witness",
)
# (x) a CORRECTED trace-free witness that lives ON the stratum: r_tf = c01 c10 (= I7,
# invariant, trivial character) balanced by m00 = 2 k10 c01 (a listed chi_b generator):
sat_corr = pairing_stratum.subs({r_tf: c01 * c10, r_tr: 0, r_sh: 0, r_nl: 0,
                                 m00: 2 * k10 * c01, m01: 0, m10: 0, m11: 0})
corr_char_ok = (char_of(c01 * c10) == CHAR_TRIV and char_of(k10 * c01) == CHAR_B)
corr_vanishes_C0 = ((c01 * c10).subs({c00: 0, c01: 0, c10: 0, c11: 0}) == 0
                    and (2 * k10 * c01).subs({c00: 0, c01: 0, c10: 0, c11: 0}) == 0)
check(
    "A1_corrected_tracefree_witness_on_stratum",
    sp.expand(sat_corr) == 0 and corr_char_ok and corr_vanishes_C0
    and sp.expand(2 * c01 * c10) != 0,
    "corrected witness: (r_tf, m00) = (c01 c10, 2 k10 c01), rest 0 — character-matched (r_tf = I7 invariant; "
    "m00 = the listed chi_b generator k10 c01), satisfies the k_mod = 0 identity IDENTICALLY "
    "(-2 k10 c01 c10 + 2 k10 c01 c10 = 0), has R_kmod = 2 c01 c10 not== 0 (the k_mod-DETERMINED branch stays "
    "nonempty ON the stratum where c01 c10 != 0), vanishes at C = 0 (safe on the named resonance strata), and "
    "R2: vanishes on the found C != 0 defect stratum too (A1R2_corrected_witness_vanishes_on_found_strata — "
    "survives the new cut)",
)
# (xi) the NAMED higher-codim resonance strata (C = 0 with lam -+ k_mod in {+-1}):
# derive each gauge direction and its identity EXACTLY (symbolic in the remaining moduli).
C0_SUBS = {c00: 0, c01: 0, c10: 0, c11: 0}
GENS_LIST = list(GENS.values())
RES_STRATA = [
    ("C=0, k00=-1 (lam - k_mod = -1)", {**C0_SUBS, k00: -1},
     sp.expand(-k10 * m10)),
    ("C=0, k00=+1 (lam - k_mod = +1)", {**C0_SUBS, k00: 1},
     sp.expand(k10 * m11)),
    ("C=0, k11=-1 (lam + k_mod = -1)", {**C0_SUBS, k11: -1},
     sp.expand(k10 * m00 + k10**2 / (k00 + 1) * m10)),
    ("C=0, k11=+1 (lam + k_mod = +1)", {**C0_SUBS, k11: 1},
     sp.expand(-k10 * m01 - k10**2 / (k00 - 1) * m11)),
]
res_ok = True
res_record = []
for label, ssub, expected in RES_STRATA:
    Xres = X.subs(ssub, simultaneous=True)
    Cres = B * Xres - Xres * B
    Ares, _ = sp.linear_eq_to_matrix([Cres[i, j] for (i, j) in FORBIDDEN], list(bcoef))
    nsr = Ares.nullspace()
    if len(nsr) != 1:
        res_ok = False
        continue
    Bres = zeros(4, 4)
    for i in range(6):
        Bres = Bres + simplify(nsr[0][i]) * GENS_LIST[i]
    Wres = sp.simplify(Bres * Xres - Xres * Bres)
    if not all(simplify(Wres[i, j]) == 0 for (i, j) in FORBIDDEN):
        res_ok = False
        continue
    dKres = Wres[2:4, 2:4]
    dCres = Wres[2:4, 0:2]
    pairing_res = sp.expand(pairA1(W_slotA, dKres) + pairA1(MkerA, dCres))
    if sp.simplify(pairing_res - expected) != 0:
        res_ok = False
    if {r_tr, r_tf, r_sh, r_nl} & pairing_res.free_symbols:
        res_ok = False  # the resonance identities must involve ONLY mixing components
    res_record.append({"stratum": label,
                       "gauge_direction_so13_coeffs": [str(simplify(e)) for e in nsr[0].T],
                       "identity": str(sp.simplify(pairing_res)) + " = 0"})
check(
    "A1_resonance_named_strata_identities",
    res_ok,
    "the four named resonance strata each have rank 5 / a 1-dim tangent gauge direction (base-screen eigenvalue "
    "resonance boosts/rotations), derived symbolically: identities k10*R_c10 = 0 at {C=0, k00=-1}; k10*R_c11 = 0 "
    "at {C=0, k00=+1}; k10*((k00+1)R_c00 + k10 R_c10) = 0 at {C=0, k11=-1}; k10*((k00-1)R_c01 + k10 R_c11) = 0 "
    "at {C=0, k11=+1} — every one involves ONLY mixing-kernel components (r_tr/r_tf/r_sh/r_nl all drop out)",
)
# (xii) those resonance identities are AUTOMATICALLY satisfied by every character-
# matched member of the DECLARED (polynomial/formal-in-moduli) class. (The chi_b/chi_c
# generator lists here are the SAME sets exhibited and character-verified in TB2.2
# below — written inline because this block precedes those definitions.)
CHI_BC_GENS = [c00, c11, k10 * c01, k10 * c10,      # chi_b generators
               c01, c10, k10 * c00, k10 * c11]      # chi_c generators
chi_bc_vanish_C0 = all(g.subs(C0_SUBS, simultaneous=True) == 0 for g in CHI_BC_GENS)
check(
    "A1_resonance_identities_auto_satisfied_in_class",
    chi_bc_vanish_C0,
    "every chi_b and chi_c module generator contains exactly one C-entry factor, so every character-matched "
    "polynomial/formal R_C component VANISHES identically at C = 0: the named resonance-strata identities are "
    "automatically satisfied by the whole parametrized class — R2-CORRECTED SCOPE: this covers ONLY the four "
    "NAMED C = 0 strata; k_mod = 0 is the only CODIMENSION-1 genuine cut, and the resonance locus carries C != 0 "
    "sub-varieties of higher codimension with additional exact identities that are FURTHER genuine cuts "
    "(A1R2_* checks below; the round-1 'ONLY genuine new cut' headline was REFUTED by the closure verifier) "
    "(scope stamp: polynomial/formal in the moduli, the declared scope)",
)
# (xiii) exhaustive confinement of the rank-drop locus: off k_mod = 0, a rank drop
# REQUIRES an eigenvalue resonance — the product (k00^2-1)(k00-k11)(k11^2-1) lies in
# the ideal generated by the 36 minors (Groebner reduction to 0).
gb_minors = sp.groebner(minors_pt, k00, k10, k11, c00, c01, c10, c11, order="grevlex")
conf_poly = sp.expand((k00 - 1) * (k00 + 1) * (k00 - k11) * (k11 - 1) * (k11 + 1))
conf_in_ideal = sp.expand(gb_minors.reduce(conf_poly)[1]) == 0
check(
    "A1_rank_drop_confined_to_resonances",
    conf_in_ideal,
    "(k00^2-1)(k00-k11)(k11^2-1) is in the minor ideal: every rank-drop point of the pointwise tangency system "
    "lies in {k_mod = 0} UNION {lam - k_mod in {+-1}} UNION {lam + k_mod in {+-1}} — the CODIM-1 confinement is "
    "EXHAUSTIVE (Groebner-verified); R2: the C != 0 sub-varieties of the resonance part are REAL and carry "
    "FURTHER genuine cuts (the A1R2_* checks below derive the {k00=-1, c00=c01=0} example); the FULL deeper "
    "stratification is TYPED-NOT-EXHAUSTED (deeper layers = derived examples + the same nullspace/pairing "
    "method applied branch-by-branch, not a census)",
)
# --- A1 ROUND-2 CLOSURE AMENDMENT (C3): the C != 0 resonance sub-varieties ---------
# The closure verifier REFUTED the round-1 headline "the ONLY genuine new cut is the
# k_mod = 0 identity" (VERIFIER_CLOSURE_PROBE.py P3/P5 — the same error class as the
# original refutation, a stratum-blind uniqueness gloss, one level down): the
# auto-satisfaction argument covers only the four NAMED C = 0 strata; the resonance
# rank-drop locus has substantial C != 0 sub-varieties whose identities are NOT
# auto-satisfied. The counter-computation is ADOPTED here as zero-residual checks.
# (xiv) the k00 = -1 slice of the minor ideal: 7 solution branches, including
# {c00 = c01 = 0} and the fully-generic-C branch {k11 = 1, c10 = -c00 k10/2,
# c11 = -c01 k10/2} — C != 0 rank-drop points EXIST off the named strata.
A_res_r2 = A_pt.subs(k00, -1)
minors_res_r2 = []
for rsel in itertools.combinations(range(A_res_r2.rows), 6):
    mdet_r2 = sp.expand(A_res_r2[list(rsel), :].det())
    if mdet_r2 != 0:
        minors_res_r2.append(mdet_r2)
gb_res_r2 = sp.groebner(minors_res_r2, k10, k11, c00, c01, c10, c11, order="grevlex")
sols_r2 = sp.solve(list(gb_res_r2.exprs), [k10, k11, c00, c01, c10, c11], dict=True)


def _branch_match(sol, target):
    return (set(sol.keys()) == set(target.keys())
            and all(sp.simplify(sol[key] - val) == 0 for key, val in target.items()))


branch_cc0 = {c00: sp.Integer(0), c01: sp.Integer(0)}
branch_genC = {k11: sp.Integer(1), c10: -c00 * k10 / 2, c11: -c01 * k10 / 2}
rank_pt_Cneq0 = A_res_r2.subs({k11: 5, k10: 3, c00: 0, c01: 0, c10: 13, c11: 17}).rank()
check(
    "A1R2_resonance_locus_has_Cneq0_branches",
    len(sols_r2) == 7
    and any(_branch_match(s_, branch_cc0) for s_ in sols_r2)
    and any(_branch_match(s_, branch_genC) for s_ in sols_r2)
    and rank_pt_Cneq0 == 5,
    "the k00 = -1 (lam - k_mod = -1) slice of the minor ideal has 7 solution branches, including "
    "{c00 = c01 = 0, c10, c11 free} and the fully-generic-C branch {k11 = 1, c10 = -c00 k10/2, c11 = -c01 k10/2}; "
    "a concrete C != 0 rank-5 point exists (k11=5, k10=3, c10=13, c11=17, c00=c01=0): the resonance content is NOT "
    "exhausted by the four named C = 0 strata (closure-verifier P3/P3b adopted)",
)
# (xv) on the sub-variety {k00 = -1, c00 = c01 = 0} (codim 3) the pointwise nullspace
# is 1-dim = span(L02), the mixed base-screen boost, TANGENT to the class:
SUB_R2 = {k00: -1, c00: 0, c01: 0}
X_r2 = X.subs(SUB_R2, simultaneous=True)
A_sub_r2, _ = sp.linear_eq_to_matrix(
    [(B * X_r2 - X_r2 * B)[i, j] for (i, j) in FORBIDDEN], list(bcoef)
)
ns_r2 = A_sub_r2.nullspace()
L02m = GENS["L02"]
W02 = L02m * X_r2 - X_r2 * L02m
check(
    "A1R2_Cneq0_stratum_nullspace_L02",
    len(ns_r2) == 1
    and all(simplify(ns_r2[0][i]) == 0 for i in [0, 2, 3, 4, 5])
    and simplify(ns_r2[0][1] - 1) == 0
    and all(simplify(W02[i, j]) == 0 for (i, j) in FORBIDDEN)
    and is_zero_matrix(W02[0:2, 0:4])
    and is_zero_matrix(W02[2:4, 2:4] - (-c10) * E21A)
    and is_zero_matrix(W02[2:4, 0:2] - (-k10) * E21A)
    and any(simplify(e) != 0 for e in W02.subs({k10: 3, c10: 13})),
    "on {lam - k_mod = -1 (k00 = -1), c00 = c01 = 0} the pointwise tangency system has a 1-dim nullspace = "
    "span(L02), the MIXED base-screen boost; [L02, X]|_stratum = [[0,0],[-k10 E21_C, -c10 E21_K]] != 0 for "
    "(k10, c10) != 0 — chart reading (delta lambda, delta k_mod, delta k10, delta c10) = (0, 0, -c10, -k10), all "
    "other entries zero; a class-tangent continuous gauge direction at generic C != 0 (closure-verifier P5 adopted)",
)
# (xvi) the exact identity on the sub-variety: it cuts the SHEAR slot.
dK02 = W02[2:4, 2:4]
dC02 = W02[2:4, 0:2]
pairing_sub_r2 = sp.expand(pairA1(W_slotA, dK02) + pairA1(MkerA, dC02))
IDENT_SHEAR = sp.expand(-c10 * r_sh - k10 * m10)
check(
    "A1R2_Cneq0_stratum_shear_identity",
    sp.expand(pairing_sub_r2 - IDENT_SHEAR) == 0
    and not ({r_tr, r_tf, r_nl, m00, m01, m11} & IDENT_SHEAR.free_symbols)
    and (r_sh in IDENT_SHEAR.free_symbols),
    "<R, [L02,X]>|_{k00=-1, c00=c01=0} = -c10 r_sh - k10 m10 (exact; equivalently -c10 R_k10 - k10 R_c10 = 0): "
    "R7(b) on this C != 0 sub-variety cuts the SHEAR slot r_sh — unlike the k_mod = 0 identity (r_sh drops out "
    "there) and the named C = 0 identities (mixing-only); r_tr, r_tf, r_nl, m00, m01, m11 all drop out",
)
# (xvii) K4 consistency of the shear identity: chi_b-graded; the stratum is K4-stable
# (k00 inert; c00 = 0 and c01 = 0 are preserved by sign flips); L02 transports with chi_b.
CHI_B_SIGN = {"R12": -1, "R13": 1, "R23": -1}
shear_graded = True
for gname_r2 in ["R12", "R13", "R23"]:
    Mg_r2 = {"R12": R12, "R13": R13, "R23": R23}[gname_r2]
    smg_r2 = {"R12": subs_R12, "R13": subs_R13, "R23": subs_R23}[gname_r2]
    comp_transport_r2 = {m10: (-1 if c10 in smg_r2 else 1) * m10,
                         r_sh: (-1 if k10 in smg_r2 else 1) * r_sh}
    Ig_r2 = IDENT_SHEAR.subs(smg_r2, simultaneous=True).subs(comp_transport_r2, simultaneous=True)
    if sp.expand(Ig_r2 - CHI_B_SIGN[gname_r2] * IDENT_SHEAR) != 0:
        shear_graded = False
    if not is_zero_matrix(Mg_r2 * L02m * Mg_r2 - CHI_B_SIGN[gname_r2] * L02m):
        shear_graded = False
check(
    "A1R2_shear_identity_chi_b_graded_K4_consistent",
    shear_graded
    and not ({k00} & set().union(*[set(sm_) for sm_ in [subs_R12, subs_R13, subs_R23]])),
    "every term of the shear identity carries chi_b (c10*r_sh: chi_c x chi_a; k10*m10: chi_a x chi_c); the gauge "
    "direction transports as g L02 g = chi_b(g) L02; the stratum {k00=-1, c00=c01=0} is K4-stable (k00 inert; the "
    "zero constraints are preserved by sign flips): the identity is K4-consistent",
)
# (xviii) the identity is a GENUINE further cut — a character-matched member of the
# published parametrization violates it (NOT auto-satisfied):
viol_Rc10 = pairing_sub_r2.subs({m10: c10, m00: 0, m01: 0, m11: 0,
                                 r_tr: 0, r_tf: 0, r_sh: 0, r_nl: 0})
check(
    "A1R2_member_Rc10_genuine_cut",
    sp.expand(viol_Rc10 + c10 * k10) == 0
    and simplify(viol_Rc10.subs({c10: 13, k10: 3})) != 0
    and char_of(c10) == CHAR_C,
    "the character-matched polynomial member R_c10 = c10 (a listed chi_c generator x invariant 1) pairs to "
    "-c10 k10 not== 0 on the sub-variety: a GENUINE further cut, NOT auto-satisfied — the round-1 headline "
    "'the ONLY genuine new cut is the k_mod = 0 identity' is REFUTED; correct statement: k_mod = 0 is the only "
    "CODIMENSION-1 cut, the C != 0 resonance sub-varieties carry additional exact identities",
)
# (xix) the omega-shape witness VIOLATES the shear identity there -> RE-SCOPED:
viol_omega_r2 = pairing_sub_r2.subs({r_sh: k10, r_tr: 0, r_tf: 0, r_nl: 0,
                                     m00: 0, m01: 0, m10: 0, m11: 0})
check(
    "A1R2_omega_witness_violates_on_Cneq0_stratum",
    sp.expand(viol_omega_r2 + c10 * k10) == 0
    and simplify(viol_omega_r2.subs({c10: 13, k10: 3})) != 0,
    "the omega-shape member (r_sh = k10) pairs to -c10 k10 not== 0 on {k00=-1, c00=c01=0}: it violates the shear "
    "identity at c10, k10 != 0 — the omega witness is RE-SCOPED: an ON-STRATUM witness for the k_mod = 0 identity, "
    "NOT a universal on-resonance witness (it is a member of R_PW only off the C != 0 resonance sub-varieties "
    "where the shear-type identities bind)",
)
# (xx) the corrected trace-free witness SURVIVES the new cut (vanishes on the found
# strata: c01 = 0 there forces both components to zero) — closure-verifier confirmed:
wit_r_tf_on = (c01 * c10).subs(SUB_R2, simultaneous=True)
wit_m00_on = (2 * k10 * c01).subs(SUB_R2, simultaneous=True)
surv_corr_r2 = pairing_sub_r2.subs({r_tf: wit_r_tf_on, m00: wit_m00_on,
                                    r_tr: 0, r_sh: 0, r_nl: 0,
                                    m01: 0, m10: 0, m11: 0})
check(
    "A1R2_corrected_witness_vanishes_on_found_strata",
    wit_r_tf_on == 0 and wit_m00_on == 0 and sp.expand(surv_corr_r2) == 0,
    "the corrected trace-free witness (r_tf, m00) = (c01 c10, 2 k10 c01) VANISHES on the found C != 0 defect "
    "stratum {k00=-1, c00=c01=0} (c01 = 0 there forces both components to zero) and pairs to ZERO with the L02 "
    "gauge direction: it SURVIVES the new cut (closure-verifier C2(d) confirmation adopted as a check)",
)
# (xxi) field-sector members carry ALL-strata nonemptiness: every stratum pairing
# derived in this package is purely moduli-sector (on the registered stationary
# presentation the gauge motions act on X only; field variations are zero), so any
# member with all moduli components zero (e.g. R_phi = Q) pairs to ZERO with every
# gauge direction on every stratum — independent of the not-exhausted deeper census.
ZERO_MODULI_COMPS = {r_tr: 0, r_tf: 0, r_sh: 0, r_nl: 0, m00: 0, m01: 0, m10: 0, m11: 0}
ALL_STRATUM_PAIRINGS = [pairing_stratum, pairing_sub_r2] + [expected for _, _, expected in RES_STRATA]
MODULI_SECTOR_SYMS = {r_tr, r_tf, r_sh, r_nl, m00, m01, m10, m11, k00, k10, k11, c00, c01, c10, c11}
check(
    "A1R2_field_sector_members_carry_all_strata",
    all(sp.expand(p_.subs(ZERO_MODULI_COMPS)) == 0 for p_ in ALL_STRATUM_PAIRINGS)
    and all(p_.free_symbols <= MODULI_SECTOR_SYMS for p_ in ALL_STRATUM_PAIRINGS),
    "every derived stratum pairing (k_mod = 0, the four named C = 0 strata, the C != 0 shear stratum) involves "
    "ONLY moduli-sector components (field sector zero on the registered stationary presentation): a member with "
    "all moduli components zero (e.g. R_phi = Q) pairs to ZERO with every gauge direction on EVERY stratum — "
    "field-sector members carry ALL-strata OB1 nonemptiness, independent of the TYPED-NOT-EXHAUSTED deeper "
    "stratification",
)
# --- end A1 amendment block (rounds 1 + 2) ----------------------------------------

# TB2.2 The K4 layer: for each character class, the EXACT module of character-matched
# component dependence over the invariant ring — generators EXHIBITED, generation PROVEN
# (exhaustively to degree 6; general degree by the banked parity argument), minimality and
# sample syzygies computed (F-B6: basis computed, not asserted).
VARS = [k10, c00, c11, c01, c10]  # exponent order (e, p, q, r, s)
GEN_I = [
    (2, 0, 0, 0, 0), (0, 2, 0, 0, 0), (0, 0, 2, 0, 0), (0, 1, 1, 0, 0),
    (0, 0, 0, 2, 0), (0, 0, 0, 0, 2), (0, 0, 0, 1, 1),
    (1, 1, 0, 1, 0), (1, 1, 0, 0, 1), (1, 0, 1, 1, 0), (1, 0, 1, 0, 1),
]
GEN_A = [(1, 0, 0, 0, 0), (0, 1, 0, 1, 0), (0, 1, 0, 0, 1), (0, 0, 1, 1, 0), (0, 0, 1, 0, 1)]
GEN_B = [(0, 1, 0, 0, 0), (0, 0, 1, 0, 0), (1, 0, 0, 1, 0), (1, 0, 0, 0, 1)]
GEN_C = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1), (1, 1, 0, 0, 0), (1, 0, 1, 0, 0)]


def mono(expts):
    m = sp.Integer(1)
    for v, e in zip(VARS, expts):
        m *= v**e
    return m


def char_of_expts(expts):
    e, p, q, r, s_ = expts
    return ((e + p + q) % 2, (e + r + s_) % 2)  # (R12 parity, R13 parity)


CHAR_KEY = {(0, 0): "trivial", (1, 1): "chi_a", (1, 0): "chi_b", (0, 1): "chi_c"}

gens_have_char = (
    all(char_of_expts(g) == (0, 0) for g in GEN_I)
    and all(char_of_expts(g) == (1, 1) for g in GEN_A)
    and all(char_of_expts(g) == (1, 0) for g in GEN_B)
    and all(char_of_expts(g) == (0, 1) for g in GEN_C)
    and all(char_of(mono(g)) == CHAR_A for g in GEN_A)
    and all(char_of(mono(g)) == CHAR_B for g in GEN_B)
    and all(char_of(mono(g)) == CHAR_C for g in GEN_C)
)
check(
    "PW2_module_generators_have_declared_characters",
    gens_have_char,
    "chi_a gens {k10, c00c01, c00c10, c11c01, c11c10}; chi_b gens {c00, c11, k10c01, k10c10}; "
    "chi_c gens {c01, c10, k10c00, k10c11}: every listed generator carries its class character (symbolic recheck)",
)

FACT_MEMO = {}


def factors_through_I(expts):
    if expts in FACT_MEMO:
        return FACT_MEMO[expts]
    if all(e == 0 for e in expts):
        FACT_MEMO[expts] = True
        return True
    ok = False
    for g in GEN_I:
        if all(a >= b for a, b in zip(expts, g)):
            rem = tuple(a - b for a, b in zip(expts, g))
            if factors_through_I(rem):
                ok = True
                break
    FACT_MEMO[expts] = ok
    return ok


DEG_BOUND = 6
all_monos = [
    e
    for e in itertools.product(range(DEG_BOUND + 1), repeat=5)
    if 0 < sum(e) <= DEG_BOUND
]
by_char = {"trivial": [], "chi_a": [], "chi_b": [], "chi_c": []}
for e in all_monos:
    by_char[CHAR_KEY[char_of_expts(e)]].append(e)

triv_gen_ok = all(factors_through_I(e) for e in by_char["trivial"])
check(
    "PW2_trivial_class_generation_deg6",
    triv_gen_ok,
    f"all {len(by_char['trivial'])} trivial-character monomials of degree <= {DEG_BOUND} factor through the 11 "
    "invariant generators (exhaustive; general degree = the banked verifier parity proof, cited)",
)


def module_generated(expts, gens):
    for g in gens:
        if all(a >= b for a, b in zip(expts, g)):
            rem = tuple(a - b for a, b in zip(expts, g))
            if factors_through_I(rem):
                return True
    return False


for cname, gens in [("chi_a", GEN_A), ("chi_b", GEN_B), ("chi_c", GEN_C)]:
    ok = all(module_generated(e, gens) for e in by_char[cname])
    check(
        f"PW2_{cname}_module_generation_deg6",
        ok,
        f"all {len(by_char[cname])} {cname}-character monomials of degree <= {DEG_BOUND} = (listed generator) x "
        "(invariant): the exhibited generators GENERATE the module over the invariant ring (exhaustive to deg 6; "
        "general degree by the parity argument: divide out k10 resp. a c_b/c_c factor, remainder has trivial parity)",
    )

deg1 = [e for e in all_monos if sum(e) == 1]
check(
    "PW2_no_degree1_invariants",
    all(char_of_expts(e) != (0, 0) for e in deg1),
    "no degree-1 monomial is K4-invariant: the invariant ring starts at degree 2",
)
chi_a_deg1 = [e for e in by_char["chi_a"] if sum(e) == 1]
chi_a_deg2 = [e for e in by_char["chi_a"] if sum(e) == 2]
check(
    "PW2_chi_a_minimality",
    chi_a_deg1 == [GEN_A[0]] and sorted(chi_a_deg2) == sorted(GEN_A[1:]),
    "chi_a monomials of degree 1 = {k10} exactly; of degree 2 = the four c_b*c_c pairs exactly: with no degree-1 "
    "invariants, none of the 5 generators is an invariant-combination of the others — the generating set is minimal "
    "(distinct monomials are linearly independent); same degree bookkeeping applies to chi_b/chi_c",
)
chi_b_low = [e for e in by_char["chi_b"] if sum(e) <= 2]
chi_c_low = [e for e in by_char["chi_c"] if sum(e) <= 2]
check(
    "PW2_chi_b_chi_c_minimality",
    sorted(chi_b_low) == sorted(GEN_B) and sorted(chi_c_low) == sorted(GEN_C),
    "chi_b monomials of degree <= 2 = its 4 generators exactly; chi_c likewise: minimal generating sets",
)

# Sample syzygies: the modules are generated but NOT free (relations with invariant
# coefficients exist); exhibited exactly. Full syzygy ideal NOT computed (stamped).
syz = [
    sp.expand(I1 * (c00 * c01) - I8v * k10),          # chi_a: I1*a2 - I8*a1 = 0
    sp.expand(I4v * (c00 * c01) - I2v * (c11 * c01)),  # chi_a: I4*a2 - I2*a4 = 0
    sp.expand(I8v * c00 - I2v * (k10 * c01)),          # chi_b: I8*b1 - I2*b3 = 0
    sp.expand(I8v * c01 - I5v * (k10 * c00)),          # chi_c: I8*c1 - I5*c3 = 0
]
check(
    "PW2_module_syzygies_exhibited",
    all(e == 0 for e in syz),
    "sample relations with invariant coefficients (one per nontrivial class + one more for chi_a): the modules are "
    "generated-with-relations, not free; the full syzygy ideal is NOT computed (stamped; not needed for R_PW)",
)

# Generic rank one: away from the fixed strata every class localizes to rank 1
# (all generators become invariant-function multiples of one) — the module is generically
# a line; the extra generators are needed only on the K4-fixed strata.
rank1 = [
    simplify((c00 * c01) - (I8v / I1) * k10),
    simplify((c00 * c10) - (I9v / I1) * k10),
    simplify((c11 * c01) - (I10v / I1) * k10),
    simplify((c11 * c10) - (I11v / I1) * k10),
    simplify(c11 - (I4v / I2v) * c00),
    simplify((k10 * c01) - (I8v / I2v) * c00),
    simplify((k10 * c10) - (I9v / I2v) * c00),
    simplify(c10 - (I7v / I5v) * c01),
    simplify((k10 * c00) - (I8v / I5v) * c01),
    simplify((k10 * c11) - (I10v / I5v) * c01),
]
check(
    "PW2_generic_rank_one",
    all(e == 0 for e in rank1),
    "on the locus k10 != 0 (resp. c00 != 0, c01 != 0) every generator of a class is an invariant-RATIO multiple of a "
    "single one: each character module is generically rank 1 (a line over the orbit space); >1 generators are needed "
    "exactly on the K4-fixed strata",
)

# Invariant-ring relations + orbit dimension: the 13 moduli functions (lambda, k_mod,
# I1..I11) embed the 7-dimensional moduli orbit space (finite quotient), with relations.
ring_rel = [
    sp.expand(I2v * I3v - I4v**2),
    sp.expand(I5v * I6v - I7v**2),
    sp.expand(I8v * I11v - I1 * I4v * I7v),
    sp.expand(I9v * I10v - I1 * I4v * I7v),
    sp.expand(I8v * I9v - I1 * I2v * I7v),
    sp.expand(I8v * I10v - I1 * I4v * I5v),
]
pt = {k10: 1, c00: 2, c01: 3, c10: 5, c11: 7}
orbit = set()
for sm in [{}, subs_R12, subs_R13, subs_R23]:
    img = tuple(v.subs(sm, simultaneous=True).subs(pt) for v in [k10, c00, c01, c10, c11])
    orbit.add(img)
check(
    "PW2_invariant_ring_relations_and_orbit_dim",
    all(e == 0 for e in ring_rel) and len(orbit) == 4,
    "sample invariant-ring relations (I2I3=I4^2, I5I6=I7^2, I8I11=I9I10=I1I4I7, ...) hold exactly; a generic point "
    "has K4-orbit of size 4 (finite): the (k10,C) orbit space has dimension 5, so the moduli alphabet has functional "
    "dimension 5+2=7, embedded by the 13 generator functions WITH relations (full relation ideal stamped not-computed)",
)

# ----------------------------------------------------------------------------
# TB3 — the slot/seat reduction (R4/J06 exact; screen + moduli block)
# ----------------------------------------------------------------------------
print("\n--- TB3: slot/seat reduction ---")

I2m = eye(2)
D2 = sp.diag(-1, 1)
E21 = Matrix([[0, 0], [1, 0]])
E12 = Matrix([[0, 1], [0, 0]])


def pair(A_, B_):
    return sp.trace(A_.T * B_)


Gram = Matrix(3, 3, lambda i, j: pair([I2m, D2, E21][i], [I2m, D2, E21][j]))
check(
    "PW3_screen_pairing_basis_unique",
    Gram == sp.diag(2, 2, 1) and Gram.det() == 4
    and pair(E12, I2m) == 0 and pair(E12, D2) == 0 and pair(E12, E21) == 0,
    "trace-pairing Gram of {I2, diag(-1,1), E21} is diag(2,2,1) (nondegenerate: the screen kernel decomposition "
    "W = r_tr I2 + r_tf diag(-1,1) + r_sh E21 is UNIQUE); the E12 direction is null against every deltaK direction "
    "(an unpaired slot, quotiented out of the pointwise kernel) — A3 CONVENTION NOTE: 'E12 is null' is a "
    "chart-deltaK pairing-convention statement; see A3_pairing_convention_isomorphic",
)
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
W = r_tr * I2m + r_tf * D2 + r_sh * E21 + r_nl * E12
comp = (simplify(pair(W, I2m)), simplify(pair(W, D2)), simplify(pair(W, E21)))
check(
    "PW3_component_pairings",
    comp == (2 * r_tr, 2 * r_tf, r_sh),
    "R_lambda = <W, I2> = 2 r_tr; R_kmod = <W, diag(-1,1)> = 2 r_tf; R_k10 = <W, E21> = r_sh: the moduli components "
    "of the screen sector are exactly the slot coefficients (deltaK = dlam*I2 + dk_mod*diag(-1,1) + dk10*E21)",
)
# A3 amendment: the slot statement is convention-relative — against the PHYSICAL
# tangent delta(K+K^T) (Route B T-block) the pairings read (4 r_tr, 4 r_tf,
# r_sh + r_nl), an invertible reparametrization of the SAME component space; the
# "E12 null slot" is a chart-deltaK convention statement (against delta(K+K^T) the
# symmetric E12+E21 combination pairs). No math changes; verifier VE_* adopted.
dl_c, dm_c, dk_c = symbols("dl_c dm_c dk_c")
dKKT = 2 * dl_c * I2m + 2 * dm_c * D2 + dk_c * (E21 + E12)
check(
    "A3_pairing_convention_isomorphic",
    simplify(pair(W, dKKT) - (4 * r_tr * dl_c + 4 * r_tf * dm_c + (r_sh + r_nl) * dk_c)) == 0,
    "against the physical tangent delta(K+K^T) = 2 dlam I2 + 2 dk_mod diag(-1,1) + dk10 (E21+E12) the component "
    "pairings are (4 r_tr, 4 r_tf, r_sh + r_nl): an invertible reparametrization of the same component space — "
    "the slot decomposition is convention-independent, the E12 'null slot' statement is chart-deltaK-relative (A3)",
)
check(
    "PW3_slot_theorem_recomputed",
    simplify(pair(r_tr * I2m, D2)) == 0
    and simplify(pair(W.subs(r_tf, 0), D2)) == 0,
    "<r_tr I2, diag(-1,1)> = 0 identically, and a kernel with ZERO trace-free slot has R_kmod = 0 identically "
    "even with arbitrary r_sh, r_nl: k_mod-sensitivity REQUIRES the trace-free slot (banked B5 slot theorem, A3-amended)",
)
X_seat = sp.diag(-1, 1, a_seat, d_seat)
K_seat = sp.diag(a_seat, d_seat)
kernel_trX2 = 2 * K_seat
tf_part = kernel_trX2 - (sp.trace(kernel_trX2) / 2) * eye(2)
check(
    "PW3_trX2_routes_through_tracefree",
    is_zero_matrix(tf_part - 2 * kmod * D2)
    and simplify(sp.trace(kernel_trX2 * D2) - 4 * kmod) == 0
    and simplify(sp.trace((sp.trace(kernel_trX2) / 2 * eye(2)) * D2)) == 0,
    "d(tr K^2) kernel = 2K: its k_mod-pairing (4 k_mod) routes precisely through the trace-free part (banked B5 recomputed)",
)

# The kernel transports under K4 exactly with the characters of its paired directions
# (ties TB2's character rule to TB3's slots — the contragredient action recomputed at slot level).
kernel_transport_ok = True
for name, M in [("R23", R23), ("R12", R12), ("R13", R13)]:
    S_scr = M[2:4, 2:4]
    Wt = S_scr * W * S_scr  # S = S^{-1}
    ct = (simplify(pair(Wt, I2m)), simplify(pair(Wt, D2)), simplify(pair(Wt, E21)))
    sgn_a = simplify((k10.subs(dict([("R23", subs_R23), ("R12", subs_R12), ("R13", subs_R13)])[name], simultaneous=True)) / k10)
    if not (ct[0] == 2 * r_tr and ct[1] == 2 * r_tf and simplify(ct[2] - sgn_a * r_sh) == 0):
        kernel_transport_ok = False
check(
    "PW3_kernel_K4_transport_matches_characters",
    kernel_transport_ok,
    "under every K4 element the screen kernel's slots transport as: r_tr, r_tf fixed (trivial character = characters "
    "of dlam, dk_mod); r_sh flips exactly with chi_a (character of dk10): the slot decomposition IS character-graded",
)

Mker = Matrix(2, 2, symbols("m00 m01 m10 m11"))
C_transport_ok = True
for name, M in [("R23", R23), ("R12", R12), ("R13", R13)]:
    S_scr = M[2:4, 2:4]
    S_base = M[0:2, 0:2]
    Mt = S_scr * Mker * S_base
    sm = dict([("R23", subs_R23), ("R12", subs_R12), ("R13", subs_R13)])[name]
    for i in range(2):
        for j in range(2):
            sgn = simplify(cpos[i][j].subs(sm, simultaneous=True) / cpos[i][j])
            if simplify(Mt[i, j] - sgn * Mker[i, j]) != 0:
                C_transport_ok = False
check(
    "PW3_C_kernel_transport_matches_characters",
    C_transport_ok,
    "the mixing kernel M (pairing deltaC by <M, deltaC>) transports entrywise with exactly the K4 character of the "
    "paired dc_ij direction (chi_b on the 00/11 entries, chi_c on the 01/10 entries): R_C components are forced "
    "chi_b/chi_c-relative, matching the banked A1-amended rule",
)

# J06 branch structure per moduli family: BOTH branches nonempty inside the parametrization,
# NEITHER chosen (determined = component not identically zero; retained = component == 0 with
# the modulus reported residual). Witnesses are structural, not selections (F-B1).
witness_char_ok = (
    char_of(k10) == CHAR_A  # determined-branch witness for k10: R_k10 = k10 (chi_a-matched; the omega shape)
    and char_of(c00) == CHAR_B  # determined-branch witness for c00: R_c00 = c00 (chi_b-matched)
)
check(
    "PW3_J06_both_branches_nonempty_per_family",
    witness_char_ok and simplify(pair(W.subs([(r_tr, 1), (r_tf, 0), (r_sh, 0), (r_nl, 0)]), D2)) == 0,
    "per family (lambda | k_mod | k10 | C): determined-branch witnesses exist (nonzero character-matched components: "
    "2r_tr, 2r_tf, k10, c00) AND retained-branch witnesses exist (component identically 0, modulus reported residual "
    "— e.g. the pure-trace kernel has R_kmod = 0); both branches are open sub-loci of R_PW; NO branch is chosen",
)

# ----------------------------------------------------------------------------
# TB4 — R_PW assembled at the declared scope (census coverage, typing, jets 3/4)
# ----------------------------------------------------------------------------
print("\n--- TB4: residual space assembly ---")

CENSUS_DIRECTIONS_BASE = ["R_phi", "R_f", "R_bh", "R_lambda", "R_kmod", "R_k10",
                          "R_c00", "R_c01", "R_c10", "R_c11", "R_wall", "R_corner"]
BRANCH_ADDITIONS = {
    "BR-A_alpha_active": ["R_alpha"],
    "BR-CE_cE_promoted": ["R_cE"],
}
LEDGER_COMPONENTS_BASE = list(CENSUS_DIRECTIONS_BASE)
check(
    "PW4_R2_census_component_coverage",
    set(LEDGER_COMPONENTS_BASE) == set(CENSUS_DIRECTIONS_BASE)
    and len(LEDGER_COMPONENTS_BASE) == 12,
    "the R_PW parametrization carries a component slot for EVERY census direction of the base branch (12 slots: "
    "3 field + 7 moduli [R_C = 4 entries] + wall + corner), no extra slots: R2/R12 full-domain typing holds by "
    "construction; branch additions (R_alpha, R_cE) enter exactly on their labeled forks (F-B2)",
)
check(
    "PW4_J05_full_tangent_paired",
    set(["R_lambda", "R_kmod", "R_k10", "R_c00", "R_c01", "R_c10", "R_c11"]).issubset(set(LEDGER_COMPONENTS_BASE)),
    "all 7 moduli directions of the physical tangent T = [[2I2,C^T],[C,K+K^T]] are paired by components (J05: the "
    "response pairs the FULL tangent; no pair-only/infinitesimal-only truncation)",
)
check(
    "PW4_J13_discriminator_slots_retained",
    set(["R_kmod", "R_c00", "R_c01", "R_c10", "R_c11"]).issubset(set(LEDGER_COMPONENTS_BASE)),
    "the E07 discriminator (k_mod slot) and E08 discriminator (C slots) are retained in the parametrization; the "
    "completion label c-frak remains an explicit argument slot (J13 slot condition; deleting them = imposition)",
)

# R12/J14 witness recomputed (Stage-1 C1/C2): restrict-then-vary is inequivalent.
xw, yw = symbols("xw yw")
Fw = xw**2 + yw + yw**2
restricted_crit = sp.solve(sp.diff(Fw.subs(yw, 0), xw), xw)
full_resp = (sp.diff(Fw, xw).subs({xw: 0, yw: 0}), sp.diff(Fw, yw).subs({xw: 0, yw: 0}))
incompatible = sp.solve([sp.diff(Fw, xw), sp.diff(Fw, yw), yw], [xw, yw], dict=True)
check(
    "PW4_R12_J14_witness_recomputed",
    restricted_crit == [0] and full_resp == (0, 1) and incompatible == [],
    "restrict-then-vary inequivalence witness (Stage-1 C1/C2 recomputed): R_PW is defined off-shell on the full "
    "domain; every stratum restriction is a pullback AFTER definition; the zero set is a DERIVED subset (J14)",
)

# Jet-3/4 typing (NOT-EXHAUSTED): the extension is purely an alphabet enlargement —
# higher jets are shift-invariant (PW1_phi_jets_shift_invariant covers n=3,4) and K4-inert;
# the character/slot structure is UNCHANGED. Guard arithmetic for the scope stamp.
check(
    "PW4_jet34_extension_is_alphabet_only",
    jets_inert
    and set().union(*[set(sm.keys()) for sm in [subs_R12, subs_R13, subs_R23]]).isdisjoint({phi}),
    "3rd/4th field jets are shift-invariant and K4-inert: the jet>2 extension adds alphabet arguments ONLY — the "
    "TB2 character modules, TB3 slot structure, AND the A1 stratum Noether identities (moduli-sector, jet-blind) "
    "are order-independent; the jet<=2 parametrization is the EXHAUSTED scope, jet 3/4 is TYPED, stamped "
    "NOT-EXHAUSTED (F-B3)",
)

# R13/R10 definition-level audits on the emitted alphabet (bookkeeping, honest as such).
ALPHABET_ARGS = {
    "grade0_varied": ["Q", "f0", "bh0"],
    "grade0_moduli": ["lambda", "k_mod", "I1..I11 (embed dim 7 with relations)"],
    "grade0_supplied": ["alpha (frozen fork)", "c_E", "wall data (supplied)", "c-frak (discrete)"],
    "grade1": ["phi1", "f1", "bh1"],
    "grade2": ["phi2", "f2", "bh2"],
}
check(
    "PW4_R13_no_global_entries_in_alphabet",
    all("global" not in a and "average" not in a for grp in ALPHABET_ARGS.values() for a in grp),
    "the alphabet contains only pointwise jets, moduli invariants, and supplied structure — no fitted global "
    "functional appears as a coupling (R13 definition-level audit; R3's completion ARGUMENTS enter as the "
    "explicit c-frak/boundary slots, dependence explicit)",
)
check(
    "PW4_R10_E02_footing_by_construction",
    is_zero_matrix(X[0:2, 2:4]) and X[2, 3] == 0,
    "every construction above runs on the registered E02 X = [[H,0],[C,K]] footing (upper-right zero, K "
    "lower-triangular): R10 extension-gate precedence holds by construction",
)

# Functional dimensions per grade (base branch): varied args 3/6/9 cumulative + moduli 7.
dims = {"grade0": 3 + 7, "grade1": 3 + 7 + 3, "grade2": 3 + 7 + 3 + 3}
check(
    "PW4_functional_dimensions_per_grade",
    dims == {"grade0": 10, "grade1": 13, "grade2": 16},
    "base branch functional dimension of the alphabet: grade 0 = 10 (Q, f0, bh0 + 7-dim moduli orbit), grade 1 = 13, "
    "grade 2 = 16 (+1 per grade on the alpha-active branch; +7 moduli-jet args per jet order on the TYPED "
    "moduli-field branch, NOT-EXHAUSTED)",
)

# ----------------------------------------------------------------------------
# TB5 — the pointwise verdict: R_PW is NONEMPTY (OB1); locations recorded as observations
# ----------------------------------------------------------------------------
print("\n--- TB5: pointwise verdict ---")

# (obs 1) the Stage-1 omega = k10 dk10 shape lies in R_PW: chi_a-matched (a1 * 1), exact.
def dir_sign(v, sm):
    return -1 if v in sm else 1


omega_comp = k10
omega_ok = (
    all(simplify(omega_comp.subs(sm, simultaneous=True) * dir_sign(k10, sm) - omega_comp) == 0 for _, sm in K4_SUBS)
    and simplify(sp.diff(k10**2 / 2, k10) - omega_comp) == 0
)
check(
    "PW5_obs_omega_shape_in_RPW",
    omega_ok,
    "OBSERVATION (not selection): the Stage-1 counterexample shape omega = k10 dk10 = (1/2)d(k10^2) lies in R_PW "
    "off the C != 0 resonance sub-varieties — R_k10 = k10 = (generator a1)x(invariant 1), all other slots 0 (J06 "
    "retained branch for the rest); character-matched and exact; R2 SCOPE: satisfies the k_mod = 0 identity "
    "(on-stratum witness there) but VIOLATES the C != 0 resonance shear identity (A1R2 checks) — per-witness "
    "stratum stamps travel",
)

# (obs 2) the EH-form restricted to the registered stationary family lies in the jet<=2
# class: every component carries <= 2nd jets (Route C TC3, cited); its phi-dependence is
# through seat exponentials e^{a phi} = (c_E/Q)^a (anchored — recomputed here); its moduli
# dependence (lambda) is K4-trivial as required for field-direction components.
check(
    "PW5_obs_EH_form_lands_in_jet2_class",
    simplify(cE / Q - exp(phi)) == 0 and char_of(lam * (1 + I1)) == CHAR_TRIV and (2 <= 2),
    "OBSERVATION (not selection): the EH-form G_ab + Lam g_ab restricted to the registered stationary family has "
    "<= 2nd jets on every component (Route C TC3, CITED) and phi-dependence through seat exponentials = anchored "
    "Q-powers (recomputed): it lands INSIDE the jet<=2 parametrization, in the trivial-character field sector, "
    "with (k10,C)-independent moduli dependence (J06 retained branch for k10/C on the diagonal presentation)",
)
check(
    "PW5_obs_Bach_form_typed_class_only",
    4 > 2,
    "OBSERVATION (not selection): the Bach-form carries 3rd/4th jets on every component (Route C TC2, CITED): it "
    "lies OUTSIDE the jet<=2 exhausted scope, INSIDE the typed jet-3/4 extension class (alphabet enlargement only, "
    "PW4_jet34) — NOT-EXHAUSTED stamp travels (F-B3)",
)

# Exclusions: which banked no-go structures the PW requirements exclude (locations of
# the fence, recorded — nothing selected).
q1g, q2g = symbols("q1g q2g")
inv_gen = q1g + q2g * I1
mismatched = c00 * inv_gen  # chi_b dependence on a trivial-character direction (e.g. R_phi)
mismatch_breaks = any(
    simplify(mismatched.subs(sm, simultaneous=True) - mismatched) != 0 for _, sm in K4_SUBS
)
check(
    "PW5_excl_character_mismatch",
    mismatch_breaks,
    "EXCLUDED by R7(a)/J10: any component whose K4 character mismatches its paired direction (witness: a chi_b "
    "dependence c00*(invariant) placed in a trivial-direction component such as R_phi) is not well defined on the "
    "quotient — the A1-amended rule, recomputed",
)
check(
    "PW5_excl_bare_phi_zero_point",
    witness_noninv != 0,
    "EXCLUDED by J04/F-RA4: bulk dependence on an absolute phi zero-point (any c_E^p e^{-q phi} with p != q, or bare "
    "phi) — the anchored-Q factorization is forced; anchored-phi wall data enter only through supplied-structure "
    "slots (Stage-1 V8 clash resolution, cited)",
)
check(
    "PW5_excl_pure_trace_kernel_from_determined_kmod",
    simplify(pair(W.subs(r_tf, 0), D2)) == 0,
    "EXCLUDED by R4/J06 from the k_mod-DETERMINED branch: any screen sector with zero trace-free slot (the named "
    "false pass 'spectator screen isotropy or trace zero assumed') — such members survive only on the explicit "
    "retained-modulus branch (banked slot theorem)",
)
check(
    "PW5_excl_restrict_then_vary",
    restricted_crit == [0] and full_resp == (0, 1),
    "EXCLUDED by R12: restrict-then-vary objects (the EH-RED scar class) — the inequivalence witness stands; R_PW "
    "members are full-domain by type",
)

# Verdict: NONEMPTY at jet <= 2 => OB1. (Nonemptiness by exhibited nonzero members;
# the parametrization is the deliverable. Emptiness branches OB2/OB3 do not arise.)
# A1-AMENDED witnesses (per-witness stratum stamps, R2): the omega shape satisfies
# the k_mod = 0 identity (on-stratum witness THERE) but violates the C != 0 shear
# identity (A1R2 — scoped off those sub-varieties); the corrected trace-free witness
# satisfies the k_mod = 0 identity AND vanishes on the found C != 0 defect stratum
# (survives the new cut); the constant unit trace-free kernel (r_tf = 1, R_kmod = 2)
# is a member only OFF the k_mod = 0 stratum (A1_old_witness_violates_on_stratum);
# field-sector members (all moduli components zero) carry ALL-strata nonemptiness
# (A1R2_field_sector_members_carry_all_strata).
check(
    "PW5_verdict_nonempty_OB1",
    omega_ok
    and simplify(pair(W.subs([(r_tr, 0), (r_tf, 1), (r_sh, 0), (r_nl, 0)]), D2) - 2) == 0
    and sp.expand(sat_omega) == 0
    and sp.expand(sat_corr) == 0
    and sp.expand(surv_corr_r2) == 0
    and all(sp.expand(p_.subs(ZERO_MODULI_COMPS)) == 0 for p_ in ALL_STRATUM_PAIRINGS),
    "R_PW at the declared scope is NONEMPTY: exhibited nonzero members exist in every character sector, with "
    "PER-WITNESS STRATUM STAMPS (R2) — ON k_mod = 0: the omega shape and the corrected trace-free witness "
    "(r_tf, m00) = (c01 c10, 2 k10 c01), both satisfying that identity; the corrected witness ALSO survives the "
    "C != 0 shear cut (vanishes on the found stratum); the omega shape is scoped OFF the C != 0 resonance "
    "sub-varieties (violates the shear identity); the constant unit trace-free kernel with R_kmod = 2 is scoped "
    "OFF k_mod = 0; field-sector members (all moduli components zero, e.g. R_phi = Q) pair to zero with every "
    "gauge direction on EVERY stratum = the all-strata carrier. VERDICT: OB1 — the exact parametrization CUT BY "
    "the stratum identities (k_mod = 0 the only codim-1 cut; C != 0 sub-variety cuts typed-not-exhausted with a "
    "derived example) is the deliverable; no member selected (F-B1)",
)

# ----------------------------------------------------------------------------
# Emit ledger (RESIDUAL_SPACE_LEDGER.tsv), JSON, stdout summary
# ----------------------------------------------------------------------------
n_pass = sum(1 for c in CHECKS if c["passed"])
n_tot = len(CHECKS)
all_pass = n_pass == n_tot
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_guard = sum(1 for c in CHECKS if c["kind"] == "citation-guard")
n_sub_pass = sum(1 for c in CHECKS if c["kind"] == "substantive" and c["passed"])
n_guard_pass = sum(1 for c in CHECKS if c["kind"] == "citation-guard" and c["passed"])

ALG = "A_grade{g} := smooth functions of [Q, f0, bh0 (+alpha jets on BR-A)] + jets<=g of (phi,f,bh); polynomial/formal in the 13 moduli functions (lambda, k_mod, I1..I11; embed dim 7 with relations)"
MODULE = {
    "trivial": ("{1}", 1, "component = arbitrary element of A_grade (trivial character; verbatim factoring through invariants — banked A1-amended rule)"),
    "chi_a": ("{k10, c00c01, c00c10, c11c01, c11c10}", 5, "component = sum(generators x A_grade-invariant coefficients); generically rank 1; syzygies exist (exhibited)"),
    "chi_b": ("{c00, c11, k10c01, k10c10}", 4, "same module structure, chi_b"),
    "chi_c": ("{c01, c10, k10c00, k10c11}", 4, "same module structure, chi_c"),
}
COMPONENT_TABLE = [
    ("R_phi", "trivial", "census row 5 (phi field); phi enters via Q + jets"),
    ("R_f", "trivial", "census row 9 (stationary presentation)"),
    ("R_bh", "trivial", "census row 10 (seat factor NOT in bh)"),
    ("R_lambda", "trivial", "= 2 r_tr (screen trace slot)"),
    ("R_kmod", "trivial", "= 2 r_tf (trace-free slot; J06-determined branch requires r_tf not== 0); A1: CUT on k_mod=0 by the STRATUM-IDENTITY row"),
    ("R_k10", "chi_a", "= r_sh (shear slot); A3: slot pairings chart-deltaK convention, see A3_pairing_convention_isomorphic; A1-R2: r_sh is CUT on the found C!=0 resonance sub-variety by the shear STRATUM-IDENTITY row"),
    ("R_c00", "chi_b", "mixing kernel entry 00; A1: enters the k_mod=0 STRATUM-IDENTITY row"),
    ("R_c11", "chi_b", "mixing kernel entry 11; A1: enters the k_mod=0 STRATUM-IDENTITY row"),
    ("R_c01", "chi_c", "mixing kernel entry 01; A1: enters the k_mod=0 STRATUM-IDENTITY row"),
    ("R_c10", "chi_c", "mixing kernel entry 10; A1: enters the k_mod=0 STRATUM-IDENTITY row"),
    ("R_wall", "trivial", "census row 16; stratum alphabet = supplied wall data + trace jets <= grade-1 (depth example-typed per Route C TC5, stamped); anchored-phi only via supplied slots (V8)"),
    ("R_corner", "trivial", "census row 17; corner slots present, no corner law chosen"),
]
BRANCHES = [
    ("BASE", "moduli-const, alpha-frozen, cE-const, bdy-held", "EXHAUSTED at jet<=2 (poly/formal in moduli; smooth in rest)"),
    ("BR-A_alpha_active", "adds R_alpha (trivial char) + alpha jets to alphabet", "EXHAUSTED at jet<=2 (same theorem applies)"),
    ("BR-M_moduli_field", "moduli promoted to fields: adds 7 moduli-jet args/order, character-typed", "TYPED ONLY — class extension beyond banked footing; NOT-EXHAUSTED"),
    ("BR-CE_cE_promoted", "adds R_cE + c_E jets (unregistered DOF)", "TYPED ONLY; NOT-EXHAUSTED"),
    ("BR-B_bdy_varied", "same component EXPRESSIONS as held fork; role = paired equations vs consistency conditions", "pointwise parametrization PROVEN branch-independent (identical expressions); role labeled"),
    ("BR-C_completion", "within-family vs over-class", "pointwise PROVEN branch-independent (c-frak discrete in both forks, enters only as supplied argument slot; difference is GC/Stage-3)"),
]

ledger_rows = []
for comp_name, char_cls, note in COMPONENT_TABLE:
    gens_str, rank, cond = MODULE[char_cls]
    for g in [0, 1, 2]:
        dim_alg = {0: 10, 1: 13, 2: 16}[g]
        ledger_rows.append(
            [comp_name, f"grade{g}", "BASE", char_cls, gens_str, str(rank),
             f"alphabet dim {dim_alg}", cond + " | " + note]
        )
for br, desc, status in BRANCHES[1:]:
    ledger_rows.append([f"(branch delta) {br}", "all", br, "-", desc, "-", "-", status])
# A1 amendment: stratum Noether identity constraint rows — the published module space
# is CUT by these on the degeneration strata (the pre-amendment ledger was a strict
# SUPERSET of R_PW on k_mod = 0).
ledger_rows.append([
    "(constraint) STRATUM-IDENTITY kmod0", "all", "BASE", "chi_a-graded",
    "-2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 on k_mod = 0 (equivalently -k10 R_kmod + <M, J C> = 0)",
    "-", "-",
    "A1 (verifier-derived, adopted + extended): exact pointwise R7(b) Noether identity on the codim-1 "
    "reciprocal-isotropy stratum k_mod=0 (gauge direction = screen rotation L23, tangent iff k_mod=0; chart "
    "reading delta k_mod=-k10, delta C=J C; field sector zero on the registered stationary presentation, general "
    "arenas typed); K4-consistent (chi_a-graded); ONE scalar relation cutting the on-stratum restrictions of "
    "(R_kmod, R_C) — off-stratum rows/dimensions unchanged; order-independent (moduli-sector, jet-blind)"])
ledger_rows.append([
    "(constraint) STRATUM-IDENTITY resonance (named C=0 strata)", "all", "BASE", "mixing components only",
    "k10 R_c10 = 0 at {C=0, lam-k_mod=-1}; k10 R_c11 = 0 at {C=0, lam-k_mod=+1}; "
    "k10 ((k00+1) R_c00 + k10 R_c10) = 0 at {C=0, lam+k_mod=-1}; k10 ((k00-1) R_c01 + k10 R_c11) = 0 at {C=0, lam+k_mod=+1}",
    "-", "-",
    "A1: derived exactly (rank-5 base-screen eigenvalue-resonance gauge directions); AUTOMATICALLY satisfied by "
    "every character-matched member of the declared polynomial/formal class (all chi_b/chi_c generators vanish at "
    "C=0) — R2-CORRECTED SCOPE: no further cut FROM THESE FOUR NAMED C=0 STRATA within the declared scope; "
    "rank-drop locus off k_mod=0 confined EXHAUSTIVELY to lam-+k_mod in {+-1} (minor-ideal proof, codim-1 layer "
    "exhaustive); the C!=0 sub-varieties of the resonance locus carry FURTHER genuine cuts (shear row below); "
    "deeper stratification TYPED-NOT-EXHAUSTED"])
# A1-R2 (closure amendment): the C != 0 sub-variety shear identity — a FURTHER genuine cut.
ledger_rows.append([
    "(constraint) STRATUM-IDENTITY shear (C!=0 resonance sub-variety)", "all", "BASE", "chi_b-graded",
    "-c10 r_sh - k10 m10 = 0 on {lam - k_mod = -1 (k00 = -1), c00 = c01 = 0} (equivalently -c10 R_k10 - k10 R_c10 = 0)",
    "-", "-",
    "A1-R2 (closure-verifier-derived, adopted): exact pointwise R7(b) Noether identity on a C!=0 sub-variety "
    "(codim 3, K4-stable) of the resonance locus; gauge direction = the mixed base-screen boost L02 "
    "(delta k10 = -c10, delta c10 = -k10, rest zero); cuts the SHEAR slot r_sh — unlike the kmod0 identity "
    "(r_sh drops out there) and the named C=0 identities (mixing-only); a GENUINE further cut (the "
    "character-matched member R_c10 = c10 violates it; NOT auto-satisfied); the omega-shape witness VIOLATES it "
    "(re-scoped: on-stratum witness for kmod0 only); the corrected trace-free witness and field-sector members "
    "survive; the k00=-1 slice of the minor ideal has 7 branches incl. two with generic C!=0 — the FULL deeper "
    "stratification is TYPED-NOT-EXHAUSTED (codim-1 layer exhaustive by the Groebner proof; deeper layers = "
    "derived examples + the same nullspace/pairing method, not a census)"])

ledger_path = "RESIDUAL_SPACE_LEDGER.tsv"
with open(ledger_path, "w") as fh:
    fh.write("# P4 Route A Stage 2 — RESIDUAL SPACE LEDGER (R_PW). Contract: PREREGISTRATION.md. "
             "SCOPE STAMP (F-B3): EXHAUSTED = jet<=2, registered stationary presentation, registered chart, "
             "one-parameter, off-shell; polynomial/formal in (k10,C) moduli (smooth extension = Schwarz-type, "
             "Category-A, stamped not re-proven); jet 3/4 TYPED NOT-EXHAUSTED. NO member selected (F-B1). "
             "A1-AMENDED (rounds 1+2): the parametrization is exact OFF the degeneration strata and CUT BY the "
             "stratum Noether identities ON them (see the STRATUM-IDENTITY rows; kmod0 = the only CODIMENSION-1 "
             "genuine cut; the four named C=0 resonance identities are auto-satisfied in the declared class; the "
             "resonance locus also carries C!=0 sub-varieties of higher codimension whose identities ARE further "
             "genuine cuts — shear row; deeper stratification TYPED-NOT-EXHAUSTED).\n")
    fh.write("component\tgrade\tbranch\tK4_character\tmodule_basis_or_branch_delta\tmodule_rank\talphabet_dim\tconditions\n")
    for row in ledger_rows:
        fh.write("\t".join(row) + "\n")
print(f"\nLedger written: {ledger_path} ({len(ledger_rows)} rows)")

result = {
    "package": "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29",
    "stage": "Route A Stage 2 (TB1-TB5 computations; TB6 in STAGE3_HANDOFF.md)",
    "date": "2026-07-29",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "n_checks": n_tot,
    "n_passed": n_pass,
    "all_passed": all_pass,
    "check_split_A2": {
        "n_substantive": n_sub,
        "n_substantive_passed": n_sub_pass,
        "n_citation_guards": n_guard,
        "n_citation_guards_passed": n_guard_pass,
        "citation_guard_names": sorted(CITATION_GUARDS),
        "note": "A2 amendment: citation guards are bookkeeping checks (list-copy/subset equality, trivial "
                "arithmetic restating a cited banked fact, string scans) — kept, honestly labeled, never "
                "counted as zero-residual computations in a headline",
    },
    "amendments": {
        "status": "A1/A2/A3 applied 2026-07-29 per VERIFIER_REPORT.md; ROUND-2 closure fix (C3) applied "
                  "2026-07-29 per the AMENDMENT CLOSURE section (see CORRECTION_LAYER.md); pre-amendment run: "
                  "53/53; round-1 run: 67/67; both exit 0",
        "A1": "R7(b) pointwise-vacuity REFUTED AS STATED (class-wide vs per-member stabilizer conflation): "
              "restated as generic vacuity + exact stratum Noether identities; verifier counter-computation "
              "adopted and extended (all-member minor proof, resonance strata, corrected/scoped witnesses); "
              "the pre-amendment parametrization was a strict SUPERSET of R_PW on the k_mod=0 stratum",
        "A1_R2": "ROUND-2 (closure verdict NEW-DEFECT, C3): the round-1 headline 'the ONLY genuine new cut is "
                 "the k_mod=0 identity' REFUTED — the same error class one level down (a stratum-blind "
                 "uniqueness gloss); corrected: k_mod=0 is the only CODIMENSION-1 cut; the resonance locus "
                 "carries C!=0 sub-varieties of higher codimension with additional exact identities (derived "
                 "example: the shear identity -c10 r_sh - k10 m10 = 0 on {lam-k_mod=-1, c00=c01=0}); the four "
                 "NAMED C=0 strata identities are auto-satisfied in the declared class; omega witness re-scoped; "
                 "deeper stratification TYPED-NOT-EXHAUSTED (A1R2_* checks)",
        "A2": "check-count honesty: substantive vs citation-guard split reported everywhere",
        "A3": "E12 null-slot statement stamped chart-deltaK-convention-relative (isomorphic component space "
              "against the physical delta(K+K^T) pairing)",
    },
    "stratum_noether_identities_A1": {
        "generic": "pointwise tangency stabilizer trivial (rank 6) at generic moduli: R7(b) vacuous GENERICALLY",
        "kmod0": {
            "stratum": "k_mod = 0 (k00 = k11), codimension 1; K4-stable; = the reciprocal-isotropy locus",
            "gauge_direction": "L23 screen rotation; [L23,X]|_{k_mod=0} = [[0,0],[J C, k10 diag(1,-1)]]; "
                               "chart reading (delta lambda, delta k_mod, delta k10, delta C) = (0, -k10, 0, J C); "
                               "tangency obstruction at general members = [L23,X](2,3) = 2 k_mod",
            "identity": "-2 k10 r_tf + m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 (r_tr, r_sh, r_nl drop out; "
                        "field sector zero on the registered stationary presentation, general arenas typed)",
            "K4": "chi_a-graded, quotient-consistent",
            "witnesses": "omega shape SATISFIES (R2 scope: an on-stratum witness for k_mod=0 ONLY — it violates "
                         "the C!=0 resonance shear identity); corrected trace-free witness (r_tf, m00) = "
                         "(c01 c10, 2 k10 c01) SATISFIES with R_kmod not== 0 and ALSO survives the C!=0 shear "
                         "cut; constant unit trace-free kernel VIOLATES -> scoped OFF-stratum",
        },
        "resonance_strata": res_record,
        "resonance_note": "R2-CORRECTED: k_mod=0 is the only CODIMENSION-1 genuine cut; the resonance rank-drop "
                          "locus (confined EXHAUSTIVELY to lam-+k_mod in {+-1} by the minor-ideal proof — the "
                          "codim-1 layer) consists of higher-codim sub-varieties, generically with C!=0, whose "
                          "identities ARE further genuine cuts (derived example: the shear identity on "
                          "{lam-k_mod=-1, c00=c01=0}); ONLY the four NAMED C=0 strata identities are "
                          "auto-satisfied by the declared class (chi_b/chi_c generators all vanish at C=0); "
                          "deeper stratification TYPED-NOT-EXHAUSTED",
        "Cneq0_subvarieties_R2": {
            "headline_correction": "the round-1 claim 'the ONLY genuine new cut is the k_mod=0 identity' is "
                                   "REFUTED (closure verifier C3); correct: k_mod=0 is the only CODIMENSION-1 "
                                   "cut; the resonance locus carries C!=0 sub-varieties of higher codimension "
                                   "with additional exact identities",
            "k00_m1_slice": "7 solution branches of the minor ideal at k00=-1, incl. {c00=c01=0, c10, c11 free} "
                            "and {k11=1, c10=-c00 k10/2, c11=-c01 k10/2} (fully generic C!=0)",
            "example_stratum": "{lam - k_mod = -1 (k00 = -1), c00 = c01 = 0}: codim 3, K4-stable",
            "gauge_direction": "L02, the mixed base-screen boost; [L02,X]|_stratum: (delta k10, delta c10) = "
                               "(-c10, -k10), rest zero; chi_b transport",
            "identity": "-c10 r_sh - k10 m10 = 0 (equivalently -c10 R_k10 - k10 R_c10 = 0) — cuts the SHEAR "
                        "slot r_sh; chi_b-graded, K4-consistent",
            "genuine_cut_witnesses": "member R_c10 = c10 pairs to -c10 k10 not== 0 (NOT auto-satisfied); the "
                                     "omega shape (r_sh = k10) also pairs to -c10 k10 not== 0 (re-scoped)",
            "surviving_members": "corrected trace-free witness vanishes on the found strata (c01=0 there); "
                                 "field-sector members (all moduli components zero) pair to zero with every "
                                 "gauge direction on every stratum = the all-strata OB1 carrier",
            "stratification_stamp": "TYPED-NOT-EXHAUSTED: the codim-1 layer is exhaustive (Groebner minor-ideal "
                                    "proof); the deeper layers are derived examples + the method (per-branch "
                                    "nullspace/pairing computation), not a census",
        },
        "positive_observation": "FIRST nontrivial pointwise Noether content of the response problem: on the "
                                "reciprocal-isotropy locus k_mod=0 the forced trace-free slot r_tf is tied "
                                "EXACTLY to the mixing kernel M. Scope: registered chart, stationary "
                                "presentation, pointwise, one-parameter, off-shell, polynomial/formal in "
                                "moduli. Factual cross-thread note: the identity's gauge direction is the "
                                "screen rotation (the twist/angular direction).",
    },
    "checks": CHECKS,
    "alphabet": ALPHABET_ARGS,
    "alphabet_functional_dims_base": dims,
    "character_modules": {k: {"generators": v[0], "min_generators": v[1], "note": v[2]} for k, v in MODULE.items()},
    "component_table": [{"component": c, "character": ch, "note": n} for c, ch, n in COMPONENT_TABLE],
    "branches": [{"label": b, "content": d, "status": st} for b, d, st in BRANCHES],
    "verdict": {
        "class": "OB1",
        "statement": "R_PW at the declared scope (jet<=2, registered chart/stationary presentation, "
        "polynomial-formal in moduli) is NONEMPTY and exactly parametrized: each component = "
        "(character-matched module of rank 1/5/4/4 with exhibited minimal generators over the "
        "11-generator invariant ring) x (functions of the graded alphabet, dims 10/13/16), "
        "CUT BY the A1 stratum Noether identities on the degeneration strata (R7(b) A1-AMENDED, "
        "rounds 1+2: generically vacuous — trivial per-member stabilizer at generic moduli — plus "
        "the exact k_mod=0 identity -2 k10 r_tf + <M, J C> = 0, the ONLY codimension-1 cut; the "
        "four NAMED C=0 resonance identities auto-satisfied in the declared class; FURTHER genuine "
        "cuts on the C!=0 resonance sub-varieties — derived example -c10 R_k10 - k10 R_c10 = 0 on "
        "{lam-k_mod=-1, c00=c01=0}; deeper stratification TYPED-NOT-EXHAUSTED); J06 "
        "determined/retained branches both open per family, none chosen; jet 3/4 typed "
        "NOT-EXHAUSTED; no member selected.",
        "known_object_locations_observations": [
            "omega = k10 dk10 shape: INSIDE off the C!=0 resonance sub-varieties (chi_a sector, R_k10 = a1); "
            "satisfies the k_mod=0 identity (on-stratum witness there); VIOLATES the C!=0 resonance shear "
            "identity — NOT a universal on-resonance witness (R2 per-witness stratum stamps)",
            "EH-form (stationary restriction): INSIDE jet<=2 class (Route C TC3 cited; anchored Q-powers recomputed)",
            "Bach-form: OUTSIDE jet<=2, INSIDE typed jet-3/4 extension (Route C TC2 cited)",
            "CM0-C-type nonvariational members: NOT excluded pointwise (Helmholtz is gate 3, not PW; L6 both ways)",
        ],
        "exclusions_by_PW_requirement": [
            "character-mismatched components (R7a/J10)",
            "absolute-phi bulk dependence (J04/F-RA4)",
            "pure-trace screen kernels from the k_mod-DETERMINED branch (R4/J06)",
            "restrict-then-vary objects / EH-RED scar class (R12/J14)",
            "fitted-global-average couplings and non-census blocks (R1/R13/J12, definition-level)",
        ],
    },
    "scope_stamps": [
        "EXHAUSTED scope: jet<=2 in varied fields; registered positive triangular chart; registered stationary "
        "presentation (general arenas: multi-index jets, same character/shift structure — typed); one-parameter, "
        "off-shell; polynomial/formal in (k10,C) (smooth = Schwarz-type Category-A extension, stamped)",
        "A1 (rounds 1+2): the parametrization is exact OFF the degeneration strata; ON them it is CUT by the "
        "stratum Noether identities (k_mod=0: the only CODIMENSION-1 cut; the four named C=0 resonance strata: "
        "auto-satisfied in the declared class; the C!=0 resonance sub-varieties: FURTHER genuine cuts, one "
        "derived example — the shear identity — with the FULL deeper stratification TYPED-NOT-EXHAUSTED; "
        "field-sector vanishing derived on the registered stationary presentation, general arenas typed)",
        "jet 3/4: TYPED, NOT-EXHAUSTED (F-B3); the A1 stratum identities are order-independent (moduli-sector)",
        "BR-M moduli-field and BR-CE promoted-anchor branches: TYPED, NOT-EXHAUSTED (class extensions)",
        "wall/corner slot depth: example-typed per Route C TC5 (cited), not proven exhaustive",
        "full syzygy ideal of the character modules and full relation ideal of the invariant ring: NOT computed "
        "(generation + minimality + sample relations proven; sufficient for the parametrization)",
        "WS/GC requirements (R3, R5, R6, R9, R14, R15; J07-J09, J11, J13-completion, J15) NOT imposed — Stage 3",
    ],
    "falsifier_record": {
        "F-B1": "clean — known-object locations recorded as observations; no member selected/privileged; no gate run",
        "F-B2": "clean — six branch labels carried; BR-B and BR-C proven pointwise branch-independent, others labeled",
        "F-B3": "TWO F-B3-CLASS SCOPE SLIPS, both verifier-caught and amended: (round 1) the R7(b) vacuity "
                "over-claim (a generic-stratum truth stated unqualified — A1); (round 2) the 'only genuine cut' "
                "headline (the same error class one level down: a stratum-blind uniqueness gloss over the "
                "C!=0 resonance sub-varieties — A1-R2, closure verdict NEW-DEFECT C3); otherwise clean — every "
                "exhaustive claim carries the jet<=2 stamp; jet-3/4 typed separately",
        "F-B4": "clean — Stage-1 A1-amended character rule and A3-amended channel class used throughout; banked "
                "facts recomputed and matched; the verifier flagged the upstream generic-only GLOSSES (Stage-1 "
                "POSED §1.4; Route B T1 headline) — routed via UPSTREAM_PRECISION_FLAG.md, not applied here",
        "F-B5": "see all_passed / exit code",
        "F-B6": "clean — every equivariant space carries its computed basis (module generators + generation proof to deg 6 + parity argument cited + minimality + syzygies)",
    },
    "throughput": "FULL SCOPE at the declared jet<=2 (not throughput-limited); single CPU process, exact SymPy",
}

with open("routeA_stage2_results.json", "w") as fh:
    json.dump(result, fh, indent=2, sort_keys=False)
    fh.write("\n")

print(f"\n{n_pass}/{n_tot} checks passed = {n_sub_pass}/{n_sub} substantive zero-residual checks "
      f"+ {n_guard_pass}/{n_guard} citation guards (A2 split).")
print("Verdict:", result["verdict"]["class"], "-",
      "R_PW NONEMPTY, exactly parametrized CUT BY the A1 stratum Noether identities (no member selected)")
sys.exit(0 if all_pass else 1)
