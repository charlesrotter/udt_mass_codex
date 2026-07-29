#!/usr/bin/env python3
"""P4 Route A Slice 2b — full-cell generality + the branched mass legs (TE1-TE6).

Contract: udt_p4_routeA_slice2b_full_cell_2026-07-29/PREREGISTRATION.md (frozen first;
Charles's rulings R1 (labeled mass-definition branches M-GEN / M-WALL / M-DENS, derived-
typed from BANKED structure only, NO branch promoted) and R2 (moduli bookkeeping carried
BOTH ways: INTEGRATED int WM R_mu dx = 0 vs POINTWISE R_mu = 0; the divergence map is a
first-class deliverable); the BOOTSTRAP-LENS frame (Slice-2 prereg 2) governs in full).
Exact SymPy, zero-residual checks + exact quadrature identities, deterministic (no floats,
no randomness, no network, no numeric solvers, no GPU), single CPU process, bounded.
Exit 0 iff every check passes (F-D5 inherited).

SLICE-2B BOUNDARY (binding): NO candidate crowned, NO mass rule promoted (F-E1), NO
invented mass kernel (F-E2 -- every mass functional below is derived-typed from banked
structure, with its provenance stamp), every claim carries cell + pairing + mass-branch +
bookkeeping-branch + stratum + BACKGROUND stamps (F-E3, the named class, FOUR prior
catches), no Slice-2 result quoted branch-free (F-E4 -- the banked tie is INTEGRATED-
branch), no fork pre-decided (F-E5); the inherited F-D1..F-D8 travel in full.

AMENDMENT PASS (2026-07-29, per VERIFIER_REPORT.md verdict PASS-WITH-REQUIRED-
AMENDMENTS; record = CORRECTION_LAYER.md):
- A1 (F-E3 -- the FIFTH named-class catch): the ledger R2-survivor and tie-status
  columns now carry their in-column QUADRATIC CLASS stamp (read cell-generally the
  unstamped columns were false: the general member's lam-row is a_F' int p0 W_F Ltil dx,
  survivors uncharacterized -- typed in-column now).
- A2 (even-handedness, DECISION-RELEVANT-R1): M-GEN-eq extended to the W1 class under
  the SAME banked principle that granted W2-fs (weight-free aF = 0 generator; verifier
  derivation adopted as the zero-residual check A2_W1_MGENeq_extension; value
  +-2 ell Ltil0, orientation-sign labeled).
- A3: the dispatch's unsubstantiated "self-caught dropped term" claim (M-DENS-coord
  law) is WITHDRAWN in CORRECTION_LAYER.md (no package record exists; the shipped law
  is verifier-confirmed correct) -- no script change.
- A4: TE2_MWALL_P2_zero re-coded derivation-backed (verifier's affine-atlas derivation
  adopted); TE3_tie_fate_map strengthened to a real computation; dead masses_vanish
  removed; honest split restated everywhere counts appear.
- ADOPTED verifier strengthenings (credited): ADOPTED_atlas_exhaustive_energy_ODE
  (w'^2 law => w exactly quadratic -- the atlas is EXHAUSTIVE on the class),
  ADOPTED_Ip_signchange_exact (in-package exact sign-change certificate, evalf-free),
  ADOPTED_consensus_Ip_closed_form (I_p = -4 + log 4 + 4 sqrt(3) pi/9 exactly).

BANKED INPUTS (cited; recomputed as consistency only, never re-derived as new):
- Slice 2 (d110fe0): SOLUTION_ATLAS_LEDGER.tsv + EXACT_DERIVATION.md -- the GEN-QUAD
  closed form (quadratic-w family), affine atlas, omega stratum, W3 degeneracy; the
  sign-stamped A1 emergence; the tie 2E0*I_p = 0 (INTEGRATED branch) + its P2 absence;
  the NV UNDETERMINED reason; the M = 2*ell*E0 CHOSE stamp (now the M-GEN branch label).
- Stage 3 (21d589c): gate-cut map; pairing branches (P1-4D aF=2lam; P1-triad aF=1+2lam;
  P2 aF=0; P3-bulkP2/P3-bulkP1 = declared bulk + wall blocks); TC3 gate-5 wall/corner
  slot census (M-WALL's typing source); the corrected anchored-log iff.
- Stage 2 (2c0e7cc): stratified R_PW; k_mod = 0 identity; BR-M typed NOT-EXHAUSTED
  (the R2 POINTWISE branch here is run AS A LABELED BRANCH per Charles's ruling, on the
  BASE-branch constant-moduli arena -- not a silent adoption of BR-M's field fork).
- Stage 1: POSED_INVERSE_PROBLEM.md (R5 same-solution rule; 1.5 pairings; J07-J11);
  SIX_GATE_SPECS.md.
- native_action_final_adjudication_2026-07-18: the typed closure-identity rows
  (rho+S=2rho4 vs rho+p_par SEPARATE -- both G09-carrier-gated, typed OUT here, never
  merged); G09 carrier = POSIT (F-D7); G12.
- WR-L / Xmax / proper-density canon senses (C-2026-07-09-1 lineage): the PROPER density
  sense (density per unit branch volume) used as one labeled M-DENS sub-sense.
Conventions: registered stationary one-parameter presentation, fields (phi, f, bh) jets
p0..p2/f0..f2/h0..h2; moduli (lam, k_mod, k10, C) constant on BASE; anchored weight
W_F = e^{aF p0}; cell x in [-ell, ell].
"""

import json
import os
import sys

import sympy as sp
from sympy import (Function, Matrix, Rational, Symbol, symbols, exp, log, atan, atanh,
                   sqrt, diff, expand, simplify, eye, zeros, integrate, cancel)

HERE = os.path.dirname(os.path.abspath(__file__))

CHECKS = []

CITATION_GUARDS = {
    # guards = definitional unpacking / recording-table / citation / typing rows,
    # never counted as residual computations (honest split, house rule)
    "S0_ready_bin_citation",
    "TE1_pmixed_and_nonquadratic_obstruction",
    "R2_survivor_inclusion_theorem",
    "TE2_mass_branch_availability_table",
    "TE3_bookkeeping_divergence_map",
    "TE4_completion_typing_record",
    "TE5_ledgers_written",
    "TE6_next_surface_written",
}


def check(name, ok, detail=""):
    kind = "citation-guard" if name in CITATION_GUARDS else "substantive"
    CHECKS.append({"name": name, "passed": bool(ok), "detail": detail, "kind": kind})
    status = "PASS" if ok else "FAIL"
    tag = " [guard]" if kind == "citation-guard" else ""
    print(f"[{status}]{tag} {name}" + (f" -- {detail}" if detail else ""))


# ============================================================================
# Jet machinery (registered stationary presentation; BASE branch) -- reused
# from the banked Slice-2 script machinery (cited).
# ============================================================================
print("--- Jet machinery (Slice-2 machinery reused) ---")

FIELDS = ["p", "f", "h"]
VFIELDS = ["vp", "vf", "vh"]
JMAX = 6
J = {a: symbols(f"{a}0:{JMAX + 1}") for a in FIELDS}
JV = {a: symbols(f"{a}0:{JMAX + 1}") for a in VFIELDS}
lam, kmod = symbols("lam k_mod")
k10s = Symbol("k10")
cE = Symbol("c_E", positive=True)
alpha_s = Symbol("alpha")
frak_c = Symbol("frak_c")

ALL_CHAINS = [list(J[a]) for a in FIELDS]
ALL_CHAINS_V = ALL_CHAINS + [list(JV[a]) for a in VFIELDS]


def _Dx_over(chains):
    def D(expr):
        out = sp.Integer(0)
        for chain in chains:
            for k in range(len(chain) - 1):
                d = diff(expr, chain[k])
                if d != 0:
                    out += d * chain[k + 1]
        return out
    return D


Dx = _Dx_over(ALL_CHAINS)
DxV = _Dx_over(ALL_CHAINS_V)


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
vp0, vf0, vh0 = JV["vp"][0], JV["vf"][0], JV["vh"][0]
vp1, vf1, vh1 = JV["vp"][1], JV["vf"][1], JV["vh"][1]

a_w = Symbol("a_w")            # symbolic anchored exponent aF (2lam / 1+2lam / 0)
WFa = exp(a_w * p0)

# ============================================================================
# S0 -- banked footing recomputed (consistency, cited)
# ============================================================================
print("\n--- S0: banked footing recomputed (consistency) ---")

Ltil0 = (p1**2 + f1**2 + h1**2) / 2
R_LE = {a: expand(exp(-a_w * p0) * Euler(WFa * Ltil0, a, 2)) for a in FIELDS}
R_p_stated = a_w * (f1**2 + h1**2 - p1**2) / 2 - p2
R_f_stated = -(a_w * p1 * f1 + f2)
R_h_stated = -(a_w * p1 * h1 + h2)
ONSHELL = {p2: a_w * (f1**2 + h1**2 - p1**2) / 2, f2: -a_w * p1 * f1, h2: -a_w * p1 * h1}
E0dens = expand(WFa * Ltil0)
check(
    "S0_genquad_footing_recomputed",
    expand(R_LE["p"] - R_p_stated) == 0 and expand(R_LE["f"] - R_f_stated) == 0
    and expand(R_LE["h"] - R_h_stated) == 0
    and simplify(Dx(E0dens).subs(ONSHELL)) == 0
    and simplify(Dx(WFa * f1).subs(ONSHELL)) == 0,
    "banked Slice-2 footing recomputed at symbolic aF (consistency, F-D4): the GEN-QUAD "
    "tuple from the generated construction, and the first integrals E0dens = e^{aF p0} "
    "Ltil0, e^{aF p0} f1 conserved on-shell (banked TD1 checks re-instantiated)",
)

check(
    "S0_ready_bin_citation",
    True,
    "[citation] READY bin (banked Stage-3 surface, unchanged): 20 composite cells = 5 "
    "pairing branches (P1-4D aF=2lam; P1-triad aF=1+2lam; P2 aF=0; P3-bulkP2 bulk aF=0; "
    "P3-bulkP1 bulk aF=2lam; P3 = declared bulk + wall blocks) x {GENERIC, KMOD0} x "
    "{LOCALLY-EXACT, NONVARIATIONAL}. OUT (typed only, inherited): RES-CNEQ0 "
    "(CENSUS-REQUIRED), 4th-order class (EXTENSION-REQUIRED), carriers (G09/F-D7), "
    "BR-CE, time-live. The R2 POINTWISE branch below is Charles's ruled bookkeeping "
    "branch on the BASE constant-moduli arena (labeled), not the BR-M field fork "
    "(which stays typed NOT-EXHAUSTED)",
)

# ============================================================================
# TE1 -- full-cell generality: structural theorems at ARBITRARY member
# ============================================================================
print("\n--- TE1: full-cell generality (arbitrary LE member; NV typing) ---")

# --- The general LE member: arbitrary generating density Ltil(p0,p1,f0,f1,h0,h1) ---
Lt = Function("Ltil")(p0, p1, f0, f1, h0, h1)
S_gen = WFa * Lt
EulerS = {a: expand(Euler(S_gen, a, 2)) for a in FIELDS}
E_S = expand(p1 * diff(S_gen, p1) + f1 * diff(S_gen, f1) + h1 * diff(S_gen, h1) - S_gen)
beltrami = expand(Dx(E_S) + p1 * EulerS["p"] + f1 * EulerS["f"] + h1 * EulerS["h"])
check(
    "TE1_general_energy_first_integral",
    beltrami == 0,
    "FULL-CELL THEOREM (LE cells, arbitrary member): for the ARBITRARY generating density "
    "Ltil(p0,p1,f0,f1,h0,h1) (the cell's whole census scope at jet <= 2) and S = W_F Ltil, "
    "the energy E := sum_a u_a1 dS/du_a1 - S obeys Dx(E) = -sum_a u_a1 E_a(S) IDENTICALLY "
    "(zero residual with Ltil an arbitrary SymPy Function): E is an exact first integral on "
    "EVERY solution of EVERY LE-cell member -- the Slice-2 representative first integral "
    "extended to the full cell. The f/h SHIFT currents do NOT extend (they exist exactly on "
    "the sub-class dLtil/df0 = dLtil/dh0 = 0 -- the general member has one guaranteed first "
    "integral, not three). SCOPE: all five pairing branches (aF symbolic), LE cells, "
    "GENERIC+KMOD0, jet <= 2, BASE branch, x-autonomous census members, all backgrounds",
)

