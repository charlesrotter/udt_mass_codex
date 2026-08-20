# G187 external certification-repair follow-up adjudication

Date: 2026-08-20

The fresh external gpt-5.4 repair-only reviewer returned:

```text
G187_CERTIFICATION_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
```

It verified all 31 sealed payload hashes and byte counts, reran `run_catch_proofs.py`, and reran the
full package verifier including the 10,000-witness exact-Fraction curvature reconstruction. The
repaired layer now contains 15 algebraic mutation catches and 14 separately labelled in-memory
artifact-scope guards, with no literal `True` placeholders in either catch dictionary.

The reviewer confirmed that the preregistered scope ceiling, source set, metric, screen transport,
tidal formulas, finite Jacobi map, and scientific landing are unchanged. The certification repair
is accepted and closed.

The original scientific caveat remains: the independent replay is engine-independent and rebuilds
the curvature from the metric two-jet, but it shares the declared curvature convention and target
scope rather than constituting a theorem over unrelated metric ansatz families.
