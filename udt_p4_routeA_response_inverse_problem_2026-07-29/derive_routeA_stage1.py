#!/usr/bin/env python3
"""P4 Route A Stage 1 — requirement-forced structure derivation (TA6 + TA2/TA4 identities).

Contract: udt_p4_routeA_response_inverse_problem_2026-07-29/PREREGISTRATION.md (frozen first).
Exact SymPy, zero-residual checks, deterministic (no floats, no randomness, no network),
single CPU process, bounded. Exit 0 iff every check passes; nonzero otherwise (F-A5).

This script POSES nothing new and SELECTS nothing: every check either (a) recomputes a
banked identity used as a load-bearing input (consistency recomputation, cited), or
(b) establishes a requirement-FORCED structural statement about the general response
object, candidate-free, with its scope stamp emitted into the JSON (F-A6).

AMENDED 2026-07-29 per VERIFIER_REPORT.md (A1/A3): the F-RA1 K4 clause is restated as
character-matched RELATIVE invariance (new A6 checks, embodying the verifier's
omega = k10*dk10 counterexample); the F-RA2 channel class is narrowed to functionals of
tr X and det e^{phi X}, with the exact slot theorem (new B5 checks, embodying the
verifier's tr(X^2) counter-channel). Pre-amendment run: 34/34, exit 0.

Conventions copied from the banked Route B script registration (07-28):
  eta = diag(-1,1,1,1); slots (0,1) = clock/ruler base, (2,3) = screen.
  Lorentz generator L{ab}: L[a,b] = 1, L[b,a] = -eta_aa/eta_bb.
  Extension class chart: X = [[H,0],[C,K]], H = diag(-1,1),
  K = [[k00,0],[k10,k11]] lower-triangular, C = [[c00,c01],[c10,c11]].
"""

import json
import sys

import sympy as sp
from sympy import Matrix, Rational, Symbol, symbols, exp, diff, simplify, eye, zeros

CHECKS = []


def check(name, residual_ok, detail=""):
    CHECKS.append({"name": name, "passed": bool(residual_ok), "detail": detail})
    status = "PASS" if residual_ok else "FAIL"
    print(f"[{status}] {name}" + (f" -- {detail}" if detail else ""))


def is_zero_matrix(M):
    return all(simplify(e) == 0 for e in M)


# ----------------------------------------------------------------------------
# S0 — conventions and generators (recomputation of banked registration)
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
    all(is_zero_matrix(L.T * eta + eta * L) for L in GENS.values()),
    "all six L satisfy L^T.eta + eta.L = 0",
)
check("S0_generator_count_6", len(GENS) == 6, "so(1,3) basis size")

# ----------------------------------------------------------------------------
# A — TA6(a): J10 equivariance + scalar-only centralizer + K4 => covariance type
# ----------------------------------------------------------------------------

# A1: commutant of so(1,3) in gl(4) is exactly the scalars (rank-15 linear system).
bvars = symbols("b0:16")
B = Matrix(4, 4, bvars)
eqs = []
for L in GENS.values():
    Cm = B * L - L * B
    eqs.extend(list(Cm))
Amat, _ = sp.linear_eq_to_matrix(eqs, list(bvars))
rank = Amat.rank()
null = Amat.nullspace()
check("A1_so13_commutant_rank_15", rank == 15, f"rank = {rank}")
scalar_ok = len(null) == 1 and is_zero_matrix(
    Matrix(4, 4, list(null[0])) - null[0][0] * eye(4)
)
check(
    "A1_so13_commutant_solution_is_scalar",
    scalar_ok,
    "nullspace = span{I}: the only Lorentz-invariant generator is c*I (scalar-only centralizer, recomputes banked 07-26/07-28 fact)",
)

