# G246 commands

Run from the repository root:

```bash
python3 udt_g246_two_observer_null_incidence_descent_2026-08-24/derive_two_observer_null_incidence.py --no-write
python3 udt_g246_two_observer_null_incidence_descent_2026-08-24/verify_two_observer_null_incidence_independent.py --no-write
python3 udt_g246_two_observer_null_incidence_descent_2026-08-24/run_catch_proofs.py --no-write
python3 udt_g246_two_observer_null_incidence_descent_2026-08-24/verify_package.py --no-write
```

Repository integration gates, not sealed bounded replays:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

The evidentiary replays read no observational outcomes and write no persistent output.
