# G162 run record

Date: 2026-08-18
Working branch: `grok`
Preregistered source snapshot: `ee261b38`
Preregistration commit: `0358b471`
Second-repair harness commit: `0060721c`
Crosswalk correction commit: `5a9cb8e9`
Density/domain repair commit: `837542d9`
Dual-domain verifier repair commit: `b7039e4f`

Commands:

```bash
python3 udt_g162_lambda_dependence_frontier_census_2026-08-18/derive_lambda_census.py
python3 udt_g162_lambda_dependence_frontier_census_2026-08-18/verify_lambda_census_independent.py
python3 udt_g162_lambda_dependence_frontier_census_2026-08-18/run_catch_proofs.py
python3 udt_g162_lambda_dependence_frontier_census_2026-08-18/verify_package.py
```

The production implementation uses SymPy exact algebra. The independent replay uses only stdlib
`Fraction` arithmetic and an independently implemented dual-number first jet. No observational
data, fit, long solve, GPU, timeout, or protected package was used.

The initial execution found D15 unmatched by the five preregistered types and is recorded as
`DEPENDENCY_CENSUS_TYPE_FAILURE`. The first repair failed fresh review. The second repair corrects
only the six defects in `FIRST_REPAIR_FAILURE_RECORD.json`; its preregistration and source changes
are banked before the final displayed rerun.

`FINAL_SCALE_TYPING_REPAIR.md` records the last reviewer-caught density and boost-domain
distinctions. That source correction is also banked before the last rerun.

`FINAL_REPAIR_EXECUTION_NOTE.md` records the dual-domain guard type stop; its one-line verifier
repair was banked before the successful final replay.

Final repository gates:

```text
python3 verify_current_scientific_premises.py
PASS: G162-extended premise guards; PASS: 149-row premise registry ...

pytest -q
121 passed, 1 xfailed in 1.76s

python3 udt_g162_lambda_dependence_frontier_census_2026-08-18/verify_package.py
status: PASS; 14 exact checks; 900 independent trials per family; 22 census rows; 12 catches
```
