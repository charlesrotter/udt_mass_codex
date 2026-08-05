# Reproduction commands

Run from repository root with CPU-only Python:

```bash
python3 udt_complete_coframe_extension_solvability_audit_2026-08-04/derive_extension_solvability.py --no-write
python3 udt_complete_coframe_extension_solvability_audit_2026-08-04/independent_extension_solvability.py --no-write
python3 udt_complete_coframe_extension_solvability_audit_2026-08-04/verify_audit.py --no-write
python3 verify_current_scientific_premises.py
python3 udt_complete_coframe_extension_solvability_audit_2026-08-04/verify_repository_gates.py
python3 udt_complete_coframe_extension_solvability_audit_2026-08-04/verify_package_manifest.py
```

The repository-gate script includes the documented full test baseline. No GPU process, numerical
field solve, timeout-based scientific test, or network access is used.
