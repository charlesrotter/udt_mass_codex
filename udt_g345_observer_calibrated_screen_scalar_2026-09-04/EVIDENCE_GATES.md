# G345 evidence gates

Date: 2026-09-04

| Gate | Status | Evidence |
|---|---|---|
| Preregistered before outcomes | PASS | commit `d22f1bdb`; `PREREGISTRATION.md` |
| Bounded domain complete | PASS | analytic positivity plus every endpoint order, mixed/principal direction, affine/reference/screen gauge, and per-lift classification |
| Production replay | PASS | `DERIVATION_RESULT.json`: `9824/9824` |
| Independent implementation | PASS | `INDEPENDENT_VERIFICATION.json`: `4360/4360` |
| Hostile mutations | PASS | `CATCH_PROOF_RESULT.json`: `17/17` |
| First execution preserved | PASS | `PREREGISTRATION_EXECUTION_NOTE.md` |
| Premise audit | PASS | `PREMISE_LEDGER.tsv`; no imported transfer law |
| Fresh external adversarial review | PASS | 29 payloads authenticated; formulas independently reconstructed; bounded result accepted |
| Final aggregate | PASS | `19/19`, including exact external return and transmission provenance |
| Repository integration | PASS | 328-row premise verifier; 220 tests passed and 1 pre-existing xfail |

The current grade is `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`. The reviewer found no high-,
medium-, or blocking low-severity defect. Its three non-blocking verifier-quality caveats remain in
`EXTERNAL_REVIEW_RESPONSE.md`; no scientific canon claim is made.
