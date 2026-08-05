# Reproduction commands

Run from repository root, CPU only:

```bash
python3 udt_second_jet_curvature_solder_atlas_2026-08-04/derive_second_jet_solder.py --no-write
python3 udt_second_jet_curvature_solder_atlas_2026-08-04/independent_second_jet_solder.py --no-write
python3 udt_second_jet_curvature_solder_atlas_2026-08-04/verify_audit.py --no-write
python3 verify_current_scientific_premises.py
python3 udt_second_jet_curvature_solder_atlas_2026-08-04/verify_repository_gates.py
python3 udt_second_jet_curvature_solder_atlas_2026-08-04/verify_package_manifest.py
```

The repository gate includes the documented full test baseline. No GPU, relaxation, time-live
solve, timeout-based scientific criterion, or network access is used.
