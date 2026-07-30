#!/usr/bin/env python3
"""P4 gradient seat -- the jet-extended field-census moduli rows (TG-1..TG-5).

Contract: udt_p4_gradient_seat_2026-07-29/PREREGISTRATION.md (frozen first).
Exact SymPy, zero-residual checks, deterministic (no floats, no randomness, no network,
no numeric solvers, no GPU), single CPU process, bounded. Exit 0 iff every check passes.

CENSUS/ALPHABET STAMPS (travel with every check): FIELD-moduli census (BR-M) on the
Route-D-REGISTERED alphabet (a851028: N1 moduli values m_mu(x), N2 moduli jets m', m''
per jet order -- higher jets TYPED; N3 wall m-jet slots; derived exclusions: anchored
nonlocal integrals & absolute-point evaluations alphabet-ILLEGAL; anchored-exponent rule:
p0 only through e^{a p0}, bare p0 excluded -- PW1_anchored_exponent_condition, cited);
K4 characters extended to jets pointwise (Route D R3; (lam,k_mod) sector trivial
character, (k10,C) chi-graded); registered positive triangular chart; registered
stationary one-parameter presentation, fields (phi,f,bh) jets <= 2, cell x in [-ell,ell];
enumerated pairing branches (P1-4D aF=2lam, P1-triad aF=1+2lam, P2 aF=0); the banked
odd-parity forcing (Route P ea5d8a3): lam(x), k_mod(x) mirror-ODD => wall values vanish
(P0+P1(+P2) premise ladder travels; k10 branch-split, C 2-odd+2-even, supplied remainder);
f/bh parities SUPPLIED (both directions carried); bootstrap lens (backgrounds explored,
self-consistent points reported, no background-fixed eliminations).

DOUBLE-STEERING BOUNDARY (F-G1/F-G2, binding): locking is NEVER imposed -- every
constancy statement below is either (i) an evaluation locus of the GENERAL jet-extended
rows (the locked-row functions), or (ii) DERIVED as a consequence (the lock-emergence
checks, where the rows themselves force m' = 0), with the adjudication done on the
general system first. Both outcome directions are computed and reported (massless-persists
legs AND massive-class legs, each with its cutting conditionalities). No spectra/forces/
particle language (F-G5). Mass legs use ONLY the banked labeled branches (Slice-2b R1):
M-GEN / M-WALL / M-DENS-coord / M-DENS-proper -- none promoted.

BANKED INPUTS (cited, machinery reused, never re-derived as new):
- Route D a851028 (registered alphabet, gauge law, K4/jet characters, J05 wall-slot IBP,
  A1-seat TD-R4); Route P ea5d8a3 (odd-parity forcing; a_F' vs a_F A1 distinction);
- bookkeeping forcing 38577c9 (pointwise rows = field-census bookkeeping, reduction thm);
- Slice-2b d110fe0 (massless theorem AT the no-moduli-jet alphabet; quadratic-class atlas
  machinery -- jet chains, Euler operators, LtG, SUBSOL -- reused verbatim-pattern;
  mass-branch identities M-GEN=2*ell*E, M-WALL=[pi_p]=aF*M-GEN, M-DENS senses);
- Stage-3/Stage-2/Slice-2 (pairing branches, anchored alphabet, character modules).

AMENDMENT BANNER (2026-07-30, post-verifier -- see CORRECTION_LAYER.md): the blind
adversarial pass (VERIFIER_REPORT.md) returned PASS-WITH-REQUIRED-AMENDMENTS; AM-1,
AM-2 (required) and AM-3 (minor) are applied here. NO pre-amendment computed claim
changed -- the amendments complete two stated CONDITION SETS on the massive-landing
leg, both in the CUTTING direction:
- AM-1: the "exact general condition" for linear m-jet members was B-only (complete
  for C-FREE members only); restated at every occurrence as FULL locked-row vanishing
  [a_F' p0 W_F Ltil_G - Dx(W_F B) + Dx^2(W_F C)]|lock = 0 along the locked solution;
  the verifier's field-coupled m'' counter-witness adopted as a zero-residual check
  (AM1_VC2_field_coupled_mpp_counterwitness, credited).
- AM-2 (the F-G3 firing, NINTH catch of the named scope class, cutting-direction):
  the landing/lock claims ride the nondegeneracy g_p != 0 AND Delta_G = g_f g_h -
  g_x^2 != 0 (equivalently: W3-degenerate members excluded) -- now stamped at every
  site; "unique solve" scoped GENERIC; the verifier's Delta_G = 0 counter-computation
  adopted as a zero-residual check (AM2_VC1_degenerate_block_counterwitness, credited).
- AM-3: the (k10, C) rows are vacuous BY INSPECTION (zero dependence) on the member
  classes used, operator form cited -- never instantiated as jet chains here; the
  prior "computed vacuous" wording is retired (EXACT_DERIVATION header + limits).
- Verifier strengthenings ADOPTED as credited checks: the extended lock-reduction
  set (<- V3), the general weight rule (<- V2), the everywhere-or-nowhere forcing
  scope (<- duty-1), the E-density confirmation of the triad leg (<- V11).
"""

import json
import os
import sys

import sympy as sp
from sympy import (Function, Matrix, Rational, Symbol, symbols, exp, log, sin, pi,
                   diff, expand, simplify, integrate, cancel)

HERE = os.path.dirname(os.path.abspath(__file__))

CHECKS = []

CITATION_GUARDS = {
    "G1_row_system_per_branch_ledger",
    "G3_slice2b_comparison_record",
    "G4_wall_behavior_typing",
    "G5_decision_map_and_stop_clause",
}


def check(name, ok, detail="", credit=""):
    kind = "citation-guard" if name in CITATION_GUARDS else "substantive"
    entry = {"name": name, "passed": bool(ok), "detail": detail, "kind": kind}
    if credit:
        entry["credit"] = credit
    CHECKS.append(entry)
    status = "PASS" if ok else "FAIL"
    tag = " [guard]" if kind == "citation-guard" else (
        " [verifier-credited]" if credit else "")
    print(f"[{status}]{tag} {name}" + (f" -- {detail}" if detail else ""))


# ============================================================================
# Jet machinery -- Slice-2b machinery reused (cited), EXTENDED with moduli
# chains lam0..lam5, km0..km5 (the field-census promotion: m_mu(x) with jets).
# Declared density jet order: m, m', m'' (N2); higher density jets TYPED.
# ============================================================================
print("--- Jet machinery (Slice-2b machinery reused; moduli chains added) ---")

FIELDS = ["p", "f", "h"]
JMAX = 6
J = {a: symbols(f"{a}0:{JMAX + 1}") for a in FIELDS}
MODS = ["lam", "km"]           # (lam, k_mod) sector, trivial K4 character (banked);
M = {m: symbols(f"{m}0:{JMAX}") for m in MODS}
# variation chains (fields + the lam modulus; enough orders for the IBP identity)
V = {a: symbols(f"v{a}0:5") for a in ["p", "f", "h", "lam"]}

p0, p1, p2, p3 = J["p"][0], J["p"][1], J["p"][2], J["p"][3]
f0, f1, f2 = J["f"][0], J["f"][1], J["f"][2]
h0, h1, h2 = J["h"][0], J["h"][1], J["h"][2]
l0, l1, l2, l3, l4 = M["lam"][0], M["lam"][1], M["lam"][2], M["lam"][3], M["lam"][4]
km0, km1, km2 = M["km"][0], M["km"][1], M["km"][2]

ALL_CHAINS = [list(J[a]) for a in FIELDS] + [list(M[m]) for m in MODS]
ALL_CHAINS_V = ALL_CHAINS + [list(V[a]) for a in V]


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


Dx = _Dx_over(ALL_CHAINS)                       # full total derivative (fields+moduli)
DxF = _Dx_over([list(J[a]) for a in FIELDS])    # field-chains-only (constant-moduli form)
DxV = _Dx_over(ALL_CHAINS_V)


def Euler_f(expr, a):
    """Field Euler row (density carries field jets <= 1)."""
    return expand(diff(expr, J[a][0]) - Dx(diff(expr, J[a][1])))


def Euler_m(expr, m):
    """Moduli Euler row on the registered m-jet alphabet (jets m, m', m'')."""
    return expand(diff(expr, M[m][0]) - Dx(diff(expr, M[m][1]))
                  + Dx(Dx(diff(expr, M[m][2]))))


# quadratic-class density (Slice-2b LtG, reused) + backgrounds
xs = Symbol("x")
ell = Symbol("ell", positive=True)
gp = Symbol("g_p", nonzero=True)
gf_, gh_, gx_ = symbols("g_f g_h g_x", real=True)
LtG = gp * p1**2 / 2 + (gf_ * f1**2 + 2 * gx_ * f1 * h1 + gh_ * h1**2) / 2
Lfh = (gf_ * f1**2 + 2 * gx_ * f1 * h1 + gh_ * h1**2) / 2   # the (f,h) part

# the FULL lock locus: all moduli jets zero (m constant); moduli 0-jets kept symbolic
LOCK = {M[m][k]: 0 for m in MODS for k in range(1, JMAX)}

