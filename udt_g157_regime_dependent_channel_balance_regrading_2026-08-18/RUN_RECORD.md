# G157 run record

Date: 2026-08-18

No GPU, long solve, observational data, fit, or protected package was used.

```bash
python3 udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/derive_regime_balance.py
python3 udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/verify_regime_balance_independent.py
python3 udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 udt_g157_regime_dependent_channel_balance_regrading_2026-08-18/verify_package.py
python3 -m pytest -q
```

Production method: exact symbolic matrices and source-led regrading.

Independent method: standard-library exact `Fraction` matrices plus independently coded floating
one-parameter subgroup checks, with deterministic seed 157.
