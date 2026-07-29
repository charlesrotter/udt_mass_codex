# Blind adversarial verifier report — udt_p4_routeP_seal_parity_2026-07-29

Verifier: blind verifier, same-session-spawned (zero package context at start; NOT a
hosted external different-model review — that caveat travels with this pass).
Date: 2026-07-29. Contract: `PREREGISTRATION.md`, confirmed committed at `faf9294`
(2026-07-29 19:02) BEFORE any derivation artifact (all derivation artifacts untracked
at verification time — contract-first VERIFIED in git).

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS

The classification, the parity theorems, the escape witness, the fixed loci, the V5
adjudication, and the family-consistency claims are all CONFIRMED by independent
re-derivation with my own constructions (`VERIFIER_INDEPENDENT_CHECK.py`, 41/41 after
fixing three bugs in MY OWN harness — commutant comparison target, and two
real-domain solve calls; the package was right in all three places). One consequence
leg (the TP4/check-25 anchored-pairing landing PROSE) mis-cites a banked statement in
a way that changes its meaning (a_F′ = 0 rendered as a_F = 0) and must be corrected
before banking. The computed content of that check is correct; the flaw is textual
but load-bearing for one map-fact claim.

## Duty 1 — RERUN

- `python3 derive_routeP_seal_parity.py`: exit 0; 34/34 (26 substantive + 8 guard).
- `routeP_results.json`, `DRESSING_CLASSIFICATION_LEDGER.tsv`: byte-identical on
  rerun (sha256 match); stdout byte-identical to `DERIVATION_STDOUT.txt`.
- Exact SymPy only: whole script read — no floats, no randomness, no numeric/evalf
  solves, no network/GPU; solve calls are exact. The `nonzero=True` symbols used in
  the no-Lorentz solve imply real in SymPy's assumption lattice, so the q² = −1
  emptiness check is sound (I re-verified with explicit `real=True`).
- Split audit: the 26 "substantive" checks are all genuinely computed booleans. Of
  the 8 "guards", 7 are hard-coded-True assembly/citation prose and 1
  (`TC_VJ_top_rows_zero`) is computed — the guard label is honest (EXACT_DERIVATION
  declares guards as citation/assembly bookkeeping); the computed one being labeled
  guard is conservative-direction mislabeling only.

## Duty 2 — INDEPENDENT RE-DERIVATION (own script, own routes)

`VERIFIER_INDEPENDENT_CHECK.py` — 41/41 PASS. Highlights:

- **Classification completeness (attacked):** re-derived necessity my own way — Q = 0
  from annihilation of the full generic C-block (linear solve, forced exactly);
  P antidiagonal by full generic-P solve of PH + HP = 0; S lower-triangular from the
  k10-coefficient −s01² (real-zero only at s01 = 0, whole system then vanishes); the
  image H-block is EXACTLY −PHP⁻¹ for any block-lower-triangular J (R cannot
  compensate — closes a compensation loophole the package used implicitly);
  commutant of the class = scalars (my route: symbolic-moduli coefficient
  extraction). Constructive attacks all fail as they must: off-block swap, screen-F₂,
  identity base, and the J² = −I route (P = antidiag(1,−1) squares to −I but no real
  lower-tri S does) — **no in-class involutive dressing outside the derived family
  was constructible**. Sufficiency verified on the MOST generic members (branch (b),
  symbolic p and s1, R generic in its solved 2-dim space; branch (a) with R ≠ 0):
  involutive, in-class, correct parities. Family classification CONFIRMED complete
  on its stated conditions (class-preservation + J² scalar + realness).
- **ε_λ dressing-independence:** tr(J·X·adj J) = det J·tr X re-verified on the
  16-symbol J; tr X = 2λ; no counter-J exists among invertible linear dressings —
  the theorem needs only P0+P1, as claimed. Transcription lemma L0: the mechanism
  (conjugation commutes with the anchored flow + re-anchoring forced by E(0) = I) is
  general; the package's exact witness is the K = 0 E04 member but the generic-block
  ODE identity it verifies does not depend on the closed form's K-content.
- **Escape witness:** J_out = diag(F₂,F₂) confirmed: exact involution, mirrors
  X = diag(−1,1,−k,k) (λ = 0, k_mod ≠ 0), and leaves the class on generic members
  (so it is genuinely outside the family — P2 is load-bearing for the k_mod kill,
  and the witness itself has λ = 0, consistent with the λ-kill being inescapable).
  (Minor: the check-22 prose says "(F₂ K adj F₂)[0,1] = k10"; it is −k10 — the
  computed check only uses ≠ 0, so no impact.)
