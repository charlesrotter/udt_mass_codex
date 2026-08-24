# G248 banking replay record

Date: 2026-08-24

This record is completed only after the integration checks are run.

Required commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/verify_package.py
python3 verify_current_scientific_premises.py
pytest -q
git diff --check
```

Expected G248 evidence:

- production: 4,096 cases and 307,205 assertions;
- independent: 10,000 cases and 540,002 assertions;
- hostile controls: 18/18 caught;
- external landing: `G248_ACCEPTED_WITH_STATED_BOUNDS`;
- registry: 231 exact current rows, with the manifest's pre-G248 registry digest reconstructed from
  the rows strictly beneath the unique G248 row.

Final observed results are appended after successful replay.

## Observed result

- G248 package replay: `PASS`; all 14 registered checks true.
- Current-premise verifier: `PASS`; 231 exact rows and G248 extended guards accepted.
- Repository tests: `153 passed, 1 xfailed` (the existing bounded matter-sector habit-pin xfail).
- Diff whitespace/error audit: `PASS`.
