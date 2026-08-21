# G197 replay commands

From repository root:

```bash
python3 udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/verify_native_provenance.py
python3 udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/verify_package.py
python3 verify_current_scientific_premises.py
pytest -q tests/test_startup_surface.py
pytest -q
```

The zero-context transcripts record their exact disposable-clone commands. They are evidence
artifacts, not required for ordinary replay.
