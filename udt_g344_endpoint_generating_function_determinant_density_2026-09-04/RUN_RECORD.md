# G344 run record

Date: 2026-09-04

All accepted runs used CPU double precision, Python standard-library arithmetic, explicit
Gauss/Simpson quadrature, finite endpoint differences, and RK4 action integration. No GPU process
or long solve was used.

## First frozen executions

The initially frozen production (`13100/13100`), independent (`4612/4612`), and hostile (`14/14`)
runs passed. Proof-writing then exposed the additive endpoint-function qualification recorded in
`PREREGISTRATION_EXECUTION_NOTE.md`. Those first passes are not the accepted final evidence.

## Accepted post-qualification reruns

```text
UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_endpoint_generator.py
PASS 13580/13580

UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_endpoint_generator_independent.py
PASS 4882/4882

UDT_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
PASS 14/14 hostile catches
```

The accepted reruns include all six endpoint orderings. No candidate formula, tolerance, physical
attachment, or maximum conclusion changed.

## First aggregate replay

The first `verify_package.py` run passed all three executable replays and the no-byte-change gate
but reported `18/19`: its documentation check required capitalized `Its determinant` while the
derivation contained lowercase `its determinant`. The verifier token was corrected to the exact
existing text. No evidence file, formula, tolerance, or scientific claim changed.

## External and post-review gates

```text
external gpt-5.4 sealed review
ACCEPT_G344_BOUNDED_SCREEN_ENDPOINT_GENERATOR_AND_BIDENSITY
No blocking finding; registered replay 19/19 and separate scratch reconstruction passed.
```

The external reviewer retained two non-blocking evidence caveats: compact-lift executable coverage
is documentary because the package contains no multi-lift aggregation path, and text-token gates
are packaging guards rather than analytic proof.

## Final repository integration gates

After adding the exact G344 registry row and startup pointers:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B verify_current_scientific_premises.py
PASS: 327-row premise registry and G344 startup/premise guards

PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/
220 passed, 1 xfailed
```

The first full suite attempt found only that the new `INDEX.md` pointer exceeded its startup line
cap by one line. The pointer was folded onto the existing G343/G344 line, its exact targeted test
passed, and the clean full-suite rerun produced the result above. The marked xfail is the existing
matter-sector habit-pin gate and is unrelated to G344.
