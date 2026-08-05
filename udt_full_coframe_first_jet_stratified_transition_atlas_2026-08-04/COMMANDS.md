# Reproduction commands

Run from repository root, CPU only:

```bash
python3 udt_full_coframe_first_jet_stratified_transition_atlas_2026-08-04/derive_stratified_first_jet.py --no-write
python3 udt_full_coframe_first_jet_stratified_transition_atlas_2026-08-04/independent_stratified_first_jet.py --no-write
python3 udt_full_coframe_first_jet_stratified_transition_atlas_2026-08-04/verify_audit.py --no-write
python3 verify_current_scientific_premises.py
python3 udt_full_coframe_first_jet_stratified_transition_atlas_2026-08-04/verify_repository_gates.py
python3 udt_full_coframe_first_jet_stratified_transition_atlas_2026-08-04/verify_package_manifest.py
```

The repository gate includes the documented full test baseline. No GPU, numerical relaxation,
time-live solve, timeout-based scientific test, or network access is used.