sym_ok = all(
    expand(diff(EulerS[a], J[b][2]) + diff(S_gen, J[a][1], J[b][1])) == 0
    for a in FIELDS for b in FIELDS
)
check(
    "TE1_general_leading_symbol_dichotomy",
    sym_ok,
    "FULL-CELL THEOREM (LE cells, arbitrary member): dE_a(S)/du_b2 = -d2S/du_a1 du_b1 = "
    "-W_F Hess(Ltil)_ab IDENTICALLY (arbitrary Ltil), and W_F > 0 (banked T0), so the "
    "DETERMINEDNESS DICHOTOMY is pairing-independent: a member is in solved form u'' = "
    "F(u, u') iff det Hess_{u'}(Ltil) != 0, and there (Picard, Category-A cited) its LOCAL "
    "solution space is EXACTLY the 6-dim initial-data manifold -- the banked rank-6 "
    "exhaustiveness extended from the representative to EVERY nondegenerate-Hessian member "
    "of the cell. Degenerate-Hessian members form the complementary stratum (per-member "
    "typing; witness next). SCOPE: LE cells, all branches, both strata, jet <= 2, BASE",
)

L_deg = p1**2 / 2
S_deg = WFa * L_deg
deg_f = expand(Euler(S_deg, "f", 2))
deg_h = expand(Euler(S_deg, "h", 2))
Hess_deg = Matrix(3, 3, lambda i, j: diff(L_deg, [p1, f1, h1][i], [p1, f1, h1][j]))
check(
    "TE1_degenerate_LE_instance",
    deg_f == 0 and deg_h == 0 and Hess_deg.det() == 0 and Hess_deg.rank() == 1,
    "degenerate-stratum witness (exact): the LE member Ltil = p1^2/2 has Hessian rank 1 "
    "(det 0); its f/h rows vanish IDENTICALLY -- an UNDERDETERMINED member (f, bh arbitrary "
    "functions on its zero set), the LE-cell analog of the banked NV W3 degeneracy: the "
    "degenerate stratum is POPULATED in the LE cell too. SCOPE: LE cells, all branches, "
    "both strata, all backgrounds (member-level fact)",
)

# --- The fiberwise-quadratic p-unmixed class: exact closed form (extends GEN-QUAD) ---
xs = Symbol("x")
a_r = Symbol("a_r", real=True, nonzero=True)     # free real aF, both signs
gp = Symbol("g_p", nonzero=True)
gf_, gh_, gx_ = symbols("g_f g_h g_x", real=True)
w0 = Symbol("w0", positive=True)
w1 = Symbol("w1", real=True)
cf, ch = symbols("c_f c_h", real=True)
ell = Symbol("ell", positive=True)

DeltaG = gf_ * gh_ - gx_**2                       # det of the (f,h) block (nonzero)
LtG = gp * p1**2 / 2 + (gf_ * f1**2 + 2 * gx_ * f1 * h1 + gh_ * h1**2) / 2
S_G = exp(a_r * p0) * LtG
R_G = {a: expand(exp(-a_r * p0) * Euler(S_G, a, 2)) for a in FIELDS}

qc = (gh_ * cf**2 - 2 * gx_ * cf * ch + gf_ * ch**2) / DeltaG   # c^T G^{-1} c
E0G = (gp * w1**2 / a_r**2 + qc) / (2 * w0)
AG = a_r**2 * E0G / (2 * gp)
wG = AG * xs**2 + w1 * xs + w0
p0x = log(wG) / a_r
p1x = diff(p0x, xs)
p2x = diff(p0x, xs, 2)
f1x = (gh_ * cf - gx_ * ch) / (DeltaG * wG)
h1x = (-gx_ * cf + gf_ * ch) / (DeltaG * wG)
f2x = diff(f1x, xs)
h2x = diff(h1x, xs)
SUBSOL = {p0: p0x, p1: p1x, p2: p2x, f1: f1x, f2: f2x, h1: h1x, h2: h2x}
res_G = {a: simplify(R_G[a].subs(SUBSOL)) for a in FIELDS}
E_S_G = expand(p1 * diff(S_G, p1) + f1 * diff(S_G, f1) + h1 * diff(S_G, h1) - S_G)
E_onsol = simplify(E_S_G.subs(SUBSOL) - E0G)
check(
    "TE1_quadratic_class_closed_form",
    all(res_G[a] == 0 for a in FIELDS) and E_onsol == 0,
    "EXACT SOLUTION FAMILY, full fiberwise-quadratic p-unmixed class (Ltil = g_p p1^2/2 + "
    "(f1,h1) G_fh (f1,h1)^T/2, constant g_p != 0, det G_fh != 0 -- extends GEN-QUAD = the "
    "g_p = 1, G_fh = I instance): e^{aF p0} = w(x) = A x^2 + w1 x + w0 with A = aF^2 E0/"
    "(2 g_p), (f', h') = G_fh^{-1}(c_f, c_h)/w, E0 = (g_p w1^2/aF^2 + c^T G_fh^{-1} c)/"
    "(2 w0): ALL THREE field equations vanish identically at free real aF of both signs, "
    "arbitrary real (g_f, g_h, g_x), and E(solution) = E0 exactly (the TE1 energy = W_F "
    "Ltil on this class). 6 parameters (w0, w1, c_f, c_h, f(0), h(0)) x retained moduli x "
    "background. SCOPE: LE cells, aF != 0 branches, BASE, both strata, all backgrounds",
)

# ADOPTED (verifier strengthening, credited -- VERIFIER_REPORT.md Duty 2(a)): the
# atlas-EXHAUSTIVENESS argument via the reduced energy ODE, closing the quantifier gap
# under every "exactly/only" survivor claim on the class.
wfun = Function("w", positive=True)(xs)
E0c = Symbol("E0c")
E_from_sub = (exp(a_r * p0) * LtG).subs({
    p0: log(wfun) / a_r, p1: wfun.diff(xs) / (a_r * wfun),
    f1: (gh_ * cf - gx_ * ch) / (DeltaG * wfun),
    h1: (-gx_ * cf + gf_ * ch) / (DeltaG * wfun)})
E_class = gp * wfun.diff(xs)**2 / (2 * a_r**2 * wfun) + qc / (2 * wfun)
enODE = wfun.diff(xs)**2 - (2 * a_r**2 / gp) * (E0c * wfun - qc / 2)
check(
    "ADOPTED_atlas_exhaustive_energy_ODE",
    cancel(sp.simplify(E_from_sub - E_class)) == 0
    and cancel(enODE - (2 * a_r**2 * wfun / gp) * (E_class - E0c)) == 0
    and expand(enODE.diff(xs)
               - 2 * wfun.diff(xs) * (wfun.diff(xs, 2) - a_r**2 * E0c / gp)) == 0,
    "ATLAS EXHAUSTIVENESS on the fiberwise-quadratic p-unmixed class (verifier-derived, "
    "adopted, credited): on the class the conserved TE1 energy reads E = g_p w'^2/"
    "(2 aF^2 w) + c^T G^{-1} c/(2 w) (zero residual vs the substituted on-shell energy), "
    "so E = E0 is the ODE w'^2 = (2 aF^2/g_p)(E0 w - qc/2); differentiating gives "
    "d/dx[ODE] = 2 w' (w'' - aF^2 E0/g_p) IDENTICALLY: every NONCONSTANT solution has "
    "w'' = aF^2 E0/g_p constant, i.e. w EXACTLY quadratic with A = aF^2 E0/(2 g_p); the "
    "constants are the w' == 0 stratum. With the 6 parameters matching the Picard data "
    "count, the quadratic atlas is the WHOLE solution space of the class -- the "
    "'exactly/only' survivor quantifiers below are grounded, not asserted. SCOPE: LE "
    "cells, aF != 0 branches, fiberwise-quadratic p-unmixed class, BASE, all backgrounds",
)

disc_G = expand(w1**2 - 4 * AG * w0)
disc_identity = simplify(disc_G + (a_r**2 / gp) * qc)
# definiteness leg (diagonal-positive instance; general definite class by constant
# congruence of the (f,h) block -- Category-A linear algebra, cited):
possub = {gp: Symbol("gpp", positive=True), gf_: Symbol("gfp", positive=True),
          gh_: Symbol("ghp", positive=True), gx_: 0}
E0_pos = E0G.subs(possub)
disc_pos = expand(disc_G.subs(possub))
check(
    "TE1_definiteness_scoped_sign_structure",
    disc_identity == 0
    and sp.ask(sp.Q.nonnegative(E0_pos)) is True
    and sp.ask(sp.Q.nonpositive(disc_pos)) is True,
    "FULL-CELL REFINEMENT of the banked emergent sign structure (observed, not imposed): "
    "disc(w) = -(aF^2/g_p) c^T G_fh^{-1} c EXACTLY. On the POSITIVE-DEFINITE sub-class "
    "(g_p > 0, G_fh > 0; proven at the diagonal-positive instance, general definite case "
    "by constant congruence of the (f,h) block -- Category-A cited): E0 >= 0 and "
    "disc <= 0 (nodeless, globally regular) -- the banked GEN-QUAD emergence (E0 >= 0, "
    "nodelessness, A1 well/bump sign law) is the G = I instance of the DEFINITE class and "
    "carries to all of it. On the INDEFINITE sub-class the sign structure FAILS (witnesses "
    "next): the banked emergence is DEFINITENESS-SCOPED, not cell-general -- a full-cell "
    "structure finding. No member is excluded (characterize, not filter). SCOPE: LE cells, "
    "aF != 0 branches, fiberwise-quadratic class, BASE, all backgrounds",
)

IND = {gp: 1, gf_: -1, gh_: 1, gx_: 0, a_r: 1, w0: 1, w1: 0, cf: 2, ch: 0}
w_ind = wG.subs(IND)                     # expect 1 - x^2
E0_ind = E0G.subs(IND)                   # expect -2
res_ind = {a: simplify(R_G[a].subs(SUBSOL).subs(IND)) for a in FIELDS}
disc_ind = disc_G.subs(IND)
check(
    "TE1_indefinite_noded_witness",
    all(res_ind[a] == 0 for a in FIELDS)
    and expand(w_ind - (1 - xs**2)) == 0 and E0_ind == -2 and disc_ind == 4
    and w_ind.subs(xs, 1) == 0 and w_ind.subs(xs, -1) == 0,
    "INDEFINITE witness (exact, rational): g_p = 1, G_fh = diag(-1, 1), aF = 1, w0 = 1, "
    "w1 = 0, c = (2, 0): zero residual in all three equations with E0 = -2 < 0, w = "
    "1 - x^2, disc = +4 > 0 -- a NODED member (w -> 0, depth p0 -> -infinity at x = +-1): "
    "regular exactly on cells with ell < 1 (node radius = the real root of w, closed "
    "form). NEGATIVE-energy, noded solutions POPULATE the indefinite sub-class: E0 >= 0 "
    "and nodelessness are NOT cell-general. SCOPE: LE cells, aF != 0 branches (background "
    "point aF = 1 shown; family symbolic), BASE, both strata",
)

INDA = {gp: 1, gf_: -1, gh_: 1, gx_: 0, a_r: 1, w0: 2, w1: 1, cf: 1, ch: 0}
w_inda = wG.subs(INDA)                   # expect x + 2 (A = 0)
E0_inda = E0G.subs(INDA)                 # expect 0
res_inda = {a: simplify(R_G[a].subs(SUBSOL).subs(INDA)) for a in FIELDS}
check(
    "TE1_indefinite_E0zero_nonconstant_witness",
    all(res_inda[a] == 0 for a in FIELDS)
    and expand(w_inda - (xs + 2)) == 0 and E0_inda == 0,
    "second indefinite witness (exact, rational): same class, w0 = 2, w1 = 1, c = (1, 0): "
    "zero residual with E0 = 0 and w = x + 2 -- a NONCONSTANT (affine-w, p0 = log(x+2)) "
    "member with EXACTLY ZERO energy (node at x = -2, outside any cell with ell < 2). On "
    "the banked definite representative E0 = 0 forced constants (sum of squares); at full "
    "cell the E0 = 0 stratum contains NONCONSTANT members on the indefinite sub-class -- "
    "load-bearing for the R2 pointwise-survivor structure below. SCOPE: LE cells, aF != 0 "
    "branches, BASE, both strata",
)

