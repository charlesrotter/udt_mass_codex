# G194 external-review adjudication

Date: 2026-08-20

## Final adjudicated landing

`G194_R5_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`

The first reviewer did not refute the bounded theorem, but found two evidence-packaging defects:

1. sealed read-only replay fails during temporary-directory discovery before the Torch verifier;
2. the package verifier conditionally consults an ambient repository premise script.

Both findings were accepted.  R2 removed the ambient premise-verifier dependency, R3 recorded the
exact independence grade, and R5 replaced the write-triggering autodiff path.  The preregistered R5
equivalence census passed all 384 comparisons with maximum error
`5.551115123125783e-16`; its artifact-drift gate found zero forbidden differences and maximum
allowed diagnostic drift `4.440892098500626e-16`.

The fresh external repair-only reviewer ran the exact registered no-write replay.  It exited `0`,
reported fresh artifact identity, preserved package digests, left the review runtime empty, and
retained 267 histories, 4,007 independent assertions, and 22 hostile catches.  The reviewer
therefore accepted R5, retained R2/R3, and the unchanged bounded landing.

The reviewer's independence qualification is also accepted and already matches the package's
disclosure: metric jets/Riemann are independently spot-checked, while the interval IVP comparison
is formula-driven rather than a metric curvature reconstruction at every adaptive step.

## Retained bounded grade

`EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS`

The exact function-space proof is supported only for arbitrary smooth symmetric `M` in the
displayed coframe family and supplied central pair.  The review does not strengthen the declared
independence grade or widen the scientific scope.  Antisymmetric rotation, arbitrary complete
coframes, other germs, physical history, transfer, global completion, and `X_max` remain open.

No canonization is implied.
