# CORRECTION LAYER — P4 Route A Stage 3 (Slice 1) (amendments A1–A4, per VERIFIER_REPORT.md)

Date: 2026-07-29. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`).
A1 is SUBSTANTIVE: one claim strand — the anchored-log forcing quantifier — was
REFUTED AS PHRASED by an in-family counter-construction (the verifier's V10b); the
computations behind it were correct and the corrected statement is strictly narrower
(amendment, not demolition). A2 memorializes both F-S3-class catches in the new
`AUDIT_REPORT.md`; A3 adds the bare-φ/anchored-log reconciliation line; A4 is a
check-split honesty reclassification. Nothing here changes the outcome class, the
partition structure, any witness, the transversality corners, the boundary census,
the typing tables, the 30-cell map, or any stamp/flag.

## 1. Original claims (as they stood pre-amendment)

- **The anchored-log forcing** (script details `TC1_H4_witness_lambda_slot_contains_log`
  ~L395 and the JSON `pairing_dependence_map` entry ~L1140; JSON both occurrences;
  stdout; `EXACT_DERIVATION.md` §1.2.6; echoed in `SLICE2_SURFACE.md` §2 LE×KMOD0):
  "under the λ-dependent P1 volumes the LE cell's λ-slot carries forced log(c_E/Q)
  dependence **whenever the field sector is nonzero**."
- **The W2 witness** (corrected DURING derivation — a self-catch): an earlier draft
  claimed "W2 (the field sector alone) is LE under P1"; the shipped package already
  carried the corrected full-tuple form (W2′ = field sector + the λ-slot 2p0·L̃₀),
  but the catch itself was memorialized nowhere (A2).
- **Headline count**: "49/49 = 33 substantive + 16 citation guards", with three
  guard-grade checks counted substantive (A4).
- **No bare-φ reconciliation note** where the anchored-log legality is stated (A3;
  the verifier's F-S4 tension flag, reconciled not broken).

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifacts
preserved in `VERIFIER_INDEPENDENT_CHECK.py`, **29/29 checks, exit 0**)

- **A1 (the refutation — COMPUTATIONS CORRECT, QUANTIFIER REFUTED).** Counterexample
  V10b, built inside the package's own banked alphabet class: L̃ = e^{−2λp0}·L̃₀
  (anchored, formal-in-λ, Q-smooth) generates S = W_F·L̃ = L̃₀ — λ-INDEPENDENT — whose
  member **R_a = e^{−2λp0}(p2, f2, h2), ALL moduli slots ZERO**, satisfies every LE
  condition under P1-4D ((i)–(iii), H4 for every modulus, H5) with a NONZERO,
  genuinely λ- and p0-dependent field sector, a ZERO λ-slot, and NO log anywhere.
  The TRUE statement (verifier-derived V10a/V10c, adopted exactly): the λ-row reads
  E_a(W_M R_λ) = ∂λ(W_F R_a) = W_F[∂λR_a + a_F′·p0·R_a]; **the λ-slot is forced
  nonzero — log-carrying via the a_F′·p0 term — IFF ∂λ(W_F·R_a) ≢ 0 for some field
  slot a — in particular for every λ-INDEPENDENT nonzero field sector** (where the
  forcing is real and the generated witness R_λ = 2p0·L̃₀ stands). Exactly the F-S3
  error class: a "whenever/all" quantifier missing its exact condition. The forced-
  structure framing (not an obstruction, not a selection) was correct throughout.
- **Reproductions (attacked, all REPRODUCED):** the condition system = Fréchet
  self-adjointness with necessity on the generic EL image (V1, non-vacuity probe
  V1b); the P1-4D weight-cancellation and exact condition-(ii) shift (V2); all four
  witnesses W1/W2′/W3/ω with their defects and blindness-locus scopes (V3); the W2
  self-corrected statement verified CORRECT and COMPLETE (the field-only tuple fails
  exactly H4(λ); the full W2′ needs only the λ-slot); **the intertwining bijection**
  (e^{±a_F p0} K₄-inert, exactly invertible, sends the P1 partition onto the P2
  partition — isomorphic-but-distinct confirmed, V4); **W3 branch-independence
  attacked and SURVIVED** (Hi1 = 2e^{a_F p0} for SYMBOLIC a_F, nowhere zero; no
  moduli-slot rescue possible — a genuine proof); the four-corner transversality
  with correct scope (V5, incl. the exact Stage-2 identity match); the boundary
  census by independent by-parts (V6/V7/V11: N=2 self-pairable, N=4 third-jet
  momenta, parity-halving, P3 interior-defect inheritance with a different
  variation pair, anchored wall rule); TC2/TC4 typing (V8/V9). Contract-first
  verified in git (dbc114f); byte-identical rerun 49/49.
- **A2:** both F-S3 catches (the derivation self-catch AND the verifier catch) owed
  a falsifier-record memorial in the (then-unwritten) `AUDIT_REPORT.md`.
- **A3 (recommended):** one-line reconciliation of Stage-2's "bare φ excluded" with
  the anchored-depth-log legality (the supplied-c_E anchored reading).
- **A4 (minor):** `TC4_torsion_period_vacuous`, `TC1_no_empty_adjudicated_cell`,
  `TC2_kmod0_identity_is_row_dependency` are guard-grade in computational content;
  honest substantive count ~30/33.

## 3. Changes made (this amendment pass)

1. **`derive_routeA_stage3.py`** —
   - **A1 restatements** at both script occurrences: the
     `TC1_H4_witness_lambda_slot_contains_log` detail (~L395) and the JSON
     `pairing_dependence_map` anchored-log entry (~L1140) now carry the exact iff
     condition, the counterexample citation, and scope stamps; the JSON
     `field_moduli_H4` line and the ledger LE-row H4 conditions text carry the iff;
     the `TC1_W2_LE_P1_NV_P2` detail ties the field-only H4(λ) failure to the A1 iff
     condition. Docstring amendment banner.
   - **3 new zero-residual A1 checks** (all substantive; the verifier's computation
     adopted): `A1_V10b_counterexample_LE_zero_lambda_slot` (the full V10b member:
     S = W_F·L̃ = L̃₀ exactly; (i)–(iii) field-field via the package's own Helmholtz
     machinery; H4 for every modulus with zero slots; nonzero λ- and p0-dependent
     field sector = e^{−2λp0}(p2,f2,h2); zero λ-slot),
     `A1_anchored_log_iff_condition` (with a zero λ-slot the H4(λ) residual is
     EXACTLY ∂λ(W_F R_a) = W_F[∂λR_a + a_F′p0R_a], symbolic a_F; both directions
     instantiated — counterexample side all-zero, W1's p-row nonzero),
     `A1_lambda_independent_sector_forcing_real` (the λ-independent sub-case:
     ∂λ(W_F R_p) = 2p0·W_F·R_p ≠ 0 with the explicit log factor; R_λ = 2p0L̃₀
     stands).
   - **A4 reclassification**: the three named checks added to the guard set (kind
     relabel ONLY — their math, pass conditions, and detail strings are unchanged);
     `check_split.note` records the reclassification.
   - JSON gains `amendments` (A1/A4); the `falsifier_record["F-S3"]` entry now
     memorializes both catches (the A2 record also lives in `AUDIT_REPORT.md`).
2. **`EXACT_DERIVATION.md`** — header (52/52 = 33 substantive + 19 guards; amendment
   banner); §1.2.3 W2′ tie to the iff condition; **§1.2.6 fully restated** (the
   corrected iff statement adopted verbatim, the V10b counterexample, the iff-check
   and sub-case check names, the A3 bare-φ reconciliation line, scope stamps); §6
   F-S3 (both catches recorded) and F-S5 (new counts).
3. **`SLICE2_SURFACE.md`** — the §2 LE×KMOD0 echo restated with the A1-corrected
   scope (the iff condition carried into the candidate-declaration duty).
4. **`AUDIT_REPORT.md`** (NEW, owed by contract §6) — grade, TC1–TC6 table, the
   joint-map summary, the corrected anchored-log statement, the A2 falsifier
   memorial with the method observation, limits that travel, verifier record,
   Slice-2 pointer.
5. **Regenerated deterministically by rerun:** `routeA_stage3_results.json`,
   `GATE_CUT_LEDGER.tsv` (34 rows; only the LE-rows' H4 conditions text changed),
   `DERIVATION_STDOUT.txt`.
6. **Rerun record:** `python3 derive_routeA_stage3.py` → **52/52, exit 0 = 33
   substantive zero-residual checks + 19 citation guards** (49 pre-amendment checks
   all surviving with math and pass conditions unchanged — 2 substantive detail
   strings amended, 3 kind-relabels — plus the 3 new `A1_*` checks), ~61 s, single
   CPU process. Three consecutive runs byte-identical: JSON sha256
   a0371b62acbaf3f82683bebd3c859fb35cde4a6ff59a5113229666c1b2eb3ccd, ledger sha256
   652535b3b706dfd3cca39217459e1247103f7c8ac15194ce41e8ab0729a1eb8a, stdout sha256
   4f497a7181f2fe4d5fdb77c11ad403389b15df9c3d6d7b2ed392a9009fb7b7e6 — determinism
   reconfirmed post-amendment.

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The outcome class** — OS1 (the joint gate-cut map is a populated partition; OS2/
  OS3 not triggered) — untouched; the refuted strand was descriptive prose/detail
  text inside TC1, not a partition computation.
- **The partition structure and ALL witnesses** — the condition system
  ((i)–(iii)/H4/H5), the pairing-dependence map's other five entries, W1/W2′/W3/ω
  with their cells, defects, and blindness-locus scopes, the intertwining bijection,
  the W3 branch-independence proof: all byte-equivalent in math (verifier-reproduced
  29/29).
- **The transversality corners** — the four-corner (G3-cell × identity-cut) table on
  KMOD0 under P2, its witnesses and scope stamps (verifier-reproduced V5).
- **The boundary census results and scopes** — N=2 self-pairable at jet ≤ 2, N=4
  structurally unable (typed extension REQUIRED, never "excluded"), parity-halving,
  the supplied-parity tags, the anchored wall rule, P3 bulk inheritance, corners
  typed-only (verifier-reproduced V6/V7/V11).
- **TC2/TC4 typing** — DETERMINED/CONSTRAINED-balanced/CENSUS-REQUIRED per stratum;
  the torsion-vacuity statement and its closed-form/torsion-cycle scope; the
  completion-data and J07/J11 obligation types (A4 relabeled the KIND of two of
  these checks, not their content).
- **The 30-cell map and its CENSUS-REQUIRED rows** — 20 adjudicated witness-nonempty
  composite cells + 10 RES-CNEQ0 CENSUS-REQUIRED (resonance rule), the 4 observation
  rows, all open-fork and Slice-2 columns (the only ledger delta = the LE-rows' H4
  conditions text now carries the iff).
- **The F-S7 flags** — carried on every J07/J11-typed row and both ledger G6 texts;
  no banked G6 claim rests on the twisted-H¹ MODEL-KNOWLEDGE row.
- **The prereg contract, the ceiling, and the F-S1/F-S2/F-S6 discipline** — no member
  selected, no pairing adopted, no solution-dependent claim, no physics; the
  maximum-conclusion ceiling stands.
