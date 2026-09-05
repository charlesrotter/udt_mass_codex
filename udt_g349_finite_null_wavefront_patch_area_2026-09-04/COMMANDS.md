# G349 registered commands

Date: 2026-09-04
Status: outcome unseen

Run only after the preregistration and frozen scripts are committed and pushed:

```bash
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S derive_finite_null_patch_area.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S verify_finite_null_patch_area_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -B -S run_catch_proofs.py
```

No result file may be written by these commands in no-write mode. Exact outputs and any failure or
repair will be recorded after first execution.
