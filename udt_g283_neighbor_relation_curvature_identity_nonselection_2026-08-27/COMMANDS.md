# G283 registered commands

Run from the repository root:

```bash
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/verify_preregistration_chronology.py
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/verify_preregistration.py
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/derive_identity_nonselection.py
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/verify_independent.py
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/run_catch_proofs.py
python3 udt_g283_neighbor_relation_curvature_identity_nonselection_2026-08-27/verify_package.py
```

The first, second, fifth, and sixth commands are standard-library-only. The production derivation uses
SymPy. The independent verifier uses only the Python standard library and does not import the
production module.
