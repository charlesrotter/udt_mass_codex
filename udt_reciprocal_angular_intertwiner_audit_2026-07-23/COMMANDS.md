# Command record

CPU-only production derivation:

```bash
PYTHONPATH=/tmp/udt_finite_cell_density_site PYTHONDONTWRITEBYTECODE=1 \
  python3 udt_reciprocal_angular_intertwiner_audit_2026-07-23/derive_reciprocal_angular_intertwiner.py
```

Independent standard-library verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_reciprocal_angular_intertwiner_audit_2026-07-23/verify_reciprocal_angular_intertwiner_independent.py
```

Fresh review, replay, tests, manifests, and repository gates are preserved
in their corresponding package artifacts.
