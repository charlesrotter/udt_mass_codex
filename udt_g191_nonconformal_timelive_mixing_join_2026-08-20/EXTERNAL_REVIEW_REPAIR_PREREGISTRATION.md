# G191 external-review repair preregistration

Date: 2026-08-20

The first sealed external review returned `G191_REPAIR_REQUIRED` because the registered no-write
replay was not self-contained. The intake builder copied the eight frozen upstream sources below a
`sources/` prefix while the package manifest and verifier retained repository-relative paths. The
verifier also unconditionally called the repository-wide premise verifier, which was intentionally
absent from the bounded intake.

The repair is restricted to replay packaging:

1. copy each frozen upstream source to its manifest-declared repository-relative path inside the
   sealed intake;
2. run the repository premise verifier whenever it is present, but record
   `SEALED_INTAKE_NOT_APPLICABLE` when a bounded sealed intake intentionally omits that
   repository-wide startup-surface verifier;
3. rebuild a fresh read-only intake and require the exact registered no-write replay to finish;
4. require byte identity of the scientific production, independent-verification, and catch-proof
   artifacts across the repair.

No coframe, metric, pair surface, affine ray, curvature, frequency, Jacobi formula, symbolic
limit, sample seed, numerical grid, tolerance, branch classification, premise status, or
scientific landing may change. A follow-up reviewer must return the grade; this repair cannot
self-promote G191.

