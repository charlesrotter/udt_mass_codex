# G348 commands

Date: 2026-09-04

No derivation or outcome command was run before this preregistration was banked.

Planned bounded replay commands:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_generic_null_screen_area.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_generic_null_screen_area_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

The exact environment, versions, parameters, counts, errors, and outputs will be recorded only
after execution. Every replay must preserve evidence bytes in no-write mode.
