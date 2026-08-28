# G287 evidence gates

| Gate | Status | Evidence |
|---|---|---|
| Discovery timing disclosed | PASS | `PREREGISTRATION.md` |
| Exhaustive bounded dependency census | PASS | 22/22 rows mechanically resolved to sealed markers |
| Exact production derivation | PASS | `DERIVATION_RESULT.json` |
| Implementation-distinct verification | PASS | `INDEPENDENT_VERIFICATION.json` |
| Hostile semantic catches | PASS | `CATCH_PROOF_RESULT.json`, 6/6 executable mutants |
| Repair hostile probes | PASS | `REPAIR_CATCH_PROOF_RESULT.json`, 5/5 regressions rejected |
| Aggregate all-command replay | PASS | builders, sealed replay, manifests, and exact artifacts |
| Frozen source hashes | PASS | `SOURCE_MANIFEST.tsv`, 23 rows |
| Premise/type audit | PASS | `PREMISE_LEDGER.tsv` |
| External adversarial review | ACCEPT_WITH_REPAIRS | bounded science retained; R1--R3 implemented |
| Repair-only external follow-up | OPEN | corrected intake not yet transmitted |

The scientific result is externally accepted with evidence repairs implemented. It remains
`VERIFIED_WITH_CAVEATS` until the repair-only follow-up closes R1--R3. The initial MAP discovery
means this package must not claim outcome-blind preregistration of the core distinction.
