# G245 commands

Run from the repository root.

```bash
python3 verify_current_scientific_premises.py
python3 udt_g245_metric_owned_observer_null_cone_field_2026-08-24/derive_metric_owned_null_cone.py --no-write
python3 udt_g245_metric_owned_observer_null_cone_field_2026-08-24/verify_metric_owned_null_cone_independent.py --no-write
python3 udt_g245_metric_owned_observer_null_cone_field_2026-08-24/run_catch_proofs.py --no-write
python3 udt_g245_metric_owned_observer_null_cone_field_2026-08-24/verify_package.py --no-write
python3 -m pytest -q
```

The derivation and independent verifier read no observational outcomes. The no-write replays make
no persistent changes.
