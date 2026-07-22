# Exact commands

Run from repository root:

```bash
python3 udt_timelive_spherical_areal_polarization_audit_2026-07-22/build_source_lineage.py
python3 udt_timelive_spherical_areal_polarization_audit_2026-07-22/derive_timelive_areal_polarization.py
python3 udt_timelive_spherical_areal_polarization_audit_2026-07-22/verify_timelive_areal_polarization.py
python3 udt_timelive_spherical_areal_polarization_audit_2026-07-22/freeze_manifest.py
python3 udt_timelive_spherical_areal_polarization_audit_2026-07-22/verify_repository_gates.py
```

The production derivation is pinned by `requirements.txt`. The independent verification uses only
the Python standard library. All computations are CPU-only and exact.