# A2: the exact Klein four-group residual (banked Route B A1) — recomputed.
I4 = eye(4)
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]
check(
    "A2_klein_elements_proper_orthochronous",
    all(
        is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 and M[0, 0] == 1
        for M in K4
    ),
    "all four in SO+(1,3)",
)
closed = all(any(is_zero_matrix(M1 * M2 - M3) for M3 in K4) for M1 in K4 for M2 in K4)
check("A2_klein_closure", closed, "multiplication table closed")
check("A2_klein_involutions", all(is_zero_matrix(M * M - I4) for M in K4), "every element an involution")
check("A2_klein_R12_R13_product_is_R23", is_zero_matrix(R12 * R13 - R23), "K4 = Z2 x Z2 structure")

# A3: K4 action on the registered class X = [[H,0],[C,K]] — recomputed exactly.
k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb

XR23 = R23 * X * R23  # R23^{-1} = R23
expected_R23 = X.subs({c00: -c00, c01: -c01, c10: -c10, c11: -c11}, simultaneous=True)
check("A3_R23_action_C_negated_K_fixed", is_zero_matrix(XR23 - expected_R23), "(K,C) -> (K,-C)")

XR12 = R12 * X * R12
expected_R12 = X.subs({k10: -k10, c00: -c00, c11: -c11}, simultaneous=True)
check("A3_R12_action_flips_k10_c00_c11", is_zero_matrix(XR12 - expected_R12), "k10->-k10, (c00,c11)->-(c00,c11)")

XR13 = R13 * X * R13
expected_R13 = X.subs({k10: -k10, c01: -c01, c10: -c10}, simultaneous=True)
check("A3_R13_action_flips_k10_c01_c10", is_zero_matrix(XR13 - expected_R13), "k10->-k10, (c01,c10)->-(c01,c10)")

lam_expr = (k00 + k11) / 2
kmod_expr = (k11 - k00) / 2
invariant_seat = all(
    simplify((M * X * M)[2, 2] - k00) == 0 and simplify((M * X * M)[3, 3] - k11) == 0
    for M in K4
)
check(
    "A3_lambda_kmod_K4_invariant",
    invariant_seat,
    "k00,k11 (hence lambda=(k00+k11)/2, k_mod=(k11-k00)/2) fixed by all of K4 (banked)",
)

# A4: the K4-invariance pattern on moduli monomials — certification of the factorization
# statement "K4-well-defined components factor through K4-invariants".
subs_R12 = {k10: -k10, c00: -c00, c11: -c11}
subs_R13 = {k10: -k10, c01: -c01, c10: -c10}
subs_R23 = {c00: -c00, c01: -c01, c10: -c10, c11: -c11}
ACTIONS = [subs_R12, subs_R13, subs_R23]

invariant_monomials = [
    k10**2, c00**2, c11**2, c00 * c11, c01**2, c10**2, c01 * c10,
    k10 * c00 * c01, k10 * c00 * c10, k10 * c11 * c01, k10 * c11 * c10,
]
inv_ok = all(
    all(simplify(m.subs(a, simultaneous=True) - m) == 0 for a in ACTIONS)
    for m in invariant_monomials
)
check(
    "A4_invariant_monomials_certified",
    inv_ok,
    "k10^2; quadratics within each C character class; the four mixed cubics k10*{c00,c11}*{c01,c10}",
)

noninvariant_monomials = [k10, c00, c01, c10, c11, k10 * c00, k10 * c01, c00 * c01]
noninv_ok = all(
    any(simplify(m.subs(a, simultaneous=True) + m) == 0 for a in ACTIONS)
    for m in noninvariant_monomials
)
check(
    "A4_noninvariant_monomials_certified",
    noninv_ok,
    "each listed monomial is flipped by at least one K4 element: bare k10, bare C entries, k10*c-linear, cross-class quadratic are NOT chart-honest",
)

# A5: no Lorentz-invariant generator exists inside the class (base block founded H != c*I).
csym = Symbol("c")
sols = sp.solve([csym - (-1), csym - 1], [csym], dict=True)
check(
    "A5_no_lorentz_invariant_generator_in_class",
    len(sols) == 0,
    "commutant = c*I (A1) but the founded base block H=diag(-1,1) forces c=-1 AND c=+1: inconsistent -> no invariant member; the response must be an EQUIVARIANT family, not an invariant object",
)

