# G240 commands

Run from this directory:

```bash
python3 derive_null_image_cluster_census.py
python3 verify_cluster_census_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

No-write replays:

```bash
python3 derive_null_image_cluster_census.py --no-write
python3 verify_cluster_census_independent.py --no-write
python3 run_catch_proofs.py --no-write
python3 verify_package.py --no-write
```

Build the corrected repair-only intake. The builder runs the delivered sealed verifier and a
missing-`sources/` negative gate before reporting success:

```bash
python3 build_review_intake.py
```

Repository gates from the repository root:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

No command reads observational outcomes or protected packages.
