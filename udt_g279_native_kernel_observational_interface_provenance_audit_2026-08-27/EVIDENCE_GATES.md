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
| Repository tests | BLOCKED_MECHANICAL | 180 pass, 1 known xfail; `LIVE.md` exceeds word cap |
| Fresh blind adversarial review | ACCEPT_WITH_REPAIRS | all 57 payloads and six replays verified; landing retained |
| R1/R2 repair-only follow-up | PENDING | corrected sealed intake and explicit user authorization required |

Current grade: `EXTERNAL_ACCEPT_WITH_REPAIRS__R1_R2_IMPLEMENTED_AWAITING_FOLLOWUP`.

No final positive provenance verdict is banked until the pending repair-only and mechanical gates
close.
