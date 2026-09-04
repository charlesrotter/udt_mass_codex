# G343 run record

Date: 2026-09-04

All accepted runs used CPU double precision, Python standard-library arithmetic, explicit
Gauss/Simpson quadrature, and no persistent output from the executable scripts.

## Accepted corrected runs

```text
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_bilocal_propagator.py
PASS 8888/8888

UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_bilocal_independent.py
PASS 2960/2960

UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
PASS 13/13 hostile catches
```

No GPU process or long solve was used. See `PREREGISTRATION_EXECUTION_NOTE.md` for the discarded
implicit-reference runs and the preserved first corrected-chart comparison failure.

## External and post-review gates

```text
external gpt-5.4 sealed review
ACCEPT_G343_BOUNDED_BILOCAL_SCREEN_PHASE_SPACE_PROPAGATOR
No findings at any severity; registered replay 19/19 and separate 25-case scratch check passed.

UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_package.py
PASS 21/21

PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/
220 passed, 1 xfailed

PYTHONDONTWRITEBYTECODE=1 python3 -B verify_current_scientific_premises.py
PASS: 326-row premise registry and G343 startup/premise guards
```

The one repository xfail is the registered legacy matter-sector habit-pin gate and is outside
G343. The post-review documentation and startup edits did not change the scientific result.
