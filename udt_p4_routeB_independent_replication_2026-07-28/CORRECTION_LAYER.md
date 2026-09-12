# CORRECTION LAYER — verifier-required amendments (applied 2026-07-28)

Blind adversarial verifier (agent a9a44fb516420bd38, 2026-07-28) returned
**PASS_WITH_CORRECTIONS**. Both required corrections and all actionable notes are
applied IN PLACE (edits visible in git per repo discipline); this layer records each.

## CR-1 (F-D quantifier catch — REQUIRED, applied)

Three statements said the E07/k direction is "UNCONSTRAINED by every
supplied-reduction/banked gate", and the ledger row E07/C3 was stamped UNCONSTRAINED.
Bank-accurate form: the banked 07-27 full-class solves show each of the three
conditional gates (supplied SO(3) → K=diag(+1,+1); supplied SO+(1,2) → K=diag(−1,−1);
supplied reciprocal swap → K=0) **conditionally forces k = 0** under its own supplied
structure. The TRUE narrow claim (verifier-adjudicated against all four cited banked
records): **no banked gate pins k ≠ 0; k is unconstrained only ABSENT supplied
structure.** Applied at: EXACT_DERIVATION.md §4 (post-pin-table paragraph), §7 L2
re-tag, T5 table E07 row; STRATUM_SURVIVAL_LEDGER.tsv row E07/C3 (status
UNCONSTRAINED → CONDITIONAL). No survival verdict or re-tag changes: L2 remains
MODULUS-CARRIED (the k=0 forcings are conditional, cited, and were already the T5
content).

## CR-2 (preregistration vocabulary — REQUIRED, recorded)

Ledger rows diagonal-subfamily/C1 and E07-line/C1 use status
`NOT_WELL_POSED_POINTWISE`, which is outside the frozen §2 status vocabulary
(FORCED_OUT | CONDITIONAL | SURVIVES_WITH_MODULI | UNCONSTRAINED). Disposition:
**explicit vocabulary extension recorded here** rather than a silent re-map — the T1
algebra discovered a status the frozen list did not anticipate (a stratum condition
that is not a covariantly well-posed condition at all, only a chart section /
so(2)-invariant pair). Re-mapping to SURVIVES_WITH_MODULI would misreport a typing
fact as a survival fact. The preregistration file itself is UNEDITED (no-retune rule);
the extension is declared, scoped to C1 typing rows only, and flagged for Charles.

## Notes (applied or recorded)

- **N-3 (quantifier, applied):** "det-one is the unique fully covariant stratum
  condition" now carries its quantifier — unique AMONG the package's listed
  stratum/chart conditions; other fully covariant functions on the class exist
  (verifier: δ(det X) = 0, det X = −ad). EXACT_DERIVATION.md §7 (iii).
- **N-4 (scope, recorded):** the so(2)-fixed-set = isotropic-line statement is
  triangular-chart-scoped; on the chart-free full-K class the fixed set is the
  2-modulus family {a=d, k21=−b, C=0} (verifier-computed). The in-text sentence was
  already correctly scoped; this note stamps the T5 SO(2) column with the same chart
  scope.
- **N-5 (text defect, applied):** garbled TSV cell E03/C2 repaired with the exact
  E03-internal total-φ=0 witness (det-one members (a,d)=(1,−1),(−1,1); verifier check
  `E3_E03_internal_witness`).
- **N-6 (wording, applied):** "NOT-TRANSLATABLE off a=d" → "NOT-TRANSLATED (no banked
  formula)" — forecloses the impossibility misreading.
- **N-7 (recorded):** `T4_conditional_pins_on_isotropic_line` is algebraically
  trivial; its load-bearing content is the bank audit, which the verifier adjudicated
  separately (narrow claim TRUE).

Verifier deliverables preserved in-package: VERIFIER_REPORT.md, INDEPENDENT_REDERIVE.py
(44 independent checks, all pass), INDEPENDENT_STDOUT.txt. Byte-identical production
rerun confirmed (47/47, exit 0, deterministic ×2).
