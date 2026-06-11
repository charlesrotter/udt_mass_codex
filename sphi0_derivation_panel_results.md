# S_phi0[Typed Nodes] Derivation Panel — Results

Status: working audit, not canonical. Created: 2026-06-11 (session of
2026-06-10/11). New files only; no existing record edited.

## Purpose

Tier-D rounds 1 and 2 (126/126, 740/740 misses) established that the six
lepton wall numbers require an OBJECT — the boundary functional
S_phi0[typed nodes] and its Hessian — not a vocabulary member. This push
attempted the native derivation. Process: three independent data-blind
derivation agents (routes A/B/C below), then two blind adversarial
verifiers over the panel's load-bearing claims. All agents were
forbidden from consulting lepton data or the wall numbers; each filed a
data-blind disclosure (incidental exposures in greps were declared and
discarded; the derived forms contain no adjustable constants, so the
claim is checkable).

Routes:
- A — DtN/Calderon: S_phi0 as the metric's own DtN quadratic form;
  two-sided Calderon projector construction.
- B — boundary measure / Gaussian reduction: invariant slot measures,
  sector weights from the gauged angular operator.
- C — symplectic gluing / Schur complement: exact two-boundary collar
  DtN, constraint elimination, depth bookkeeping.

Verifiers: V1 (nu-order, monopole licensing, M1 dressing bookkeeping,
shape-norm recount), V2 (independence theorem, Calderon projector, E1
three-way conflict, frame cancellation, depth arithmetic). Verifier runs
2026-06-10/11; scratch verification records in the agents' reports
(43+4 PASS/structural-only refutations V1; 14 PASS V2 numerics; panel
scripts 30 + 23 + 38 claims, 0 standing numerical failures anywhere).

## Headline

NO parameter-free coefficient was derived — C_E1 and C_M1 remain
underived. But the push produced (i) a first-class refutation that
relocates the warped branch's foundations, (ii) exact new boundary
machinery (verifier-confirmed), (iii) two derived between-rung objects
(quarter-rung eta/8 and half-rung eta/4), and (iv) a positive
localization of the missing object.

## Banked positives (verifier-confirmed mathematics)

1. S_phi0 IS the DtN quadratic form. The second variation of the C1
   action on the self-similar collar, restricted to boundary data, is
   exactly the (one- or two-sided) Dirichlet-to-Neumann form — by the
   Dirichlet principle (A) and Hamilton–Jacobi (C). Exact; no
   linearization anywhere in the chain.
2. Exact two-boundary collar DtN (C; V2 to 60 digits + independent ODE
   shooting): off-diagonal b_ell = W0/Delta in closed Bessel form;
   b_ell -> const * y_c^{(2-q)/2} = y_c^{5/6}; Lambda_cc ->
   (5/6) y_c^{5/6} (ell-independent leading order); Lambda_00 -> D(λ);
   exact Schur identity Lambda_00 - b^2/(Lambda_cc + k_c) = the
   Neumann-inner DtN at any y_c. The exponent law (2-q)/2 is q-general
   (checked at q = 0.4).
3. Two-sided Calderon projector (A; V2): C_core =
   (D_- + D_+)^{-1} [[D_+, 1],[D_- D_+, D_-]] — idempotent,
   complementary, fixes the core graph, annihilates the far graph. Its
   Dirichlet-fiber limit (D_+ -> inf) degenerates exactly to the banked
   Cauchy graph projector form, with lambda_g = D_-; the banked
   lambda_g = eta/2 identification is the intrinsic-branch CHOICE
   (section-381 fork remains open). The symmetric weld reproduces the
   eta/2 + eta/2 -> eta composition law in form. Fills the section-383
   gap algebraically only.
