#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P4 Route P — the seal-parity derivation (TP1-TP4 computational legs).

Contract: udt_p4_routeP_seal_parity_2026-07-29/PREREGISTRATION.md (frozen first).
Question: does the banked seal/mirror structure DERIVE the mirror parity eps_m of the
moduli (lambda, k_mod, k10, C) — or is eps_m supplied data?

Method: the Route-B K4-exhaustiveness METHOD (probe members -> necessary conditions ->
enumeration), applied to the DRESSING J: the complete set of linear frame dressings J
under which the depth mirror phi -> -phi is represented ON the registered class as
X |-> -J X J^{-1}.  The V5 swap candidate is adjudicated INSIDE this classification
(F-P2: nothing adopted).  Both census branches carried (F-P4: no census adoption).

Machinery lineage (REUSED, not re-derived):
  - class blocks / eta / H conventions: udt_p4_routeB_extension_selection_2026-07-28/
    derive_routeB_stage1.py (banked 07-25 registration; 07-27 eta & swap F).
  - jet-kill lever statement + -X obstruction + V5 candidate facts:
    udt_p4_bookkeeping_forcing_2026-07-29/derive_bookkeeping_forcing.py
    (TF2_parity_jet_kill_and_constant_lever, ADOPTED_swap_dressing_parity_candidate).
  - E04 closed-form exponential: Route B T2 (banked exact form).

Exact SymPy only: no floats, no numeric solvers, no randomness, no network, no GPU.
Deterministic; exit nonzero on any failed check.  Category-A named steps: Picard
uniqueness for the linear matrix ODE (banked Slice-2 lane); real-square positivity.

AMENDMENT PASS (2026-07-29, post-verifier; VERIFIER_REPORT.md verdict
PASS-WITH-REQUIRED-AMENDMENTS; see CORRECTION_LAYER.md):
  A1 (required, load-bearing textual) — the TP4_aF_anchor_landing detail and the
     results-JSON aF_landing entry mis-cited the banked no-lambda-row criterion
     (a_F' = 0: the P2 pairing's identically-zero anchor weight DERIVATIVE) as the
     weight VALUE a_F = 0.  Corrected here; the a_F'-vs-a_F distinction is now a
     zero-residual check (A1_aFprime_vs_aF_distinction).  Drift direction:
     CUTTING-side inflation (anti-massive) — memorialized in the falsifier record.
  A2 — dropped prime restored in the EXACT_DERIVATION TP4 quote (a_F' = 0).
  A3 — the blind verifier's mutation catch-proofs ADOPTED as in-package checks
     (credited: VERIFIER_INDEPENDENT_CHECK.py V3_catch_* / V2f_attack_*), plus the
     verifier's compensation-loophole-closing H-block lemma (V2b).
  A4 — check-22 prose sign slip fixed and hardened to an exact equality (-k10);
     family parameter count stated per-branch (3 in branch (a), 4 in branch (b));
     eta-readout stamp added to the ledger's Lorentz row (banked 07-20
     null-coordinate O(1,1) caveat); the verifier's completed K4-honesty leg
     (R13 o J non-involutive) adopted (credited).