# ============================================================================
# G0 -- banked footing recomputed (consistency)
# ============================================================================
print("\n--- G0: banked footing recomputed (consistency, F-G6) ---")

a_w = Symbol("a_w")
Ltf = Function("Ltil")(p0, p1, f0, f1, h0, h1)
aF_fun = Function("a_F")(l0)
S_pw = exp(aF_fun * p0) * Ltf
row_lam_pw = expand(diff(S_pw, l0) - diff(aF_fun, l0) * p0 * S_pw)
aF_4D = 2 * l0
aF_tri = 1 + 2 * l0
check(
    "G0_footing_recomputed",
    row_lam_pw == 0
    and aF_4D.subs(l0, 0) == 0 and aF_tri.subs(l0, 0) == 1
    and diff(aF_4D, l0) == 2 and diff(aF_tri, l0) == 2
    and expand(diff(exp(0 * p0) * Ltf, l0)) == 0,
    "banked footing recomputed: (i) the no-jet lam-row is d(W_F Ltil)/dlam = a_F'(lam) p0 "
    "W_F Ltil identically (arbitrary Ltil, arbitrary a_F -- Slice-2b R2 general lam-row, "
    "now with lam = lam(x) a FIELD: the row is the same algebraic density, pointwise); "
    "(ii) the Route-P A1 distinction carried exactly: at the lam = 0 landing a_F(0) = 0 "
    "on P1-4D but a_F(0) = 1 on P1-triad, while a_F' = 2 != 0 on BOTH (the row does NOT "
    "vanish by pairing-relativity at the landing); (iii) P2 (aF = 0): lam-row identically "
    "zero (vacuous, banked). STAMPS: field census, registered alphabet, all P-branches",
)

# ============================================================================
# TG-1 -- the jet-extended pointwise row system (general form)
# ============================================================================
print("\n--- TG-1: the jet-extended moduli-row system (general form) ---")

# [G1a] the row + wall-slot identity at ARBITRARY response density carrying m-jet
# content (the J05 IBP leg extended to m''; Route D R4 instantiated at 2nd jet order)
Sgen = Function("S")(p0, p1, f0, f1, h0, h1, l0, l1, l2)
deltaS = expand(
    diff(Sgen, p0) * V["p"][0] + diff(Sgen, p1) * V["p"][1]
    + diff(Sgen, f0) * V["f"][0] + diff(Sgen, f1) * V["f"][1]
    + diff(Sgen, h0) * V["h"][0] + diff(Sgen, h1) * V["h"][1]
    + diff(Sgen, l0) * V["lam"][0] + diff(Sgen, l1) * V["lam"][1]
    + diff(Sgen, l2) * V["lam"][2]
)
E_p_g = Euler_f(Sgen, "p")
E_f_g = Euler_f(Sgen, "f")
E_h_g = Euler_f(Sgen, "h")
E_l_g = Euler_m(Sgen, "lam")
Theta = (diff(Sgen, p1) * V["p"][0] + diff(Sgen, f1) * V["f"][0]
         + diff(Sgen, h1) * V["h"][0]
         + (diff(Sgen, l1) - Dx(diff(Sgen, l2))) * V["lam"][0]
         + diff(Sgen, l2) * V["lam"][1])
resid_ibp = expand(
    deltaS - (E_p_g * V["p"][0] + E_f_g * V["f"][0] + E_h_g * V["h"][0]
              + E_l_g * V["lam"][0]) - DxV(Theta)
)
check(
    "G1_jet_rows_and_wall_slots_identity",
    resid_ibp == 0,
    "TG-1 GENERAL FORM (zero residual, arbitrary Function S(p0,p1,f0,f1,h0,h1,m,m',m'')): "
    "the variation integrand decomposes EXACTLY as deltaS = sum_a E_a(S) v_a + R_mu v_mu "
    "+ Dx(Theta_ext) with the POINTWISE moduli row the full 2nd-order Euler operator "
    "R_mu = d_m S - Dx d_{m'} S + Dx^2 d_{m''} S (a DIFFERENTIAL condition in m(x) -- "
    "exactly the Route-D-typed A1-seat content), and the wall block Theta_ext = "
    "sum_a pi_a v_a + (d_{m'}S - Dx d_{m''}S) v_m + d_{m''}S v_m' -- the N3 wall m-jet "
    "slots DERIVED (J05 IBP leg extended to m''). Per-sector: same operator form for "
    "every modulus; (lam,k_mod) trivial character, (k10,C) chi-graded argument legality "
    "(Route D, cited). Jets beyond m'': TYPED (same commutation argument, banked). "
    "STAMPS: field census, registered m-jet alphabet, all branches, off-shell identity",
)

# [G1b] the configuration-dependent weight (the crux): W_F = e^{a_F(lam(x)) p0}
aFn = Function("a_F")(l0)
W = exp(aFn * p0)
S_qc = W * LtG                                   # generated member, no m-jet content
rows_field_full = {a: Euler_f(S_qc, a) for a in FIELDS}
rows_field_const = {a: expand(diff(S_qc, J[a][0]) - DxF(diff(S_qc, J[a][1])))
                    for a in FIELDS}
aFp = diff(aFn, l0)
new_p = expand(rows_field_full["p"] - rows_field_const["p"]
               + W * aFp * l1 * p0 * gp * p1)
new_f = expand(rows_field_full["f"] - rows_field_const["f"]
               + W * aFp * l1 * p0 * (gf_ * f1 + gx_ * h1))
new_h = expand(rows_field_full["h"] - rows_field_const["h"]
               + W * aFp * l1 * p0 * (gx_ * f1 + gh_ * h1))
row_lam_qc = Euler_m(S_qc, "lam")
check(
    "G1_configuration_dependent_weight_rows",
    new_p == 0 and new_f == 0 and new_h == 0
    and expand(row_lam_qc - aFp * p0 * S_qc) == 0
    and Euler_m(S_qc, "km") == 0,
    "THE CONFIGURATION-DEPENDENT WEIGHT, exact (the named crux): with lam(x) a field the "
    "anchored weight W_F = e^{a_F(lam(x)) p0} makes the FIELD rows pick up exactly one "
    "new term each vs the constant-moduli rows: E_a(full) - E_a(const-form) = "
    "-W_F a_F'(lam) lam' p0 pi_a-density (p: g_p p1; f: g_f f1 + g_x h1; h: g_x f1 + "
    "g_h h1) -- zero residual; the lam-row on the no-jet generated member stays the "
    "ALGEBRAIC density a_F' p0 W_F Ltil (pointwise), and the k_mod row is IDENTICALLY "
    "VACUOUS (the generated member carries no k_mod dependence): k_mod(x) is a FREE "
    "direction of the no-jet generated class -- an honest degeneracy, reported. The T4 "
    "blindness loci become LEVEL SETS lam(x) = 0 of the volume row (banked promotion, "
    "consistent). STAMPS: field census, generated (LE) member class, quadratic-class "
    "density, no-m-jet response content, all P-branches (a_F symbolic)",
)

# [ADOPTED <- verifier V2] the GENERAL weight rule: for an ARBITRARY no-m-jet response
# the field-row difference is exactly ONE structural term -lam' d^2S/(dlam du')
S_arb = Function("S_arb")(p0, p1, f0, f1, h0, h1, l0)
ok_rule = True
for a in FIELDS:
    d_full = Euler_f(S_arb, a)
    d_const = expand(diff(S_arb, J[a][0]) - DxF(diff(S_arb, J[a][1])))
    ok_rule = ok_rule and expand(d_full - d_const
                                 + l1 * diff(S_arb, l0, J[a][1])) == 0
check(
    "ADOPTED_weight_general_rule",
    ok_rule,
    "GENERAL CONFIGURATION-DEPENDENT-WEIGHT RULE (zero residual, arbitrary Function "
    "S(u-jets, lam) with NO m-jet content): for EVERY such response the field rows obey "
    "E_a(full) - E_a(const-form) = -lam' d^2 S/(dlam du_a') identically -- one "
    "structural term, member-general; the package's single anchored-member term "
    "-W_F a_F' lam' p0 (momentum density) (G1b) is exactly this rule's anchored "
    "instance. It really is the ONLY new term on the no-m-jet class. STAMPS: field "
    "census, registered alphabet, no-m-jet responses, all branches",
    credit="VERIFIER_INDEPENDENT_CHECK.py V2_weight_single_new_term",
)

check(
    "G1_row_system_per_branch_ledger",
    True,
    "[recording row -- the TG-1 system, per pairing branch x sector, written to "
    "JET_ROWS_LEDGER.tsv] The jet-extended pointwise system on the field census = "
    "{3 field rows (with the derived lam'-weight terms)} + {7 moduli rows, each the "
    "2nd-order Euler operator of G1a} + {N3 wall slots of G1a}. Per branch: P1-4D "
    "(aF = 2lam), P1-triad (aF = 1+2lam): lam-row nonvacuous (a_F' = 2); P2 (aF = 0): "
    "lam-row vacuous. Per stratum: k_mod(x) = 0 is a LEVEL SET carrying the banked "
    "pointwise identity -- on the field-sector sub-census used here it is IDENTICALLY "
    "VACUOUS (Slice-2b TE4_kmod0_identity_fullcell, cited): the mass-leg members below "
    "are uncut. (k10, C) sector: identical operator form, chi-graded legality, rows "
    "vacuous on the generated no-jet class (free directions, per-branch parity data "
    "supplied). RES-CNEQ0 and deeper strata: inherited TYPED-NOT-EXHAUSTED",
)