check(
    "TE1_pmixed_and_nonquadratic_obstruction",
    True,
    "[typing row -- the honest generality boundary, stamped, not silently narrowed] "
    "(1) p-MIXED quadratic members (cross terms p1 f1 / p1 h1): the shift currents still "
    "reduce f1, h1 affinely in p1, but the w-substitution no longer linearizes the p-row "
    "(the anchored weight couples to p0 only -- weight anisotropy): closed form NOT "
    "obtained; the TE1 general theorems (energy + dichotomy) still cover these members. "
    "(2) NON-QUADRATIC members: no closed-form quadrature in general (Liouville-class "
    "obstruction); the exact full-cell theory = the energy first integral + the "
    "determinedness dichotomy + Picard local structure (checks above) -- exact and "
    "cell-general, but not a closed-form atlas. (3) NV cells: the general member is an "
    "arbitrary component tuple (source form); its zero set realizes an essentially "
    "arbitrary 2nd-order system (universality): NO general solution theory exists beyond "
    "the leading-symbol dichotomy (pairing-independent by banked T0); the banked witnesses "
    "(W1 affine/determined, W2-fs quadratic-w, W3 degenerate) are instances, recomputed "
    "below. These are OBSTRUCTION statements (TE1's honest boundary), not scope cuts",
)

Delta_W1 = {"p": WFa * p2, "f": WFa * f2, "h": WFa * h2}
sym_W1 = Matrix(3, 3, lambda i, j: diff(Delta_W1[FIELDS[i]], J[FIELDS[j]][2]))
W3_fh_rows_zero = all(diff(p1, J[a][k]) == 0 for a in ["f", "h"] for k in range(3))
check(
    "TE1_NV_fullcell_structure",
    sym_W1 == WFa * eye(3) and W3_fh_rows_zero,
    "NV-cell full-cell structure (witness legs recomputed, consistency): W1 = (p2, f2, h2) "
    "has leading symbol W_F * Id (rank 3: determined; zero set = the affine atlas, banked); "
    "W3 = (p1, 0, 0) has identically-zero f/h rows (degenerate stratum, banked). The "
    "determinedness dichotomy of TE1 is the complete PAIRING-INDEPENDENT structure theorem "
    "available for the NV cell at full generality; the solution ATLAS is member-by-member "
    "(obstruction row above). SCOPE: NV cells, all branches, both strata, jet <= 2, BASE",
)

# ============================================================================
# R2 -- the bookkeeping branches (INTEGRATED vs POINTWISE), full-cell
# ============================================================================
print("\n--- R2: bookkeeping branches (INTEGRATED vs POINTWISE) ---")

check(
    "R2_survivor_inclusion_theorem",
    True,
    "[definitional unpacking] INCLUSION (every cell, every modulus): R_mu = 0 pointwise "
    "implies int WM R_mu dx = 0 (integral of the zero function), so the POINTWISE survivor "
    "set is CONTAINED in the INTEGRATED survivor set in every cell x background; the "
    "divergence content is exactly WHERE the inclusion is strict (computed below). SCOPE: "
    "all READY cells, both strata, all backgrounds, BASE arena (constant moduli) with the "
    "pointwise row read as Charles's R2 branch",
)

aFlam = Function("a_F")(lam)
S_lam = exp(aFlam * p0) * Lt             # arbitrary lam-independent Ltil
row_lam = expand(diff(S_lam, lam) - diff(aFlam, lam) * p0 * S_lam)
check(
    "R2_general_lambda_row_aFprime_control",
    row_lam == 0,
    "FULL-CELL THEOREM (LE cells, arbitrary lam-independent member): the generated lam-row "
    "integrand is d(W_F Ltil)/dlam = a_F'(lam) * p0 * (W_F Ltil) IDENTICALLY (arbitrary "
    "Ltil, arbitrary a_F(lam)): INTEGRATED row = a_F' int p0 W_F Ltil dx = 0; POINTWISE "
    "row = a_F' p0 W_F Ltil = 0 at every x. BOTH rows are IDENTICALLY ABSENT iff a_F' = 0 "
    "(the P2/P3-bulkP2 side and the banked blindness loci): the banked pairing-RELATIVITY "
    "of the background tie is FULL-CELL GENERAL, on both bookkeeping branches. "
    "(lam-DEPENDENT Ltil adds int W_F dLtil/dlam dx -- typed, labeled, out of the "
    "lam-independent census row.) SCOPE: LE cells, all branches, BASE, all backgrounds",
)

lamrow_quad = simplify((2 * p0 * exp(a_r * p0) * LtG).subs(SUBSOL) - 2 * E0G * p0x)
check(
    "R2_quadclass_integrated_survivors",
    lamrow_quad == 0,
    "on the quadratic class W_F Ltil = E0 on-shell (TE1), so with the enumerated P1 "
    "instances (a_F' = 2, banked) the INTEGRATED lam-row is exactly 2 E0 I_p = 0, I_p = "
    "int_{-ell}^{ell} p0 dx -- the banked Slice-2 tie recovered as the g_p, G_fh-INDEPENDENT "
    "full-class law [F-E4: this tie is INTEGRATED-branch]. INTEGRATED survivors (P1-side LE, "
    "quadratic class) = {E0 = 0} UNION {I_p = 0}; the nonconstant I_p = 0 locus is nonempty "
    "at every aF != 0 background (banked A2 legs + Category-A continuity, cited; now ALSO "
    "certified in-package exactly -- ADOPTED_Ip_signchange_exact below). SCOPE: "
    "P1-4D/P1-triad/P3-bulkP1 LE cells, GENERIC+KMOD0, INTEGRATED branch, all backgrounds",
)

# ADOPTED (verifier strengthening, credited -- VERIFIER_REPORT.md Duty 2(a), made
# evalf-free for the derivation script's purity rule): an EXACT sign-change certificate
# for I_p on a massive family, independent of the banked-A2 citation.
dalzell = integrate(xs**4 * (1 - xs)**4 / (1 + xs**2), (xs, 0, 1))
Ip_c1 = integrate(log(xs**2 / 2 + Rational(1, 2)), (xs, -1, 1))
Ip_c6 = integrate(log(18 * xs**2 + Rational(1, 2)), (xs, -1, 1))
Ip_c6_closed = 2 * log(Rational(37, 2)) - 4 + Rational(2, 3) * atan(6)
FAM = {gp: 1, gf_: 1, gh_: 1, gx_: 0, a_r: 1, w0: Rational(1, 2), w1: 0, ch: 0}
E0_fam_c1 = E0G.subs(FAM).subs(cf, 1)
E0_fam_c6 = E0G.subs(FAM).subs(cf, 6)
e_partial = sum(Rational(1, sp.factorial(k)) for k in range(5))          # = 65/24
e_tail = Rational(1, 120) * Rational(6, 5)                               # geometric bound
check(
    "ADOPTED_Ip_signchange_exact",
    simplify(dalzell - (Rational(22, 7) - sp.pi)) == 0
    and Rational(22, 7) < 4
    and simplify(Ip_c1 - (sp.pi - 4)) == 0
    and simplify(Ip_c6 - Ip_c6_closed) == 0
    and E0_fam_c1 == 1 and E0_fam_c6 == 36
    and e_partial == Rational(65, 24) and e_tail == Rational(1, 100)
    and (e_partial + e_tail) < Rational(11, 4)
    and Rational(121, 16) < Rational(37, 2)
    and sp.atan(6).is_positive is True,
    "EXACT I_p sign-change certificate (verifier leg adopted, credited; evalf-free): on "
    "the family a_F = 1, g = I, w1 = 0, w0 = 1/2, ell = 1 (E0 = c^2, all E0 > 0): "
    "I_p(c=1) = int log(x^2/2 + 1/2) dx = pi - 4 < 0 EXACTLY (pi < 22/7 by the Dalzell "
    "integral int_0^1 x^4(1-x)^4/(1+x^2) dx = 22/7 - pi with manifestly nonnegative "
    "integrand -- Category-A named; 22/7 < 4); I_p(c=6) = 2 log(37/2) - 4 + (2/3) atan 6 "
    "> 0 EXACTLY (e < 65/24 + 1/100 = 1631/600 < 11/4 by the positive factorial series' "
    "geometric tail bound -- rational arithmetic verified -- so e^2 < 121/16 < 37/2, "
    "hence log(37/2) > 2; atan 6 > 0). Sign change on a connected E0 > 0 family + "
    "continuity (Category-A) => a MASSIVE I_p = 0 member EXISTS: the strict-inclusion "
    "existence certificate now stands IN-PACKAGE and EXACT, independent of the banked-A2 "
    "citation (which concurs). SCOPE: P1-side LE cells, quadratic class, INTEGRATED "
    "branch, background point aF = 1, ell = 1 shown (banked A2 covers the general "
    "background claim)",
)

# pointwise: 2 E0 p0(x) = 0 for all x. Leg (i): p0 == 0 => w == 1 => A = 0, w1 = 0,
# w0 = 1; and E0 = 2 g_p A / aF^2, so A = 0 => E0 = 0. Leg (ii): E0 = 0 directly.
E0_from_A = expand(E0G - 2 * gp * AG / a_r**2)
wpoly = sp.Poly(wG - 1, xs)
coeffs_w1 = wpoly.all_coeffs()           # [A, w1, w0 - 1]
sol_p0zero = sp.solve([sp.Eq(c, 0) for c in [coeffs_w1[0], coeffs_w1[1]]], [cf, w1],
                      dict=True)
check(
    "R2_quadclass_pointwise_survivors",
    cancel(E0_from_A) == 0 and coeffs_w1[1] == w1 and cancel(coeffs_w1[2] - (w0 - 1)) == 0
    and cancel(coeffs_w1[0] - AG) == 0,
    "POINTWISE branch (P1-side LE, quadratic class): the row 2 E0 p0(x) = 0 at EVERY x "
    "forces E0 = 0 EXACTLY -- either E0 = 0 directly, or p0 == 0, i.e. w == 1 identically, "
    "whose x^2-coefficient A = aF^2 E0/(2 g_p) = 0 forces E0 = 0 again (E0 = 2 g_p A/aF^2, "
    "zero residual). POINTWISE survivors = {E0 = 0}: on the DEFINITE sub-class these are "
    "exactly the CONSTANT solutions (banked sum-of-squares); on the INDEFINITE sub-class "
    "they include NONCONSTANT affine-w members (TE1 witness w = x + 2, E0 = 0). The "
    "massive (E0 != 0) INTEGRATED locus {I_p = 0} does NOT survive the pointwise branch: "
    "the inclusion is STRICT here. SCOPE: P1-4D/P1-triad/P3-bulkP1 LE cells, "
    "GENERIC+KMOD0, POINTWISE branch, all backgrounds",
)

VM = Symbol("V_M", positive=True)
sol_int = sp.solve(sp.Eq(k10s * VM, 0), k10s)
sol_pw = sp.solve(sp.Eq(k10s, 0), k10s)
P2row = expand(diff(exp(0 * p0) * Lt, lam))
check(
    "R2_omega_convergence_P2_vacuity",
    sol_int == [0] and sol_pw == [0] and P2row == 0,
    "CONVERGENCE rows of the bookkeeping fork: (a) the omega k10-row -- INTEGRATED "
    "k10 * int WM dx = 0 forces k10 = 0 (positive integrand, Category-A), POINTWISE "
    "R_k10 = k10 = 0 forces k10 = 0 (k10 constant on BASE): the two branches produce the "
    "IDENTICAL survivor stratum {k10 = 0} (omega's banked LE cells, all backgrounds); "
    "(b) the P2-side lam-row is IDENTICALLY zero for EVERY lam-independent member (aF' = "
    "0), so both branches are vacuous and agree (survivors = all backgrounds, degenerate, "
    "reported); (c) NV representatives declare zero moduli slots -- both branches vacuous, "
    "agree (general NV members with nonzero moduli slots: typed, inclusion holds, "
    "strictness member-dependent). SCOPE: as stamped per leg, BASE, both strata",
)

# ============================================================================
# TE2 -- the branched mass legs (R1): availability typing + per-branch values
# ============================================================================
print("\n--- TE2: branched mass legs (M-GEN / M-WALL / M-DENS) ---")

