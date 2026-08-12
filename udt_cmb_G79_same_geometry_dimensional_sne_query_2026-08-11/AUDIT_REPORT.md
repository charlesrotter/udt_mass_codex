# G79 audit report — same-geometry dimensional SNe query

Date: 2026-08-11

Status: `PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED`

## Landing

`DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY`

One outcome-independently selected G75/G77 control geometry has now produced, from the same full
metric and the same stationary observer query, both a reciprocal endpoint depth and an angular
distance.  P1 was not used to construct, tune, or select the geometry.

## What was learned

1. The exact stationary endpoint result is `1+z=sqrt(21)/4` and
   `phi_pair=log(sqrt(21)/4)`.
2. The full screen/Jacobi calculation gives `d_A/R=0.7559850215834019`; hence `d_A=R(d_A/R)`.
   The dimensionless sky relation cannot determine `R`.
3. A separate direct-Christoffel neighboring-ray calculation agrees with the full Jacobi matrix
   to `4.3838551044245423e-11` relative.
4. The old P1 distance has the same type only because its frozen assembly conditionally posits
   `d_A=r`.  The resulting one-point expression is compatibility algebra, not a fit.
5. A supplied thermal spectrum would inherit the same redshift factor, while the Jacobi map would
   remap source directions.  This is only a deferred typed route for `cmb_temp`, to be revisited
   after the dimensional SNe and/or `X_max` endpoint curve.  No source temperature field,
   last-scattering endpoint, whole-sky `z(n)`, or spectrum is derived here.

## Four evidence gates

1. **Preregistered:** yes, commit `4bea21b7`, before the selected profile was disclosed or the solve
   was run.
2. **Full or bounded:** complete for one exactly selected stationary profile/query and its full
   nonlinear null/screen/Jacobi equations; not the 591-profile family or a physical cosmic query.
3. **Independently verified:** yes locally, by a separately written direct-loop Christoffel and
   finite-difference neighboring-ray implementation; fresh zero-context adversarial review is
   still required before a final verified grade.
4. **Premises audited:** yes; physical choices and inactive downstream objects are listed in
   `PREMISE_LEDGER.tsv` and `TYPE_LEDGER.tsv`.

## Numerical gates

- source manifest: `16/16`;
- direct/analytic redshift difference: `2.886579864025407e-15`;
- production null residual: `1.4183200820413355e-15`;
- Killing-energy drift: `2.6645352591003757e-15`;
- screen Gram residual: `9.325873406851315e-15`;
- independent full-Jacobi relative difference: `4.3838551044245423e-11`;
- independent null error: `2.1058184982859585e-15`;
- endpoint: `ENDPOINT_REGULAR_NO_CAUSTIC`.

## Completeness map

This is one stationary-axial, one-profile, one-ray tile.  All metric coordinates, mixing, angular
screen, null path, screen transport, and Jacobi columns are live inside that tile.  It does not
cover other profiles, directions, endpoints, time-live histories, branches, source populations,
polarization, physical scale selection, global completion, action, matter, or stability.

## Authority boundary

No physical profile or endpoint is selected.  `x=1` is not `X_max`.  `R` remains symbolic.  No SNe
datum is fitted.  No CMB temperature or spectrum is predicted.  The seven protected stopped-draft
paths remain unread and untouched.

## Next gate after review

If this survives fresh review, continue the same-geometry dimensional SNe join and then the
physical `X_max`/endpoint-curve question as separately authorized.  Defer `cmb_temp` application
until that distance/redshift architecture is available, and keep its lenses-plus-redshift formula
conditional until a physical source and endpoint are owned.
