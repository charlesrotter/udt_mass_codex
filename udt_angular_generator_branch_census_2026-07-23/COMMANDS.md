# Command record

Production exact derivation:

```bash
PYTHONPATH=/tmp/udt_finite_cell_density_site \
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_angular_generator_branch_census_2026-07-23/derive_angular_generator_branch_census.py
```

Independent standard-library verification:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 udt_angular_generator_branch_census_2026-07-23/verify_angular_generator_branch_census_independent.py
```

Repository replay, tests, manifest, and gates are preserved in their
corresponding package artifacts.
