# G166 run record

Date: 2026-08-18

## Preregistration

- commit: `5ed7af16`
- frozen sources: 13
- method: exact symbolic production plus independent stdlib/Fraction replay

## Commands

```text
python3 udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/derive_primary_pair_kernel.py
python3 udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/verify_primary_pair_kernel_independent.py
python3 udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/run_catch_proofs.py
python3 udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/verify_package.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q tests/test_startup_surface.py
python3 -m pytest -q
```

## Results

- exact production checks: 22/22
- frozen source hashes: 13/13
- independent exact Fraction trials: 1,200/1,200
- semantic mutation catches: 9/9
- premise registry: 152 rows pass; startup guards: 50/50 pass
- repository regression: 124 pass, 1 registered xfail
- fresh external review: open
