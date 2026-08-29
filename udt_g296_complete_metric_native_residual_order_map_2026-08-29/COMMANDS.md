# G296 sealed replay commands

Every command below is runnable from the sealed intake with Python's standard library only:

```bash
python3 udt_g296_complete_metric_native_residual_order_map_2026-08-29/derive_native_residual_order_map.py
python3 udt_g296_complete_metric_native_residual_order_map_2026-08-29/verify_native_residual_independent.py
python3 udt_g296_complete_metric_native_residual_order_map_2026-08-29/run_catch_proofs.py
python3 udt_g296_complete_metric_native_residual_order_map_2026-08-29/verify_prereg_ancestry_proof.py
python3 udt_g296_complete_metric_native_residual_order_map_2026-08-29/verify_package.py
```

The repository-wide premise-registry verifier and full test suite are separate integration gates.
They are run from the repository before banking, but are not claimed to be sealed package replays.
