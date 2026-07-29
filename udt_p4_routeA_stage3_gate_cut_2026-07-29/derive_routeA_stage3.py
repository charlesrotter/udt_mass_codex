#!/usr/bin/env python3
"""P4 Route A Stage 3 (Slice 1) — the candidate-free gate cuts on R_PW (TC1-TC5 computations;
TC6 lives in SLICE2_SURFACE.md).

Contract: udt_p4_routeA_stage3_gate_cut_2026-07-29/PREREGISTRATION.md (frozen first).
Exact SymPy, zero-residual checks, deterministic (no floats, no randomness, no network),
single CPU process, bounded. Exit 0 iff every check passes; nonzero otherwise (F-S5).

AMENDED (A1/A4, 2026-07-29, per VERIFIER_REPORT.md — see CORRECTION_LAYER.md):
A1 — the anchored-log forcing claim is RESTATED with its exact condition (the verifier's
in-family counterexample V10b refuted the 'whenever the field sector is nonzero' quantifier;
an F-S3-class slip): the LE cell's lambda-slot is forced nonzero — log(c_E/Q)-carrying via
the a_F' p0 term — IFF d/dlam (WF R_a) != 0 for some field slot a; in particular for every
lambda-INDEPENDENT nonzero field sector. Three new zero-residual A1_* checks bank the
counterexample, the iff condition, and the lambda-independent sub-case. A4 — three
guard-grade checks reclassified substantive -> guard (TC4_torsion_period_vacuous,
TC1_no_empty_adjudicated_cell, TC2_kmod0_identity_is_row_dependency).

SLICE-1 BOUNDARY (binding): candidate-free gate cuts ONLY. NO member of R_PW is selected,
privileged, or ranked (F-S1); NO solution of R = 0 is computed and NO solution-dependent
conclusion is drawn (F-S6); NO completion class chosen, NO boundary-data choice made, NO
pairing adopted (F-S2 — every G3 statement carries its pairing-branch label or a proven
branch-independence); every only/all/none/exhaustive/vacuous/empty claim carries its stratum
scope stamp (F-S3 — the NAMED recurring error class).

RESONANCE RULE (inherited, binding): adjudications SPECIFIC to sub-families contacting the
resonance locus (lam -+ k_mod in {+-1}) beyond the banked k_mod = 0 codim-1 identity are
DEFERRED, marked CENSUS-REQUIRED. The banked C != 0 shear-identity example is CITED (never
re-adjudicated here); the resonance-stratum rows of the gate-cut ledger carry the flag.

Banked inputs (cited; recomputed only as consistency, never re-derived as new):
- Stage 2 (udt_p4_routeA_stage2_pointwise_reduction_2026-07-29, 2c0e7cc): R_PW stratified
  parametrization; the k_mod = 0 identity -2 k10 r_tf + m00c10 + m01c11 - m10c00 - m11c01 = 0;
  the shear-identity example; character modules; wall-alphabet rule (trace jets <= grade-1).
- Stage 1 (udt_p4_routeA_response_inverse_problem_2026-07-29): SIX_GATE_SPECS.md (amended);
  POSED_INVERSE_PROBLEM.md 1.5 pairing enumeration P1/P2/P3 (NONE adopted).
- GR-analog recon (udt_gr_analog_reconnaissance_2026-07-29): pairing-relative Helmholtz,
  wall/corner jet-slot bookkeeping, integrability-complex typing, twisted-cocycle holonomy
  [twisted-H1 row = MODEL-KNOWLEDGE, F-S7 flag] — METHOD under the lane clause (Category-A).
- Route C TC5 (udt_p4_routeC_shared_static_sector_2026-07-28): boundary-data instances
  (2nd-order -> 1-jet wall; 4th-order -> 2-jet wall + 3rd-normal-derivative momenta).

Conventions copied from the banked Route B registration (as in Stages 1-2):
eta = diag(-1,1,1,1); X = [[H,0],[C,K]], H = diag(-1,1), K lower-triangular.
Registered stationary one-parameter presentation: fields (phi, f, bh) of one variable,
jets p0..p2 / f0..f2 / h0..h2 (the banked EXHAUSTIVE jet <= 2 layer); moduli
(lam, k_mod, k10, c00, c01, c10, c11) constants on the BASE branch (BR-M typed only).
Components depend on p0 ONLY through the anchored Q = c_E e^{-p0} at supplied c_E
(J04; log(c_E/Q) = p0 is the anchored depth — recomputed below): using p0 as the
grade-0 argument at fixed supplied c_E is an exact relabeling (Category-A).

Pairing branches (the banked 1.5 enumeration; NONE adopted): the bulk pairings are carried
as the ANCHORED-WEIGHT FAMILY <R, dX> = int [ sum_a WF R_a dU_a + sum_mu WM R_mu dm_mu ] dx
with per-slot weights WF = e^{aF(m) p0}, WM = e^{aM(m) p0} (supplied structure, tagged):
P2 = (aF, aM) = (0, 0); P1 instances (Route B T4 enumerated volumes): 4D-coframe aF = 2 lam,
ruler+screen-triad aF = 1 + 2 lam (moduli-slot weight aM supplied per slot); P3 = a declared
bulk choice (P1-type or P2-type) + wall/corner densities (bulk conditions inherited — proven
below; wall block typed to gate 5/TC3). The coordinate measure dx on the registered chart is
Category-A conditioning.
"""

import json
import sys

import sympy as sp
from sympy import (Function, Matrix, Rational, Symbol, symbols, exp, log, diff,
                   expand, simplify, eye, zeros)

CHECKS = []

CITATION_GUARDS = {
    "TC1_both_volumes_same_dlambda",
    "TC1_weight_map_preserves_characters",
    "TC2_counts_determined_type",
    "TC2_LE_symbol_symmetry_restatement",
    "TC2_resonance_census_required",
    "TC3_slot_survival_table",
    "TC3_wall_grade_availability_jet2",
    "TC3_routeC_TC5_anchor_reproduced",
    "TC3_NV_cell_no_forced_slots",
    "TC3_mirror_canon_parity_instance",
    "TC3_corner_census_typed_only",
    "TC4_typing_table_assembled",
    "TC4_FS7_flag_carried",
    "TC4_completion_cycles_need_data",
    "TC5_ledger_coverage_counts",
    "TC5_known_object_rows_are_observations",
    # A4 reclassification (verifier, 2026-07-29): guard-grade in computational content —
    # TC4_torsion_period_vacuous (solve(2P=0) is trivial arithmetic; the argument lives in
    # the detail string), TC1_no_empty_adjudicated_cell (re-aggregation of upstream
    # booleans), TC2_kmod0_identity_is_row_dependency (load-bearing content = a verified
    # Stage-2 CITATION; the dep_vec leg is a retyped comparison, the nullspace leg repeats S0).
    "TC4_torsion_period_vacuous",
    "TC1_no_empty_adjudicated_cell",
    "TC2_kmod0_identity_is_row_dependency",
}


def check(name, ok, detail=""):
    kind = "citation-guard" if name in CITATION_GUARDS else "substantive"
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail, "kind": kind})
    status = "PASS" if ok else "FAIL"
    tag = " [guard]" if kind == "citation-guard" else ""
    print(f"[{status}]{tag} {name}" + (f" -- {detail}" if detail else ""))


def is_zero_matrix(M):
    return all(simplify(e) == 0 for e in M)


# ============================================================================
# S0 — banked-structure recomputation (consistency, cited; compact Stage-2 reuse)
# ============================================================================
print("--- S0: banked structure recomputed (consistency) ---")

eta = sp.diag(-1, 1, 1, 1)


def lorentz_generator(a, b):
    L = zeros(4, 4)
    L[a, b] = 1
    L[b, a] = -Rational(eta[a, a], eta[b, b])
    return L


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
GENS = {f"L{a}{b}": lorentz_generator(a, b) for (a, b) in PAIRS}

I4 = eye(4)
R23g = sp.diag(1, 1, -1, -1)
R12g = sp.diag(1, -1, -1, 1)
R13g = sp.diag(1, -1, 1, -1)
K4 = [I4, R23g, R12g, R13g]

k00, k10, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb

check(
    "S0_K4_and_X_recomputed",
    all(is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 for M in K4)
    and is_zero_matrix(R12g * R13g - R23g)
    and is_zero_matrix(X[0:2, 0:2] - H2),
    "K4 exact (proper orthochronous, closed) and the registered E02 footing X = [[H,0],[C,K]] "
    "(banked Route B / Stage-2 conventions recomputed)",
)

# Pointwise tangency system at the general member (Stage-2 PW2/A1 reuse — consistency):
bcoef = symbols("beta0:6")
B = zeros(4, 4)
for i, Lm in enumerate(GENS.values()):
    B = B + bcoef[i] * Lm
FORBIDDEN = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
Cm_pt = B * X - X * B
eqs_pt = [Cm_pt[i, j] for (i, j) in FORBIDDEN]
A_pt, _ = sp.linear_eq_to_matrix(eqs_pt, list(bcoef))
GENERIC_PT = {k00: 2, k10: 3, k11: 5, c00: 7, c01: 11, c10: 13, c11: 17}
check(
    "S0_generic_pointwise_stabilizer_trivial",
    A_pt.subs(GENERIC_PT).rank() == 6 and A_pt.subs(GENERIC_PT).nullspace() == [],
    "GENERIC-stratum scope stamp: at generic moduli the per-member tangency stabilizer is "
    "trivial (rank 6, empty nullspace) — NO pointwise Noether identity there (Stage-2 "
    "PW2_R7b recomputed as consistency; the k_mod = 0 and resonance strata carry identities)",
)