- **C-signature:** charpoly (x−1)²(x+1)² re-derived in all four branches with
  symbolic p, s1, in the P⁻¹ form of the block law; linear-in-C part confirmed
  R-independent. Odd/even basis p-dependence confirmed.
- **Fixed loci:** branch (a) K = 0 + 2 C-conditions (dim 2, R-generic); F-member
  cell = (c00,c10) = (−c01,−c11) — matches the banked Route-B T5 swap cell verbatim
  (`T4_banked_swap_full_class_two_mixing_freedoms`). Branch (b) k10-free dim 3.
- **K₄ honesty:** all THREE nontrivial K₄ elements checked (package checked two):
  R23∘J in-family; R12∘J and R13∘J both square to diag(−1,−1,1,1) ≠ scalar —
  neither can flip the k10 branch. Package claim confirmed and completed.
- **Consequence loci:** λ = 0 = E07/det-one axis (Route B `T4_E07_axis_is_traceless
  _line` / `T4_vol4_blind_locus_is_traceless_line` — matches); k_mod = 0 = KMOD0
  stratum with the banked S8 one-dependency bookkeeping (forcing package — matches);
  λ = −1/2 triad-blind line NOT hit (0 ≠ −1/2, and Route B confirms λ = −1/2 never
  meets the E07 axis). a_F values at λ = 0: 2λ → 0, 1+2λ → 1 — arithmetic confirmed.
- **TP1 tag table spot-read:** CANON C-2026-06-10-2 ("mirrored across phi → −phi" —
  definitional wording, confirmed) and C-2026-07-04-1 (sector split σ_φ static /
  t→−t time-on; φ odd ⇒ Dirichlet + flux seal; ω OPEN — all as tabled). ε_φ = −1
  THEORY-cite and "f/bh parities SUPPLIED" match the Slice-2 record verbatim. The
  07-20 record confirmed: MULTIPLE_COMPLETIONS; F_b = [[0,b],[1/b,0]] full constant
  real family; raw swap = η-anti-isometry in the diagonal readout with no positive
  conformal-η solution; angular completion non-unique (+I/−I/axis continuum,
  selector not supplied); "smallest missing object" as quoted. The frame action is
  genuinely left open by the bank; the package's family is the banked F_b family
  transported in-class with the involution/realness cut added — "REFINED not
  contradicted" is accurate.

## Duty 3 — FALSIFIER HUNTS

- **F-P3 (scope stamps) — ONE FIRING, the required amendment (see below):** the
  check-25 / TP4 / results-json prose mis-scopes a banked citation. All OTHER
  claims carry full stamps (premise ladder P0/P1/P2 on every k_mod statement
  checked; branch/R/census stamps present; φ-dependent dressings typed out of
  scope; DECISION_SURFACE D1 correctly makes P2 the single load-bearing supplied
  premise of the cutting half and does NOT repeat the mis-citation).
- **F-P1 (steering, both directions):** the cutting legs carry their premises and
  the package computes the strongest attack on its own cut (escape witness) — no
  harmless-side underexploration found: I hunted for a banked source deriving OR
  refuting P2 and found none (J07 transition-data obligation is banked-open — Route
  B T3 "J07 open for all strata"; 07-20 derives no complete coframe action). The
  ONE drift found points in the CUTTING direction: the mis-citation (below) makes
  the λ = 0 landing sound tie-free ("divergence ABSENT at that weight") — stronger
  than banked. It must be corrected; with it corrected, no eulogy/drama language
  remains (ceiling respected).
- **F-P2 (V5 discipline):** clean — V5's F is derived to be the (p=1, S=+I, R=0)
  member, with an explicit distinct member (p=2) exhibited; premise NOT forced;
  nothing adopted.
- **F-P4 (census / Route D):** grep-clean — no Route-D result cited anywhere in the
  package (only the prereg's framing references, which predate); both census
  branches carried in every consequence statement.
- **F-P5 (bank contradiction):** none found — −X obstruction, V5 facts, E04 form,
  T5 swap cell, 07-20 family, K₄ actions, KMOD0/S8, E07 axis, λ = −1/2 line all
  re-checked against their banked sources and consistent.
- **F-P6:** no symbolic failure. BUT the EXACT_DERIVATION F-P6 bullet asserts
  "catch-proofs verified (wrong-parity, wrong-dressing, wrong-signature and
  screen-swap-in-class claims all FAIL the same machinery)" with NO catch-proof
  artifact in the package — an asserted verification not in evidence (amendment
  A3). My own mutations now supply the evidence: wrong-parity (k_mod even), wrong
  C-signature ((x−1)³(x+1)), k10-odd-on-branch-(b), and screen-swap-in-class all
  FAIL the machinery (`V3_catch_*`, `V2f_attack_*` — all caught).

