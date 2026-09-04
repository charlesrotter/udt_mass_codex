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

The exact environment, versions, parameters, counts, errors, and outputs will be recorded in
`RUN_RECORD.md` only after execution. Every command must preserve evidence bytes in no-write mode.
