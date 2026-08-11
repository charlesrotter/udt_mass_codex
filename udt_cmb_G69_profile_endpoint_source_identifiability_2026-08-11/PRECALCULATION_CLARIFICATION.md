# G69 precalculation clarification

Date: 2026-08-11

This clarification is registered after the primary preregistration commit `8b7340cb` but before
writing or running the atlas derivation. It changes no profile, endpoint, source control, allowed
landing, or authority boundary.

For each F02 shape and registered sensitivity endpoint:

1. The sensitivity center is the arithmetic midpoint of the readout vectors at the two registered
   amplitudes `epsilon=1/20` and `epsilon=1/5`; no new `epsilon=1/8` metric is synthesized.
2. The endpoint and lapse columns are the arithmetic means of their respective finite-difference
   columns at those two registered amplitudes.
3. The amplitude column is the secant between the two registered amplitudes.
4. The raw matrix columns are derivatives with respect to `(x,a,epsilon)` in that order.
5. The scale-normalized matrix is formed by dividing each nonzero raw column by its Euclidean norm.
   A zero column gives infinite condition number. No result-dependent row scaling is allowed.
6. Numerical rank is classified by `sigma_min/sigma_max` of the column-normalized matrix:
   - greater than or equal to `1e-6`: `FULL_RANK_OBSERVED`;
   - less than or equal to `1e-8`: `RANK_DEFICIENT_OBSERVED`;
   - between those thresholds: `RANK_NUMERICALLY_UNRESOLVED`.
7. An independent `CubicSpline` reconstruction must agree with the production monotone-PCHIP
   intermediate `D` maps within `2e-7` relative over all 315 cells. This is an interpolation-method
   check, not independent path integration.

The rank remains a coordinate- and tile-scoped numerical observation. It cannot select a physical
parameter or override the exact source-covariance non-identifiability statement.
