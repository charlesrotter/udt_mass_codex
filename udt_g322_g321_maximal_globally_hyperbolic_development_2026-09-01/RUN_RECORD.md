# G322 run record

Date: 2026-09-01
Python: `3.10.12`
Preregistration: `8bf4aedb`

Question: apply the imported maximal Cauchy-development theorem to the fixed complete G321 data,
without changing the UDT equation or selecting data.

Commands:

```text
python3 -S derive_maximal_development.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

Production controls: `p=3/2`, `a=1/5`, `J0=100`, modes `1,2,3,4`, both signs, 2,048 periodic
points per mode/sign.

Independent controls: `p=1.7`, `a=0.12`, `J0=300`, modes `1,3,5`, both signs, 1,024 periodic
points per mode/sign, direct connection/Ricci index loops.

Production output: `PASS_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW`, 62 machine assertions.

Independent output: `PASS_INDEPENDENT`, 19 assertions, no production import or production-result
read.

Aggregate output: all 14 hostile evidence mutations caught; package verifier passed with the fresh
external review graded `REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED`. Repairs R1 and R2 are
preregistered at commit `c91dbd85` in `REPAIR_LEDGER.tsv`. The repair-only reviewer replayed the
same four commands, obtained byte-identical tracked outputs, caught all 14 mutations, and returned
`G322_REPAIRS_ACCEPTED__CONDITIONAL_MAXIMAL_GLOBALLY_HYPERBOLIC_DEVELOPMENT_PER_FIXED_DATUM_UPHELD`.

No GPU or time integration was used. This is a theorem-interface audit, not a numerical evolution.