## Duty 4 — CONTRACT COMPLIANCE

TP1–TP5 all addressed (TP5 = DECISION_SURFACE_UPDATE.md — a handle, no
recommendation, confirmed). Scope ladder unused — consistent (< 2 s wall; full
declared scope). Ceiling respected: no parity imposed (all derived/constrained/
supplied-stamped), no census adopted, no massive-branch survives/dies language —
EXCEPT insofar as amendment A1's mis-citation overstates one map fact. Outcome
class OP3 matches the declared outcome menu.

## REQUIRED AMENDMENTS (each exact)

- **A1 (the mis-citation; F-P3 firing).** The banked λ-row-absence criterion is
  **a_F′ = 0** (the P2 PAIRING, whose anchor weight is identically zero:
  forcing-package §4 "P2 side (a_F′ = 0): no λ-row either way"; Slice-2b line 252
  same), NOT the weight VALUE a_F = 0. On the P1-4D pairing at the forced
  background λ = 0: a_F(0) = 0 but a_F′(0) = 2 ≠ 0, so the λ-row form
  a_F′·∫p0·W_F·L̃ does NOT vanish by banked pairing-relativity there (what happens
  to it at an a_F = 0 background is UNDERIVED on banked footing — the quadratic
  atlas and the I_p sign-change certificate both presuppose a_F ≠ 0). Strike or
  correct, in a CORRECTION_LAYER (the stdout/json are frozen): (i) check-25 detail
  and `routeP_results.json` `aF_landing` "the a_F = 0 point has no lambda-row";
  (ii) EXACT_DERIVATION TP4 "…and 'no λ-row either way' (the banked
  massive/massless divergence is ABSENT at that weight)". The SURVIVING correct
  statements: the sign-change certificate's premise ("nonempty at every a_F ≠ 0
  background") FAILS at the λ = 0 landing (premise-failure, NOT a massless
  verdict — the massive-locus nonemptiness is simply UNCERTIFIED there); the
  P1-triad premise is INTACT (a_F = 1); and this package's own fold-quotient
  statement (no constant-branch λ-carrier under P0+P1+P2) stands independently.
- **A2 (minor, same leg).** EXACT_DERIVATION TP4 quotes the banked record as
  "P2 side (a_F = 0)" — restore the prime: "(a_F′ = 0)". (The forcing package
  itself uses a_F′.)
- **A3 (catch-proof claim).** Substantiate or reword the F-P6 "catch-proofs
  verified" sentence: no catch-proof artifact exists in the package. May now cite
  this report's mutation set (`VERIFIER_INDEPENDENT_CHECK.py` V3_catch_* /
  V2f_attack_*) or add the driver's own.
- **A4 (recommended, not blocking).** (i) Ledger row "Lorentz membership EMPTY"
  should carry the readout stamp ("in the registered diagonal η₂ readout") — the
  banked 07-20 record notes every F_b is an exact O(1,1) reflection under the
  ADDITIONAL null-coordinate choice of K as metric; the script detail has the
  η-scope, the ledger row does not. (ii) Check-22 prose sign slip
  ("= k10" → "= −k10"). (iii) TC_family_assembly "4 continuous parameters":
  branch (a) has 3 (p + 2 R); branch (b) has 4 — state per-branch.

## What was NOT verified

No external different-model review; no verification of the banked upstream results
themselves beyond consistency spot-reads (they carry their own verifier records);
the Category-A named steps (Picard uniqueness; real-square positivity) accepted as
named conventions per the contract's Category-A lane.

---

# AMENDMENT CLOSURE (same blind verifier, same-session-spawned, 2026-07-29)

## VERDICT: NEW-DEFECT (minor, memorial-ordinal prose only) — all A1–A4 closure
items otherwise CLOSED; closure completes on a one-line harmonization

## Duty 1 — rerun (CLOSED)

Exit 0; **41/41 = 33 substantive + 8 guard** (34 pre-amendment surviving + the new
`A1_aFprime_vs_aF_distinction` + 6 adopted legs — arithmetic checks: 26+1+6 = 33
substantive, guards unchanged at 8). JSON + TSV byte-identical on my rerun; stdout
identical to the shipped `DERIVATION_STDOUT.txt`. PREREGISTRATION.md byte-identical
to the frozen faf9294 copy (contract untouched by the amendment). The A1 check
computes exactly my distinction (a_F(0) = 0 with a_F′(0) = 2 ≠ 0 under P1-4D;
P2's a_F′ ≡ 0 as the criterion's holder; triad a_F′ = 2 with value 1) against the
banked pairing definitions. Each of the 6 adopted legs reproduces my computation
faithfully (H-block −PHP⁻¹ lemma on fully generic block J; the four mutation
catch-proofs — k_mod-even, wrong C-signature, k10-odd-on-(b), screen-swap-in-class
— all constructed as in my script and CAUGHT; R13∘J squares to diag(−1,−1,1,1),
completing K₄). Check-22 hardened to the exact equality (F₂ K adj F₂)[0,1] = −k10
(strictly stronger than the pre-amendment ≠ 0) — verified.

