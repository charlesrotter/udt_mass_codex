# BLIND VERIFIER REPORT — P4 Route A Stage 1

Verifier: blind adversarial, same-session-spawned (**caveat: not a hosted external
model** — a fresh-context agent of the same session/harness, zero prior arc context,
framed to ADJUDICATE, not confirm). Date: 2026-07-29.
Script: `VERIFIER_INDEPENDENT_CHECK.py` (31/31, exit 0; own constructions — Kronecker
nullspace commutant, character-theoretic invariant ring, actual matrix exponential,
own solves, counterexample constructions).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS (4 amendments, listed exactly in §6)

The contract (PREREGISTRATION.md, sole file of commit 940c8fe, 00:09, all other
artifacts untracked and later-stamped — **contract-first VERIFIED**) is honored; the
core forced statements F-RA1 (covariance type), F-RA2 (slot conclusion), F-RA3, F-RA4
all SURVIVE independent re-derivation; but two universally-quantified sub-claims are
FALSE as written (exact counterexamples below) and infect the gate specs. They are
precision/quantifier errors (F-A6 class — exactly what this pass hunts), not
load-bearing collapses: each has a well-defined correct restatement under which the
forcing stands.

## 1. Rerun (Duty 1): PASS

`python3 derive_routeA_stage1.py` — exit 0, 34/34, twice; `routeA_stage1_results.json`
byte-identical to the banked copy (sha256 7c0fad83…a6a0) and across reruns; stdout
matches `DERIVATION_STDOUT.txt` byte-for-byte. Imports: json/sys/sympy only — no
floats, randomness, or network.

## 2. Independent re-derivation (Duty 2)

**F-RA1 core — CONFIRMED.** Own construction (stacked Kronecker operator
L^T⊗I − I⊗L over all six generators, 96×16): rank 15, nullspace = span{I} — the
so(1,3) commutant is scalars only. H = diag(−1,1) not scalar ⇒ no Lorentz-invariant
member; equivariant-family forcing stands. Tangent block form and transport law
independently recomputed and matched.

**K₄ factorization — BOTH directions tested; direction 2 TRUE, but the component
quantifier is FALSE (Amendment A1/A2).**
- Direction 1: all 11 listed generators (k10²; the six within-character-class C
  quadratics; the four mixed cubics) are K₄-invariant — confirmed against the matrix
  action recomputed from scratch, matching Route B T1(b) verbatim.
- Direction 2 (the hard one): the 11 DO generate the full invariant ring of
  polynomial functions of (k10, C). Proven two ways: (a) parity/character argument —
  invariance ⇔ e+p+q even AND e+r+s even (e = k10-exponent; p,q / r,s the two C
  character classes); e≥2 ⇒ divisible by k10²; e=1 ⇒ both class-sums odd ⇒ divisible
  by a mixed cubic; e=0 ⇒ product of within-class quadratics; (b) exhaustive check:
  all 127 invariant monomials of degree ≤ 6 factor through the 11
  (`V2_direction2_generation_to_degree6`).