check(
    "TE2_mass_branch_availability_table",
    True,
    "[typing row -- availability DERIVED from banked structure only, F-E2 clean; NO branch "
    "promoted, F-E1] M-GEN (generated-energy functional; provenance: the TE1 first "
    "integral = the Slice-2 CHOSE instantiation now labeled): AVAILABLE on LE cells "
    "(generator exists; energy derived); NOT AVAILABLE on NV cells (no generator -- the "
    "banked Helmholtz defect, re-derived below); labeled sub-branch M-GEN-eq (the TUPLE'S "
    "OWN autonomy first integral, where the tuple coincides with a generated tuple of the "
    "ENUMERATED weight menu -- provenance: banked TD1_W2fs_same_zero_set + TD1_LE_energy_"
    "first_integral; A2 amendment: the earlier anchored-only restriction had NO stated "
    "derivation and is REMOVED -- even-handed under the same banked principle): AVAILABLE "
    "for W2-fs-class (anchored aF = 2lam generator) AND for W1-class (weight-free aF = 0 "
    "generator -- A2_W1_MGENeq_extension below; DECISION-RELEVANT-R1); NOT for W3 (no "
    "generated-tuple identity in banked structure -- a refusal, not an invented "
    "discriminator, F-E2). M-WALL "
    "(boundary/wall reading; provenance: the banked TC3 gate-5 N=2 by-parts census -- wall "
    "momenta pi_a = dS/du_a1; re-derived full-cell below): AVAILABLE on LE cells as the "
    "p-slot momentum wall difference [pi_p] (on the quadratic class the f/h-slot "
    "differences vanish IDENTICALLY -- the p-slot is the only nonvacuous slot, DERIVED; "
    "beyond the shift-invariant class the p-slot selection is a LABELED sub-choice, "
    "stamped); on NV cells = the member's OWN declared R_wall (banked reps declare ZERO "
    "wall blocks => M-WALL = 0, trivially determined; nonzero-wall NV members typed OPEN). "
    "Under the canon parity instance eps_phi = -1 the v_p wall SLOT is parity-killed, so "
    "M-WALL is a TRACE functional of the solution, not a paired boundary charge in that "
    "sector (stamped). M-DENS (integrated-density reading; provenance: the R5 triple's V "
    "[branch volume, THEORY] and rho senses with M inferred): TWO labeled sub-senses kept "
    "separate -- M-DENS-coord (rho = E0dens read in the registered chart) and M-DENS-"
    "proper (rho = E0dens/W_F, the proper/per-branch-volume sense, WR-L/Xmax canon "
    "lineage); AVAILABLE on LE cells (E0dens derived); NOT on NV cells (no derived "
    "density). The banked carrier-stress closure rows rho+S=2rho4 and rho+p_par=2(rho2_par"
    "+rho4_par) are G09-CARRIER-GATED: typed OUT here, kept SEPARATE, never merged "
    "(F-D7). No other mass definition is derived-typed at this slice; none invented",
)

MGEN_G = integrate(E0G, (xs, -ell, ell))
check(
    "TE2_MGEN_general_value",
    simplify(MGEN_G - 2 * ell * E0G) == 0 and beltrami == 0,
    "M-GEN value: E is constant on-shell (TE1 theorem, arbitrary LE member), so M-GEN := "
    "int_{-ell}^{ell} E dx = 2 ell E for EVERY LE-cell member -- closed form at FULL "
    "generality; on the quadratic class M-GEN = 2 ell E0 (recovering the banked Slice-2 "
    "CHOSE value as the M-GEN branch value). Sign: E0 >= 0 on the definite sub-class "
    "(banked emergence, definiteness-scoped -- TE1); E0 < 0 members exist on the "
    "indefinite sub-class (witness E0 = -2): M-GEN is NOT sign-definite at full cell. "
    "SCOPE: LE cells, all branches, both strata, mass-branch M-GEN, both R2 branches "
    "(the functional is R2-independent; its SURVIVOR domain is not), all backgrounds",
)

# by-parts identity at arbitrary member (the TC3 N=2 census re-derived full-cell):
deltaS = expand(
    diff(S_gen, p0) * vp0 + diff(S_gen, p1) * vp1
    + diff(S_gen, f0) * vf0 + diff(S_gen, f1) * vf1
    + diff(S_gen, h0) * vh0 + diff(S_gen, h1) * vh1
)
Theta2 = diff(S_gen, p1) * vp0 + diff(S_gen, f1) * vf0 + diff(S_gen, h1) * vh0
byparts = expand(
    deltaS - (EulerS["p"] * vp0 + EulerS["f"] * vf0 + EulerS["h"] * vh0) - DxV(Theta2)
)
pi_p_sol = (exp(a_r * p0) * gp * p1).subs(SUBSOL)      # = g_p w'/aF on the solution
MWALL_G = simplify(pi_p_sol.subs(xs, ell) - pi_p_sol.subs(xs, -ell))
pi_f_sol = simplify((exp(a_r * p0) * (gf_ * f1 + gx_ * h1)).subs(SUBSOL))
pi_h_sol = simplify((exp(a_r * p0) * (gx_ * f1 + gh_ * h1)).subs(SUBSOL))
check(
    "TE2_MWALL_theta2_and_pslot",
    byparts == 0
    and simplify(MWALL_G - 2 * a_r * ell * E0G) == 0
    and diff(pi_f_sol, xs) == 0 and diff(pi_h_sol, xs) == 0,
    "M-WALL derivation: (a) the N=2 by-parts identity deltaS-integrand = sum_a E_a(S) v_a "
    "+ Dx(Theta2), Theta2 = sum_a pi_a v_a, pi_a = dS/du_a1, holds IDENTICALLY for the "
    "ARBITRARY LE member (the banked TC3 census re-derived at full cell -- M-WALL's typing "
    "source); (b) on the quadratic class the f/h wall momenta are the CONSERVED shift "
    "currents (pi_f = c_f, pi_h = c_h exactly -- x-derivative zero), so their wall "
    "differences VANISH identically: the p-slot is the ONLY nonvacuous wall-difference "
    "slot (derived, not chosen, on this class); (c) M-WALL := pi_p(ell) - pi_p(-ell) = "
    "g_p [w'/aF] = 4 A ell g_p/aF = 2 aF ell E0 EXACTLY (g_p and G_fh cancel): "
    "*** M-WALL = aF * M-GEN *** on the whole fiberwise-quadratic p-unmixed class -- the "
    "exact mass-branch divergence law. SCOPE: LE cells, aF != 0 branches, quadratic "
    "class (beyond it the relation is member-dependent, typed), mass-branch M-WALL, "
    "BASE, all backgrounds",
)

# A4 (amendment): re-coded DERIVATION-BACKED (the prior coding was tautological --
# verifier catch; the verifier's own derivation V_MWALL_P2_zero_derived adopted).
rows_P2 = [expand(Euler(LtG, a, 2)) for a in FIELDS]          # aF = 0: S = LtG, W_F = 1
sol_P2 = sp.solve([sp.Eq(r, 0) for r in rows_P2], [p2, f2, h2], dict=True)
AFF0 = {p2: 0, f2: 0, h2: 0}
check(
    "TE2_MWALL_P2_zero",
    sol_P2 == [{p2: 0, f2: 0, h2: 0}]
    and all(expand(r.subs(AFF0)) == 0 for r in rows_P2)
    and simplify(Dx(gp * p1).subs(AFF0)) == 0
    and simplify(Dx(LtG).subs(AFF0)) == 0,
    "M-WALL at aF = 0 (P2/P3-bulkP2 LE cells) -- DERIVED (A4; verifier derivation "
    "adopted): the Euler rows of S = Ltil_G at aF = 0 are (-g_p p2, -(G(f2,h2))_i); with "
    "g_p != 0, det G != 0 they FORCE the affine atlas u'' = 0 (unique solve, zero "
    "residual on re-substitution); there pi_p = g_p p1 is CONSTANT (Dx = 0 on-shell), so "
    "M-WALL = pi_p(ell) - pi_p(-ell) = 0 IDENTICALLY, while the energy E = Ltil_G is "
    "conserved (Dx = 0 on-shell) and free, so M-GEN = 2 ell E0 is free: MAXIMAL "
    "mass-branch divergence on the weight-free side (M-WALL reads zero mass on every "
    "P2-side LE solution; M-GEN does not); the quadratic-class law M-WALL = aF * M-GEN "
    "is consistent with this limit (both sides -> 0 with aF at fixed M-GEN). SCOPE: "
    "P2/P3-bulkP2 LE cells, mass branches M-WALL vs M-GEN, BASE, all backgrounds",
)

MDENS_proper = integrate((E0G / wG) * wG, (xs, -ell, ell))
check(
    "TE2_MDENS_proper_calibration",
    simplify(MDENS_proper - MGEN_G) == 0,
    "M-DENS-proper: rho_proper = E0dens/W_F (the proper/per-branch-volume density sense, "
    "WR-L/Xmax canon lineage), M := int rho_proper dV_branch = int (E0/w) w dx = 2 ell E0 "
    "= M-GEN IDENTICALLY -- the proper-density sense REPRODUCES the generated-energy "
    "branch exactly on the whole quadratic class: the prereg's cross-branch CALIBRATION "
    "observation, exact. SCOPE: LE cells, all aF (at aF = 0 both = 2 ell E0), mass "
    "branches M-DENS-proper vs M-GEN, BASE, all backgrounds",
)

V_G = integrate(wG, (xs, -ell, ell))
V_stated = Rational(2, 3) * AG * ell**3 + 2 * w0 * ell
MDENS_coord = E0G * V_G
div_coord = cancel(MDENS_coord - MGEN_G - E0G * (V_G - 2 * ell))
div_form = cancel((V_G - 2 * ell) - (Rational(2, 3) * AG * ell**3 + 2 * (w0 - 1) * ell))
check(
    "TE2_MDENS_coord_divergence",
    simplify(V_G - V_stated) == 0 and div_coord == 0 and div_form == 0,
    "M-DENS-coord: rho_coord = E0dens = E0 (the on-shell constant registered-chart "
    "density), V = int W_F dx = (2/3) A ell^3 + 2 w0 ell (the branch's own volume, "
    "THEORY), M := rho_coord * V = E0 V; the divergence from M-GEN is EXACTLY "
    "M-DENS-coord - M-GEN = E0 (V - 2 ell), V - 2 ell = (2/3) A ell^3 + 2 (w0 - 1) ell "
    "-- zero iff E0 = 0 or V = 2 ell (the unit-mean-weight SOLUTION locus; on the P2 "
    "side V = 2 ell identically, so the senses agree there). On the INTEGRATED tie "
    "locus {I_p = 0, E0 > 0, nonconstant} Jensen's inequality (log strictly concave -- "
    "named Category-A step) gives int log w = 0 => V > 2 ell STRICTLY: the coord sense "
    "STRICTLY exceeds M-GEN on every massive self-consistent definite member. SCOPE: "
    "LE cells, mass branch M-DENS (both sub-senses labeled), BASE, all backgrounds",
)

# NV re-grades:
ONSHELL_W1 = {p2: 0, f2: 0, h2: 0}
w1_cons = all(simplify(Dx(J[a][1]).subs(ONSHELL_W1)) == 0 for a in FIELDS)
E_W2fs = exp(2 * lam * p0) * Ltil0
dE_W2fs = simplify(Dx(E_W2fs).subs({p2: 2 * lam * (f1**2 + h1**2 - p1**2) / 2,
                                    f2: -2 * lam * p1 * f1, h2: -2 * lam * p1 * h1}))
defect_W1 = expand(diff(Delta_W1["p"], p1) + diff(Delta_W1["p"], p1)
                   - 2 * Dx(diff(Delta_W1["p"], p2)))
check(
    "TE2_NV_regrade_per_branch",
    w1_cons and dE_W2fs == 0 and simplify(defect_W1 / WFa + 2 * a_w * p1) == 0,
    "NV-cell mass re-grade PER BRANCH (the banked UNDETERMINED re-graded honestly): "
    "*** W1-class (P1-side NV; affine atlas): M-GEN proper STILL-UNDETERMINED -- the "
    "Helmholtz defect -2 aF p1 e^{aF p0} != 0 obstructs a generator under the cell's OWN "
    "anchored pairing (re-derived); p1, f1, h1 are EACH conserved on the affine atlas "
    "(derived); DETERMINED-under-M-GEN-eq (A2 amendment, even-handed with the W2-fs "
    "grant -- see A2_W1_MGENeq_extension next: the W1 tuple IS the weight-free aF = 0 "
    "generated tuple, so its energy is the tuple's own): M = +-2 ell Ltil0, sign per "
    "tuple orientation (labeled); member stays NV under P1 (stamped); "
    "DECISION-RELEVANT-R1. The earlier refusal reason ('conserved 1-jets exist but none "
    "structure-selected') UNDERCOUNTED banked structure: the aF = 0 generator IS the "
    "selector, exactly parallel to W2-fs's aF = 2lam generator (verifier catch, A2); "
    "M-WALL DETERMINED = 0 (zero declared wall blocks -- trivially; an artifact of the "
    "declaration, stamped); M-DENS STILL-UNDETERMINED (no derived density). "
    "*** W2-fs-class (P2-side NV; quadratic-w atlas): the tuple's OWN "
    "autonomy first integral E0 = e^{2 lam p0} Ltil0 is conserved on-shell (zero residual "
    "-- banked identity recomputed), so under the LABELED sub-branch M-GEN-eq the cell is "
    "DETERMINED-under-M-GEN-eq: M = 2 ell E0 on the quadratic-w atlas (provenance: banked "
    "tuple identity; NOT a pairing-generated energy -- the member stays NV under P2, "
    "stamped); M-WALL DETERMINED = 0 (same trivial reason); M-DENS STILL-UNDETERMINED. "
    "*** W3: zero set {p0 const} x (f, bh arbitrary): M-GEN/M-GEN-eq/M-DENS undetermined "
    "(no generated-tuple identity in banked structure); M-WALL = 0. NO branch promoted; "
    "each verdict carries its branch label (F-E1). SCOPE: NV cells per branch as "
    "stamped, both strata, both R2 branches (moduli slots zero: R2-vacuous), all "
    "backgrounds",
)