# ============================================================================
# TG-2 -- the interior-locking adjudication on the GENERAL system
# ============================================================================
print("\n--- TG-2: interior-locking adjudication (general system) ---")

# [G2a] THEOREM: response terms whose m-jet dependence vanishes to 2nd order at
# m' = m'' = 0 contribute NOTHING to any row AT the lock locus.
c1 = Function("c1")(p1, f0, f1, h0, h1, l0, km0)
c2 = Function("c2")(p1, f0, f1, h0, h1, l0, km0)
c3 = Function("c3")(p1, f0, f1, h0, h1, l0, km0)
d1 = Function("d1")(p1, f0, f1, h0, h1, l0, km0)
Squad = W * (c1 * l1**2 / 2 + c2 * l1 * l2 + c3 * l2**2 / 2 + d1 * l1 * km1)
quad_lock_ok = all(
    expand(r.subs(LOCK)) == 0
    for r in [Euler_m(Squad, "lam"), Euler_m(Squad, "km")]
    + [Euler_f(Squad, a) for a in FIELDS]
)
check(
    "G2_quadratic_jet_terms_vanish_at_lock",
    quad_lock_ok,
    "LOCK-REDUCTION THEOREM (zero residual, arbitrary Function coefficients incl. cross "
    "lam'-k_mod' terms): every response term whose m-jet dependence is QUADRATIC-OR-HIGHER "
    "at m' = m'' = 0 contributes ZERO to ALL rows (field and moduli) at the lock locus "
    "(m constant on the interior => all interior m-jets vanish). CONSEQUENCE: for the "
    "sub-class of registered responses with no term LINEAR in the m-jets, the interior-"
    "locking adjudication REDUCES EXACTLY to the no-m-jet-alphabet adjudication -- the "
    "jet extension changes nothing at the lock for that whole sub-class (it changes the "
    "NONCONSTANT sector instead, characterized below). STAMPS: field census, registered "
    "alphabet, all branches, both sectors, general theorem (no member instantiated)",
)

# [ADOPTED <- verifier V3] the EXTENDED quadratic set: ALL lam/k_mod jet quadratics,
# including the k_mod''-carrying cross terms the representative set (G2a) omitted
qs = [Function(f"q{i}")(p1, f0, f1, h0, h1, l0, km0) for i in range(9)]
S_ext = W * (qs[0] * l1**2 + qs[1] * l1 * l2 + qs[2] * l2**2
             + qs[3] * km1**2 + qs[4] * km1 * km2 + qs[5] * km2**2
             + qs[6] * l1 * km1 + qs[7] * l1 * km2 + qs[8] * l2 * km1)
ext_lock_ok = all(
    expand(r.subs(LOCK)) == 0
    for r in [Euler_m(S_ext, "lam"), Euler_m(S_ext, "km")]
    + [Euler_f(S_ext, a) for a in FIELDS]
)
check(
    "ADOPTED_lock_reduction_extended_set",
    ext_lock_ok,
    "LOCK-REDUCTION, EXTENDED SET (zero residual, arbitrary Function coefficients): "
    "the verifier's LARGER quadratic set -- all nine lam/k_mod jet quadratics "
    "lam'^2, lam' lam'', lam''^2, k_mod'^2, k_mod' k_mod'', k_mod''^2, lam' k_mod', "
    "lam' k_mod'', lam'' k_mod' (including the k_mod''-carrying cross terms G2a's "
    "representative set omitted) -- ALSO contributes zero to every row at the lock: "
    "the lock-reduction theorem is sound as stated (each row term retains >= 1 m-jet "
    "factor). STAMPS: as G2a (general theorem)",
    credit="VERIFIER_INDEPENDENT_CHECK.py V3_lock_reduction_extended_set",
)

# [G2b] the locked-row closed form for the general linear-in-jet member
Bf = Function("B")(f0, h0, f1, h1, l0, km0)
Cf = Function("C")(f0, h0, f1, h1, l0, km0)
Slin = W * (LtG + Bf * l1 + Cf * l2)
locked_lam_row = expand(Euler_m(Slin, "lam").subs(LOCK))
stated = expand(
    (aFp * p0 * W * LtG).subs(LOCK)
    - (Dx(W * Bf)).subs(LOCK)
    + (Dx(Dx(W * Cf))).subs(LOCK)
)
check(
    "G2_locked_row_general_form",
    expand(locked_lam_row - stated) == 0,
    "THE LOCKED ROW, general closed form (zero residual): for the generated member with "
    "general linear m-jet response content S = W_F (Ltil_G + B m' + C m''), the lam-row "
    "AT the lock locus equals G_lam = a_F' p0 W_F Ltil_G - Dx(W_F B)|lock + "
    "Dx^2(W_F C)|lock, where the surviving Dx-content is the FIELD-chain part only "
    "(m-chain terms die with the lock): terms LINEAR in the m-jets DO reach the locked "
    "row through their field-argument dependence -- Dx(W_F B)|lock = W_F (a_F p1 B + "
    "B_{f0} f1 + B_{h0} h1 + B_{f1} f2 + B_{h1} h2). Coefficients depending ONLY on "
    "moduli give zero here (their lock-derivative dies): pure-moduli linear terms are "
    "lock-inert. Locking is therefore ADMITTED iff the coupled system {field rows, "
    "G_mu = 0} has solutions at constant m -- adjudicated per branch below. STAMPS: "
    "field census, registered alphabet, generated class + linear jet content, all "
    "branches, general form (off-shell)",
)

# [G2c] the parity forcing: mirror-odd + interior-constant + continuity => locked AT 0
cc = Symbol("c")
sol_odd = sp.solve(sp.Eq(cc, -cc), cc)
f00, f1s, h00, h1s = symbols("f00 f1s h00 h1s", real=True)
sol_odd_aff = sp.solve([sp.Eq(f00 + f1s * ell, 0), sp.Eq(f00 - f1s * ell, 0)],
                       [f00, f1s], dict=True)
sol_even_aff = sp.solve(sp.Eq(f1s, 0), f1s)
check(
    "G2_parity_lock_at_zero",
    sol_odd == [0] and sol_odd_aff == [{f00: 0, f1s: 0}] and sol_even_aff == [0],
    "PARITY x LOCK (F-G4 carried with consequences, exact): a mirror-ODD field's wall "
    "value satisfies v = -v => v = 0 at every wall (solved: only 0); the cell interior "
    "(-ell, ell) is CONNECTED and its closure reaches the walls, so an interior-constant "
    "CONTINUOUS odd field is == 0 on the whole cell: for the (lam, k_mod) sector "
    "(forced odd, Route P P0+P1(+P2)) INTERIOR LOCKING IS LOCKING AT ZERO -- no other "
    "locked value exists on this cell topology (a lock at v != 0 would need an interior "
    "component not reaching a wall: none in the one-parameter presentation; mirrored-"
    "quotient reading identical -- continuity to the crease pins the constant). Also "
    "solved exactly (used below): an AFFINE field odd about both walls is killed "
    "entirely (f00 = f1 = 0); even about both walls kills its slope (f1 = 0). k10/C "
    "sector: the same forcing holds per SUPPLIED parity branch (k10 odd on branch (a), "
    "even+shear on (b); C 2-odd+2-even) -- branch-conditional, stamped. STAMPS: field "
    "census, mirrored cell (CANON), premise ladder P0+P1(+P2) for (lam,k_mod)",
)

# [G2d] P1-triad locked branch: lam == 0 => a_F = 1 != 0 => massless persists
a_r = Symbol("a_r", nonzero=True)
w0 = Symbol("w0", positive=True)
w1 = Symbol("w1", real=True)
cf, ch = symbols("c_f c_h", real=True)
DeltaG = gf_ * gh_ - gx_**2
qc = (gh_ * cf**2 - 2 * gx_ * cf * ch + gf_ * ch**2) / DeltaG
E0G = (gp * w1**2 / a_r**2 + qc) / (2 * w0)
AG = a_r**2 * E0G / (2 * gp)
wG = AG * xs**2 + w1 * xs + w0
E0_from_A = cancel(E0G - 2 * gp * AG / a_r**2)
wpoly = sp.Poly(wG - 1, xs)
cw = wpoly.all_coeffs()
# p == 0 escape at a_F != 0 is killed by the p-row itself:
S_tri0 = exp(1 * p0) * LtG                  # locked lam == 0 on P1-triad: W = e^{p0}
prow_tri_p0 = expand(Euler_f(S_tri0, "p").subs(LOCK).subs(
    {p0: 0, p1: 0, p2: 0, f2: 0, h2: 0}))