- **COUNTEREXAMPLE to the stated quantifier** ("every component's dependence on
  (k10, C) must factor through the exact K₄-invariants … bare k10- or C-linear
  dependence is not chart-honest"): the one-form **ω = k10·dk10 = ½·d(k10²)** is
  exact and K₄-INVARIANT (component and dk10 flip together under R12/R13), hence
  perfectly well defined on the quotient — yet its R_k10 component is BARE
  k10-linear (`V3_ATTACK_*`). The correct forced condition is **character-matched
  RELATIVE invariance per component**: a component R_v must transform with the K₄
  character of its paired direction dv. Verbatim factor-through-invariants holds
  ONLY for components along K₄-invariant directions (δφ, base data, δλ, δk_mod,
  boundary data); R_k10 must be χ_a-relative (e.g. k10·invariant, or c_b·c_c·invariant),
  R_C components χ_b/χ_c-relative. As written, gate 2's FAIL condition and gate 4
  step 2 would WRONGLY FAIL the legitimate candidate d(k10²).

**F-RA2 — computations CONFIRMED; channel-class quantifier FALSE as worded
(Amendment A3); slot conclusion SURVIVES.** tr X_seat = 2λ, ∂/∂k_mod ≡ 0; det
e^{φX} = e^{2λφ} recomputed via the actual matrix exponential; any F(tr X) blind —
all confirmed. **Counterexample to "every trace/volume/density-built screen
functional"**: tr(X²) = 2 + 2λ² + 2k_mod² is trace-BUILT and pairs with k_mod
(∂ = 4k_mod ≠ 0) (`V4_ATTACK_*`). The proven class is: functionals of tr X (first
trace) and of det e^{φX}. The downstream forcing survives in exact form: a screen
pairing kernel with zero trace-free part has identically zero k_mod-pairing
(⟨r_tr·I₂, diag(−1,1)⟩ = 0), and d(tr X²)'s kernel 2K = 2λI₂ + 2k_mod·diag(−1,1)
pairs with k_mod precisely THROUGH its trace-free slot — so "determined branch
reachable only with the trace-free slot (and/or mixing slots)" stands.

**F-RA3 — CONFIRMED** by own solves: restricted critical point (0,0), full response
there (0,1) (normal residual exactly 1), full zero set {(0,−1/2)} disjoint from the
stratum.

**F-RA4 — CONFIRMED; no further forcing found.** Additivity, shift-as-left-
translation, anchor absorption recomputed. Verifier attempted a further pointwise
forcing from G01 and found none: the every-scalar-f composition witness blocks any
functional-form selection at the pointwise level. Near-null stamp is honest.

## 3. Prose falsifier hunts (Duty 3)

- **F-A1: CLEAN.** EH/Bach appear only as cited jet-order examples (POSED §2.2, R6,
  gate-5 step 1); CM0-C only as the recorded-exclusion example (§2.3). No gate is
  run; no candidate constructed or privileged; the pairing structures (P1/P2/P3) are
  enumerated with none adopted.
- **F-A2: CLEAN.** All 16 census rows carry both fork options with consequences
  (c_E const-vs-promoted; α active-vs-frozen; each modulus const-vs-field; boundary
  varied-vs-held; completion within-vs-over). No fork is decided in prose; POSED §1.1
  types the moduli factor per BOTH options.
- **F-A3: CLEAN.** Gate 3 stamps NONVARIATIONAL as a pass-classification, FAIL only
  on undeclared pairing/jet order; §2.3 keeps the nonvariational case fully in scope;
  nothing in the object's definition structurally privileges Helmholtz-exactness.
- **F-A6: TWO SLIPS FOUND** — the two false universal quantifiers above (F-RA1
  component clause; F-RA2 channel clause). All other forced statements carry correct
  scope stamps; the PW/WS/GC tallies (8/2/4 + R11 per-row) recount correctly.
- **F-A4: CLEAN.** K₄ actions match Route B T1(b) verbatim (signs, invariant seat);
  seat formulas, tangent block, scalar-only centralizer, E04 closed form, volume
  scaling all match the bank; J06/J10/J14 instantiations quote the joint TSV
  pass-conditions and named false-passes verbatim; Route C #78 cited only as the
  no-shortcut record.

## 4. TA4 classification audit (Duty 4, 5 rows sampled)

R4 (PW, seat-level): correct — slot-level pairing is pointwise-decidable; faithful to
J06 + Route B T4 (subject to A3's wording fix). R8 (PW jet-level): correct —
Helmholtz conditions are jet-level; formalized as gate property, faithful to L6.
R12 (PW definitional): correct; witness valid. R5 (WS): correct — same-solution
closure needs a solution; faithful to the three-part mass ruling. R9 (GC): correct —
periods need completion/cycle data. Nit (non-blocking): R9/gate-6's
"K₄-orbifold cycles" sub-condition is VACUOUS for closed one-forms — periods over
order-2 orbifold (torsion) classes vanish automatically (2·period = period over γ² = 0).

## 5. Clash-scan adequacy (Duty 5, 3 own constructions)

- The reported near-tension (trace-free slot vs 4D-volume-only P1) resolution is
  LEGITIMATE: volume-factor k_mod-blindness does not annihilate an R_k_mod density
  integrated against it; enumeration-not-adoption is the correct handling, not a
  paper-over.
- **Construction 1 — REAL UNSCANNED TENSION (Amendment A4):** the φ=0 mirror/seal
  interface (POSED §1.2; census row 16) anchors an absolute φ zero-point, while
  F-RA4/census row 6 forbid any component from depending on one ("smuggled anchor,
  F-A2 flag"). Mirror and shift do not commute (−(φ+s) ≠ −φ+s). Not a proven clash —
  boundary data are SUPPLIED structure and the c_E anchor can absorb the shift — but
  §3.2's scan omitted it; it must be recorded with its resolution.
- Construction 2 (K₄-torsion periods): vacuous condition, spec nit (above), no clash.
- Construction 3 (R4 slot vs G01 shift): no clash constructible — the slot pairing is
  s-independent and volume blindness survives shifts (`V8_clash3_*`).

## 6. REQUIRED AMENDMENTS (exact list)

- **A1.** Restate the K₄ clause of F-RA1 (EXACT_DERIVATION §1 forced box; POSED §2.1
  bullet 3; script FORCED statement + JSON; census rows 13–14 wording) as:
  components transform with the K₄ CHARACTER of their paired direction
  (character-matched relative invariance); verbatim factor-through-the-11-invariants
  holds exactly for components along K₄-invariant directions; bare-k10/C-linear
  dependence is illegitimate ONLY in those components. Counterexample on record:
  ω = k10·dk10 = ½d(k10²).
- **A2.** Fix SIX_GATE_SPECS gate 2 (FAIL clause) and gate 4 (step 2): replace
  "bare-k10/C-linear (non-K₄-honest) dependence → FAIL" with "character-mismatched
  component dependence → FAIL". As written they would fail legitimate candidates.
- **A3.** Narrow F-RA2's channel class (EXACT_DERIVATION §2 box; POSED R4 row; script
  FORCED statement) from "every trace/volume/density-built screen functional" to
  "every functional of tr X (first trace) and of the volume density det e^{φX}" —
  or state the exact slot form: a screen kernel with zero trace-free part has
  identically zero k_mod-pairing. Counter-channel on record: tr(X²) pairs (∂ = 4k_mod).
- **A4.** Add to POSED §3.2's clash scan: the φ=0-interface vs shift-equivariance
  tension, with its resolution (supplied boundary structure; anchor absorption)
  recorded; note the K₄-torsion-period vacuity at gate 6 / R9.

## 7. Outcome-claim adjudication

With A1–A4 applied, the claimed outcome stands: **OA1/OA2 MIXED** — F-RA1 (amended
form), F-RA2 (amended form), F-RA3 forced and nontrivial; F-RA4 near-null; tallies
8 PW / 2 WS / 4 GC correct; no OA3 (the one new tension found is resolvable and
resolution-recorded, not a requirement clash). No candidate, action, modulus value,
or physics is selected anywhere in the package. Not committed by the verifier.

## 8. AMENDMENT CLOSURE (same verifier, 2026-07-29)

Adjudicated adversarially (attack, not confirm), same-session-spawned blind verifier
(not a hosted external model).

### VERDICT: CLOSED

Per-item findings:

1. **Rerun: PASS.** `derive_routeA_stage1.py` → exit 0, **40/40** (34 original + 3
   `A6_*` + 3 `B5_*`), twice; `routeA_stage1_results.json` byte-identical across
   reruns (sha256 e56025cb…01f6); stdout byte-matches the banked
   `DERIVATION_STDOUT.txt`. Still json/sys/sympy only. The new check CODE was audited
   line-by-line, not trusted: `A6_counterexample_*` verifies ω = k10·dk10 is
   K₄-invariant as a one-form (component × direction-sign product invariant under all
   three nontrivial elements), exact, and NOT verbatim-invariant;
   `A6_character_matching_rule_*` tests the corrected rule with a GENERIC invariant
   multiplier (q1 + q2·k10² + q3·c00c11 + q4·k10c00c01) across all four character
   classes including both χ_a realizations (k10·inv and c_b·c_c·inv);
   `A6_character_mismatch_*` shows a generic χ_b component on the χ_a direction fails
   — mismatch, not bare-linearity, is the failure mode. `B5_*` embodies tr(X²) =
   2+2λ²+2k_mod² with ∂/∂k_mod = 4k_mod, the slot theorem ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0,
   and the routing decomposition (trace part contributes exactly 0; trace-free part
   carries the full 4k_mod) — all matching my V3/V4 constructions. The `dir_sign`
   helper is correct for every (variable, element) pair (pure sign-flip actions).
2. **A1: IMPLEMENTED CORRECTLY.** F-RA1 now states character-matched RELATIVE
   invariance per component (component character × direction character = trivial) in
   all four required places (EXACT_DERIVATION §1 box, POSED §2.1 bullet 3, census
   rows 13–14, script FORCED + JSON), with verbatim factoring restricted to
   K₄-invariant directions, my ω counterexample on record, and the generation
   direction correctly attributed as verifier-proven (cited to
   `VERIFIER_INDEPENDENT_CHECK.py` V2, not overclaimed as the package's own). The
   necessity direction of the rule (a well-defined one-form component MUST be
   character-matched) is supported in-script by the generic mismatch contrast and
   follows generally from isotypic decomposition under the sign action — logic
   re-verified, sound.
3. **A2: IMPLEMENTED CORRECTLY.** Gate 2 FAIL clause and gate 4 step 2 now fail on
   character-MISMATCH; both explicitly mark bare-k10-linear R_k10 (the d(k10²)
   shape) as LEGITIMATE. The specs would no longer misclassify the counterexample.
4. **A3: IMPLEMENTED CORRECTLY.** F-RA2 narrowed to functionals of tr X (first
   trace) and det e^{φX}; tr(X²) counter-channel on record; the slot theorem stated
   exactly as proven. The amended clause "any channel that pairs with k_mod does so
   precisely through its trace-free part" was attacked as possibly
   exemplified-as-forall: it is in fact FULLY GENERAL (tr(A·diag(−1,1)) kills the
   pure-trace part of ANY kernel A identically — the slot theorem's contrapositive),
   so no residual quantifier slip.
5. **A4: IMPLEMENTED CORRECTLY.** POSED §3.2 carries the φ=0 mirror-vs-shift tension
   with a TYPED resolution (supplied-structure/anchor-absorption routing — matches my
   V8 construction; explicitly "typed, not decided"; correctly NOT recorded as an
   OA3 clash). Gate 6 carries the torsion-vacuity scope note with the correct
   2·period = 0 argument and correctly keeps the live content (non-torsion cycles,
   step-3 holonomy).
6. **CORRECTION_LAYER did-NOT-change list: HOLDS.** Outcome class string unchanged in
   JSON; tallies 8 PW / 2 WS / 4 GC unchanged (recounted); no-OA3 unchanged; F-RA3
   and F-RA4 statements identical to pre-amendment (compared against my Duty-2
   record); census fork-typing intact (rows 13–14 still carry the const-vs-field
   fork); six gates, same sequence. AUDIT_REPORT represents my findings faithfully:
   31/31, contract-first-in-git, both quantifier catches with the exact
   counterexamples, the generation-direction proof credited, A1–A4 listed, the
   not-a-hosted-external-model caveat traveling.

No new defect found. The amended package remains F-A1/F-A2/F-A3/F-A4 clean; the two
F-A6 catches are cured with the counterexamples embodied as zero-residual checks.
Verdict stands: **PASS-WITH-REQUIRED-AMENDMENTS → amendments applied and verified →
CLOSED.** Not committed by the verifier.
