#!/usr/bin/env python3
"""P4 Route A Slice 2 — the solution-touching legs on the gate-cut map (TD1-TD6).

Contract: udt_p4_routeA_slice2_solution_legs_2026-07-29/PREREGISTRATION.md (frozen first;
BOOTSTRAP-LENS frame Charles 2026-07-29 binding). Exact SymPy, zero-residual checks +
exact quadrature identities, deterministic (no floats, no randomness, no network, no
numeric solvers, no GPU), single CPU process, bounded. Exit 0 iff every check passes (F-D5).

AMENDED 2026-07-29 per VERIFIER_REPORT.md (PASS-WITH-REQUIRED-AMENDMENTS; both F-D3-class
stamp repairs — no computation refuted, no falsifier fired):
A1 (sign(aF) stamp): the depth-profile SHAPE is sign-scoped — p0''(vertex) has the SIGN of
    aF (single-MINIMUM well for aF > 0; single-MAXIMUM bump for aF < 0, which occurs inside
    the explored background range: P1-4D at lam < 0, P1-triad at lam < -1/2); 'symmetric'
    means about the VERTEX. The sign-FREE content is unchanged: E0 >= 0 forced (sum of
    squares), global regularity, nodelessness, and the closed form itself (now verified at
    FREE REAL aF — the old positive=True declaration was conditioning, not load-bearing).
    New zero-residual checks A1_* (the verifier's sign-free re-derivation adopted).
A2 (proof-coverage legs): the 'nonempty nonconstant at every aF != 0 background' locus
    claim was TRUE but exhibited only at (aF, ell) = (1, 1), and the 'w <= 5/8 => I_p < 0'
    leg flips sign for aF < 0. The verifier's general-(aF, ell) BOTH-signs symbolic legs
    are adopted as zero-residual checks A2_*; the locus sentence now carries its witness
    stamp. The continuity leg stays Category-A (named, cited).

SLICE-2 BOUNDARY (binding): solutions of R = 0 for READY-bin representative families ONLY.
NO candidate crowned as THE law (F-D1); NO elimination without background-robustness proof
(F-D2 — none is made here); every only/all/none/works/fails claim carries cell + fork-branch
+ stratum + BACKGROUND scope stamps (F-D3, the NAMED error class, three prior catches); NO
bank contradiction (F-D4); NO cross-solution splicing in any R5 triple (F-D6); NO matter
carrier adopted, NO source content beyond the typed rows (F-D7); the bootstrap neither
imposed nor suppressed — every candidate's self-consistent locus computed and REPORTED, or
explicitly reported NOT-DERIVABLE with its reason (F-D8 both directions).

REPRESENTATIVE-SUB-FAMILY STAMP (prereg TD1 allowance, travels with EVERY atlas row):
the exhaustive member of each READY cell is an arbitrary element of a functional-dimension-
sized class (Stage-2 parametrization); full-generality solution of R = 0 for the whole cell
exceeds any budget. Each cell's atlas rows below are REPRESENTATIVE FAMILIES (the banked
Stage-3 witnesses + the generated free-quadratic family), each tagged CHOSE(representative)
in the premise ledger. Every 'solution space' claim is scoped to its representative family;
NONE is a cell census. This is the prereg's representative-sub-family clause, not a silent
narrowing.

READY BIN (banked Stage-3 surface): 20 adjudicated composite cells = 5 pairing branches
(P1-4D aF=2lam; P1-triad aF=1+2lam; P2 aF=0; P3-bulkP2 bulk aF=0; P3-bulkP1 bulk aF=2lam)
x 2 strata (GENERIC, KMOD0) x 2 G3 cells (LOCALLY-EXACT, NONVARIATIONAL). OUT (typed only):
RES-CNEQ0 (CENSUS-REQUIRED, resonance rule), 4th-order class (EXTENSION-REQUIRED), carriers
(G09/F-D7), BR-M/BR-CE (typed NOT-EXHAUSTED upstream), time-live.

BASE-BRANCH MODULI READING (derived in T0 below): on the constant-moduli BASE branch the
delta-m_mu coefficient of the pairing is the INTEGRATED row  int WM R_mu dx = 0 (one scalar
relation per cell per modulus); the pointwise row R_mu = 0 belongs to the BR-M field fork
(typed NOT-EXHAUSTED upstream — out of READY scope, stamped).

Banked inputs (cited; recomputed as consistency only, never re-derived as new):
- Stage 3 (21d589c): GATE_CUT_LEDGER.tsv + SLICE2_SURFACE.md (the binding surface);
  witnesses W1/W2'/W3/omega; anchored-log iff; transversality; TC3 wall census.
- Stage 2 (2c0e7cc): stratified R_PW; k_mod = 0 identity; character modules.
- Stage 1: POSED_INVERSE_PROBLEM.md (R5 same-solution rule; R14); SIX_GATE_SPECS.md.
- Route C (udt_p4_routeC_shared_static_sector_2026-07-28): the restricted EH ODE system
  (a known 2nd-order instance, GR-as-reference lane; conditional stamps travel).
- native_action_final_adjudication_2026-07-18: mass rows CONDITIONAL/OPEN (the R5 mass
  instantiation below is therefore CHOSE-tagged and conditional); typed closure identities
  kept separate; G09 carrier = POSIT; G12 no derived bootstrap->local map.
Conventions: eta = diag(-1,1,1,1); X = [[H,0],[C,K]]; registered stationary one-parameter
presentation, fields (phi,f,bh) jets p0..p2/f0..f2/h0..h2; moduli (lam,k_mod,k10,C) constant
on BASE; anchored Q = c_E e^{-p0} at supplied c_E (p0 = log(c_E/Q) exact relabeling).
"""

import json
import os
import sys

import sympy as sp
from sympy import (Function, Matrix, Rational, Symbol, symbols, exp, log, atan,
                   sqrt, diff, expand, simplify, eye, zeros)

HERE = os.path.dirname(os.path.abspath(__file__))

CHECKS = []

CITATION_GUARDS = {
    # guards = definitional unpacking / recording-table / citation bookkeeping rows,
    # never counted as residual computations (honest split, house rule A2)
    "T0_base_branch_integrated_row",
    "TD3_lens_classification_record",
    "TD4_gate1_onshell_record",
    "TD4_R14_diagnostic_column",
    "TD5_NV_wall_duty_record",
    "TD5_gate2_J06_record",
    "TD5_jet34_slice2b_requirements",
    "TD6_ledger_coverage",
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
# S0 — banked structure recomputed (consistency, cited)
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
K4 = [I4, sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)]

