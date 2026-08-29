# G292 external-review repair preregistration

Date: 2026-08-28
Status: `FROZEN_BEFORE_REPAIR`

The fresh sealed external reviewer returned `ACCEPT_WITH_REPAIRS` and no scientific defects. The
following four repairs are frozen before implementation. The scientific formulas, witness family,
free parameters, tolerances, omitted strata, and bounded landing must not change.

## R1 — fail closed without symbolic production replay

`verify_package.py` must require `sympy` and fail if it is unavailable. A preserved production JSON
may not substitute for the preregistered fresh production replay while the aggregate reports
`PASS`.

## R2 — sealed-safe replay instructions

`RUN_RECORD.md` must declare the `sympy` dependency and specify that replays from a read-only sealed
intake are run from a writable ephemeral copy or with a writable bytecode-cache prefix. This is a
documentation repair only.

## R3 — separate abstract connection coverage from metric realizability

`EXACT_DERIVATION.md` and the bounded-space evidence wording must say that the general theorem covers
the supplied abstract smooth orientable metric-connection stratum. It does not prove that every
such abstract connection is induced by a complete UDT metric history. Only the registered
`g_(R,epsilon)` family is explicitly realized metrically.

## R4 — close stale review/provenance statuses after replay

After implementing R1–R3, rerun the full premise verifier, the G292 production/independent/hostile
aggregate, and the repository tests. Only if those pass may the evidence gate and exact report be
updated to the externally reviewed bounded grade. Record the review verdict and retain all open
scientific strata.

## Acceptance contract

- `verify_package.py` fails closed when `sympy` is unavailable;
- writable-copy replay instructions are explicit;
- abstract connection classification is not promoted to a metric-realization theorem;
- full premise registry, G292 aggregate, and repository tests pass;
- landing token remains exactly unchanged;
- no protected or observational material enters.
