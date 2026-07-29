# CORRECTION LAYER — P4 Route P seal-parity (amendments A1–A4 + adopted verifier legs, per VERIFIER_REPORT.md)

Date: 2026-07-29. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`; A1
required and **load-bearing textual** — one map-fact claim's meaning changed by a
mis-citation; A2 minor same-leg; A3 an asserted-not-evidenced sentence; A4
recommended, all implemented). **No pre-amendment COMPUTED claim was broken** (the
verifier confirmed every computed leg by independent re-derivation, 41/41 own-script);
the flaw was prose that mis-scoped a banked citation in a way that changed its
meaning. Outcome class **OP3 stands**. The verifier's mutation catch-proofs, its
completed K₄-honesty leg, and its compensation-loophole-closing H-block lemma are
ADOPTED as in-package checks (credited).

## 1. Original claims (as they stood pre-amendment)

- **The anchored-pairing landing (A1 — the load-bearing textual flaw):** check-25
  (`TP4_aF_anchor_landing`), the `routeP_results.json` `aF_landing` entry, and the
  `EXACT_DERIVATION.md` TP4 bullet stated that the P1-4D branch "lands ON a_F = 0,
  the value at which the banked record states … 'no λ-row either way' (the banked
  massive/massless divergence is ABSENT at that weight)" — reading the banked P2-side
  condition **a_F′ = 0** (the pairing weight's λ-DERIVATIVE identically zero) as the
  weight VALUE **a_F = 0**. That is a different criterion: under P1-4D at λ = 0,
  a_F(0) = 0 but a_F′(0) = 2 ≠ 0, so the λ-row does NOT vanish by banked
  pairing-relativity at the landing; what happens to it at an a_F = 0 background is
  UNDERIVED on banked footing (the quadratic atlas and the I_p sign-change
  certificate both presuppose a_F ≠ 0). The mis-reading made the landing sound
  tie-free — STRONGER than banked, in the ANTI-massive (cutting) direction.
- **The TP4 quote (A2):** `EXACT_DERIVATION.md` quoted the banked record as
  "P2 side (a_F = 0)" — the prime was dropped (the forcing package itself writes
  a_F′).
- **The F-P6 catch-proof sentence (A3):** "catch-proofs verified (wrong-parity,
  wrong-dressing, wrong-signature and screen-swap-in-class claims all FAIL the same
  machinery)" — asserted with NO catch-proof artifact in the package.
- **A4 items:** the ledger row "Lorentz membership EMPTY" carried no readout stamp
  (the script detail had the η-scope; the row did not); the check-22 detail said
  "(F2 K adj F2)[0,1] = k10" (it is −k10; the computed check used only ≠ 0);
  `TC_family_assembly` said "4 continuous parameters" flatly (branch (a) has 3).
- **The check split:** 34/34 exit 0 = 26 substantive + 8 guards (verifier-audited
  honest; unchanged in kind — the amendment adds 7 substantive checks).

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifact
preserved in `VERIFIER_INDEPENDENT_CHECK.py`, **41/41 own-construction checks,
exit 0**)

- **Reruns:** exit 0; JSON/TSV byte-identical on rerun (sha256); stdout identical to
  the packaged `DERIVATION_STDOUT.txt`; exact-SymPy-only confirmed by whole-script
  read; the 26+8 split audited honest (one computed check conservatively labeled
  guard — conservative-direction only).
- **Classification completeness independently re-derived and ATTACKED** with the
  verifier's own routes: Q = 0 by full generic linear solve; P antidiagonal by full
  generic-P solve; S lower-triangular from the −s01² coefficient; commutant = scalars
  by symbolic-moduli coefficient extraction; **the compensation-loophole-closing
  lemma** — the image H-block is EXACTLY −PHP⁻¹ for ANY block-lower-triangular J (R
  cannot compensate), closing a loophole the package's P-necessity step used
  implicitly (now adopted: `ADOPTED_H_block_R_cannot_compensate`, credited).
  Constructive attacks (off-block swap, screen-F₂, identity base, the J² = −I route)
  all fail as they must — no in-class involutive dressing outside the derived family
  was constructible. Sufficiency verified on the MOST generic members of both
  branches.
- **The three my-harness-was-wrong reversals — recorded as CONFIRMATIONS:** the
  verifier's own harness initially disagreed in three places (its commutant
  comparison target, and two real-domain solve calls); on inspection all three were
  bugs in the VERIFIER'S script — **the package was right in all three places**.
  41/41 after the verifier fixed its own harness.
- **ε_λ dressing-independence** re-verified on the 16-symbol J (needs only P0+P1, as
  claimed); the L0 transcription mechanism confirmed general (not K-content-bound).
- **Escape witness** J_out = diag(F₂,F₂) confirmed exact, genuinely outside the
  family, λ = 0 — consistent with the λ-kill being inescapable and P2 load-bearing
  for the k_mod kill only. (Minor: the check-22 sign slip found here — A4.)
- **C-signature, fixed loci, T5-cell match, K₄:** charpoly (x−1)²(x+1)² re-derived in
  all four branches in the P⁻¹ form; branch-(a) locus dim 2 with the F-member cell
  matching the banked Route-B T5 swap cell VERBATIM; branch-(b) k10-free dim 3; all
  THREE nontrivial K₄ elements checked — R13∘J non-involutive completes the package's
  two-of-three coverage (now adopted: `ADOPTED_K4_R13_non_involutive`, credited).
- **Falsifier hunts:** F-P3 ONE FIRING = the A1 mis-citation. **F-P1: the one drift
  found points in the CUTTING direction** (the mis-citation made the λ = 0 landing
  sound tie-free — stronger than banked, anti-massive); no harmless-side
  underexploration found (the verifier hunted for a banked source deriving or
  refuting P2 — none exists; J07 banked-open). F-P2/F-P4/F-P5 clean; F-P6 = the A3
  evidence gap, with the verifier's own mutation set supplying the missing evidence:
  wrong-parity, wrong-signature, k10-odd-on-branch-(b), screen-swap-in-class all
  CAUGHT (`V3_catch_*` / `V2f_attack_*`).
- **TP1/07-20 spot-reads:** canon wordings, ε_φ THEORY-cite, f/bh SUPPLIED tags, and
  the 07-20 MULTIPLE_COMPLETIONS record all verified verbatim; "REFINED not
  contradicted" adjudicated accurate.

## 3. Changes made (this amendment pass)

1. **`derive_routeP_seal_parity.py`** —
   - Header amendment banner (A1–A4, scoped; "no pre-amendment computed claim
     changed").
   - **A1:** the `TP4_aF_anchor_landing` detail rewritten to the corrected statement
     (premise-failure ⇒ UNCERTIFIED, not refuted; a_F′ = 0 criterion vs a_F = 0
     value; a_F = 0 background status UNDERIVED; drift direction memorialized) — and
     a NEW zero-residual check `A1_aFprime_vs_aF_distinction` embodying the
     distinction against the banked pairing definitions: P1-4D a_F = 2λ has
     a_F(0) = 0 but a_F′(0) = 2 ≠ 0; P2's a_F ≡ 0 is the criterion's holder;
     P1-triad a_F′(0) = 2 with a_F(0) = 1. JSON `aF_landing` corrected by rerun;
     `amendment` key added to the JSON.
   - **A3/A4 adoptions (7 new substantive checks, all credited to
     `VERIFIER_INDEPENDENT_CHECK.py`):** `ADOPTED_H_block_R_cannot_compensate`
     (← V2b, the loophole-closing lemma), `ADOPTED_catch_wrong_parity_kmod_even`
     (← V3_catch_kmod_even_is_false), `ADOPTED_catch_wrong_C_signature`
     (← V3_catch_wrong_signature_fails), `ADOPTED_catch_k10_odd_on_branch_b`
     (← V3_catch_k10_odd_on_branch_b_fails), `ADOPTED_catch_screen_swap_in_class`
     (← V2f_attack_screen_swap_fails_class), `ADOPTED_K4_R13_non_involutive`
     (← V7_R13_composition_not_involutive), plus the A1 distinction check above.
   - **A4:** check-22 sign fixed in prose AND hardened — the off-triangular entry is
     now checked as an exact equality (F₂ K adj F₂)[0,1] = −k10;
     `TC_family_assembly` restated per-branch (branch (a): 3 continuous parameters;
     branch (b): 4); the ledger's Lorentz row now carries the η-readout stamp (the
     banked 07-20 null-coordinate O(1,1) caveat) and an AMENDMENT stamp row was
     appended to the ledger.
2. **`EXACT_DERIVATION.md`** — header counts (41/41 = 33 substantive + 8 guards) +
   amendment banner; TP2 item 4 η-readout stamp; TP2 family verdict per-branch
   counts; K₄-honesty paragraph completed (R13 leg, credited); the TP4
   anchored-pairing bullet rewritten per A1+A2 (the corrected bifurcation:
   UNCERTIFIED vs INTACT, never ABSENT); falsifier record updated — F-P3 ONE FIRING
   memorialized WITH ITS DIRECTION (cutting-side inflation; EIGHTH catch of the named
   scope class per this package's prereg watch — the memorial's original "sixth" was
   itself a closure-caught ordinal drift, harmonized here; first verified
   anti-massive-direction catch), F-P1
   memorial added, F-P6 catch-proof sentence substantiated by the adopted checks;
   Limits gain (vi) the η-readout caveat and (vii) the A1-corrected landing scope.
3. **`DRESSING_CLASSIFICATION_LEDGER.tsv`** — regenerated by rerun: Lorentz row
   η-readout-stamped; amendment stamp row appended.
4. **`DECISION_SURFACE_UPDATE.md`** — header amendment note; the D1
   pairing-bifurcation echo restated in the A1-corrected form (the verifier found D1
   itself clean; the echo now carries the corrected language explicitly).
5. **`CORRECTION_LAYER.md`** (this file) + **`AUDIT_REPORT.md`** (owed by prereg §2
   deliverables / §5 steps 4–5) written.
6. **Rerun record:** `python3 derive_routeP_seal_parity.py` → **41/41, exit 0 = 33
   substantive zero-residual exact-SymPy checks + 8 citation/assembly guards** (the
   34 pre-amendment checks all surviving — three detail strings restated per
   A1/A4, check-22 strengthened to an exact equality, no other computation touched —
   plus the A1 distinction check and the 6 adopted verifier legs), < 2 s wall,
   single CPU process. **Three consecutive runs byte-identical** (stdout AND JSON AND
   TSV): stdout sha256 04530643c7b583c38a7f1b88cc60ac71508004aefcc36831bab97538c9c8b764,
   JSON sha256 1cf916c9152c26cfe575fe0ccd51819c3fee0d7da7b0207f91448970005e0be7 —
   determinism reconfirmed post-amendment. `DERIVATION_STDOUT.txt`,
   `routeP_results.json`, `DRESSING_CLASSIFICATION_LEDGER.tsv` regenerated by rerun.
   Exact SymPy only (no floats, no numeric solvers, no randomness, no network, no
   GPU).

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The outcome-class assignment — OP3 (mixed per-sector)** — untouched.
- **The dressing-family classification and its COMPLETENESS** — J =
  [[antidiag(p,1/p),0],[R,S]] on its stated conditions (class-preservation + J²
  scalar + realness): verifier-re-derived with its own routes and constructive
  attacks; the loophole-closing lemma STRENGTHENS its grounding without moving it.
- **ε_λ = −1 DERIVED, dressing-INDEPENDENT** (needs only P0+P1) — untouched.
- **The P2-conditional ε_kmod = −1** (family-uniform) WITH its chart-escape witness
  (J_out = diag(F₂,F₂); P2 load-bearing) — untouched.
- **The C-signature theorem** (charpoly (x−1)²(x+1)² in every branch; exactly 2 odd +
  2 even, family-uniform; basis supplied) — untouched.
- **The fixed loci and the T5-cell match** (branch (a) K = 0 dim 2 with the F-member
  cell = the banked Route-B T5 swap cell; branch (b) k10-free dim 3) — untouched.
- **The constants-pinning consequence ITSELF** — constant census (BASE) under
  P0+P1+P2: the λ and k_mod dials parity-killed (forced to 0, fold-inadmissible
  constant directions); the fold-quotient no-λ-carrier statement; the field-census
  no-collapse reading; the T4/E07-axis and KMOD0-stratum landings — untouched. ONLY
  its PAIRING-side certificate language was corrected (A1): what the landing means
  for the banked certificate is premise-failure/UNCERTIFIED, never
  "divergence ABSENT".
- **The V5 adjudication** (F = family member, premise NOT forced), **the K₄-honesty
  claim** (now completed, not changed), **the 07-20 REFINED-not-contradicted
  transport**, **the per-sector verdict table (TP3)**, **the decision surface D1–D3
  with no recommendation**, and **the prereg ceiling** (no parity imposed, no census
  adopted, no massive-branch verdict language) — all unchanged.

## Closure residue (applied by the driver, 2026-07-29)

The AMENDMENT CLOSURE found one prose-only defect: the memorial ordinal ("sixth catch")
contradicted this package's own frozen prereg ("EIGHTH-catch watch") — corpus ordinals had
drifted across packages. Harmonized to EIGHTH at all three sites with the drift noted; the
AUDIT_REPORT's unverified universal ("every prior catch inflated toward the massive-keeping
picture") softened to the verified statement (catches have now landed in both directions;
each prior catch's direction lives in its own package record). Closure statement: with this
line fixed, closure is complete on all four duties.
