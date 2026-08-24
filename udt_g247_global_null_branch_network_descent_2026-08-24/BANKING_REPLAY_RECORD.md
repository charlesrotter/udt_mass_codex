# G247 banking replay record

Date: 2026-08-24

This record is completed only after the integration checks are run.

Required commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 udt_g247_global_null_branch_network_descent_2026-08-24/verify_package.py
python3 verify_current_scientific_premises.py
pytest -q
git diff --check
```

Expected G247 evidence:

- production: 2,048 cases and 20,499 assertions;
- independent: 5,000 cases and 55,010 assertions;
- hostile controls: 16/16 caught;
- external landing: `G247_ACCEPTED_WITH_STATED_BOUNDS`;
- registry: 230 exact current rows, with the manifest's pre-G247 registry digest reconstructed only
  by removing the single G247 row.

Final observed results are appended after successful replay.

## Observed result

- G247 package replay: `PASS`; all 13 registered checks true.
- Current-premise verifier: `PASS`; 230 exact rows and G247 extended guards accepted.
- Repository tests: `152 passed, 1 xfailed` (the existing bounded matter-sector habit-pin xfail).
- Diff whitespace/error audit: `PASS`.