# A2 (amendment): the M-GEN-eq extension to the W1 class -- the verifier's derivation
# (V_W1_is_weightfree_generated_tuple) adopted as zero-residual checks. Even-handedness:
# the SAME banked principle that granted W2-fs (the tuple coincides with an enumerated
# generated tuple, so its energy is the tuple's own) applies to W1 at aF = 0.
gen_w1 = {a: expand(Euler(-Ltil0, a, 2)) for a in FIELDS}
E_w1gen = expand(p1 * diff(-Ltil0, p1) + f1 * diff(-Ltil0, f1)
                 + h1 * diff(-Ltil0, h1) - (-Ltil0))
g_null = Function("g_null")(p0, f0, h0)
L_null = Dx(g_null)
E_null = expand(p1 * diff(L_null, p1) + f1 * diff(L_null, f1)
                + h1 * diff(L_null, h1) - L_null)
check(
    "A2_W1_MGENeq_extension",
    expand(gen_w1["p"] - p2) == 0 and expand(gen_w1["f"] - f2) == 0
    and expand(gen_w1["h"] - h2) == 0
    and simplify(E_w1gen + Ltil0) == 0
    and simplify(Dx(-Ltil0).subs(ONSHELL_W1)) == 0
    and expand(Euler(Ltil0, "p", 2) + p2) == 0
    and E_null == 0,
    "A2 (M-GEN-eq extended to W1; verifier derivation adopted, credited; "
    "DECISION-RELEVANT-R1 -- flagged for Charles): (a) the W1 tuple (p2, f2, h2) "
    "(banked; the anchored presentation W_F (p2, f2, h2) has the IDENTICAL zero set, "
    "W_F > 0) IS Euler(-Ltil0) EXACTLY -- the weight-free (aF = 0) generated tuple of "
    "the ENUMERATED menu (banked record: 'W1 = (p2, f2, h2) ... LE at a_F = 0'); (b) the "
    "generator is unique up to null Lagrangians: for the autonomous jet-local null "
    "Lagrangian Dx(g(p0, f0, h0)) the energy is IDENTICALLY ZERO (zero residual), so the "
    "generated energy is well-defined up to tuple ORIENTATION (+W1 vs -W1, same zero "
    "set: generator -Ltil0 vs +Ltil0, energy -Ltil0 vs +Ltil0) and the shared "
    "additive-constant normalization convention (SAME freedom rides the W2-fs grant -- "
    "even-handedness preserved, labeled); (c) the energy -Ltil0 is CONSERVED on the "
    "affine atlas (zero residual): M-GEN-eq(W1) = +-2 ell Ltil0, sign per orientation "
    "(labeled sub-choice); provenance = the SAME banked tuple-identity principle as the "
    "W2-fs grant (F-E2 clean: nothing invented -- the availability table's anchored-only "
    "restriction is what lacked a derivation and is removed). The member stays NV under "
    "P1 (pairing-relative, stamped). SCOPE: NV cells, W1-class, P1-side branches, affine "
    "atlas, mass sub-branch M-GEN-eq, both R2 branches (moduli slots zero), all "
    "backgrounds",
)

rho_gen = cancel(MGEN_G / V_G)
rho_wall = cancel((2 * a_r * ell * E0G) / V_G)
rho_coordv = E0G
closure_ok = (
    simplify(rho_gen * V_G - MGEN_G) == 0
    and simplify(rho_wall * V_G - 2 * a_r * ell * E0G) == 0
    and simplify(rho_coordv * V_G - MDENS_coord) == 0
)
check(
    "TE2_R5_triples_rerun",
    closure_ok,
    "R5 triples RE-RUN per mass branch on ONE quadratic-class solution (same-solution "
    "discipline, F-D6 inherited): (V, M, rho) with V = (2/3)A ell^3 + 2 w0 ell and "
    "M-GEN: M = 2 ell E0, rho = M/V; M-WALL: M = 2 aF ell E0, rho = M/V (note rho "
    "NEGATIVE for aF < 0 on definite members -- branch-labeled); M-DENS-coord: rho = E0, "
    "M = E0 V; M-DENS-proper: identical to M-GEN. Closure rho V = M holds EXACTLY in "
    "every branch on the same solution. NV cells: under M-WALL the triple is (V, 0, 0), "
    "closure trivial; under M-GEN/M-DENS no triple exists (undetermined; W2-fs under "
    "M-GEN-eq: same triple as M-GEN; W1 under M-GEN-eq (A2): M = +-2 ell Ltil0 on the "
    "affine atlas, triple closes definitionally rho := M/V, same-solution). SCOPE: per "
    "branch as labeled, LE cells aF != 0 (P2: V = 2 ell), BASE, all backgrounds",
)

# ============================================================================
# TE3 -- the three divergence maps
# ============================================================================
print("\n--- TE3: divergence maps ---")

rel_wall = expand(2 * a_r * ell * E0G - a_r * MGEN_G)
agree_wall_locus = cancel((2 * a_r * ell * E0G - MGEN_G) - 2 * ell * E0G * (a_r - 1))
check(
    "TE3_massbranch_divergence_map",
    rel_wall == 0
    and agree_wall_locus == 0
    and simplify(MDENS_proper - MGEN_G) == 0
    and div_coord == 0,
    "MASS-BRANCH DIVERGENCE MAP (exact, quadratic class, LE cells, BASE, all "
    "backgrounds): (1) M-DENS-proper == M-GEN IDENTICALLY (agreement everywhere -- the "
    "calibration row); (2) M-WALL = aF * M-GEN: M-WALL - M-GEN = 2 ell E0 (aF - 1) -- "
    "agreement EXACTLY on {E0 = 0} UNION {aF = 1} (aF = 1 is a BACKGROUND locus: "
    "P1-4D lam = 1/2, P1-triad lam = 0); P2 side (aF = 0): M-WALL == 0, maximal "
    "divergence; (3) M-DENS-coord - M-GEN = E0 (V - 2 ell) -- agreement exactly on "
    "{E0 = 0} UNION {V = 2 ell} (a SOLUTION locus, not a background locus; P2 side: "
    "identical agreement); (4) ALL FOUR readings agree simultaneously on {E0 = 0} UNION "
    "({aF = 1} AND {V = 2 ell}) -- a nonzero-mass consensus locus EXISTS (exact witness "
    "next check) but lies OFF the integrated moduli-row survivor set (Jensen strict, "
    "Category-A: V = 2 ell nonconstant => I_p != 0). No disagreement is resolved; no "
    "branch preferred (F-E1)",
)

WIT4 = {gp: 1, gf_: 1, gh_: 1, gx_: 0, a_r: 1, w0: Rational(1, 2), w1: 0,
        cf: sqrt(3), ch: 0, ell: 1}
E0_w4 = E0G.subs(WIT4)
V_w4 = V_G.subs(WIT4)
m_gen4 = (2 * ell * E0G).subs(WIT4)
m_wall4 = (2 * a_r * ell * E0G).subs(WIT4)
m_dc4 = MDENS_coord.subs(WIT4)
m_dp4 = MDENS_proper.subs(WIT4)
res_w4 = {a: simplify(R_G[a].subs(SUBSOL).subs(WIT4)) for a in FIELDS}
check(
    "TE3_allfour_agreement_witness",
    all(res_w4[a] == 0 for a in FIELDS)
    and E0_w4 == 3 and V_w4 == 2
    and m_gen4 == 6 and m_wall4 == 6 and m_dc4 == 6 and simplify(m_dp4 - 6) == 0
    and AG.subs(WIT4) == Rational(3, 2),
    "ALL-FOUR consensus WITNESS (exact): at the background point aF = 1 (P1-4D "
    "lam = 1/2 / P1-triad lam = 0), ell = 1, the member w = (3/2)x^2 + 1/2 (g = I, "
    "w1 = 0, c = (sqrt(3), 0)) is an exact solution (zero residual) with E0 = 3, "
    "V = 2 = 2 ell, and M-GEN = M-WALL = M-DENS-coord = M-DENS-proper = 6: all four "
    "labeled readings agree at NONZERO mass -- an OE3-flavored convergence observation, "
    "NOT a promotion (F-E1). Caveat (stamped): this member is nonconstant with "
    "V = 2 ell, so I_p < 0 (Jensen strict, named Category-A) and the INTEGRATED lam-row "
    "2 E0 I_p != 0: the consensus point lies OFF the integrated self-consistent locus "
    "(field-sector solution only; on the POINTWISE branch it is likewise not a "
    "survivor). SCOPE: LE cells, anchored branches at the aF = 1 background, quadratic "
    "class, all four mass branches, both R2 branches (as stamped), GENERIC+KMOD0",
)

# ADOPTED (verifier strengthening, credited -- VERIFIER_REPORT.md Duty 2(b)(iv)): the
# consensus witness's off-survivor stamp by EXACT closed-form quadrature (stronger than
# the Jensen citation, which remains valid), evalf-free.
IpW_exact = integrate(log(Rational(3, 2) * xs**2 + Rational(1, 2)), (xs, -1, 1))
IpW_closed = -4 + log(4) + 4 * sqrt(3) * sp.pi / 9
taylor_e75 = sum(Rational(7, 5)**k / sp.factorial(k) for k in range(6))
check(
    "ADOPTED_consensus_Ip_closed_form",
    simplify(IpW_exact - IpW_closed) == 0
    and taylor_e75 > 4
    and Rational(26, 15)**2 > 3
    and Rational(7, 5) + 4 * Rational(26, 15) * Rational(22, 7) / 9 < 4
    and simplify(dalzell - (Rational(22, 7) - sp.pi)) == 0,
    "EXACT consensus-witness closed form (verifier quadrature adopted, credited): "
    "I_p(witness w = (3/2)x^2 + 1/2, ell = 1) = -4 + log 4 + 4 sqrt(3) pi / 9 EXACTLY "
    "(closed form, zero residual), and it is NEGATIVE by the exact rational chain: "
    "log 4 < 7/5 (e^{7/5} exceeds its positive-series partial sum "
    "sum_{k<=5} (7/5)^k/k! > 4 -- rational arithmetic verified), sqrt(3) < 26/15 "
    "(675 < 676), pi < 22/7 (Dalzell, above), so log 4 + 4 sqrt(3) pi/9 < 7/5 + "
    "2288/945 = 3611/945 < 4. Hence 2 E0 I_p != 0 at the witness: the all-four "
    "consensus point is OFF the integrated survivor set by EXACT quadrature (Jensen "
    "citation no longer load-bearing there), and E0 = 3 != 0 keeps it off the pointwise "
    "set -- the OE3-flavored observation's stamp is now certificate-backed. SCOPE: LE "
    "cells, anchored branches at the aF = 1 background, quadratic class, INTEGRATED + "
    "POINTWISE stamps as given, all backgrounds",
)

SGN = {a_r: -1, ell: 1}
mgen_neg = (2 * ell * E0G).subs(SGN).subs(possub)
mwall_neg = (2 * a_r * ell * E0G).subs(SGN).subs(possub)
check(
    "TE3_sign_divergence_aFneg",
    sp.ask(sp.Q.nonnegative(mgen_neg)) is True
    and sp.ask(sp.Q.nonpositive(mwall_neg)) is True
    and E0_ind == -2,
    "SIGN structure of the map (A1 sign stamp carried): on the DEFINITE sub-class at "
    "aF < 0 (the BUMP side of the banked A1 law; inside the explored background range: "
    "P1-4D lam < 0, P1-triad lam < -1/2) M-GEN >= 0 while M-WALL = aF M-GEN <= 0: the "
    "wall reading assigns NEGATIVE mass to every definite bump-side member with E0 > 0 "
    "-- a sign divergence, branch-labeled, observed not adjudicated. On the INDEFINITE "
    "sub-class E0 < 0 members flip every branch's sign (witness E0 = -2). SCOPE: LE "
    "cells, quadratic class, mass branches as labeled, BASE, background stamps as given",
)

