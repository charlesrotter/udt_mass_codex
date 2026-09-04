# G346 commands

Date: 2026-09-04

No derivation or outcome command was run before this preregistration was banked.

Planned bounded replay commands:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_directional_angular_area.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_directional_angular_area_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

The exact commands, environment, versions, parameters, and outputs will be recorded in
`RUN_RECORD.md` after execution.
