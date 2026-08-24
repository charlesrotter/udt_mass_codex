# G241 independent-replay correction preregistration

Date: 2026-08-23

The production evaluation completed and returned
`NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS`. The independent route then stopped before
producing any candidate result because this installed `mpmath` version does not accept a matrix
right-hand side in `lu_solve`.

The only authorized repair is mechanical:

```text
replace lu_solve(C, B) and lu_solve(C, theta)
with an explicitly formed high-precision inverse C^-1 multiplied by B and theta.
```

No candidate degree, threshold, covariance entry, carrier formula, monotonicity gate, tidal sign,
source/query premise, or landing may change. The repaired independent implementation must still be
high-precision and must not read the production result. A different landing or a disagreement above
the registered comparison tolerances fails the package.
