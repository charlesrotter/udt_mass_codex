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

All first executions were subsequently run exactly as listed. Production passed `11204/11204`,
implementation-distinct verification passed `4251/4251`, and hostile checks caught `20/20`. No
formula, tolerance, alternative, or maximum conclusion was changed after execution.

The sealed pre-review aggregate replay passed `19/19` after the packaging-only self-reference
repair recorded in `PREREGISTRATION_EXECUTION_NOTE.md`. External `gpt-5.4` then authenticated the
sealed intake, replayed all four commands, independently reconstructed the load-bearing formulas,
and accepted without required repair. The post-review aggregate, including exact return and
transmission authentication, passes `21/21`.
