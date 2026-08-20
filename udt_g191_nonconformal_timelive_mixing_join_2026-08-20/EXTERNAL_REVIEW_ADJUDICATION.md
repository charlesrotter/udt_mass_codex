# G191 first external-review adjudication

The external grade is `G191_REPAIR_REQUIRED`.

This is a reproducibility and intake-packaging failure, not a scientific rejection. The reviewer
found no counterexample in the frozen artifacts to the bounded coframe, affine, frequency,
curvature, Jacobi, limit, or branch claims. However, the only authorized fresh replay failed before
those assertions because the intake moved sources below `sources/` while the verifier retained
repository-relative paths, then attempted to call a repository-wide premise verifier absent from
the bounded intake.

The repair is preregistered in `EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md`. G191 remains
`VERIFIED_WITH_CAVEATS_EXTERNAL_REPAIR_PENDING`; it is not accepted or bankable until a corrected
sealed replay passes and a repair-only external follow-up accepts it.

