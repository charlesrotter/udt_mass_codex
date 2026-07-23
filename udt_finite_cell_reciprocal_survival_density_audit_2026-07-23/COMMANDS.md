# Commands

Production and independent verification used the pinned dependency in an
isolated temporary site directory:

```bash
python3 -m pip install --disable-pip-version-check --no-deps \
  --target /tmp/udt_finite_cell_density_site sympy==1.14.0
PYTHONPATH=/tmp/udt_finite_cell_density_site \
  python3 udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/derive_finite_cell_survival.py
PYTHONPATH=/tmp/udt_finite_cell_density_site \
  python3 udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/verify_finite_cell_survival_independent.py
PYTHONPATH=/tmp/udt_finite_cell_density_site \
  python3 udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/run_full_tests.py
python3 udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/build_manifest.py
python3 udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/verify_repository_gates.py
```

The fresh zero-context GPT-5.4 reviewer independently copied the repository
to a new temporary directory, installed the same pinned SymPy version into a
separate target, reran both scripts, replayed all source hashes and catches,
and compared the generated artifacts byte-for-byte.
