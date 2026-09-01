# G319 evidence gates

Date: 2026-09-01

| Gate | Status | Evidence |
|---|---|---|
| Preregistered before outcomes | PASS | commit `5c54d109` pushed before outcome scripts |
| Bounded scope justified | PASS | `MAP.md`, `COMPLETENESS_MAP.md`, `PREMISE_LEDGER.tsv` |
| Exact production derivation | PASS | `derive_ratio_free_family.py`, `DERIVATION_RESULT.json` |
| Implementation-distinct replay | PASS | `verify_independent.py`, `INDEPENDENT_VERIFICATION.json` |
| Direct physical constraints | PASS | independent Christoffel/Ricci and momentum index loops |
| Zero/crossing stratum retained | PASS WITH OPEN GLOBAL CLASSIFICATION | 324 exact compatible germs; no division through `B=0` |
| Hostile mutation catches | PASS | `run_catch_proofs.py`, `CATCH_PROOF_RESULT.json` |
| Premise audit | PASS | all 301 exact current registry rows verified |
| Full repository regression | PASS | 214 passed and one known xfail |
| Fresh external adversarial review | PASS | all 33 payloads authenticated; five replay artifacts byte-identical; bounded landing accepted |

Final bounded grade: `EXTERNALLY_ACCEPTED_BOUNDED`.
