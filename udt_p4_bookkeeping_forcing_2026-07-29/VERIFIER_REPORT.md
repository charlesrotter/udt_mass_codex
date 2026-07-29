# BLIND ADVERSARIAL VERIFIER REPORT — udt_p4_bookkeeping_forcing_2026-07-29

Date: 2026-07-29. Verifier: blind adversarial pass, **same-session-spawned agent**
(zero package context at start; caveat: NOT a hosted external model — the honest
description is a fresh-context agent of the same assistant, adversarially framed).
Contract: `PREREGISTRATION.md` (verified committed ALONE at 0c84489 BEFORE any
derivation artifact; all six derivation artifacts untracked at verification time —
contract-first CONFIRMED in git). Independent script: `VERIFIER_INDEPENDENT_CHECK.py`
(this package; 20/20 own-construction checks, exit 0).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS (one required, one recommended — both
prose-only; no computed claim broken; OF3 stands)

The TF1 crux is PROVEN as claimed; the TF2 "no banked source decides the census"
completeness claim SURVIVED a directed hunt (including the four named candidate
omissions); no F-K1 merit-steering found; the massive-favoring legs were attacked
first and hardest and held.

## 1. Rerun (duty 1)

- `python3 derive_bookkeeping_forcing.py`: exit 0, 19/19. Split audited line-by-line:
  checks 2,3,5,6,8,9,10,11,14,16,17 = 11 substantive; 1,4,7,12,13,15,18,19 = 8 guards
  — the claimed 11+8 split is honest (no substantive-tagged tautologies found; every
  guard is genuinely citation/definitional).
- Two independent reruns byte-identical to each other AND to the packaged
  `DERIVATION_STDOUT.txt` / `bookkeeping_forcing_results.json`. Runtime < 1 s, single
  CPU process. Script inspected: exact SymPy only — no floats, no randomness, no
  network, no numeric solvers.

## 2. Independent re-derivation (duty 2; own constructions throughout)

