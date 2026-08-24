# G243 numerical-stability repair preregistration

Date: 2026-08-24

Status: `PREREGISTERED_AFTER_DIAGNOSTIC_FAILURE__BEFORE_EXACT_NULLSPACE_REPAIR`

## Observed stop

The original whitened production route and independent direct-precision route selected the same
interior candidate, the same turning classification, and coefficients agreeing much more tightly
than the preregistered `1e-8` selected-coefficient gate. However, some deliberately extreme
large-alpha census rows missed the preregistered absolute `1e-7` raw-chi-square agreement gate.
The largest original miss was about `0.198` at `K=24`, `log10(alpha)=12`.

An unbanked diagnostic that numerically diagonalized the semidefinite penalty reduced but did not
eliminate the problem. After clipping its three smallest numerical eigenvalues, the largest
raw-chi-square miss was about `7.21e-5` at `K=64`, `log10(alpha)=12`. That diagnostic is not
accepted evidence.

## Exact cause and registered repair

The second-derivative penalty has an algebraically exact three-dimensional nullspace:

1. the Pantheon release offset;
2. the DES release offset;
3. the anchored affine spline shape.

At the extreme registered alpha values, treating these exact zeros as floating-point eigenvalues
multiplies roundoff by as much as `1e12`.

The only authorized repair is to construct the three null vectors analytically, use a complete QR
basis to split null and penalized coordinates, eliminate the three unpenalized coordinates by an
exact block Schur complement, and solve only the positive penalized block spectrally. Production
must whiten its already frozen block design before this reduction. The independent route must
continue to assemble Pantheon covariance-solve and DES marginal-precision-Schur normal equations
and perform its own generalized symmetric eigensolve.

## Frozen items

The following may not change:

- data, cuts, covariance policy, basis counts, alpha grid, penalty, or GCV definition;
- the `1e-7` all-candidate raw-chi-square and GCV agreement gates;
- the `1e-8` selected-coefficient agreement gate;
- the lack of monotonicity enforcement;
- the SNe-only closure against angular and BOSS outcomes;
- any landing or interpretation.

## Return

- If every registered candidate satisfies the original chi-square/GCV gates, the exact-nullspace
  repair is mechanical and the preregistered scientific landing may be evaluated.
- Otherwise return `CROSS_ROUTE_OR_FULL_COVARIANCE_FAILURE__NO_FREEZE`.

No failed or diagnostic output may be silently discarded; this document is the chronology record.