4. The exact f-variable rewrite (B; V1): per unit solid angle,
   e^{-2phi}(d phi)^2 sqrt(-g) = (1/4)[r^2 f_r^2 + |grad_Omega f|^2/f]
   exactly (f = e^{-2phi}; g_tt g_rr = -1). The second jet in u = δf on
   the collar is (1/4)∫[y^2 u'^2 + λ y^{1/3} u^2] dy with NO cross
   terms; its DtN is D_B(λ) = sqrt(λ) I_4(6 sqrt λ)/I_3(6 sqrt λ),
   Bessel order nu = 1/q = 3.
5. Monopole sector identity (A and B independently; V1 symbolic + 4/4
   two-sided shooting): the gauged S^2 Laplacian at flux n has lowest
   eigenvalue j(j+1) - (n/2)^2 at j = n/2: |n|=1 gives λ = 1/2 with
   degeneracy 2 (exactly the banked CP1/Hopf doublet — an unforced
   consistency hit); n=2 gives λ = 1 with degeneracy 3 (exactly the M2
   triplet). Pure geometry, not an SM import; USE is conditional on
   Pbundle |n|=1 plus a unit-charged node variable. Sector weights
   under the uniform-clock reading: M1 -> eta/8 (quarter-rung),
   M2 -> eta/4 (half-rung) — the first DERIVED objects of the
   between-rung size the round-2 miss called for.

## The first-class refutation (V1, claim 1)

THE BANKED nu = 5/2 WARPED DtN FAMILY IS NOT THE C1 SECOND JET IN ANY
VARIABLE. It is exactly the spatial Dirichlet energy probe (the
section-253 object; verified symbolically, with the banked D1 and B
reproduced to 12 digits from the probe form). The C1 second jet at the
self-similar background is PARAMETRIZATION-DEPENDENT, because the
background is off-shell for the scalar-only EOM:
- f-variables (u = δf): nu = 3;
- phi-variables (full metric response): effective bulk mass
  2q(1-q) y^{-2}, nu = sqrt(17) — the same Bessel order as the L0
  interface threshold family (same 2q(1-q) source; cross-link recorded,
  not independent evidence);
- fixed-metric hybrid: nu = sqrt(7).
The two jets differ by a BULK term (off-shell first-variation residue),
not a contact term — "just a boundary term" is refuted. The
fluctuation-variable choice is load-bearing. The corpus's canonical
chain (Pi_f at section 165; dS_b/dF at 254) supports f as the licensed
variable, but this is now a NAMED PREMISE (P_f-variable), not a fact.
Consequence: the frozen warped branch's gamma rides the spatial probe,
which was never derived as the C1 Hessian. The warped branch is not
thereby falsified — but its foundation is relocated from "the C1
action's own warped kernel" to "the spatial probe object," and any
future warped-branch derivation must either derive the probe natively
or rebuild on the licensed jet.

## Refutations within the panel (verifier rulings)

1. Typed-slot independence "theorem" (A, C): REFUTED AS STATED. The
   core-phi0 coupling b_ell vanishes only at the same rate as the core
   slot's own stiffness (b/Lambda_cc -> -0.02444 at ell=1, a nonzero
   constant); at the canonical endpoint the core slot is a FLAT
   direction, so "independence" there is vacuous. What survives
   (conditional, useful): the phi0-side dressing decouples from core
   data exactly. NEW NEGATIVE, positively localizing the missing
   object: the banked depth-5/7 bookkeeping's CORE-SIDE node weights
   receive ZERO support from the collar — their eta/2 actions must come
   from the core interior or a boundary measure not yet derived.
2. Route B's C_E1 = exp(eta) shape-norm recount: REFUTED as a
   derivation. It contradicts the banked per-node unit-norm primitive
   (Punit; the corpus's own norm-sensitivity table already tabulated
   and declined the norm^2 = 1/2 variant; section 209 banks the
   delta_ij/2 moment with "no branch correction by itself"), and is
   internally incoherent (corrects the exponent but not the
   multiplicity-3 traces). It survives only as a reminder that Punit +
   node independence are underived.
3. Mirror equipartition (C): not banked, not exact-by-canon (the C1
   density is not phi -> -phi invariant); interpretation-level.