check(
    "TE3_bookkeeping_divergence_map",
    True,
    "[recording row -- computed in R2 above] BOOKKEEPING DIVERGENCE MAP: STRICT "
    "divergence on P1-side LE cells (P1-4D/P1-triad/P3-bulkP1 bulk; aF' != 0): "
    "INTEGRATED survivors = {E0 = 0} UNION {I_p = 0 massive locus, nonempty at every "
    "aF != 0 background}; POINTWISE survivors = {E0 = 0} only -- the fork DECIDES "
    "whether any massive self-consistent member exists (under EVERY mass branch, since "
    "all branch masses vanish iff E0 = 0 -- TE3 tie row). AGREEMENT on: omega k10-rows "
    "(both {k10 = 0}), P2-side LE lam-rows (both vacuous), NV representatives (zero "
    "moduli slots, both vacuous). General NV members with nonzero moduli slots: "
    "inclusion holds, strictness member-dependent (typed). SCOPE: per cell as stamped, "
    "BASE arena, both strata, all backgrounds; no fork decided (F-E5)",
)

# A4 (amendment): strengthened to a REAL computation (the prior coding was two trivial
# solves + one reused identity -- verifier catch). Content now: (i) each of the four
# branch masses vanishes IFF E0 = 0 (solved with the declared positivity/nonzero
# assumptions); (ii) the integrated lam-row 2 E0 I_p rewrites through EACH branch mass
# with a NONZERO factor (zero-residual identities); (iii) the pointwise analog forces
# E0 = 0 (the R2 leg, cross-cited by its own computation E0 = 2 g_p A / aF^2).
E0v = Symbol("E0v", real=True)
Ip_s = Symbol("I_p")
MASS_FORMS = {
    "MGEN": 2 * ell * E0v,               # ell > 0
    "MWALL": 2 * a_r * ell * E0v,        # a_r != 0, ell > 0
    "MDENScoord": E0v * VM,              # V_M > 0 on regular cells
    "MDENSproper": 2 * ell * E0v,        # == M-GEN (calibration)
}
mass_zero_solves = {k: sp.solve(sp.Eq(v, 0), E0v) for k, v in MASS_FORMS.items()}
row_sym = 2 * E0v * Ip_s
row_rewrites = [
    cancel(row_sym - (MASS_FORMS["MGEN"] / ell) * Ip_s),
    cancel(row_sym - (MASS_FORMS["MWALL"] / (a_r * ell)) * Ip_s),
    cancel(row_sym - (2 * MASS_FORMS["MDENScoord"] / VM) * Ip_s),
    cancel(row_sym - (MASS_FORMS["MDENSproper"] / ell) * Ip_s),
]
check(
    "TE3_tie_fate_map",
    all(v == [0] for v in mass_zero_solves.values())
    and all(r == 0 for r in row_rewrites)
    and lamrow_quad == 0 and cancel(E0_from_A) == 0,
    "TIE-FATE MAP (the banked 2 E0 I_p = 0 tie per branch combination; bootstrap "
    "observation ONLY, per lens -- nothing adopted; A4-strengthened: mass-zero solves "
    "under the declared assumptions (ell > 0, aF != 0, V > 0) + zero-residual "
    "nonzero-factor rewrites of the row through EACH branch mass + the pointwise "
    "E0-forcing leg cross-cited by its own computation): *** INTEGRATED x {M-GEN, M-WALL, "
    "M-DENS-coord, M-DENS-proper}: the tie reads (branch mass) * I_p = 0 up to nonzero "
    "factors -- M-GEN = 2 ell E0, M-WALL = 2 aF ell E0 (aF != 0), M-DENS-coord = E0 V "
    "(V > 0 on regular cells, Category-A), M-DENS-proper = M-GEN: each vanishes IFF "
    "E0 = 0 (ell > 0), so the tie's zero locus is MASS-BRANCH-ROBUST and its nontrivial "
    "branch {I_p = 0, E0 != 0} carries NONZERO mass under all four readings "
    "simultaneously: the bootstrap-shaped tie couples MASS ITSELF to the background "
    "seat, whichever labeled definition is used. *** POINTWISE x every mass branch: the "
    "analog 2 E0 p0(x) = 0 forces E0 = 0 (R2), so every pointwise survivor is MASSLESS "
    "under all four readings: the tie's massive branch is ABSENT -- it exists ONLY on "
    "the INTEGRATED side of the fork [F-E4 made structural]. *** P2-side (aF' = 0): no "
    "tie and no analog on either branch (absent; blindness-loci degeneration carried). "
    "SCOPE: P1-side LE cells (quadratic class) vs P2-side, both strata, both R2 "
    "branches, all backgrounds; observation only, settling is Charles's",
)

# ============================================================================
# TE4 -- wall/corner/completion structure of the full-generality solutions
# ============================================================================
print("\n--- TE4: wall traces, J09 node loci, completion typing ---")

w_wallP = wG.subs(xs, ell)
w_wallM = wG.subs(xs, -ell)
wp_wallP = diff(wG, xs).subs(xs, ell)
wp_wallM = diff(wG, xs).subs(xs, -ell)
Fq = Symbol("A_q", positive=True)
s_pos = sqrt(4 * Fq * w0 - w1**2)
wq = Fq * xs**2 + w1 * xs + w0
F_atan = (2 * cf / s_pos) * atan((2 * Fq * xs + w1) / s_pos)
parity_sub = {gp: 1, gf_: 1, gh_: 1, gx_: 0, a_r: 1,
              w0: Rational(1, 2), w1: 0, cf: Rational(3, 5) / ell, ch: Rational(4, 5) / ell}
w_par = wG.subs(parity_sub)
p2_par = p2x.subs(parity_sub)
check(
    "TE4_wall_traces_and_parity",
    expand(w_wallP - (AG * ell**2 + w1 * ell + w0)) == 0
    and expand(wp_wallP - (2 * AG * ell + w1)) == 0
    and simplify(diff(F_atan, xs) - cf / wq) == 0
    and simplify(w_par.subs(xs, ell) - 1) == 0
    and simplify(p2_par.subs(xs, ell)) == 0 and simplify(p2_par.subs(xs, -ell)) == 0,
    "the full-generality solutions DETERMINE their wall data (gate-5 duty, filled): "
    "wall traces in exact closed form -- w(+-ell) = A ell^2 +- w1 ell + w0, w'(+-ell) = "
    "+-2A ell + w1, hence p0/p1/p2 traces and the M-WALL momenta traces; f/h traces by "
    "the exact atan quadrature (disc < 0 class; verified by differentiation); the banked "
    "canon-parity witness (eps_phi = -1: p0(+-ell) = p2(+-ell) = 0 with w = x^2/(2 ell^2) "
    "+ 1/2) re-cut inside the G-class at the g = I point (recomputed). f/bh parities "
    "remain SUPPLIED (tagged). SCOPE: LE cells, quadratic class, aF != 0, BASE, canon "
    "parity instance for the witness leg, all backgrounds",
)

root_p = (-w1 + sqrt(disc_G)) / (2 * AG)
w_at_root = simplify(wG.subs(xs, root_p))
check(
    "TE4_J09_node_locus",
    w_at_root == 0 and w_ind.subs(xs, 1) == 0
    and sp.ask(sp.Q.nonpositive(disc_pos)) is True,
    "J09 (null/type-changing strata) FILLED where the solutions determine it: the "
    "coframe-degeneracy/node locus of a quadratic-class member is EXACTLY the real-root "
    "set of w -- empty iff disc = -(aF^2/g_p) c^T G^{-1} c < 0 (the whole definite "
    "sub-class: no continuation needed, J09 vacuous -- filled), and at disc > 0 the node "
    "radii x_node = (-w1 +- sqrt(disc))/(2A) are exact closed forms (w(x_node) = 0, zero "
    "residual): the J09 domain declaration is 'cell regular iff both nodes lie outside "
    "[-ell, ell]' -- an EXPLICIT exclusion statement per member (witness: node radius 1 "
    "at the E0 = -2 member). SCOPE: LE cells, quadratic class, BASE, all backgrounds",
)

r_tf, m00, m01, m10, m11 = symbols("r_tf m00 m01 m10 m11")
c00, c01, c10, c11 = symbols("c00 c01 c10 c11")
IDENT_KMOD0 = -2 * k10s * r_tf + m00 * c10 + m01 * c11 - m10 * c00 - m11 * c01
sol_m00 = sp.solve(sp.Eq(IDENT_KMOD0, 0), m00)
resub = simplify(IDENT_KMOD0.subs(m00, sol_m00[0]))
check(
    "TE4_kmod0_identity_fullcell",
    len(sol_m00) == 1 and resub == 0
    and IDENT_KMOD0.subs({r_tf: 0, m00: 0, m01: 0, m10: 0, m11: 0}) == 0,
    "KMOD0 stratum at FULL cell: the banked pointwise Noether identity -2 k10 r_tf + "
    "m00 c10 + m01 c11 - m10 c00 - m11 c01 = 0 is a single LINEAR relation on a general "
    "member's screen/mixing components -- solvable for m00 wherever c10 != 0 (codim-1 "
    "constraint on the screen-carrying sub-census; exact), and IDENTICALLY VACUOUS on "
    "the field-sector sub-census (r_tf = M = 0 -- the banked all-strata carrier class, "
    "which contains every member used in the mass legs above): the KMOD0 full-cell "
    "atlases of the field-sector census are the GENERIC ones restricted to k_mod = 0, "
    "uncut (banked, now cell-general on that sub-census); L23-orbit quotient carried "
    "(banked). SCOPE: KMOD0 stratum, all branches, jet <= 2, BASE",
)

check(
    "TE4_completion_typing_record",
    True,
    "[typing row -- filled vs typed split, L4 carried] J07 (chart-overlap twisted "
    "1-cocycle) + J11 (loop holonomy): NOT determined by the one-parameter solutions (no "
    "chart overlap in the registered presentation) -- stay TYPED, NEEDS-TRANSITION-DATA "
    "[F-S7 flag inherited]. J08/L4 (completion 𝔠): the solution components contain no "
    "frak_c (jet-alphabet census, banked fork-independence; recomputed on the G-class -- "
    "components frak_c-free), so completion enters ONLY through gate-6 periods/completion "
    "cycles: NEEDS-COMPLETION-DATA, the L4 fork carried BOTH ways, undecided (F-E5). J09: "
    "FILLED (node-locus row above). J10 (gauge): banked equivariance + the L23 quotient "
    "carried on KMOD0 (row above). Corners: TYPED-ONLY (codim-2, absent from the "
    "one-parameter presentation -- banked TC3). P3 wall blocks (BR-B varied fork): at "
    "N = 2 the varied-fork wall equations couple the momenta traces pi_a(+-ell) to the "
    "declared wall-density gradients, ONE relation per parity-surviving slot per wall "
    "(canon instance eps_phi = -1 kills the v_p slot; f/bh slots per SUPPLIED parity): "
    "each nonzero wall block cuts the 6-param family by at most 2 x (number of surviving "
    "slots) conditions -- the CUT COUNT is determined, the cut LOCUS needs the (free, "
    "unenumerated) wall-density data: typed OPEN, stamped (the Slice-2b P3 wall tile "
    "remains open at the data level, not the structure level)",
)

# ============================================================================
# TE5 -- the composite map (ledger deliverables)
# ============================================================================
print("\n--- TE5: composite map ledgers ---")

BRANCHES = [
    ("P1-4D", "aF=2lam", "anchored"),
    ("P1-triad", "aF=1+2lam", "anchored"),
    ("P2", "aF=0", "weightfree"),
    ("P3-bulkP2", "bulk aF=0 + wall blocks", "weightfree"),
    ("P3-bulkP1", "bulk aF=2lam + wall blocks", "anchored"),
]
STRATA = ["GENERIC", "KMOD0"]
CELLS = ["LOCALLY-EXACT", "NONVARIATIONAL"]

