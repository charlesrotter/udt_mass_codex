# G156 run record

Date: 2026-08-18

No long solve, GPU process, fitted data, or protected package was used.

Commands:

```bash
python3 udt_g156_three_observer_scale_carry_audit_2026-08-18/derive_three_observer_scale_carry.py
python3 udt_g156_three_observer_scale_carry_audit_2026-08-18/verify_scale_carry_independent.py
python3 udt_g156_three_observer_scale_carry_audit_2026-08-18/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 udt_g156_three_observer_scale_carry_audit_2026-08-18/verify_package.py
python3 -m pytest -q
```

Production method: SymPy exact symbolic matrices and determinant identities.

Independent method: Python standard library and exact `Fraction` arithmetic, randomized with seed
156 over 500 positive-upper-triangular composition and endpoint-gauge trials.
