# BLIND VERIFIER REPORT — P4 angular completion (step 2 of 3)

Verifier: blind adversarial verifier, **same-session-spawned** (zero package-context at
start; independent re-derivations throughout). Date: 2026-07-30. **Caveat: not a hosted
external model** — a fresh agent in the same session/repo; the same-session caveat
travels with this pass per the multi-round precedent. Contract: `PREREGISTRATION.md`,
verified committed at 9310173 BEFORE any derivation artifact (all six derivation files
untracked at verification time; contract-first CONFIRMED in git).

**VERDICT: PASS-WITH-REQUIRED-AMENDMENTS** (six, exact, below — one substantive
provenance/scope amendment (A1), one check-taxonomy amendment (A2), one premise-nesting
amendment (A3), three minor). No leg of the cutting chain is refuted; the harmless
escape is genuinely stated at equal precision; no falsifier fires in a voiding way.

---

## Duty 0 — rerun / reproducibility

- `derive_angular_completion.py` rerun x3 in a clean scratch dir: **exit 0 every time,
  31/31 PASS, stdout byte-identical across reruns AND byte-identical to the packaged
  `DERIVATION_STDOUT.txt`; regenerated JSON byte-identical to the packaged
  `angular_completion_results.json`.** Wall ~0.4 s, single CPU process.
- No floats / `evalf` / numeric solvers / randomness / GPU in the script (grepped).
- Substantive/guard split audited: 27 + 4 as claimed; the 4 guards
  (`TA1_banked_state_ledger`, `FA2/FA3/FA4_*`) are honestly labeled trivially-true
  bookkeeping rows. **However see A2: one "substantive" check (SB3b) is vacuous as
  coded** — the honest substantive count is 26 (or SB3b must be made a real check).
- Contract-first: 9310173 contains ONLY `PREREGISTRATION.md` (+ a LIVE.md line); all
  result artifacts are working-tree-only. CONFIRMED.

## Duty 1 — independent re-derivation (`VERIFIER_INDEPENDENT_CHECK.py`, preserved)

Written from scratch with different constructions (brute force over GL(2,Z) instead of
the signed-permutation ansatz; explicit torus fixed-point sets instead of linear
kernels; explicit pullback bookkeeping; `linsolve` for the underdetermined probes).
**All checks pass** (one SymPy 1.13 quirk found in MY OWN first draft, not in the
package: `sp.solve` on one underdetermined linear equation in two unknowns returns the
particular solution `{f0:0, f1:0}`; the package's `TA4_affine_parity_lemmas` is NOT
affected — its even-system involves only f1 and its odd-system is determined; verified
by hand).

Leg-by-leg (the cutting direction, F-A1(B)):

