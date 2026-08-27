# G281 registered commands

Run from repository root unless otherwise noted. All commands are read-only.

```bash
python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_sne_provenance_audit.py
python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_sne_provenance_independent.py
python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_saved_lineage_outputs.py
python3 verify_luminosity_distance_n2.py
```

The following G279/G280 commands are repository-recorded historical evidence. Their scripts were
not present in the first G281 sealed intake and are therefore not registered sealed-review commands:

```bash
cd udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27
python3 derive_native_provenance.py --no-write
python3 verify_native_chain_independent.py --no-write
python3 run_catch_proofs.py --no-write
cd ../udt_g280_projective_position_optical_area_bridge_audit_2026-08-27
python3 derive_projective_optical_bridge.py --no-write
python3 verify_projective_optical_bridge_independent.py --no-write
python3 run_catch_proofs.py --no-write
```

Repository banking gates:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
git diff --check
```

External-review intake preparation:

```bash
python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/build_review_intake.py
```
