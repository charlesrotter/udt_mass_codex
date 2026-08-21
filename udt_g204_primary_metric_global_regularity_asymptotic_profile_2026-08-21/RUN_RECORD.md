# G204 run record

Date: 2026-08-21

Original preregistration: `ea91f45e`

Smoothness correction preregistration: `785b0447`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/derive_global_regularity.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/verify_global_regularity_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/run_boundary_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g204_primary_metric_global_regularity_asymptotic_profile_2026-08-21/run_catch_proofs.py
```

Observed sequence:

1. direct curvature and first replacement passed bounded-curvature checks;
2. manual Cartesian-smoothness audit found its nonzero odd center powers;
3. original smoothness claim failed closed and even-areal repair was preregistered;
4. repaired production: 113 assertions pass;
5. independent: 10,000 distinct cases and 160,010 assertions pass;
6. diagnostics: 80-digit center convergence and outer decay pass;
7. hostile catches: 13/13.

Package replay initially stopped only on a prose token split across a line break. The mechanical
check was repaired to normalize whitespace and then returned `all_pass=true`; all four evidence
artifacts remained byte-stable under the no-write replay.
