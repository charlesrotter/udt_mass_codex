# Commands

All computations were CPU-only and run from repository root.

```bash
python3 udt_reciprocal_subbundle_ownership_audit_2026-07-22/build_source_lineage.py
python3 udt_reciprocal_subbundle_ownership_audit_2026-07-22/derive_reciprocal_subbundle_ownership.py
python3 udt_reciprocal_subbundle_ownership_audit_2026-07-22/verify_reciprocal_subbundle_ownership.py
python3 udt_reciprocal_subbundle_ownership_audit_2026-07-22/freeze_manifest.py
python3 udt_reciprocal_subbundle_ownership_audit_2026-07-22/verify_repository_gates.py
```

The repository gate runs the documented CPU-only test baseline with CUDA disabled and replays all
six hard-frozen manifests, all prior scientific manifests, current navigation targets, package
hashes, and original dirty-checkout metadata.