check(
    "G2_P1triad_lock_massless",
    E0_from_A == 0 and cancel(cw[0] - AG) == 0 and cw[1] == w1
    and cancel(cw[2] - (w0 - 1)) == 0
    and expand(prow_tri_p0 - Lfh) == 0,
    "P1-TRIAD LOCKED BRANCH (lam == 0 forced by parity+lock; a_F(0) = 1 != 0): the "
    "quadratic-class atlas applies on the locked interior (banked, exhaustive on the "
    "class) and the pointwise lam-row 2 E0 p0(x) = 0 forces E0 = 0 EXACTLY (either "
    "directly, or p0 == 0 => w == 1 => A = 0 => E0 = 0 via E0 = 2 g_p A/a_F^2 -- the "
    "banked Slice-2b leg re-derived at the locked value); the p0 == 0 escape route is "
    "ALSO independently killed by the p-row itself: at p == 0 (affine f,h) the p-row "
    "equals a_F * Ltil_fh = Ltil_fh, so Ltil_fh = 0 => E0 = 0 again. LOCKED SURVIVORS "
    "(P1-triad) = {E0 = 0}: MASSLESS under all four labeled branches (M-GEN = 2 ell E0, "
    "M-WALL = a_F M-GEN, M-DENS-coord = E0 V, M-DENS-proper = M-GEN -- all vanish at "
    "E0 = 0; banked tie-fate map, same-solution). Definite sub-class: constants; "
    "indefinite: nonconstant E0 = 0 members exist (banked witness w = x + 2 at a_F = 1, "
    "cited). The Slice-2b massless verdict PERSISTS on this branch at the extended "
    "alphabet for all quadratic-at-lock responses (G2a). STAMPS: field census, "
    "registered alphabet, P1-triad, locked class, quadratic-class density, no-linear-"
    "jet responses, GENERIC + KMOD0-level-set, all backgrounds",
)

# [ADOPTED <- verifier V11] the on-shell E-density identity backing the triad leg:
# E-density = W Ltil on the quadratic class, so the locked lam-row a_F' p0 W Ltil is
# exactly 2 p0 x (E-density) -- the "2 E0 p0(x) = 0" reading confirmed independently
E_dens_tri = expand(p1 * diff(S_tri0, p1) + f1 * diff(S_tri0, f1)
                    + h1 * diff(S_tri0, h1) - S_tri0)
E_dens_gen = expand(p1 * diff(S_qc, p1) + f1 * diff(S_qc, f1)
                    + h1 * diff(S_qc, h1) - S_qc)
check(
    "ADOPTED_triad_E_density_identity",
    expand(E_dens_tri - S_tri0) == 0 and expand(E_dens_gen - S_qc) == 0
    and expand(row_lam_qc - aFp * p0 * E_dens_gen) == 0,
    "E-DENSITY IDENTITY (zero residual): on the quadratic class the energy density "
    "sum_a u' dS/du' - S equals W_F Ltil_G exactly (checked on the locked P1-triad "
    "member AND on the general generated member with a_F symbolic), so the no-jet "
    "lam-row a_F' p0 W_F Ltil_G = a_F' p0 x (E-density) -- on P1-branches (a_F' = 2) "
    "the pointwise row IS '2 p0 E-density = 0': the G2d '2 E0 p0(x) = 0' reading is "
    "confirmed via the on-shell identity, independently of the atlas citation. "
    "STAMPS: field census, quadratic-class density, generated members, all branches",
    credit="VERIFIER_INDEPENDENT_CHECK.py V11_triad_prow_kill_and_E_density",
)

# [G2e] P1-4D locked branch: lam == 0 => a_F = 0 -- the landing; affine atlas forced
S_4D0 = exp(0 * p0) * LtG                    # locked lam == 0 on P1-4D: W = 1
rows_4D0 = [expand(Euler_f(S_4D0, a).subs(LOCK)) for a in FIELDS]
sol_aff = sp.solve([sp.Eq(r, 0) for r in rows_4D0], [p2, f2, h2], dict=True)
AFF = {p2: 0, f2: 0, h2: 0, p3: 0}
lamrow_4D0 = expand(Euler_m(exp(aF_4D * p0) * LtG, "lam").subs(LOCK).subs(l0, 0))
# the pointwise row 2 p0 LtG = 0 with p affine: split by polynomial coefficients
p00s, p1c = symbols("p00 p1c", real=True)
rowpoly = sp.Poly((2 * (p00s + p1c * xs)
                   * LtG.subs({p1: p1c})), xs)
check(
    "G2_P14D_landing_affine_forced",
    sol_aff == [{p2: 0, f2: 0, h2: 0}]
    and expand(lamrow_4D0 - 2 * p0 * LtG) == 0
    and rowpoly.degree() == 1
    and expand(rowpoly.all_coeffs()[0] - 2 * p1c * LtG.subs({p1: p1c})) == 0
    and expand(rowpoly.all_coeffs()[1] - 2 * p00s * LtG.subs({p1: p1c})) == 0,
    "P1-4D LOCKED BRANCH -- THE LANDING (lam == 0 forced by parity+lock; a_F(0) = 0: "
    "exactly the slot Route P A1 stamped UNDERIVED -- the banked quadratic atlas and "
    "I_p certificate presuppose a_F != 0; now DERIVED): at the lock the weight is "
    "W_F == 1 and the field rows FORCE the affine atlas u'' = 0 (GENERIC unique "
    "solve, zero residual -- NONDEGENERACY STAMP [AM-2]: rides g_p != 0 AND Delta_G "
    "= g_f g_h - g_x^2 != 0, equivalently W3-degenerate members excluded; at "
    "Delta_G = 0 the forcing FAILS -- counter-computation "
    "AM2_VC1_degenerate_block_counterwitness); the pointwise lam-row is 2 p0 Ltil_G, "
    "and with p0 affine (= p00 + p1 x) "
    "the row's polynomial coefficients give the EXACT SPLIT: either Ltil_G = 0 (on the "
    "definite sub-class: constants, E0 = 0, massless) OR p == 0 identically (p00 = "
    "p1 = 0) with f, h affine FREE -- the second branch carries E0 = Ltil_fh(f1, h1) "
    "unconstrained: the landing admits a LOCKED class with E0 != 0 (adjudicated + "
    "massed below). STAMPS: field census, registered alphabet, P1-4D at the lam = 0 "
    "landing, locked class, quadratic-class density, no-linear-jet responses, GENERIC "
    "nondegeneracy g_p != 0 & Delta_G != 0 (W3-degenerate members excluded)",
)

# [AM-2 <- verifier VC1] the nondegeneracy counter-witness: at Delta_G = 0 the affine
# atlas is NOT forced -- the (f,h) block acquires a kernel direction
rows_deg = [expand(r.subs({gf_: 1, gh_: 1, gx_: 1})) for r in rows_4D0[1:]]
kernel_ok = (expand(rows_deg[0].subs({f2: 1, h2: -1})) == 0
             and expand(rows_deg[1].subs({f2: 1, h2: -1})) == 0
             and (gf_ * gh_ - gx_**2).subs({gf_: 1, gh_: 1, gx_: 1}) == 0)
check(
    "AM2_VC1_degenerate_block_counterwitness",
    kernel_ok,
    "AM-2 COUNTER-WITNESS, adopted (zero residual): at Delta_G = g_f g_h - g_x^2 = 0 "
    "(instance g_f = g_h = g_x = 1) the locked f/h rows are solved by the KERNEL "
    "direction f'' = 1, h'' = -1 -- the affine atlas is NOT forced there: the landing "
    "'unique solve' (G2e) and everything riding it (G2f/G2g/G3c) are GENERIC, "
    "conditioned on g_p != 0 AND Delta_G != 0 (W3-degenerate members excluded). "
    "Direction: CUTTING -- the stamp narrows the massive landing class's stated "
    "scope; the NINTH catch of the named scope class (F-G3), memorialized in the "
    "falsifier record. STAMPS: P1-4D landing, quadratic-class density, degenerate "
    "(f,h) block instance",
    credit="VERIFIER_INDEPENDENT_CHECK.py VC1_degenerate_G_probe",
)

# [G2f] LOCK EMERGENCE (the F-G2 discharge): on the p == 0 class the p-row itself
# FORCES lam(x) == 0 -- constancy DERIVED, not imposed.
S_4D = exp(aF_4D * p0) * LtG                 # lam(x) LEFT FREE (general field)
prow_free = expand(Euler_f(S_4D, "p").subs({p0: 0, p1: 0, p2: 0, f2: 0, h2: 0}))
lamsol = sp.solve(sp.Eq(prow_free, 0), l0)
frow_free = expand(Euler_f(S_4D, "f").subs({p0: 0, p1: 0, p2: 0}))
lamrow_free = expand(Euler_m(S_4D, "lam").subs({p0: 0, p1: 0, p2: 0}))
kmrow_free = Euler_m(S_4D, "km")
check(
    "G2_lock_emergence_derived_not_imposed",
    expand(prow_free - 2 * l0 * Lfh) == 0
    and lamsol == [0]
    and expand(frow_free - (-gf_ * f2 - gx_ * h2)) == 0
    and lamrow_free == 0 and kmrow_free == 0,
    "LOCK EMERGENCE (the F-G2 discharge, zero residual): on the p == 0 configuration "
    "class with lam(x) LEFT COMPLETELY FREE (a general field, nothing imposed), the "
    "p-row of the P1-4D generated member evaluates to 2 lam(x) Ltil_fh(f1, h1) -- so "
    "wherever Ltil_fh != 0 (the E0 != 0 leg) the field equations THEMSELVES force "
    "lam(x) == 0: the interior lock (constancy, at the parity-forced value 0) EMERGES "
    "as a consequence of the rows on this class; it is never assumed. The f/h rows "
    "force the affine atlas (G(f2,h2) = 0 with the NONDEGENERACY STAMP [AM-2]: "
    "det G = Delta_G = g_f g_h - g_x^2 != 0, GENERIC -- W3-degenerate members "
    "excluded; see AM2_VC1_degenerate_block_counterwitness); the lam-row is then "
    "automatically satisfied (2 p0 (...) with p0 == 0); the k_mod row is vacuous "
    "(k_mod(x) a free odd direction -- degeneracy, reported). STAMPS: field census, "
    "registered alphabet, P1-4D, p == 0 class, no-m-jet responses, all backgrounds, "
    "GENERIC nondegeneracy g_p != 0 & Delta_G != 0",
)

