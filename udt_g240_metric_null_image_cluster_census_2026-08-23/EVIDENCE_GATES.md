# G240 evidence gates

| Gate | Status | Evidence |
|---|---|---|
| preregistered before outcome | PASS | commit `7e08dc15` |
| bounded/full declared space | PASS WITH CAVEAT | all branches on locally finite proper regular relation; critical/infinite strata open |
| exact production derivation | PASS | `DERIVATION_RESULT.json` |
| independent implementation | PASS | 2,003 exact enumerations in `INDEPENDENT_VERIFICATION.json` |
| hostile catch proof | PASS | 15/15 in `CATCH_PROOF_RESULT.json` |
| premise/provenance audit | PASS LOCALLY | 11 frozen sources; 222-row repository verifier PASS |
| no-shortcuts suite | PASS | 144 passed, 1 expected xfail |
| fresh adversarial review | SCIENCE RETAINED; REPAIR REQUIRED | external `gpt-5.4` retained the bounded theorem and found one sealed-layout defect |
| repair preregistration | PASS | commit `44a01bd2`; R1 frozen before implementation |
| repository no-write replay after R1 | PASS AT FROZEN 222-ROW STATE | verifier recorded `REPOSITORY_ROOT`; live 223-row integration intentionally changes that frozen source hash |
| sealed as-delivered replay after R1 | EXTERNALLY ACCEPTED | reviewer obtained `PASS` with `SEALED_SOURCES_ROOT`; no mirroring or rearrangement |
| sealed missing-sources negative gate | EXTERNALLY ACCEPTED | reviewer reproduced the registered fail-closed assertion without `sources/` |
| repair-only follow-up | ACCEPTED | `G240_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`; no remaining R1 defect |
| live banking integration | PASS SEPARATELY | 223-row global verifier and tests pass; frozen 222-row G240 manifest is not refreshed |
| premise audit complete | PASS WITH DECLARED CEILING | reviewer confirmed the all-image query remains `CHOSE`; physical transfer/detection remains `OPEN` |

Current maximum grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__R1_REPAIR_ACCEPTED`.
