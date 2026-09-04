# G342 registered commands

Run from the repository root with bytecode disabled:

```bash
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -S udt_g342_full_null_jacobi_beam_area_2026-09-04/derive_full_null_jacobi.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -S udt_g342_full_null_jacobi_beam_area_2026-09-04/verify_full_null_jacobi_independent.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -S udt_g342_full_null_jacobi_beam_area_2026-09-04/run_catch_proofs.py
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -S udt_g342_full_null_jacobi_beam_area_2026-09-04/verify_package.py
```