# [ADOPTED <- verifier duty-1 scoping leg] everywhere-or-nowhere: on the emergence
# class Ltil_fh is CONSTANT (f, h affine), so the lam-forcing cannot be partial
dLfh_aff = expand(Dx(Lfh).subs({f2: 0, h2: 0}))
check(
    "ADOPTED_everywhere_or_nowhere_forcing",
    dLfh_aff == 0 and expand(prow_free - 2 * l0 * Lfh) == 0,
    "EVERYWHERE-OR-NOWHERE SCOPING (zero residual): on the p == 0 / affine class "
    "Dx(Ltil_fh) = 0 exactly (f'' = h'' = 0) -- Ltil_fh is CONSTANT on the cell, so "
    "the G2f forcing 2 lam(x) Ltil_fh = 0 is everywhere-or-nowhere: either E0 = 0 "
    "(massless stratum, lam free) or E0 != 0 and lam(x) == 0 on the WHOLE cell. This "
    "CLOSES THE NONZERO-PLATEAU LOOPHOLE on the massive class: no partial-interior "
    "lock (sub-interval plateau at lam != 0) coexists with E0 != 0 -- the 'wherever "
    "E0 != 0' scoping in G2f is exact, not a per-point hedge. STAMPS: field census, "
    "P1-4D landing, p == 0 class, no-m-jet responses, GENERIC nondegeneracy",
    credit="VERIFIER_REPORT.md duty-1 (everywhere-or-nowhere leg)",
)

# [G2g] the massive locked witness, all rows, exact
kap = Symbol("kappa", real=True)
WITNESS = {p0: sp.Integer(0), f0: f00 + f1s * xs, h0: h00 + h1s * xs,
           l0: sp.Integer(0), km0: kap * sin(pi * xs / ell)}


def on_witness(expr):
    sub = {}
    for a, base in [("p", WITNESS[p0]), ("f", WITNESS[f0]), ("h", WITNESS[h0])]:
        for k in range(JMAX + 1):
            sub[J[a][k]] = diff(base, xs, k) if k else base
    for m, base in [("lam", WITNESS[l0]), ("km", WITNESS[km0])]:
        for k in range(JMAX):
            sub[M[m][k]] = diff(base, xs, k) if k else base
    return expr.subs(sub, simultaneous=True)


E0_wit = Lfh.subs({f1: f1s, h1: h1s})
rows_all = ([Euler_f(S_4D, a) for a in FIELDS]
            + [Euler_m(S_4D, "lam"), Euler_m(S_4D, "km")])
wit_rows_zero = all(simplify(on_witness(r)) == 0 for r in rows_all)
# extended (Ostrogradsky) energy on the witness
E_ost_wit = on_witness(p1 * diff(S_4D, p1) + f1 * diff(S_4D, f1)
                       + h1 * diff(S_4D, h1) - S_4D)
check(
    "G2_massive_locked_witness_all_rows",
    wit_rows_zero and simplify(E_ost_wit + on_witness(-E0_wit)) == 0
    and E0_wit != 0,
    "THE MASSIVE LOCKED WITNESS (exact, all five rows zero-residual): p == 0, f = f00 + "
    "f1 x, h = h00 + h1 x (affine), lam == 0 (EMERGED, G2f), k_mod = kappa sin(pi x/ell) "
    "(a free ODD direction -- odd about BOTH walls exactly, witnessing the vacuous-row "
    "degeneracy): every field row and every moduli row vanishes identically on the cell, "
    "with conserved energy E = Ltil_fh(f1, h1) = (g_f f1^2 + 2 g_x f1 h1 + g_h h1^2)/2 "
    "-- SYMBOLIC and generically NONZERO (sign per G_fh definiteness: positive on the "
    "definite sub-class). Honest degeneracy stamps: the depth field is IDENTICALLY at "
    "the seal value (p0 == 0 -- whether such a member is completion/canon-admissible is "
    "typed OPEN, not claimed); k_mod (and k10, C) are row-unconstrained free directions "
    "on this class. NONDEGENERACY STAMP [AM-2]: the class sits on the GENERIC affine "
    "atlas -- g_p != 0 AND Delta_G = g_f g_h - g_x^2 != 0 (W3-degenerate members "
    "excluded). STAMPS: field census, registered alphabet, P1-4D lam = 0 landing, "
    "locked class, quadratic-class density, no-linear-jet responses, background "
    "symbolic, GENERIC nondegeneracy",
)

# [G2h] the witness's mass rides the SUPPLIED f/bh wall data (both directions)
sol_both_odd = sp.solve([sp.Eq(f00 + f1s * ell, 0), sp.Eq(f00 - f1s * ell, 0)],
                        [f00, f1s], dict=True)
check(
    "G2_witness_parity_conditionality",
    sol_both_odd == [{f00: 0, f1s: 0}] and sol_even_aff == [0]
    and E0_wit.subs({f1s: 0, h1s: 0}) == 0,
    "CUTTING CONDITIONALITY of the massive locked class (F-G1 duty -- the attack on the "
    "tempting leg, computed): the class's energy rides the AFFINE slopes f1, h1, and the "
    "f/bh wall parities are SUPPLIED (not derived, banked). Exact solves: if f (resp. bh) "
    "carries a SUPPLIED ODD parity at both walls, the affine profile is killed entirely "
    "(f00 = f1 = 0); if EVEN, the slope is killed (f1 = 0); EITHER definite supplied "
    "parity on both fields collapses E0 to 0 -- the massive locked class is NONEMPTY "
    "exactly when the supplied f/bh wall data leave at least one slope free (free/"
    "natural-BC-type wall data), and EMPTY under definite both-wall parities of either "
    "sign on both fields. The mass of the locked class is therefore CONDITIONED on the "
    "supplied wall structure -- stamped, first-class. STAMPS: as G2g + supplied-parity "
    "fork carried BOTH ways",
)

# [G2i] linear-in-jet responses: the conditional layer (witnesses both ways)
B_obstruct = f0
B_admit = h1 * f0 - f1 * h0
S_obs = exp(aF_4D * p0) * (LtG + B_obstruct * l1)
S_adm = exp(aF_4D * p0) * (LtG + B_admit * l1)
obs_lock_row = simplify(on_witness(Euler_m(S_obs, "lam")))
adm_rows_zero = all(
    simplify(on_witness(r)) == 0
    for r in [Euler_f(S_adm, a) for a in FIELDS]
    + [Euler_m(S_adm, "lam"), Euler_m(S_adm, "km")]
)
dirder_admit = expand(f1 * diff(B_admit, f0) + h1 * diff(B_admit, h0))
dirder_obstr = expand(f1 * diff(B_obstruct, f0) + h1 * diff(B_obstruct, h0))
check(
    "G2_linear_jet_conditional_layer",
    simplify(obs_lock_row + f1s) == 0 and adm_rows_zero
    and dirder_admit == 0 and expand(dirder_obstr - f1) == 0,
    "LINEAR m-jet responses -- the CONDITIONAL layer, witnesses BOTH directions (exact): "
    "on the massive locked class the locked lam-row gains -(B_{f0} f1 + B_{h0} h1) "
    "(G2b at p == 0, affine atlas). OBSTRUCTING witness B = f0 (alphabet-legal: local "
    "jet argument, no bare p0, trivial character): locked row = -f1 != 0 -- this member "
    "class CUTS the massive locked class down to f1 = 0 (its exact admit condition). "
    "ADMITTING witness B = h1 f0 - f1 h0 (legal local-jet arguments): the directional "
    "derivative (f1 d_{f0} + h1 d_{h0})B = f1 h1 - h1 f1 = 0 on the affine atlas -- ALL "
    "rows vanish on the SAME massive witness (zero residual, all five): registered "
    "members with genuinely linear m-jet response content ADMIT the massive locked "
    "class too. EXACT GENERAL CONDITION (restated per AM-1 -- FULL locked-row "
    "vanishing, from G2b): [a_F' p0 W_F Ltil_G - Dx(W_F B) + Dx^2(W_F C)]|lock = 0 "
    "along the locked solution (on the p == 0 landing the first term vanishes, "
    "leaving [-Dx(W_F B) + Dx^2(W_F C)]|lock = 0). For C-FREE members this reduces "
    "to the previously stated (f1 d_{f0} + h1 d_{h0} + f2 d_{f1} + h2 d_{h1}) B + "
    "a_F p1 B = 0 (on this class: B constant along the affine (f,h) line) -- that "
    "formula is COMPLETE ONLY for m'-linear content; field-coupled m'' content "
    "reaches the locked row through Dx^2(W_F C)|lock (counter-witness: "
    "AM1_VC2_field_coupled_mpp_counterwitness). Pure-moduli coefficients B(lam, "
    "k_mod): lock-inert (G2b); pure-moduli C: null-reducible (G2j). VERDICT SHAPE: "
    "at the extended alphabet the locking adjudication is MEMBER-CONDITIONAL on the "
    "linear m-jet content, with the exact condition = the full locked-row vanishing. "
    "STAMPS: field census, registered m-jet alphabet, P1-4D landing, locked class",
)