# A6 (AMENDMENT A1, per VERIFIER_REPORT.md): character-matched RELATIVE invariance —
# the CORRECTED K4 clause of F-RA1. The original clause ("every component's (k10, C)-
# dependence must factor through the exact K4-invariants; bare k10/C-linear dependence
# is not chart-honest") is FALSE as universally quantified. Verifier counterexample:
# omega = k10*dk10 = (1/2) d(k10^2) is an EXACT, K4-INVARIANT one-form whose R_k10
# component is bare k10-linear (component and dk10 flip TOGETHER under R12/R13).
# The FORCED rule is: a component R_v must transform with the K4 CHARACTER of its
# paired direction dv (component character x direction character = trivial); verbatim
# factoring-through-invariants holds exactly for components along K4-invariant
# directions (dphi, base data, dlambda, dk_mod, boundary data).
# Characters under (R12, R13) [R23 = R12*R13]: trivial = (+,+) for phi/lam/k_mod;
# chi_a = (-,-) for k10; chi_b = (-,+) for c00, c11; chi_c = (+,-) for c01, c10.
K4_SUBS = [("R12", subs_R12), ("R13", subs_R13), ("R23", subs_R23)]


def dir_sign(v, subs_map):
    """Sign character of a coordinate direction dv under a K4 element (None = K4-invariant direction)."""
    if v is None:
        return 1
    return -1 if v in subs_map else 1


# (i) the counterexample as a zero-residual check: omega = k10*dk10 is K4-invariant as
# a ONE-FORM (pulled-back component * direction sign == component for every K4 element)
# while its component is NOT verbatim invariant — and omega is exact.
omega_comp = k10
omega_invariant = all(
    simplify(omega_comp.subs(sm, simultaneous=True) * dir_sign(k10, sm) - omega_comp) == 0
    for _, sm in K4_SUBS
)
component_not_verbatim = simplify(omega_comp.subs(subs_R12, simultaneous=True) + omega_comp) == 0
omega_exact = simplify(sp.diff(k10**2 / 2, k10) - omega_comp) == 0
check(
    "A6_counterexample_omega_k10_dk10_invariant_component_not_verbatim",
    omega_invariant and component_not_verbatim and omega_exact,
    "omega = k10*dk10 = (1/2)d(k10^2): K4-invariant AND exact as a one-form, yet its R_k10 component is bare k10-linear (flips together with dk10) -- refutes the original verbatim quantifier (verifier V3 counterexample recomputed)",
)

# (ii) the corrected rule on a GENERIC character-matched component set: for every
# character class, component character x direction character = trivial => the one-form
# is K4-invariant (well defined on the quotient).
q1, q2, q3, q4 = symbols("q1 q2 q3 q4")
inv_generic = q1 + q2 * k10**2 + q3 * c00 * c11 + q4 * k10 * c00 * c01  # generic invariant multiplier
matched_component_set = [
    (None, inv_generic),            # component along a K4-invariant direction (dphi/dlambda/dk_mod): trivial character
    (k10, k10 * inv_generic),       # R_k10 chi_a-relative via bare k10
    (k10, c00 * c01 * inv_generic), # R_k10 chi_a-relative via the c_b*c_c bilinear (verifier's alternative form)
    (c00, c00 * inv_generic),       # R_c00 chi_b-relative
    (c00, k10 * c01 * inv_generic), # R_c00 chi_b-relative via k10*c_c
    (c01, c01 * inv_generic),       # R_c01 chi_c-relative
]
matched_ok = all(
    all(
        simplify(comp.subs(sm, simultaneous=True) * dir_sign(v, sm) - comp) == 0
        for _, sm in K4_SUBS
    )
    for v, comp in matched_component_set
)
check(
    "A6_character_matching_rule_generic_component_set",
    matched_ok,
    "generic character-matched components (component character x direction character = trivial) are K4-invariant as one-form components in every character class -- the corrected forced rule holds",
)