No pre-amendment computed claim changed; outcome class OP3 stands.
"""

import json
import sys

import sympy as sp

# ----------------------------------------------------------------------------
# Conventions (copied from the banked Route-B script; THEORY: 07-25 registration)
# ----------------------------------------------------------------------------
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
H2 = sp.diag(-1, 1)                      # base block: slots (0=clock, 1=ruler)
eta2 = sp.diag(-1, 1)
eta4 = sp.diag(-1, 1, 1, 1)


def bm(A, B, C, D):
    return sp.Matrix(sp.BlockMatrix([[A, B], [C, D]]))


k00, k11, k10 = sp.symbols("k00 k11 k10")
c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
Kg = sp.Matrix([[k00, 0], [k10, k11]])   # K lower-triangular on slots (2,3)=screen
Cg = sp.Matrix([[c00, c01], [c10, c11]])
Xg = bm(H2, Z2, Cg, Kg)                  # generic registered-class member
X0 = bm(H2, Z2, Z2, Z2)                  # fixed part
LAM = (k00 + k11) / 2                    # Route B T4 adapted coordinates
KMOD = (k11 - k00) / 2
phi = sp.symbols("phi")

MODULI = [k00, k11, k10, c00, c01, c10, c11]

# 7-dim linear part V of the class (basis)
V_BASIS = []
for (i, j) in [(2, 2), (3, 2), (3, 3)]:          # K slots
    E = sp.zeros(4, 4); E[i, j] = 1; V_BASIS.append(E)
for (i, j) in [(2, 0), (2, 1), (3, 0), (3, 1)]:  # C slots
    E = sp.zeros(4, 4); E[i, j] = 1; V_BASIS.append(E)

CHECKS = []


def check(name, kind, ok, detail):
    CHECKS.append({"name": name, "kind": kind, "pass": bool(ok), "detail": detail})
    print(("PASS" if ok else "FAIL") + f" [{kind}] {name}")
    print("      " + detail)


def is_zero(M):
    return sp.simplify(sp.expand(M)) == sp.zeros(*M.shape) if hasattr(M, "shape") \
        else sp.simplify(sp.expand(M)) == 0


# ============================================================================
# S0 — banked-input consistency recomputations (never re-derived, recomputed)
# ============================================================================
print("=" * 78)
print("S0 — banked-input recomputations")
print("=" * 78)

# [1] the -X obstruction (banked, forcing package S3): naive generator negation
# leaves the class (H block -H != H).
mXg = -Xg
ok = (mXg[0:2, 0:2] == -H2) and (sp.simplify(-H2 - H2) != sp.zeros(2, 2))
check(
    "S0_minus_X_H_block_obstruction", "substantive", ok,
    "-X has H-block -H = diag(1,-1) != H = diag(-1,1) (residual -2H != 0): the depth"
    " mirror is NOT represented in-class by bare generator negation. Recomputes the"
    " banked S3 obstruction (forcing package, TF2_parity_jet_kill_and_constant_lever).",
)

# [2] the V5 swap-candidate facts (banked ADOPTED_swap_dressing_parity_candidate).
F2s = sp.Matrix([[0, 1], [1, 0]])
Fsw = bm(F2s, Z2, Z2, I2)
XmF = sp.simplify(-Fsw * Xg * Fsw.inv())
ok = (XmF[0:2, 0:2] == H2 and XmF[0:2, 2:4] == Z2
      and sp.simplify(XmF[2:4, 2:4] + Kg) == Z2
      and sp.simplify(XmF[2:4, 0:2] + Cg * F2s) == Z2)
check(
    "S0_swap_F_candidate_action", "substantive", ok,
    "-F X F^-1 with F = diag(F2, I2): H-block FIXED, K -> -K (lambda, k_mod, k10 all"
    " ODD), C -> -C.F2 — zero residual. Recomputes the banked V5 candidate facts.",
)

ok = (sp.simplify(F2s.T * eta2 * F2s + eta2) == Z2
      and sp.simplify(F2s.T * eta2 * F2s - eta2) != Z2
      and sp.simplify(Fsw.T * eta4 * Fsw - eta4) != sp.zeros(4, 4)
      and sp.simplify(Fsw.T * eta4 * Fsw + eta4) != sp.zeros(4, 4))
check(
    "S0_swap_F_eta_behavior", "substantive", ok,
    "F2^T eta2 F2 = -eta2 (base-block ANTI-isometry, banked '07-27 F non-Lorentz');"
    " full 4x4: F^T eta F = diag(1,-1,1,1) != +/-eta — F is neither an isometry nor a"
    " full anti-isometry of eta. Consistent with the 07-20 coframe-involution record"
    " (raw_swap_anti_isometry_in_eta).",
)

# [3] commutant of the class is scalars (needed to type J^2).
Zs = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"z{i}{j}"))
eqs = []
for B in [X0] + V_BASIS:
    Comm = sp.expand(Zs * B - B * Zs)
    eqs.extend(list(Comm))
zvars = [sp.Symbol(f"z{i}{j}") for i in range(4) for j in range(4)]
Amat = sp.Matrix([[sp.diff(e, v) for v in zvars] for e in eqs])
null = Amat.nullspace()
ok = (len(null) == 1
      and sp.simplify(sp.Matrix(4, 4, lambda i, j: null[0][4 * i + j])
                      - null[0][0] * sp.eye(4)) == sp.zeros(4, 4))
check(
    "S0_class_commutant_is_scalars", "substantive", ok,
    "Solve [Z, X] = 0 for all class members (X0 + 7-dim V basis): nullspace dim = 1,"
    " spanned by the identity. Hence any J with J^2 acting trivially on the class by"
    " conjugation has J^2 = mu*I (scalar).",
)

# ============================================================================
# L0 — the transcription lemma: mirror on the anchored presentation
# ============================================================================
print("=" * 78)
print("L0 — transcription lemma: phi -> -phi + linear dressing => X |-> -J X J^-1")
print("=" * 78)

# [4] banked E04 closed form solves E' = X E, E(0) = I (recompute).
EH = sp.diag(sp.exp(-phi), sp.exp(phi))
ME04 = bm(EH, Z2, Cg * H2 * (EH - I2), I2)
XE04 = bm(H2, Z2, Cg, Z2)
ok = (is_zero(sp.diff(ME04, phi) - XE04 * ME04)
      and sp.simplify(ME04.subs(phi, 0)) == sp.eye(4))
check(
    "L0_E04_closed_form_recompute", "substantive", ok,
    "Banked Route-B T2 closed form M(phi;C) solves M' = X M, M(0) = I — recomputed"
    " zero-residual (the exact exponential witness used below).",
)

# [5] adjugate cancellation on a fully generic 16-symbol J: adj(J).J = det(J) I —
# the algebraic core of J e^{-phi X} J^-1 = e^{phi(-J X J^-1)} for ANY invertible
# linear dressing.
J16 = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"j{i}{j}"))
ok = sp.expand(J16.adjugate() * J16 - J16.det() * sp.eye(4)) == sp.zeros(4, 4)
check(
    "L0_adjugate_cancellation_generic_J", "substantive", ok,
    "adj(J).J = det(J).I for fully generic 4x4 J (16 symbols) — the cancellation that"
    " makes (J A J^-1)(J B J^-1) = J A B J^-1 an identity for EVERY invertible linear"
    " dressing, with no structure assumed on J.",
)

# [6] the dressed mirrored family solves the dressed ODE (exact instance, block J).
Pgen = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"pP{i}{j}"))
Sgen = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"sS{i}{j}"))
Rgen = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"rR{i}{j}"))
Jb = bm(Pgen, Z2, Rgen, Sgen)
Jbinv = bm(Pgen.inv(), Z2, -Sgen.inv() * Rgen * Pgen.inv(), Sgen.inv())
ok_inv = is_zero(sp.expand(Jb * Jbinv - sp.eye(4)))
Y = Jb * ME04.subs(phi, -phi) * Jbinv
Xdressed = -Jb * XE04 * Jbinv
ok_ode = is_zero(sp.expand(sp.diff(Y, phi) - Xdressed * Y))
ok_anchor = sp.simplify(Y.subs(phi, 0)) == sp.eye(4)
check(
    "L0_dressed_family_solves_dressed_ODE", "substantive", ok_inv and ok_ode and ok_anchor,
    "Y(phi) := J M(-phi;C) J^-1 satisfies Y' = (-J X J^-1) Y and Y(0) = I, verified"
    " zero-residual on the exact E04 exponential with a GENERIC block dressing J"
    " (P, S, R all fully symbolic 2x2). With Picard uniqueness (named Category-A,"
    " banked lane), the mirrored anchored family's generator IS -J X J^-1. The"
    " re-anchoring (right factor J^-1) is forced by the registration E(0) = I:"
    " J E(0) G = I => G = J^-1.",
)

check(
    "L0_transcription_assembly", "guard", True,
    "ASSEMBLED LEMMA (premise P1, DERIVED): on the registered anchored one-parameter"
    " presentation, IF the seal's action on the coframe is a constant invertible"
    " linear map J, THEN the depth mirror phi -> -phi acts on generators as"
    " X |-> -J X J^-1. CHOSE-OR-DERIVED ledger: linearity + phi-independence of J ="
    " the registered constant-generator presentation's own footing (a phi-dependent"
    " dressing would leave the presentation — typed OUT OF SCOPE, not used);"
    " phi -> -phi = CANON (C-2026-06-10-2 wording, C-2026-07-04-1 static-sector"
    " localization).",
)

# ============================================================================
# TC — the dressing classification (TP2 core): Route-B probe/necessity method
# Condition D: -J X J^-1 in the registered class for ALL class members X
# (chart-representability of the fold: premise P2, TYPED below), plus the fold
# composition structure (J^2 acts trivially: J^2 = mu I by S0 commutant).
# ============================================================================
print("=" * 78)
print("TC — dressing classification (the complete compatible set)")
print("=" * 78)

# [7] guard: every element of V.J has zero top block-row (so J v in V.J forces the
# top block-row of J v to vanish).
u7 = bm(Z2, Z2, sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"uc{i}{j}")),
        sp.Matrix([[sp.Symbol("uk00"), 0], [sp.Symbol("uk10"), sp.Symbol("uk11")]]))
ok = (u7 * J16)[0:2, :] == sp.zeros(2, 4)
check(
    "TC_VJ_top_rows_zero", "guard", ok,
    "For any u in V and any J: (u J) has zero top block-row. Hence the class"
    " condition J v J^-1 in V (<=> J v in V J) forces the top block-row of J v = 0.",
)

# [8] necessity: Q = 0 (upper-right block of J), by C/K probes.
forced = set()
for v in V_BASIS:
    top = (J16 * v)[0:2, :]
    for e in top:
        if e != 0:
            forced.add(e)
ok = forced == {sp.Symbol("j02"), sp.Symbol("j03"), sp.Symbol("j12"), sp.Symbol("j13")}
check(
    "TC_Q_block_zero_forced", "substantive", ok,
    "Probing all 7 V-basis directions: the vanishing of the top block-row of J v"
    " forces EXACTLY the four upper-right entries {j02, j03, j12, j13} = Q to zero"
    " and nothing else. Q = 0 NECESSARY; J is block-lower-triangular.",
)

# [9] necessity: S lower-triangular (K-triangularity probe).
Sfull = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"t{i}{j}"))
expr = sp.expand((Sfull * Kg * Sfull.adjugate())[0, 1])
coeffs = [expr.coeff(m) for m in (k00, k10, k11)]
sols = sp.solve(coeffs, [sp.Symbol("t01")], dict=True)
ok_nec = sols == [{sp.Symbol("t01"): 0}]
Slow = sp.Matrix([[sp.Symbol("s00"), 0], [sp.Symbol("s10"), sp.Symbol("s11")]])
ok_suf = sp.simplify(sp.expand((Slow * Kg * Slow.adjugate())[0, 1])) == 0
check(
    "TC_S_lower_triangular_forced", "substantive", ok_nec and ok_suf,
    "(S K adj(S))[0,1] = t00*t01*(k11-k00) - t01^2*k10: zero for all lower-tri K"
    " <=> t01 = 0 (necessity, exact solve); lower-tri S conjugation preserves"
    " K-lower-triangularity identically (sufficiency). S lower-triangular FORCED.",
)

# [10] necessity: P anti-diagonal (H-block of the affine part).
PfH = sp.expand(Pgen * H2 + H2 * Pgen)
sols = sp.solve(list(PfH), [sp.Symbol("pP00"), sp.Symbol("pP11")], dict=True)
ok_nec = sols == [{sp.Symbol("pP00"): 0, sp.Symbol("pP11"): 0}]
p, q = sp.symbols("p q", nonzero=True)
Pad = sp.Matrix([[0, p], [q, 0]])
ok_suf = sp.simplify(-Pad * H2 * Pad.inv() - H2) == Z2
check(
    "TC_P_antidiagonal_forced", "substantive", ok_nec and ok_suf,
    "-P H P^-1 = H <=> P H + H P = 0 <=> P = antidiag(p, q), pq != 0 (both"
    " directions exact). The dressed H-block is restored ONLY by an anti-diagonal"
    " (clock<->ruler-exchanging) base action. NOTE: this reproduces, inside the"
    " registered class, the banked 07-20 base family F_b = [[0,b],[1/b,0]]"
    " (constant_real_classification.general_inverting_involution).",
)

# [11] no Lorentz dressing exists (the family is entirely non-Lorentz).
ok = sp.simplify(Pad.T * eta2 * Pad - sp.diag(q**2, -p**2)) == Z2
ok = ok and (sp.solve([q**2 + 1], [q]) == [])  # q^2 = -1 has no real solution
check(
    "TC_no_lorentz_dressing_exists", "substantive", ok,
    "P^T eta2 P = diag(q^2, -p^2) for anti-diagonal P: equality with eta2 ="
    " diag(-1,1) needs q^2 = -1 — impossible over the reals. NO compatible dressing"
    " is an eta-isometry on the base block: every seal dressing is necessarily"
    " non-Lorentz (generalizes the banked 'F non-Lorentz' fact to the WHOLE"
    " compatible set; consistent with 07-20 no_positive_conformal_eta_solution).",
)

# [12] R is unconstrained by class-preservation (enters only the C-image).
sig = sp.Symbol("sigma")
Rfree = sp.Matrix(2, 2, lambda i, j: sp.Symbol(f"rr{i}{j}"))
Jc = bm(Pad, Z2, Rfree, Slow)
Jcinv = bm(Pad.inv(), Z2, -Slow.inv() * Rfree * Pad.inv(), Slow.inv())
ok_inv = is_zero(sp.expand(Jc * Jcinv - sp.eye(4)))
Xm = sp.expand(-Jc * Xg * Jcinv)
Kt = Xm[2:4, 2:4]
Ct = Xm[2:4, 0:2]
ok_class = (sp.simplify(Xm[0:2, 0:2]) == H2 and Xm[0:2, 2:4] == Z2
            and sp.simplify(Kt[0, 1]) == 0)
ok_Kt = sp.simplify(Kt + Slow * Kg * Slow.inv()) == Z2
ok_R_free = Kt.free_symbols.isdisjoint(Rfree.free_symbols)
ok_Ct = is_zero(sp.expand(
    Ct - (-(Rfree * H2 + Slow * Cg) * Pad.inv()
          + Slow * Kg * Slow.inv() * Rfree * Pad.inv())))
check(
    "TC_R_unconstrained_and_blocks_exact", "substantive",
    ok_inv and ok_class and ok_Kt and ok_R_free and ok_Ct,
    "With Q=0, P anti-diagonal, S lower-tri and R ARBITRARY: -J X J^-1 is in-class"
    " for every member, with EXACT block laws K~ = -S K S^-1 (R-free) and"
    " C~ = -(R H + S C) P^-1 + S K S^-1 R P^-1 (an affine map: R gives a constant"
    " offset -R H P^-1 plus a K->C shear). Class-preservation alone does NOT cut R.",
)

# [13] involution: J^2 = mu I; realness forces mu = pq > 0; scale gauge.
J2 = sp.expand(Jc * Jc)
ok_P2 = sp.simplify(J2[0:2, 0:2] - p * q * I2) == Z2
S2 = sp.expand(Slow * Slow)
# S^2 = pq I: diagonal gives s00^2 = s11^2 = pq; realness: pq = s00^2 > 0.
eq_offdiag = S2[1, 0]        # s10*(s00 + s11)
sols_s11 = sp.solve(sp.Eq(S2[0, 0], S2[1, 1]), sp.Symbol("s11"))
ok_s11 = set(sols_s11) == {sp.Symbol("s00"), -sp.Symbol("s00")}
ok_branch_a = sp.simplify(eq_offdiag.subs(sp.Symbol("s11"), sp.Symbol("s00"))
                          ) == 2 * sp.Symbol("s00") * sp.Symbol("s10")
ok_branch_b = sp.simplify(eq_offdiag.subs(sp.Symbol("s11"), -sp.Symbol("s00"))) == 0
# scale gauge: c J induces the same dressing action
csc = sp.Symbol("c_scale", nonzero=True)
ok_gauge = is_zero(sp.expand((csc * Jc) * Xg * (Jcinv / csc) - Jc * Xg * Jcinv))
check(
    "TC_involution_and_realness", "substantive",
    ok_P2 and ok_s11 and ok_branch_a and ok_branch_b and ok_gauge,
    "J^2 = [[pq I, 0],[RP+SR, S^2]]; centrality (S0 commutant) => S^2 = pq I and"
    " RP + SR = 0. Lower-tri S: s00^2 = s11^2 = pq, s10(s00+s11) = 0 => branch (a)"
    " s11 = s00, s10 = 0 (S = sigma I) or branch (b) s11 = -s00 (s10 free)."
    " REALNESS: pq = s00^2 > 0 (real square; named Category-A positivity) — the"
    " J^2 = -I complex-structure branch is EMPTY over the reals. Scale gauge"
    " J -> cJ leaves the action invariant (zero residual): normalize pq = 1.",
)

# normalized family pieces
Pn = sp.Matrix([[0, p], [1 / p, 0]])           # pq = 1
s0, s1v = sp.Symbol("s0"), sp.Symbol("s1")
Sa = lambda sgn: sgn * I2                       # branch (a), sigma = +/-1
Sb = sp.Matrix([[s0, 0], [s1v, -s0]])           # branch (b), s0 = +/-1, s1 free

# [14] R-space per branch: solve R P + S R = 0 -> dim 2 each.
r0, r1, r2, r3 = sp.symbols("r0 r1 r2 r3")
Rg = sp.Matrix([[r0, r1], [r2, r3]])
dims = {}
bases_note = {}
for label, S, subs in [("a_sigma_plus", I2, {}), ("a_sigma_minus", -I2, {}),
                       ("b_s0_plus", Sb.subs(s0, 1), {}),
                       ("b_s0_minus", Sb.subs(s0, -1), {})]:
    eqsR = list(sp.expand(Rg * Pn + S * Rg))
    Am = sp.Matrix([[sp.diff(e, v) for v in (r0, r1, r2, r3)] for e in eqsR])
    ns = Am.nullspace()
    dims[label] = len(ns)
ok = all(d == 2 for d in dims.values())
# spot instance at exact rationals for the generic-symbol branch-(b) solve
Am_i = sp.Matrix([[sp.diff(e, v) for v in (r0, r1, r2, r3)]
                  for e in list(sp.expand(Rg * Pn.subs(p, 2)
                                          + Sb.subs({s0: 1, s1v: 3}) * Rg))])
ok = ok and len(Am_i.nullspace()) == 2
check(
    "TC_R_solution_space_dim_2_per_branch", "substantive", ok,
    f"R P + S R = 0 solved exactly: nullity {dims} — TWO R-parameters in every"
    " branch (symbolic p, s1; exact-rational spot instance p=2, s1=3 confirms)."
    " Branch (a): rows of R proportional to (1, -sigma p).",
)

check(
    "TC_family_assembly", "guard", True,
    "COMPLETE COMPATIBLE SET (the TP2 classification, normalized pq = 1): J ="
    " [[antidiag(p, 1/p), 0], [R, S]] with p != 0 free; S in branch (a) {+I, -I} or"
    " branch (b) {[[s0,0],[s1,-s0]]: s0 = +/-1, s1 free}; R in the 2-dim branch"
    " solution space of RP + SR = 0. A FAMILY, NOT unique and NOT empty —"
    " continuous parameters PER BRANCH (A4): branch (a): 3 (p + 2 R; sigma = +/-1"
    " discrete); branch (b): 4 (p, s1 + 2 R; s0 = +/-1 discrete). The V5 swap F = member"
    " (p=1, S=+I, R=0). Conditions that cut it: class-preservation (Q=0, S"
    " lower-tri, P anti-diag), fold composition (J^2 scalar), realness (pq>0).",
)

# [15] V5 adjudication: F is IN the family; the family has OTHER members, so the
# premise "dressing = F" is NOT forced by these conditions.
okF = (Fsw == bm(Pn.subs(p, 1), Z2, Z2, I2))
Jalt = bm(Pn.subs(p, 2), Z2, Z2, I2)   # p=2 member, also compatible
XmAlt = sp.expand(-Jalt * Xg * Jalt.inv())
ok_alt = (XmAlt[0:2, 0:2] == H2 and XmAlt[0:2, 2:4] == Z2
          and sp.simplify(XmAlt[2:4, 2:4] + Kg) == Z2
          and sp.expand(Jalt * Jalt) == sp.eye(4)
          and sp.simplify(Jalt - Fsw) != sp.zeros(4, 4))
check(
    "TC_V5_adjudicated_inside_family", "substantive", okF and ok_alt,
    "The banked V5 candidate F = diag(F2, I2) IS the family member (p=1, S=+I,"
    " R=0). A DISTINCT member (p=2, S=+I, R=0) is exhibited: involutive, in-class"
    " action, not equal to F. VERDICT: the swap premise is NOT forced by the banked"
    " seal conditions (F-P2 honored: F adjudicated, not adopted) — but see TP3:"
    " the lambda/k_mod parities V5 computed hold for EVERY family member.",
)

# ============================================================================
# TP3 — the parity computation on the classified family
# ============================================================================
print("=" * 78)
print("TP3 — parities per moduli sector")
print("=" * 78)

# [16] the trace leg — dressing-INDEPENDENT (any invertible linear J).
ok = sp.expand(sp.trace(J16 * Xg * J16.adjugate()) - J16.det() * sp.trace(Xg)) == 0
check(
    "TP3_trace_similarity_generic_J", "substantive", ok,
    "tr(J X adj(J)) = det(J) tr(X) for FULLY GENERIC 4x4 J (16 symbols): trace is"
    " similarity-invariant, so tr(-J X J^-1) = -tr X for EVERY invertible linear"
    " dressing. With tr X = 2*lambda (tr H = 0): eps_lambda = -1 holds on the whole"
    " GL(4) dressing class — it does NOT depend on which dressing the seal supplies.",
)

# [17] lambda and k_mod odd, family-uniform (diag preserved by lower-tri conj).
SKS = sp.expand(Slow * Kg * Slow.inv())
ok_diag = (sp.simplify(SKS[0, 0] - k00) == 0 and sp.simplify(SKS[1, 1] - k11) == 0)
lam_t = sp.simplify((Kt[0, 0] + Kt[1, 1]) / 2)
kmod_t = sp.simplify((Kt[1, 1] - Kt[0, 0]) / 2)
ok_par = (sp.simplify(lam_t + LAM) == 0 and sp.simplify(kmod_t + KMOD) == 0)
check(
    "TP3_lambda_kmod_odd_family_uniform", "substantive", ok_diag and ok_par,
    "diag(S K S^-1) = diag(K) for every lower-tri S (triangular algebra), so"
    " K~ = -S K S^-1 gives lambda~ = -lambda and k_mod~ = -k_mod for EVERY member of"
    " the compatible family (any p, any S branch, any R). eps_lambda = eps_kmod = -1"
    " DERIVED family-uniformly under premise P2 (chart-representability).",
)

# [18] k10: branch split.
Kta = sp.expand(-(I2 * Kg * I2))                       # S = +I (sigma cancels)
ok_a = sp.simplify(Kta[1, 0] + k10) == 0
for s0val in (1, -1):
    Sbv = Sb.subs(s0, s0val)
    Ktb = sp.expand(-(Sbv * Kg * Sbv.inv()))
    okb = sp.simplify(Ktb[1, 0] - (k10 + 2 * (s1v / s0val) * KMOD)) == 0
    ok_a = ok_a and okb
check(
    "TP3_k10_branch_split", "substantive", ok_a,
    "k10~ = -k10 on branch (a) (S = +/-I): ODD. k10~ = +k10 + 2(s1/s0) k_mod on"
    " branch (b): EVEN up to a k_mod-shear (which vanishes on the k_mod = 0 fixed"
    " locus). eps_k10 is NOT family-uniform: it is decided by the S-branch — exactly"
    " the screen/angular completion the banked 07-20 record left NON-UNIQUE"
    " (angular +I / -I vs axis-reflection; 'selector: not supplied').",
)

# [19] C sector: signature (2 odd + 2 even) forced; WHICH combinations supplied.
x = sp.Symbol("x")
target = sp.expand((x - 1)**2 * (x + 1)**2)
ok_sig = True
for label, S in [("a+", I2), ("a-", -I2),
                 ("b+", Sb.subs(s0, 1)), ("b-", Sb.subs(s0, -1))]:
    # map C |-> -S C P on basis E00,E01,E10,E11 (row-major vec)
    cols = []
    for E in (sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [0, 0]]),
              sp.Matrix([[0, 0], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])):
        img = sp.expand(-S * E * Pn)
        cols.append([img[0, 0], img[0, 1], img[1, 0], img[1, 1]])
    Mc = sp.Matrix(cols).T
    cp = sp.expand(Mc.charpoly(x).as_expr())
    ok_sig = ok_sig and sp.simplify(cp - target) == 0
check(
    "TP3_C_signature_2odd_2even_forced", "substantive", ok_sig,
    "The linear C-action C |-> -S C P (R = 0) has characteristic polynomial"
    " (x-1)^2 (x+1)^2 in EVERY branch, for symbolic p (and s1): exactly TWO odd and"
    " TWO even C-combinations, family-uniformly. The parity SIGNATURE of the C"
    " sector is DERIVED; which combinations are odd is member-dependent.",
)

# [20] the odd/even C-basis moves with p (the supplied calibration).
# For S = +I: mu_i+- = p*c_i0 +- c_i1; odd space = span{(1,p)} per row.
Ct_p = sp.expand(-(I2) * Cg * Pn)
mu_plus_0 = p * c00 + c01
mu_minus_0 = p * c00 - c01
mu_p_img = sp.expand(p * Ct_p[0, 0] + Ct_p[0, 1])
mu_m_img = sp.expand(p * Ct_p[0, 0] - Ct_p[0, 1])
ok_odd = sp.simplify(mu_p_img + mu_plus_0) == 0     # mu+ -> -mu+  (odd)
ok_even = sp.simplify(mu_m_img - mu_minus_0) == 0   # mu- -> +mu-  (even)
ok_moves = sp.simplify((p * c00 + c01).subs(p, 1) - (p * c00 + c01).subs(p, 2)) != 0
check(
    "TP3_C_basis_p_dependent", "substantive", ok_odd and ok_even and ok_moves,
    "At S = +I: the ODD combinations are mu_i+ = p c_i0 + c_i1 and the EVEN are"
    " mu_i- = p c_i0 - c_i1 (zero residual) — the basis depends explicitly on the"
    " family parameter p (and flips role under sigma -> -sigma, shifts under R)."
    " WHICH two C-combinations are odd = SUPPLIED (the completion calibration).",
)

# [21] R gives an affine offset (and a K->C shear), spectrum unchanged.
offset = sp.expand(-Rfree * H2 * Pad.inv())
ok_off = any(sp.simplify(e) != 0 for e in offset)   # nonzero as polynomial in r's
check(
    "TP3_R_affine_offset_and_triangularity", "substantive", ok_off and ok_Ct,
    "With R != 0 the C-action is AFFINE: constant offset -R H P^-1 (nonzero for"
    " generic R) + linear part + a K->C shear (block law verified in check"
    " TC_R_unconstrained_and_blocks_exact). The moduli map is block-triangular"
    " (K~ depends on K only), so the parity spectrum {(-1)^3 on K-diag... } is"
    " R-independent; R shifts WHERE the odd combinations are forced to sit"
    " (affine fixed values instead of 0). Map fact, stamped.",
)

# [22] chart-escape witness: OUT-of-class dressing mirrors a k_mod != 0 member.
kk = sp.Symbol("kk", nonzero=True)
Xk = sp.diag(-1, 1, -kk, kk)          # class member: lambda = 0, k_mod = kk
Jout = bm(F2s, Z2, Z2, F2s)
ok_wit = sp.simplify(Jout * Xk * Jout.inv() + Xk) == sp.zeros(4, 4)
# A4 sign fix + hardening: the off-triangular entry is EXACTLY -k10 (not +k10).
ok_out = sp.simplify(sp.expand((F2s * Kg * F2s.adjugate())[0, 1]) + k10) == 0
check(
    "TP3_chart_escape_witness_kmod", "substantive", ok_wit and ok_out,
    "J_out = diag(F2, F2) satisfies J_out X J_out^-1 = -X for the member"
    " X = diag(-1,1,-k,k) (lambda = 0, k_mod = k != 0) — a fold-invariant member"
    " with k_mod != 0 EXISTS if the dressing may leave the registered chart"
    " (F2 on the screen violates S-lower-triangularity: (F2 K adj F2)[0,1] = -k10"
    " != 0 generically; sign per amendment A4, now checked as an exact equality)."
    " The k_mod kill is therefore CHART-CONDITIONAL (premise"
    " P2). The lambda kill is NOT escapable this way (trace leg, check 16).",
)

check(
    "TP3_verdict_assembly", "guard", True,
    "PARITY VERDICT (stamps: registered class; anchored presentation; premise"
    " ladder P0 = fold canon (CANON), P1 = transcription (DERIVED, L0), P2 ="
    " chart-representability (TYPED, chose-or-derived: NOT derived — its"
    " alternative is J07-type cross-chart transition data, banked-open)):"
    " lambda: eps = -1 DERIVED, dressing-independent (needs only P0+P1);"
    " k_mod: eps = -1 DERIVED under P2, family-uniform (escapable only by leaving"
    " the chart — witness above); k10: CONSTRAINED (branch (a) -1, branch (b) +1"
    " with k_mod-shear) — missing datum = the screen/angular completion (07-20"
    " MULTIPLE_COMPLETIONS residue); C: CONSTRAINED (signature 2 odd + 2 even"
    " FORCED; which combinations = supplied calibration p, branch, R).",
)

# ============================================================================
# TP4 — fixed loci and consequences as map facts
# ============================================================================
print("=" * 78)
print("TP4 — fixed loci (mirror-invariant constant members) and landings")
print("=" * 78)

# [23] branch (a) fixed locus: X = -J X J^-1  <=>  J X + X J = 0.
ra, rb = sp.symbols("ra rb")
sols_fix = {}
for sigval in (1, -1):
    Rbr = sp.Matrix([[ra, -sigval * p * ra], [rb, -sigval * p * rb]])
    Jfix = bm(Pn, Z2, Rbr, sigval * I2)
    eqs = list(sp.expand(Jfix * Xg + Xg * Jfix))
    sol = sp.solve(eqs, MODULI, dict=True)
    sols_fix[sigval] = sol
ok_a = True
for sigval, sol in sols_fix.items():
    ok_a = ok_a and len(sol) == 1
    s = sol[0]
    ok_a = ok_a and s.get(k00, 0) == 0 and s.get(k11, 0) == 0 and s.get(k10, 0) == 0
    solved_c = [v for v in (c00, c01, c10, c11) if v in s]
    ok_a = ok_a and len(solved_c) == 2          # 2 C-conditions -> dim-2 locus
# banked cross-check at the F member (p=1, sigma=1, R=0):
JF = bm(Pn.subs(p, 1), Z2, Z2, I2)
solF = sp.solve(list(sp.expand(JF * Xg + Xg * JF)), MODULI, dict=True)
sF = solF[0]
ok_F = (sF.get(k00, 0) == 0 and sF.get(k11, 0) == 0 and sF.get(k10, 0) == 0
        and sp.simplify(sF.get(c00, c00) + c01) == 0
        and sp.simplify(sF.get(c10, c10) + c11) == 0)
check(
    "TP4_fixed_locus_branch_a", "substantive", ok_a and ok_F,
    "Branch (a) (S = sigma I, symbolic p, R generic in its 2-dim space): the"
    " mirror-invariant locus is k00 = k11 = k10 = 0 (K = 0 entirely) with exactly"
    " two C-conditions (dim-2 locus; affine-shifted when R != 0). At the F member"
    " (p=1, sigma=1, R=0): K = 0 and (c00, c10) = (-c01, -c11) — EXACTLY the banked"
    " Route-B T5 swap column cell (E02 ∩ swap: dim 2). F-P5 consistency: the banked"
    " swap locus is recovered as this family member's fixed locus.",
)

# [24] branch (b) fixed locus: k10 FREE (dim-3 locus).
ok_b = True
for s0val in (1, -1):
    Jfixb = bm(Pn, Z2, Z2, Sb.subs(s0, s0val))
    eqs = list(sp.expand(Jfixb * Xg + Xg * Jfixb))
    sol = sp.solve(eqs, MODULI, dict=True)
    ok_b = ok_b and len(sol) == 1
    s = sol[0]
    ok_b = ok_b and s.get(k00, 0) == 0 and s.get(k11, 0) == 0
    ok_b = ok_b and (k10 not in s)              # k10 unconstrained
    solved_c = [v for v in (c00, c01, c10, c11) if v in s]
    ok_b = ok_b and len(solved_c) == 2          # dim-3 locus (k10 + 2 C free)
check(
    "TP4_fixed_locus_branch_b", "substantive", ok_b,
    "Branch (b) (axis-type S, s1 symbolic, R = 0 representative): mirror-invariant"
    " locus is k00 = k11 = 0 with k10 FREE and two C-conditions (dim-3 locus)."
    " The k10 dial survives the fold exactly on the branch-(b) completions.",
)

# [25] a_F landings and T4 loci.
aF_4D = 2 * LAM
aF_triad = 1 + 2 * LAM
sub0 = {k00: 0, k11: 0}
ok = (aF_4D.subs(sub0) == 0 and aF_triad.subs(sub0) == 1
      and sp.Rational(0) != sp.Rational(-1, 2))
# det e^{phi X} = e^{phi tr X} = 1 on the locus (4D volume-blind): diagonal witness
Xdiag0 = sp.diag(-1, 1, 0, 0)
ok_det = sp.simplify(sp.exp(phi * sp.trace(Xdiag0)) - 1) == 0
check(
    "TP4_aF_anchor_landing", "substantive", ok and ok_det,
    "On the forced locus lambda = k_mod = 0: P1-4D anchored pairing weight"
    " a_F = 2 lambda = 0 — the 4D-anchored branch lands ON a_F = 0. AT THAT"
    " LANDING (corrected per amendment A1): the banked massive-locus certificate's"
    " PREMISE ('nonempty at every a_F != 0 background') FAILS — massive-locus"
    " nonemptiness there is UNCERTIFIED on banked footing, NOT refuted"
    " (premise-failure, not a massless verdict: the quadratic atlas and the I_p"
    " sign-change certificate both presuppose a_F != 0). The banked 'no lambda-row"
    " either way' statement is the a_F' = 0 criterion (the P2 pairing, whose"
    " anchor weight is identically zero), NOT the weight VALUE a_F = 0: under"
    " P1-4D at lambda = 0, a_F' = 2 != 0 (check A1_aFprime_vs_aF_distinction), so"
    " the lambda-row does NOT vanish by banked pairing-relativity there — its"
    " status at an a_F = 0 background is UNDERIVED. P1-triad weight"
    " a_F = 1 + 2 lambda = 1 != 0: the triad-anchored branch's certificate premise"
    " is INTACT. T4 loci: the locus is lambda = 0 = the det-one/E07 axis (4D"
    " volume-blind: det e^{phi X} = 1, recomputed) and does NOT meet the"
    " triad-blind line lambda = -1/2. Map facts only; no pairing branch adopted.",
)

# [25b — amendment A1] the a_F'-vs-a_F distinction as a zero-residual check: the
# banked no-lambda-row criterion is a_F' = 0 (the pairing weight's lambda-
# DERIVATIVE identically zero — the P2 pairing), NOT the weight VALUE a_F = 0.
lamS = sp.Symbol("lambda")
aF4D_l = 2 * lamS                # P1-4D anchor weight (banked enumerated family)
aFtri_l = 1 + 2 * lamS           # P1-triad
aFP2_l = sp.Integer(0) * lamS    # P2: a_F identically 0 => a_F' identically 0
ok_a1 = (sp.diff(aF4D_l, lamS).subs(lamS, 0) == 2       # a_F'(0) = 2 != 0
         and aF4D_l.subs(lamS, 0) == 0                  # the VALUE coincidence
         and sp.diff(aFP2_l, lamS) == 0                 # the criterion's holder
         and sp.diff(aFtri_l, lamS).subs(lamS, 0) == 2)
check(
    "A1_aFprime_vs_aF_distinction", "substantive", ok_a1,
    "AMENDMENT A1 (verifier-caught, credited): under P1-4D at the forced landing"
    " lambda = 0 the anchor weight VALUE is a_F = 0 but its lambda-DERIVATIVE is"
    " a_F' = 2 != 0, computed against the banked pairing definitions (P1-4D"
    " a_F = 2 lambda; P1-triad a_F = 1 + 2 lambda; P2 a_F identically 0). The"
    " banked 'no lambda-row either way' statement is the a_F' = 0 criterion (the"
    " P2 pairing: forcing package Sec. 4; Slice-2b), which P1-4D at lambda = 0"
    " does NOT satisfy — so the lambda-row form a_F'*Int(p0 W_F Ltilde) does not"
    " vanish by banked pairing-relativity at the landing, and the a_F = 0"
    " background's lambda-row status is UNDERIVED on banked footing. Drift"
    " direction memorialized: the original prose was CUTTING-side inflation"
    " (anti-massive) — caught by the blind verifier.",
)

check(
    "TP4_kmod0_stratum_landing", "guard", True,
    "k_mod = 0 places every mirror-invariant constant member ON the banked KMOD0"
    " stratum: the banked stratum-identity bookkeeping (one integrated-row"
    " dependency on the constant census; pointwise dependency on the field census —"
    " forcing package S8) applies to the entire fixed locus. Branch (a) further"
    " forces K = 0 (the E04 stratum, C-carrying).",
)

check(
    "TP4_S3_lever_application", "guard", True,
    "Applying the BANKED S3 lever (TF2_parity_jet_kill_and_constant_lever — reused,"
    " not re-derived) with the parities derived here: CONSTANT-census branch (BASE),"
    " under P0+P1+P2: the constant lambda and k_mod dials are parity-killed"
    " (forced to 0; the constant direction is fold-inadmissible) — the CUTTING"
    " outcome FIRES for the (lambda, k_mod) sector; k10 constant killed on branch"
    " (a) completions only; two C-combinations forced (to 0, or to R-shifted affine"
    " values). FIELD-census branch (BR-M): no collapse — lambda(x), k_mod(x) forced"
    " ODD about the wall (fields), k10/C per branch. BOTH census branches carried;"
    " neither adopted (F-P4). Ceiling: these are map facts; no massive-branch"
    " verdict language.",
)

# [26] K4 composition honesty: the residual chart quotient cannot flip the
# derived parities within the real family.
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
Jf0 = bm(Pn, Z2, Z2, I2)
J23 = R23 * Jf0
ok_23 = (sp.expand(J23 * J23) == sp.eye(4)
         and sp.simplify(J23[2:4, 2:4] + I2) == Z2)   # = branch (a) sigma = -1
J12 = R12 * Jf0
ok_12 = sp.simplify(sp.expand(J12 * J12) - sp.diag(-1, -1, 1, 1)) == sp.zeros(4, 4)
check(
    "TP4_K4_composition_honesty", "substantive", ok_23 and ok_12,
    "R23(pi) o J stays in the family (it is the sigma -> -sigma member: C-parity"
    " roles swap — part of the family freedom already counted). R12(pi) o J has"
    " square diag(-1,-1,1,1) != scalar: NOT an involutive dressing — the K4 chart"
    " quotient CANNOT flip the k10-parity branch within the real family. The"
    " classification is K4-honest (moduli read modulo K4, banked A1).",
)

# ============================================================================
# Consistency / falsifier guards
# ============================================================================
check(
    "X_0720_family_transport", "guard", True,
    "F-P5 consistency with the banked 07-20 coframe-involution record: the derived"
    " base family antidiag(p, 1/p) IS the banked F_b = [[0,b],[1/b,0]] family"
    " (b = p) transported into the registered class; the S-branches {+I, -I,"
    " axis-type} realize exactly the banked non-unique angular extensions"
    " (conjugacy traces 2, -2, 0); MULTIPLE_COMPLETIONS is REFINED, not"
    " contradicted: this package adds the R-mixing freedom (base->screen), the"
    " involution/realness cut (pq > 0), and the family-uniform parity facts."
    " No banked contradiction found (F-P5 not fired).",
)

check(
    "X_scope_and_falsifiers", "guard", True,
    "F-P1: both directions audited — the cutting legs (lambda/k_mod kill) carry"
    " their premise ladder visibly (P2 typed, NOT derived; escape witness"
    " computed); the harmless legs (k10/C supplied) carry the exact missing datum."
    " F-P2: no dressing adopted; V5 = adjudicated family member. F-P3: stamps on"
    " every claim (registered class, anchored presentation, premise ladder, census"
    " branch, branch (a)/(b), R). F-P4: no Route-D result cited; census fork open."
    " F-P6: see exit code. SCOPE: full declared scope, no scope-ladder reduction;"
    " phi-dependent (non-constant) dressings are outside the registered"
    " constant-generator presentation and are TYPED out of scope, not classified.",
)

# ============================================================================
# ADOPTED — blind-verifier legs adopted as in-package checks (amendment pass,
# A3/A4; all credited to VERIFIER_INDEPENDENT_CHECK.py, blind verifier
# 2026-07-29; 41/41 there)
# ============================================================================
print("=" * 78)
print("ADOPTED — verifier catch-proofs and completed legs (credited)")
print("=" * 78)

# [27] the compensation-loophole-closing lemma (verifier V2b): for ANY
# block-lower-triangular J the image H-block is EXACTLY -P H P^-1 and the image
# upper-right block is exactly zero — R CANNOT compensate, so the P-necessity
# step (check TC_P_antidiagonal_forced) needs no assumption on R.
IMGgen_full = sp.expand(-Jb * Xg * Jbinv)
ok_lem = (is_zero(sp.expand(IMGgen_full[0:2, 0:2] - (-Pgen * H2 * Pgen.inv())))
          and IMGgen_full[0:2, 2:4] == Z2)
check(
    "ADOPTED_H_block_R_cannot_compensate", "substantive", ok_lem,
    "ADOPTED (verifier V2b, credited): for ANY block-lower-triangular J ="
    " [[P,0],[R,S]] with P, S, R fully generic 2x2, the image -J X J^-1 of a"
    " generic class member has H-block EXACTLY -P H P^-1 and upper-right block"
    " exactly 0 — the mixing block R cannot compensate the base action. This"
    " closes the compensation loophole the package's P-necessity step used"
    " implicitly.",
)

# [28] mutation catch-proof (verifier V3_catch_kmod_even_is_false): the FALSE
# claim eps_kmod = +1 must FAIL the machinery.
ok_m1 = sp.simplify(kmod_t - KMOD) != 0
check(
    "ADOPTED_catch_wrong_parity_kmod_even", "substantive", ok_m1,
    "ADOPTED mutation catch-proof (verifier V3_catch_kmod_even_is_false,"
    " credited): the WRONG-PARITY claim eps_kmod = +1 (k_mod EVEN) fails — the"
    " family image has k_mod~ = -k_mod, so k_mod~ - k_mod = -2 k_mod != 0."
    " CAUGHT by the same machinery that passes the true claim.",
)

# [29] mutation catch-proof (verifier V3_catch_wrong_signature_fails): the
# FALSE C-signature (x-1)^3 (x+1) must FAIL.
mutp = sp.expand((x - 1) ** 3 * (x + 1))
ok_m2 = sp.simplify(cp - mutp) != 0
check(
    "ADOPTED_catch_wrong_C_signature", "substantive", ok_m2,
    "ADOPTED mutation catch-proof (verifier V3_catch_wrong_signature_fails,"
    " credited): the WRONG-SIGNATURE claim charpoly = (x-1)^3 (x+1) (3 even + 1"
    " odd) fails against the computed C-action charpoly (x-1)^2 (x+1)^2. CAUGHT.",
)

# [30] mutation catch-proof (verifier V3_catch_k10_odd_on_branch_b_fails): the
# FALSE claim 'k10 ODD on branch (b)' must FAIL.
Sb1 = Sb.subs(s0, 1)
Ktb1 = sp.expand(-(Sb1 * Kg * Sb1.inv()))
ok_m3 = sp.simplify(Ktb1[1, 0] + k10) != 0
check(
    "ADOPTED_catch_k10_odd_on_branch_b", "substantive", ok_m3,
    "ADOPTED mutation catch-proof (verifier V3_catch_k10_odd_on_branch_b_fails,"
    " credited): the claim k10~ = -k10 on branch (b) fails — there"
    " k10~ = +k10 + 2(s1/s0) k_mod, so k10~ + k10 = 2 k10 + 2 s1 k_mod != 0."
    " CAUGHT: the branch split (check TP3_k10_branch_split) has teeth.",
)

# [31] mutation catch-proof (verifier V2f_attack_screen_swap_fails_class): the
# FALSE claim 'screen-swap dressing is in-class' must FAIL.
Jat2 = bm(sp.Matrix([[0, 1], [1, 0]]), Z2, Z2, F2s)
im2 = sp.expand(-Jat2 * Xg * Jat2.inv())
ok_m4 = sp.simplify(im2[2:4, 2:4][0, 1]) != 0
check(
    "ADOPTED_catch_screen_swap_in_class", "substantive", ok_m4,
    "ADOPTED mutation catch-proof (verifier V2f_attack_screen_swap_fails_class,"
    " credited): the dressing with S = F2 (screen swap) maps a generic member"
    " OUT of the registered class — the image K-block's upper entry is nonzero"
    " generically. CAUGHT: S-lower-triangularity (check"
    " TC_S_lower_triangular_forced) is genuinely cutting.",
)

# [32] completed K4-honesty leg (verifier V7_R13_composition_not_involutive):
# the THIRD nontrivial K4 element (the package checked R23 and R12).
R13 = sp.diag(1, -1, 1, -1)
J13 = R13 * Jf0
ok_k4 = sp.simplify(sp.expand(J13 * J13) - sp.diag(-1, -1, 1, 1)) == sp.zeros(4, 4)
check(
    "ADOPTED_K4_R13_non_involutive", "substantive", ok_k4,
    "ADOPTED (verifier V7_R13_composition_not_involutive, credited): R13(pi) o J"
    " squares to diag(-1,-1,1,1) != scalar — like R12 o J, NOT an involutive"
    " dressing. With this leg all THREE nontrivial K4 elements are checked"
    " (R23 in-family; R12, R13 non-involutive): the K4 chart quotient cannot"
    " flip the k10-parity branch within the real family — the"
    " TP4_K4_composition_honesty claim is now complete, not sampled.",
)

# ============================================================================
# Outputs
# ============================================================================
n_pass = sum(1 for c in CHECKS if c["pass"])
n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_guard = sum(1 for c in CHECKS if c["kind"] == "guard")
all_ok = n_pass == len(CHECKS)

print("=" * 78)
print(f"TOTAL: {n_pass}/{len(CHECKS)} checks pass "
      f"({n_sub} substantive + {n_guard} guard)")
print("=" * 78)

results = {
    "package": "udt_p4_routeP_seal_parity_2026-07-29",
    "contract": "PREREGISTRATION.md (frozen)",
    "amendment": "A1-A4 applied post-verifier (VERIFIER_REPORT.md"
                 " PASS-WITH-REQUIRED-AMENDMENTS; CORRECTION_LAYER.md): A1"
                 " aF_landing / check-25 prose corrected (the banked no-lambda-row"
                 " criterion is a_F' = 0, not the value a_F = 0; landing ="
                 " certificate-premise failure = UNCERTIFIED, not refuted); A3/A4"
                 " verifier catch-proofs + K4 leg + H-block lemma adopted"
                 " (credited). No pre-amendment computed claim changed.",
    "outcome_class": "OP3 (mixed per-sector)",
    "premise_ladder": {
        "P0": "fold = Z2 quotient, depth mirror phi->-phi (CANON C-2026-06-10-2,"
              " C-2026-07-04-1; eps_phi = -1 is canon-definitional for the depth"
              " field, static sector)",
        "P1": "transcription X |-> -J X J^-1 for a constant linear frame dressing"
              " J (DERIVED, L0; Picard named Category-A)",
        "P2": "chart-representability: the mirror acts ON the registered class"
              " (TYPED, not derived; alternative = J07 cross-chart transition"
              " data, banked-open)",
    },
    "dressing_classification": {
        "verdict": "NONEMPTY FAMILY (not unique, not empty)",
        "form": "J = [[antidiag(p,1/p), 0],[R, S]], pq=1 normalized; S in"
                " {+I,-I} (branch a) or [[s0,0],[s1,-s0]], s0=+-1 (branch b);"
                " R in the 2-dim solution space of RP+SR=0; continuous"
                " parameters per branch (A4): branch (a) 3 (p + 2 R), branch"
                " (b) 4 (p, s1 + 2 R)",
        "cutting_conditions": ["class-preservation: Q=0, S lower-tri, P antidiag",
                                "fold composition: J^2 = scalar",
                                "realness: pq = s00^2 > 0 (no J^2=-I branch)"],
        "no_lorentz_member": True,
        "V5_swap_F": "family member (p=1, S=+I, R=0); premise NOT forced",
    },
    "parity_verdict": {
        "lambda": {"status": "DERIVED", "eps": -1,
                   "basis": "trace similarity-invariance; dressing-INDEPENDENT"
                            " (any invertible linear J); needs P0+P1 only"},
        "k_mod": {"status": "DERIVED (under P2)", "eps": -1,
                  "basis": "diag preserved by lower-tri conjugation;"
                           " family-uniform; chart-escape witness shows P2 is"
                           " load-bearing"},
        "k10": {"status": "CONSTRAINED", "eps": "branch (a): -1; branch (b): +1"
                          " (+ k_mod-shear)",
                "missing_datum": "the screen/angular completion of the seal"
                                 " involution (banked 07-20 MULTIPLE_COMPLETIONS"
                                 " residue; selector not supplied)"},
        "C": {"status": "CONSTRAINED",
              "forced": "signature exactly 2 ODD + 2 EVEN combinations"
                        " (family-uniform)",
              "missing_datum": "WHICH combinations: the calibration (p, S-branch,"
                               " R) — same supplied completion + quadratic"
                               " readout (07-20 smallest missing object)"},
    },
    "consequences_map_facts": {
        "constant_census_BASE": "under P0+P1+P2: lambda and k_mod dials"
            " parity-killed (0); branch (a) also k10 -> 0 (K = 0, E04 stratum);"
            " 2 C-combinations forced; locus dim 2 (a) / 3 (b)",
        "aF_landing": "P1-4D a_F = 2 lambda -> 0: the massive-locus"
            " certificate's PREMISE (a_F != 0) FAILS at the landing —"
            " nonemptiness there UNCERTIFIED on banked footing, NOT refuted"
            " (premise-failure, not a massless verdict; atlas + I_p certificate"
            " presuppose a_F != 0). The banked no-lambda-row criterion is"
            " a_F' = 0 (the P2 pairing), NOT the value a_F = 0: P1-4D has"
            " a_F'(0) = 2 != 0, so the lambda-row's status at a_F = 0 is"
            " UNDERIVED (A1 corrected). P1-triad a_F = 1 (premise INTACT)",
        "T4_loci": "locus = lambda = 0 (det-one/E07 axis, 4D volume-blind);"
            " k_mod = 0 (KMOD0 stratum); NOT on lambda = -1/2",
        "banked_swap_cell_recovered": "F member fixed locus = Route-B T5 swap"
            " column (K=0, (c00,c10)=(-c01,-c11), dim 2)",
        "field_census_BRM": "no collapse; lambda(x), k_mod(x) forced ODD;"
            " k10/C per branch",
    },
    "checks": CHECKS,
    "counts": {"total": len(CHECKS), "pass": n_pass,
               "substantive": n_sub, "guard": n_guard},
    "all_pass": all_ok,
}

import os
outdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(outdir, "routeP_results.json"), "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)

# ----------------------------------------------------------------------------
# DRESSING_CLASSIFICATION_LEDGER.tsv
# ----------------------------------------------------------------------------
LEDGER = [
    ("element", "status", "exact_condition", "source_check", "notes"),
    ("Q (upper-right block)", "FORCED = 0",
     "top block-row of J v must vanish for all v in V",
     "TC_Q_block_zero_forced", "necessity by C/K probes; Route-B probe method"),
    ("P (base block)", "FORCED anti-diagonal antidiag(p,1/p) after pq=1 gauge",
     "-P H P^-1 = H <=> PH + HP = 0",
     "TC_P_antidiagonal_forced",
     "reproduces banked 07-20 F_b family in-class; p = free family parameter"
     " (SUPPLIED calibration)"),
    ("S (screen block)", "FORCED lower-triangular; involution splits branches",
     "(S K S^-1) lower-tri for all lower-tri K; S^2 = pq I",
     "TC_S_lower_triangular_forced; TC_involution_and_realness",
     "branch (a) S = +/-I; branch (b) S = [[s0,0],[s1,-s0]], s0=+-1, s1 free"
     " (SUPPLIED: the banked-open angular completion)"),
    ("R (base->screen mixing)", "FREE on a 2-dim branch space",
     "RP + SR = 0 (from J^2 scalar); class-preservation does not constrain R",
     "TC_R_unconstrained_and_blocks_exact; TC_R_solution_space_dim_2_per_branch",
     "SUPPLIED; R=0 contains the V5 member; R shifts the C fixed values (affine)"),
    ("J^2", "FORCED scalar, = pq I with pq > 0",
     "commutant of class = scalars; realness of lower-tri S",
     "S0_class_commutant_is_scalars; TC_involution_and_realness",
     "no real J^2 = -I branch; scale gauge -> pq = 1"),
    ("Lorentz membership", "EMPTY in the registered diagonal eta2 readout (A4"
     " readout stamp)",
     "P^T eta2 P = diag(q^2,-p^2) != eta2 over the reals",
     "TC_no_lorentz_dressing_exists",
     "EVERY compatible dressing is non-Lorentz IN THE REGISTERED DIAGONAL eta2"
     " READOUT (generalizes banked F fact); banked 07-20 caveat travels: under"
     " the ADDITIONAL null-coordinate choice of K as metric, every F_b is an"
     " exact O(1,1) reflection — the EMPTY verdict is readout-scoped"),
    ("eps_lambda", "DERIVED -1 (dressing-independent)",
     "tr(-J X J^-1) = -tr X for any invertible J",
     "TP3_trace_similarity_generic_J", "needs only P0 (canon fold) + P1 (L0)"),
    ("eps_kmod", "DERIVED -1 under P2 (chart-representability)",
     "diag(S K S^-1) = diag K for lower-tri S",
     "TP3_lambda_kmod_odd_family_uniform; TP3_chart_escape_witness_kmod",
     "chart-escape witness J_out = diag(F2,F2) shows P2 is load-bearing"),
    ("eps_k10", "CONSTRAINED (branch-split)",
     "branch (a): -1; branch (b): +1 with 2(s1/s0)k_mod shear",
     "TP3_k10_branch_split",
     "missing datum = screen/angular completion (07-20 MULTIPLE_COMPLETIONS)"),
    ("eps_C", "CONSTRAINED (signature forced 2 odd + 2 even)",
     "charpoly of C |-> -S C P is (x-1)^2(x+1)^2 in every branch",
     "TP3_C_signature_2odd_2even_forced; TP3_C_basis_p_dependent",
     "WHICH combinations odd = supplied (p, branch, R); odd space at S=+I is"
     " mu_i+ = p c_i0 + c_i1"),
    ("fixed locus branch (a)", "k00=k11=k10=0; 2 C-conditions (dim 2)",
     "J X + X J = 0",
     "TP4_fixed_locus_branch_a",
     "at F member = banked T5 swap cell (K=0, (c00,c10)=(-c01,-c11))"),
    ("fixed locus branch (b)", "k00=k11=0; k10 FREE; 2 C-conditions (dim 3)",
     "J X + X J = 0",
     "TP4_fixed_locus_branch_b", "k10 dial survives the fold on branch (b) only"),
    ("V5 swap F", "ADJUDICATED: family member (p=1, S=+I, R=0), premise NOT"
     " forced",
     "distinct compatible members exhibited",
     "TC_V5_adjudicated_inside_family",
     "its lambda/k_mod parities hold family-wide; its k10/C action is"
     " member-specific"),
    ("AMENDMENT 2026-07-29", "A1-A4 applied post-verifier",
     "see CORRECTION_LAYER.md + VERIFIER_REPORT.md",
     "A1_aFprime_vs_aF_distinction; ADOPTED_* (verifier-credited)",
     "A1: check-25 pairing prose corrected (a_F' = 0 criterion vs a_F = 0 value;"
     " landing = certificate-premise failure, UNCERTIFIED not refuted); A4:"
     " Lorentz row eta-readout-stamped, per-branch parameter counts, -k10 sign;"
     " A3: verifier mutation set + K4 leg + H-block lemma adopted as checks"),
]
with open(os.path.join(outdir, "DRESSING_CLASSIFICATION_LEDGER.tsv"), "w") as f:
    for row in LEDGER:
        f.write("\t".join(row) + "\n")

print("WROTE routeP_results.json, DRESSING_CLASSIFICATION_LEDGER.tsv")
sys.exit(0 if all_ok else 1)