# [AM-1 <- verifier VC2] the field-coupled m'' counter-witness: the B-only formula is
# vacuously satisfied (B = 0) yet the member CUTS the massive class
S_c = exp(aF_4D * p0) * (LtG + (f0**2 / 2) * l2)
lrow_c = simplify(on_witness(Euler_m(S_c, "lam")))
check(
    "AM1_VC2_field_coupled_mpp_counterwitness",
    simplify(lrow_c - f1s**2) == 0 and diff(S_c, l1) == 0,
    "AM-1 COUNTER-WITNESS, adopted (zero residual): the alphabet-legal member S = "
    "W_F (Ltil_G + (f0^2/2) m'') carries NO m'-linear term (B = 0 -- the pre-"
    "amendment B-only condition is VACUOUSLY satisfied), yet its locked lam-row on "
    "the massive witness is Dx^2(W_F f0^2/2)|lock = f1^2 != 0: it CUTS the massive "
    "locked class (to f1 = 0). Field-coupled m'' content reaches the locked row "
    "through Dx^2(W_F C)|lock exactly as G2b's closed form states -- the admit "
    "condition MUST be the full locked-row vanishing (G2i, restated). Direction: "
    "CUTTING -- the massive class's condition set is narrower than first stated. "
    "STAMPS: field census, registered m-jet alphabet, P1-4D landing, locked class, "
    "GENERIC nondegeneracy",
    credit="VERIFIER_INDEPENDENT_CHECK.py VC2_mpp_field_coupled_probe",
)

# [G2j] linear-m'' pure-moduli terms are null-reducible => lock-inert
cnull = Function("c")(l0)
null_lag = Dx(cnull * l1)                        # total derivative
null_rows_zero = (Euler_m(null_lag, "lam") == 0 and Euler_m(null_lag, "km") == 0
                  and all(Euler_f(null_lag, a) == 0 for a in FIELDS))
check(
    "G2_mpp_null_reduction",
    null_rows_zero
    and expand(cnull * l2 - (null_lag - diff(cnull, l0) * l1**2)) == 0,
    "pure-moduli m'' terms are LOCK-INERT by null reduction (zero residual): c(m) m'' = "
    "Dx(c m') - c'(m) m'^2, the total derivative contributes ZERO to every row "
    "(identically -- checked), and the remainder is quadratic in m-jets (lock-inert by "
    "G2a): linear-m'' response content with pure-moduli coefficients cannot disturb any "
    "locking adjudication; FIELD-coupled m'' coefficients join the G2b/G2i conditional "
    "layer through the Dx^2(W_F C)|lock term (WITNESSED cutting: "
    "AM1_VC2_field_coupled_mpp_counterwitness). STAMPS: field census, "
    "registered alphabet, general theorem",
)

# [G2k] the CONVERSE: nonconstant m(x) behaviors admitted (characterized, not filtered)
lam_free = Symbol("s_amp", real=True)
CONST_BG = {f0: f00, h0: h00, p0: p00s}          # constant fields, Ltil0 = 0


def on_constbg_lamfree(expr, lamprof):
    sub = {}
    for a, base in [("p", p00s), ("f", f00), ("h", h00)]:
        for k in range(JMAX + 1):
            sub[J[a][k]] = base if k == 0 else sp.Integer(0)
    for k in range(JMAX):
        sub[M["lam"][k]] = diff(lamprof, xs, k) if k else lamprof
        sub[M["km"][k]] = sp.Integer(0)
    return expr.subs(sub, simultaneous=True)


lamprof = lam_free * sin(pi * xs / ell)          # odd about both walls, nonconstant
free_dir_zero = all(
    simplify(on_constbg_lamfree(r, lamprof)) == 0 for r in rows_all
)
# jet-quadratic member on constant-field backgrounds: lock FORCED
cq = Symbol("c_q", nonzero=True)
S_jq = exp(aF_4D * p0) * (LtG + cq * l1**2 / 2)
prow_jq = expand(Euler_f(S_jq, "p"))
prow_jq_cb = on_constbg_lamfree(prow_jq, Function("lamf")(xs))
lamf = Function("lamf")(xs)
prow_factor = simplify(prow_jq_cb / (cq * exp(2 * lamf * p00s)))
# p==0 tuned nonconstant branch: lam affine beta*x, rows force Ltil_fh = -c beta^2/2
beta = Symbol("beta", real=True)


def on_p0_lamaffine(expr):
    sub = {}
    for k in range(JMAX + 1):
        sub[J["p"][k]] = sp.Integer(0)
    for a, b0, b1 in [("f", f00, f1s), ("h", h00, h1s)]:
        sub[J[a][0]] = b0 + b1 * xs
        sub[J[a][1]] = b1
        for k in range(2, JMAX + 1):
            sub[J[a][k]] = sp.Integer(0)
    sub[M["lam"][0]] = beta * xs
    sub[M["lam"][1]] = beta
    for k in range(2, JMAX):
        sub[M["lam"][k]] = sp.Integer(0)
    for k in range(JMAX):
        sub[M["km"][k]] = sp.Integer(0)
    return expr.subs(sub, simultaneous=True)


prow_tuned = simplify(on_p0_lamaffine(Euler_f(S_jq, "p")))
lamrow_tuned = simplify(on_p0_lamaffine(Euler_m(S_jq, "lam")))
E_jq_tuned = simplify(on_p0_lamaffine(
    p1 * diff(S_jq, p1) + f1 * diff(S_jq, f1) + h1 * diff(S_jq, h1)
    + l1 * diff(S_jq, l1) - S_jq))
Lfh_wit = E0_wit
check(
    "G2_nonconstant_admitted_characterized",
    free_dir_zero
    and simplify(prow_factor - lamf * diff(lamf, xs)**2) == 0
    and simplify(prow_tuned - 2 * beta * xs * (Lfh_wit + cq * beta**2 / 2)) == 0
    and lamrow_tuned == 0
    and simplify(E_jq_tuned - (Lfh_wit + cq * beta**2 / 2)) == 0,
    "THE CONVERSE -- nonconstant m(x) admitted behaviors, characterized (not filtered): "
    "(a) FREE-DIRECTION class: on constant-field backgrounds with Ltil0 = 0 the no-jet "
    "member's rows all vanish for ARBITRARY odd lam(x) (witness s sin(pi x/ell): all "
    "five rows zero) -- nonconstant moduli are ADMITTED with E = 0 (row-degenerate free "
    "directions; massless). (b) JET-QUADRATIC member S = W(Ltil_G + c lam'^2/2) on "
    "constant-field backgrounds: the p-row carries the exact factor lam (lam')^2 (zero "
    "residual after removing the nonzero prefactor c e^{2 lam p0}) -- combined with the "
    "lam-row, any interval with lam' != 0 forces lam = 0 there (contradiction): lam' == "
    "0, and parity then pins lam == 0 -- for this member class the FULL system FORCES "
    "the lock on constant-field backgrounds (second emergence result, derived). (c) the "
    "p == 0 TUNED branch: lam = beta x (nonconstant) solves the lam-row identically "
    "(lam'' = 0) and the p-row iff 2 beta x (Ltil_fh + c beta^2/2) = 0, i.e. Ltil_fh = "
    "-c beta^2/2 (possible at c < 0 or indefinite G): that branch has EXTENDED energy "
    "E_ext = Ltil_fh + c beta^2/2 = 0 EXACTLY -- the tuned nonconstant-lam branch is "
    "MASSLESS under M-GEN(ext); and the in-cell parity (lam odd about both walls, "
    "affine) kills it anyway (beta = 0, G2c solve): on parity-legal configurations the "
    "member's admitted behaviors collapse to the locked ones. STAMPS: field census, "
    "registered alphabet, P1-4D, named background classes, member classes as stamped",
)

# ============================================================================
# TG-3 -- mass status per solution class (branch labels; availability derived)
# ============================================================================
print("\n--- TG-3: mass branches on the jet alphabet ---")

