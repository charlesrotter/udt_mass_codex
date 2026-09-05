# G351 R5 sealed-package self-containment repair preregistration

Date: 2026-09-05

## Observed defect

The first locally built sealed intake omitted `build_review_intake.py` even though the aggregate
verifier requires and reads that file. Consequently, replay from the sealed copy failed before any
scientific check ran. That intake is superseded and must not be transmitted.

## Repair-only scope

1. Add `build_review_intake.py` and this preregistration to the builder's exact package file set.
2. Add an aggregate guard proving that every package file required by `verify_package.py` is
   included by `build_review_intake.py`, including the builder itself.
3. Extend the existing standard-library audit to the builder.
4. Synchronize only the aggregate count and packaging-status prose made stale by these guards.
5. Build a fresh intake and require the registered no-write aggregate to pass from that sealed
   copy before requesting external-review authorization.

## Frozen scientific landing

The G351 theorem, its premise classification, and every open item remain unchanged. This repair
may not change the metric, kernel, angular sector, response law, value of `q`, openness of `p`,
measure/density scope, caustic boundary, source or population status, light interpretation,
distance, history, scale, `X_max`, or canon status.

## Acceptance contract

- the superseded intake is not transmitted;
- the fresh builder output contains `build_review_intake.py`;
- the fresh sealed-copy replay passes all aggregate checks without changing package bytes or
  producing bytecode;
- an omitted required package file is rejected by the new aggregate guard;
- no scientific file or conclusion changes.
