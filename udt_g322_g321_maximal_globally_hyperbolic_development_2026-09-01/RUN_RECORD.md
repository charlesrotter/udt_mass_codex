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

Production output: `PASS_PENDING_INDEPENDENT_AND_EXTERNAL_REVIEW`, 54 machine assertions.

Independent output: `PASS_INDEPENDENT`, 11 assertions, no production import or production-result
read.

Aggregate output: all 12 hostile evidence mutations caught; package verifier passed with the fresh
external review graded `REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED`. Repairs R1 and R2 are
preregistered in `REPAIR_LEDGER.tsv`; repair-only follow-up is pending.

No GPU or time integration was used. This is a theorem-interface audit, not a numerical evolution.
