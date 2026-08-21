# G203 run record

Date: 2026-08-21

Preregistration commit: `f1fa632a`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/derive_parameter_ownership.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/verify_parameter_ownership_independent.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g203_quiet_overlap_parameter_ownership_classification_2026-08-21/run_catch_proofs.py
```

Observed:

- first production run failed on a structural expression-order comparison for
  \(R^2-r_0^2=(R-r_0)(R+r_0)\);
- repaired to exact simplified difference equal to zero;
- production: 70 assertions pass;
- independent: 20,000 distinct cases, 280,011 assertions, eight source hashes pass;
- hostile catches: 10/10.
