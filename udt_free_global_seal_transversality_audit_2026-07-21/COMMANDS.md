# Commands

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_free_global_seal_transversality_audit_2026-07-21/derive_free_seal_transversality.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_free_global_seal_transversality_audit_2026-07-21/verify_free_seal_transversality.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_free_global_seal_transversality_audit_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_free_global_seal_transversality_audit_2026-07-21/verify_repository_gates.py
```

All calculations are exact symbolic or integer/rank checks. No ODE/PDE evolution is run.