SCOPE_NOTE = (
    "# P4 Route A Slice 2b -- FULL-CELL ATLAS LEDGER (TE5 composite map). Contract: "
    "PREREGISTRATION.md (R1 labeled mass branches, R2 both bookkeeping branches; "
    "bootstrap-lens frame governs). SCOPE STAMP (F-E3, travels with every row): jet <= 2, "
    "registered stationary presentation, BASE arena (constant moduli; the POINTWISE "
    "column is Charles's R2 branch on that arena, labeled -- BR-M's field fork stays "
    "typed NOT-EXHAUSTED), enumerated pairing branches, READY bin only (RES-CNEQ0 "
    "CENSUS-REQUIRED; 4th-order EXTENSION-REQUIRED; carriers G09/F-D7 out; time-live "
    "out). FULL-CELL structure = the TE1 theorems (energy first integral + determinedness "
    "dichotomy, arbitrary member) + the exact closed-form atlas on the fiberwise-"
    "quadratic p-unmixed class + stated obstructions beyond it (honest boundary). Mass "
    "columns are LABELED BRANCHES -- M-GEN / M-WALL / M-DENS-coord / M-DENS-proper -- "
    "NO branch promoted (F-E1), none invented (F-E2); carrier closure rows rho+S=2rho4 / "
    "rho+p_par G09-gated OUT, kept separate. NO candidate crowned, NO elimination (F-D1/"
    "F-D2 never engaged), NO fork decided (F-E5). Outcome class OE1."
)
HDR = ("pairing_branch\tstratum\tG3_cell\tfull_cell_solution_structure\t"
       "generality_obstruction\tM_GEN\tM_WALL\tM_DENS_coord\tM_DENS_proper\t"
       "R2_INTEGRATED_survivors\tR2_POINTWISE_survivors\ttie_status\t"
       "TE4_wall_completion\tbackground_stamps")

LE_STRUCT_ANCH = (
    "TE1 theorems (arbitrary member): energy E = sum u' dS/du' - S exactly conserved; "
    "solved-form iff det Hess_{u'}(Ltil) != 0 (pairing-independent) with Picard 6-dim "
    "local data manifold per nondegenerate member; degenerate stratum populated (Ltil = "
    "p1^2/2 witness). EXACT closed-form atlas on the fiberwise-quadratic p-unmixed class "
    "(g_p, G_fh): e^{aF p0} = w = (aF^2 E0/(2 g_p))x^2 + w1 x + w0, (f',h') = "
    "G_fh^{-1}c/w, E0 = (g_p w1^2/aF^2 + c^T G_fh^{-1} c)/(2 w0); disc = -(aF^2/g_p) "
    "c^T G^{-1} c: DEFINITE sub-class => E0 >= 0, nodeless (banked A1 well/bump emergence "
    "= its g = I instance, definiteness-scoped); INDEFINITE sub-class => E0 < 0 noded "
    "members and E0 = 0 nonconstant members exist (witnesses)"
)
LE_STRUCT_FREE = (
    "TE1 theorems (arbitrary member) as in anchored cells; at aF = 0 the quadratic class "
    "degenerates to the affine atlas u = u(0) + u'(0)x (banked blindness transition, "
    "cell-general through the weight)"
)
NV_STRUCT = (
    "general member = arbitrary component tuple (source form): leading-symbol "
    "determinedness dichotomy (pairing-independent, banked T0) is the complete "
    "cell-general theorem; witnesses recomputed (W1 affine/determined; W2-fs quadratic-w; "
    "W3 degenerate); universality obstruction: no member-independent solution atlas"
)
OBS_LE = ("closed form NOT obtained for p-mixed quadratic members (weight anisotropy) or "
          "non-quadratic members (Liouville-class) -- TE1 theorems still cover them; "
          "stated obstruction, stamped")
OBS_NV = "member-by-member atlas only (universality obstruction, stamped)"

MGEN_LE = ("AVAILABLE (derived): M-GEN = 2 ell E for EVERY LE member (E the TE1 first "
           "integral); quadratic class: 2 ell E0; sign definiteness-scoped (E0 < 0 "
           "members on indefinite sub-class)")
MWALL_LE_ANCH = ("AVAILABLE (derived, TC3 by-parts): M-WALL = [pi_p] = 2 aF ell E0 = "
                 "aF * M-GEN on the quadratic class (p-slot = only nonvacuous slot, "
                 "derived there; p-slot labeled sub-choice beyond); NEGATIVE on definite "
                 "bump-side (aF < 0) members; trace functional under canon parity "
                 "(v_p slot parity-killed, stamped)")
MWALL_LE_FREE = ("AVAILABLE, IDENTICALLY ZERO on the affine atlas (pi_p = g_p p1 "
                 "constant): reads zero mass on every P2-side LE solution")
MDC_LE_ANCH = ("AVAILABLE (labeled sense): M-DENS-coord = E0 V; diverges from M-GEN by "
               "E0 (V - 2 ell) exactly (zero iff E0 = 0 or V = 2 ell); STRICTLY exceeds "
               "M-GEN on massive nonconstant integrated-tie survivors (Jensen, "
               "Category-A)")
MDC_LE_FREE = "AVAILABLE: at aF = 0, V = 2 ell and M-DENS-coord = 2 ell E0 = M-GEN (agree)"
MDP_LE = ("AVAILABLE (labeled sense, WR-L/proper lineage): M-DENS-proper == M-GEN "
          "IDENTICALLY (the calibration row)")
MGEN_NV_P1 = ("STILL-UNDETERMINED under M-GEN proper (Helmholtz defect obstructs a "
              "generator under the cell's own anchored pairing); DETERMINED under the "
              "labeled sub-branch M-GEN-eq (A2 even-handed extension, verifier-derived: "
              "the W1 tuple IS the weight-free aF = 0 generated tuple Euler(-Ltil0), "
              "banked identity; energy -Ltil0 conserved on the affine atlas): M = "
              "+-2 ell Ltil0, sign per tuple orientation (labeled); member stays NV "
              "under P1 (stamped) [DECISION-RELEVANT-R1]; W3: still-undetermined (no "
              "generated-tuple identity in banked structure)")
MGEN_NV_P2 = ("STILL-UNDETERMINED under M-GEN (pairing-generated); DETERMINED under the "
              "labeled sub-branch M-GEN-eq (tuple-autonomy first integral, banked "
              "provenance): M = 2 ell E0 on the quadratic-w atlas")
MWALL_NV = ("DETERMINED = 0 (zero DECLARED wall blocks -- trivial, an artifact of the "
            "declaration, stamped; nonzero-wall NV members typed OPEN)")
MDENS_NV = "STILL-UNDETERMINED (no derived density sense for a nonvariational member)"

R2I_ANCH_LE = ("QUADRATIC CLASS (A1 stamp): {E0 = 0} UNION {I_p = 0 massive locus, "
               "nonempty at every aF != 0 background (banked A2 + Category-A; in-package "
               "exact certificate ADOPTED_Ip_signchange_exact)}; BEYOND the quadratic "
               "class: row = a_F' int p0 W_F Ltil dx (nonconstant integrand -- no E0 "
               "factorization), survivors UNCHARACTERIZED (typed); omega rows: k10 = 0")
R2P_ANCH_LE = ("QUADRATIC CLASS (A1 stamp): {E0 = 0} ONLY (exact: pointwise row "
               "2 E0 p0(x) = 0 forces E0 = 0): constants on the definite sub-class; + "
               "nonconstant affine-w members on the indefinite sub-class; BEYOND the "
               "quadratic class: row = a_F' p0 W_F Ltil pointwise, survivors "
               "UNCHARACTERIZED (typed); omega rows: k10 = 0 (agree)")
R2_FREE_LE = ("lam-row identically absent (aF' = 0): both branches vacuous, AGREE; "
              "survivors = whole atlas, all backgrounds (degenerate, reported); omega "
              "rows: k10 = 0 both branches")
R2_NV = ("moduli slots zero (reps): both branches vacuous, AGREE; general NV nonzero "
         "moduli slots: pointwise included in integrated, strictness member-dependent "
         "(typed)")

TIE_ANCH = ("QUADRATIC CLASS (A1 stamp): INTEGRATED: tie = 2 E0 I_p = 0 present; zero "
            "locus mass-branch-ROBUST (every branch mass vanishes iff E0 = 0); "
            "nontrivial branch {I_p = 0, E0 != 0} massive under ALL four readings. "
            "POINTWISE: analog forces E0 = 0 -- massive branch ABSENT. BEYOND the "
            "quadratic class: integrated row = a_F' int p0 W_F Ltil dx (no E0 "
            "factorization), tie form and survivors UNCHARACTERIZED (typed). Bootstrap "
            "observation only (lens)")
TIE_FREE = "no tie either R2 branch (aF' = 0; banked P2 absence, now cell-general)"
TIE_NV = "no tie (zero moduli slots); W2-fs carries the quadratic-w atlas with NO lam-row"

TE4_LE = ("wall traces closed-form (w, w', atan f/h traces; canon-parity witness "
          "recomputed); J09 FILLED (node locus = real roots of w; definite class "
          "nodeless); J07/J11 NEEDS-TRANSITION-DATA; J08/L4 carried (components "
          "frak_c-free; periods NEED-COMPLETION-DATA); corners typed-only; P3 wall "
          "blocks: cut COUNT determined per parity-surviving slot, cut locus needs the "
          "free wall-density data (typed OPEN)")
TE4_NV = ("zero-declared walls: vacuous varied-fork wall eqs (banked); J09 per member; "
          "J07/J11/J08/corners as in LE cells; KMOD0 identity vacuous on field-sector "
          "census (cell-general)")

BG_ANCH = ("background (lam, c_E, ell, frak_c) free/explored; aF sign law A1 carried "
           "(well aF > 0 / bump aF < 0); blindness loci lam = 0 (P1-4D) / lam = -1/2 "
           "(P1-triad) => affine + tie absent; M-WALL/M-GEN agreement locus aF = 1 "
           "(lam = 1/2 / lam = 0)")
BG_FREE = "background free/explored; aF = 0 everywhere on the branch (weight-free)"

rows = []
for (br, brdef, kind) in BRANCHES:
    anchored = (kind == "anchored")
    for st in STRATA:
        for cell in CELLS:
            if cell == "LOCALLY-EXACT":
                struct = (LE_STRUCT_ANCH if anchored else LE_STRUCT_FREE)
                obs = OBS_LE
                mgen_c = MGEN_LE
                mwall_c = MWALL_LE_ANCH if anchored else MWALL_LE_FREE
                mdc = MDC_LE_ANCH if anchored else MDC_LE_FREE
                mdp = MDP_LE
                r2i = R2I_ANCH_LE if anchored else R2_FREE_LE
                r2p = R2P_ANCH_LE if anchored else R2_FREE_LE
                tie = TIE_ANCH if anchored else TIE_FREE
                te4 = TE4_LE
            else:
                struct = NV_STRUCT
                obs = OBS_NV
                mgen_c = MGEN_NV_P1 if anchored else MGEN_NV_P2
                mwall_c = MWALL_NV
                mdc = MDENS_NV
                mdp = MDENS_NV
                r2i = R2_NV
                r2p = R2_NV
                tie = TIE_NV
                te4 = TE4_NV
            if st == "KMOD0":
                struct = struct + " ; KMOD0: k_mod = 0 pin, identity vacuous on the field-sector census (cell-general), L23 quotient carried"
            rows.append("\t".join([
                br + " (" + brdef + ")", st, cell, struct, obs, mgen_c, mwall_c,
                mdc, mdp, r2i, r2p, tie, te4, BG_ANCH if anchored else BG_FREE,
            ]))

with open(os.path.join(HERE, "FULL_CELL_ATLAS_LEDGER.tsv"), "w") as fh:
    fh.write(SCOPE_NOTE + "\n" + HDR + "\n")
    for r in rows:
        fh.write(r + "\n")

