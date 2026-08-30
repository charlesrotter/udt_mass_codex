# G300 registered checks

Run from repository root:

```bash
python3 -S udt_g300_metric_celestial_query_bundle_descent_2026-08-29/derive_celestial_query_bundle.py
python3 -S udt_g300_metric_celestial_query_bundle_descent_2026-08-29/verify_celestial_query_bundle_independent.py
python3 -S udt_g300_metric_celestial_query_bundle_descent_2026-08-29/run_catch_proofs.py
python3 -S udt_g300_metric_celestial_query_bundle_descent_2026-08-29/verify_package.py
python3 verify_current_scientific_premises.py
```

The first four checks are exact standard-library rational arithmetic and write no evidence files.
The final command verifies the complete 284-row premise registry and startup surface.
