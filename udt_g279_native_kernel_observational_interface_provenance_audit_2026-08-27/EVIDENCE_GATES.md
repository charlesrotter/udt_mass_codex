# G279 evidence gates

| Gate | State | Evidence |
|---|---|---|
| Preregistered before source conclusions | PASS | commits `d4f5de04`, `8f79bed1` |
| Exact bounded source universe | PASS | 31-row `SOURCE_MANIFEST.tsv` |
| Founding algebra rederived | PASS | `INDEPENDENT_VERIFICATION.json` |
| Complete-pair-before-readout | PASS | exact block identity and 10,000 random cases |
| Executable dependency cut | PASS | `DEPENDENCY_LEDGER.tsv`, AST inventories |
| Scaffold exclusion | PASS | executable trace plus 16 hostile mutations |
| Import subtraction | PASS | 9 cases in `SUBTRACTION_RESULT.json` |
| Independent implementation | PASS | no production imports or stored results; 109,549 assertions |
| Premise registry | PASS | 260-row verifier |
| Repository tests | PASS | 184 passed, 1 known xfail; startup surface within all limits |
| Fresh blind adversarial review | ACCEPT_WITH_REPAIRS | all 57 payloads and six replays verified; landing retained |
| R1/R2 repair-only follow-up | PASS | all 61 payloads and six bit-identical replays verified; no defect |

Current grade: `EXTERNAL_REPAIRS_ACCEPTED__ALL_FOUR_GATES_CLOSED`.

The bounded science and repository mechanics are externally and locally closed. This remains a
source-bounded provenance result, not canonization or observational-scale selection.
