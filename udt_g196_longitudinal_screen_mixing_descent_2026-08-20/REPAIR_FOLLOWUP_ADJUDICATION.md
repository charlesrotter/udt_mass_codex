# G196 repair-only follow-up adjudication

Date: 2026-08-21

## Final landing

`G196_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`

The fresh external reviewer found no remaining R1 or R2 defect. R1 accurately separates the
independently implemented Torch metric-side contractions from the formula-level IVP regression
driven by shared `candidate_matrices(...)` coefficients. The original preregistration remains
visible with a dated correction.

For R2, the reviewer ran the exact registered package replay in a strictly read-only sandbox. It
exited zero in `1336.947` seconds with 17 production assertions, 204 histories, 5,313 independent
metric-side and regression assertions, 9 hostile catches, fresh/sealed artifact identity, and
stale-artifact rejection. Torch imported without a writable temporary directory. All 38/38 sealed
hashes matched before and after, and `.review_runtime` remained empty.

The final grade is `EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS`. The retained theorem applies only to
the displayed positive `a(eta)`, real `M(eta,z)` affine coframe family and one supplied central
outgoing germ. It does not cover arbitrary complete metrics or coframes, other directions,
physical observer populations or functions, transfer, observations, global completion, or
`X_max`.

No canonization is implied.
