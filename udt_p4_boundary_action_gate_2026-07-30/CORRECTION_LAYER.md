# CORRECTION LAYER — P4 boundary-action gate (amendments AM-V1 + AM-V2 + minor notes, per VERIFIER_REPORT.md)

Date: 2026-07-30. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`; two
REQUIRED amendments AM-V1, AM-V2 + minor notes — all implemented). **No pre-amendment
COMPUTED claim was broken** (the verifier re-derived every load-bearing leg
independently — `VERIFIER_INDEPENDENT_CHECK.py`, 31 checks, exit 0, all pass, on its
own layout/IBP/constructions): both required amendments are **phrasing-level
overclaim cuts** — notably, BOTH overclaims ran in the EXCITING direction (a
premise-reduction claim on the banked forcing theorem; a global-uniqueness reading of
a germ-local fact) and the blind pass caught both. Verdict **OW2 stands** unchanged:
a FAMILY with exact wall-moduli; no candidate emptied, none unique-selected; B has no
candidate-selecting content at N=2 — the discriminator is the discrete POSTURE.

## 1. Original claims (as they stood pre-amendment)

- **AM-V1 (the cousin-premise conflation):** `EXACT_DERIVATION.md` TW5 bullet (iii)
  stated "At the crease the conditional-fold premise 'no seam surface term' is
  FORCED by R6 + parity, not assumed — the premise set of the banked forcing theorem
  loses one independent member AT THE CREASE"; `DECISION_SURFACE_UPDATE.md` G18
  bullet 1 stated the premise "is now FORCED by R6 + parity, not assumed" and bullet
  2 stated "ρ′_s = 0 … automatic at the crease" flatly; the TW4 bank-contradiction
  sweep said "the new result shows the premise is FORCED at the crease itself"; the
  JSON `TW5_consequences.G18` carried the same "FORCED (not assumed)" phrasing. As
  read, these conflate two DIFFERENT premises: the banked conditional-forces-fold
  theorem operates in the TWO-SIDED matching problem (deciding fold-vs-partner on
  the double cover, BEFORE any fold is concluded) and keeps ALL its premises; the
  new crease result is POSTURE-CONDITIONAL — GIVEN the single-copy quotient posture,
  no active wall action is admissible at N=2 — a complementary COUSIN fact, not a
  derivation of the theorem's premise. The package's own parenthetical ("the
  two-sided version … still carries it") conceded the distinction.
- **AM-V2 (germ locality):** the flat statements "all higher germ content
  variationally INERT" (`EXACT_DERIVATION.md` TW2 item 2 tail; DECISION_SURFACE
  table D-a row; ledger P02; JSON `active_content`), "two members differing beyond
  the first germ give IDENTICAL stationarity conditions" (TW4 nonuniqueness prose),
  and the two "effectively UNIQUE" ledger rows (V01, V04) lacked the scope "at the
  realized seam germ / per realized configuration". The inertness is GERM-LOCAL: the
  verifier's V2c counter-computation shows a pure (ρ−ρ_s)³ perturbation, inert at
  ρ_s, has ACTIVE content 3(ρ₁−ρ_s)² at a different realized trace ρ₁.
- **Minor (a):** "the exact N=2 form of the banked BDY-TD total-derivative/primitive
  nonuniqueness" over-identified — M19/BDY-TD is momentum/primitive-shifting
  total-derivative freedom; the inert germs shift nothing at the realized point
  (closer to primitive nonuniqueness); the analogy is a gloss, not an identification.
- **Minor (b):** the contract's "J07/J08 imposed exactly" is discharged BY TYPING
  (their banked class is typing/GC requirements) — compliant, but the discharge
  status was not explicitly noted where the requirement cut is presented.
- **Minor (c):** the mirror-wall theorem was proven once (even-invariant
  construction); the verifier's SYMMETRIZATION proof (generic degree-4 polynomial
  density in all six jets, even part — strictly more general, no invariant basis
  assumed) was available for adoption.

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifact
preserved as `VERIFIER_INDEPENDENT_CHECK.py`, 31 checks, exit 0, all pass)

- **Rerun / reproducibility:** exit 0; 57/57 with the substantive/guard split
  audited by name and found honest ("if anything the S0a rows are under-billed as
  guards"); stdout byte-identical across two reruns AND against the committed
  `DERIVATION_STDOUT.txt`; regenerated JSON byte-identical. **Contract-first
  VERIFIED in git** (da29fa0 commits PREREGISTRATION.md + LIVE.md only; every
  derivation artifact postdates it). Forbidden-content grep clean (no x_max, no
  anchor values, no G18/fold assumption, no census/pairing adoption).
- **The independent selector hunt (F-B1, attacked the landed no-selection direction
  hardest) — per-requirement record:** **R9** = global periods, banked class GC (on
  K₄-torsion cycles provably VACUOUS for closed forms per the banked V8 note; live
  content = completion-class / J07/J11 cocycle cycles — exactly what the package
  types OPEN); **R13** = argument/provenance-level, cannot pin the germ FUNCTION;
  **K₄ character** trivial on wall directions (banked, argument-level); **J07/J08**
  banked as typing requirements, discharged by the 𝔠-argument + per-stratum typing;
  **N=4** a genuinely new derivation (2-jet natural BCs), prereg-sanctioned
  deferral. **No banked-derivable selector was missed**; a further GC cut can only
  SHRINK the open-end germ family (the fold/glue results are PW-rigid downward).
  **The no-selection headline SURVIVED the hunt, correctly stamped "at N=2"
  everywhere checked.**
- **The N=4 ρ″-germ note:** the package correctly scopes the crease kill to N=2 —
  at N=4 a ρ″-germ would survive parity; the EXTENSION-REQUIRED stamp travels (now
  made explicit in limits (i)).
- **Independent re-derivations, all CORRECT:** the R6 unpaired-jet cut (own IBP:
  the N=2 boundary residue is (∂L/∂u′)·v — contains v, never v′; weight-robust);
  the inert-germ theorem on a fully generic function (V2a/V2b) **plus the V2c
  germ-locality certification → AM-V2**; the crease derivation (doubled momentum
  −8cosh(2φ)ρ′ matching the banked seam pkg; branch-uniform at φ=0; δφ essential;
  joint forcing 𝔅_ρ=0; the even-part slope-kill) — sound, with the FRAMING against
  the banked theorem the cousin-premise conflation → AM-V1; the flux-seal ⟺ 𝔅_Q=0
  equivalence both directions; the mirror-wall theorem by symmetrization (V5a–V5d,
  strictly more general; the un-symmetrized generic density fails the kill — the
  mirror-compatibility stamp genuinely load-bearing); the D-b non-independence +
  open-end laws (fold −𝔅_ρ/8→0; open-end −𝔅_ρ/4, q=−c_E𝔅_Q; the (β₁,β₂) plane
  realizes any output pair); consistency spot-checks at source (>3, incl. the M19
  row read VERBATIM).
- **The two over-claim cuts:** AM-V1 and AM-V2 — both phrasing-level, both in the
  exciting direction, neither changing the verdict class, the per-candidate table,
  or the no-selection-at-N=2 adjudication.
- **Mid-run bug-fix adjudication (CLEAN):** the original `TW5c` coding tested
  parity about the cell CENTER — a genuinely WRONG premise (odd-about-center leaves
  f = βx alive, so the check rightly failed); the final per-wall form is the banked
  gradient-seat form and is STRONGER (kills α and β). The fix corrected the
  premise, did not weaken any condition.
- **Falsifier hunts:** F-B3 hunted FIRST — full stamps on all three surfaces, no
  unstamped claim; F-B1 not fired (see the hunt); F-B2 (Tonti) not fired (B enters
  as a generic function; witnesses used only for nonemptiness/realization); F-B4/
  F-B5/F-B6 not fired; F-B7 none (the verifier's one in-run failure was its OWN
  cosh-canonicalization coding bug, fixed — the package identity is exact).
- **Minor notes:** the BDY-TD gloss flagged (not load-bearing); several SUBSTANTIVE
  checks are algebraically thin reproductions whose load lives in the jump laws +
  banked values (verified independently) — honest, noted for the record.

## 3. Changes made (this amendment pass)

1. **`derive_boundary_action.py`** —
   - Docstring amendment banner (AM-V1/AM-V2/minors; no pre-amendment computed
     claim changed). `check`/`check_nonzero`/`check_bool` gain a `credit` field
     (credited checks print `[verifier-credited]`; JSON lists them under
     `checks_verifier_credited`); JSON gains an `amendment` key; counts gain a
     `verifier_credited` field.
   - **AM-V1:** JSON `TW5_consequences.G18` restated in the posture-conditional
     form (fold posture self-consistent; the two-sided theorem keeps ALL premises,
     loses ZERO members; the G18 reduction posture ∧ Branch-G ∧ germ data
     unchanged). NEW credited GUARD note **`AMV1_cousin_premise_distinction_note`**
     (cited-argument row distinguishing the two premises exactly, placed at the
     fold cut where the crease result is derived).
   - **AM-V2:** the TW2c comment restated germ-locally; NEW credited checks
     **`AMV2a_higher_germ_active_at_other_trace_exact`** (zero-residual: the
     verifier's (ρ−ρ_s)³ perturbation has active content EXACTLY 3(ρ₁−ρ_s)² at a
     different realized trace) and **`AMV2b_locality_counterexample_nonzero_off_
     trace`** (certified nonzero off-trace); JSON `active_content` and
     `per_candidate` fold/glue texts scoped "at the realized seam germ / per
     realized configuration".
   - **Minor (a):** the BDY-TD comment/JSON gloss softened
     (primitive-nonuniqueness-like; looser analogy, not the exact form).
   - **Minor (b):** JSON `TW3_cut.J07_J08` notes the discharge-by-typing status
     explicitly.
   - **Minor (c):** the verifier's symmetrization proof adopted as credited checks
     **`AMV3a`–`AMV3d`** (generic degree-4 polynomial density in all six jets,
     even part under (p0,f1,h1) → −(…): π_f, π_h vanish identically at the kill
     locus; π_p generically nonzero with its variation essential-killed; the
     un-symmetrized density fails the kill — load-bearing stamp re-proven).
2. **`EXACT_DERIVATION.md`** — amendment banner + post-amendment counts + status
   VERIFIED-WITH-AMENDMENT; TW2 item 2 germ-local scoping + softened gloss +
   credited-check citations; TW3 contract note (J07/J08 discharged by typing); the
   fold paragraph restated posture-conditional with the AMV1 premise-bookkeeping
   note; the mirror-wall paragraph marked DOUBLY PROVEN (AMV3 credited); the glue
   effective-uniqueness scoped; the TW4 table rows (fold, glue) scoped; the TW4
   nonuniqueness prose scoped germ-locally; the TW4 three-way-honesty block records
   the verifier's independent selector hunt and its survival; the bank-contradiction
   sweep restated (premise set loses ZERO members); **TW5 bullet (iii) rewritten in
   the posture-conditional form** (the required AM-V1 rephrase, verbatim below);
   the F-B7 record updated (64/64; the TW5c fix adjudicated CLEAN); limits gain
   (i) the N=4 ρ″-germ note, (i-b) germ locality, (i-c) posture-conditionality.
3. **`WALL_RESPONSE_LEDGER.tsv`** — P02, V01, V04 scoped per AM-V2 (V01 also
   carries the AM-V1 posture-conditional stamp); V02 marked doubly proven (AMV3);
   AMEND-2026-07-30 row appended.
4. **`DECISION_SURFACE_UPDATE.md`** — header (verified-with-amendment); the lay
   verdict line restated conditionally ("IF the seam is a mirrored crease…"); the
   D-a table row scoped + gloss softened; **G18 bullets 1–2 rewritten in the
   posture-conditional form** with "loses ZERO members" and "the G18 reduction
   (posture ∧ Branch-G ∧ germ data) survives the amendment unchanged" explicit.
5. **`CORRECTION_LAYER.md`** (this file) + **`AUDIT_REPORT.md`** (the owed
   deliverable) written.
6. **Rerun record:** `python3 derive_boundary_action.py` → **64/64, exit 0 = 55
   SUBSTANTIVE zero-residual exact-SymPy checks (49 original + 6 verifier-credited:
   AMV2a/b, AMV3a–d) + 9 GUARD (8 original + the AMV1 cited-argument note)** — all
   57 pre-amendment computations surviving, none altered, none relabeled. **Three
   consecutive runs byte-identical** (stdout AND JSON): stdout sha256
   dcd8dbe367fde4f112601651033e4a5da34a321c176f8a6a0a321ca073fd9611, JSON sha256
   a9d2f4ccb37bfb04e0a2579286ca0828e3d7689a6c0a1115e6d8c86c25d6a408 — determinism
   reconfirmed post-amendment. `DERIVATION_STDOUT.txt` and
   `boundary_action_results.json` regenerated by rerun, ~0.7 s wall, single CPU
   process. Exact SymPy only (no floats, no numeric solvers, no randomness, no GPU).

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The composite verdict OW2** — a FAMILY with exact wall-moduli; no candidate
  emptied, none unique-selected — untouched (the verifier re-derived every
  load-bearing leg; both amendments are scope/framing cuts; **OW2 unaffected** —
  the verifier's own words).
- **The no-selection-at-N=2 headline** — B has NO candidate-selecting content at
  N=2; the discriminator is the discrete POSTURE — untouched, and STRENGTHENED by
  surviving the verifier's independent per-requirement selector hunt (R9/GC, R13,
  K₄ character, J07/J08, N=4: no banked-derivable selector missed).
- **The TW1 census** (C01–C14; both arenas; provenance and parity gradings) —
  untouched.
- **The TW2 parametrization with its R6 cut** — one trivial-character function of
  the parity-surviving 0-jet traces per wall stratum; φ only through Q; the
  unpaired-jet cut (weight-robust) excluding all 1-jet arguments at N=2 —
  untouched (verifier re-derived on its own IBP).
- **The crease result ITSELF** — GIVEN the quotient posture, the active germ is
  forced trivial at N=2 (Q-germ inert by essential δφ=0; ρ-germ forced 0 by R6 C¹
  + parity vs the natural BC) — untouched AS RESTATED in the posture-conditional
  form; AM-V1 rescopes the FRAMING, it does not weaken the derivation (the
  verifier: "The DERIVATION is sound").
- **The glue pin + flux-seal equivalence** — 𝔅_ρ = q/2 (K6c reproduced) AND
  [π_φ] = 0 ⟺ 𝔅_Q = 0 (the NEW exact equivalence) — untouched.
- **The mirror-wall theorem** — the effective wall response at a mirror wall
  forced trivial at N=2, pairing-branch-independent — untouched and now DOUBLY
  PROVEN (the package's even-invariant construction + the verifier's strictly-
  more-general symmetrization proof, adopted as credited checks AMV3a–d).
- **The open-end laws** — q = −c_E𝔅_Q, ρ′_s = −𝔅_ρ/4; the free 2-germ-function
  family realizing ANY (q, ρ′_s) output pair; the banked q=0-under-no-choice
  exhibited as the germ-flat stratum — untouched (the open-end "2 germ FUNCTIONS"
  count already embodied the function-level freedom; the verifier required no
  change there).
- **The D-b dependence** — D-b NOT independent of D-a at the fold/open-end
  postures (a derived function of the B-germ); FREE at partner — untouched.
- **All consistency reproductions** — TS1/S1f handshake underdetermination; K6c
  B′ = q/2; K6d q = 0 ∧ ρ′ = 0 under no-choice; K4d; K4e–K4g; ΔΠ = q/2
  (banked-in-use, cited); Slice-2b M-WALL = a_F·M-GEN — untouched (all
  zero-residual; verifier spot-checked at source).
- Also untouched: the ceiling (no closure / census / pairing adopted; no law
  crowned; the G18 update remains a PROPOSAL with Charles ruling); all F-B3
  stamps; the pairing-relation one-way typing (F-B5); x_max held (G14); no anchor
  values; every one of the 57 pre-amendment checks (0 relabeled, 0 altered).
