# Audit report — complete screen Jacobi/Riccati propagation atlas

Date: 2026-08-16
Status: `EXTERNALLY_VERIFIED_WITH_CAVEATS__REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS`

## Landing

```text
CONDITIONAL_SCREEN_DILATION_RATE_DERIVED_FROM_PROPAGATED_PAIR_AREA
__WHEN_QUERY_IDENTIFIES_THE_COMPLETE_PAIR_SCREEN_WITH_THE_JACOBI_MAP
__CONSTANT_A_IS_A_SPECIAL_PROPAGATION_SUBFAMILY
__SCREEN_ROTATION_REMAINS_ZERO_ORDER_GAUGE
__NO_INDEPENDENT_SCREEN_AMPLITUDE_REMAINS_AFTER_W_DELTA_AND_INITIAL_DATA_ARE_SUPPLIED
__METRIC_HISTORY_QUERY_INITIAL_DATA_BRANCH_AND_DEPTH_MAP_REMAIN_SUPPLIED
```

When a supplied regular Jacobi-type observer query identifies the same complete pair-screen block
with its physical Jacobi map, that block is

\[
W=Q(SY+Z),
\]

and its area is `A_perp=|det W|`. The G107 screen weight becomes

\[
a_{\rm eff}=\frac12\frac{d\log A_\perp}{d\delta}
=\frac{\operatorname{tr}(\dot W W^{-1})}{2\dot\delta}.
\]

Therefore, after the metric history, query, branch, initial screen, and depth map are supplied,
there is no additional screen-volume coefficient to fit. The coframe and pair-realization pieces
can compensate separately; Jacobi propagation fixes their physical product.

The result is not a universal distance-only law. Generic complete geometry leaves direction,
shear, curvature, branch, initial-data, and depth-reparameterization dependence. The constant G107
`a` is the special case in which the logarithmic area is affine in `delta` and the isotropic
extension assumptions also hold.

## Gates

1. Preregistered before production/independent outcomes: yes.
2. Full space: complete for the declared regular local rank-two Jacobi/Riccati identities and
   analytic constant-tidal control families; not a function-space or global branch census.
3. Independent verification: separate Jacobi and Riccati integrations, analytic controls, hostile
   gauge/factorization/depth mutations, and all 21 saved G68 endpoints pass.
4. Fresh external review: accepted the conditional derivation and required three
   non-outcome-changing repairs. A fresh sealed follow-up verified the exact repairs and returned
   `REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS` with no remaining defect.
5. Premise audit: pending repository-wide verifier before banking.

## Maximum conclusion

The screen-volume rate is a conditional output of complete metric propagation, not an independent
coefficient, once all propagation inputs are supplied. The current foundations still do not select
those physical inputs or a cosmological history. No BAO/CMB/SNe outcome, score, `X_max`, bootstrap,
source, action, matter, or signalling conclusion follows.
