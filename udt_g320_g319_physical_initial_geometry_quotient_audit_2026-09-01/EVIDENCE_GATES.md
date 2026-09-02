# G320 evidence gates

Date: 2026-09-01

| Gate | Status | Evidence |
|---|---|---|
| Preregistered | `PASS` | commit `a00e8ed3` precedes every outcome script and generated result |
| Full space or bounded scope justified | `PASS_BOUNDED` | exact G319 slice and all dropped sectors are explicit in `MAP.md` and `COMPLETENESS_MAP.md` |
| Independently verified on load-bearing premise | `PASS_INTERNAL` | `verify_independent.py` rebuilds Ricci by index loops and uses different profiles/modes/grid/J0 |
| Every premise audited | `PASS_INTERNAL` | `PREMISE_LEDGER.tsv`; current 302-row registry verifier required |
| Hostile false-pass audit | `PASS` | 26/26 registered mutations caught |
| Aggregate package replay | `PASS_PENDING_EXTERNAL_REVIEW` | all four registered commands and package guards pass |
| Repository regression | `PASS` | 215 passed, one known documented xfail |
| Fresh external adversarial review | `PASS` | all 32 payloads authenticated; four replays and five byte-identical outputs; no scientific defect |

Current grade: `EXTERNALLY_ACCEPTED_BOUNDED`.
