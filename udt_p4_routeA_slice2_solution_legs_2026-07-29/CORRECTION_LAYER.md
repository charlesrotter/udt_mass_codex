# CORRECTION LAYER — P4 Route A Slice 2 (solution-touching legs) (amendments A1–A2, per VERIFIER_REPORT.md)

Date: 2026-07-29. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`).
Both amendments are **F-D3-class STAMP repairs — no computation refuted, no claim's
underlying mathematics touched, no falsifier fired**: A1 installs the missing sign(a_F)
scope stamp on the depth-profile SHAPE language ("well"); A2 closes a proof-coverage
gap on a TRUE claim (the locus-nonemptiness witnesses covered only one background
point) by adopting the verifier's general legs. Nothing here changes the outcome
class, any atlas closed form, any lens tally, the tie derivation, or any banked input.

## 1. Original claims (as they stood pre-amendment)

- **The "well" shape language** (script `TD1_LE_disc_E0_sign_structure` detail; the
  ledger `well family` label on all 10 quadratic-w rows; `EXACT_DERIVATION.md` §2.1
  ("a symmetric well in the anchored depth with a single minimum"), the §2.1
  background-transition bullet ("well vs affine"), the §1 T0 visible-instance line
  ("(affine, well)"), §2.3 W2-fs ("the FULL well atlas"), the §4 lens table ("wells
  for a_F ≠ 0"); `SLICE2B_SURFACE.md` §2 ("nodeless-well structure")): stated with no
  sign(a_F) qualification, though the explored background range includes a_F < 0
  (P1-4D: λ < 0; P1-triad: λ < −1/2), where the profile is a single-MAXIMUM bump.
  The closed-form verification also ran with `positive=True` on a_F (conditioning
  that was not shown non-load-bearing in-package).
- **The locus-nonemptiness claim** (script `TD2_selfconsistent_locus_nonempty`
  detail; `EXACT_DERIVATION.md` §3; the ledger `self_consistent_locus` column):
  "nonempty nonconstant at every a_F ≠ 0 background (witnessed legs + continuity)" —
  exhibited only at (a_F, ℓ) = (1, 1), with the sign leg written as
  "w ≤ 5/8 < 1 ⟹ I_p < 0" (an implication that flips for a_F < 0, since
  I_p = (∫log w)/a_F).
- **Dead code** (verifier note N4, cosmetic): unused `legA_ok`/`bound_A` in
  `derive_routeA_slice2.py`.

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifacts
preserved in `VERIFIER_INDEPENDENT_CHECK.py` + `VERIFIER_INDEPENDENT_STDOUT.txt`,
**21/21 own-construction checks, exit 0**)

- **The sign(a_F) catch (A1)** — `V_shape_sign_of_aF`: p0″(vertex) = 8A²/(a_F³c²)
  has the SIGN of a_F, so the "single-minimum well" reading holds only for a_F > 0;
  for a_F < 0 (inside the explored range) the profile is a single-maximum bump.
  **This is the FOURTH instance of the NAMED scope class in this arc** (Stage-2
  round-1 A1: the R7(b) stratum gloss; Stage-2 closure C3: the "only genuine cut"
  uniqueness gloss; Stage-3 A1: the anchored-log "whenever" quantifier; Slice-2 A1:
  a shape word missing its sign scope) — **mechanism-caught**: F-D3 was
  pre-registered as the class to hunt FIRST, and the verifier's first hunt found it.
  The sign-FREE content was verified UNAFFECTED: E0 ≥ 0 forcing (sum of squares),
  global regularity, nodelessness, and the closed form itself re-derived sign-free
  (`V_well_zero_residual_signfree` at free real a_F — the package's positivity
  declaration proven NOT load-bearing).
- **The proof-coverage catch (A2)** — the "every a_F ≠ 0 background" nonemptiness
  claim is **TRUE but was under-witnessed**: the exhibited legs cover only
  (a_F, ℓ) = (1, 1) and the stated sign-leg implication flips for a_F < 0. The
  verifier's `V_locus_legs_sign±` checks prove the claim at SYMBOLIC (|a_F|, ℓ) and
  BOTH signs of a_F (legs w ≤ 5/8 vs w ≥ 2 with E0 > 0 along the whole connecting
  path) — a coverage gap, not an error.
- **Strengthenings (beyond the package's own proofs):** the EXPLICIT global inverse
  of the parameter→initial-data map ((w0, w1, c_f, c_h) = (e^{aP0}, ae^{aP0}P1,
  e^{aP0}F1, e^{aP0}H1)) — stronger than and confirming the rank-6 spot check
  (`V_explicit_inverse_initial_data`); the symbolic-ℓ both-signs locus legs above.
- **Confirmations (attacked, all reproduced):** the GEN-QUAD tuple by an independent
  function-based EL route; both quadratures by differentiation; the background tie
  2E0·I_p = 0 re-derived (a_F′ = 2 on both P1 instances; on-shell W_F L̃₀ ≡ E0; the
  a_M-cancellation genuine given the banked Stage-3 generated construction); the
  **P2-side ABSENCE genuinely derived** (a_F′ ≡ 0), = the blindness-loci
  degeneration of the P1 tie; the pairing-relativity reading adjudicated CLEAN (FOR
  and AGAINST-universality both recorded, nothing promoted or suppressed); the
  M = 2ℓE0 CHOSE/CONDITIONAL stamp present at every use; F-D6 same-member
  integration; fork independence incl. the vacuous α-slot on BR-A; W3/ω/KMOD0/
  Route C (own parse, explicit-x substitution, autonomy verified); NV
  NOT-DERIVABLE-AT-SLICE-2 honesty (F-D8-compliant explicit report). Contract-first
  confirmed in git (PREREGISTRATION.md sole content of ef35a67); rerun ×2
  byte-identical; guard split honest (notes N1/N2 recorded, not required).

## 3. Changes made (this amendment pass)

1. **`derive_routeA_slice2.py`** —
   - Docstring amendment banner (A1/A2, verbatim scope of each).
   - **3 new zero-residual A1 checks** (verifier's sign-free re-derivation adopted):
     `A1_well_zero_residual_signfree` (the closed form solves all three field
     equations at FREE REAL a_F, both signs, c_f/c_h real),
     `A1_vertex_curvature_sign_of_aF` (p0″(vertex) = 8A²/(a_F³c²) exactly;
     instantiated positive at a_F = +1, negative at a_F = −1),
     `A1_bump_instance_regular_nodeless` (the explicit a_F = −1 member
     w = x²/2 + 1: zero residual, disc = −2 < 0, globally regular, nodeless,
     p0″(0) < 0 — a bump, exactly as regular as the well).
   - **2 new zero-residual A2 checks** (verifier's legs adopted):
     `A2_locus_legs_general_sign_pos`/`_neg` — symbolic (|a_F|, ℓ), each sign:
     leg A′ realizes w = x²/(8ℓ²) + 1/2 ≤ 5/8 < 1, leg B′ realizes
     w = x²/ℓ² + 2 ≥ 2 > 1, E0 > 0 proven symbolically on both; I_p changes sign
     between the legs for either sign of a_F; continuity (Category-A) gives the
     I_p = 0, E0 > 0 root at every a_F ≠ 0, ℓ background.
   - **Stamp restatements (detail strings only; math and pass conditions of all 36
     pre-amendment checks unchanged):** `TD1_LE_disc_E0_sign_structure` (sign-stamped
     shape + "symmetric = about the vertex"), `TD1_LE_well_solution_zero_residual`
     (positivity declaration noted as conditioning, A1 cited),
     `TD2_selfconsistent_locus_nonempty` ((a_F, ℓ) = (1, 1) witness stamp + the
     sign-dependence note), `TD3_lens_classification_record` (sign-stamped tally),
     the ledger strings `WELL_SOL` (family renamed shape-neutrally: "nodeless
     quadratic-w family", with the A1 sign stamp in-row) and `SC_P1` (witness stamp
     + A2 citation).
   - Dead code `legA_ok`/`bound_A` removed (N4, cosmetic).
   - JSON gains an `amendments` block (verdict, A1, A2, dead-code note).
2. **`EXACT_DERIVATION.md`** — header (41/41 = 33 substantive + 8 guards; amendment
   banner); §1 T0 visible instance "(affine, nodeless quadratic-w)"; §2.1 emergent
   sign structure split into the sign-FREE bullet + a new **"Shape is
   sign(a_F)-scoped (A1)"** bullet (the sign law, the bump instance, the explored
   a_F < 0 range, "symmetric = about the vertex", the three A1 check names); §2.1
   background-transition bullet (quadratic-w vs affine; the WELL↔BUMP flip recorded
   as a second sign-scoped facet); §2.3 W2-fs (sign-stamped atlas name); §3 P1-side
   locus bullet fully restated (witness stamp, the sign-dependent-implication note,
   the A2 check names); §4 lens table (sign-stamped); §7 F-D3 (the two repairs
   recorded, fourth-catch pointer) and F-D5 (new counts); limits gain (viii) — the
   sign(a_F) scope on every shape word.
3. **`SLICE2B_SURFACE.md`** — basis line (41/41; amendment pointer); the §2
   bootstrap-follow-ups bullet ("nodeless quadratic-w structure (single-minimum well
   for a_F > 0 / single-maximum bump for a_F < 0 — the A1 sign stamp travels)").
4. **`AUDIT_REPORT.md`** (NEW, owed by contract §6 step 5) — grade, TD1–TD6 table,
   the sign-stamped emergence, the bootstrap-lens record, lens tallies, the
   falsifier record with the fourth-catch memorial, limits, verifier record,
   Slice-2b pointer.
5. **Regenerated deterministically by rerun:** `SOLUTION_ATLAS_LEDGER.tsv` (still
   20 rows + preamble; delta = the `nodeless quadratic-w family` label with the A1
   sign stamp on the 10 quadratic-w rows and the A2-stamped `self_consistent_locus`
   text), `routeA_slice2_results.json`, `DERIVATION_STDOUT.txt`.
6. **Rerun record:** `python3 derive_routeA_slice2.py` → **41/41, exit 0 = 33
   substantive zero-residual checks + 8 citation guards** (36 pre-amendment checks
   all surviving with math and pass conditions unchanged — 4 substantive detail
   strings + 2 ledger strings amended — plus the 5 new `A1_*`/`A2_*` checks), <2 s,
   single CPU process. Three consecutive runs byte-identical: JSON sha256
   1871e1e2f9d1224aef41e1a4c977f8a7f4629d114a1f1a113dd7387d2d062d4c, ledger sha256
   afad41240d024b3d3353d1846a8ee3dcc7e129c6e984d507b42bca36ece8b373, stdout sha256
   22905d5ec6e2db3e019015e8a0e62fe042665ab95d10b77a0290a03aad09c88c — determinism
   reconfirmed post-amendment.

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The outcome class** — OD1 (survivors map populated; OD2/OD3/OD4 not triggered)
  — untouched; both amendments are stamp/coverage repairs on prose and detail text.
- **The atlas closed forms** — the quadratic-w family (e^{a_F p0} = (a_F²E0/2)x² +
  w1x + w0, f′ = c_f/w, h′ = c_h/w), the affine atlas, the ω stratum {k10 = 0}, the
  W3 degenerate set, the quadratures, the first integrals: all byte-equivalent in
  math (verifier-reproduced by independent routes).
- **E0 ≥ 0 forcing and regularity/nodelessness** — SIGN-FREE, verified so by the
  verifier and now by the in-package A1 checks; the emergent-structure observation
  stands with only its shape word sign-scoped.
- **The background tie 2E0·I_p = 0 and its pairing-relativity** — the derivation,
  the a_M-cancellation, the P2-side identical absence, the blindness-loci
  degeneration, and the FOR/AGAINST-universality observation record: untouched
  (verifier-re-derived).
- **The lens tallies** — all representatives WORKS-GENERICALLY (rep-scoped); NV R5
  legs UNDETERMINED; **zero eliminations (F-D2 never engaged)**; no
  CONDITIONAL-ON-BACKGROUND find: unchanged (A1/A2 change no class membership —
  bumps are solutions exactly as wells are).
- **The KMOD0 quotient** — the stratum identity, the gauge tangent, the L23-orbit
  reading: untouched.
- **Fork independence** — α/𝔠/c_E absence, a_M-independence, BR-B role-only:
  untouched.
- **All F-D records** — F-D1/F-D2/F-D4/F-D5/F-D6/F-D7/F-D8 clean as verified; the
  F-D3 record now additionally memorializes the two verifier-caught stamp repairs.
- **The prereg contract, the ceiling, and the bootstrap-lens frame** — no law
  crowned, no carrier, no background fixed, the bootstrap neither imposed nor
  suppressed; settling stays with Charles.
