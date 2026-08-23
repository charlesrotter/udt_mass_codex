# G237 evidence gates

Date: 2026-08-23

| gate | status | evidence |
|---|---|---|
| preregistered before outcomes | PASS | commit `ad49b9c8` pushed before production |
| bounded scope justified | PASS | common G236 support; static-central query; four inherited grids |
| source hashes frozen | PASS | `SOURCE_MANIFEST.tsv`, `VERIFICATION_RESULT.json` |
| production algebra controls | PASS | `JOINT_STATE_RESULT.json` |
| independent raw-data reconstruction | PASS | `INDEPENDENT_RAW_GLS.json` |
| cross-route agreement | PASS | max theta error `6.3994e-13`; covariance `2.7756e-17`; chi-square `2.4693e-10` |
| raw residual certification | PASS | all four resolutions below preregistered ceilings |
| hostile mutation catches | PASS | `CATCH_PROOF_RESULT.json` |
| premise audit | PASS_WITH_CAVEAT | zero cross-release covariance is chosen, not derived |
| external fresh review | SCIENTIFIC_CORE_ACCEPTED_REPAIR_REQUIRED | `EXTERNAL_REVIEW.md` |
| wording repair | PASS | `LAY_REPORT.md`, `REPAIR_CERTIFICATION.json` |
| self-contained chronology replay | PASS | `CHRONOLOGY_OBJECT_BUNDLE.json`, `CHRONOLOGY_BUNDLE_VERIFICATION.json` |
| command/payload alignment | PASS | `COMMANDS.md`, repaired sealed-intake inventory |
| covariance-label repair | PASS | `INDEPENDENT_RAW_GLS.json`, `REPAIR_CERTIFICATION.json` |
| repair-only external follow-up | PASS | `EXTERNAL_REPAIR_FOLLOWUP.md`; no defects or improvements |

Current maximum grade:

```text
EXTERNALLY_VERIFIED_WITH_CAVEATS__REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_RETAINED
```