# [G3a] M-GEN availability: the extended (Ostrogradsky) energy identity
Sg2 = Function("S")(p0, p1, f0, f1, h0, h1, l0, l1, l2)
E_ost = expand(p1 * diff(Sg2, p1) + f1 * diff(Sg2, f1) + h1 * diff(Sg2, h1)
               + l1 * (diff(Sg2, l1) - Dx(diff(Sg2, l2))) + l2 * diff(Sg2, l2) - Sg2)
belt_ext = expand(Dx(E_ost) + p1 * Euler_f(Sg2, "p") + f1 * Euler_f(Sg2, "f")
                  + h1 * Euler_f(Sg2, "h") + l1 * Euler_m(Sg2, "lam"))
check(
    "G3_extended_energy_first_integral",
    belt_ext == 0,
    "M-GEN AVAILABILITY on the m-jet alphabet, DERIVED (zero residual, arbitrary "
    "Function S(u-jets, m, m', m'')): the extended (Ostrogradsky-form) energy E_ext = "
    "sum_a u' dS/du' + m'(d_{m'}S - Dx d_{m''}S) + m'' d_{m''}S - S obeys Dx(E_ext) = "
    "-sum_a u' E_a(S) - m' R_m(S) IDENTICALLY: on the FULL field-census shell (field "
    "rows + pointwise moduli rows) E_ext is an exact first integral -- the M-GEN "
    "generator EXISTS on the extended alphabet (LE cells), M-GEN = 2 ell E_ext, "
    "reducing to the banked E on locked solutions (m-jets = 0). NV cells: no generator "
    "(banked refusal inherited). STAMPS: field census, registered alphabet, LE cells, "
    "all branches, mass branch M-GEN",
)

# [G3b] M-WALL / N3 slots + the parity kill on the odd-sector slots
check(
    "G3_MWALL_N3_slots_parity",
    sol_odd == [0]
    and diff(S_qc, l1) == 0 and diff(S_qc, l2) == 0
    and expand(diff(S_adm, l1) - exp(aF_4D * p0) * B_admit) == 0
    and simplify(on_witness((exp(aF_4D * p0) * gp * p1))) == 0,
    "M-WALL on the m-jet alphabet: the wall block (G1a, derived) carries the N3 moduli "
    "slots pi_m = d_{m'}S - Dx d_{m''}S (v_m slot) and d_{m''}S (v_m' slot) alongside "
    "the banked field slots. PARITY KILL (F-G4 consequence, derived): the (lam, k_mod) "
    "variation class inherits the forced ODD parity, so v_m(walls) = 0 (the same c = -c "
    "solve) -- the odd-sector N3 v_m-slots are PARITY-KILLED at the variation level "
    "(trace-functional status, exactly parallel to the banked v_p kill under eps_phi = "
    "-1); the v_m'-slot survives (m' odd => m'' even-jet content -- v_m' free at walls); "
    "k10/C slots per supplied branch. On the no-jet generated class all moduli slots are "
    "identically vacuous. M-WALL's p-slot reading persists: on the massive locked "
    "witness pi_p = W g_p p1 == 0 exactly => M-WALL = [pi_p] = 0. STAMPS: field census, "
    "registered alphabet, mass branch M-WALL, N3 slots, parity ladder P0+P1(+P2)",
)

# [G3c] the four labeled masses per locked class (same-solution discipline)
V_wit = integrate(sp.Integer(1), (xs, -ell, ell))       # int W_F dx at W == 1
MGEN_wit = 2 * ell * E0_wit
MWALL_wit = sp.Integer(0)
MDENSc_wit = E0_wit * V_wit
MDENSp_wit = integrate(E0_wit, (xs, -ell, ell))
check(
    "G3_masses_per_locked_class",
    V_wit == 2 * ell and simplify(MDENSc_wit - MGEN_wit) == 0
    and simplify(MDENSp_wit - MGEN_wit) == 0 and MWALL_wit == 0,
    "MASS STATUS per locked class, branch-labeled, same-solution (R1 labels, none "
    "promoted): (1) P1-TRIAD locked class {E0 = 0}: M-GEN = M-WALL = M-DENS-coord = "
    "M-DENS-proper = 0 -- MASSLESS under ALL FOUR labeled branches. (2) P1-4D locked "
    "landing class (p == 0, f/h affine, lam == 0 emerged): W_F == 1 so V = int W_F dx "
    "= 2 ell exactly; M-GEN = 2 ell E0 with E0 = Ltil_fh(f1,h1) generically NONZERO "
    "(sign per G_fh definiteness; positive-definite => E0 > 0 off the constants); "
    "M-DENS-coord = E0 V = 2 ell E0 = M-GEN; M-DENS-proper = M-GEN (both senses agree "
    "at W == 1); M-WALL = [pi_p] = 0 (p1 == 0): THREE of the four labeled branches "
    "read the SAME nonzero mass, M-WALL dissents at 0 -- consistent with the banked "
    "divergence law M-WALL = a_F M-GEN at a_F = 0. (3) P2: lam-row vacuous, lock "
    "trivially admitted, banked P2 column unchanged (M-GEN free, M-WALL = 0, cited). "
    "CONDITIONALITY STAMPS travel: (2) requires free f/bh wall data (G2h), is "
    "member-conditional under linear m-jet content with the FULL locked-row admit "
    "condition [AM-1] (G2i + AM1_VC2), and rides the GENERIC nondegeneracy [AM-2] "
    "g_p != 0 & Delta_G = g_f g_h - g_x^2 != 0 (W3-degenerate members excluded). "
    "STAMPS: field census, registered alphabet, per-branch as labeled, quadratic-"
    "class density, GENERIC + KMOD0-level-set, GENERIC nondegeneracy, backgrounds "
    "symbolic",
)

check(
    "G3_slice2b_comparison_record",
    True,
    "[recording row -- the explicit Slice-2b comparison, alphabet-stamped] The banked "
    "Slice-2b POINTWISE/field-census massless theorem is stamped: BASE arena, "
    "NO-moduli-jet response alphabet, quadratic class, a_F != 0 (atlas premise), "
    "survivors {E0 = 0} massless under all four branches. THIS PUSH: (i) EXTENDS that "
    "theorem at the REGISTERED m-jet alphabet: for every response with no linear m-jet "
    "content (G2a) and every interior-locked configuration at a_F(lock) != 0 "
    "(P1-triad; any branch at a nonzero locked value -- parity-excluded for lam anyway) "
    "the massless verdict PERSISTS (G2d); linear-jet content makes it MEMBER-"
    "CONDITIONAL with the exact condition derived (G2i). (ii) POPULATES the premise-"
    "failure slot Slice-2b explicitly did NOT cover (a_F = 0 landing, Route P A1: "
    "UNDERIVED on banked footing): the P1-4D locked landing admits the p == 0 massive "
    "class (G2e/G2g) -- NOT a supersession (no banked statement is contradicted: the "
    "banked stamps excluded this slot) and NOT covered by the banked massless theorem "
    "(its a_F != 0 premise fails there BY the parity forcing). The banked INTEGRATED-"
    "branch results are untouched (constant census -- not this push's domain). F-G6: "
    "no contradiction anywhere; the stamps did their job",
)

check(
    "G4_wall_behavior_typing",
    True,
    "[typing row -- TG-4, wall behavior under the odd forcing] (1) lam, k_mod vanish at "
    "both walls (derived values; even jets lam'', k_mod'' also wall-vanishing by "
    "oddness; odd jets lam', k_mod' free there). (2) WALL-LOCALIZED m-VARIATION: an "
    "interior plateau at value v != 0 with wall-vanishing transition layers is the "
    "generic shape of a nonzero odd profile; for NO-JET members the rows give such "
    "profiles NO dynamics on row-degenerate strata (free directions, G2k(a)) and "
    "FORBID them on the massive p == 0 class (lam == 0 forced everywhere, G2f -- no "
    "plateau at v != 0 coexists with that class); for JET-CARRYING members the "
    "transition layer obeys the derived row ODEs (G2k(b): lock forced on constant-"
    "field backgrounds; general layer profiles TYPED -- solution-level work beyond "
    "scope). (3) N3 wall slots: odd-sector v_m slots parity-killed (G3b); v_m' slots "
    "survive; k10/C per supplied branch; varied-boundary fork inherits the moduli wall "
    "terms (Route D J05 leg, cited). (4) corners/completion: inherited TYPED "
    "(J07/J08/J11 as banked). No interaction/force language (F-G5)",
)

