# Commands

All calculations are CPU-only and use the Python standard library.

```bash
python3 udt_xmax_dilation_asymptote_correction_2026-07-23/derive_xmax_dilation_correction.py
python3 udt_xmax_dilation_asymptote_correction_2026-07-23/verify_xmax_dilation_correction_independent.py
sha256sum --check udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23/MANIFEST.sha256
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
```

The production derivation and independent verifier do not import one
another. The independent verifier starts again from rational
`q=exp(-phi)` witnesses, redoes the WR-L exponent logic, audits every source
hash and status table, and exercises fail-closed semantic mutations.