# (iii) contrast (characterize, not filter): a character-MISMATCHED component breaks
# quotient well-definedness — this is the dependence that actually fails.
mismatched = c00 * inv_generic  # chi_b component placed on the chi_a direction dk10
mismatch_breaks = any(
    simplify(mismatched.subs(sm, simultaneous=True) * dir_sign(k10, sm) - mismatched) != 0
    for _, sm in K4_SUBS
)
check(
    "A6_character_mismatch_breaks_invariance_contrast",
    mismatch_breaks,
    "a chi_b-character component on the dk10 (chi_a) direction is NOT K4-invariant as a one-form: character MISMATCH (not bare-linearity) is the failure mode",
)

# T2 identities (TA2): the physical tangent and its transport law — recomputed.
T = X.T * eta + eta * X
T_expected = zeros(4, 4)
T_expected[0:2, 0:2] = 2 * eye(2)
T_expected[0:2, 2:4] = Cb.T
T_expected[2:4, 0:2] = Cb
T_expected[2:4, 2:4] = Kb + Kb.T
check("T2_tangent_block_form", is_zero_matrix(T - T_expected), "T = X^T.eta + eta.X = [[2I, C^T],[C, K+K^T]] (banked S0)")

t = Symbol("t")
ch = (exp(t) + exp(-t)) / 2
sh = (exp(t) - exp(-t)) / 2
Boost = Matrix([[ch, sh, 0, 0], [sh, ch, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
BoostInv = Boost.subs(t, -t)
check("T2_boost_is_lorentz", is_zero_matrix(sp.expand(Boost.T * eta * Boost - eta)), "exp(t L01) in SO+(1,3), exact exp form")

xg = symbols("x0:16")
Xgen = Matrix(4, 4, xg)


def tangent(M):
    return M.T * eta + eta * M


lhs = tangent(Boost * Xgen * BoostInv)
rhs = BoostInv.T * tangent(Xgen) * BoostInv
check(
    "T2_tangent_transport_bilinear_boost",
    is_zero_matrix(sp.expand(lhs - rhs)),
    "T(Lam X Lam^-1) = Lam^-T T(X) Lam^-1 for a generic X under the exact boost",
)
klein_transport = all(
    is_zero_matrix(sp.expand(tangent(M * Xgen * M) - M.T.inv() * tangent(Xgen) * M.inv()))
    for M in [R23, R12, R13]
)
check("T2_tangent_transport_bilinear_klein", klein_transport, "same law under all nontrivial K4 elements")

# ----------------------------------------------------------------------------
# B — TA6(b): requirement 4 + J06 on the two-scalar seat (lambda, k_mod)
# ----------------------------------------------------------------------------
lam, kmod, phi = symbols("lam k_mod phi")
a_seat = lam - kmod
d_seat = lam + kmod
check(
    "B1_seat_reconstruction",
    simplify((a_seat + d_seat) / 2 - lam) == 0 and simplify((d_seat - a_seat) / 2 - kmod) == 0,
    "a=lam-k_mod, d=lam+k_mod <=> lam=(a+d)/2, k_mod=(d-a)/2 (banked two-scalar seat)",
)

X_seat = sp.diag(-1, 1, a_seat, d_seat)
trX = sp.trace(X_seat)
check("B1_trace_channel_blind_to_kmod", simplify(trX - 2 * lam) == 0 and diff(trX, kmod) == 0,
      "tr X_seat = 2*lam exactly; d(tr)/d(k_mod) = 0 identically")

K_seat = sp.diag(a_seat, d_seat)
trace_part = (sp.trace(K_seat) / 2) * eye(2)
tracefree_part = K_seat - trace_part
check(
    "B2_screen_trace_tracefree_decomposition",
    is_zero_matrix(trace_part - lam * eye(2))
    and is_zero_matrix(tracefree_part - kmod * sp.diag(-1, 1))
    and sp.trace(tracefree_part) == 0,
    "K_seat = lam*I2 + k_mod*diag(-1,1); the anisotropic slot is exactly the k_mod direction",
)

Ffun = sp.Function("F")
trace_channel = Ffun(trX)
check(
    "B3_generic_trace_functional_zero_kmod_pairing",
    simplify(diff(trace_channel, kmod)) == 0,
    "ANY functional F(tr) has identically zero pairing with d/d(k_mod): the trace channel cannot select the transverse line (requirement 4 exact form)",
)

det_expX = exp(-phi) * exp(phi) * exp(a_seat * phi) * exp(d_seat * phi)
check(
    "B3_volume_density_channel_blind_to_kmod",
    simplify(det_expX - exp(2 * lam * phi)) == 0 and simplify(diff(det_expX, kmod)) == 0,
    "det e^{phi X_seat} = e^{2 lam phi}: every functional of the volume density det e^{phi X} is k_mod-blind (A3-amended class wording; matches banked T4_vol4_scaling)",
)

check(
    "B3_det_screen_channel_pairs_kmod_contrast",
    simplify(diff(K_seat.det(), kmod) + 2 * kmod) == 0,
    "contrast (characterize, not filter): det K = lam^2 - k_mod^2 DOES pair with k_mod generically -- the blindness is channel-specific, not universal",
)

sol_axes = sp.solve([lam, kmod], [lam, kmod], dict=True)
check(
    "B4_axes_intersect_only_at_spectator",
    sol_axes == [{lam: 0, kmod: 0}],
    "E07 axis {lam=0} and isotropic axis {k_mod=0} meet only at the origin (banked T4; MAP 'k=lambda' REFUTED stands)",
)

# B5 (AMENDMENT A3, per VERIFIER_REPORT.md): the channel-class quantifier NARROWED.
# The original F-RA2 clause ("every trace/volume/density-built screen functional is
# k_mod-blind") is FALSE as universally quantified. Verifier counter-channel:
# tr(X^2) is trace-BUILT yet pairs with k_mod. The theorem that survives: functionals
# of tr X (first trace) and of det e^{phi X} are k_mod-blind; and the EXACT slot
# theorem <r_tr*I2, diag(-1,1)> = 0 holds — the trace-free slot is still forced.
trX2 = sp.trace(X_seat * X_seat)
check(
    "B5_counter_channel_trX2_pairs_with_kmod",
    simplify(trX2 - (2 + 2 * lam**2 + 2 * kmod**2)) == 0
    and simplify(diff(trX2, kmod) - 4 * kmod) == 0,
    "tr(X_seat^2) = 2 + 2*lam^2 + 2*k_mod^2 with d/d(k_mod) = 4*k_mod != 0: a trace-BUILT channel that is NOT k_mod-blind -- the proven blind class is functionals of tr X (first trace) and of det e^{phi X} only (verifier V4 counter-channel recomputed)",
)

r_tr = Symbol("r_tr")
D2 = sp.diag(-1, 1)  # d(K_seat)/d(k_mod): the k_mod pairing direction on the seat
check(
    "B5_slot_theorem_pure_trace_kernel_zero_kmod_pairing",
    simplify(sp.trace((r_tr * eye(2)) * D2)) == 0,
    "<r_tr*I2, diag(-1,1)> = 0 identically: a screen pairing kernel with ZERO trace-free part has identically zero k_mod-pairing -- the exact surviving form of F-RA2's forcing",
)

kernel_trX2 = 2 * K_seat  # d tr(K^2) = <2K, dK>
tf_part = kernel_trX2 - (sp.trace(kernel_trX2) / 2) * eye(2)
check(
    "B5_trX2_kmod_pairing_routes_through_tracefree_slot",
    is_zero_matrix(tf_part - 2 * kmod * D2)
    and simplify(sp.trace(kernel_trX2 * D2) - 4 * kmod) == 0
    and simplify(sp.trace(tf_part * D2) - 4 * kmod) == 0
    and simplify(sp.trace((sp.trace(kernel_trX2) / 2 * eye(2)) * D2)) == 0,
    "d(tr K^2) kernel = 2K = 2*lam*I2 + 2*k_mod*diag(-1,1): its k_mod-pairing (= 4*k_mod) routes PRECISELY through its trace-free part 2*k_mod*diag(-1,1) (the pure-trace part contributes 0) -- slot-presence forcing SURVIVES the counter-channel (verifier V4 slot theorem recomputed)",
)

# ----------------------------------------------------------------------------
# C — TA6(c): requirement 12 (restrict-then-vary FORBIDDEN) + J14, structurally
# ----------------------------------------------------------------------------
x, y = symbols("x y")
Fw = x**2 + y + y**2  # exact witness functional on a 2-direction toy domain
restricted_crit = sp.solve(diff(Fw.subs(y, 0), x), x)
check("C1_restricted_stationarity_witness", restricted_crit == [0], "restrict {y=0} then vary: critical point x=0")

full_response_at_origin = (diff(Fw, x).subs({x: 0, y: 0}), diff(Fw, y).subs({x: 0, y: 0}))
check(
    "C1_full_response_normal_residual_nonzero",
    full_response_at_origin == (0, 1),
    "full response at the restricted critical point = (0, 1): the normal component is EXACTLY 1, not 0 -- restricted stationarity is not stationarity",
)

incompatible = sp.solve([diff(Fw, x), diff(Fw, y), y], [x, y], dict=True)
full_zero = sp.solve([diff(Fw, x), diff(Fw, y)], [x, y], dict=True)
check(
    "C2_full_zero_set_disjoint_from_restricted_critical",
    incompatible == [] and full_zero == [{x: 0, y: -Rational(1, 2)}],
    "the full zero set {(0,-1/2)} never meets the stratum {y=0}: zero-set-after-definition (J14) and vary-then-restrict (req 12) are inequivalent to the forbidden order, witnessed exactly",
)

# ----------------------------------------------------------------------------
# D — TA6(d): the additive-depth law (G01) at the pointwise level
# ----------------------------------------------------------------------------
p1, p2, s = symbols("phi1 phi2 s")
E_seat = lambda ph: sp.diag(exp(-ph), exp(ph), exp(a_seat * ph), exp(d_seat * ph))
check(
    "D1_seat_same_member_additivity",
    is_zero_matrix(sp.expand(E_seat(p2) * E_seat(p1) - E_seat(p1 + p2)).applyfunc(simplify)),
    "e^{phi2 X}e^{phi1 X} = e^{(phi1+phi2)X} per member (G01 composition realized)",
)

# E04 closed form (banked): M(phi;C) = [[e^{phi H},0],[C H (e^{phi H} - I), I]]
ph = Symbol("phi_")
expH = sp.diag(exp(-ph), exp(ph))


def M_E04(ph_val, Cm):
    eH = sp.diag(exp(-ph_val), exp(ph_val))
    M = zeros(4, 4)
    M[0:2, 0:2] = eH
    M[2:4, 0:2] = Cm * H2 * (eH - eye(2))
    M[2:4, 2:4] = eye(2)
    return M


X_E04 = zeros(4, 4)
X_E04[0:2, 0:2] = H2
X_E04[2:4, 0:2] = Cb
Mp = M_E04(ph, Cb)
ode_ok = is_zero_matrix(sp.expand(sp.diff(Mp, ph) - X_E04 * Mp).applyfunc(simplify))
init_ok = is_zero_matrix(Mp.subs(ph, 0) - eye(4))
add_ok = is_zero_matrix(sp.expand(M_E04(p2, Cb) * M_E04(p1, Cb) - M_E04(p1 + p2, Cb)).applyfunc(simplify))
check("D1_E04_closed_form_ODE_init_additive", ode_ok and init_ok and add_ok,
      "M' = X M, M(0)=I, same-member additivity exact (banked T2 closed form recomputed)")

fp, fq, fr = symbols("f_p f_q f_r")
delta = lambda u, v: v - u
check(
    "D2_every_scalar_f_depth_composition",
    simplify(delta(fp, fq) + delta(fq, fr) - delta(fp, fr)) == 0
    and simplify(delta(fq, fp) + delta(fp, fq)) == 0,
    "delta_f(p,q)=f(q)-f(p) satisfies reversal + 3-point composition for EVERY scalar f (joint audit sec.1 witness recomputed): additivity has zero selector rank on pointwise phi-dependence",
)

check(
    "D3_shift_is_left_group_translation",
    is_zero_matrix(sp.expand(E_seat(phi + s) - E_seat(s) * E_seat(phi)).applyfunc(simplify)),
    "e^{(phi+s)X} = e^{sX} e^{phi X}: a constant depth shift acts by left translation, not a new functional form",
)

cE = Symbol("c_E", positive=True)
check(
    "D3_anchor_absorption",
    simplify(cE * exp(-(phi + s)) - (cE * exp(-s)) * exp(-phi)) == 0,
    "founded stationary readout Q = c_E e^{-phi}: the shift is absorbed into the anchor c_E (joint audit sec.3)",
)

# ----------------------------------------------------------------------------
# Emit results
# ----------------------------------------------------------------------------
n_pass = sum(1 for c in CHECKS if c["passed"])
n_tot = len(CHECKS)
all_pass = n_pass == n_tot

FORCED = [
    {
        "id": "F-RA1",
        "target": "TA6(a)",
        "statement": (
            "J10 equivariance + the scalar-only so(1,3) centralizer (A1) + the founded "
            "non-scalar base block H (A5) force the response's covariance type: it CANNOT be a "
            "Lorentz-invariant object anchored on a fixed generator/plane (no such member exists "
            "in the class); it is forced to be an EQUIVARIANT family whose components transform "
            "contragradiently to the tangent transport T -> Lam^-T T Lam^-1 (T2 checks). On the "
            "registered chart the K4 quotient forces CHARACTER-MATCHED RELATIVE INVARIANCE per "
            "component (A1-AMENDED): a component R_v must transform with the K4 character of its "
            "paired direction dv (component character x direction character = trivial; A6 checks). "
            "Verbatim factoring through the exact K4-invariants (A4: k10^2, the C character-class "
            "quadratics, the four mixed cubics -- a GENERATING set of the full invariant ring, "
            "verifier-proven via character/parity + exhaustive degree<=6 factorization, "
            "VERIFIER_INDEPENDENT_CHECK.py V2) holds exactly for components along K4-invariant "
            "directions (dphi, base data, dlambda, dk_mod, boundary data); R_k10 must be "
            "chi_a-relative (e.g. k10*invariant or c_b*c_c*invariant), R_C components "
            "chi_b/chi_c-relative. Character MISMATCH (not bare-linearity) is the failure mode. "
            "Counterexample on record: omega = k10*dk10 = (1/2)d(k10^2) is K4-invariant and exact "
            "with a bare-k10-linear component (A6)."
        ),
        "scope": "POINTWISE (registered chart, one-parameter, off-shell); global assignment J07/J11 untouched",
        "checks": ["A1_*", "A2_*", "A3_*", "A4_*", "A5_*", "A6_*", "T2_*"],
    },
    {
        "id": "F-RA2",
        "target": "TA6(b)",
        "statement": (
            "Requirement 4 + J06 on the banked two-scalar seat (A3-AMENDED): the trace channel "
            "is exactly 2*lam, and every functional of tr X (first trace) and of the volume "
            "density det e^{phi X} = e^{2 lam phi} has identically zero pairing with the k_mod "
            "direction (B1/B3) -- NOT every trace/volume/density-built functional (counter-channel "
            "on record: tr(X^2) = 2 + 2*lam^2 + 2*k_mod^2 pairs with d/d(k_mod) = 4*k_mod, B5). "
            "The exact surviving slot theorem: a screen pairing kernel with zero trace-free part "
            "has identically zero k_mod-pairing (<r_tr*I2, diag(-1,1)> = 0, B5), and d(tr X^2)'s "
            "k_mod-pairing routes precisely through its trace-free part 2*k_mod*diag(-1,1) (B5). "
            "Hence J06's 'determined' branch for k_mod is reachable ONLY by a response carrying "
            "the trace-free screen slot k_mod*diag(-1,1) (B2) (and/or the k10, C mixing slots); a "
            "candidate without that slot can pass J06 only via its explicit-residual-modulus "
            "branch; omitting the slot silently = J06's named false pass ('spectator screen "
            "isotropy or trace zero assumed'). No candidate value is demanded (F-A1 respected): "
            "this forces a SLOT in the general object, not a nonzero value."
        ),
        "scope": "POINTWISE on the (lam, k_mod) seat; whole-solution/global selection of the moduli untouched (07-26 rank zero respected)",
        "checks": ["B1_*", "B2_*", "B3_*", "B4_*", "B5_*"],
    },
    {
        "id": "F-RA3",
        "target": "TA6(c)",
        "statement": (
            "Requirement 12 + J14 force a DEFINITIONAL ordering property of the object itself: "
            "the response is a one-form on the FULL typed domain, with components along every "
            "census direction (fields, moduli under both fork options, boundary data); any "
            "stratum restriction is a pullback of the full object performed AFTER definition. "
            "Exact witness (C1/C2): a two-direction functional whose restricted stationarity set "
            "{(0,0)} is disjoint from its true zero set {(0,-1/2)}, with normal residual exactly "
            "1 at the restricted critical point. J14's off-shell/on-shell separation is built in: "
            "the on-shell set is a DERIVED subset of the off-shell domain, never an input."
        ),
        "scope": "STRUCTURAL/DEFINITIONAL (pointwise-decidable on the object's definition); instantiated by an exact finite-dimensional witness",
        "checks": ["C1_*", "C2_*"],
    },
    {
        "id": "F-RA4",
        "target": "TA6(d)",
        "statement": (
            "The additive-depth law (G01) forces, at the pointwise level, ONLY shift-equivariance: "
            "phi -> phi + s acts by left group translation e^{sX} (D1/D3), absorbable into the "
            "observed anchor c_E on the founded stationary readout (D3_anchor_absorption). It "
            "forces NOTHING further about the response's pointwise phi-dependence: the "
            "every-scalar-f composition witness (D2, recomputing the joint audit) shows additivity "
            "has zero selector rank on pointwise functional form. Reported as-is (near-null "
            "result on this item; OA2-flavored)."
        ),
        "scope": "POINTWISE; the realized-profile/whole-solution content of G01 is untouched",
        "checks": ["D1_*", "D2_*", "D3_*"],
    },
]

result = {
    "package": "udt_p4_routeA_response_inverse_problem_2026-07-29",
    "stage": "Route A Stage 1 (TA6 + TA2/TA4 identities)",
    "date": "2026-07-29",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "n_checks": n_tot,
    "n_passed": n_pass,
    "all_passed": all_pass,
    "checks": CHECKS,
    "forced_statements": FORCED,
    "outcome_class": "OA1/OA2 MIXED: nontrivial candidate-free forced structure exists "
    "(F-RA1..F-RA3 = OA1 items); the G01 item is near-null pointwise (F-RA4 = OA2 item); "
    "no requirement clash surfaced (no OA3)",
    "throughput": "FULL SCOPE (not throughput-limited); single CPU process, exact SymPy",
    "no_candidate_no_gate_run": "no response candidate constructed, selected, or privileged; no gate executed (F-A1 clean by construction)",
    "amendments": "A1-A4 applied 2026-07-29 per VERIFIER_REPORT.md: F-RA1 K4 clause restated "
    "as character-matched RELATIVE invariance (new A6 checks; verifier counterexample "
    "omega = k10*dk10 embodied); F-RA2 channel class narrowed to functionals of tr X and "
    "det e^{phi X} with the exact slot theorem (new B5 checks; verifier counter-channel "
    "tr(X^2) embodied); gate specs 2/4/6 corrected in SIX_GATE_SPECS.md; clash scan "
    "extended in POSED_INVERSE_PROBLEM.md sec.3.2. Pre-amendment run: 34/34, exit 0. "
    "See CORRECTION_LAYER.md.",
}

with open("routeA_stage1_results.json", "w") as fh:
    json.dump(result, fh, indent=2, sort_keys=False)
    fh.write("\n")

print(f"\n{n_pass}/{n_tot} zero-residual checks passed.")
print("Outcome class:", result["outcome_class"])
sys.exit(0 if all_pass else 1)
