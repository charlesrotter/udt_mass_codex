# G194 external-review repair preregistration

Date: 2026-08-20

The fresh gpt-5.4 review returned
`GENERAL_SYMMETRIC_CLOSURE_ACCEPTED_WITH_CAVEATS` and retained the bounded mathematical landing.
This repair cycle is packaging-only.

## R1 — dependency-free temporary-directory discovery

Before importing Torch in the independent verifier, when both `G194_NO_WRITE=1` and
`G194_REVIEW_RUNTIME_REQUIRED=1`, set Python's already existing `tempfile.tempdir` variable to the
resolved intake-local `.review_runtime` directory.  This bypasses `tempfile`'s writable-directory
probe; it does not grant write permission or create a file.  The verifier must still prove:

- `.review_runtime` is empty before and after replay;
- every evidence-file digest is unchanged;
- the fresh numerical result is byte-equivalent as parsed JSON to the sealed artifact.

The repair fails if Torch or any dependency actually needs to write, if the read-only replay still
fails, or if any evidence digest changes.

## R2 — eliminate ambient repository dependence

Remove execution of `ROOT/verify_current_scientific_premises.py` from `verify_package.py`.  The
sealed package verifier must report that repository premise verification is a separate outer gate.
The repository-level verifier remains mandatory before banking, but it may not influence sealed
artifact identity.

The repair fails if `verify_package.py` reads or executes any unmanifested repository file.

## R3 — retain the exact independence grade

Add an explicit machine-readable statement that the independent evidence is:

`METRIC_JET_RIEMANN_SPOTCHECK_PLUS_FORMULA_DRIVEN_MATRIX_IVP`

and is not full metric-derived interval propagation.  No numerical method, history, tolerance,
result, or scientific wording may be strengthened.

## Frozen scientific landing

The coframe, arbitrary functions, equations, factor ordering, Gram proof, 267 histories, 4,007
assertions, 22 mutations, tolerances, and bounded maximum conclusion are frozen.  Any change to
them invalidates this repair-only cycle and requires a new scientific preregistration.

## Follow-up requirement

Build a fresh sealed intake and request a repair-only external follow-up.  The follow-up may verify
only R1--R3 and the unchanged bounded landing.  Final banking remains prohibited until that replay
passes and the follow-up accepts the repairs.
