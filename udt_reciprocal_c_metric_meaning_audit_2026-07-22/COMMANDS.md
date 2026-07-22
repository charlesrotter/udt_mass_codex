# Commands

All calculations were CPU-only and run from repository root.

```bash
python3 udt_reciprocal_c_metric_meaning_audit_2026-07-22/build_source_lineage.py
python3 udt_reciprocal_c_metric_meaning_audit_2026-07-22/derive_metric_meaning.py
python3 udt_reciprocal_c_metric_meaning_audit_2026-07-22/verify_metric_meaning.py
python3 udt_reciprocal_c_metric_meaning_audit_2026-07-22/freeze_manifest.py
python3 udt_reciprocal_c_metric_meaning_audit_2026-07-22/verify_repository_gates.py
```

The repository gate disables CUDA for the documented test baseline, replays all six hard-frozen
manifests and all prior scientific manifests, verifies current navigation, and checks only metadata
for the original 54-path dirty checkout.