DIV_NOTE = (
    "# P4 Route A Slice 2b -- DIVERGENCE MAPS (TE3; first-class deliverable per R2). "
    "Contract: PREREGISTRATION.md. Every row stamped (F-E3): cell class + pairing + "
    "mass-branch + bookkeeping-branch + stratum (GENERIC+KMOD0 unless noted) + "
    "background. Quadratic class = the fiberwise-quadratic p-unmixed LE class (exact "
    "closed forms); nothing resolved, nothing promoted (F-E1/F-E5); observation only."
)
DIV_HDR = "map\trow\tstatement\tstamps"
div_rows = [
    ("MASS-BRANCH", "calibration", "M-DENS-proper == M-GEN identically (= 2 ell E0)",
     "LE cells, all 5 pairings, quadratic class, both R2 branches, all backgrounds"),
    ("MASS-BRANCH", "wall-vs-gen", "M-WALL = aF * M-GEN exactly; difference 2 ell E0 (aF - 1); agreement iff E0 = 0 or aF = 1 (background locus: P1-4D lam = 1/2, P1-triad lam = 0); sign flip: M-WALL <= 0 <= M-GEN on definite bump-side (aF < 0) members",
     "LE cells, anchored pairings (P1-4D/P1-triad/P3-bulkP1), quadratic class, mass branches M-WALL vs M-GEN, all backgrounds"),
    ("MASS-BRANCH", "wall-P2-max", "M-WALL identically 0 on the affine atlas while M-GEN = 2 ell E0 free: maximal divergence",
     "LE cells, weight-free pairings (P2/P3-bulkP2), affine atlas, all backgrounds"),
    ("MASS-BRANCH", "coord-vs-gen", "M-DENS-coord - M-GEN = E0 (V - 2 ell) exactly; agreement iff E0 = 0 or V = 2 ell (solution locus; P2 side agrees identically); on massive nonconstant integrated-tie survivors (I_p = 0) V > 2 ell strictly (Jensen, Category-A): coord strictly exceeds M-GEN there",
     "LE cells, anchored pairings, quadratic class, mass branches M-DENS-coord vs M-GEN, all backgrounds"),
    ("MASS-BRANCH", "all-four", "simultaneous agreement of all four readings on {E0 = 0} UNION ({aF = 1} AND {V = 2 ell}): a nonzero-mass consensus point EXISTS (exact witness w = (3/2)x^2 + 1/2 at aF = 1, ell = 1: all four = 6) but lies OFF the integrated moduli-row survivor set (Jensen strict) and off the pointwise one -- OE3-flavored observation, no promotion",
     "LE cells, anchored pairings at aF = 1 background, quadratic class, all mass branches, both R2 branches (off-survivor, stamped), all backgrounds"),
    ("MASS-BRANCH", "NV-availability", "availability itself diverges: M-WALL determined (= 0, zero-declared walls) where M-GEN proper/M-DENS stay undetermined; BOTH NV witness classes determined under the labeled M-GEN-eq sub-branch -- W2-fs via its anchored aF = 2lam generator (= 2 ell E0), W1 via its weight-free aF = 0 generator (= +-2 ell Ltil0, orientation-sign labeled; A2 even-handed extension, verifier-derived) [DECISION-RELEVANT-R1: whether M-GEN-eq is admitted to the R1 menu, and its normalization convention, is Charles's call]; W3 undetermined (no generated-tuple identity)",
     "NV cells, all pairings, banked representatives, all backgrounds"),
    ("MASS-BRANCH", "sign-scope", "every branch's mass is proportional to E0 (or E0 V): sign structure is DEFINITENESS-scoped (E0 < 0 noded members exist on the indefinite sub-class, witness E0 = -2)",
     "LE cells, quadratic class, all mass branches, all backgrounds"),
    ("BOOKKEEPING", "P1-LE-strict", "STRICT: INTEGRATED survivors {E0 = 0} UNION {I_p = 0 massive, nonempty every aF != 0 background}; POINTWISE survivors {E0 = 0} only -- the fork decides whether ANY massive self-consistent member exists",
     "LE cells, anchored pairings, quadratic class, INTEGRATED vs POINTWISE, GENERIC+KMOD0, all backgrounds"),
    ("BOOKKEEPING", "pointwise-refined", "POINTWISE survivor set {E0 = 0} = constants on the definite sub-class (banked) but contains NONCONSTANT affine-w members on the indefinite sub-class (witness w = x + 2, E0 = 0)",
     "LE cells, anchored pairings, quadratic class, POINTWISE branch, all backgrounds"),
    ("BOOKKEEPING", "omega-agree", "omega k10-row: both branches force k10 = 0 -- exact agreement",
     "omega's banked LE cells, all pairings, both R2 branches, all backgrounds"),
    ("BOOKKEEPING", "P2-agree", "lam-row identically absent (aF' = 0): both branches vacuous, agree (degenerate; reported)",
     "LE cells, weight-free pairings + blindness loci, both R2 branches, all backgrounds"),
    ("BOOKKEEPING", "NV-agree", "banked NV representatives: zero moduli slots, both branches vacuous, agree; general NV: inclusion (pointwise in integrated) holds, strictness member-dependent (typed)",
     "NV cells, all pairings, both R2 branches, all backgrounds"),
    ("TIE-FATE", "integrated-robust", "tie 2 E0 I_p = 0 present; zero locus mass-branch-ROBUST (all four masses vanish iff E0 = 0); nontrivial branch {I_p = 0, E0 != 0} massive under ALL four readings: the bootstrap-shaped tie couples MASS to the background seat under every labeled definition",
     "LE cells, anchored pairings, quadratic class, INTEGRATED x each mass branch, all backgrounds; observation only (lens)"),
    ("TIE-FATE", "pointwise-absent", "the pointwise analog 2 E0 p0(x) = 0 forces E0 = 0: every pointwise survivor is massless under all four readings -- the tie's massive branch exists ONLY on the INTEGRATED side (the banked tie is INTEGRATED-branch, F-E4, now structural)",
     "LE cells, anchored pairings, quadratic class, POINTWISE x each mass branch, all backgrounds; observation only (lens)"),
    ("TIE-FATE", "P2-absent", "no tie and no analog on either branch (aF' = 0); the P1 tie degenerates to this at the blindness loci (lam = 0 / lam = -1/2) -- pairing-relativity of the tie is FULL-CELL general (arbitrary lam-independent member)",
     "LE cells, weight-free pairings + blindness loci, both R2 branches, all backgrounds"),
]
with open(os.path.join(HERE, "DIVERGENCE_MAPS.tsv"), "w") as fh:
    fh.write(DIV_NOTE + "\n" + DIV_HDR + "\n")
    for (m, r, s, st_) in div_rows:
        fh.write("\t".join([m, r, s, st_]) + "\n")

check(
    "TE5_ledgers_written",
    len(rows) == 20 and len(div_rows) == 15,
    "[recording row] FULL_CELL_ATLAS_LEDGER.tsv written: 20 READY composite cells x "
    "(full-cell structure, obstruction, four labeled mass columns, both R2 survivor "
    "columns, tie status, TE4 wall/completion, background stamps). DIVERGENCE_MAPS.tsv "
    "written: 15 rows across the three maps (MASS-BRANCH 7, BOOKKEEPING 5, TIE-FATE 3), "
    "each stamped. THE composite map deliverable (TE5)",
)

# ============================================================================
# TE6 -- the next surface (handle, not a launch)
# ============================================================================
print("\n--- TE6: next surface ---")

NEXT = """# P4 Route A Slice 2b -- NEXT SURFACE (TE6): a handle, NOT a launch

Date: 2026-07-29. Contract: `PREREGISTRATION.md`. Nothing here is launched, decided, or
recommended for adoption; the branch-collapse items are QUESTIONS for Charles on the
divergence evidence (F-E5 respected).

## The surface in five lines

1. **Branch-collapse questions now ripe for Charles (evidence in DIVERGENCE_MAPS.tsv):**
   (a) R2 fork -- INTEGRATED vs POINTWISE is now a MASS question: only the INTEGRATED
   reading admits massive self-consistent members on anchored P1-side LE cells (every
   pointwise survivor is massless under all four labeled readings); (b) R1 menu -- the
   exact laws M-DENS-proper == M-GEN, M-WALL = aF * M-GEN, M-DENS-coord - M-GEN =
   E0 (V - 2 ell) locate ALL the disagreement in two computable factors; the all-branch
   nonzero-mass consensus locus ({aF = 1} AND {V = 2 ell}) exists but lies off both
   R2 survivor sets; (c) [A2, DECISION-RELEVANT-R1] the M-GEN-eq sub-branch now covers
   BOTH NV witness classes even-handedly (W2-fs via its anchored aF = 2lam generator,
   = 2 ell E0; W1 via its weight-free aF = 0 generator, = +-2 ell Ltil0 with the
   orientation sign a labeled sub-choice): whether M-GEN-eq is admitted to the R1 menu
   at all -- and under what orientation/normalization convention -- is Charles's call.
   Both forks are Charles's calls, later.
2. **Still-queued tiles (out of this scope, unchanged):** restricted-EH G3 status under
   the enumerated pairings (Route C anchor banked); the RES-CNEQ0 resonance census
   (10 cells, deeper C != 0 stratification first); the 4th-order/jet-3/4 extension
   (wall grade 4; Bach-side anchor; the Slice-2 first-integral template does NOT
   transfer -- new derivation tile).
3. **Carrier-gated legs (G09):** the M-DENS carrier closure rows (rho+S=2rho4 vs
   rho+p_par, kept separate) become instantiable only with a POSIT-disciplined carrier;
   the vacuum atlases here are the reference backgrounds those sourced solves perturb.
4. **Open data-level structure:** P3 wall-density data (cut count determined, locus
   needs the free wall data); J07/J11 transition data; completion/period data (L4 both
   ways); nonzero-wall NV members' M-WALL; p-mixed quadratic + non-quadratic closed
   forms (obstructions stated -- any future closed form extends the atlas, the TE1
   theorems already cover the members).
5. **Time-live:** outside the registered stationary arena entirely; nothing here
   transfers without re-derivation (inherited stamp).
"""
with open(os.path.join(HERE, "NEXT_SURFACE.md"), "w") as fh:
    fh.write(NEXT)

check(
    "TE6_next_surface_written",
    os.path.exists(os.path.join(HERE, "NEXT_SURFACE.md")),
    "[recording row] NEXT_SURFACE.md written: branch-collapse questions for Charles "
    "(R1/R2 on the divergence evidence), queued tiles (restricted-EH G3, resonance "
    "census, 4th-order), carrier-gated legs (G09), data-level open structure, time-live. "
    "A handle, not a launch",
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
    "package": "udt_p4_routeA_slice2b_full_cell_2026-07-29",
    "contract": "PREREGISTRATION.md (frozen; R1 labeled mass branches; R2 both "
                "bookkeeping branches; bootstrap-lens frame binding)",
    "outcome_class": "OE1 (composite map populated across branches; no elimination; "
                     "convergence rows recorded as observations [M-DENS-proper == M-GEN "
                     "calibration; omega-row R2 agreement; the all-four nonzero-mass "
                     "consensus witness at aF = 1, V = 2 ell -- off both R2 survivor "
                     "sets] -- OE3-flavored rows inside an OE1 map, not promotions)",
    "scope_reductions": "NONE (full declared scope; TE4 delivered as "
                        "filled-where-determined + typed elsewhere per prereg TE4; "
                        "obstruction statements are TE1's honest-boundary clause, "
                        "not reductions)",
    "checks_total": len(CHECKS),
    "checks_substantive": n_sub,
    "checks_guards": n_grd,
    "checks_failed": n_fail,
    "amendments": {
        "verdict": "PASS-WITH-REQUIRED-AMENDMENTS (VERIFIER_REPORT.md); all four "
                   "amendments applied + the verifier's strengthenings adopted "
                   "(record: CORRECTION_LAYER.md)",
        "A1": "F-E3 FIFTH named-class catch: quadratic-class stamps installed "
              "in-column on the ledger R2_INTEGRATED_survivors / "
              "R2_POINTWISE_survivors / tie_status columns (anchored-LE rows), with "
              "the beyond-class row form and UNCHARACTERIZED typing",
        "A2": "M-GEN-eq extended EVEN-HANDEDLY to the W1 class via its weight-free "
              "aF = 0 generator (verifier derivation adopted as "
              "A2_W1_MGENeq_extension; M = +-2 ell Ltil0, orientation-sign labeled; "
              "member stays NV under P1) -- DECISION-RELEVANT-R1, flagged for Charles",
        "A3": "the dispatch's 'self-caught dropped term' claim (M-DENS-coord law) is "
              "WITHDRAWN: no package record exists; the shipped law is "
              "verifier-confirmed correct; logged as a dispatch-vs-record process "
              "defect in CORRECTION_LAYER.md (no script change)",
        "A4": "TE2_MWALL_P2_zero re-coded derivation-backed (affine atlas DERIVED "
              "from the aF = 0 Euler rows); TE3_tie_fate_map strengthened (mass-zero "
              "solves under declared assumptions + nonzero-factor row rewrites); dead "
              "masses_vanish removed; honest split restated",
        "adopted_strengthenings": "ADOPTED_atlas_exhaustive_energy_ODE (atlas "
                                  "EXHAUSTIVE on the class via the energy ODE); "
                                  "ADOPTED_Ip_signchange_exact (exact evalf-free "
                                  "sign-change certificate); "
                                  "ADOPTED_consensus_Ip_closed_form (I_p = -4 + log 4 "
                                  "+ 4 sqrt(3) pi/9 exactly, certified negative) -- "
                                  "verifier-credited",
    },
    "checks": CHECKS,
}
with open(os.path.join(HERE, "routeA_slice2b_results.json"), "w") as fh:
    json.dump(results, fh, indent=1, sort_keys=False)

sys.exit(0 if n_fail == 0 else 1)
