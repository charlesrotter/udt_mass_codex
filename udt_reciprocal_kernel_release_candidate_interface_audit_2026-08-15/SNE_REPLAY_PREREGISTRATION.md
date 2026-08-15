# Preregistration — one complete-geometry SNe curve with provisional radiative transfer

Date: 2026-08-15
Mode: metric-led, CPU, no profile fitting, no `X_max` identification

## Whole question

What redshift/angular-distance/luminosity-distance curve does the already preregistered G79 control
geometry produce when its source endpoint is swept over the Pantheon+ redshift range, and how does
that fixed curve compare with the frozen SNe magnitude/covariance data after only one additive
magnitude offset is profiled out?

This is one bounded complete-query tile. It is not a search over geometries and not a physical
history selection.

## Frozen geometry and query

- `pinned-by-THEORY` for this replay: the G79 outcome-independent control
  `A(x)=1-x^2/4`, `h(x)=x^6/20`, chosen before its SNe output existed.
- `CHOSE_CONTROL`: receiver `x=1/4`, stationary Killing observer, outward equatorial radial member
  of its complete orthonormal sky.
- `free-and-evaluated`: source endpoint `x_s`, determined pointwise from each observed `z` through
  the same geometry's exact endpoint relation, not fitted.
- `OBSERVED`: reciprocal calibration `c_E`; it cancels from the dimensionless curve.
- `OPEN_FREE`: overall length/magnitude calibration; represented by one analytically profiled
  additive offset only.
- `POSIT__CONDITIONAL`: the two statements in `PROVISIONAL_RADIATIVE_INTERFACE.md`, hence
  `d_L=Z^2 d_A` on the regular branch.
- `CHOSE_OBSERVATIONAL_INPUT`: frozen Pantheon+SH0ES table and full covariance, noncalibrators with
  `zCMB>0.023`, matching the registered G65 primary data layer.
- `CHOSE_COMPARISON`: applying this one-ray relation to the all-sky sample characterizes curve
  compatibility only; it is not a derived isotropy or sky-averaging theorem.

No SNe outcome, P1 parameter, `X_max`, bootstrap value, opacity coefficient, action, source term,
or matter parameter may change the geometry or query.

## Computation

1. Integrate the full nonlinear null path, parallel screen, curvature, and two-column Jacobi system
   once to the largest required source endpoint.
2. Evaluate the dense solution at every observed redshift using
   `Z=1+z=sqrt(A_receiver/A_source)` and the monotone source position.
3. Form `d_A/R=sqrt(abs(det D))` and the provisional `d_L/R=Z^2 d_A/R`.
4. Profile one additive magnitude offset using the full covariance. Do not fit the curve shape.
5. Only after freezing the result, compare its chi-square with the frozen P1 compatibility anchor.

## Certification contract

- every observed source endpoint must lie in `x_receiver<x_s<2` with positive lapse;
- monotone outward path and no caustic over the sampled range;
- maximum null residual `<1e-8`, screen Gram/ray residual `<1e-7`, Killing-energy drift `<1e-8`;
- two production step controls must agree in `d_A/R` to relative `<2e-7` over all data points;
- an implementation-distinct direct-Christoffel neighboring-ray calculation at fixed redshifts
  `0.03,0.10,0.50,1.00,2.00` must agree with the Jacobi curve to relative `<3e-4` where in range;
- an independent likelihood calculation from the saved curve must reproduce the offset and
  chi-square within `2e-6` and `2e-4` respectively;
- hostile mutations must catch removal of either provisional transfer premise and any fitted change
  to the frozen geometry.

Failure of a certification gate is a solver/evidence failure, not a physics verdict. Any regular
curve and residual pattern is retained; no lower-chi-square acceptance filter is allowed.

## Maximum conclusion

At most:

```text
OBSERVED_CONDITIONAL_ONE_CONTROL_GEOMETRY_SNE_CURVE
__PROVISIONAL_TRANSPARENT_NULL_CARRIER_INTERFACE
__NO_HISTORY_XMAX_EM_OR_PARTICLE_CLOSURE
```

No fit superiority, unique universe, native luminosity law, all-sky theorem, `X_max`, CMB result,
action, source, carrier emergence, matter, mass, or bootstrap selection can follow.
