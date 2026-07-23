# Command record

Production exact derivation:

```bash
PYTHONPATH=/tmp/udt_finite_cell_density_site \
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_angular_bulk_jacobi_selector_audit_2026-07-23/derive_angular_bulk_jacobi_selector.py
```

Independent standard-library verification:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_angular_bulk_jacobi_selector_audit_2026-07-23/verify_angular_bulk_jacobi_selector_independent.py
```

Repository replay, tests, manifest construction, and repository gates are
preserved in their corresponding package artifacts.
