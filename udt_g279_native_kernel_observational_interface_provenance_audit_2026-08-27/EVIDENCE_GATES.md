# G279 evidence gates

| Gate | State | Evidence |
|---|---|---|
| Preregistered before source conclusions | PASS | commits `d4f5de04`, `8f79bed1` |
| Exact bounded source universe | PASS | 31-row `SOURCE_MANIFEST.tsv` |
| Founding algebra rederived | PASS | `INDEPENDENT_VERIFICATION.json` |
| Complete-pair-before-readout | PASS | exact block identity and 10,000 random cases |
| Executable dependency cut | PASS | `DEPENDENCY_LEDGER.tsv`, AST inventories |
| Scaffold exclusion | PASS | executable trace plus 14 hostile mutations |
| Import subtraction | PASS | 9 cases in `SUBTRACTION_RESULT.json` |
| Independent implementation | PASS | no production imports or stored results; 109,549 assertions |
| Premise registry | PASS | 260-row verifier |
| Repository tests | BLOCKED_MECHANICAL | 180 pass, 1 known xfail; `LIVE.md` exceeds word cap |
| Fresh blind adversarial review | PENDING | sealed intake and explicit user authorization required |

Current grade: `LOCAL_VERIFIED_AWAITING_EXTERNAL`.

No final positive provenance verdict is banked until the two pending/mechanical gates close.
