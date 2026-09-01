# G318 evidence gates

Date: 2026-09-01

| Gate | Status | Evidence |
|---|---|---|
| Preregistered before outcomes | PASS | commit `b3130170` |
| Bounded scope justified | PASS | `MAP.md`, `COMPLETENESS_MAP.md`, `PREMISE_LEDGER.tsv` |
| Exact production derivation | PASS | `derive_nonconstant_psi_family.py`, `DERIVATION_RESULT.json` |
| Implementation-distinct replay | PASS | `verify_independent.py`, `INDEPENDENT_VERIFICATION.json` |
| Hostile mutation catches | PASS | `run_catch_proofs.py`, `CATCH_PROOF_RESULT.json` |
| Direct physical constraints | PASS | production and index-loop independent replay |
| Initial Weyl reconstruction | PASS | independent Christoffel/Ricci/covariant-curl replay |
| Premise audit | PASS | 301-row exact registry and current startup guards |
| Full repository regression | PASS | 214 passed, one known xfail |
| Fresh external adversarial review | PASS | all 33 payloads authenticated; replay byte-identical; bounded landing accepted |

Final bounded grade: `EXTERNALLY_ACCEPTED_BOUNDED`.
