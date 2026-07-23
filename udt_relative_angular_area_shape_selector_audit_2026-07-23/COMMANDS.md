# Command record

Production exact derivation:

```bash
PYTHONPATH=/tmp/udt_finite_cell_density_site \
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_relative_angular_area_shape_selector_audit_2026-07-23/derive_relative_angular_area_shape_selector.py
```

Independent standard-library verification:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_relative_angular_area_shape_selector_audit_2026-07-23/verify_relative_angular_area_shape_selector_independent.py
```

Repository replay, tests, manifest construction, and repository gates are
preserved in their corresponding package artifacts.
