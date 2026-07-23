# Command record

CPU-only pinned environment:

```bash
PYTHONPATH=/tmp/udt_finite_cell_density_site python3 \
  udt_reciprocal_seam_descent_audit_2026-07-23/derive_reciprocal_seam_descent.py

PYTHONPATH=/tmp/udt_finite_cell_density_site python3 \
  udt_reciprocal_seam_descent_audit_2026-07-23/verify_reciprocal_seam_descent_independent.py

PYTHONPATH=/tmp/udt_finite_cell_density_site PYTHONDONTWRITEBYTECODE=1 \
  python3 udt_reciprocal_seam_descent_audit_2026-07-23/replay_and_capture.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_reciprocal_seam_descent_audit_2026-07-23/run_full_tests.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_reciprocal_seam_descent_audit_2026-07-23/build_manifest.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_reciprocal_seam_descent_audit_2026-07-23/verify_repository_gates.py
```

Raw replays, external review, tests, repository gates, and package manifest
are recorded in their respective artifacts.
