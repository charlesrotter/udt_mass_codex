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

## R2 — failed-candidate pole-neighborhood comparison

After R1, the independent route reproduced the landing. Package comparison then stopped on the
degree-two dense-grid minimum: the two values are approximately `-3.766906274e8` and differ by
`7.22e-4` (`1.92e-12` relative). This candidate already fails the registered positive-slope gate;
its grid approaches a zero-slope tidal pole, so a fixed `1e-7` absolute comparison is ill-scaled.

The only R2 change authorized is to compare the dense tidal extrema with
`absolute_tolerance=1e-7` plus `relative_tolerance=5e-10`. Coefficients, chi-square, derivative
minimum, classifications, knot values, scale-invariance checks, candidate order, and landing keep
their original tolerances and formulas. R2 may not suppress or relabel the noninvertible candidates.
