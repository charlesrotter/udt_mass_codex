# Commands

Run from repository root:

```bash
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/build_source_manifest.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/derive_intrinsic_objects.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/verify_intrinsic_objects_independent.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/replay_and_capture.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/run_full_tests.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/build_manifest.py
python3 udt_complete_metric_intrinsic_object_audit_2026-07-23/verify_repository_gates.py
python3 -m pytest tests/
```

All derivation and verification work is CPU-only.
