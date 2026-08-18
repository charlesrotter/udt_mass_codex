# G165 run record

Date: 2026-08-18
Preregistration commit: `208c6d51`

Commands:

```text
python3 -m py_compile udt_g165_conformal_fiber_rank_audit_2026-08-18/*.py
python3 udt_g165_conformal_fiber_rank_audit_2026-08-18/derive_conformal_fiber_rank.py
python3 udt_g165_conformal_fiber_rank_audit_2026-08-18/verify_conformal_fiber_rank_independent.py
python3 udt_g165_conformal_fiber_rank_audit_2026-08-18/run_catch_proofs.py
python3 udt_g165_conformal_fiber_rank_audit_2026-08-18/verify_package.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q tests/test_startup_surface.py
python3 -m pytest -q
```

The first independent run exposed only brittle phrase matching in the verification harness. The
scientific quantities had already passed. The exact source phrases were registered, the rational
replay was strengthened to construct pair metrics directly from rational `T,L,beta`, and the full
independent run then passed.
