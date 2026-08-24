# G248 commands

All registered replays are no-write unless `--output` is explicitly supplied.

```bash
python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/derive_regular_branch_measure.py --cases 4096
python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/verify_regular_branch_measure_independent.py --cases 10000
python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/run_catch_proofs.py
python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/verify_package.py
python3 udt_g248_metric_regular_branch_measure_ownership_2026-08-24/build_review_intake.py
```
