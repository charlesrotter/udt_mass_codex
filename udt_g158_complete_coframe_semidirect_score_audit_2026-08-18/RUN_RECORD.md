# G158 run record

Date: 2026-08-18

No GPU, long solve, observational data, fit, or protected package was used.

```bash
python3 udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/derive_complete_coframe_score.py
python3 udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/verify_complete_coframe_independent.py
python3 udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q
python3 udt_g158_complete_coframe_semidirect_score_audit_2026-08-18/verify_package.py
```

Production method: exact symbolic structured-matrix algebra.

Independent method: standard-library `Fraction` matrices and separately coded floating
fixed-generator paths, with deterministic seed 158.
