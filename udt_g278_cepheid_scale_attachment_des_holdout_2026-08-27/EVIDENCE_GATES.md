# G278 evidence gates

| gate | status | evidence |
|---|---|---|
| outcome-blind preregistration | PASS | commit `8366e111`, pushed before production |
| bounded space declared | PASS | four frozen G236 resolutions, exact calibrator and DES masks |
| load-bearing independent verification | PASS | `INDEPENDENT_VERIFICATION.json`, 10/10 checks |
| hostile non-vacuity controls | PASS | `CATCH_PROOF_RESULT.json`, 8/8 checks |
| premise audit | PASS | 260-row verifier passed before production |
| source integrity | PASS | 10/10 `SOURCE_MANIFEST.tsv` hashes |
| G236 regression | PASS | maximum coefficient error `6.49e-13` |
| calibrator consistency | PASS | `57.1347 / 76`, ceiling `137.6441` |
| calibrator subset robustness | PASS | 46/46; maximum `3.1115 sigma` |
| covariance serialization | PASS | maximum `3.57e-8 mag`, tolerance `1e-4 mag` |
| resolution stability | **FAIL** | `60.4054`, ceiling `15.2474` |
| outcome-informed curve-localization diagnostic | PASS AS DIAGNOSTIC | sensitivity persists outside boundary bands; original landing retained |
| DES no-retuning adequacy | PASS | `1434.5793 / 1623`, ceiling `1907.8684` |
| fresh external adversarial review | PENDING | sealed intake not yet authorized/reviewed |

Verdict ceiling: `INTERNALLY_VERIFIED LEAD WITH RESOLUTION CAVEAT` until fresh external review.
