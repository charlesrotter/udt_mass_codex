# Table IV and released-Gaussian widths are different statistical objects

The primary paper's Table IV prints separately marginalized one-dimensional summaries. The public
Cobaya product supplies a joint 13-dimensional Gaussian approximation in the
`(D_V/r_d, D_M/r_d, D_H/r_d)` coordinate basis.

Therefore:

```text
Table-IV one-dimensional marginalized width
    is not required to equal
sqrt(diagonal entry of the released joint Gaussian covariance).
```

The released central vector agrees with the printed central values to below `0.001`. Its covariance
is exactly symmetric, full rank, positive-Cholesky, and is consumed verbatim by the released Cobaya
likelihood. The largest difference between `sqrt(diag(C_released))` and a printed Table-IV width is
`0.0097815861`.

This gap is not repaired, rescaled, fitted away, or used to remove a bin. It is retained as a
representation caveat. All quantitative use of this package must use the released vector and its
released covariance together. The Table-IV widths are a paper cross-check, not a replacement
likelihood.
