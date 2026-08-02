# Preregistered numerical certification parameters

Date: 2026-08-02  
Base preregistration: `c06eb8a6`  
Intrinsic-method refinement: `bf500492`

This append-only layer fixes numerical parameters before any finite-loop value or numerical
curvature-zero candidate has been computed. It does not weaken the exact global-zero requirement.

## Curvature-zero reconnaissance (non-certifying)

For each of `C04,C08,C09,C10`, use the exact intrinsic curvature expression divided by its proved
positive real denominator on the unit sphere. Run `1024` deterministic `numpy` normal starts with
seed `20260802`, each normalized to `S3`, using four residuals: the three curvature components and
`q0^2+q1^2+q2^2+q3^2-1`.

Use SciPy `least_squares`, `max_nfev=3000`, and `ftol=xtol=gtol=1e-13`. Retain a diagnostic
candidate only when the maximum absolute residual is at most `1e-10` and the exact defect measure
evaluates above `1e-12`. Cluster retained candidates by antipodal-invariant Euclidean separation
`1e-7` and preserve every cluster. Failure to find a root proves nothing. Found candidates guide
exact decomposition but are not a completeness certificate.

## Primary finite-loop quadrature

- arithmetic: `mpmath`, `100` decimal digits;
- orientation: increasing registered parameter `t` from `0` to `2*pi`;
- periodic trapezoid panels: `256,512,1024,2048`;
- convergence gate: the `1024`/`2048` absolute difference is at most
  `max(1e-70,1e-65*abs(H_2048))`;
- otherwise the integral remains `UNRESOLVED_NUMERICAL` without retuning.

## Independent finite-loop quadrature

Use a separate implementation of the quaternion path, coframe contraction, profiles, and
connection with `mpmath` at `120` decimal digits and tanh-sinh adaptive quadrature. Agreement with
the primary value requires absolute difference at most `max(1e-70,1e-65*abs(H_primary))`.
Orientation reversal must independently return `-H` to the same bound.

Exact `C16=4*C08` and `C17=5*C08` connection/curvature scaling is proved algebraically first and
then replayed on every loop. Decimal agreement cannot substitute for the exact identity.

All loop values remain `OBSERVED_HIGH_PRECISION` unless a separate rigorous interval certificate
excludes zero. No decimal pattern, near-equality, or apparent zero is promoted to an exact claim.
