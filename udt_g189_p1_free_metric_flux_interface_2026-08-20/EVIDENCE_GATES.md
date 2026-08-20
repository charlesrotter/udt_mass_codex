# G189 evidence gates

| gate | status | evidence |
|---|---|---|
| initial preregistration | PASS | commit `d9f68684` |
| regular-center correction preregistration | PASS | commit `c3fd11f4` |
| 17 frozen source hashes | PASS | `PRODUCTION_RESULT.json` |
| exact metric/flux/profile algebra | PASS | `derive_p1_free_flux_interface.py` |
| Pantheon+ production replay | PASS | `PRODUCTION_RESULT.json` |
| DES-SN5YR production replay | PASS | `PRODUCTION_RESULT.json` |
| implementation-distinct replay | PASS | `INDEPENDENT_VERIFICATION.json` |
| algebraic mutation catches | 9/9 PASS | `CATCH_PROOF_RESULT.json` |
| semantic/scope guards | 9/9 PASS | `CATCH_PROOF_RESULT.json` |
| no shape fit | PASS | zero shape parameters; one analytic catalog offset |
| P1 absent from candidate | PASS | separate `model_chi`; P1 reference only |
| fresh external adversarial review | `ACCEPTED_WITH_REPAIRS` | `EXTERNAL_REVIEW_RAW.md` |
| host-independent DES source gate | PASS internally | logical `external_data/...` manifest rows |
| production-artifact-independent second replay | PASS internally | production artifact is not read by second implementation |
| repair-only external follow-up | OPEN | fresh repaired intake not yet transmitted |

Maximum current grade:
`EXTERNALLY_ACCEPTED_WITH_REPAIRS__REPAIRS_IMPLEMENTED_AND_INTERNALLY_VERIFIED__FOLLOWUP_OPEN`.
