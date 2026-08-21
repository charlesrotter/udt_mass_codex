# G199 run record

Date: 2026-08-21

Preregistration commit: `1514ed99`

Commands:

```text
python3 -m py_compile \
  udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/derive_primary_bidirectional_radial_null.py \
  udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/verify_primary_bidirectional_radial_null_independent.py

python3 udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/derive_primary_bidirectional_radial_null.py

python3 udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/verify_primary_bidirectional_radial_null_independent.py

python3 udt_g199_primary_metric_bidirectional_radial_null_2026-08-21/run_catch_proofs.py
```

Observed results:

- production: 65/65 exact assertions;
- independent: 2,000 cases, 60,000 assertions, all 2,000 nonflat;
- opposite-sign comparisons: 2,000;
- catch proofs: 9/9.
