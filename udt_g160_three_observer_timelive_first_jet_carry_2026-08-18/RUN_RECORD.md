# G160 run record

Date: 2026-08-18

No GPU, long solve, observational data, fit, or protected package was used.

```bash
python3 udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/derive_timelive_first_jet_carry.py
python3 udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/verify_timelive_carry_independent.py
python3 udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/run_catch_proofs.py
python3 verify_current_scientific_premises.py
python3 -m pytest -q
python3 udt_g160_three_observer_timelive_first_jet_carry_2026-08-18/verify_package.py
```

Production: exact SymPy arbitrary-matrix derivation.

Independent: standard-library exact `Fraction` and first-order dual-number direct-product replay,
seed 160.

The initial independent sampler rejected null/spacelike transported clock columns, matching the
preregistered timelike domain. Fresh review later exposed stabilizer nonfaithfulness, false
necessity wording for `B+(2)`, and four missing independent loads. Exact witnesses and independent
coverage were added without changing the preregistered question or importing physics.