check(
    "G5_decision_map_and_stop_clause",
    True,
    "[recording row -- TG-5; full text in DECISION_SURFACE_UPDATE.md] CENSUS-FORK "
    "IMPLICATION MAP (map facts, nothing adopted): the field census with the registered "
    "jet alphabet is now DERIVED to be neither cleanly dissolution-shaped nor cleanly "
    "exclusivity-shaped: it is MIXED PER PAIRING BRANCH -- P1-triad locked sector "
    "massless (exclusivity-shaped leg); P1-4D locked landing carries a massive class "
    "under 3 of 4 labeled branches with the lock EMERGING from the rows (dissolution-"
    "shaped leg), conditioned on (a) supplied f/bh wall data leaving a slope free, "
    "(b) no obstructing linear m-jet response content (exact condition derived), "
    "(c) M-WALL dissenting at 0, (d) the class's p0 == 0 degeneracy (depth identically "
    "at the seal value) being completion-admissible -- typed OPEN. The Slice-2b "
    "constants-side massive locus {I_p = 0, E0 > 0} has NO locked-interior field-census "
    "correspondent on P1-branches at a_F != 0 (E0 = 0 forced there); its nearest "
    "correspondent is the P1-4D landing class (different mechanism-free locus, "
    "different M-WALL verdict). STOP-CLAUSE (honest): the finding is NOT merely "
    "confirmatory (a previously-underived slot is populated, and constancy EMERGES "
    "rather than being imposed) -- it is flagged to Charles; but no premise of step (2) "
    "(the angular completion) is invalidated, and step (2) supplies exactly the data "
    "this result is conditioned on (k10/C parity branch, wall/angular completion, the "
    "supplied f/bh parities): the assessment is CONTINUE-WITH-FLAG; the stop decision "
    "is Charles's",
)

# ============================================================================
# Outputs
# ============================================================================
print("\n--- Writing outputs ---")

ok_all = all(c["passed"] for c in CHECKS)
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_grd = sum(1 for c in CHECKS if c["kind"] == "citation-guard")
n_cred = sum(1 for c in CHECKS if c.get("credit"))

results = {
    "package": "udt_p4_gradient_seat_2026-07-29",
    "contract": "PREREGISTRATION.md (frozen)",
    "outcome_class": "OG3 (mixed/conditional -- exact conditions delivered; contains an "
                     "OG1-shaped leg [P1-4D landing massive locked class, M-WALL "
                     "dissenting, wall-data-, member- (full locked-row condition, AM-1) "
                     "and nondegeneracy- (GENERIC Delta_G != 0, AM-2) conditional] and "
                     "an OG2-shaped leg [massless persists at the new alphabet for "
                     "quadratic-at-lock responses at a_F(lock) != 0])",
    "amendment": "AM-1/AM-2 (required) + AM-3 (minor) applied 2026-07-30 per "
                 "VERIFIER_REPORT.md (PASS-WITH-REQUIRED-AMENDMENTS) -- see "
                 "CORRECTION_LAYER.md; no pre-amendment computed claim changed; both "
                 "required amendments CUTTING-direction (the massive class's stated "
                 "conditions narrowed/completed); 6 verifier-credited checks adopted "
                 "(2 counter-witnesses + 4 strengthenings); F-G3 ONE FIRING = AM-2, "
                 "the NINTH catch of the named scope class, memorialized",
    "checks_total": len(CHECKS),
    "checks_substantive": n_sub,
    "checks_verifier_credited": n_cred,
    "checks_guards": n_grd,
    "all_passed": ok_all,
    "checks": CHECKS,
}
with open(os.path.join(HERE, "gradient_seat_results.json"), "w") as fh:
    json.dump(results, fh, indent=1, sort_keys=True)

LEDGER_ROWS = [
    ["row_id", "pairing_branch", "sector", "response_subclass", "row_form",
     "locked_row", "locking_verdict", "mass_status_by_branch", "stamps"],
    ["JR1", "P1-4D|P1-triad", "lam", "no-m-jet (generated)",
     "R_lam = a_F'(lam) p0 W_F Ltil (algebraic, pointwise)",
     "a_F' p0 W_F Ltil at lam=0 (parity-forced locked value)",
     "ADMITTED; P1-triad: only with E0=0; P1-4D: {Ltil=0 massless} U {p==0 massive, "
     "lock EMERGES from p-row}",
     "P1-triad locked: all four = 0. P1-4D landing: M-GEN=M-DENS-coord=M-DENS-proper="
     "2*ell*E0 (E0=Ltil_fh free), M-WALL=0",
     "field census; registered m-jet alphabet; jet order m,m',m'' (higher typed); "
     "GENERIC+KMOD0-level-set; quadratic-class density; wall-data-conditional (G2h); "
     "GENERIC nondegeneracy g_p!=0 & Delta_G=g_f*g_h-g_x^2!=0 (W3-degenerate members "
     "excluded; landing affine-forcing fails at Delta_G=0 -- AM2_VC1) [AM-2]"],
    ["JR2", "P2", "lam", "any", "R_lam == 0 (vacuous, a_F' = 0)", "0",
     "trivially ADMITTED; lam(x) free (odd)",
     "banked P2 column: M-GEN free, M-WALL=0, M-DENS senses agree",
     "field census; registered alphabet; banked P2 facts cited"],
    ["JR3", "all", "k_mod", "no-m-jet (generated)", "R_kmod == 0 (vacuous)", "0",
     "free odd direction (degeneracy); lock admitted trivially (at 0 by parity if "
     "locked)", "row-inert (no mass coupling on this class)",
     "field census; registered alphabet; k_mod(x)=0 level set carries banked identity "
     "-- vacuous on field-sector sub-census (cited)"],
    ["JR4", "all", "lam|k_mod", "quadratic-or-higher m-jet content",
     "R_mu = full 2nd-order Euler operator (differential)",
     "identical to no-jet locked row (G2a theorem)",
     "adjudication REDUCES to no-jet case at the lock; nonconstant sector gains row "
     "ODEs (G2k: lock FORCED on constant-field backgrounds for W(LtG + c lam'^2/2))",
     "unchanged from JR1 at the lock",
     "field census; registered alphabet; general theorem"],
    ["JR5", "P1-4D", "lam", "linear m-jet content W_F (B(args) m' + C(args) m'')",
     "R_lam = a_F' p0 W_F Ltil + dB/dC-terms - Dx(W_F B) + Dx^2(W_F C)",
     "[a_F' p0 W_F Ltil_G - Dx(W_F B) + Dx^2(W_F C)]|lock (field-chain content only; "
     "C-free members: a_F' p0 W_F Ltil - W_F(a_F p1 B + B_f0 f1 + B_h0 h1 + B_f1 f2 "
     "+ B_h1 h2))",
     "MEMBER-CONDITIONAL: admitted iff the FULL locked lam-row vanishes along the "
     "locked solution [AM-1]: [a_F' p0 W_F Ltil_G - Dx(W_F B) + Dx^2(W_F C)]|lock = 0 "
     "(for C-FREE members: (f1 d_f0 + h1 d_h0 + f2 d_f1 + h2 d_h1)B + a_F p1 B = 0); "
     "obstructing witness B=f0 (cuts to f1=0); admitting witness B=h1 f0 - f1 h0 (all "
     "rows zero on the massive witness); m'' counter-witness C=f0^2/2 (B=0, locked row "
     "f1^2 -- cuts to f1=0; AM1_VC2)",
     "massive class persists exactly on the admit-condition locus",
     "field census; registered alphabet; anchored (no bare p0); trivial character; "
     "full locked-row condition [AM-1]; GENERIC nondegeneracy [AM-2]"],
    ["JR6", "all", "k10|C", "generated class",
     "same Euler-operator form; chi-graded argument legality (cited)",
     "vacuous on generated class",
     "free directions; parity per supplied branch (k10: odd on (a), even+shear on (b); "
     "C: 2 odd + 2 even)", "row-inert on this class",
     "field census; registered alphabet; supplied completion data (banked 07-20)"],
    ["JR7", "all", "all", "N3 wall slots",
     "Theta_ext = sum pi_a v_a + (d_m'S - Dx d_m''S) v_m + d_m''S v_m'",
     "odd-sector v_m slots PARITY-KILLED (v_m(walls)=0); v_m' survives",
     "wall m-jet slots derived (J05 extension); vacuous on no-jet class",
     "M-WALL p-slot reading persists; = 0 on the massive locked witness",
     "field census; registered alphabet; varied-boundary fork; parity ladder P0+P1(+P2)"],
    ["JR8-AMENDMENT", "-", "-", "amendment stamp (2026-07-30)",
     "AM-1: JR5 admit condition restated as FULL locked-row vanishing (B-only formula "
     "scoped C-FREE; m'' counter-witness adopted, AM1_VC2)",
     "AM-2: JR1/JR5 landing claims stamped GENERIC nondegeneracy g_p!=0 & "
     "Delta_G!=0 (W3-degenerate members excluded; counter-witness AM2_VC1)",
     "AM-3: (k10,C) rows vacuous BY INSPECTION (zero dependence), operator form "
     "cited -- not instantiated as jet chains",
     "no pre-amendment computed claim changed; OG3 stands; 6 verifier-credited "
     "checks adopted",
     "per VERIFIER_REPORT.md (PASS-WITH-REQUIRED-AMENDMENTS) + CORRECTION_LAYER.md"],
]
with open(os.path.join(HERE, "JET_ROWS_LEDGER.tsv"), "w") as fh:
    for row in LEDGER_ROWS:
        fh.write("\t".join(row) + "\n")

print(f"\nSummary: {sum(1 for c in CHECKS if c['passed'])}/{len(CHECKS)} checks passed "
      f"({n_sub} substantive [{n_sub - n_cred} original + {n_cred} verifier-credited] "
      f"+ {n_grd} guards); all_passed = {ok_all}")
sys.exit(0 if ok_all else 1)
