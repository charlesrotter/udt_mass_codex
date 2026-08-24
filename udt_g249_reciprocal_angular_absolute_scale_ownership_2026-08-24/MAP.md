# G249 map — reciprocal/angular absolute-scale ownership

Date: 2026-08-24

## Whole question

Does the G248 interlock between reciprocal clock rate and Jacobi area make the angular area an
absolute function of reciprocal depth because `phi=log(1+z)` is calibrated through `c_E`? Or does
the primary metric still retain a dimensional scale modulus after all dimensionless reciprocal and
angular-shape information is fixed?

This is an ownership audit. It does not target a desired observational scale and opens no
observational outcome.

## Dependency chain

```text
OBSERVED c_E + supplied ordered reciprocal depth
  -> dimension-matched clock coordinate x0=c_E t
  -> dimensionless clock ratio r_AB=exp(-delta_AB)

supplied smooth metric + supplied regular null branch
  -> curvature tidal operator T
  -> vertex-normalized Jacobi map D
  -> area A=abs(det D), shape C=(D^dagger D)/A

clock ratio + Jacobi area
  -> G248 ordered incidence coarea density (r_AB/A_AB)d_tau_A
```

The audit tests whether the first chain fixes the dimensional normalization of the second.

## Whole arena and bounded diagnostic

The abstract calculation uses any smooth one-parameter homothetic metric family and the complete
matrix Jacobi equation. The primary static-spherical metric is used only as an exact diagnostic
chart:

```text
g_R=-F(r/R)(c_E dt)^2+F(r/R)^(-1)dr^2+r^2 dOmega^2,
F>0, R>0.
```

No profile `F`, value of `R`, observer population, source, detector, transfer law, `X_max`, or
observational datum is selected.

## What is covered

- dimensional ownership of `c_E`, `phi`, redshift, Jacobi area, and the G248 coefficient `r/A`;
- exact homothety covariance of the metric, curvature tidal operator, full Jacobi map, area, and
  unit-determinant shape;
- local same-`phi` angular-tide counterexamples from the primary metric jets;
- the conditional one-anchor recovery of an absolute scale after a full dimensionless history and
  monotone regular branch are supplied.

## What is dropped

- physical history or profile selection;
- time-live/nonspherical solution-space classification beyond the general homothety theorem;
- nonmonotone branch aggregation, caustics, cuts, critical or infinite-image strata;
- source population, radiative transfer, luminosity, detector, catalogue, BAO/CMB/SNe outcomes;
- action, source, matter, bootstrap, mass, signalling, and numerical `X_max`.

## Maximum conclusion

The audit may classify whether `c_E` and reciprocal redshift remove the absolute angular scale
modulus. It may not identify a numerical scale, fit an anchor, select a physical metric history, or
turn G248 coarea into a probability or flux law.