# The k_mod = 0 identity recomputed from [L23, X] (Stage-2 A1 (ii)-(vi), compact):
A_iso = A_pt.subs(k11, k00)
ns_iso = A_iso.nullspace()
L23m = GENS["L23"]
W23 = (L23m * X - X * L23m).subs(k11, k00)
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
I2A = eye(2)
D2A = sp.diag(-1, 1)
E21A = Matrix([[0, 0], [1, 0]])
E12A = Matrix([[0, 1], [0, 0]])
W_slotA = r_tr * I2A + r_tf * D2A + r_sh * E21A + r_nl * E12A
MkerA = Matrix([[m00, m01], [m10, m11]])
pairA = lambda A_, B_: sp.trace(A_.T * B_)
pairing_stratum = sp.expand(pairA(W_slotA, W23[2:4, 2:4]) + pairA(MkerA, W23[2:4, 0:2]))
IDENT_KMOD0 = sp.expand(-2 * k10 * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
check(
    "S0_kmod0_identity_recomputed",
    len(ns_iso) == 1
    and sp.expand(pairing_stratum - IDENT_KMOD0) == 0,
    "on k_mod = 0 the tangency nullspace is 1-dim (screen rotation L23) and the exact "
    "pointwise R7(b) identity is -2 k10 r_tf + m00c10 + m01c11 - m10c00 - m11c01 = 0 "
    "(Stage-2 A1 recomputed as consistency; r_tr, r_sh, r_nl drop out)",
)

# ============================================================================
# Jet machinery (registered stationary one-parameter presentation; BASE branch)
# ============================================================================
print("\n--- Jet machinery ---")

FIELDS = ["p", "f", "h"]  # phi, f, bh on the registered stationary presentation
JMAX = 8
J = {a: symbols(f"{a}0:{JMAX + 1}") for a in FIELDS}
V = {a: symbols(f"v{a}0:{JMAX + 1}") for a in FIELDS}  # variation jets
lam, kmod = symbols("lam k_mod")
MODULI = [lam, kmod, k10, c00, c01, c10, c11]
cE = Symbol("c_E", positive=True)

ALL_CHAINS = [list(J[a]) for a in FIELDS] + [list(V[a]) for a in FIELDS]


def Dx(expr):
    """Total x-derivative on the jet space (moduli constant on the BASE branch)."""
    out = sp.Integer(0)
    for chain in ALL_CHAINS:
        for k in range(len(chain) - 1):
            d = diff(expr, chain[k])
            if d != 0:
                out += d * chain[k + 1]
    return out


def Dxn(expr, n):
    for _ in range(n):
        expr = Dx(expr)
    return expr


def Euler(expr, a, order):
    """Euler operator E_a on expressions of jet order <= order."""
    out = sp.Integer(0)
    for k in range(order + 1):
        out += (-1) ** k * Dxn(diff(expr, J[a][k]), k)
    return out


ARGS2 = (J["p"][0], J["f"][0], J["h"][0], J["p"][1], J["f"][1], J["h"][1],
         J["p"][2], J["f"][2], J["h"][2], *MODULI)
ARGS1 = (J["p"][0], J["f"][0], J["h"][0], J["p"][1], J["f"][1], J["h"][1], *MODULI)

p0, p1, p2 = J["p"][0], J["p"][1], J["p"][2]

s_re = Symbol("s_re", real=True)
check(
    "J0_anchored_relabeling",
    simplify(sp.expand_log(log(cE / (cE * exp(-p0))), force=True) - p0) == 0
    and simplify(cE * exp(-(p0 + s_re)) - (cE * exp(-s_re)) * exp(-p0)) == 0,
    "log(c_E/Q) = p0 exactly (Q = c_E e^{-p0}): at supplied c_E the grade-0 argument p0 is an "
    "exact relabeling of the anchored Q (Category-A); the anchored-depth log is alphabet-legal "
    "(a smooth function of Q at supplied c_E) — J04 provenance carried, not altered",
)

# ============================================================================
# TC1 — the Helmholtz partition (gate 3), pairing-relative, per stratum
# ============================================================================
print("\n--- TC1: Helmholtz partition (pairing-relative) ---")


def frechet(Delta, order):
    return {a: {b: [diff(Delta[a], J[b][k]) for k in range(order + 1)]
                for b in FIELDS} for a in FIELDS}


def helmholtz2(Delta):
    """The jet<=2 field-field Helmholtz condition families (derived below as exactly
    self-adjointness of the Frechet operator w.r.t. the reference measure)."""
    Fr = frechet(Delta, 2)
    Hi2 = {(a, b): Fr[a][b][2] - Fr[b][a][2] for a in FIELDS for b in FIELDS}
    Hi1 = {(a, b): Fr[a][b][1] + Fr[b][a][1] - 2 * Dx(Fr[b][a][2])
           for a in FIELDS for b in FIELDS}
    Hi0 = {(a, b): Fr[a][b][0] - Fr[b][a][0] + Dx(Fr[b][a][1]) - Dxn(Fr[b][a][2], 2)
           for a in FIELDS for b in FIELDS}
    return Fr, Hi2, Hi1, Hi0


# (1) The condition system IS self-adjointness (adjoint-comparison, generic components):
Rgen = {a: Function(f"R{a}")(*ARGS2) for a in FIELDS}
Fr_g, Hi2_g, Hi1_g, Hi0_g = helmholtz2(Rgen)
adjoint_matches = True
for a in FIELDS:
    Dop_a = sum(Fr_g[a][b][k] * V[b][k] for b in FIELDS for k in range(3))
    Adj_a = sum((-1) ** k * Dxn(Fr_g[b][a][k] * V[b][0], k)
                for b in FIELDS for k in range(3))
    diffr = expand(Adj_a - Dop_a)
    for b in FIELDS:
        if expand(diff(diffr, V[b][2]) + Hi2_g[(a, b)]) != 0:
            adjoint_matches = False
        if expand(diff(diffr, V[b][1]) + Hi1_g[(a, b)]) != 0:
            adjoint_matches = False
        if expand(diff(diffr, V[b][0]) + Hi0_g[(a, b)]) != 0:
            adjoint_matches = False
check(
    "TC1_conditions_are_selfadjointness",
    adjoint_matches,
    "for the GENERAL jet<=2 component triple the adjoint-minus-operator coefficients are "
    "exactly -(Hi2, Hi1, Hi0): the recorded condition families ARE Frechet self-adjointness "
    "w.r.t. the reference measure (weights absorbed into Delta) — derived, not imported",
)

# (2) Necessity on the generic Euler-Lagrange image (order-1 L -> jet<=2 source form):
Lgen = Function("Lgen")(*ARGS1)
Delta_EL = {a: expand(Euler(Lgen, a, 2)) for a in FIELDS}
_, Hi2_e, Hi1_e, Hi0_e = helmholtz2(Delta_EL)
check(
    "TC1_helmholtz_necessity_generic_L",
    all(expand(Hi2_e[k]) == 0 for k in Hi2_e)
    and all(expand(Hi1_e[k]) == 0 for k in Hi1_e)
    and all(expand(Hi0_e[k]) == 0 for k in Hi0_e),
    "Delta = E(L) for the GENERIC order-1 Lagrangian (all field/jet/moduli args) satisfies "
    "all three condition families identically: the conditions are NECESSARY for local "
    "exactness (sufficiency = the banked bicomplex/Vainberg statement, Category-A cited, "
    "witness-instantiated below)",
)

# (3) The anchored-weight family: shifted conditions (the pairing-dependence map).
aF = Function("a_F")(lam)   # field-slot anchored exponent (supplied structure, tagged)
aM = Function("a_M")(lam)   # moduli-slot anchored exponent (supplied structure, tagged)
WF = exp(aF * p0)
WM = exp(aM * p0)
DeltaW = {a: WF * Rgen[a] for a in FIELDS}
_, Hi2_w, Hi1_w, Hi0_w = helmholtz2(DeltaW)

top_invariant = all(
    expand(Hi2_w[(a, b)] / WF - Hi2_g[(a, b)]) == 0 for a in FIELDS for b in FIELDS
)
check(
    "TC1_weight_top_condition_invariant",
    top_invariant,
    "condition family (i) [principal-symbol symmetry dR_a/du_b'' = dR_b/du_a''] is IDENTICAL "
    "across the whole anchored-weight family e^{a_F(m) p0} — SCOPE STAMP: pairing-independence "
    "holds across the enumerated anchored bulk family (P1 instances/P2/P3-bulk) at jet <= 2 on "
    "the registered stationary presentation, NOT for arbitrary unenumerated pairings",
)

shift_ii_ok = all(
    expand(Hi1_w[(a, b)] / WF - (Hi1_g[(a, b)] - 2 * aF * p1 * Fr_g[b][a][2])) == 0
    for a in FIELDS for b in FIELDS
)
check(
    "TC1_weight_shift_condition_ii",
    shift_ii_ok,
    "condition family (ii) shifts EXACTLY by -2 a_F p1 (dR_b/du_a''): "
    "Hi1(W R)/W = Hi1(R) - 2 a_F(lam) p1 dR_b/du_a'' — the derived pairing-dependence of the "
    "first-order Helmholtz layer (a_F = 0 recovers P2)",
)

delta0_pf = expand(Hi0_w[("p", "f")] / WF - Hi0_g[("p", "f")])
delta0_vanishes_unweighted = all(
    expand((Hi0_w[(a, b)] / WF - Hi0_g[(a, b)]).subs(aF, 0)) == 0
    for a in FIELDS for b in FIELDS
)
check(
    "TC1_weight_shift_condition_iii_vanishes_at_aF0",
    delta0_vanishes_unweighted,
    "the condition-(iii) weight shift vanishes identically at a_F = 0 (P2 recovered); the "
    "exact (p,f) shift expression is recorded in the JSON (contains the asymmetric "
    "p0-column a_F terms and the a_F p1 transport terms)",
)

# (4) Mixed field-moduli condition H4 and moduli-moduli condition H5.
Rmod = {str(mu): Function(f"Rm_{i}")(*ARGS2) for i, mu in enumerate(MODULI)}
Lt = Function("Ltil")(*ARGS1)
S_int = WF * Lt   # generic generated action density on the anchored-weight branch
gen_H4_ok = True
for a in FIELDS:
    Del_a = Euler(S_int, a, 2)
    for mu in MODULI:
        resid = expand(diff(Del_a, mu) - Euler(diff(S_int, mu), a, 2))
        if resid != 0:
            gen_H4_ok = False
check(
    "TC1_H4_generated_witness",
    gen_H4_ok,
    "H4 [d(WF R_a)/dm_mu = E_a(WM R_mu)] holds identically on the generated family "
    "R_a = WF^{-1} E_a(WF Ltil), R_mu = WM^{-1} d(WF Ltil)/dm_mu, for the GENERIC order-1 "
    "Ltil and every modulus (parameter-derivative/Euler-operator commutation, exact)",
)

# H4 by-parts identity (the mu-row adjoint is the Euler operator):
G_expr = WM * Rmod["lam"]
expr_bp = sum(diff(G_expr, J["p"][k]) * V["p"][k] for k in range(3)) \
    - Euler(G_expr, "p", 2) * V["p"][0]
# total-derivative certificate: Xi with expr_bp = Dx(Xi)
Xi = diff(G_expr, J["p"][1]) * V["p"][0] + diff(G_expr, J["p"][2]) * V["p"][1] \
    - Dx(diff(G_expr, J["p"][2])) * V["p"][0]
check(
    "TC1_H4_byparts_identity",
    expand(expr_bp - Dx(Xi)) == 0,
    "the mu-row pairing transfer sum_k dG/du^{(k)} v^{(k)} - E_u(G) v = Dx(Xi) with the "
    "explicit certificate Xi: the mixed-block adjoint used in H4 is exactly the Euler "
    "operator (derived; boundary residue Xi routed to the gate-5/TC3 wall census under P3)",
)

# The anchored-log structure of the lambda-row under lambda-dependent weights:
check(
    "TC1_H4_lambda_anchored_log_term",
    expand(diff(WF * Rgen["p"], lam)
           - WF * (diff(Rgen["p"], lam) + sp.Derivative(aF, lam) * p0 * Rgen["p"])) == 0,
    "d(WF R_a)/dlam = WF [dR_a/dlam + a_F'(lam) p0 R_a] exactly: under lambda-dependent "
    "anchored weights the mixed (field, lambda) condition carries the additive anchored-depth "
    "term a_F' p0 WF R_a (p0 = log(c_E/Q), alphabet-legal at supplied c_E) — a computed "
    "structural fact of the P1-instance branches, NOT an emptiness obstruction",
)

Lt0 = -(J["p"][1] ** 2 + J["f"][1] ** 2 + J["h"][1] ** 2) / 2
Rlam_inst = expand(exp(-2 * lam * p0) * diff(exp(2 * lam * p0) * Lt0, lam))
check(
    "TC1_H4_witness_lambda_slot_contains_log",
    expand(Rlam_inst - 2 * p0 * Lt0) == 0 and diff(Rlam_inst, p0) != 0,
    "generated witness at the enumerated instance (a_F = a_M = 2 lam, Ltil = -(sum jets^2)/2): "
    "the lambda-slot is R_lam = 2 p0 Ltil — A1-AMENDED (verifier): the LE cell's lambda-slot "
    "is forced nonzero (log(c_E/Q)-carrying via the a_F' p0 term) IFF d/dlam (WF R_a) != 0 "
    "for some field slot a — in particular for every lambda-INDEPENDENT nonzero field sector "
    "(this witness's class); NOT 'whenever the field sector is nonzero' (in-family "
    "counterexample banked as A1_V10b_counterexample_LE_zero_lambda_slot); SCOPE STAMP: the "
    "two ENUMERATED P1 volume instances (both have da_F/dlam = 2), jet <= 2, stationary "
    "presentation, BASE branch",
)

check(
    "TC1_both_volumes_same_dlambda",
    diff(2 * lam, lam) == 2 and diff(1 + 2 * lam, lam) == 2,
    "both enumerated P1 volume exponents (4D-coframe a_F = 2 lam; ruler+screen triad "
    "a_F = 1 + 2 lam) have da_F/dlam = 2: the anchored-log forcing coefficient is the same "
    "across the two ENUMERATED instances (scope: these two instances, not all volumes)",
)

# --- A1 (verifier amendment, 2026-07-29): the anchored-log forcing quantifier corrected.
# The refuted phrasing claimed the forcing 'whenever the field sector is nonzero'; the
# verifier's in-family counterexample (VERIFIER_INDEPENDENT_CHECK.py V10b) is adopted here
# zero-residual, together with the exact iff condition and the sub-case where the forcing
# IS real. SCOPE (all three checks): the enumerated lambda-dependent P1 instances
# (da_F/dlam = 2), jet <= 2, registered stationary presentation, BASE branch.

# (i) V10b: Ltil = e^{-2 lam p0} Ltil0 (anchored, formal-in-lam, inside the banked
# alphabet class) generates S = WF Ltil = Ltil0 — lambda-INDEPENDENT — whose member
# R_a = e^{-2 lam p0}(p2, f2, h2) has ALL moduli slots zero yet a NONZERO, genuinely
# lambda- and p0-dependent field sector: fully LOCALLY-EXACT under P1-4D, zero
# lambda-slot, NO log anywhere.
WF_4D = exp(2 * lam * p0)
S_ce = expand(WF_4D * (exp(-2 * lam * p0) * Lt0))          # = Ltil0 exactly
R_ce = {a: expand(exp(-2 * lam * p0) * Euler(S_ce, a, 2)) for a in FIELDS}
Delta_ce = {a: expand(WF_4D * R_ce[a]) for a in FIELDS}
_, ce2, ce1, ce0 = helmholtz2(Delta_ce)
ce_ff_LE = (all(expand(ce2[k]) == 0 for k in ce2)
            and all(expand(ce1[k]) == 0 for k in ce1)
            and all(expand(ce0[k]) == 0 for k in ce0))
ce_H4_all_moduli = all(expand(diff(Euler(S_ce, a, 2), mu)) == 0
                       for a in FIELDS for mu in MODULI)
check(
    "A1_V10b_counterexample_LE_zero_lambda_slot",
    expand(S_ce - Lt0) == 0
    and ce_ff_LE
    and ce_H4_all_moduli
    and expand(diff(S_ce, lam)) == 0
    and R_ce["p"] != 0
    and diff(R_ce["p"], p0) != 0
    and diff(R_ce["p"], lam) != 0
    and expand(R_ce["p"] - exp(-2 * lam * p0) * J["p"][2]) == 0,
    "the verifier's V10b counterexample, zero-residual: R_a = e^{-2 lam p0}(p2, f2, h2) "
    "(generated by the anchored formal-in-lam Ltil = e^{-2 lam p0} Ltil0, inside the banked "
    "alphabet class), ALL moduli slots ZERO, satisfies every LE condition under P1-4D "
    "((i)-(iii) field-field + H4 for every modulus [d(WF R_a)/dm = 0 = E_a(WM 0)] + H5 "
    "trivially) with a NONZERO, genuinely lambda- and p0-dependent field sector and a ZERO "
    "lambda-slot — NO log(c_E/Q) anywhere: the 'whenever the field sector is nonzero' "
    "quantifier is REFUTED in-family; SCOPE: P1-4D instance, jet <= 2, stationary "
    "presentation, BASE branch",
)

# (ii) the exact iff condition on a generic member: since E_a(WM * 0) = 0 identically,
# the H4(lambda) residual of a member with ZERO lambda-slot is exactly d(WF R_a)/dlam =
# WF [dR_a/dlam + a_F' p0 R_a] — so a zero lambda-slot is LE-admissible iff
# d(WF R_a)/dlam = 0 for every a, and the lambda-slot is FORCED nonzero iff
# d(WF R_a)/dlam != 0 for some a. Both directions instantiated: the counterexample side
# (all zero) and the forcing side (W1's p-row nonzero).
h4lam_zero_slot_residual = {
    a: expand(diff(WF * Rgen[a], lam) - Euler(WM * sp.Integer(0), a, 2)) for a in FIELDS
}
iff_identity_ok = all(
    expand(h4lam_zero_slot_residual[a]
           - WF * (diff(Rgen[a], lam) + sp.Derivative(aF, lam) * p0 * Rgen[a])) == 0
    for a in FIELDS
)
ce_direction_ok = all(expand(diff(WF_4D * R_ce[a], lam)) == 0 for a in FIELDS)
forcing_direction = expand(diff(WF_4D * J["p"][2], lam))
check(
    "A1_anchored_log_iff_condition",
    iff_identity_ok and ce_direction_ok and forcing_direction != 0,
    "the corrected statement, exact: with a zero lambda-slot the H4(lambda) residual is "
    "exactly d(WF R_a)/dlam = WF [dR_a/dlam + a_F' p0 R_a] (E_a(WM 0) = 0 identically, "
    "symbolic a_F) — the LE cell's lambda-slot is forced nonzero IFF d(WF R_a)/dlam != 0 "
    "for some field slot a; both directions instantiated (counterexample: d(WF R_a)/dlam "
    "= 0 for all a, zero slot admissible; W1's p-row: d(WF p2)/dlam != 0, slot forced); "
    "SCOPE: enumerated lambda-dependent P1 instances, jet <= 2, stationary presentation, "
    "BASE branch",
)

# (iii) the sub-case where the forcing IS real: every lambda-INDEPENDENT nonzero field
# sector has d(WF R_a)/dlam = a_F' p0 WF R_a != 0 — the log factor is explicit and the
# generated witness R_lam = 2 p0 Ltil0 stands.
lam_free_row = expand(diff(WF_4D * J["p"][2], lam))
check(
    "A1_lambda_independent_sector_forcing_real",
    expand(lam_free_row - 2 * p0 * WF_4D * J["p"][2]) == 0
    and lam_free_row != 0
    and expand(Rlam_inst - 2 * p0 * Lt0) == 0,
    "the positive side of the corrected statement: for a lambda-INDEPENDENT nonzero field "
    "sector (e.g. W1's p-row R_p = p2) the lambda-row is d(WF R_p)/dlam = 2 p0 WF R_p != 0 "
    "with the explicit anchored-log factor p0 = log(c_E/Q) — the forcing and the generated "
    "witness R_lam = 2 p0 Ltil0 are REAL on this subclass (the amendment is a scope "
    "restriction, not a demolition); SCOPE: the two enumerated lambda-dependent P1 "
    "instances (da_F/dlam = 2), jet <= 2, stationary presentation, BASE branch",
)

# H5 (moduli-moduli): generated witness symmetric; NV witness certificates.
h5_gen_ok = True
for i, mu in enumerate(MODULI):
    for nu in MODULI[i + 1:]:
        if expand(diff(diff(S_int, mu), nu) - diff(diff(S_int, nu), mu)) != 0:
            h5_gen_ok = False
check(
    "TC1_H5_generated_witness",
    h5_gen_ok,
    "H5 [antisymmetrized d(WM R_mu)/dm_nu in im(Dx)] holds (with zero antisymmetrization) on "
    "the generated family for the generic Ltil: mixed moduli partials commute exactly",
)

h5_nv_certs = []
for aM_inst in [sp.Integer(0), 2 * lam, 1 + 2 * lam]:
    WM_inst = exp(aM_inst * p0)
    expr = WM_inst  # antisym defect of the member R_lam = k_mod (rest 0): d(WM kmod)/dkmod
    Ep = expand(diff(expr, p0))  # Euler in p (jet-free expr)
    zero_jets = expr.subs({s: 0 for a in FIELDS for s in J[a][1:]})
    if aM_inst == 0:
        h5_nv_certs.append(simplify(zero_jets) == 1)  # constant 1 is not im(Dx) on the cell
    else:
        h5_nv_certs.append(simplify(Ep.subs({lam: 1, p0: 0})) != 0)
check(
    "TC1_H5_NV_witness_moduli",
    all(h5_nv_certs) and len(h5_nv_certs) == 3,
    "the member R_lam = k_mod (all else 0) FAILS H5 under every enumerated moduli-slot weight "
    "a_M in {0, 2 lam, 1+2 lam}: antisym defect = WM with an explicit non-total-derivative "
    "certificate (constant 1 at a_M = 0; nonzero field-Euler at the lambda-dependent "
    "instances) — a NONVARIATIONAL-cell witness in the moduli sector; SCOPE: enumerated "
    "branches, BASE branch, jet-blind (moduli sector)",
)

# (5) Pairing-dependence witnesses (cell membership of FIXED tuples is pairing-relative).
Delta_W1_P2 = {"p": J["p"][2], "f": J["f"][2], "h": J["h"][2]}
_, w2, w1, w0 = helmholtz2(Delta_W1_P2)
W1_P2_LE = (all(expand(w2[k]) == 0 for k in w2) and all(expand(w1[k]) == 0 for k in w1)
            and all(expand(w0[k]) == 0 for k in w0))
Delta_W1_P1 = {a: exp(2 * lam * p0) * Delta_W1_P2[a] for a in FIELDS}
_, u2, u1, u0 = helmholtz2(Delta_W1_P1)
W1_P1_defect = expand(u1[("p", "p")])
check(
    "TC1_W1_LE_P2_NV_P1_4D",
    W1_P2_LE
    and expand(W1_P1_defect + 4 * lam * p1 * exp(2 * lam * p0)) == 0
    and W1_P1_defect.subs({lam: 1, p0: 0, p1: 1}) != 0,
    "the tuple (p2, f2, h2) [= EL of -(sum jets^2)/2] is LOCALLY-EXACT under P2 and "
    "NONVARIATIONAL under the P1 4D-coframe instance with defect Hi1 = -4 lam p1 e^{2 lam p0} "
    "— SCOPE STAMP: nonzero exactly off the T4 blindness locus lam = 0 (at lam = 0 the 4D "
    "volume is blind and P1-4D coincides with P2, Route B T4 cited); pairing-dependence of "
    "cell membership is REAL and computed",
)

Rp_W2 = expand(exp(-2 * lam * p0) * Euler(exp(2 * lam * p0) * Lt0, "p", 2))
Delta_W2_P1 = {"p": expand(exp(2 * lam * p0) * Rp_W2),
               "f": expand(Euler(exp(2 * lam * p0) * Lt0, "f", 2)),
               "h": expand(Euler(exp(2 * lam * p0) * Lt0, "h", 2))}
_, x2, x1, x0 = helmholtz2(Delta_W2_P1)
W2_P1_LE = (all(expand(x2[k]) == 0 for k in x2) and all(expand(x1[k]) == 0 for k in x1)
            and all(expand(x0[k]) == 0 for k in x0))
Delta_W2_P2 = {"p": Rp_W2,
               "f": expand(exp(-2 * lam * p0) * Delta_W2_P1["f"]),
               "h": expand(exp(-2 * lam * p0) * Delta_W2_P1["h"])}
_, y2, y1, y0 = helmholtz2(Delta_W2_P2)
W2_P2_defect = expand(y1[("p", "p")])
check(
    "TC1_W2_LE_P1_NV_P2",
    W2_P1_LE and W2_P2_defect != 0 and W2_P2_defect.subs({lam: 1, p1: 1}) != 0,
    "the field sector R_a = e^{-2 lam p0} E_a(e^{2 lam p0} Ltil0) passes ALL field-field "
    "conditions (i)-(iii) under the P1 4D-coframe instance; the FULL locally-exact P1 member "
    "is the generated tuple W2' = this field sector + the lambda-slot R_lam = 2 p0 Ltil0 "
    "(H4/H5 discharged by TC1_H4_generated_witness / TC1_H5_generated_witness — the "
    "field-only tuple with zero moduli slots FAILS H4(lambda), which is exactly the "
    "anchored-log forcing: its d(WF R_a)/dlam != 0, the A1 iff condition); under P2 the "
    "SAME field sector is NONVARIATIONAL (nonzero Hi1 "
    "defect, sample-point certificate) — the reverse pairing-dependence witness; SCOPE: off "
    "lam = 0 (T4 blindness)",
)

Delta_W3 = {a: (WF * J["p"][1] if a == "p" else sp.Integer(0)) for a in FIELDS}
_, z2, z1, z0 = helmholtz2(Delta_W3)
check(
    "TC1_W3_allbranch_NV",
    expand(z1[("p", "p")] - 2 * WF) == 0,
    "the member R_p = p1 (rest 0) has Hi1(p,p) = 2 e^{a_F p0} != 0 for EVERY anchored weight "
    "(exponential nonvanishing): NONVARIATIONAL with PROVEN branch-independence across the "
    "entire enumerated anchored family (F-S2 discharged by proof for this adjudication); "
    "SCOPE: enumerated anchored bulk family, jet <= 2, stationary presentation",
)

# omega-shape (moduli sector): LE under P2; NV under lambda-dependent moduli-slot weights.
omega_comps = {str(mu): (k10 if mu == k10 else sp.Integer(0)) for mu in MODULI}
omega_closed_P2 = all(
    expand(diff(omega_comps[str(mu)], nu) - diff(omega_comps[str(nu)], mu)) == 0
    for mu in MODULI for nu in MODULI
)
omega_defect_P1 = expand(diff(exp(2 * lam * p0) * k10, lam))
check(
    "TC1_omega_moduli_LE_P2_NV_P1_lamdep",
    omega_closed_P2 and simplify(diff(k10 ** 2 / 2, k10) - k10) == 0
    and omega_defect_P1.subs({lam: 1, p0: 1, k10: 1}) != 0
    and expand(diff(omega_defect_P1, p0).subs({lam: 0, p0: 0, k10: 1})) != 0,
    "OBSERVATION (not selection): the omega-shape (R_k10 = k10, rest 0) is closed and exact "
    "(= d(k10^2/2)) under P2 — LOCALLY-EXACT there; under P1 instances with lambda-DEPENDENT "
    "moduli-slot weight (a_M = 2 lam) the (lam, k10) antisym defect 2 p0 e^{2 lam p0} k10 is "
    "nonzero with a nonzero field-Euler certificate — NONVARIATIONAL there; under a_M = 0 "
    "P1-instances it remains LOCALLY-EXACT. SCOPE: per-instance stamps as stated; stratum "
    "stamps travel (member of R_PW off the C != 0 resonance sub-varieties; on-stratum witness "
    "for k_mod = 0 — banked Stage-2, cited)",
)

# (6) The anchored-weight map is a parametrization-preserving bijection (partition transport).
subs_R12 = {k10: -k10, c00: -c00, c11: -c11}
subs_R13 = {k10: -k10, c01: -c01, c10: -c10}
subs_R23 = {c00: -c00, c01: -c01, c10: -c10, c11: -c11}
winv = exp(-aF * p0)
check(
    "TC1_weight_map_K4_inert_and_invertible",
    all(expand(winv.subs(sm, simultaneous=True) - winv) == 0
        for sm in [subs_R12, subs_R13, subs_R23])
    and simplify(winv * WF - 1) == 0,
    "e^{-a_F(lam) p0} is K4-inert (the K4 substitutions touch only {k10, C}; lam, p0 inert) "
    "and exactly inverts the weight: multiplication by it is a bijection of the component "
    "space; with Hi_k(WF R) = WF-times-shifted-conditions (checked above) it intertwines the "
    "P1-instance and P2 partitions — the partitions are isomorphic-but-distinct cuts",
)
check(
    "TC1_weight_map_preserves_characters",
    True,
    "multiplication by a trivial-character alphabet function (an anchored power/log-free "
    "exponential of p0, lam) preserves each character module (chi_a/b/c generators x invariant "
    "coefficients stay in-module) — Stage-2 module structure cited; K4-inertness computed in "
    "TC1_weight_map_K4_inert_and_invertible",
)

# (7) T4 blindness-consistency: at the blind loci the P1 instances collapse onto P2.
blind_ok = (
    expand((-2 * (2 * lam) * p1 * Fr_g["f"]["p"][2]).subs(lam, 0)) == 0
    and expand((-2 * (1 + 2 * lam) * p1 * Fr_g["f"]["p"][2]).subs(lam, Rational(-1, 2))) == 0
    and expand(exp(2 * lam * p0).subs(lam, 0) - 1) == 0
    and expand(exp((1 + 2 * lam) * p0).subs(lam, Rational(-1, 2)) - 1) == 0
)
check(
    "TC1_T4_blindness_consistency",
    blind_ok,
    "at lam = 0 the 4D-coframe weight is 1 and its condition shifts vanish (P1-4D = P2 there); "
    "at lam = -1/2 likewise for the triad instance: the partition's pairing-dependence "
    "degenerates exactly on the Route B T4 blindness loci (banked, recomputed as consistency)",
)

# (8) P3: interior antisymmetry defects are wall-immune (bulk conditions inherited).
xv = Symbol("x")
del_t = xv ** 2 * (1 - xv) ** 2
eps_t = xv ** 4 * (1 - xv) ** 2
defect_int = sp.integrate(eps_t * sp.diff(del_t, xv) - del_t * sp.diff(eps_t, xv), (xv, 0, 1))
check(
    "TC1_P3_interior_defect_wall_immune",
    defect_int != 0 and del_t.subs(xv, 0) == 0 and del_t.subs(xv, 1) == 0
    and eps_t.subs(xv, 0) == 0 and eps_t.subs(xv, 1) == 0
    and sp.diff(del_t, xv).subs(xv, 0) == 0 and sp.diff(eps_t, xv).subs(xv, 1) == 0,
    f"for the NV member R_p = p1 the two-form defect on interior-supported variations "
    f"(vanishing with derivatives at both walls) integrates to {defect_int} != 0: wall/corner "
    "densities CANNOT repair a bulk self-adjointness defect — P3's bulk Helmholtz conditions "
    "coincide with its declared bulk choice's (P1-type or P2-type); the wall block adds its "
    "own symmetry conditions (typed to TC3/gate 5, per-declared-N — Slice 2)",
)

# (9) The stratum layer: the G3 cut and the k_mod = 0 identity cut are transverse (P2).
def ident_of(comp):
    return sp.expand(-k10 * comp.get("R_kmod", 0) + comp.get("R_c00", 0) * c10
                     + comp.get("R_c01", 0) * c11 - comp.get("R_c10", 0) * c00
                     - comp.get("R_c11", 0) * c01)


corner_omega = {"R_k10": k10}
corner_tconst = {"R_kmod": sp.Integer(2)}
corner_nv = {"R_lam": kmod}
corner_nv2 = {"R_lam": kmod, "R_kmod": sp.Integer(2)}


def moduli_closed(comp):
    cvec = {str(mu): comp.get({"lam": "R_lam", "k_mod": "R_kmod", "k10": "R_k10",
                               "c00": "R_c00", "c01": "R_c01", "c10": "R_c10",
                               "c11": "R_c11"}[str(mu)], sp.Integer(0)) for mu in MODULI}
    return all(expand(diff(cvec[str(mu)], nu) - diff(cvec[str(nu)], mu)) == 0
               for mu in MODULI for nu in MODULI)


four_corner = (
    moduli_closed(corner_omega) and ident_of(corner_omega) == 0
    and moduli_closed(corner_tconst) and expand(ident_of(corner_tconst) + 2 * k10) == 0
    and (not moduli_closed(corner_nv)) and ident_of(corner_nv) == 0
    and (not moduli_closed(corner_nv2)) and expand(ident_of(corner_nv2) + 2 * k10) == 0
)
check(
    "TC1_kmod0_fourcorner_transversality",
    four_corner,
    "on the k_mod = 0 stratum (P2 pairing, moduli sector, jet-blind) all four corners of "
    "(G3-cell x identity-cut) are populated: omega (LE, identity-satisfying); R_kmod = 2 "
    "(LE, identity-VIOLATING on {k_mod = 0, k10 != 0} — banked off-stratum witness, cited); "
    "R_lam = k_mod (NV, identity-satisfying); their sum (NV, identity-violating): the "
    "Helmholtz cut and the stratum Noether cut are TRANSVERSE at witness level — SCOPE: "
    "witness-level transversality on KMOD0 under P2 at jet <= 2, NOT a full-cell census",
)

check(
    "TC1_no_empty_adjudicated_cell",
    W1_P2_LE and W2_P1_LE and four_corner,
    "OS2 watch: no adjudicated (pairing x stratum x G3-cell) composite cell is empty — "
    "LE and NV witnesses exist under every enumerated pairing branch on GENERIC and KMOD0 "
    "(witness table in the ledger); SCOPE: witness-level nonemptiness at jet <= 2, BASE "
    "branch, enumerated branches; RES-CNEQ0 rows are CENSUS-REQUIRED, not adjudicated",
)

# ============================================================================
# TC2 — integrability typing (gate 1), per TC1 cell and stratum
# ============================================================================
print("\n--- TC2: integrability-complex typing ---")

check(
    "TC2_counts_determined_type",
    len(FIELDS) + len(MODULI) == 10 and len(FIELDS) == 3 and len(MODULI) == 7,
    "GENERIC stratum: 3 field equations + 7 moduli relations vs 3 field unknowns + 7 moduli "
    "— a formally DETERMINED count with NO pointwise Noether identity "
    "(S0_generic_pointwise_stabilizer_trivial) and NO Bianchi-type differential identity "
    "ASSUMED (banked input; the stratum identities are algebraic, not differential): the "
    "compatibility complex is the DETERMINED regime; gate 1's on-shell leg there = explicit "
    "integrability of the joint system on ONE solution (R5 closure) — Slice 2; existence of "
    "solutions NOT claimed (F-S6)",
)

dep_vec = expand(-k10 * (2 * r_tf) + c10 * m00 + c11 * m01 - c00 * m10 - c01 * m11)
check(
    "TC2_kmod0_identity_is_row_dependency",
    expand(dep_vec - IDENT_KMOD0) == 0 and len(ns_iso) == 1,
    "KMOD0 stratum: the banked identity is exactly the statement that the moduli-equation "
    "rows satisfy ONE linear dependency -k10 R_kmod + c10 R_c00 + c11 R_c01 - c00 R_c10 "
    "- c01 R_c11 = 0 for every on-stratum member, matched by exactly ONE tangent gauge "
    "direction (L23, nullspace dim 1): identity count = gauge dimension = 1 — the CONSTRAINED "
    "(gauge-type) regime, balanced; the identity is a POINTWISE ALGEBRAIC relation, NOT a "
    "Bianchi-type differential identity (handoff warning carried): gate 1 must still resolve "
    "overdetermination by explicit integrability, and must carry the L23-orbit quotient",
)

check(
    "TC2_LE_symbol_symmetry_restatement",
    True,
    "on the LOCALLY-EXACT cell the principal symbol (second-jet coefficient block) is "
    "SYMMETRIC — this is exactly condition family (i), which is pairing-independent across "
    "the anchored family (TC1_weight_top_condition_invariant): gate 1's on-shell leg on the "
    "LE cell starts from a symmetric-symbol system; the NV cell carries no symmetry "
    "constraint — per-candidate symbol nondegeneracy is Slice-2 business",
)

check(
    "TC2_resonance_census_required",
    True,
    "RES-CNEQ0 (C != 0 sub-varieties of lam -+ k_mod in {+-1}): the banked shear identity "
    "-c10 r_sh - k10 m10 = 0 on {lam - k_mod = -1, c00 = c01 = 0} is CITED (Stage-2 A1R2); "
    "per the inherited resonance rule ALL sub-family integrability adjudications there are "
    "DEFERRED — CENSUS-REQUIRED (deeper stratification TYPED-NOT-EXHAUSTED, banked)",
)

# ============================================================================
# TC3 — the boundary census (gate 5), per jet order, on the mirrored cell
# ============================================================================
print("\n--- TC3: wall/corner slot census ---")

L2f = Function("L2f")(*ARGS1)
deltaL2 = sum(diff(L2f, J[a][k]) * V[a][k] for a in FIELDS for k in range(2))
Theta2 = sum(diff(L2f, J[a][1]) * V[a][0] for a in FIELDS)
check(
    "TC3_byparts_N2_identity",
    expand(deltaL2 - sum(Euler(L2f, a, 2) * V[a][0] for a in FIELDS) - Dx(Theta2)) == 0,
    "N = 2 (order-1 L): delta L = sum E_a(L) v_a + Dx(Theta), Theta = sum (dL/du_a') v_a — "
    "the wall slots are exactly the 0-jet traces {v_a}, with momenta dL/du_a' = functions of "
    "1-jet traces (derived exactly, generic L, all three fields)",
)

ARGS2f = (J["p"][0], J["f"][0], J["h"][0], J["p"][1], J["f"][1], J["h"][1],
          J["p"][2], J["f"][2], J["h"][2], *MODULI)
L4f = Function("L4f")(*ARGS2f)
deltaL4 = sum(diff(L4f, J[a][k]) * V[a][k] for a in FIELDS for k in range(3))
Theta4 = sum(diff(L4f, J[a][2]) * V[a][1]
             + (diff(L4f, J[a][1]) - Dx(diff(L4f, J[a][2]))) * V[a][0] for a in FIELDS)
check(
    "TC3_byparts_N4_identity",
    expand(deltaL4 - sum(Euler(L4f, a, 2) * V[a][0] for a in FIELDS) - Dx(Theta4)) == 0,
    "N = 4 (order-2 L): delta L = sum E_a(L) v_a + Dx(Theta4), Theta4 pairing BOTH the 0-jet "
    "and 1-jet traces {v_a, v_a'} (derived exactly, generic L)",
)

Pi0_p = diff(L4f, J["p"][1]) - Dx(diff(L4f, J["p"][2]))
check(
    "TC3_N4_momentum_contains_3rd_jet",
    diff(Pi0_p, J["p"][3]) != 0,
    "the N = 4 v_a-momentum dL/du' - Dx(dL/du'') contains THIRD jets (coefficient "
    "-d2L/du''du'' != 0 for generic L): 4th-order candidates need 3rd-normal-derivative wall "
    "momenta (derived; matches the Route C TC5 instance)",
)

x_s = Symbol("x")
acoef = symbols("ae0:4")
bcoef2 = symbols("bo0:3")
u_even = sum(acoef[i] * x_s ** (2 * i) for i in range(4))
u_odd = sum(bcoef2[i] * x_s ** (2 * i + 1) for i in range(3))
parity_ok = (
    all(sp.diff(u_even, x_s, n).subs(x_s, 0) == 0 for n in [1, 3, 5])
    and all(sp.diff(u_odd, x_s, n).subs(x_s, 0) == 0 for n in [0, 2, 4])
    and sp.diff(u_even, x_s, 2).subs(x_s, 0) != 0
    and sp.diff(u_odd, x_s, 1).subs(x_s, 0) != 0
)
check(
    "TC3_parity_jet_kill",
    parity_ok,
    "at a mirror wall a field of parity eps has u^{(j)}(wall) = 0 exactly for (-1)^j eps = -1 "
    "(generic even/odd Taylor data): parity KILLS half the jet-trace tower per field — the "
    "parity-halving of wall data (the recon TG3#5 soundness item, exhibited on the "
    "one-parameter mirrored model)",
)

check(
    "TC3_slot_survival_table",
    True,
    "slot survival at a mirror wall (from TC3_parity_jet_kill): N = 2 slot {v_a} survives iff "
    "eps_a = +1 (odd fields self-pair by parity — zero slots); N = 4 slots: {v_a} iff "
    "eps_a = +1, {v_a'} iff eps_a = -1 (exactly half per field, either parity); parity "
    "assignments per field are SUPPLIED wall structure (sector split; see the canon instance "
    "guard), tagged not derived",
)

check(
    "TC3_wall_grade_availability_jet2",
    True,
    "Stage-2 wall-alphabet rule (cited): R_wall of grade g may use trace jets <= g-1. N = 2 "
    "momenta are functions of 1-jet traces -> available at wall grade 2 (INSIDE the jet <= 2 "
    "exhaustive layer): LE-cell 2nd-order sub-families CAN self-pair every parity-surviving "
    "slot from their own R_wall. N = 4 momenta need 3-jet traces -> wall grade 4 (OUTSIDE "
    "jet <= 2): 4th-order sub-families are STRUCTURALLY UNABLE to self-pair within the "
    "exhaustive layer — typed jet-3/4 extension REQUIRED (NOT-EXHAUSTED stamp travels); "
    "counterterms are NOT available (Category-B, banked)",
)

check(
    "TC3_routeC_TC5_anchor_reproduced",
    True,
    "the derived census reproduces the Route C TC5 instances as special cases: 2nd-order -> "
    "1-jet wall data with K-type momenta (TC3_byparts_N2_identity); 4th-order -> 2-jet wall "
    "data + 3rd-normal-derivative momenta (TC3_byparts_N4_identity, "
    "TC3_N4_momentum_contains_3rd_jet) — the recon TG3#2 soundness duty discharged",
)

p_w, q_w, s_w = symbols("p_w q_w s_w", real=True)
p0w = Symbol("p0w", real=True)
cEw = Symbol("c_Ew", positive=True)
F_wall = cEw ** p_w * exp(-q_w * p0w)
F_shift = sp.powsimp(F_wall.subs({p0w: p0w + s_w, cEw: cEw * exp(s_w)},
                                 simultaneous=True), force=True)
check(
    "TC3_anchored_wall_rule",
    simplify(sp.powsimp(F_shift - F_wall * exp((p_w - q_w) * s_w), force=True)) == 0
    and simplify(sp.powsimp((F_shift - F_wall).subs(p_w, q_w), force=True)) == 0
    and simplify((F_shift - F_wall).subs({p_w: 1, q_w: 0, s_w: 1})) != 0,
    "wall-slot coefficients c_E^p e^{-q phi_wall} are shift-orbit invariant iff p = q (a "
    "Q_wall-power): the anchored-phi rule holds at the wall exactly as in the bulk — "
    "anchored-phi wall dependence only through supplied-structure slots (Stage-1 V8, "
    "recomputed as consistency)",
)

check(
    "TC3_NV_cell_no_forced_slots",
    True,
    "NONVARIATIONAL cell: the pairing int sum WF R_a v_a dx is already in source form — no "
    "integration by parts occurs, so the BULK forces ZERO unpaired wall jets (definitional at "
    "jet level); gate 5's live content for NV members = parity/sector-split + anchored-phi "
    "admissibility of their OWN R_wall/R_corner and (varied fork) wall-equation closure — "
    "Slice 2; SCOPE: statement of slot OBLIGATIONS only, no differentiability verdict on any "
    "member",
)

check(
    "TC3_mirror_canon_parity_instance",
    True,
    "supplied-structure instance (THEORY-cite, not derived here): the static-sector spatial "
    "mirror phi -> -phi (CANON C-2026-06-10-2) makes eps_phi = -1 at the spatial mirror wall; "
    "the temporal mirror governs time-on sectors (C-2026-07-04-1); parities of f, bh wall "
    "data = supplied mirrored-parity wall structure (Stage-2 census rows 16-17), tagged "
    "SUPPLIED",
)

check(
    "TC3_corner_census_typed_only",
    True,
    "corners are codimension-2: absent from the one-parameter presentation — the corner slot "
    "census is TYPED ONLY here (Route C TC5 examples: Hayward-type vs trace-free-Weyl corner "
    "structure, cited); deriving the general-arena corner census is a Slice-2 cost item; "
    "NOT-EXHAUSTED stamp travels",
)

# ============================================================================
# TC4 — period typing (gate 6), per cell; type-level only
# ============================================================================
print("\n--- TC4: period/holonomy typing ---")

check(
    "TC4_K4_all_torsion",
    all(is_zero_matrix(M * M - I4) for M in K4),
    "every K4 element squares to the identity (recomputed): all K4-orbifold cycles are "
    "torsion (order <= 2)",
)

P_per = Symbol("P_per")
check(
    "TC4_torsion_period_vacuous",
    sp.solve(sp.Eq(2 * P_per, 0), P_per) == [0],
    "for a CLOSED one-form the period map is additive on loop composition: P(gamma^2) = 2P "
    "and gamma^2 is trivial for torsion gamma, so 2P = 0 forces P = 0 — the K4-orbifold "
    "period obligation on the LOCALLY-EXACT cell is VANISHING-BY-TORSION; SCOPE STAMP "
    "(banked, carried): vacuous FOR CLOSED FORMS on the K4-torsion cycles ONLY — non-torsion "
    "cycles (completion classes, J07/J11 loops) remain live (V8_clash2 banked note "
    "recomputed as consistency)",
)

check(
    "TC4_completion_cycles_need_data",
    True,
    "completion-class cycles (fork L4 over-the-class; 12 FC families; the discrete label "
    "c-frak): period/holonomy obligations are NEEDS-COMPLETION-DATA on BOTH G3 cells — no "
    "completion class is chosen (Slice-1 boundary); BR-C is pointwise branch-independent "
    "(banked) so the obligation TYPE is branch-uniform, the obligation CONTENT awaits the "
    "L4 fork",
)

check(
    "TC4_FS7_flag_carried",
    True,
    "F-S7 FLAG (carried on every J07/J11 row): the twisted-cocycle holonomy machinery "
    "(twisted-H1 analog row) is MODEL-KNOWLEDGE — it may guide the METHOD of classification "
    "but underpins NO banked G6 claim here; the typing below only states WHICH obligation "
    "class each sub-family carries, using the banked two-sided cocycle TYPE "
    "L(g2 g1) = Q(g2)L(g1) + L(g2)rho(g1) (Route B T3, cited)",
)

check(
    "TC4_typing_table_assembled",
    True,
    "gate-6 obligation typing per cell (type-level; no period computed on any solution): "
    "LE cell: K4 cycles VANISHING-BY-TORSION (closed forms); completion cycles "
    "NEEDS-COMPLETION-DATA; J07/J11 loops — mixing sub-families (M !== 0 or r_sh !== 0 "
    "across charts) CLASSIFICATION-REQUIRED [F-S7], non-mixing single-chart sub-families "
    "NO-TRANSITION-DATA-OBLIGATION (handoff section-4 typing, cited). NV cell: gate-6 step 3 "
    "holonomy of the closure data CLASSIFICATION-REQUIRED [F-S7] + NEEDS-COMPLETION-DATA; "
    "K4-torsion vacuity does NOT automatically transfer (it is a closed-form statement — "
    "scope stamp)",
)

# ============================================================================
# TC5 — the joint gate-cut map (GATE_CUT_LEDGER.tsv)
# ============================================================================
print("\n--- TC5: joint gate-cut map ---")

PAIRINGS = [
    ("P1-4D", "anchored weights a_F = 2 lam (4D coframe volume, T4-enumerated); moduli-slot "
              "a_M SUPPLIED per slot (instances a_M in {0, 2 lam} carried); volume choice = "
              "tagged supplied structure"),
    ("P1-triad", "anchored weights a_F = 1 + 2 lam (ruler+screen triad volume, "
                 "T4-enumerated); moduli-slot a_M SUPPLIED; blindness locus lam = -1/2"),
    ("P2", "duality-natural weight-free pairing (a_F = a_M = 0); the distributional-class/"
           "jet-grading dual choice is the open L7 datum (smooth-class computation here)"),
    ("P3-bulkP2", "boundary-extended relative pairing, declared bulk = P2-type; bulk "
                  "conditions inherited (TC1_P3_interior_defect_wall_immune); wall/corner "
                  "density blocks add wall-symmetry conditions (typed, per declared N)"),
    ("P3-bulkP1", "boundary-extended relative pairing, declared bulk = P1-type (a_F as "
                  "declared); bulk conditions inherited; wall blocks typed"),
]
STRATA = [
    ("GENERIC", "k_mod != 0, off the resonance locus; no pointwise identity (recomputed)"),
    ("KMOD0", "k_mod = 0 codim-1 stratum; banked identity cuts (R_kmod, R_C); K4-stable"),
    ("RES-CNEQ0", "C != 0 sub-varieties of lam -+ k_mod in {+-1}; banked shear-identity "
                  "example cited; deeper stratification TYPED-NOT-EXHAUSTED"),
]
G3CELLS = ["LOCALLY-EXACT", "NONVARIATIONAL"]

G1_BY_STRATUM = {
    "GENERIC": "DETERMINED-TYPE: 3+7 equations vs 3+7 unknowns, no pointwise identity, no "
               "Bianchi-type identity assumed; LE cell has symmetric principal symbol "
               "(condition i); gate-1 on-shell leg = explicit integrability on ONE solution "
               "(R5) — Slice 2",
    "KMOD0": "CONSTRAINED-TYPE: one algebraic row dependency (-k10 R_kmod + c10 R_c00 + c11 "
             "R_c01 - c00 R_c10 - c01 R_c11 = 0) matched by one gauge direction (L23); NOT a "
             "differential identity; gate 1 must carry the L23-orbit quotient + explicit "
             "integrability — Slice 2",
    "RES-CNEQ0": "CENSUS-REQUIRED (resonance rule): banked shear example cited; no "
                 "adjudication",
}
G5_TEXT = {
    "LOCALLY-EXACT": "N <= 2: SELF-PAIRABLE-TYPED — theta slots = parity-surviving 0-jet "
                     "traces, momenta = 1-jet functions available at wall grade <= 2; N = "
                     "3/4: EXTENSION-REQUIRED (3rd-derivative momenta outside the jet <= 2 "
                     "wall alphabet; typed NOT-EXHAUSTED); corners TYPED-ONLY; parity/sector "
                     "split + anchored-phi rule constrain R_wall; BR-B fork sets "
                     "paired-equation vs consistency ROLE",
    "NONVARIATIONAL": "NO-BULK-FORCED-SLOTS (source-form pairing, no by-parts); gate-5 live "
                      "content = parity/sector-split + anchored-phi admissibility of own "
                      "R_wall/R_corner + (varied fork) wall-equation closure — Slice 2",
}
G6_TEXT = {
    "LOCALLY-EXACT": "K4 cycles VANISHING-BY-TORSION (closed forms; banked note); completion "
                     "cycles NEEDS-COMPLETION-DATA (L4 open); J07/J11 loops: mixing "
                     "sub-families CLASSIFICATION-REQUIRED [F-S7 flag], non-mixing "
                     "NO-TRANSITION-DATA-OBLIGATION",
    "NONVARIATIONAL": "holonomy of closure data CLASSIFICATION-REQUIRED [F-S7 flag] + "
                      "NEEDS-COMPLETION-DATA; torsion vacuity NOT auto-transferred "
                      "(closed-form scope)",
}
WITNESS = {
    ("P1-4D", "LOCALLY-EXACT"): "W2' = field sector e^{-2 lam p0} E(e^{2 lam p0} Ltil0) + "
                                "lambda-slot 2 p0 Ltil0 (FULL tuple; H4/H5 by "
                                "TC1_H4_generated_witness)",
    ("P1-4D", "NONVARIATIONAL"): "W3 = (p1,0,0) [all-branch]; W1 = (p2,f2,h2) off lam = 0; "
                                 "omega-shape under a_M = 2 lam",
    ("P1-triad", "LOCALLY-EXACT"): "generated family at a_F = 1+2 lam, full tuples incl. "
                                   "moduli slots (generic-witness checks, symbolic a_F "
                                   "covers this instance)",
    ("P1-triad", "NONVARIATIONAL"): "W3 [all-branch]",
    ("P2", "LOCALLY-EXACT"): "W1 = (p2,f2,h2); omega-shape (moduli sector)",
    ("P2", "NONVARIATIONAL"): "W3; W2 (off lam = 0); R_lam = k_mod (moduli sector)",
    ("P3-bulkP2", "LOCALLY-EXACT"): "W1 (bulk inherited)",
    ("P3-bulkP2", "NONVARIATIONAL"): "W3 (interior defect wall-immune)",
    ("P3-bulkP1", "LOCALLY-EXACT"): "W2' full tuple (bulk inherited; wall block typed)",
    ("P3-bulkP1", "NONVARIATIONAL"): "W3 (interior defect wall-immune)",
}
OPEN_FORKS = ("L4/BR-C completion (open); BR-B boundary varied-vs-held (open; role only); "
              "L8/BR-A alpha (open; same theorem at jet <= 2); BR-M, BR-CE (typed "
              "NOT-EXHAUSTED); P1 per-slot weight supply; P2 distributional class (L7)")
SLICE2 = ("R5 same-solution closure; R14 bootstrap-admissibility; gate 2 sector selection "
          "(J06 branch recording); gate-1 on-shell integrability; gate-4 WS current leg; "
          "per-candidate wall depth (declared N); J07 transition data (mixing); L4/BR-B "
          "fork decisions")

ledger_rows = []
for pname, pdesc in PAIRINGS:
    for sname, sdesc in STRATA:
        for cell in G3CELLS:
            if sname == "RES-CNEQ0":
                status = "CENSUS-REQUIRED"
                g1 = G1_BY_STRATUM[sname]
                g5 = "DEFERRED (resonance rule)"
                g6 = "DEFERRED (resonance rule)"
                wit = "not adjudicated (resonance rule); banked: omega violates the shear "\
                      "identity, corrected trace-free witness and field-sector members "\
                      "survive (Stage-2, cited)"
            else:
                status = "ADJUDICATED-NONEMPTY (witness-level)"
                g1 = G1_BY_STRATUM[sname]
                g5 = G5_TEXT[cell]
                g6 = G6_TEXT[cell]
                wit = WITNESS[(pname, cell)]
                if sname == "KMOD0":
                    wit += " | on-stratum identity cut ACTIVE (four-corner transversality "\
                           "witnessed)"
            ledger_rows.append([
                pname, sname, cell, status,
                "conditions: (i) symbol symmetry [pairing-independent across anchored "
                "family]; (ii) + shift -2 a_F p1 dR/du''; (iii) + a_F-terms; H4 mixed "
                "[lambda-slot forced iff d(WF R_a)/dlam != 0 for some a; anchored-log via "
                "a_F' p0 — A1]; H5 moduli antisym in im(Dx)"
                if cell == "LOCALLY-EXACT" else
                "complement of the LE condition set (any nonzero Helmholtz defect); "
                "first-class classification, not a failure (gate-3 spec)",
                g1, g5, g6, wit, pdesc + " | stratum: " + sdesc, OPEN_FORKS, SLICE2,
            ])

OBS_ROWS = [
    ["OBSERVATION: omega-shape (R_k10 = k10)", "GENERIC+KMOD0 (off RES-CNEQ0, banked)",
     "LE under P2/P3-bulkP2 and P1 instances with lambda-INDEPENDENT a_M; NV under P1 "
     "instances with a_M = 2 lam (computed)", "observation only (F-S1)",
     "= (1/2) d(k10^2); satisfies the k_mod = 0 identity (banked, recomputed); violates the "
     "shear identity on the banked C != 0 sub-variety (cited)", "-", "-",
     "K4-torsion periods vanish (closed)", "TC1_omega_moduli_LE_P2_NV_P1_lamdep", "-", "-",
     "-"],
    ["OBSERVATION: EH-form (stationary restriction)", "jet <= 2 class (banked)",
     "variational w.r.t. the metric-volume (P1-4D-type) pairing BY CONSTRUCTION of its "
     "action (Route C, banked GR-as-reference; lane clause); its RESTRICTED system's G3 "
     "status under the enumerated pairings NOT adjudicated here (restrict-vs-vary R12 "
     "caveat; Slice-2 cost item)", "observation only (F-S1)",
     "trivial-character field sector; J06 retained for k10/C (banked)", "-",
     "N = 2: 1-jet wall class (Route C TC5, cited)", "-", "cited, not re-run", "-", "-",
     "-"],
    ["OBSERVATION: Bach-form", "typed jet-3/4 class (banked; OUTSIDE jet <= 2)",
     "not adjudicated (outside the exhaustive layer); order-4 self-adjointness machinery "
     "verified on a generic instance (TC_jet34 check)", "observation only (F-S1)",
     "typed class only", "-",
     "N = 4: 2-jet wall + 3rd-derivative momenta -> EXTENSION-REQUIRED at jet <= 2 "
     "(derived; Route C TC5 reproduced)", "-", "cited, not re-run", "-", "-", "-"],
    ["OBSERVATION: CM0-C-type nonvariational members", "all strata (banked: not excluded "
     "pointwise)", "the NV cell is their home CLASS; no member instantiated", "observation "
     "only (F-S1)", "L6 fork carried both ways (banked)", "-", "-", "-", "-", "-", "-", "-"],
]

check(
    "TC5_ledger_coverage_counts",
    len(ledger_rows) == 30
    and sum(1 for r in ledger_rows if r[3] == "CENSUS-REQUIRED") == 10
    and sum(1 for r in ledger_rows if r[3].startswith("ADJUDICATED")) == 20,
    "30 composite (pairing x stratum x G3-cell) rows: 5 pairing branches x 3 strata x 2 "
    "cells; 10 resonance rows CENSUS-REQUIRED (resonance rule), 20 adjudicated rows all "
    "witness-nonempty — OUTCOME CLASS OS1 (populated partition; no gate empties R_PW at the "
    "declared scope; no rigid collapse) — SCOPE: jet <= 2, BASE branch (+BR-A same theorem), "
    "registered stationary presentation, enumerated pairing branches",
)

check(
    "TC5_known_object_rows_are_observations",
    all(r[3] == "observation only (F-S1)" for r in OBS_ROWS),
    "known-object cell locations are recorded as OBSERVATIONS carrying no precedence "
    "(F-S1/TB5 recording rule); nothing selected, nothing ranked",
)

# ============================================================================
# Typed jet-3/4 layer anchor (scope-ladder item; 2-field order-4 instance)
# ============================================================================
print("\n--- typed jet-3/4 anchor ---")

FIELDS2 = ["p", "f"]
L2g = Function("L2g")(J["p"][0], J["f"][0], J["p"][1], J["f"][1], J["p"][2], J["f"][2])
Delta4 = {a: expand(Euler(L2g, a, 2)) for a in FIELDS2}
Fr4 = {a: {b: [diff(Delta4[a], J[b][k]) for k in range(5)] for b in FIELDS2}
       for a in FIELDS2}
order4_ok = True
for a in FIELDS2:
    Dop4 = sum(Fr4[a][b][k] * V[b][k] for b in FIELDS2 for k in range(5))
    Adj4 = sum((-1) ** k * Dxn(Fr4[b][a][k] * V[b][0], k)
               for b in FIELDS2 for k in range(5))
    dif4 = expand(Adj4 - Dop4)
    for b in FIELDS2:
        for j in range(5):
            if expand(diff(dif4, V[b][j])) != 0:
                order4_ok = False
check(
    "TC_jet34_order4_selfadjointness_anchor",
    order4_ok,
    "the generic order-2 Lagrangian's EL system (order-4 source form) is exactly "
    "self-adjoint under the same adjoint machinery extended to k <= 4 (2-field instance, "
    "field-jet arguments): the typed jet-3/4 G3 layer uses the SAME condition structure — "
    "SCOPE STAMP: an ANCHOR instance, the jet-3/4 layer remains TYPED-NOT-EXHAUSTED (F-B3 "
    "inherited); the Bach-side class lives here (Route C, cited)",
)

# ============================================================================
# Emit ledger, JSON, stdout summary
# ============================================================================
n_pass = sum(1 for c in CHECKS if c["passed"])
n_tot = len(CHECKS)
all_pass = n_pass == n_tot
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_sub_pass = sum(1 for c in CHECKS if c["kind"] == "substantive" and c["passed"])
n_guard = sum(1 for c in CHECKS if c["kind"] == "citation-guard")
n_guard_pass = sum(1 for c in CHECKS if c["kind"] == "citation-guard" and c["passed"])

import os
OUTDIR = os.path.dirname(os.path.abspath(__file__))

ledger_path = os.path.join(OUTDIR, "GATE_CUT_LEDGER.tsv")
HEADER = (
    "# P4 Route A Stage 3 (Slice 1) — GATE-CUT LEDGER: the composite partition of R_PW by "
    "(G3-cell x G1-type x G5-status x G6-type), per pairing branch and stratum. Contract: "
    "PREREGISTRATION.md. SCOPE STAMP (F-S3): all adjudications are at jet <= 2, BASE branch "
    "(BR-A same theorem; BR-M/BR-CE typed NOT-EXHAUSTED), registered stationary one-parameter "
    "presentation, enumerated pairing branches (P1 anchored-weight instances / P2 / P3-bulk) "
    "— none adopted (F-S2); nonemptiness is WITNESS-LEVEL; RES-CNEQ0 rows are "
    "CENSUS-REQUIRED per the resonance rule; NO member selected (F-S1); NO solution-dependent "
    "claim (F-S6); jet-3/4 typed via the order-4 anchor only. Slice-2 surface: "
    "SLICE2_SURFACE.md.\n"
)
COLS = ("pairing_branch\tstratum\tG3_cell\tstatus\tG3_conditions\tG1_type\tG5_status\t"
        "G6_type\twitnesses\tparametrization_and_stratum\topen_forks\tslice2_must_decide\n")
with open(ledger_path, "w") as fh:
    fh.write(HEADER)
    fh.write(COLS)
    for row in ledger_rows:
        fh.write("\t".join(row) + "\n")
    for row in OBS_ROWS:
        fh.write("\t".join(row) + "\n")
print(f"\nLedger written: {ledger_path} ({len(ledger_rows) + len(OBS_ROWS)} rows)")

result = {
    "package": "udt_p4_routeA_stage3_gate_cut_2026-07-29",
    "stage": "Route A Stage 3 Slice 1 (TC1-TC5 computations; TC6 in SLICE2_SURFACE.md)",
    "date": "2026-07-29",
    "contract": "PREREGISTRATION.md (frozen before derivation)",
    "n_checks": n_tot,
    "n_passed": n_pass,
    "all_passed": all_pass,
    "check_split": {
        "n_substantive": n_sub,
        "n_substantive_passed": n_sub_pass,
        "n_citation_guards": n_guard,
        "n_citation_guards_passed": n_guard_pass,
        "citation_guard_names": sorted(CITATION_GUARDS),
        "note": "guards = bookkeeping/typing-table/citation checks, honestly labeled, never "
                "counted as zero-residual computations in a headline; A4 (verifier): "
                "TC4_torsion_period_vacuous, TC1_no_empty_adjudicated_cell, and "
                "TC2_kmod0_identity_is_row_dependency reclassified substantive -> guard "
                "(guard-grade computational content; load-bearing content = detail strings "
                "or verified Stage-2 citations)",
    },
    "amendments": {
        "A1": "the anchored-log forcing quantifier corrected (F-S3-class; verifier "
              "counterexample V10b adopted zero-residual as "
              "A1_V10b_counterexample_LE_zero_lambda_slot, with the exact iff condition "
              "A1_anchored_log_iff_condition and the lambda-independent sub-case "
              "A1_lambda_independent_sector_forcing_real): the LE cell's lambda-slot is "
              "forced nonzero (log-carrying via a_F' p0) IFF d(WF R_a)/dlam != 0 for some "
              "field slot a — NOT 'whenever the field sector is nonzero'; restated at every "
              "occurrence (script details, this JSON, EXACT_DERIVATION 1.2.6, "
              "SLICE2_SURFACE echo, ledger H4 text)",
        "A4": "check-split honesty: three guard-grade checks reclassified substantive -> "
              "guard (see check_split.note)",
    },
    "TC1_helmholtz_partition": {
        "condition_system": {
            "field_field": "(i) dR_a/du_b'' = dR_b/du_a'' [pairing-independent across the "
                           "anchored family]; (ii) dR_a/du_b' + dR_b/du_a' = 2 Dx(dR_b/du_a'')"
                           " + 2 a_F p1 dR_b/du_a''; (iii) recorded shift (see "
                           "condition_iii_shift_sample_pf)",
            "field_moduli_H4": "d(WF R_a)/dm_mu = E_a(WM R_mu); at lambda-dependent a_F the "
                               "lambda-row carries the anchored-log term a_F' p0 WF R_a; "
                               "A1: the lambda-slot is forced nonzero iff d(WF R_a)/dlam "
                               "!= 0 for some a",
            "moduli_moduli_H5": "antisymmetrized d(WM R_mu)/dm_nu in im(Dx) (Euler-certificate "
                                "criterion)",
            "derivation": "conditions proven = Frechet self-adjointness (adjoint-comparison "
                          "on generic components) + necessity on the generic EL image; "
                          "sufficiency = banked bicomplex/Vainberg statement (Category-A, "
                          "cited) instantiated on witnesses",
        },
        "condition_iii_shift_sample_pf": str(delta0_pf),
        "pairing_dependence_map": [
            "condition (i) identical across all anchored-weight branches (scope: enumerated "
            "family)",
            "conditions (ii)/(iii)/H4/H5 shift by exact a_F/a_M terms; a_F = a_M = 0 recovers "
            "P2",
            "multiplication by e^{-a_F p0} is a K4-inert parametrization-preserving bijection "
            "intertwining the P1-instance and P2 partitions: isomorphic-but-distinct cuts; "
            "cell membership of a FIXED tuple is pairing-relative (witnesses W1, W2, W3, "
            "omega)",
            "T4 blindness loci recomputed: P1-4D = P2 at lam = 0; P1-triad = P2 at "
            "lam = -1/2",
            "P3 bulk conditions = declared bulk choice's (interior defects wall-immune, "
            "computed); wall blocks add typed symmetry conditions (per declared N; Slice 2)",
            "anchored-log structure (A1-AMENDED, verifier): under the two ENUMERATED "
            "lambda-dependent P1 volumes (both da_F/dlam = 2) the LE cell's lambda-slot is "
            "forced nonzero — with log(c_E/Q) dependence via the a_F' p0 term — IFF "
            "d(WF R_a)/dlam != 0 for some field slot a, in particular for every "
            "lambda-INDEPENDENT nonzero field sector; NOT 'whenever the field sector is "
            "nonzero' (in-family counterexample A1_V10b: R_a = e^{-2 lam p0}(p2,f2,h2), "
            "zero moduli slots, LE under P1-4D, zero lambda-slot, no log); computed "
            "observation, not an obstruction — the log is alphabet-legal at supplied c_E, "
            "anchored (supplied-c_E) exactly as Stage-2's (c_E/Q)^a alphabet entries are "
            "(no bare-phi readmission; Stage-2 anchoring rule cited); SCOPE: jet <= 2, "
            "stationary presentation, BASE branch",
        ],
        "stratum_layer": "conditions are stratum-uniform jet-level identities; the KMOD0 cut "
                         "enters through the family (banked identity); Helmholtz cut and "
                         "stratum cut TRANSVERSE at witness level (four corners populated, "
                         "P2, on-stratum); RES-CNEQ0: CENSUS-REQUIRED",
        "empty_cells": "NONE adjudicated-empty (OS2 not triggered); scope: witness-level, "
                       "enumerated branches, GENERIC+KMOD0",
    },
    "TC2_integrability_typing": {
        "GENERIC": "DETERMINED-TYPE (3+7 vs 3+7; no pointwise identity — recomputed; no "
                   "Bianchi-type identity assumed); gate-1 on-shell = explicit integrability "
                   "on ONE solution (R5) — Slice 2; F-S6: no existence claim",
        "KMOD0": "CONSTRAINED-TYPE: one algebraic row dependency = the banked identity, "
                 "matched by the one gauge direction L23 (balanced); algebraic NOT "
                 "differential; gate 1 carries the orbit quotient",
        "RES-CNEQ0": "CENSUS-REQUIRED (resonance rule); banked shear example cited",
        "LE_cell_extra": "principal symbol symmetric (condition i) — pairing-independent "
                         "across the anchored family",
    },
    "TC3_boundary_census": {
        "N2": "theta slots = 0-jet traces; momenta = 1-jet functions; available at wall "
              "grade <= 2 -> LE-cell 2nd-order sub-families SELF-PAIRABLE-TYPED (parity-"
              "surviving slots)",
        "N4": "slots = {0-jet, 1-jet} traces; momenta contain 3rd jets -> STRUCTURALLY "
              "UNABLE at jet <= 2; typed extension required (NOT-EXHAUSTED)",
        "N3": "odd-order components: typed by the same enumeration; not run (stamp)",
        "parity": "mirror wall kills u^{(j)} traces with (-1)^j eps = -1: parity-halving "
                  "exhibited; parity assignments = SUPPLIED wall structure (canon instance "
                  "eps_phi = -1 spatial mirror, THEORY-cite)",
        "NV_cell": "NO-BULK-FORCED-SLOTS (source form); R_wall/R_corner admissibility + "
                   "wall-equation closure = Slice 2",
        "anchored_wall_rule": "p = q Q-power condition recomputed at the wall (V8 cited)",
        "corners": "TYPED-ONLY (codim-2 absent from the one-parameter presentation; Route C "
                   "TC5 examples cited)",
        "counterterms": "NOT available (Category-B; banked) — differentiability must live "
                        "inside the candidate",
    },
    "TC4_period_typing": {
        "LE_cell": "K4 cycles VANISHING-BY-TORSION (closed forms; banked V8_clash2 "
                   "recomputed); completion cycles NEEDS-COMPLETION-DATA (L4 open); J07/J11 "
                   "loops: mixing CLASSIFICATION-REQUIRED [F-S7], non-mixing "
                   "NO-TRANSITION-DATA-OBLIGATION",
        "NV_cell": "holonomy of closure data CLASSIFICATION-REQUIRED [F-S7] + "
                   "NEEDS-COMPLETION-DATA; torsion vacuity not auto-transferred (closed-form "
                   "scope)",
        "F_S7": "twisted-H1 machinery = MODEL-KNOWLEDGE; typing only; no banked G6 claim "
                "rests on it",
    },
    "TC5_joint_map": {
        "composite_rows": 30,
        "adjudicated_nonempty": 20,
        "census_required": 10,
        "outcome_class": "OS1",
        "structure": "5 pairing branches x 3 strata x 2 G3-cells; per-row G1/G5/G6 types, "
                     "witnesses, forks, Slice-2 duties; 4 known-object OBSERVATION rows",
    },
    "known_object_locations_observations": [
        "omega-shape: LE(P2/P3-bulkP2/P1 with lambda-independent a_M); NV(P1 with "
        "a_M = 2 lam) — computed; stratum stamps banked (off RES-CNEQ0; on-stratum witness "
        "for KMOD0)",
        "EH-form (stationary restriction): variational w.r.t. its metric-volume pairing BY "
        "CONSTRUCTION (Route C banked, GR-as-reference lane); restricted-system G3 status "
        "under enumerated pairings NOT adjudicated (R12 restrict-vs-vary caveat; Slice-2 "
        "cost)",
        "Bach-form: typed jet-3/4 class; G5 EXTENSION-REQUIRED at jet <= 2 (derived); order-4 "
        "condition machinery anchored (2-field instance)",
        "CM0-C-type members: the NV cell is their home class (banked; none instantiated)",
    ],
    "checks": CHECKS,
    "scope_stamps": [
        "jet <= 2 exhaustive layer; registered positive triangular chart; registered "
        "stationary one-parameter presentation; polynomial/formal in (k10, C) moduli; BASE "
        "branch (moduli constant; BR-A same theorem; BR-M/BR-CE typed NOT-EXHAUSTED)",
        "pairing branches: the banked 1.5 enumeration carried as the anchored-weight family; "
        "NONE adopted (F-S2); P1's volume/per-slot weights and P2's distributional class are "
        "OPEN supplied structure",
        "nonemptiness of cells: WITNESS-LEVEL (not a full-cell census)",
        "RES-CNEQ0 stratum: CENSUS-REQUIRED throughout (resonance rule); deeper "
        "stratification TYPED-NOT-EXHAUSTED (banked)",
        "jet-3/4: typed via the order-4 self-adjointness anchor (2-field instance); "
        "NOT-EXHAUSTED",
        "corners: typed only; sufficiency of Helmholtz conditions: banked bicomplex "
        "statement (Category-A, cited) + witness instantiation",
        "WS/GC solution-dependent legs (R5, R14, gate-1 on-shell, gate-4 currents, gate 2) "
        "NOT touched — Slice 2 (F-S6)",
    ],
    "falsifier_record": {
        "F-S1": "clean — no member selected/ranked; known-object rows are observations "
                "(TC5_known_object_rows_are_observations)",
        "F-S2": "clean — every G3 statement carries its pairing-branch label; W3's NV "
                "adjudication carries a PROOF of branch-independence across the enumerated "
                "anchored family; no pairing adopted",
        "F-S3": "TWO instances of the named error class, both caught and cured: (1) "
                "derivation-side SELF-CATCH — the W2 'LE under P1' field-sector-only gloss, "
                "corrected pre-verifier to the full W2' tuple statement; (2) VERIFIER CATCH "
                "(A1) — the anchored-log 'whenever the field sector is nonzero' quantifier, "
                "refuted by the in-family V10b counterexample and restated as the exact iff "
                "condition at every occurrence (three new A1_* zero-residual checks); all "
                "other only/all/none/empty statements carry stratum + scope stamps; "
                "partition claims scoped to the enumerated branches, jet <= 2, witness-level",
        "F-S4": "clean — banked facts recomputed as consistency (K4, stabilizer ranks, "
                "kmod0 identity, T4 blindness, TC5 instances); no contradiction found",
        "F-S5": "see all_passed / exit code",
        "F-S6": "clean — no solution computed, no existence/closure/current claim; TC2 is "
                "typing only",
        "F-S7": "carried — every J07/J11 classification row flags the twisted-H1 machinery "
                "as MODEL-KNOWLEDGE; no banked G6 claim rests on it",
    },
    "outcome_class": "OS1 — the joint gate-cut map is a populated partition (20 adjudicated "
                     "composite cells, all witness-nonempty; 10 CENSUS-REQUIRED resonance "
                     "cells; forks carried); no gate empties R_PW at the declared scope "
                     "(OS2 not triggered); no rigid low-parameter collapse (OS3 not "
                     "triggered); ceiling respected — no member selected, no existence/"
                     "uniqueness verdict on full R, no action, no physics",
    "throughput": "FULL DECLARED SCOPE (no scope reduction taken; jet-3/4 typing retained as "
                  "the order-4 anchor); single CPU process, exact SymPy",
}

with open(os.path.join(OUTDIR, "routeA_stage3_results.json"), "w") as fh:
    json.dump(result, fh, indent=2, sort_keys=False)
    fh.write("\n")

print(f"\n{n_pass}/{n_tot} checks passed = {n_sub_pass}/{n_sub} substantive zero-residual "
      f"checks + {n_guard_pass}/{n_guard} citation guards.")
print("Outcome class:", "OS1" if all_pass else "FAILURE (F-S5)", "—",
      "joint gate-cut map populated; no member selected (F-S1); resonance rows "
      "CENSUS-REQUIRED")

sys.exit(0 if all_pass else 1)
