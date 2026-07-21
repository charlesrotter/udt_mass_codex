# Commands

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_pre_p06_boundary_selector_audit_2026-07-21/derive_boundary_selector.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_pre_p06_boundary_selector_audit_2026-07-21/verify_boundary_selector.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_pre_p06_boundary_selector_audit_2026-07-21/build_manifest.py
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES='' python3 -B udt_pre_p06_boundary_selector_audit_2026-07-21/verify_repository_gates.py
```

The derivation is deterministic and performs no numerical solve. The independent verifier does not
import the generator; it replays parent hashes, reconstructs the load-bearing algebra, validates the
complete tables, and exercises deliberate corruptions.
