# G345 commands

Date: 2026-09-04

No derivation or outcome command was run before this preregistration was banked.

Planned bounded replay commands:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_screen_scalar.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_screen_scalar_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_package.py
```

The exact production commands, environment, versions, and outputs will be appended to
`RUN_RECORD.md` after execution.

All four planned bounded commands were subsequently run exactly as listed. Production passed
`9824/9824` after the repair preserved in `PREREGISTRATION_EXECUTION_NOTE.md`; independent passed
`4360/4360`; hostile passed `17/17`; aggregate passed `17/17` without changing package bytes.