## Duty 2 — A1 installation (CLOSED)

The corrected statement (premise-failure ⇒ UNCERTIFIED (P1-4D) vs INTACT
(P1-triad), never ABSENT; no-λ-row criterion = a_F′ = 0, the P2 pairing; a_F = 0
background λ-row status UNDERIVED) is installed at all four occurrence sites:
check-25 detail, EXACT_DERIVATION TP4 bullet, JSON `aF_landing`, DECISION_SURFACE
D1 echo. Grep hunt: every surviving "ABSENT" / "no λ-row" / dropped-prime string
sits inside a quotation in the correction/memorial/verifier records only; no bare
"(a_F = 0): no λ-row" survives anywhere. The drift-direction memorial (cutting-side
inflation, first observed in the anti-massive direction) is present in the F-P1 and
F-P3 records — but see the defect below on its ordinal.

## Duty 3 — A2/A3/A4 (CLOSED)

A2: prime restored in the TP4 quote ("P2 side (a_F′ = 0)"). A3: the F-P6
catch-proof sentence now rides the adopted in-package mutation checks (evidence in
the 41, credited). A4: η-readout stamp on the ledger Lorentz row WITH the 07-20
null-coordinate O(1,1) caveat traveling; per-branch parameter counts (3 vs 4) in
the family verdict; K₄ leg completed with R13 (credited); −k10 sign fixed.

## Duty 4 — did-NOT-change list (CLOSED, verified by structured diff)

Machine diff of old vs new `routeP_results.json`: zero checks removed; exactly the
7 new checks added; exactly THREE surviving checks changed and each only as
mandated (TC_family_assembly per-branch counts; TP3_chart_escape_witness_kmod
hardened; TP4_aF_anchor_landing A1 prose — its computed booleans unchanged);
`outcome_class` (OP3), `premise_ladder`, `parity_verdict` (ε_λ dressing-independent;
P2-conditional ε_kmod; k10/C constrained), `dressing_classification` content
(family form/conditions/V5 — only the per-branch count string and readout stamp
appended), fixed loci, T5-cell recovery, and the constants-pinning consequence all
byte-stable or amended only by the declared stamps. AUDIT_REPORT is faithful to my
findings (41/41 own-script, loophole lemma credited, my three harness-reversals
recorded as package confirmations, A1–A4 dispositions, P0/P1/P2 limits stack, both
census branches carried).

## THE NEW DEFECT (exact claim + counter-computation)

**Claim (introduced by the amendment, three sites):** "the SIXTH catch of the named
scope class" (EXACT_DERIVATION F-P3; CORRECTION_LAYER §3; AUDIT_REPORT falsifier
record, which adds "every prior catch inflated toward the standing
(massive-keeping) picture").

**Counter-computation (corpus census):** this package's own FROZEN preregistration
(TP3, commit faf9294) declares an "EIGHTH-catch watch on the named scope class" —
i.e., seven priors at freeze time. The corpus supports that: Slice-2's
CORRECTION_LAYER calls its firing "the FOURTH instance of the NAMED scope class in
this arc" (implying three Stage-2-era priors), Slice-2b's verifier report banks
"the FIFTH catch", and Stage-3's CORRECTION_LAYER memorializes "both F-S3-class
catches" (a derivation self-catch AND a verifier catch = #6 and #7); the forcing
package fired none. On that census the A1 firing is the EIGHTH, not the sixth —
and "SIXTH" cannot be reconciled with the package's own prereg ordinal under ANY
counting convention (also noted: Route D's prereg in the same commit says
"SEVENTH-catch watch", so the corpus ordinals were already mutually inconsistent
pre-amendment). The universal "every prior catch inflated toward the
massive-keeping picture" is driver-asserted; I did not verify the direction of all
seven priors and it should be tagged as such or dropped.

**Required one-line fix:** harmonize the ordinal (state it as the EIGHTH on the
prereg's own census, or drop the number and say "a further catch of the named
scope class"), and soften/tag the all-priors-direction universal. Prose-only:
no computed, scoped, or physics claim rides on it. With that line fixed, the
closure is COMPLETE on all four duties.

Caveats travel: same-session-spawned blind verifier; not a hosted external
different-model review.
