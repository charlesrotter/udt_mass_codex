# G243 evidence gates

| gate | status | evidence |
|---|---|---|
| preregistered | PASS | G243 census at `8d8fdbda`; stability repair at `b5f38cd2` |
| bounded scope | PASS | five basis counts, 97 alpha values, fixed common SNe interval |
| source integrity | PASS | eight frozen hashes; exact row counts and de-overlap |
| independent selected candidate | PASS | same `K=48`, `alpha=0.1`; coefficient max difference `1.33e-12` |
| all-candidate GCV | PASS | all 485 rows within `1e-7` |
| all-candidate raw chi-square | FAIL | 29 rows exceed `1e-7`; maximum `9.17e-6` |
| monotonicity | CHARACTERIZED, NOT IMPOSED | four positive intervals; minimum `s'=-1.0187...` |
| hostile catches | PASS | 17 semantic/numerical catches |
| outcome closure | PASS | angular and BOSS outcomes closed and unused |
| fresh adversarial review | PASS | `gpt-5.4`: `G243_NO_FREEZE_ACCEPTED__LOCAL_TURNING_CANDIDATE_RETAINED`; no repairs |

The controlling grade is `NO_FREEZE`. The local candidate is `OBSERVED`, not a certified physical
history.