**(a) TF1 constant fork — CONFIRMED, and the "more conditions" attack fails.**
Re-derived from POSED §1.4 read directly: the constant-fork moduli tangent block is
ℝ⁷ (δλ, δk_mod, δk10, δC ∈ ℝ⁴), one direction per modulus; any §1.5 pairing
restricted to it is a linear functional, so vanishing supplies codim ≤ 7 —
representation-free. §1.5 read closely for a pairing supplying MORE: P1/P2 give one
scalar per direction; P3 is a SUM (∫bulk + ∮walls + Σcorners), verified single-scalar
per constant direction (`V1_P3_constant_direction_single_scalar`) — wall blocks pair
with boundary-data directions, not extra moduli conditions. Strongest attack
mounted: demand vanishing over the WHOLE enumerated weight family simultaneously
(all a_M at once) — could moment-completeness recover pointwise? NO: my own 7-slot
odd-density witness kills every weight e^{a x²} at symbolic a while pointwise nonzero
on all slots (`V1_own_7slot_odd_witness_all_weights`,
`V1_all_weights_simultaneously_still_not_pointwise`) — and the banked discipline
(J03) declares ONE pairing anyway. Both package witnesses re-derived with different
densities; the H4-Helmholtz near-miss is correctly adjudicated (a G3 membership
condition on 𝓡's components, not an on-shell row).

**(b) TF1 field fork — leg CONFIRMED; Category-A stamp ADJUDICATED LEGITIMATE.**
Package leg reproduced exactly (∫2x²(1−x²)³ = 64/315) and re-derived with my own
interior-supported variation v = x(1−x²)⁴ against my own density x³
(`V2_own_field_direction_detects_pointwise`, 256/15015 > 0, nonneg-factorization at
symbolic weight). The localization step: the LEMMA (continuous g, ∫gv = 0 for all
interior-supported v ⟹ g ≡ 0) is genuine cited calculus — Category-A-legitimate,
same lane as the banked integral-positivity/Picard citations. The function-class
QUESTION (does the declared dual class contain interior-supported variations?) is
NOT smuggled: it is discharged on banked usage (Stage-3
`TC1_P3_interior_defect_wall_immune` verified verbatim in the Stage-3 record) AND
the residual dual-class freedom is explicitly ledgered in Limits (iii) (L7/S13
open; conclusion weakens to declared-class-dense on a narrower dual class). No
F-K2-adjacent smuggle.

**(c) F-K2 audit — CLEAN.** §TF1 read line-by-line: the load-bearing step is the
banked tangent-space dimension (§1.4 ℝ⁷ vs field variations), not an imported
fundamental lemma; the §1.3 discharge record is accurate; both directions are
witness-computed, not asserted.

**(d) TF2 completeness — the F-K1-critical duty. CLAIM SURVIVES; one upstream
wording finding (A2 below).** Each of S1–S9 re-checked against the banked records:

- **S1/S4 (E02 typing / registration grade):** census rows 11–14 fork (ii) wording
  verified VERBATIM ("a class extension beyond the banked footing, typed only");
  Route B T1(a) verified verbatim ("Two CONSTANT generators X, X′..."); Stage-2 BR-M
  row verified verbatim (TYPED ONLY / NOT-EXHAUSTED). The verdict label matches the
  banked text. FINDING (A2): the UPSTREAM 07-25 registration
  (`udt_founded_phi_complete_coframe_extension_audit_2026-07-25`) says "exactly
  seven POINTWISE extension parameters" — an at-a-point statement that decides
  NEITHER branch (an at-a-point parameter count neither forces cell-constancy nor
  x-dependence), so it does not refute S1 and does NOT force the field reading; but
  it is the one banked phrase a field-branch advocate could cite, and S1's basis
  should name and adjudicate it (recommended amendment).
- **S2 (cocycle under promotion):** re-derived INDEPENDENTLY and more strongly than
  the package: the E04 closed form re-solved from the ODE, the effective member C₃
  SOLVED from the composition equations (not verified against the package's), drift
  iff distinct members, two-sided law on the composite (`V3_*`); PLUS a genuinely
  CONTINUOUSLY x-dependent generator (C(t) = C₀ + C₁t, K = 0) whose transport was
  built from its Duhamel integral and shown to satisfy the two-sided law over
  concatenated segments exactly (`V4_two_sided_cocycle_under_promotion`) — the
  law is composition-structural, verdict PERMITS-BOTH confirmed beyond the
  package's own generic-block + piecewise legs.
- **S3 (parity lever):** jet-kill re-derived on a degree-5 jet; the
  −X/mirror-not-representable argument STRENGTHENED: verified every K₄ element
  FIXES the H block, so no residual gauge element maps X → −X (`V5_*`) — the
  mirror's moduli action is indeed outside the banked gauge. ε_m SUPPLIED status
  confirmed against Stage-3 TC3 ("parity assignments are SUPPLIED wall structure";
  canon instance ε_φ = −1 only) and CANON C-2026-07-04-1 (sector split only; no
  moduli parity derived; no banked registration of the swap as the seal dressing —
  grepped). Route-P-relevant observation (computed, not adopted,
  `V5_swap_dressing_candidate_computed`): IF the seal dressing were the banked
  non-Lorentz swap F, then −FXF⁻¹ IS in-class with DERIVED parities
  (λ, k_mod, k10 all odd; C → −C·F₂) — a concrete candidate input for Route P,
  correctly NOT banked (F non-Lorentz ⟹ adopting it is supplied structure).
- **S5/S7/S8/S9:** K₄ pointwise action recomputed on my own Function-valued
  generator (`V10`); generated-row census-slaving re-derived on a fully generic
  W(m)·L form (`V9_no_mjet_euler_is_partial`) and the check-17 wall-term identity
  re-derived on my own m²P density (`V9_mjet_wall_term_difference`); the k_mod = 0
  identity descent re-derived with my own densities and weight, confirming exactly
  ONE integrated dependency = the banked TC2 count (verified verbatim in Stage-3
  §2) (`V7`); the S9 pullback identity re-derived with my own density (`V8`).
- **MISSED-SOURCE HUNT (all four named candidates + gate specs):** (i) three-gap
  "carried as explicit moduli" language (MAP §2 / POSED §1.3) — instantiated
  per-fork upstream (ℝ⁷/K₄ OR sections into it); decides nothing. (ii) G08 row
  ("7 pointwise params") — same at-a-point adjudication as A2; decides nothing.
  (iii) anchored-Q shift-absorption × m(x) — COMPUTED (`V6`): the clock row of
  e^{sX} is (e^{−s},0,0,0) for a GENERIC class member (x-dependent entries
  included), so the c_E absorption is moduli-promotion-independent, and
  e^{sX(x)}e^{φX(x)} = e^{(φ+s)X(x)} pointwise — shift structure decides nothing
  (frame-level anchoring of an x-dependent generator is a typed obligation of the
  unbuilt Route-D registration, not a census forcing). (iv) R3
  completion-as-arguments — concerns 𝔠/boundary/transition data, not moduli row
  form; neutral. SIX_GATE_SPECS read: gate 2 pairs the same 7 moduli directions;
  nothing touches row form. **NO deciding source found. OF3's completeness claim
  stands.**

**(e) TF4 restatement — exact AS SCOPED; needs one explicit clause (A1).**
Slice-2b's own stamp verified verbatim ("the POINTWISE column is Charles's R2
branch read on that arena, labeled"); the INTEGRATED-column/constant-census and
POINTWISE-column/field-census identifications are exactly TF1's content and are
correct FOR THE BANKED (no-moduli-jet) RESPONSE ALPHABET. The package's own check
17 proves the two branch row-sets differ by wall/jet terms once moduli jets enter a
registered BR-M response — so a registered field extension could carry additional
row content and the Slice-2b massless computation would need re-derivation there.
§1.2 states the no-m-jet premise and Limits (iii)/(vi) carry adjacent caveats, but
the §4 sentence "Field-moduli census ⟹ ... massless under all four labeled mass
readings" does not itself name the no-moduli-jet conditioning. Because TF4 is the
stakes restatement and the ceiling forbids overstating EITHER branch, this clause
is required (A1).

## 3. Falsifier hunts (duty 3)

- **F-K1 (hunted FIRST, hardest at the massive-keeping legs): NOT FIRED.** The
  constant-favoring verdicts (S1/S4) are verbatim reads of banked text (verified
  against the census, Route B, and Stage-2 records myself); the SAME package
  computes every form-stability leg of the field branch AND the one lever (S3,
  ε_m = −1) that would cut AGAINST constants; the derivation's outcome (REDUCED/
  OPEN) is NOT the massive-favoring outcome (FORCED-INTEGRATED) despite the named
  temptation. The field branch's UNBUILT status is stated provenance-not-
  prohibition, two-sidedly, in both the derivation and the residual surface.
- **F-K3: policed; no unstamped claim found** in EXACT_DERIVATION, FORCING_LEDGER
  (stamps in header + per-row sectors), or the JSON (verdicts carry branch/scope
  language). RES-CNEQ0 consistently example-scoped; the TF4 massless statement is
  definiteness-scoped. (The A1 clause is a scoping addition, not a missing stamp of
  the F-K3 named classes.)
- **F-K2: not fired** (§2b/2c above). **F-K4: not fired** — no silent census
  adoption anywhere; `RESIDUAL_DECISION_SURFACE.md` audited for stealth
  recommendation among D/P/C: costs and two-sided asymmetries stated evenhandedly
  ("least construction BUT the choice IS load-bearing" vs "most construction AND
  forces massless there"); Route D's "looks feasible" is grounded in the computed
  form-stability legs and paired with "can legitimately END OPEN". **F-K5: no bank
  contradiction found** — every banked fact the package recomputes matched my own
  recomputation and the source records verbatim. **F-K6: none** (19/19, exit 0).

## 4. Contract compliance (duty 4)

TF1–TF5 all addressed (TF5 = the residual surface). FULL declared scope: all eight
prereg source families interrogated (S1–S9; S9 = R12 added beyond the load-bearing
four) — the "no scope-ladder reduction" claim is consistent. Ceiling respected: no
fork decided beyond derivation; no massive/massless preference expressed; outcome
class OF3 correctly assigned (not OF1/OF2/OF4). Note: `AUDIT_REPORT.md` (a prereg
deliverable) is not yet present — due at the prereg's step (5), after this pass;
not a violation at this stage.

## 5. Required and recommended amendments

- **A1 (REQUIRED, prose-only, EXACT_DERIVATION §4):** add to the field-census
  bullet the clause: "at the banked no-moduli-jet response alphabet (§1.2); a
  registered BR-M response could carry moduli-jet row content (check 17's wall
  term) and the massless statement would need re-derivation on that extension."
  Protects the stakes statement in BOTH directions; no script change (byte-identity
  preserved).
- **A2 (RECOMMENDED, FORCING_LEDGER S1 basis + EXACT_DERIVATION §2 S1 row):** cite
  and adjudicate the 07-25 registration phrase "exactly seven pointwise extension
  parameters" (and the MAP G08 echo "7 pointwise params"): an at-a-point parameter
  count that decides neither census branch — so the S1 constant-footing reading
  rests on Route B's constant-generator derivations and the census's own fork
  wording, with the upstream phrase named rather than left for a later reader to
  discover.

## 6. Data for the driver (compressed)

Rerun 19/19 exit 0, byte-identical ×2 and vs package; split 11+8 honest.
Independent script 20/20 (in-package, preserved). TF1 crux INDEPENDENTLY
CONFIRMED both forks (own witnesses; codim ≤ 7 representation-free; multi-weight
attack defeated; localization Category-A legitimate with the dual-class freedom
ledgered). TF2 completeness SURVIVES: S1–S9 all verified against source records
verbatim; four candidate omissions + gate specs checked — none decides; new
computed legs: continuous x-dependent cocycle (V4), swap-dressing parity candidate
for Route P (V5), shift-absorption neutrality (V6). TF4 identification exact as
scoped; A1 clause required. No F-K1/K2/K3/K4/K5/K6 firing. OF3 stands.

---

# AMENDMENT CLOSURE (same verifier, 2026-07-29, post-amendment pass)

## VERDICT: CLOSED

All five adjudication items attacked and confirmed; no new defect found; no
verdict moved by the amendments.

1. **Rerun:** 21/21, exit 0; two fresh reruns byte-identical to each other AND to
   the regenerated `DERIVATION_STDOUT.txt` / `bookkeeping_forcing_results.json`.
   Split re-audited from stdout tags: 13 substantive + 8 guards — the two adopted
   checks are correctly tagged substantive. JSON old-vs-new diff (my preserved
   pre-amendment rerun vs current): EXACTLY two check details changed
   (`TF2_E02_record_constant_generator_typing` += the A2 adjudication;
   `TF4_stakes_map_fact_restatement` += the A1 clause) and EXACTLY two checks
   added — no silent edit to any other check; summary fields changed only in
   counts. **Faithfulness of the adopted checks verified against my originals
   line-by-line:** check 18 (`ADOPTED_xdep_duhamel_two_sided_cocycle`) rebuilds my
   V4 construction exactly (C(t) = C0 + C1·t, K = 0, Duhamel transport, ODE
   zero-residual, two-sided law over concatenated segments, Q = I) with correct
   crediting; check 19 (`ADOPTED_swap_dressing_parity_candidate`) rebuilds my V5
   exactly (H-block fixed, K → −K, C → −C·F₂, F₂ᵀηF₂ ≠ η) with the conditional
   framing and NOT-banked-as-derivation stamp intact.
2. **A1 coverage:** grepped every artifact for "massless" and filtered for the
   clause. Installed at: EXACT_DERIVATION §4 (field-census bullet, in-sentence);
   the TF4 JSON/stdout detail; RESIDUAL_DECISION_SURFACE at BOTH exact locations
   (the §"exact residual freedom" echo and the Route-C cost sentence) AND the lay
   caveat (the "no knob-slope terms / a BUILT knob picture could add such terms"
   phrasing — a faithful lay rendering); AUDIT_REPORT TF4 (twice, incl. the
   sign-off list). Remaining un-claused "massless" hits are ONLY in the frozen
   PREREGISTRATION (correctly untouched — a contract may not be edited) and in
   meta-references to the clause itself. No un-claused massless CLAIM survives.
3. **A2:** installed in the S1 ledger row and the §2 S1 prose row; the
   adjudication text matches my finding exactly (at-a-point count; decides
   neither branch; S1 rests on Route B constant-generator derivations + census
   fork wording; the citable phrase named and disposed).
4. **Route-P entry:** faithful to V5 — explicitly conditional ("IF the premise
   held"), premise stamped UNESTABLISHED (F non-Lorentz; no banked registration
   of the swap as seal dressing, crediting the verifier grep), consequences
   stated without preference, F-K1/F-K4 noted. The sharpened Route-P target
   ("derive or refute the seal dressing itself") is a fair statement, not a tilt.
5. **CORRECTION_LAYER did-NOT-change list — verified by comparison:** OF3 (new
   stdout: outcome class OF3); TF1 both forks (checks 1-6 byte-identical per the
   JSON diff); S1-S9 verdicts (ledger verdict columns unchanged; A2 is
   basis-only); TF3 composite + stamps (check byte-identical); three-route
   no-recommendation surface (additions are the A1 clause + the conditioned
   Route-P input only); F-K records — ALL CONFIRMED. AUDIT_REPORT faithful to my
   findings: contract-first-in-git, 20/20 independent checks, the defeated
   whole-weight-family attack, the per-candidate missed-source disposal
   (three-gap language, G08 phrase, shift-absorption, R3, gate specs), the
   localization adjudication with the ledgered dual-class freedom, and A1/A2 —
   all present and accurately stated; the same-session/not-a-hosted-external-
   model caveat travels.

No new defect. The amendments are strictly clarifying/strengthening; OF3, the
TF1 crux, the S1-S9 verdicts, and the no-preference residual surface all stand
as originally verified. Nothing committed by the verifier.