k00, k10s, k11 = symbols("k00 k10 k11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
H2 = sp.diag(-1, 1)
Kb = Matrix([[k00, 0], [k10s, k11]])
Cb = Matrix([[c00, c01], [c10, c11]])
X = zeros(4, 4)
X[0:2, 0:2] = H2
X[2:4, 0:2] = Cb
X[2:4, 2:4] = Kb

check(
    "S0_K4_and_X_recomputed",
    all(is_zero_matrix(M.T * eta * M - eta) and M.det() == 1 for M in K4)
    and is_zero_matrix(X[0:2, 0:2] - H2),
    "K4 exact and the registered E02 footing X = [[H,0],[C,K]] (banked conventions recomputed)",
)

# k_mod = 0 identity + gauge direction (Stage-2 A1, compact recompute):
L23m = GENS["L23"]
W23 = (L23m * X - X * L23m).subs(k11, k00)   # on the k_mod = 0 stratum (k11 = k00)
r_tr, r_tf, r_sh, r_nl = symbols("r_tr r_tf r_sh r_nl")
m00, m01, m10, m11 = symbols("m00 m01 m10 m11")
W_slot = r_tr * eye(2) + r_tf * sp.diag(-1, 1) + r_sh * Matrix([[0, 0], [1, 0]]) \
    + r_nl * Matrix([[0, 1], [0, 0]])
Mker = Matrix([[m00, m01], [m10, m11]])
pair = lambda A_, B_: sp.trace(A_.T * B_)
pairing_stratum = expand(pair(W_slot, W23[2:4, 2:4]) + pair(Mker, W23[2:4, 0:2]))
IDENT_KMOD0 = expand(-2 * k10s * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01)
check(
    "S0_kmod0_identity_recomputed",
    expand(pairing_stratum - IDENT_KMOD0) == 0,
    "the exact k_mod = 0 pointwise Noether identity -2 k10 r_tf + m00c10 + m01c11 - m10c00 "
    "- m11c01 = 0 recomputed from <slots, [L23,X]> (Stage-2 A1, consistency; r_tr/r_sh/r_nl "
    "drop out)",
)

# The L23 gauge direction's chart reading on the stratum (used for the TD4 orbit quotient):
Kblock = W23[2:4, 2:4]
Cblock = W23[2:4, 0:2]
Jrot = Matrix([[0, 1], [-1, 0]])
d_k10_gauge = Kblock[1, 0]              # delta k10 component
d_kmod_gauge = expand((Kblock[0, 0] - Kblock[1, 1]) / 2)   # (delta k00 - delta k11)/2
d_lam_gauge = expand((Kblock[0, 0] + Kblock[1, 1]) / 2)

# ============================================================================
# Jet machinery (registered stationary presentation; BASE branch)
# ============================================================================
print("\n--- Jet machinery ---")

FIELDS = ["p", "f", "h"]
JMAX = 6
J = {a: symbols(f"{a}0:{JMAX + 1}") for a in FIELDS}
lam, kmod = symbols("lam k_mod")
MODULI = [lam, kmod, k10s, c00, c01, c10, c11]
cE = Symbol("c_E", positive=True)
alpha_s = Symbol("alpha")
frak_c = Symbol("frak_c")   # completion label slot (discrete argument; L4 fork)

ALL_CHAINS = [list(J[a]) for a in FIELDS]


def Dx(expr):
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
    out = sp.Integer(0)
    for k in range(order + 1):
        out += (-1) ** k * Dxn(diff(expr, J[a][k]), k)
    return out


p0, p1, p2 = J["p"][0], J["p"][1], J["p"][2]
f0, f1, f2 = J["f"][0], J["f"][1], J["f"][2]
h0, h1, h2 = J["h"][0], J["h"][1], J["h"][2]

# ============================================================================
# T0 — structural theorems for the whole atlas
# ============================================================================
print("\n--- T0: structural theorems (zero-set/pairing; BASE-branch moduli rows) ---")

a_w = Symbol("a_w")   # symbolic anchored exponent a_F: covers 2 lam (P1-4D, P3-bulkP1),
#                       1 + 2 lam (P1-triad), 0 (P2, P3-bulkP2) by substitution
WFa = exp(a_w * p0)

check(
    "T0_weight_invertibility_zero_set_theorem",
    simplify(WFa * exp(-a_w * p0) - 1) == 0 and sp.exp(Symbol("y", real=True)).is_positive,
    "THEOREM (field sector, all READY cells): the anchored weight WF = e^{aF p0} has the "
    "exact inverse e^{-aF p0} and is positive, so WF*R_a = 0 iff R_a = 0 — the FIELD-sector "
    "zero set of a FIXED component tuple is IDENTICAL across the enumerated anchored pairing "
    "family (P1-4D/P1-triad/P2/P3-bulk). SCOPE: enumerated anchored branches, jet <= 2, "
    "registered stationary presentation, BASE branch. Pairing-branch dependence of R = 0 "
    "enters ONLY through (a) G3 cell MEMBERSHIP of the tuple (banked, pairing-relative) and "
    "(b) the WM-weighting of the integrated constant-moduli rows",
)

check(
    "T0_base_branch_integrated_row",
    True,
    "[definitional unpacking, cited] the enumerated pairing <R,dX> = int [sum_a WF R_a dU_a "
    "+ sum_mu WM R_mu dm_mu] dx (Stage-3 registration); on the BASE branch dm_mu is an "
    "x-CONSTANT direction, so its coefficient is the INTEGRATED scalar row int WM R_mu dx = 0 "
    "— one relation per cell per modulus. The pointwise row R_mu = 0 is the BR-M field-fork "
    "reading (typed NOT-EXHAUSTED upstream; OUT of READY scope, stamped)",
)

# ============================================================================
# TD1 — the solution atlas: LE representative (generated free-quadratic family)
# ============================================================================
print("\n--- TD1: LE representative GEN-QUAD (generated family, symbolic anchored weight) ---")

# Representative CHOICE (tagged CHOSE in the premise ledger): Ltil0 = free quadratic
# first-order density. The generated tuple R_a = WF^{-1} E_a(WF Ltil0) is the Stage-3
# W2'-class member at this Ltil0; its LE membership per branch is BANKED (generated-family
# H-conditions, Stage-3 TC1), re-instantiated below — not re-derived.
Ltil0 = (p1**2 + f1**2 + h1**2) / 2
S_dens = WFa * Ltil0
R_LE = {a: expand(exp(-a_w * p0) * Euler(S_dens, a, 2)) for a in FIELDS}

R_p_stated = a_w * (f1**2 + h1**2 - p1**2) / 2 - p2
R_f_stated = -(a_w * p1 * f1 + f2)
R_h_stated = -(a_w * p1 * h1 + h2)
check(
    "TD1_LE_generated_components_match",
    expand(R_LE["p"] - R_p_stated) == 0
    and expand(R_LE["f"] - R_f_stated) == 0
    and expand(R_LE["h"] - R_h_stated) == 0,
    "GEN-QUAD components computed from the generated construction: R_p = aF(f1^2+h1^2-p1^2)/2 "
    "- p2, R_f = -(aF p1 f1 + f2), R_h = -(aF p1 h1 + h2) — one tuple, symbolic aF covering "
    "all five enumerated branches by substitution (2lam / 1+2lam / 0)",
)

# Helmholtz (i)+(ii) re-instantiated on this member (banked generated-family theorem cited):


def frechet(Delta, order):
    return {a: {b: [diff(Delta[a], J[b][k]) for k in range(order + 1)]
                for b in FIELDS} for a in FIELDS}


Delta_LE = {a: expand(WFa * R_LE[a]) for a in FIELDS}
Fr = frechet(Delta_LE, 2)
hi2_ok = all(expand(Fr[a][b][2] - Fr[b][a][2]) == 0 for a in FIELDS for b in FIELDS)
hi1_ok = all(expand(Fr[a][b][1] + Fr[b][a][1] - 2 * Dx(Fr[b][a][2])) == 0
             for a in FIELDS for b in FIELDS)
hi0_ok = all(expand(Fr[a][b][0] - Fr[b][a][0] + Dx(Fr[b][a][1]) - Dxn(Fr[b][a][2], 2)) == 0
             for a in FIELDS for b in FIELDS)
check(
    "TD1_LE_rep_helmholtz_reinstantiated",
    hi2_ok and hi1_ok and hi0_ok,
    "GEN-QUAD satisfies the field-field Helmholtz families (i)-(iii) identically at symbolic "
    "aF (re-instantiation of the banked Stage-3 generated-family theorem — consistency, not a "
    "new derivation); H4/H5 by the banked TC1_H4/H5_generated_witness (cited)",
)

# On-shell substitution rules (the solved form of R = 0, field sector):
ONSHELL = {p2: a_w * (f1**2 + h1**2 - p1**2) / 2, f2: -a_w * p1 * f1, h2: -a_w * p1 * h1}

E0dens = expand(WFa * Ltil0)
dE = Dx(E0dens).subs(ONSHELL)
check(
    "TD1_LE_energy_first_integral",
    simplify(dE) == 0,
    "Dx(WF*Ltil0) = 0 on-shell: the anchored energy density E0 := e^{aF p0} Ltil0 is an exact "
    "first integral of the GEN-QUAD system (DERIVED from autonomy, not assumed; symbolic aF)",
)

dcf = Dx(WFa * f1).subs(ONSHELL)
dch = Dx(WFa * h1).subs(ONSHELL)
check(
    "TD1_LE_shift_currents",
    simplify(dcf) == 0 and simplify(dch) == 0,
    "Dx(e^{aF p0} f1) = Dx(e^{aF p0} h1) = 0 on-shell: two more exact first integrals "
    "c_f, c_h (from the derived f/h shift symmetries — see TD4)",
)

# --- The exact solution family (closed form), verified by substitution ---
xs = Symbol("x")
a_p = Symbol("a", positive=True)      # aF value (conditioning only; the A1 checks below
#                                       re-verify the family at FREE REAL aF, both signs)
w0 = Symbol("w0", positive=True)
w1 = Symbol("w1", real=True)
cf, ch = symbols("c_f c_h", positive=True)
f0c, h0c = symbols("f0c h0c", real=True)
ell = Symbol("ell", positive=True)

E0e = (w1**2 / a_p**2 + cf**2 + ch**2) / (2 * w0)   # E0 DEFINED by the free parameters
Aq = a_p**2 * E0e / 2
wexpr = Aq * xs**2 + w1 * xs + w0                    # w = e^{aF p0}, quadratic in x

p0x = log(wexpr) / a_p
p1x = diff(p0x, xs)
p2x = diff(p0x, xs, 2)
f1x = cf / wexpr
f2x = diff(f1x, xs)
h1x = ch / wexpr
h2x = diff(h1x, xs)

res_p = R_p_stated.subs({a_w: a_p, p1: p1x, p2: p2x, f1: f1x, h1: h1x})
res_f = R_f_stated.subs({a_w: a_p, p1: p1x, f1: f1x, f2: f2x})
res_h = R_h_stated.subs({a_w: a_p, p1: p1x, h1: h1x, h2: h2x})
check(
    "TD1_LE_well_solution_zero_residual",
    simplify(res_p) == 0 and simplify(res_f) == 0 and simplify(res_h) == 0,
    "EXACT SOLUTION FAMILY (GEN-QUAD, aF != 0): e^{aF p0} = w(x) = (aF^2 E0/2) x^2 + w1 x + "
    "w0; f' = c_f/w, h' = c_h/w; free parameters (w0>0, w1, c_f, c_h, f(0), h(0)) with "
    "E0 = (w1^2/aF^2 + c_f^2 + c_h^2)/(2 w0): all three field equations vanish IDENTICALLY "
    "(zero residual, symbolic aF, no constraint juggling; A1 re-verifies at FREE REAL aF "
    "of BOTH signs — the positivity declaration here is conditioning, not load-bearing)",
)

disc_identity = expand(w1**2 - 4 * Aq * w0 + a_p**2 * (cf**2 + ch**2))
sum_sq = expand(2 * w0 * E0e - (w1**2 / a_p**2 + cf**2 + ch**2))
check(
    "TD1_LE_disc_E0_sign_structure",
    disc_identity == 0 and sum_sq == 0,
    "disc(w) = w1^2 - 4Aw0 = -aF^2(c_f^2+c_h^2) <= 0 EXACTLY, and 2 w0 E0 = w1^2/aF^2 + "
    "c_f^2 + c_h^2 (a sum of squares): every real member with w0 > 0 has E0 >= 0, w has no "
    "real root for c != 0 (a globally regular, NODELESS depth profile — SIGN-STAMPED per A1: "
    "a single-MINIMUM well of p0 for aF > 0, a single-MAXIMUM bump for aF < 0, since "
    "p0''(vertex) has the sign of aF [A1_vertex_curvature_sign_of_aF]; 'symmetric' = about "
    "the vertex), and E0 = 0 iff w1 = c_f = c_h = 0 (constants). EMERGENT (observed, not "
    "imposed): anchored-weight positivity forces nonnegative energy on this family — "
    "SIGN-FREE, both signs of aF. SCOPE: GEN-QUAD representative, aF != 0 branches, "
    "BASE branch, GENERIC/KMOD0 strata, all backgrounds",
)

# --- A1 (amendment, verifier's sign-free re-derivation adopted): the closed form, the
# --- vertex-curvature sign law, and an explicit aF < 0 bump instance -----------------
a_r = Symbol("a_r", real=True, nonzero=True)   # FREE REAL anchored exponent (both signs)
cfr, chr_ = symbols("c_fr c_hr", real=True)
E0r = (w1**2 / a_r**2 + cfr**2 + chr_**2) / (2 * w0)
Ar = a_r**2 * E0r / 2
wr = Ar * xs**2 + w1 * xs + w0
p0r = log(wr) / a_r
p1r = diff(p0r, xs)
p2r = diff(p0r, xs, 2)
f1r = cfr / wr
f2r = diff(f1r, xs)
h1r = chr_ / wr
h2r = diff(h1r, xs)
res_p_r = R_p_stated.subs({a_w: a_r, p1: p1r, p2: p2r, f1: f1r, h1: h1r})
res_f_r = R_f_stated.subs({a_w: a_r, p1: p1r, f1: f1r, f2: f2r})
res_h_r = R_h_stated.subs({a_w: a_r, p1: p1r, h1: h1r, h2: h2r})
check(
    "A1_well_zero_residual_signfree",
    simplify(res_p_r) == 0 and simplify(res_f_r) == 0 and simplify(res_h_r) == 0,
    "A1 (verifier's sign-free re-derivation adopted): the closed-form family solves all "
    "three GEN-QUAD field equations with aF a FREE REAL nonzero symbol (NEGATIVE included) "
    "and c_f, c_h real of any sign — the TD1 positive=True declaration is NOT load-bearing. "
    "SCOPE: GEN-QUAD representative, aF != 0 branches, BASE branch, all backgrounds",
)

xv = -w1 / (2 * Ar)                      # the vertex of w
p2v = simplify(p2r.subs(xs, xv))
p2v_expected = simplify((2 * Ar) / (a_r * (cfr**2 + chr_**2) * a_r**2 / (4 * Ar)))
sgn_sub_pos = {a_r: 1, w1: 0, cfr: 1, chr_: 1, w0: 1}
sgn_sub_neg = {a_r: -1, w1: 0, cfr: 1, chr_: 1, w0: 1}
check(
    "A1_vertex_curvature_sign_of_aF",
    simplify(p2v - p2v_expected) == 0
    and sp.ask(sp.Q.positive(p2v.subs(sgn_sub_pos))) is True
    and sp.ask(sp.Q.negative(p2v.subs(sgn_sub_neg))) is True,
    "A1 SIGN LAW (both ways, zero residual): p0''(vertex) = 8A^2/(aF^3 (c_f^2+c_h^2)) has "
    "the SIGN of aF — instantiated POSITIVE at aF = +1 (single-MINIMUM well) and NEGATIVE "
    "at aF = -1 (single-MAXIMUM bump). aF < 0 occurs INSIDE the explored background range "
    "(P1-4D aF = 2 lam: lam < 0; P1-triad aF = 1 + 2 lam: lam < -1/2). SCOPE: GEN-QUAD, "
    "aF != 0 branches, BASE branch",
)

bump_sub = {a_r: -1, w1: 0, cfr: 1, chr_: 1, w0: 1}
w_bump = wr.subs(bump_sub)                          # = x^2/2 + 1 at aF = -1, E0 = 1
disc_bump = expand((w1**2 - 4 * Ar * w0).subs(bump_sub))
check(
    "A1_bump_instance_regular_nodeless",
    simplify(res_p_r.subs(bump_sub)) == 0
    and simplify(res_f_r.subs(bump_sub)) == 0
    and simplify(res_h_r.subs(bump_sub)) == 0
    and expand(w_bump - (xs**2 / 2 + 1)) == 0
    and disc_bump == -2
    and sp.ask(sp.Q.negative(p2r.subs(bump_sub).subs(xs, 0))) is True,
    "A1 BUMP INSTANCE (aF = -1, w0 = 1, w1 = 0, c_f = c_h = 1, E0 = 1): zero residual in "
    "all three equations; w = x^2/2 + 1 with disc = -2 < 0 so w > 0 EVERYWHERE (globally "
    "regular, nodeless); p0''(0) < 0 — a single-MAXIMUM bump of the depth, regular and "
    "nodeless exactly as the aF > 0 well is. The sign-free structure (E0 >= 0, regularity, "
    "nodelessness) carries; only the SHAPE word flips. SCOPE: GEN-QUAD, aF < 0 side of the "
    "explored background range, BASE branch",
)

# Local exhaustiveness: the 6-parameter family covers generic initial data (rank 6),
# and the system is in solved form u'' = F(u, u') (Picard uniqueness, Category-A cited).
data_map = Matrix([
    log(w0) / a_p,           # p0(0)
    w1 / (a_p * w0),         # p1(0)
    f0c,                     # f(0)
    cf / w0,                 # f'(0)
    h0c,                     # h(0)
    ch / w0,                 # h'(0)
])
params = [w0, w1, f0c, cf, h0c, ch]
Jac = data_map.jacobian(params).subs({w0: 1, w1: 2, f0c: 3, cf: 5, h0c: 7, ch: 11, a_p: 1})
check(
    "TD1_LE_solution_space_rank6",
    Jac.rank() == 6,
    "the parameter-to-initial-data map has rank 6 at a rational point: the closed-form family "
    "realizes generic initial data; with the system in solved form u'' = F(u,u') (Picard "
    "uniqueness, Category-A cited) the LOCAL field-sector solution space is EXACTLY the "
    "6-dim initial-data manifold, covered by the family where it extends (w > 0). SCOPE: "
    "local-in-x exhaustiveness for the REPRESENTATIVE family; sign-symmetric in c_f, c_h "
    "(taken positive here; c=0/E0=0 edges enumerated separately)",
)

R_a0 = {a: expand(R_LE[a].subs(a_w, 0)) for a in FIELDS}
check(
    "TD1_LE_blindness_affine_case",
    expand(R_a0["p"] + p2) == 0 and expand(R_a0["f"] + f2) == 0
    and expand(R_a0["h"] + h2) == 0
    and (2 * lam).subs(lam, 0) == 0 and (1 + 2 * lam).subs(lam, Rational(-1, 2)) == 0,
    "at aF = 0 the GEN-QUAD tuple degenerates EXACTLY to (-p2, -f2, -h2): solution space = "
    "AFFINE atlas u = u(0) + u'(0) x (6 params). aF = 0 is the whole P2/P3-bulkP2 branch AND "
    "the banked T4 blindness loci INSIDE the P1 branches (P1-4D at lam = 0; P1-triad at "
    "lam = -1/2): the solution-space SHAPE (well vs affine) is BACKGROUND-CONTROLLED through "
    "the pairing weight — an exact background-transition inside a single branch (observation)",
)

check(
    "TD1_LE_E0zero_constants_only",
    sum_sq == 0,   # 2 w0 E0 = sum of three squares, banked just above; conclusion recorded
    "E0 = 0 forces w1 = c_f = c_h = 0 (sum-of-squares, real class), hence w = w0 constant and "
    "p1 = f1 = h1 = 0: the E0 = 0 stratum of the family is EXACTLY the constant solutions "
    "(trivial atlas members, present at EVERY background). SCOPE: GEN-QUAD, real class, "
    "w0 > 0",
)

# Exact quadratures (honest closed forms for f, h and int p0 dx), verified by differentiation:
s_pos = sqrt(4 * Aq * w0 - w1**2)   # = sqrt(aF^2 (c_f^2 + c_h^2)) > 0 for c != 0
F_atan = (2 * cf / s_pos) * atan((2 * Aq * xs + w1) / s_pos)
check(
    "TD1_quadrature_f_closed_form",
    simplify(diff(F_atan, xs) - cf / wexpr) == 0,
    "f(x) = f(0) + (2 c_f/s) [atan((2Ax+w1)/s) - atan(w1/s)], s = sqrt(4Aw0 - w1^2) = "
    "|aF| c: EXACT closed-form quadrature (verified by differentiation); h identical with "
    "c_h. SCOPE: c != 0, aF != 0; c = 0 gives f, h constant; aF = 0 gives f, h affine",
)

G_anti = (xs + w1 / (2 * Aq)) * log(wexpr) - 2 * xs + (s_pos / Aq) * atan((2 * Aq * xs + w1) / s_pos)
check(
    "TD1_quadrature_logw_closed_form",
    simplify(diff(G_anti, xs) - log(wexpr)) == 0,
    "int log(w) dx has the EXACT antiderivative G(x) = (x + w1/2A) log w - 2x + (s/A) "
    "atan((2Ax+w1)/s) (verified by differentiation): I_p := int_{-ell}^{ell} p0 dx = "
    "[G(ell) - G(-ell)]/aF in closed form. SCOPE: E0 != 0, c != 0",
)

# ============================================================================
# TD1 — moduli-sector LE representative (omega-shape) and NV representatives
# ============================================================================
print("\n--- TD1: omega-shape / NV representatives ---")

aM = Symbol("a_M")
WMa = exp(aM * p0)
VM = Symbol("V_M", positive=True)   # int WM dx over the cell: positive (positive integrand)
sol_k10 = sp.solve(sp.Eq(k10s * VM, 0), k10s)
aM_r = Symbol("aM_r", real=True)
check(
    "TD1_omega_zero_set_k10_stratum",
    sol_k10 == [0] and sp.exp(aM_r * Symbol("z", real=True)).is_positive,
    "omega-shape (R_k10 = k10, all other slots 0; banked LE cells: P2/P3-bulkP2/P1 with "
    "lam-independent a_M): the only nonvacuous row of R = 0 is the integrated k10-row "
    "k10 * int WM dx = 0; the integrand is positive so int WM dx > 0 (Category-A positivity) "
    "and the EXACT solution space is the stratum {k10 = 0} x {ALL fields free} x {all other "
    "moduli retained} x {all backgrounds} — a_M-independent (pairing-supply "
    "branch-independence PROVEN for this row). SCOPE: omega representative, its banked LE "
    "cells, BASE branch, GENERIC+KMOD0 (off RES-CNEQ0, banked stamp)",
)

# W1 = (p2, f2, h2): zero set + its NV defect on P1-side branches (banked cell membership):
Delta_W1 = {"p": WFa * p2, "f": WFa * f2, "h": WFa * h2}
FrW1 = frechet(Delta_W1, 2)
defect_ii = expand(FrW1["p"]["p"][1] + FrW1["p"]["p"][1] - 2 * Dx(FrW1["p"]["p"][2]))
aff = {p2: 0, f2: 0, h2: 0}
check(
    "TD1_W1_affine_atlas_and_NV_defect",
    all(expand(Delta_W1[a].subs(aff)) == 0 for a in FIELDS)
    and simplify(defect_ii / WFa + 2 * a_w * p1) == 0,
    "W1 = (p2, f2, h2): zero set = the AFFINE atlas u = u(0) + u'(0) x (6 params, all moduli "
    "retained, all backgrounds); its Helmholtz-(ii) defect is exactly -2 aF p1 e^{aF p0} — "
    "NONVARIATIONAL on the aF != 0 branches (P1-4D/P1-triad/P3-bulkP1) exactly OFF the "
    "blindness loci, LE at aF = 0 (P2-side) — re-instantiating the banked TC1_W1 adjudication "
    "with symbolic aF. The SAME zero set appears in the LE cell (P2) and the NV cell "
    "(P1-side): the T0 zero-set theorem in action",
)

# W2-fs (field sector of W2' with zero moduli slots) under P2: banked NV; same zero set:
W2fs = {a: expand(exp(-2 * lam * p0) * Euler(exp(2 * lam * p0) * Ltil0, a, 2)) for a in FIELDS}
check(
    "TD1_W2fs_same_zero_set_under_P2",
    all(expand(W2fs[a] - R_LE[a].subs(a_w, 2 * lam)) == 0 for a in FIELDS),
    "W2-fs (the W2' field sector with ALL moduli slots zero; banked NONVARIATIONAL under P2, "
    "TC1_W2_LE_P1_NV_P2 cited) is the IDENTICAL tuple to GEN-QUAD at aF = 2 lam: its zero "
    "set under P2 is the SAME well atlas (with lam a free background coordinate and NO "
    "integrated lam-row, since its moduli slots are zero) — the NV cell of P2/P3-bulkP2 "
    "carries the full well atlas with no background tie. SCOPE: W2-fs representative, "
    "P2-side NV cells, BASE branch",
)

# W3 = (p1, 0, 0): all-branch NV (banked); degenerate zero set:
check(
    "TD1_W3_underdetermined_member",
    all(diff(p1, J[a][k]) == 0 for a in ["f", "h"] for k in range(3))
    and sp.solve(sp.Eq(p1, 0), p1) == [0],
    "W3 = (p1, 0, 0) (banked all-branch NV, proof cited): zero set = {p0 = const} x {f, bh "
    "ARBITRARY functions} x {moduli retained} — this MEMBER's on-shell system is DEGENERATE/"
    "UNDERDETERMINED (its f/bh rows are identically zero), a per-member fact that does NOT "
    "contradict the banked DETERMINED-TYPE gate-1 count (which types the generic member). "
    "SCOPE: W3 representative, all enumerated branches, both READY strata, all backgrounds",
)

# ============================================================================
# TD1/TD4 — KMOD0 stratum: identity residual + L23 orbit quotient on the reps
# ============================================================================
print("\n--- TD1/TD4: KMOD0 stratum legs ---")

# Representatives' slot tuples: GEN-QUAD has r_tf = 0, M = 0 (field sector + lam-slot only);
# omega has r_sh = k10, r_tf = 0, M = 0. The identity involves only (r_tf, M):
resid_genquad = IDENT_KMOD0.subs({r_tf: 0, m00: 0, m01: 0, m10: 0, m11: 0})
resid_omega = resid_genquad   # identical substitution (omega's r_sh does not enter)
check(
    "TD1_kmod0_noether_residual_zero_reps",
    expand(resid_genquad) == 0 and expand(resid_omega) == 0,
    "on KMOD0 the banked stratum Noether identity is satisfied IDENTICALLY by every atlas "
    "representative (GEN-QUAD/W1/W2-fs/W3: field-sector members, r_tf = M = 0 — the banked "
    "all-strata carrier class; omega: r_sh does not enter the identity — banked on-stratum "
    "witness): the KMOD0 solution atlases are the GENERIC ones restricted to k_mod = 0, "
    "uncut by the identity. SCOPE: the named representatives, KMOD0, jet <= 2, BASE branch",
)

genquad_moduli_indep = all(
    diff(R_LE[a].subs(a_w, 2 * lam), m) == 0 for a in FIELDS for m in [k10s, c00, c01, c10, c11]
)
check(
    "TD1_kmod0_L23_quotient_reps",
    genquad_moduli_indep
    and d_k10_gauge == 0
    and expand(d_kmod_gauge - k10s) == 0
    and d_lam_gauge == 0
    and is_zero_matrix(Cblock - Jrot * Cb),
    "the L23-orbit quotient carried on KMOD0 (gate-1 duty): the gauge tangent has chart "
    "reading (dlam, dk_mod, dk10, dC) = (0, k10, 0, J.C) with J the screen rotation; "
    "GEN-QUAD's components are (k10,C)-INDEPENDENT so its solution family is L23-invariant "
    "and the quotient acts only on the RETAINED moduli coordinates (well-defined orbit "
    "families); omega's zero set {k10 = 0} has dk10 = 0 (invariant) and on it dk_mod = 0 "
    "(stays on-stratum). SCOPE: named representatives, KMOD0, registered chart",
)

# ============================================================================
# TD2 — R5 same-solution closure + the self-consistent locus (bootstrap lens)
# ============================================================================
print("\n--- TD2: R5 closure and self-consistent loci ---")

V_cell = sp.integrate(wexpr, (xs, -ell, ell))
V_stated = 2 * Aq * ell**3 / 3 + 2 * w0 * ell
M_cell = 2 * ell * E0e
rho_cell = sp.cancel(M_cell / V_cell)
check(
    "TD2_R5_V_M_rho_closed_forms",
    expand(V_cell - V_stated) == 0 and simplify(rho_cell * V_cell - M_cell) == 0,
    "R5 triple on ONE GEN-QUAD solution (no splicing — F-D6): V = int_{-ell}^{ell} w dx = "
    "(2/3) A ell^3 + 2 w0 ell (the branch's own declared volume functional, THEORY-supplied "
    "by the pairing branch); M = int E0dens dx = 2 ell E0 (M-INSTANTIATION = the member's own "
    "first-integral energy — CHOSE-tagged, CONDITIONAL: the banked mass rows are "
    "CONDITIONAL/OPEN, stamp travels with every R5 number); rho = M/V exact closed form; "
    "the closure identity rho V = M holds on the same solution by construction. SCOPE: "
    "GEN-QUAD representative, aF != 0 branches, all backgrounds (aF = 0: V = 2 ell, M under "
    "the P2 dual class = typed L7 datum, recorded)",
)

lam_row_4D = expand(diff(exp(2 * lam * p0) * Ltil0, lam) - 2 * p0 * exp(2 * lam * p0) * Ltil0)
lam_row_triad = expand(diff(exp((1 + 2 * lam) * p0) * Ltil0, lam)
                       - 2 * p0 * exp((1 + 2 * lam) * p0) * Ltil0)
# a_M-independence of the integrated row (pairing-supply branch-independence):
Rlam_gen = WMa**-1 * diff(WFa.subs(a_w, 2 * lam) * Ltil0, lam)
row_integrand = expand(WMa * Rlam_gen - diff(WFa.subs(a_w, 2 * lam) * Ltil0, lam))
check(
    "TD2_lambda_row_exact_form",
    lam_row_4D == 0 and lam_row_triad == 0 and row_integrand == 0,
    "the generated lam-slot obeys WM R_lam = d(WF Ltil0)/dlam EXACTLY for BOTH enumerated "
    "P1 instances (aF' = 2) and for EVERY supplied a_M (the WM cancels: pairing-supply "
    "branch-independence of the integrated row PROVEN); on-shell the integrand is "
    "2 p0 (WF Ltil0) = 2 p0 E0, so the BASE-branch lam-row is 2 E0 int p0 dx = 2 E0 I_p / "
    "with I_p in the TD1 closed form. Under P2 (aF' = 0) the row is IDENTICALLY ZERO. "
    "SCOPE: GEN-QUAD, BASE branch",
)

# Self-consistent-locus nonemptiness (nontrivial branch), exact sign legs + continuity.
# A2 witness stamp: THESE two legs are exhibited at the single background point
# (aF, ell) = (1, 1); general-(aF, ell) BOTH-signs coverage = the A2_* checks below.
tsym = Symbol("t")
w_legA = wexpr.subs({a_p: 1, w0: Rational(1, 2), w1: 0, cf: Rational(3, 10), ch: Rational(2, 5)})
# leg A: w(t) <= 5/8 < 1 on [-1,1]: w = A t^2 + 1/2 with A = E0/2, E0 = c^2/(2 w0) = 1/4
w_legA_t = w_legA.subs(xs, tsym)
legA_alg = expand(w_legA_t - (tsym**2 / 8 + Rational(1, 2))) == 0
legA_bound = expand(Rational(5, 8) - w_legA_t.subs(tsym**2, 1)) == 0
w_legB = wexpr.subs({a_p: 1, w0: 2, w1: 0, cf: 2, ch: 2})
w_legB_t = w_legB.subs(xs, tsym)
legB_alg = expand(w_legB_t - (tsym**2 + 2)) == 0
check(
    "TD2_selfconsistent_locus_nonempty",
    legA_alg and legA_bound and legB_alg
    and sp.log(Rational(5, 8)).is_negative and sp.log(2).is_positive,
    "SELF-CONSISTENT LOCUS (P1-side GEN-QUAD; reported per prereg 2c): {E0 = 0 (constants)} "
    "UNION {I_p = 0} with I_p = [G(ell)-G(-ell)]/aF exact (TD1 quadrature). NONTRIVIAL "
    "nonemptiness witnessed here at the SINGLE background point (aF, ell) = (1, 1), w1 = 0 "
    "[A2 witness stamp — the general-(aF, ell) BOTH-signs legs are the A2_* checks]: leg A "
    "(w0 = 1/2, c = 1/2) gives w = t^2/8 + 1/2 <= 5/8 < 1 on [-1,1] so log w <= log(5/8) < 0 "
    "and (at aF = 1 > 0) I_p < 0 — NOTE this implication is aF-SIGN-DEPENDENT (I_p = "
    "(int log w)/aF flips with aF; the A2 legs carry both signs); leg B (w0 = 2, c = "
    "2*sqrt(2) -> c^2 = 8) gives w = t^2 + 2 >= 2 > 1 so I_p >= 2 log 2 > 0; continuity of "
    "the explicit closed form along any parameter path joining the legs (Category-A) yields "
    "an I_p = 0 root with E0 > 0. Monotonicity of log and integral positivity are the two "
    "Category-A calculus steps (stated, cited). SCOPE: GEN-QUAD, P1-4D/P1-triad/P3-bulkP1, "
    "BASE branch, GENERIC+KMOD0; this check's legs = the (aF, ell) = (1, 1) witness only",
)

# --- A2 (amendment, verifier's general-(aF, ell) BOTH-signs legs adopted): the
# --- 'every aF != 0 background' nonemptiness claim, proof coverage closed -------------
q_pos = Symbol("q", positive=True)
for sgn, tag in ((1, "pos"), (-1, "neg")):
    av = sgn * q_pos                                  # aF of this sign, |aF| = q symbolic
    # leg A': target w = x^2/(8 ell^2) + 1/2 (max 5/8 < 1 on [-ell, ell]); realized by
    # w0 = 1/2, w1 = 0, c^2 = 1/(4 aF^2 ell^2) split 3/5, 4/5 (both currents nonzero):
    cfA = Rational(3, 5) / (2 * sqrt(av**2) * ell)
    chA = Rational(4, 5) / (2 * sqrt(av**2) * ell)
    E0A = (cfA**2 + chA**2) / (2 * Rational(1, 2))
    wA = simplify((av**2 * E0A / 2) * xs**2 + Rational(1, 2))
    okA = simplify(wA - (xs**2 / (8 * ell**2) + Rational(1, 2))) == 0
    # leg B': target w = x^2/ell^2 + 2 (min 2 > 1); w0 = 2, c^2 = 8/(aF^2 ell^2):
    cfB = Rational(6, 5) * sqrt(2) / (sqrt(av**2) * ell)
    chB = Rational(8, 5) * sqrt(2) / (sqrt(av**2) * ell)
    E0B = (cfB**2 + chB**2) / (2 * 2)
    wB = simplify((av**2 * E0B / 2) * xs**2 + 2)
    okB = simplify(wB - (xs**2 / ell**2 + 2)) == 0
    check(
        f"A2_locus_legs_general_sign_{tag}",
        okA and okB
        and sp.ask(sp.Q.positive(E0A)) is True and sp.ask(sp.Q.positive(E0B)) is True,
        f"A2 (verifier legs adopted; aF {'>' if sgn > 0 else '<'} 0 branch, SYMBOLIC "
        "(|aF|, ell)): leg A' realizes w = x^2/(8 ell^2) + 1/2 <= 5/8 < 1 on the whole "
        "cell and leg B' realizes w = x^2/ell^2 + 2 >= 2 > 1, BOTH with E0 > 0 (proven "
        "symbolically); int log w dx is negative on A' and positive on B' (Category-A: log "
        "monotone, integral sign), so I_p = (int log w dx)/aF CHANGES SIGN between the "
        "legs FOR THIS SIGN OF aF too; continuity of the closed form along the connecting "
        "parameter path (E0 > 0, w > 0, disc < 0 throughout) gives an I_p = 0 root with "
        "E0 > 0. With both A2 checks: nonconstant self-consistent solutions exist at EVERY "
        "aF != 0, ell background — the claim's proof coverage now matches its scope. "
        "SCOPE: GEN-QUAD, P1-4D/P1-triad/P3-bulkP1, BASE branch, GENERIC+KMOD0",
    )

check(
    "TD2_P2_no_background_tie",
    expand(diff(exp(0 * p0) * Ltil0, lam)) == 0
    and (2 * lam).subs(lam, 0) == 0 and (1 + 2 * lam).subs(lam, Rational(-1, 2)) == 0,
    "under P2/P3-bulkP2 (aF = 0, aF' = 0) the lam-row is IDENTICALLY zero: NO background tie "
    "exists — the self-consistent locus is ALL backgrounds (degenerate, reported per F-D8, "
    "not suppressed); the P1-instance tie degenerates to this at the T4 blindness loci "
    "(lam = 0 / lam = -1/2). BOOTSTRAP OBSERVATION (recorded, not adopted): the "
    "bootstrap-SHAPED background tie (2 E0 I_p = 0) EMERGES on background-anchored pairings "
    "(aF' != 0) and is ABSENT on the weight-free pairing — the tie is pairing-branch-"
    "RELATIVE, not universal. SCOPE: GEN-QUAD family, enumerated branches, BASE branch",
)

# ============================================================================
# TD3/TD4 — lens classification + on-shell records (recording rows)
# ============================================================================
print("\n--- TD3/TD4: lens classification and on-shell records ---")

check(
    "TD3_lens_classification_record",
    True,
    "[recording row] LENS TALLIES (per representative family, per §2 — every entry scoped "
    "cell+branch+stratum+background): WORKS-GENERICALLY = GEN-QUAD (all 5 branches: solutions "
    "at EVERY admissible background — constants everywhere, nodeless quadratic-w profiles "
    "for aF != 0 (single-minimum WELL for aF > 0 / single-maximum BUMP for aF < 0 — A1 sign "
    "stamp), plus the I_p = 0 nontrivial locus), W1, W2-fs, W3, omega (zero set nonempty at "
    "every background). "
    "CONDITIONAL-ON-BACKGROUND: NONE FOUND among representatives (no §2d instance at this "
    "slice). FAILS-BACKGROUND-ROBUSTLY: NONE (no elimination claimed; F-D2 never engaged). "
    "UNDETERMINED: the R5 leg of all NV-cell representatives (mass functional "
    "NOT-DERIVABLE at this slice — see TD5 record; reported, not suppressed — F-D8)",
)

check(
    "TD4_gate1_onshell_record",
    True,
    "[recording row] GATE-1 ON-SHELL CLOSURE (per stratum): GENERIC — GEN-QUAD/W1/W2-fs are "
    "EXPLICITLY INTEGRATED determined systems (rank-6 initial-data manifold + closed forms; "
    "0 or 1 active integrated moduli rows, rest retained/reported); W3 is per-member "
    "DEGENERATE (recorded). KMOD0 — same solutions restricted to k_mod = 0; the one banked "
    "algebraic row dependency is trivially consistent on the representatives (identity "
    "residual 0) and the L23-orbit quotient is carried (TD1_kmod0 checks). RES-CNEQ0: "
    "CENSUS-REQUIRED, untouched (resonance rule). No existence claim beyond the exhibited "
    "families; no uniqueness claim beyond Picard-local",
)

check(
    "TD4_symmetries_derived_not_assumed",
    all(diff(R_LE[a], f0) == 0 and diff(R_LE[a], h0) == 0 for a in FIELDS),
    "gate-4 current leg (none assumed): the GEN-QUAD components are f0/h0-independent and "
    "x-autonomous (jet-built), so f-shift, h-shift, and x-translation are DERIVED continuous "
    "symmetries on the evaluated stratum; their currents e^{aF p0} f1, e^{aF p0} h1, "
    "E0dens are exactly conserved on-shell (TD1 first-integral checks). omega/W3: no "
    "continuous symmetry claimed (none assumed). SCOPE: named representatives, both READY "
    "strata, all enumerated branches",
)

check(
    "TD4_R14_diagnostic_column",
    True,
    "[diagnostic column ONLY — R14/G12: no bootstrap structure enters any definition] "
    "bootstrap-admissibility reading on the solution sets: ADMISSIBLE-AND-NONTRIVIAL on "
    "P1-side GEN-QUAD (the background seat lam appears as an explored family coordinate AND "
    "the member's own integrated lam-row is a bootstrap-shaped self-consistency equation "
    "2 E0 I_p = 0 tying content to background — EMERGED from the pairing structure, not "
    "imposed); ADMISSIBLE-VACUOUS on P2-side members and on omega/W1/W3 (no background tie; "
    "background remains a free explored coordinate). Recorded for/against evidence: FOR — "
    "the tie emerges unforced on anchored pairings; AGAINST universality — the tie is absent "
    "on P2 (pairing-relative, so the response structure alone does not force a bootstrap)",
)

# ============================================================================
# TD5 — NV & typed duties; gate 5 parity legs; gate 2 typed form
# ============================================================================
print("\n--- TD5: NV/wall/typed duties ---")

# Exact mirror-parity-admissible LE witness (canon instance eps_phi = -1: p0 and p2 vanish
# at both walls x = +-ell for the spatial-mirror static sector; f/bh parities SUPPLIED):
E0w = 1 / (a_p**2 * ell**2)
wall_sub = {w0: Rational(1, 2), w1: 0, cf: 3 / (5 * a_p * ell), ch: 4 / (5 * a_p * ell)}
E0_wall = E0e.subs(wall_sub)
w_wall = wexpr.subs(wall_sub)
p0_wall = (log(w_wall) / a_p)
p2_wall = diff(p0_wall, xs, 2)
check(
    "TD5_parity_admissible_witness",
    simplify(E0_wall - E0w) == 0
    and simplify(w_wall.subs(xs, ell) - 1) == 0
    and simplify(w_wall.subs(xs, -ell) - 1) == 0
    and simplify(p2_wall.subs(xs, ell)) == 0
    and simplify(p2_wall.subs(xs, -ell)) == 0
    and simplify(w_wall.subs(xs, 0) - Rational(1, 2)) == 0,
    "gate-5 canon-parity leg (eps_phi = -1, THEORY-cite C-2026-06-10-2/C-2026-07-04-1; f/bh "
    "parities SUPPLIED, tagged): the trace conditions p0(+-ell) = 0, p2(+-ell) = 0 cut an "
    "EXACT admissible sub-locus of the GEN-QUAD family, NONEMPTY: witness E0 = 1/(aF ell)^2, "
    "c^2 = 1/(aF ell)^2 (c_f, c_h = 3/5, 4/5 of 1/(aF ell)), w = x^2/(2 ell^2) + 1/2 — "
    "w(+-ell) = 1, p2(+-ell) = 0, w > 0 on the whole cell (min 1/2): an exact, everywhere-"
    "regular, mirror-admissible nonconstant solution with both shift currents on. SCOPE: "
    "GEN-QUAD, aF != 0 branches, canon parity instance, BASE branch, all aF/ell backgrounds",
)

check(
    "TD5_NV_wall_duty_record",
    True,
    "[recording row] NV-cell gate-5/R_wall duty on solutions (banked NO-BULK-FORCED-SLOTS): "
    "the NV representatives (W1, W2-fs, W3) are declared with ZERO wall/corner components, "
    "so on the BR-B varied fork their wall equations are vacuous and on the held fork the "
    "consistency conditions are trivial — their gate-5 admissibility on solutions reduces to "
    "the parity/sector-split of the SOLUTIONS' own traces (for W1-affine: odd-parity "
    "p0-traces force p0(0-jet)(wall) = 0, i.e. a_p-intercept = 0 at each wall — exact, "
    "recorded; for W2-fs: the same trace loci as GEN-QUAD). Nonzero NV wall blocks = "
    "Slice-2b (typed). R5 for NV members: the branch VOLUME functional exists (V = int WM/WF "
    "dx per branch), but NO mass functional is DERIVABLE at this slice (no generated "
    "Lagrangian/first-integral energy for a nonvariational member; adopting one would be an "
    "import) — the self-consistent point is reported NOT-DERIVABLE-AT-SLICE-2 with this "
    "reason (F-D8 compliance by explicit report, not suppression); typed to Slice-2b",
)

check(
    "TD5_gate2_J06_record",
    True,
    "[recording row] gate 2 in carrier-free typed form (no source rows touched — F-D7 clean): "
    "per-modulus J06 branches on the representatives: GEN-QUAD under P1-side branches — lam "
    "DETERMINED (nonzero integrated row 2 E0 I_p, active for E0 != 0), k_mod/k10/C RETAINED "
    "and reported (their slots are present with zero components — the explicit retained "
    "branch, not an omission); GEN-QUAD under P2-side — ALL moduli RETAINED; omega — k10 "
    "DETERMINED (row k10 V_M, forcing k10 = 0), rest RETAINED; W1/W2-fs/W3 — all RETAINED. "
    "Character-matching banked (Stage-2); no J13 discriminator slot deleted",
)

check(
    "TD5_jet34_slice2b_requirements",
    True,
    "[typed row, cited] the 4th-order class's Slice-2b requirements (banked TC3, cited): "
    "(1) the jet-3/4 exhaustive parametrization (currently typed via the order-4 anchor "
    "only); (2) wall grade 4 slots — Theta_4 pairs {v_a, v_a'} and the v_a-momentum contains "
    "THIRD jets, so 4th-order sub-families CANNOT self-pair within the jet <= 2 wall "
    "alphabet (EXTENSION-REQUIRED, banked); (3) the Bach-side instance lives here (Route C "
    "cited); (4) per-candidate wall depth from the declared N. None run here (READY-bin "
    "scope)",
)

# ============================================================================
# TD6 — cross-check on the known 2nd-order instance (Route C restricted EH)
# ============================================================================
print("\n--- TD6: Route C restricted-EH cross-check (GR-as-reference lane) ---")

eh_path = os.path.join(HERE, "..", "udt_p4_routeC_shared_static_sector_2026-07-28",
                       "EH_ODE_SYSTEM_FULL.txt")
with open(eh_path, "r") as fh:
    eh_txt = fh.read()
rows = {}
current = None
buf = []
for line in eh_txt.splitlines():
    if line.startswith("== "):
        if current is not None:
            rows[current] = "".join(buf).strip()
        current = line.strip("= ").strip()
        buf = []
    elif line.startswith("#") or not line.strip():
        continue
    else:
        buf.append(line.strip())
if current is not None:
    rows[current] = "".join(buf).strip()

Lam_s = Symbol("Lambda")
t_s, A2 = symbols("t_s A2")
eh_syms = {"lambda": lam, "Lambda": Lam_s, "alpha": alpha_s, "c_E": cE,
           "p0": p0, "p1": p1, "p2": p2, "f0": f0, "f1": f1, "f2": f2,
           "h0": h0, "h1": h1, "h2": h2}
EH_SUB = {Lam_s: 0, p1: 0, p2: 0, f1: 0, f2: 0, h0: t_s**2, h1: 2 * A2 * t_s, h2: 2 * A2**2}
eh_all_zero = True
eh_row_names = sorted(rows.keys())
for rn in eh_row_names:
    expr = sp.sympify(rows[rn].replace("lambda", "lam"), locals=eh_syms)
    val = simplify(expr.subs(EH_SUB))
    if val != 0:
        eh_all_zero = False
        print(f"  EH row {rn}: nonzero residual {val}")
check(
    "TD6_EH_crosscheck_exact_solution",
    eh_all_zero and len(eh_row_names) == 7,
    "the Route C restricted EH+Lambda instance (known 2nd-order member; GR-as-reference "
    "lane; its CONDITIONAL stamps travel — post-scale branch, R12 restrict-vs-vary caveat "
    "banked): the exact family p0 = const, f = const, bh = (A x + B)^2, Lambda = 0 solves "
    "ALL SEVEN restricted rows identically for every (alpha, lam, c_E) background — an exact "
    "consistent sub-family of the overdetermined 7-row/3-field restricted system (regular "
    "where A x + B != 0; the root is a coframe-degeneracy locus, J01, excluded from the "
    "cell). OBSERVATION only; the restricted-EH G3 status under the enumerated pairings "
    "remains an un-run Slice-2b tile (stamped)",
)

# ============================================================================
# TD6 — fork-branch independence of the atlas rows + ledger
# ============================================================================
print("\n--- TD6: fork-branch independence + survivors-map ledger ---")

alpha_absent = all(diff(R_LE[a], alpha_s) == 0 for a in FIELDS) \
    and all(diff(W2fs[a], alpha_s) == 0 for a in FIELDS)
frak_absent = all(diff(R_LE[a], frak_c) == 0 for a in FIELDS)
cE_absent = all(diff(R_LE[a], cE) == 0 for a in FIELDS)
check(
    "TD6_fork_branch_independence",
    alpha_absent and frak_absent and cE_absent and row_integrand == 0,
    "fork-branch independence PROVEN for the atlas rows (F-D3/F-B2 discipline): the "
    "representative components contain no alpha (L8/BR-A: frozen-vs-active branches give the "
    "SAME atlas — on BR-A the extra R_alpha slot is zero/retained, recorded), no completion "
    "label frak_c (L4/BR-C: the atlas is completion-independent; completion cycles/periods "
    "stay NEEDS-COMPLETION-DATA, banked), no c_E (the anchor drops out of the representative "
    "tuples; c_E remains an explicit background coordinate of the depth READOUT p0 = "
    "log(c_E/Q)); the integrated moduli row is a_M-independent (pairing-supply branch-"
    "independence, proven above); BR-B is role-only (banked PROVEN pointwise branch-"
    "independent; both roles recorded per row). SCOPE: the named representatives — NOT a "
    "cell-general claim",
)

# --- Survivors-map ledger (TD6 deliverable) ---
BRANCHES = [
    ("P1-4D", "aF=2lam", "well"),
    ("P1-triad", "aF=1+2lam", "well"),
    ("P2", "aF=0", "affine"),
    ("P3-bulkP2", "bulk aF=0 + wall blocks", "affine"),
    ("P3-bulkP1", "bulk aF=2lam + wall blocks", "well"),
]
STRATA = ["GENERIC", "KMOD0"]
CELLS = ["LOCALLY-EXACT", "NONVARIATIONAL"]

WELL_SOL = ("nodeless quadratic-w family [A1 sign stamp: single-minimum WELL of p0 for "
            "aF > 0 / single-maximum BUMP for aF < 0; nodeless + regular for BOTH signs; "
            "'symmetric' = about the vertex]: e^{aF p0} = (aF^2 E0/2)x^2 + w1 x + w0 "
            "(disc = -aF^2 c^2; E0 >= 0 forced, sign-free), f/h by exact atan quadrature; "
            "6-param field sector (rank-6 + Picard local-exhaustive) x retained moduli x "
            "background (lam, c_E, ell, frak_c); "
            "degenerates to affine atlas exactly on the blindness locus of the branch")
AFF_SOL = ("affine atlas: u = u(0) + u'(0)x, 6-param field sector x ALL moduli retained x "
           "background (lam, c_E, ell, frak_c)")
OMEGA_SOL = ("omega-shape: zero set = {k10 = 0} stratum x fields free x other moduli "
             "retained x all backgrounds (a_M-independent, proven)")
W3_SOL = ("W3: {p0 = const} x f, bh ARBITRARY x moduli retained (per-member DEGENERATE)")

LEDGER_HEADER = ("pairing_branch\tstratum\tG3_cell\trepresentative_family\t"
                 "fork_branch_stamps\tsolution_space_exact\tR5_closure\t"
                 "self_consistent_locus\tlens_class\tgate1_onshell\tgate2_J06_record\t"
                 "gate4_currents\tgate5_wall_duty\tslice2b_handle")
FORKS = ("L4/BR-C: rep frak_c-independent (PROVEN); BR-B: role-only (banked), both roles "
         "recorded; L8/BR-A: rep alpha-independent (PROVEN); pairing supply: a_M-independent "
         "rows (PROVEN); BR-M/BR-CE: OUT (typed NOT-EXHAUSTED upstream)")
R5_LE_P1 = ("V = (2/3)A ell^3 + 2 w0 ell; M = 2 ell E0 [M-instantiation = member energy, "
            "CHOSE/CONDITIONAL — banked mass rows OPEN]; rho = M/V; closure rho V = M on the "
            "SAME solution (F-D6 clean)")
R5_LE_P2 = ("V = 2 ell (weight-free); M = 2 ell E0 [same CHOSE/CONDITIONAL stamp]; "
            "rho = E0; closure on the same solution")
R5_NV = ("V per branch volume exists; MASS FUNCTIONAL NOT-DERIVABLE at this slice for NV "
         "members (no generated energy; adopting one = import) — reported per F-D8, typed "
         "to Slice-2b")
SC_P1 = ("{E0 = 0 (constants)} UNION {I_p = 0, I_p = [G(ell)-G(-ell)]/aF exact}; nonempty "
         "nonconstant at every aF != 0 background (exhibited legs at (aF, ell) = (1, 1) + "
         "general-(aF, ell) BOTH-signs legs [A2 checks] + Category-A continuity)")
SC_P2 = "background tie IDENTICALLY absent -> self-consistent locus = ALL backgrounds (degenerate, reported)"
SC_NV = "NOT-DERIVABLE-AT-SLICE-2 (no derived mass functional for NV members; reported, not suppressed)"
G1_GEN = "EXPLICITLY-INTEGRATED determined (GEN-QUAD/W1/W2-fs); W3 per-member DEGENERATE"
G1_K0 = G1_GEN + "; k_mod = 0 pin; identity residual 0 on reps; L23-orbit quotient carried"
G4 = "derived currents: e^{aF p0} f1, e^{aF p0} h1, E0dens (GEN-QUAD-class); none for omega/W3"
G5_LE = ("canon-parity trace loci exact; nonempty admissible witness w = x^2/(2 ell^2) + 1/2 "
         "(E0 = c^2 = 1/(aF ell)^2); f/bh parities SUPPLIED")
G5_NV = "zero-declared R_wall: varied-fork wall eqs vacuous / held-fork trivial; solution-trace parity loci recorded"
S2B = ("full-cell generality beyond representatives; nonzero wall blocks (P3); carriers under "
       "G09; resonance post-census; 4th-order extension; time-live; restricted-EH G3 tile")

ledger_rows = []
for (br, brdef, shape) in BRANCHES:
    for st in STRATA:
        for cell in CELLS:
            if cell == "LOCALLY-EXACT":
                if shape == "well":
                    rep = "GEN-QUAD (generated free-quadratic, " + brdef + ") + omega [where a_M lam-independent]"
                    sol = WELL_SOL + " | " + OMEGA_SOL
                    r5 = R5_LE_P1
                    sc = SC_P1 + " | omega: no tie (row forces k10 = 0 only)"
                else:
                    rep = "GEN-QUAD at aF=0 (free Lagrangian) + omega"
                    sol = AFF_SOL + " | " + OMEGA_SOL
                    r5 = R5_LE_P2
                    sc = SC_P2
                g5 = G5_LE
            else:
                if shape == "well":
                    rep = "W1 = (p2,f2,h2) [NV defect -2 aF p1 e^{aF p0}, off blindness] + W3"
                    sol = AFF_SOL + " | " + W3_SOL
                else:
                    rep = "W2-fs (well tuple at aF=2lam; banked NV under P2) + W3"
                    sol = (WELL_SOL + " (NO lam-row: moduli slots zero -> no background tie)"
                           + " | " + W3_SOL)
                r5 = R5_NV
                sc = SC_NV
                g5 = G5_NV
            g1 = G1_K0 if st == "KMOD0" else G1_GEN
            lens = ("WORKS-GENERICALLY [rep-scoped; R5 leg UNDETERMINED for NV]"
                    if cell == "NONVARIATIONAL" else "WORKS-GENERICALLY [rep-scoped]")
            ledger_rows.append("\t".join([
                br, st, cell, rep, FORKS, sol, r5, sc, lens, g1,
                "see TD5_gate2_J06_record (per-modulus branches recorded)", G4, g5, S2B,
            ]))

ledger_preamble = (
    "# P4 Route A Slice 2 — SOLUTION ATLAS LEDGER (TD6 survivors map). Contract: "
    "PREREGISTRATION.md. SCOPE STAMP (F-D3, travels with every row): REPRESENTATIVE-"
    "SUB-FAMILY atlas (prereg TD1 clause) — each row's claims are scoped to the named "
    "representative families, NOT a cell census; jet <= 2, BASE branch (constant moduli; "
    "integrated moduli rows), registered stationary presentation, enumerated pairing "
    "branches, READY bin only (RES-CNEQ0 CENSUS-REQUIRED; 4th-order EXTENSION-REQUIRED; "
    "carriers G09/F-D7 out; BR-M/BR-CE typed). NO candidate crowned (F-D1); NO elimination "
    "(F-D2 never engaged); background = free explored dimension (bootstrap-lens frame §2). "
    "Outcome class OD1."
)
ledger_path = os.path.join(HERE, "SOLUTION_ATLAS_LEDGER.tsv")
with open(ledger_path, "w") as fh:
    fh.write(ledger_preamble + "\n" + LEDGER_HEADER + "\n")
    for r in ledger_rows:
        fh.write(r + "\n")

check(
    "TD6_ledger_coverage",
    len(ledger_rows) == 20,
    "[recording row] SOLUTION_ATLAS_LEDGER.tsv written: 20 READY-bin composite cells "
    "(5 branches x {GENERIC, KMOD0} x {LE, NV}), each with representative families, fork "
    "stamps (independence PROVEN where claimed), exact solution spaces, R5 closure, "
    "self-consistent locus, lens class, gate-1/2/4/5 records, Slice-2b handle",
)

# ============================================================================
# Verdict
# ============================================================================
print("\n--- Verdict ---")
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_grd = sum(1 for c in CHECKS if c["kind"] == "citation-guard")
n_pass = sum(1 for c in CHECKS if c["passed"])
n_fail = len(CHECKS) - n_pass
print(f"CHECKS: {n_pass}/{len(CHECKS)} passed ({n_sub} substantive + {n_grd} citation "
      f"guards); {n_fail} failed")

results = {
    "package": "udt_p4_routeA_slice2_solution_legs_2026-07-29",
    "contract": "PREREGISTRATION.md (frozen; bootstrap-lens frame binding)",
    "outcome_class": "OD1 (survivors map populated; no elimination; no conditional-on-"
                     "background find among representatives; bootstrap observations recorded)",
    "amendments": {
        "verdict": "PASS-WITH-REQUIRED-AMENDMENTS (VERIFIER_REPORT.md); both F-D3-class "
                   "stamp repairs; no computation refuted, no falsifier fired",
        "A1": "sign(aF) stamp on the depth-profile SHAPE: p0''(vertex) ~ sign(aF) — WELL "
              "(single minimum) for aF > 0, BUMP (single maximum) for aF < 0 (inside the "
              "explored range: P1-4D lam < 0, P1-triad lam < -1/2); 'symmetric' = about "
              "the vertex; E0 >= 0 / regularity / nodelessness / closed form are sign-free "
              "(verified at free real aF). New checks: A1_well_zero_residual_signfree, "
              "A1_vertex_curvature_sign_of_aF, A1_bump_instance_regular_nodeless. "
              "FOURTH instance of the named F-D3/F-S3 scope class (mechanism-caught).",
        "A2": "proof-coverage repair on the locus-nonemptiness claim: TRUE at every "
              "aF != 0 background but previously exhibited only at (aF, ell) = (1, 1), "
              "and the 'w <= 5/8 => I_p < 0' leg flips for aF < 0. Verifier's "
              "general-(aF, ell) both-signs symbolic legs adopted: "
              "A2_locus_legs_general_sign_pos/_neg; witness stamp installed on the "
              "TD2 sentence; continuity leg stays Category-A.",
        "dead_code": "verifier note N4: unused legA_ok/bound_A removed (cosmetic).",
    },
    "checks_total": len(CHECKS),
    "checks_substantive": n_sub,
    "checks_guards": n_grd,
    "checks_failed": n_fail,
    "checks": CHECKS,
}
with open(os.path.join(HERE, "routeA_slice2_results.json"), "w") as fh:
    json.dump(results, fh, indent=1, sort_keys=False)

sys.exit(0 if n_fail == 0 else 1)
