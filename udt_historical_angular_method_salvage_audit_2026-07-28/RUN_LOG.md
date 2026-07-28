# Run log

All commands ran from repository root with CPU-only intent.

```text
python3 -m py_compile udt_historical_angular_method_salvage_audit_2026-07-28/derive_method_salvage.py udt_historical_angular_method_salvage_audit_2026-07-28/verify_method_salvage.py
python3 udt_historical_angular_method_salvage_audit_2026-07-28/derive_method_salvage.py
python3 udt_historical_angular_method_salvage_audit_2026-07-28/verify_method_salvage.py
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 verify_current_scientific_premises.py
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
python3 udt_historical_angular_method_salvage_audit_2026-07-28/finalize_package.py
python3 udt_historical_angular_method_salvage_audit_2026-07-28/verify_repository_gates.py
```

Pre-finalization outcomes:

- production exact algebra/census: PASS;
- independent stdlib replay: PASS with same-context caveat;
- semantic catch proofs: 27/27 exercised and rejected corruption;
- current scientific premise guards: 16/16 PASS;
- tests: 70 passed, 1 expected xfail;
- GPU use: none.
