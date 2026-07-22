# Commands

All calculations were CPU-only and run from repository root.

```bash
python3 udt_reciprocity_regime_angular_center_audit_2026-07-22/build_source_lineage.py
python3 udt_reciprocity_regime_angular_center_audit_2026-07-22/derive_regime_angular_center.py
python3 udt_reciprocity_regime_angular_center_audit_2026-07-22/verify_regime_angular_center.py
python3 udt_reciprocity_regime_angular_center_audit_2026-07-22/freeze_manifest.py
python3 udt_reciprocity_regime_angular_center_audit_2026-07-22/verify_repository_gates.py
```

The repository gate disables CUDA for the documented test baseline, replays all six hard-frozen
manifests and all prior scientific manifests, verifies current navigation, and inspects only metadata
for the original 54-path dirty checkout.