1. **{±I, ±D, ±W} classification — CONFIRMED complete, and its hinge located.** Brute
   force over integral involutions (entry bound 3) preserving the closer set gives
   exactly 6; the abstract argument (a GL(2,Z) involution preserving 4 primitive
   vectors on 2 lines is a signed permutation) is bound-independent, and the closers
   are a banked unimodular basis (gate-c `Tc1_cap_cycle_coords`, higher-isometry
   registration: "primitive cap cycles … a unimodular basis"). **No fourth in-family
   involution exists.** Hinge witness: `[[1,1],[0,-1]]` is a GL(2,Z) involution NOT
   preserving the set — the classification stands entirely on caps→caps (R-D), i.e.
   on R-A. Correctly disclosed. (See A5 for R-D's one scoped gap.)
2. **±D = the gate-(d) swap — CONFIRMED exactly.** Banked gate-(d) swap: "the lattice
   map V ↔ Y, K fixed", det −1, cap-line-FIXING (J v−=v−, J v+=−v+). Closer-basis
   D=diag(1,−1) maps V=c1+c2 ↦ c1−c2=Y: identical object. The Q=0 exclusion is sound:
   Route P's `TC_Q_block_zero_forced` forces the upper-right BASE→SCREEN block to zero
   (entries j02,j03,j12,j13 — verified against the Route P script), hence ι\*V can have
   no screen component; V ↦ ±Y has H-component Y∓… ≠ 0 ⟹ excluded. (Note the package's
   phrase "ruler→screen mixing" is the ruler-row specialization of the forced
   base→screen block — accurate.) The fold-vs-swap separation ("cleanly separated
   objects") is CORRECT and is genuinely new: the banked swap is cap-FIXING; the seal
   fold is cap-EXCHANGING — independent confirmation of the exclusion.
3. **ε_bh = +1 — AIRTIGHT, not convention-dependent.** ι\_\*(Y−fV) = ε_Y(Y−fV) verified
   by explicit pullback bookkeeping in all four cases (uses ε_f=ε_V ε_Y); bh=q_B(H,H)
   quadratic + P0 isometric identification ⟹ ε_bh=ε_Y²=+1. The only conventions used
   (A(V)=1 normalization, R-E) are banked. Also re-derived: ε_A=ε_V is FORCED (A is the
   unique radial-free connection form with A(V)=1 annihilating the horizontal
   distribution; an isometry with ι\_\*V=ε_V V preserves that characterization), so the
   ι\*A=ε_A·A step is derived, not assumed.
4. **Cap-value dichotomy — CONFIRMED, with one closable gap (A4).** Two-cap side: f_cap
   opposite (banked `Tc1_fcap_opposite`) + end-exchange ⟹ ε_f=−1 ⟹ only ±W; ±I give
   +1=−1: exact. Same-closer side as computed assumes f_c ≠ 0 (code comment only). Two
   independent closures exist: (i) banked `Tc1_fcap_registered` gives f_cap=±1 EXACTLY
   at genuine caps, so f_c≠0 is banked; (ii) the cap-CYCLE argument (the fold exchanges
   the ends, so cap-1's closer must map to cap-2's closer) reproduces the whole
   dichotomy with no f_c condition at all: same-closer ⟹ M fixes the closer line ⟹
   M=±I; opposite-closer ⟹ M exchanges the lines ⟹ M=±W. Cite one of these (A4).
5. **Crease selection — CONFIRMED, and R-C's grounding checked against CANON.**
   Explicit torus fixed-point sets (not just kernels): (+,+)=T² (dim 2), mixed = 
   circles (dim 1), (−,−)=4 points (dim 0); radial always flipped ⟹ spatial fixed-set
   dims 2/1/1/0; **codim-1 crease ⟺ M=I, unique**; det(dι)=(−1)^codim per case.
   CANON check: C-2026-07-04-1 verbatim says "Its **fixed surface** is φ=0 = r_s, a
   **spatial crease**" — the SURFACE/codim-1 wording is canon's own; "pointwise" is
   NOT in canon — R-C's typing as a READING with the setwise alternative carried is
   exactly right and is stamped where used. The realized screen block diag(−1,+1) =
   branch (b), s1=0, det=−1 basis-invariant; s1=0 basis-robust (−sin2θ off-diagonal);
   R=0 derivation under R-A sound (an isometry preserving the Killing span preserves
   its orthogonal complement ⟹ block-diagonal dι ⟹ Q=0 AND R=0).
6. **E0-collapse — CONFIRMED against the banked gradient-seat record.** Banked E0 =
   L̃_fh = (g_f f1² + 2g_x f1 h1 + g_h h1²)/2 — pure quadratic in the slopes, no
   linear/constant terms (verbatim from `derive_gradient_seat.py`). Banked condition
   (a) verbatim: "nonempty iff the SUPPLIED f/bh wall data leave an affine slope free —
   either definite supplied parity (odd or even, both walls, both fields) collapses E0
   to 0." Banked wall structure: cell x∈[−ℓ,ℓ], BOTH walls mirror/crease loci
   ("mirrored cell … continuity to the crease"), and the banked lemma is two-wall
   ("odd about both walls killed entirely; even about both walls kills its slope") —
   so the odd-parity (±W) outcomes inherit the two-wall kill legitimately (my one-wall
   probe shows odd-about-ONE-wall would NOT kill the slope — the two-wall structure is
   load-bearing and is banked, not introduced here). The gradient-seat record itself
   pre-anticipated exactly this consumption: "(i) empty the massive landing class
   (definite f/bh parities both walls)". AM-1/AM-2/p0≡0/P1-4D stamps inherited in §4 +
   §6(v). **The collapse claim is sound: in every realized outcome both parities are
   definite ⟹ f1=h1=0 ⟹ E0=0, conditional on R-A** (+ the class's own banked stamps).
7. **Three-way tension — RE-DERIVED and SHARPENED (see A1).** Two-cap c=1 members'
   in-family folds = {±W} only (leg 4); ±W fixed sets are codim-2 (leg 5) ⟹ no
   codim-1-crease in-family fold on two-cap members: CONFIRMED. Sharpening: since the
   banked complete members ARE the two-cap S³ class (see A1), the tension is stronger
   than "three symmetric legs" — under R-A + R-C-pointwise NO banked complete member
   realizes the canon fold at all.
8. **ε_k10 = +1 reversal — CONFIRMED against Route P's banked verdict structure.**
   Route P banked: "k10~ = −k10 on branch (a): ODD; k10~ = +k10 + 2(s1/s0)k_mod on
   branch (b)" and "k10 constant: killed on branch-(a) completions only (supplied
   datum decides)". I re-derived the shear term symbolically: K̃[1,0] = k10 +
   2(s1/s0)k_mod exactly — so ε_k10=+1 REQUIRES s1=0, which is exactly what the
   realized completion pins. The "reversal" phrasing is accurate (Route P tabled the
   branch-(a) kill as one scenario; the realized completion lands on the other). The
   C-law caveat checked: the package's C̃=−SCP⁻¹ is the R=0 reduction of Route P's
   full banked law C̃=−(RH+SC)P⁻¹+SKS⁻¹RP⁻¹ — legitimate BECAUSE R=0 is derived under
   R-A (and Route P's own signature check used the same reduction). 2-even+2-odd with
   the (1,±p) eigenbasis re-derived independently. E07 k↦−k and the E08 ruler-sourced
   image re-derived; silence honest.

## Duty 1 — the harmless direction (F-A1(A))

- **¬R-A stated at equal precision: YES.** The ¬R-A row of every table gives exact
  content (branch-open, SUPPLIED-free, calibration open = the 07-20 remainder,
  sharpened to one named premise); neither leg is promoted; the DECISION_SURFACE
  presents both with symmetric weight.
- **Is R-A really typed-not-derivable? CONFIRMED by bank hunt.** Route P's own verifier
  recorded "I hunted for a banked source deriving OR refuting P2 and found none"; the
  07-20 record's smallest-missing-object ("source-authorized physical quadratic
  readout/slot map plus a complete normal-angular-time-on coframe lift") is verbatim
  the datum that would settle R-A; the 07-23 "does not descend to real geometry"
  transcripts concern different objects and neither derive nor refute R-A; the 07-28
  packages derive only the c=1 plane-swap (a DIFFERENT involution, excluded from the
  fold family here) and the profile-conditional cap-swapping reflection σ (which
  becomes automatic on a mirror-doubled cell). Nothing in the bank derives or refutes
  R-A. Canon P0 does NOT already give R-A: the canon fold fixes only the (φ,r) action;
  its angular/screen realization on the REGISTERED arena is exactly the open lift.
- **HOWEVER — a hidden implication exists and must be stated (A3): R-A ⟹ P2.** The
  derived J_real is an in-chart, in-family member (SB7b), i.e. under R-A the fold IS
  chart-representable member-to-member — Route P's P2 holds. So R-A is strictly
  STRONGER than P2 on the banked footing (P2 does not imply R-A; ¬P2 ⟹ ¬R-A, and
  Route P's chart-escape witness is simultaneously a ¬R-A escape witness). The record
  calls R-A "the P2-analog / exact geometric sibling", which reads as a parallel
  independent premise; the nesting changes the decision-surface bookkeeping (granting
  R-A discharges P2's conditionality on ε_kmod; refuting P2 refutes R-A). Not a
  refutation — the results are all consistent under the nesting — but it is a
  decision-surface fact Charles needs.

## Duty 2 — falsifier hunts

- **F-A3 (FIRST — TENTH-catch watch): ONE catch, = A1 below.** The consequence claims
  riding the "Realized, canon codim-1 crease" outcome (branch-(b) selection, the
  ε_k10=+1 reversal, the explicit p-basis D3 calibration) carry the stamp "same-closer
  class only" — but that class's PROVENANCE is untagged, and it is not banked (grep:
  "same-closer" appears nowhere in the repo outside this package). Worse, it is
  outside the registered arena: the banked two-cap completion requires the two cap
  closers to be a UNIMODULAR pair (det ±1 → S³); a same-closer doubling caps the same
  primitive cycle at both ends (det(w,w)=0 → an S²×S¹-type toric completion, not S³,
  while the arena is registered on R_t×S³). Verified symbolically. All other stamps
  (premise ladder, census/pairing branches, K₄, η-caveat, p-free, AM-1/AM-2/p0≡0
  inheritance) are present and correct in the exact record; the lay DECISION_SURFACE
  is lighter but points to the exact record.
- **F-A1: does not fire.** Both directions at equal precision (above); the cutting
  chain's every link re-derived as forced from cited banked structure; no step found
  that was chosen for the outcome it favors.
- **F-A2: does not fire.** S-E/S-F verdicts are SILENT and stay silent (re-checked:
  E07/E08 maps and the slot table genuinely discriminate nothing); ¬R-A yields no
  selector anywhere; no source silence converted.
- **F-A4: does not fire.** Per-class / per-census-branch / per-pairing statements
  throughout; no step-(3) anticipation; the stop-clause explicitly reserves the call.
- **F-A5: one item, = A1.** Everything else recovered exactly against the banks
  (Route P family/laws/K₄/k10/C, gate-(c) f_cap facts, gate-(d) swap form, gradient
  seat lemma+E0+stamps, 07-20 remainder wording, CANON crease wording). R-B's claim
  that BOTH classes are "banked completion classes" is the one bank-fidelity defect.
- **F-A6: does not fire** (duty 0), modulo the A2 taxonomy correction.
- **Disclosed in-development bug fixes checked at their final resting places:** the
  sign fix (A4-type k10 shear) — final law re-derived independently, correct; the
  conjugation-vs-composition fix (K₄/R23 leg) — final `SB8b` recomputed and matches
  Route P's banked honesty operation (R23∘J = the s0-flip member; R12∘J, R13∘J
  non-involutive per Route P's adopted leg). Both sound in the final record.

## Duty 3 — contract compliance

- TA-1..TA-5 all addressed (TA-1 §1 ledger; TA-2 §2 + `SELECTOR_LEDGER.tsv`; TA-3 §3
  full table; TA-4 §4 map facts; TA-5 = `DECISION_SURFACE_UPDATE.md`).
- Stop-clause assessment: honest, reasons both ways, decision left to Charles.
  CONTINUE-WITH-FLAG is a fair reading; the FLAG (everything hangs on R-A + R-C +
  the tension) is the right flag — and A1 strengthens the case for the flag.
- Ceiling respected: no selector imposed (conditional throughout), no census/pairing
  adopted, no massive-class verdict language beyond computed map facts.
- Scope: full declared scope (S-A..S-F), no ladder reduction, well under budget.
- Deliverables: `AUDIT_REPORT.md` (named in contract §2) not yet present — owed
  before commit per §5 (A6).

## REQUIRED AMENDMENTS (exact)

- **A1 (substantive — provenance/scope of the same-closer class).** Retag R-B: the
  "same-closer doubling" class is PACKAGE-INTRODUCED, not banked (no banked source
  defines it), and lies OUTSIDE the registered R_t×S³ arena (same-cycle caps ⟹
  det(w,w)=0 ⟹ non-unimodular ⟹ S²×S¹-type completion; the banked complete class IS
  the two-cap c=1 S³ class). Consequences to restate: (i) the "Realized, canon
  codim-1 crease" outcome (branch-(b) selection, ε_k10=+1 reversal, explicit D3
  basis) currently has NO banked witness domain — it is conditional on R-A + R-C +
  an UNREGISTERED completion class; (ii) the three-way tension sharpens to: under
  R-A + R-C-pointwise, NO banked complete member realizes the canon fold — the
  escape routes are ¬R-A, the setwise crease reading (→ ±W, parities still definite),
  or registering a new completion class. The E0-collapse consequence is UNAFFECTED
  (it fires in every realized outcome, both classes).
- **A2 (check taxonomy).** `SB3b_curvature_pullback_consistency` is vacuous as coded:
  lhs and rhs are the same expression by construction (the two (−1) factors cancel);
  it passes for ANY parity values (verified with ε=7,3). The underlying claim is true
  for structural reasons (pullback commutes with d), but the check carries no
  computational load: relabel it [guard]/citation (count → 26 substantive + 5 guards)
  or implement a genuine two-sided computation.
- **A3 (premise nesting).** State R-A ⟹ P2 (via the derived in-chart J_real) in the
  premise ledger and decision surface: R-A is strictly stronger than P2, not a
  sibling; granting R-A discharges P2's conditionality (ε_kmod=−1 becomes
  R-A-unconditional); ¬P2 ⟹ ¬R-A; Route P's chart-escape witness doubles as the
  ¬R-A escape witness.
- **A4 (minor).** Close the same-closer dichotomy's f_c≠0 assumption: cite banked
  `Tc1_fcap_registered` (f_cap=±1 exactly at genuine caps), or replace with the
  f-free cap-CYCLE argument (closer-of-cap-1 must map to closer-of-cap-2), which
  yields the dichotomy with no condition.
- **A5 (minor).** Scope R-D's "canonical torus" leg: the bank leaves
  higher-isometry-members-not-preserving-the-registered-Hopf-bundle OPEN (S08
  stratum, higher-isometry package); R-D's derivation holds for members whose
  isometry identity component is the registered R_t×T² (the banked bounded family,
  incl. the swap-augmented c=1 stratum); note the S08 corner as banked-OPEN.
- **A6 (deliverable).** Add `AUDIT_REPORT.md` before commit per contract §2/§5.

## Verdict

**PASS-WITH-REQUIRED-AMENDMENTS.** The cutting chain is sound leg-by-leg (all eight
legs independently re-derived, zero residual); the classification is complete; ε_bh=+1
is airtight; the E0-collapse is correctly computed and correctly conditioned
(R-A-conditional, all realized outcomes, banked stamps inherited); the harmless escape
is honest and precisely stated; R-A's typed-not-derived status is confirmed by bank
hunt. The required amendments do not overturn any computation: A1 rescopes WHERE the
canon-crease (M=I) outcome can live (nowhere banked — which strengthens, not weakens,
the package's own tension finding and the flag to Charles); A2/A3 correct the check
count and the premise bookkeeping; A4/A5/A6 are hygiene. After amendment, the OA2
outcome class stands, with the OA1 core's conditionality set enlarged by one member:
{R-A, R-C-pointwise, an unregistered same-closer completion class}.

Independent script preserved as `VERIFIER_INDEPENDENT_CHECK.py` (exit 0, all pass;
includes the hinge witness, the vacuity demonstration inputs, and the one-wall/
two-wall probes). Not committed (per instruction).

---

# AMENDMENT CLOSURE (same verifier, 2026-07-30 — adjudicated as an attack, not a confirmation)

**CLOSURE VERDICT: CLOSED.** All six amendments implemented faithfully and
check-backed; no new defect found; no pre-amendment computed claim changed (verified
by byte-level comparison, not by trusting the did-NOT-change list). Same
same-session-spawned / not-a-hosted-external-model caveat travels.

## Closure evidence per item

- **Rerun:** exit 0, **34/34 = 30 substantive + 4 guards**, deterministic ×2 in a
  clean scratch dir; regenerated stdout AND JSON byte-identical to the packaged
  files; full sha256s recomputed and MATCH the values claimed in
  `CORRECTION_LAYER.md` §3.6 / `EXACT_DERIVATION.md` header (stdout 382b1098…4b8ad,
  JSON bf21ee72…dc6e3). JSON `counts` = {substantive: 30, guards: 4,
  verifier_credited: 3, failures: 0}; `checks_verifier_credited` lists exactly
  AM1/AM4/AM3.
- **The three credited checks reproduce my computations faithfully:**
  `AM1_same_closer_unimodularity_failure` = det(w,w)=0 for any same-cycle pair vs
  det(c1,c2)=1 for the banked closers — exactly my demonstration;
  `AM3_RA_implies_P2_nesting` = both realized J_real verified as in-chart family
  members (branch-set membership; R=0 solves RP+SR=0; J_real²=I) — exactly the step
  my nesting derivation rests on, and it covers BOTH realized branches (so the
  nesting holds on the setwise ±W leg too); `AM4_cap_cycle_dichotomy_f_free` =
  closer-LINE exchange/fix under the four in-family actions (±W exchange, ±I fix) —
  exactly my f-free cap-cycle argument, correctly at the line (mod-sign) level.
- **A2 (SB3b) — now GENUINE, mutation-tested:** Route 1 (d/dx of the pulled-back
  υ-coefficient, ε_Y f(−x)) and Route 2 ((−1)·ε_Y·f′(x)|_{x→−x}) are independent
  constructions with f generic and ε_f NOT substituted. I mutated it two ways:
  flipping the ι\*dx sign (Route 2 → +1) FAILS; corrupting the cycle parity in one
  route only (ε_V for ε_Y) FAILS in the mixed cases. The check now has real failure
  modes for exactly the bookkeeping it certifies; as-coded it passes. Substantive
  label now earned.
- **A1 at every named site — verified present:** premise-ledger R-B retag
  (PACKAGE-INTRODUCED / UNREGISTERED / outside R_t×S³, AM1 cited);
  `EXACT_DERIVATION` §2 step-4 + dichotomy paragraph + §3 canon-crease row (three
  separate stamps: outcome, ε_k10 cell, D3-basis cell) + constants-census paragraph
  + §6(iv); `SELECTOR_LEDGER` S-B row (both columns) + AMENDMENT row;
  `DECISION_SURFACE` header, summary paragraph, surprise 2, census-fork bullets,
  stop clause; JSON `outcome_class`, S-B verdict, canon-crease parity row,
  `amendment`, and the first-class `sharpened_tension` key. The sharpened tension
  appears in the required jointly-unsatisfiable form with the three escape routes
  (¬R-A / setwise crease / register a new class) at every site that states it. The
  E0-collapse UNAFFECTED status carries my confirmation (quoted verbatim in
  `EXACT_DERIVATION` §4) and is stated both-classes everywhere.
- **A3 at every decision-surface site — verified present:** ledger R-A row,
  `EXACT_DERIVATION` §4 Route-P bullet + §6(i), `SELECTOR_LEDGER` S-B row,
  `DECISION_SURFACE` summary + stop clause (premise-count reduction), JSON S-B
  verdict, `AUDIT_REPORT` — each carries the full chain (R-A ⟹ P2, strictly
  stronger, ¬P2 ⟹ ¬R-A, ε_kmod discharge, the chart-escape witness doubling).
- **A4:** SB5's note now closes the f_c gap BOTH ways (AM4 f-free argument primary;
  banked `Tc1_fcap_registered` cited as the independent alternative). **A5:** the
  R-D/S08 scope stamp is in the ledger row, `FA3_stamps`, `SELECTOR_LEDGER`,
  `EXACT_DERIVATION` §6(vii), `AUDIT_REPORT` limit 4. **A6:** `AUDIT_REPORT.md`
  present.
- **Did-NOT-change list — verified by COMPARISON, not assertion:** I diffed the
  pre-amendment stdout (preserved from my first pass) against the post-amendment
  stdout. The ONLY changes are: SB3b's note (A2), SB5's note (A1/A4 stamps), the
  three inserted credited checks, the three guard notes, and the summary line. All
  27 original substantive PASS lines — the SB1–SB8 chain, TA3 parity values, TA4
  E0-collapse, ε_bh, fold≠swap, the S0 recomputes — are byte-identical. The ¬R-A
  rows and the stop-clause direction (CONTINUE-WITH-FLAG, sharpened) are preserved
  as claimed.
- **AUDIT_REPORT fidelity:** all eight legs recorded; both discoveries credited
  (A3 nesting; A1 principal catch); the TENTH-catch ordinal with its BOTH-WAYS
  direction memorialized; A1–A6 dispositions accurate; the SymPy-quirk note carried
  (correctly attributed to my own first draft, package unaffected); my quotes
  rendered accurately; the same-verifier-closure-owed line present (this section
  discharges it).

## Residual notes (cosmetic, NON-BLOCKING — no amendment required)

1. Wall-time claims ("~10 s") overstate: measured ~0.4 s on this machine (warm
   SymPy). Harmless either way (both far under budget).
2. `DECISION_SURFACE_UPDATE.md` field-census bullet says "P2 unchanged" meaning the
   PAIRING branch P2 — a naming collision with Route P's premise P2 now that A3 is
   installed in the same document; `AUDIT_REPORT.md` already disambiguates ("P2
   pairing unchanged"). Suggest the same word there if the file is touched again;
   not required.

**CLOSED.** The package is, in this verifier's judgment, ready for the driver's
four-check and Charles's desk, with the standing caveats: same-session verifier (not
a hosted external model), and everything selective conditional on R-A (typed) + R-C
(reading) + [A1] the unregistered-class scope on the canon-crease landing.
