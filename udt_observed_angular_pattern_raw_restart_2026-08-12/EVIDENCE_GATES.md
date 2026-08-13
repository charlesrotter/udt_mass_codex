# R0 evidence gates

Date: 2026-08-12  
Object: preregistration and frozen data intake, not a scientific outcome

1. **Preregistered:** `YES`. The whole question, exact data universe, grids, weight ensemble,
   estimator, controls, exclusions, failure classes, and conclusion ceiling were written before any
   galaxy pair count or pattern output.
2. **Full space or bounded scope justified:** `YES_FOR_R0`. All eight files in the declared BOSS
   LOWZ/CMASS North/South pre-reconstruction input universe are frozen. This is not a DESI, eBOSS,
   full-survey, or physical-cosmology claim.
3. **Independently verified on the load-bearing premise:** `YES_FOR_INPUT_PROVENANCE`. Direct
   `sha256sum` results were frozen first; the separate standard-library verifier then reproduced all
   eight hashes plus byte, row, and schema checks. No scientific pattern exists to verify.
4. **Every premise audited:** `YES_FOR_R0`. `PREMISE_LEDGER.tsv` records 18 choices/statuses and
   `FALSIFICATION_CONTRACT.tsv` records 14 gates.

Machine checks:

```text
PASS: R0 preregistration (18 premises, 14 gates, 8 inputs; full hashes; no outcome artifacts)
103 passed, 1 xfailed
```

Grade: `PREREGISTERED__INPUT_PROVENANCE_VERIFIED__NO_PATTERN_EVALUATED`.

