# G200 run record

Date: 2026-08-21

Preregistration commit: `7b92835e`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/derive_primary_bidirectional_nonradial_null.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/verify_primary_bidirectional_nonradial_independent.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g200_primary_metric_bidirectional_nonradial_null_2026-08-21/run_catch_proofs.py
```

Observed results:

- production: 64/64 exact assertions;
- independent: 2,000 exact-rational third-jet cases and 38,160 assertions;
- nonzero-gradient cases: 2,000;
- exact flat controls: 40;
- catch proofs: 9/9.
