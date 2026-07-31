# CORRECTION LAYER — P4 seam-closure derivation (amendment A1 + adopted verifier legs, per VERIFIER_REPORT.md)

Date: 2026-07-30. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`; one
REQUIRED amendment A1 + non-blocking recommendations — all implemented). **No
pre-amendment COMPUTED claim was broken** (the verifier re-derived every load-bearing
leg independently — `VERIFIER_INDEPENDENT_CHECK.py`, 31 checks, exit 0, all pass,
function-level where the package worked at jet level): the required amendment is a
**PREMISE RESTORATION** on the conditional-forces-fold headline — the premise set
must include **Branch-G on BOTH sides of the seam (interior AND beyond)**, not only
"G beyond." The package's own body KNEW the premise (K3d and the P-interior
quotient-only clause sit in the same K3 verdict paragraph) — **the drop was
headline-level only**, and the ρ'_s≠0 C¹-impossibility leg is branch-INDEPENDENT
(the mirrored profile's ρ'-jump −2ρ'_s is kinematic) and unaffected. Verdict **OC2
stands** unchanged: BRIDGE-ONLY derived; closure genuinely free; the conditional
fold now on its full premise set; K6 necessary-not-selected; arena-split; banked
decider absent; standing falsifier not fired.

## 1. Original claims (as they stood pre-amendment)

- **The conditional-forces-fold premise set (A1 — the required catch):** stated as
  `{no seam surface term (⇒ WE C¹ matching)} ∧ {Branch-G beyond} ∧ {ρ'(r_s)=0} ⟹
  fold FORCED (unique continuation = odd mirror)` — with the INTERIOR-branch premise
  dropped — at six loci: `EXACT_DERIVATION.md` (the K3 verdict; the TS3 sharpening),
  `FORCING_LEDGER.tsv` (the K3 row; the COMPOSITE row),
  `DECISION_SURFACE_UPDATE.md` (item 1), the script comment above K3h, and
  `seam_closure_results.json` (`TS2_verdicts.K3`; `TS3_composite`). As read, the
  statement is FALSE for a Branch-P interior: the forcing argument runs through K3c
  ("the reflection maps G-solutions to G-solutions"), which requires the interior
  solution to be Branch G.
- **The check split:** 42/42 exit 0 = 33 SUBSTANTIVE + 9 GUARD, with ~4 of the
  SUBSTANTIVE rows trivial-by-construction (S1f_handshake_germA_flat ≡ 0−0;
  S1f_handshake_germB_mirror_seam_value_identity — a substitution identity; the K3g
  phip/rho slots — identically zero even off-locus): witness-assembly steps carrying
  no computational load, labeled as computations.
- **The F-C2 discharge:** carried at JET level (K3c/K3d on second-jet substitution);
  the banked EOMs were REUSED from `derive_universe_fold_d1.py` without an in-package
  verification that they are the genuine Euler-Lagrange equations of the banked
  reduced Lagrangians.
- **Minor:** a dead variable (`germB_val`, computed-and-unused) in the script; K6a's
  boundary-variation expression mixes the single-copy π_φ with the doubled
  ρ-momentum without a note (moot — δφ=0 essential kills the π_φ term).
- **`AUDIT_REPORT.md`:** owed by the contract's deliverable list, not yet present.

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifact
preserved as `VERIFIER_INDEPENDENT_CHECK.py`, 31 checks, exit 0, all pass)

- **Rerun:** exit 0; 42/42 with counts independently recomputed; stdout and JSON
  byte-identical on rerun; pure CPU SymPy, deterministic, no floats/numeric
  solvers/GPU (grep-verified). **Contract-first verified in git** (commit 2254888
  contains ONLY the preregistration + LIVE.md). Forbidden-content grep clean
  (G18/x_max/anchors/census/pairing only in negation/guard statements or as the TS4
  re-grade subject).
- **A1 counter-computation (V2d, zero-residual, function-level):** the odd mirror of
  a **Branch-P interior** fails the G φ-equation with exact residual
  **−4e^{−2φ}ρ'²/(Zρ²)** — nonzero wherever ρ'≠0 in the interior. So with a P
  interior satisfying all three originally-stated conditions, the unique G
  continuation EXISTS (Picard) but is NOT the mirror — "fold FORCED" false as read.
  Fix prescribed: restore the interior-branch premise at all six loci; no other
  claim changes.
- **Underdetermination GENUINE, confirmed at source:** §235/§236 read at
  `negative_phi_native_geometry.md:16668-16770` — five facts match verbatim; §236's
  own limits quoted accurately (the boundary action is the bridge's own named
  missing upgrade). **The banked §235 script confirmed a pure dataclass PRINTER —
  zero computation** — the package's honesty item is accurate and the native
  recomputation was necessary; the verifier recomputed the five facts independently
  and re-derived both witness germs (flat glue and odd mirror both pass the full
  handshake; first jets differ by φ₋'(r_s)); no missed handshake condition found
  that cuts the germ space. Decisive corroboration: the corpus itself banks BOTH
  germs in use (flat glue at the matter cell; fold-assumed at the universe cell).
- **The conditional-fold locus SOUND at the locus:** reflection seam data, the iff
  (φ_s=0 ∧ ρ'_s=0), the Picard leg (jacobian singular only at ρ=0; φ absent from
  the G RHS; autonomous system), and the off-locus C¹ gap −2ρ'_s all re-derived.
  Regularity-class adjudication: C¹ is the right class FOR the no-surface-term (WE)
  posture; the glue-with-jump weaker class is exactly covered by the D-a
  conditioning; the impossibility claim correctly scoped "as a C¹ configuration."
- **K4 confirmed** (momenta; −8cosh(2φ)ρ'; essential/natural BCs; WE
  continuity-only for P|P and P|G). **"Banked decider ABSENT" CONFIRMED at source:**
  `universe_cell_fold_jc_sigma_results.md:104` ("needs partner=mirror-image =
  closed-cell premise"); fold-JC :31-33 records the independent-partner fork with
  NO ρ'-pin.
- **K6 re-run** (fold/partner boundary terms; B'(ρ_s)=q/2 with the required B
  verified to be the 07-18 OPEN object at source; q=0 forcing re-derived).
  "Necessary but not selected" is the correct reading.
- **Arena-split CONFIRMED at source** (`weld_two_sided_results.md` :30-33, :39-41):
  matter seam = glue-with-jump IN-USE; universe seam fold = canon-assumed (G18).
  No banked reconciliation; the split is real.
- **Standing falsifier NOT FIRED is correct, and the distinction is REAL:** the
  banked unsatisfiability concerns a point involution of the toric arena under the
  pointwise crease; the conditional fold here is a 1D radial-profile relation with
  the screen/angular action explicitly unspecified — different mathematical objects;
  the banked escapes remain exactly as banked.
- **F-C2 discharge SOUND — and re-done at FUNCTION level** (V1a–V1d: the banked
  EOMs verified as genuine Euler-Lagrange equations; V2a–V2c: mirror-of-G solves G
  and mirror-of-P fails P with the exact banked residuals at function level —
  stronger than the package's jet-level check). No symmetry-of-equations promoted
  anywhere; the one under-stated premise is A1.
- **Bug-fix corroboration:** the two exp/cosh canonicalization fixes only
  STRENGTHEN the prover (a genuine nonzero cannot become zero under
  rewrite+simplify); the verifier's own independent script hit the identical
  canonicalization need on the same two expression families — genuine SymPy-path
  issues, not weakened conditions. The mis-assembled-witness fix sound at its final
  resting place; `germB_val` flagged as a harmless dead fossil. No check condition
  weakened by any fix.
- **Falsifier hunts:** F-C3 hunted FIRST — full five-slot stamps everywhere, no
  unstamped claim, **no eleventh catch**. F-C1 both directions — the fold-favorable
  content got the HARDER audit (and yielded A1); the bridge-only verdict's
  load-bearing leg re-derived and corroborated. F-C4 no smuggle; F-C5 every cited
  bank locus checked at source, no contradiction; F-C6 no symbolic failures.

## 3. Changes made (this amendment pass)

1. **`derive_seam_closure.py`** —
   - Docstring amendment banner (A1 + recommendations; no pre-amendment computed
     claim changed); `check`/`check_nonzero` gain a `credit` field (credited checks
     print `[verifier-credited]`; JSON lists them under
     `checks_verifier_credited`); the eight hand-rolled CHECKS appends unified
     through a `check_bool` helper (output content unchanged in substance).
   - **A1:** the comment above K3h restates the premise set as {no seam surface
     term (WE C¹), **Branch G on BOTH sides of the seam (interior AND beyond)**,
     ρ'_s=0}, with the counter-computation cited. NEW credited check
     **`AM1_mirror_of_P_interior_fails_G_phi_exact_residual`** (the verifier's V2d
     adopted): the mirror of a P interior fails the G φ-equation with exact
     residual −4e^{−2φ}ρ'²/(Zρ²), certified nonzero — function-level.
   - **Function-level F-C2 discharge adopted (credited):** `AM2a`–`AM2d` — the
     banked P and G EOMs verified as the GENUINE Euler-Lagrange equations of the
     banked reduced Lagrangians (previously reuse-declared only); `AM2e`/`AM2f` —
     the odd mirror of a G-solution solves G at FUNCTION level; `AM2g` — the
     mirror of a P-solution fails P at function level with the exact residual
     −(4ρ'²/(Zρ²))(e^{−2φ}+e^{2φ}). These corroborate (do not replace) the
     jet-level K3c/K3d.
   - **Relabels (honest split):** `S1f_handshake_germA_flat`,
     `S1f_handshake_germB_mirror_seam_value_identity`, `K3g_data_identity_on_
     locus_phip`, `K3g_data_identity_on_locus_rho` — SUBSTANTIVE → GUARD, each with
     an honest in-script note (trivial-by-construction / identically zero even
     off-locus; witness-assembly, not computation). The load-bearing S1f content
     (the on-locus handshake + the certified-nonzero jet gap) and the load-bearing
     K3g slots (phi, rhop — zero exactly on the locus and only there) remain
     SUBSTANTIVE.
   - Dead `germB_val` line removed. K6a single/doubled-momentum clarifying comment
     added (moot under δφ=0 essential — 2π_φ·0 = π_φ·0 = 0). JSON gains an
     `amendment` key; `TS2_verdicts.K3` and `TS3_composite` restated on the full
     premise set; counts split original/credited.
2. **`EXACT_DERIVATION.md`** — header (post-amendment counts; verified status;
   amendment banner); the K3 verdict restated on the full premise set with the A1
   note and the branch-independence of the impossibility leg; the TS3 sharpening
   restated ({B ≡ 0, Branch-G on BOTH sides, ρ'_s=0}); the D-c bullet notes the
   interior-branch datum; the TS4 FALLS-2 anchor restated ({D-a, D-b, Branch-G on
   both sides}); the K6a clarifying note added; the honest-split section rewritten
   (50/50 = 37 SUBSTANTIVE [29 original + 8 verifier-credited] + 13 GUARD, with
   the relabel reasoning and the bug-fix corroboration).
3. **`FORCING_LEDGER.tsv`** — K3 row and COMPOSITE row restated on the full premise
   set (+ AM1 in the checks column; counts updated); AMENDMENT-2026-07-30 row
   appended.
4. **`DECISION_SURFACE_UPDATE.md`** — header (verified; amendments applied); item 1
   restated on the full premise set with the P-interior clause.
5. **`CORRECTION_LAYER.md`** (this file) + **`AUDIT_REPORT.md`** (the owed
   deliverable) written.
6. **Rerun record:** `python3 derive_seam_closure.py` → **50/50, exit 0 = 37
   SUBSTANTIVE zero-residual exact-SymPy checks (29 original + 8 verifier-credited:
   AM1, AM2a–g) + 13 GUARD** (all 42 pre-amendment computations surviving — 4
   relabeled, none altered), ~1.1 s wall, single CPU process. **Three consecutive
   runs byte-identical** (stdout AND JSON): stdout sha256
   f8c472ba37dcc0843e7c5e5bfa9167d8b64f73abd2c9d2cc4c814e50cc659cd8, JSON sha256
   c0b8b772acdb928c13e50409c8b21ebc7bb5a77f676a4621224b3c473c32105a — determinism
   reconfirmed post-amendment. `DERIVATION_STDOUT.txt` and
   `seam_closure_results.json` regenerated by rerun. Exact SymPy only (no floats,
   no numeric solvers, no randomness, no GPU).

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The composite verdict OC2** — BRIDGE-ONLY derived; the closure genuinely free
  on the banked record — untouched (the verifier: "the landed verdict survived
  adversarial re-derivation on every load-bearing leg").
- **The bridge floor (TS1) + the witnessed underdetermination** — the five
  recomputed bridge facts; the two-germ witness (flat glue vs odd mirror, both
  passing the full handshake, jets differing by φ₋'(r_s)) — untouched
  (verifier-re-derived; corroborated by the corpus banking both germs in use).
- **The conditional-fold locus itself** — the iff (φ_s=0 ∧ ρ'_s=0), the on-locus
  identity, the Picard uniqueness leg (ρ_s≠0), the forcing ON the restored premise
  set — untouched AS RESTATED: with {no seam surface term (WE C¹), Branch-G on
  BOTH sides, ρ'(r_s)=0} the fold IS forced; A1 adds the premise, it does not
  weaken the theorem on its locus.
- **The off-locus impossibility** — ρ'(r_s) ≠ 0 ⟹ fold IMPOSSIBLE as a C¹
  configuration — untouched and branch-INDEPENDENT (the −2ρ'_s jump is kinematic;
  verifier-confirmed explicitly).
- **K4** — the discriminator iff (fold ⟺ ρ'(r_s)=0 + posture class; partner ⟺
  ρ'(r_s) free) and the banked decider ABSENT (fold-JC :104 at source) — untouched.
- **K6** — closure NECESSARY but NOT SELECTED (fold, partner, glue+B all
  well-posed); the bare-free-endpoint q=0 forcing; the selector object = the
  underived 07-18 boundary action — untouched.
- **The arena-split map fact** — matter-cell seam = flat-exterior glue with jump
  q/2 (banked-in-use) vs universe-cell seam = fold (canon-assumed input) —
  untouched (verifier-confirmed at source).
- **The standing-falsifier non-firing** — no unconditional fold derived; the
  conditional fold names its arena (1D radial reduction; no toric-arena involution
  asserted); the banked unsatisfiability untouched — confirmed by the verifier as
  a real distinction, not wordplay.
- **The D-a/D-b/D-c reduction** — the closure freedom reduced to {seam boundary
  action B (07-18 OPEN); the ρ'(r_s)-pin/beyond-ontology datum; the branch beyond}
  — untouched (A1 makes the interior-branch datum explicit inside it; the count of
  named banked-open data is unchanged).
- **TS4's consumer map facts** — G18 neither confirmed nor refuted (re-grade
  PROPOSAL only); FALLS-2 consumers unchanged-conditional; E0-collapse/fields-
  massive branch unchanged; constants-side triad unchanged; the OC1/OC3
  counterfactual rows — untouched (verifier: they "match the banked conditionals
  exactly").
- Also untouched: the ceiling (no closure adopted, no census/pairing adopted, no
  massive-branch verdict language); all F-C3 stamps; the K5/K7 cited-structural
  rows; x_max held (G14); no anchor values.
