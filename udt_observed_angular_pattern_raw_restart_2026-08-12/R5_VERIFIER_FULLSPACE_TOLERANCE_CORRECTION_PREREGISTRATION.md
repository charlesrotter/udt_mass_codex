# R5 verifier full-space tolerance correction — preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_SECOND_VERIFIER_FAILURE__BEFORE_RERUN`

The second verifier run completed and wrote `PASS`, but the result is rejected. Its maximum reported
gap-conditioned tolerances were approximately `5e4`, while the realized discrepancies were only
`8.11e-13` and `3.99e-14`.

The error is exact: the verification plan declares a full-dimensional projector owned regardless
of its final singular-value gap, but the implementation still passed that tiny final gap into the
conditioning formula. This made the tolerance vacuous on full-space rows.

Freeze this verifier-only correction before rerun:

1. retain and report the literal final spectral gap;
2. for rank equal to the complete vector-space dimension, use effective conditioning gap `1.0` in
   the tolerance formula, because the projector is exactly the identity;
3. keep the original spectral-gap rule at every smaller rank;
4. require the final reported maximum tolerance to be at most the theoretical boundary value
   `8192 * eps_float64 / sqrt(eps_float64)`, apart from the `2e-10` floor;
5. change no production output, subspace, count, covariance, premise, or conclusion.

The rejected PASS is a verifier-method failure, not R5 evidence. Any later excessive tolerance or
comparison failure stops again.
