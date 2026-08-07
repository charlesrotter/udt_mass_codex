# Commands

Run from the repository root:

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 \
python3 udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23/replay_and_capture.py

CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 \
python3 udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23/run_full_tests.py

python3 udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23/build_manifest.py

CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 \
python3 udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23/verify_repository_gates.py
```
