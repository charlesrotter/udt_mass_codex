# G202 run record

Date: 2026-08-21

Preregistration commit: `8503a413`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/derive_quiet_overlap_profile.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/verify_quiet_overlap_independent.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g202_quiet_overlap_profile_anchor_classification_2026-08-21/run_catch_proofs.py
```

Observed results:

- first symbolic run: 31/33 because SymPy did not resolve limits with coefficients declared merely
  nonnegative;
- repaired proof uses exact positive lower-bound factorization: 32/32;
- independent: 20,000 exact profile cases, 1,000 finite-anchor controls, 170,003 assertions;
- catch proofs: 9/9.
