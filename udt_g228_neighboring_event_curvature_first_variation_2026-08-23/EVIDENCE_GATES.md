# G228 evidence gates

Date: 2026-08-23

| Gate | Status | Evidence |
|---|---|---|
| Pre-outcome preregistration | PASS | commit `b54f4c51`; no production/independent scripts existed in that commit |
| Whole bounded subset census | PASS | all 15 nonempty subsets of `(k,l,s1,s2)` in `SUBSET_CENSUS.tsv` |
| Exact production | PASS | `DERIVATION_RESULT.json`, `SYZYGY_BASIS.json` |
| Independent load-bearing replay | PASS | `INDEPENDENT_VERIFICATION.json`; separate `Fraction` builder and row reducer |
| Orthogonal full-index anchor | PASS | `FULL_INDEX_ANCHOR.json`; 84 raw slots, ranks 4/24, module dimension 60 |
| Hostile structural catches | PASS | `HOSTILE_CATCH_RESULT.json`, 11/11 |
| Saved-artifact replay | PASS | `VERIFICATION_RESULT.json`, 13/13 |
| Fresh adversarial review | PASS_AFTER_REPAIRS | three-agent review and repair-only follow-up |
| Premise audit | PASS | `PREMISE_LEDGER.tsv`; no value-generation promotion |

Maximum current grade:

```text
DERIVED_CONDITIONAL__PREREGISTERED__EXACT_PRODUCTION_AND_TWO_REPRESENTATION_REPLAY
__FRESH_MULTI_AGENT_ADVERSARIAL_REVIEWED__REPAIRS_VERIFIED
```

The package does not generate curvature values, a metric 3-jet, a smooth metric realization, or a
physical history. The evidence gates certify necessary local algebraic compatibility only.
