# G347 commands

Date: 2026-09-04

No derivation or outcome command was run before this preregistration was banked.

Planned bounded replay commands:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_endpoint_observer_covariance.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_endpoint_observer_covariance_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

The first three commands returned `73924/73924`, `23547/23547`, and `22/22`. The first aggregate
returned `17/19` because two exact documentary phrases did not match across wording/line wrapping.
The recorded wording-only repair changed no formula, script, result JSON, tolerance, alternative,
or maximum conclusion. The repaired aggregate returned `19/19`. Every replay preserved evidence
bytes in no-write mode.

The first authorized external model designation, `gpt-5.4`, was unavailable and stopped before
substantive review. Charles authorized substitution of `gpt-5.6-sol` against the unchanged sealed
intake. The external reviewer authenticated 28 payloads, reproduced the `19/19` aggregate, passed
10,831 independent scratch checks, and returned
`ACCEPT_G347_BOUNDED_ENDPOINT_OBSERVER_COVARIANCE` without required repair.