## The coefficient situation after the panel

- C_E1: UNDERIVED. C_E1 = 1 is the frozen-model default reading (not a
  theorem); the strict status is route C's: no parameter-free number
  exists without the boundary measure / flat-direction normalization.
- C_M1: two conditional warped readings survive, NEITHER forced — both
  hit the banked calibration anchors exactly, so calibration cannot
  discriminate (the dressings coincide on the H1 triplet and differ by
  sqrt(λ/2) off it):
  - same-mode-ratio reading (A; the frozen-form-consistent extension):
    C_M1 = exp(eta [B(2) - B(1/2)]) = 1.011519893216,
    B(λ) = I_{7/2}(6 sqrt λ)/I_{5/2}(6 sqrt λ), B(1/2) = 0.486553780698;
  - eigenvalue-clock reading (B; weaker textual support):
    C_M1 = exp(eta [B(2) - B(1/2)/2]) = 1.025283774326.
  Intrinsic-branch readings: graph C_M1 = 1; operator (A and B
  convergent) C_M1 = exp(3 eta/4) = exp(1/24) = 1.042546905190.
  All inherit: the spatial-probe-vs-C1-jet condition, Pbundle + unit
  charge, and the unexamined premise that the M1 momentum-projection
  weight equals the H1 value 1/3.
- Structural prediction (C; V2 conditional, premise verified): the
  shared H1 frame block cancels exactly in C_E1/C_M1 regardless of
  branch — the ratio depends only on the per-side shape sectors.
- Depth arithmetic (3 + 2s = 5, 7; 6 -> 3 frame merge; per-cell
  exponents) survives elimination; node independence remains underived
  (P_depth stays diagnostic).
- M2: NOT suppressed by the measure/Hessian structure (K_M2 =
  (eta/4) I_3 > 0, no null direction). M2 exclusion rests entirely on
  Pbundle0 primitivity, unchanged.

## Sharpened named targets (ordered)

1. P_f-variable: derive natively WHICH fluctuation coordinate carries
   the licensed second jet (the canonical chain favors f; the
   parametrization dependence is an off-shell artifact — deriving the
   correct on-shell/constrained Hessian may collapse the fork).
2. The boundary measure / core-interior weight: the missing object is
   now LOCALIZED — core-side node weights get nothing from the collar;
   whatever supplies them (core interior, measure density mu, or a
   phi-angular coupling) is the coefficient object. (Charles's standing
   hunch — phi-angular interaction — sits exactly here.)
3. The clock fork (same-mode-ratio vs eigenvalue-clock) — derive the
   per-sector transfer action from the weld variational problem.
4. Warped-branch foundation: derive the spatial probe natively or
   rebuild gamma_warped on the licensed jet (nu = 3 family if
   P_f-variable holds: D_B(2) = 0.925083523113,
   B_C1 = I_4(6 sqrt 2)/I_3(6 sqrt 2) = 0.654132832357).

## Verifier record

- Verifier V1 (nu-order/monopole/bookkeeping/recount): blind
  adversarial pass 2026-06-10/11; independent symbolic + mpmath
  shooting; 43 PASS / 4 FAIL (all 4 = verifier's own harness artifacts,
  superseded; no surviving numerical failure against any route);
  refutations structural as recorded above.
- Verifier V2 (theorems/E1 conflict): blind adversarial pass
  2026-06-10/11; 60-digit Bessel + independent ODE cross-checks (1e-44
  agreement); 14/14 numerical sub-claims PASS; interpretation rulings
  as recorded above.
- Driver note: the panel-verifier cycle again caught over-claims before
  banking (independence "theorem", the exp(eta) recount, the contact-
  term claim) — the Self-Hardening culture held.

## Next step in this record's chain

Pre-registered evaluation of the surviving conditional coefficient
forms against the six wall numbers: tier_d_round3_contract.md (frozen
before evaluation), results in tier_d_round3_results.md.
