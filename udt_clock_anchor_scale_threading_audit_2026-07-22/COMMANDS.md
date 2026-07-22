# Exact commands

Run from repository root:

```bash
python3 udt_clock_anchor_scale_threading_audit_2026-07-22/build_source_lineage.py
python3 udt_clock_anchor_scale_threading_audit_2026-07-22/derive_clock_anchor_scale_threading.py
python3 udt_clock_anchor_scale_threading_audit_2026-07-22/verify_clock_anchor_scale_threading.py
python3 udt_clock_anchor_scale_threading_audit_2026-07-22/freeze_manifest.py
python3 udt_clock_anchor_scale_threading_audit_2026-07-22/verify_repository_gates.py
```

The production route uses the pinned SymPy dependency. The independent route uses only the Python
standard library. All calculations are exact and CPU-only.
