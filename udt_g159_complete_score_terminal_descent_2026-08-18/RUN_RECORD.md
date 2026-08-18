# G159 run record

Date: 2026-08-18

No GPU, long solve, observational data, fit, or protected package was used.

```bash
python3 udt_g159_complete_score_terminal_descent_2026-08-18/derive_terminal_first_jet.py
python3 udt_g159_complete_score_terminal_descent_2026-08-18/verify_terminal_first_jet_independent.py
python3 udt_g159_complete_score_terminal_descent_2026-08-18/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q
python3 udt_g159_complete_score_terminal_descent_2026-08-18/verify_package.py
```

Production method: exact SymPy matrix/differential algebra.

Independent method: standard-library `Fraction` pair metrics plus first-order dual-number
differentiation, live recharting, rational Lorentz frames, and deterministic seed 159.
