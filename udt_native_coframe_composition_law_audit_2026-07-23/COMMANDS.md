# Commands

Run from repository root:

```bash
python3 udt_native_coframe_composition_law_audit_2026-07-23/derive_composition_audit.py
python3 udt_native_coframe_composition_law_audit_2026-07-23/verify_composition_independent.py
```

The deterministic capture wrapper records raw stdout/stderr and environment:

```bash
python3 udt_native_coframe_composition_law_audit_2026-07-23/replay_and_capture.py
```

Repository gates and the package manifest are run only after the scientific
records and fresh adversarial review are complete.

```bash
python3 udt_native_coframe_composition_law_audit_2026-07-23/run_full_tests.py
python3 udt_native_coframe_composition_law_audit_2026-07-23/build_manifest.py
python3 udt_native_coframe_composition_law_audit_2026-07-23/verify_repository_gates.py
cd udt_native_coframe_composition_law_audit_2026-07-23
sha256sum --check MANIFEST.sha256
cd ..
```
