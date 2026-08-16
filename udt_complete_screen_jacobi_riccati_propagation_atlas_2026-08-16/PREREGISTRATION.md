# Preregistration — complete screen Jacobi/Riccati propagation atlas

Date: 2026-08-16  
Phase: preregistered before production or independent outcome generation

## Whole question

On a supplied regular observer-pair branch, does exact metric-derived screen propagation replace
G107's remaining constant screen-dilation parameter with the gauge-invariant rate

\[
a_{\rm eff}(\delta)=\frac12\frac{d\log \mathcal A_\perp}{d\delta},
\]

or does independent screen-volume freedom remain after the metric history, query, branch, initial
screen data, affine parameter, and monotone reciprocal-depth map are all supplied?

## Exact bounded regime

- one supplied smooth complete Lorentz metric history and its full Levi-Civita curvature;
- one supplied regular observer query and branch `gamma(lambda)`;
- a positive rank-two screen bundle and a regular `2x2` screen Jacobi map away from coincidence,
  caustics, focal points, and cut-locus branch changes;
- the exact complete-pair screen block `W=Q(SY+Z)`;
- an affine parameter `lambda` and a supplied monotone depth `delta(lambda)` with
  `d delta/d lambda != 0` on the tested interval;
- full nonlinear Jacobi and Riccati matrices, without a weak-field or first-order truncation;
- constant analytic tidal controls plus saved-field recomputation of the outcome-blind 21-row G68
  control ensemble;
- no BOSS, BAO, CMB, SNe, or other observational outcomes opened.

## Method classification

Metric-led conditional propagation. This is not a history selector, observational fit, action,
source law, bootstrap law, or imported GR field equation. Levi-Civita/Jacobi geometry is used only
as the differential geometry of the supplied metric.

## Exact objects

Let the physical screen map in an orthonormal screen frame be `W(lambda)`. Define

\[
\mathcal A_\perp=|\det W|,\qquad
L=\dot W W^{-1},\qquad
\theta=\operatorname{tr}L.
\]

For monotone `delta(lambda)`, preregister

\[
a_{\rm eff}=\frac{\theta}{2\dot\delta}.
\]

The calculation must prove or falsify that this equals one half of the logarithmic screen-area
derivative. It must also derive the exact reparameterized Riccati trace equation rather than assume
that `a_eff` is constant.

## Declared control families

1. isotropic defocusing: `R_screen=-kappa^2 I`, `W(0)=I`, `Wdot(0)=0`;
2. isotropic focusing: `R_screen=+kappa^2 I`, same initial data, restricted before its first caustic;
3. mixed anisotropic: `R_screen=diag(-p^2,+q^2)`, same initial data;
4. arbitrary smooth left screen rotation of each control, used only as a gauge mutation;
5. exact coframe/realization redistributions with fixed product `W=QN`, where `N=SY+Z`;
6. all 21 saved regular G68 endpoint maps, recomputed only from saved `D`, `Ddot`, and affine
   endpoint values.

The analytic controls use positive generic constants fixed before evaluation; their numerical
values are numerical controls, not physical constants.

## Premise and value ledger

| Item | Status |
|---|---|
| founded reciprocal character on supplied ordered depth | `pinned-by-THEORY` |
| complete pair identity `W=Q(SY+Z)` | `pinned-by-THEORY`, conditional on supplied regular pair realization |
| Jacobi/Riccati propagation from supplied metric/query/initial data | `pinned-by-THEORY` as metric differential geometry |
| metric history, query, branch, screen, and initial data | `free-and-explored` / supplied |
| `delta(lambda)` | supplied and monotone; not selected |
| G68 profiles and endpoints | frozen prior outcome-blind controls, not physical histories |
| analytic control constants | numerical controls only |
| observational coefficients, regime locations, and data outcomes | omitted and sealed |

## Certification and falsification contract

The proposed identification fails if any regular declared control violates

\[
2a_{\rm eff}=\frac{d\log\mathcal A_\perp}{d\delta},
\]

if the exact Jacobi and Riccati constructions disagree, if a smooth screen-frame rotation changes
the area rate, or if a passive `Q/N` redistribution with fixed `W` changes it.

A positive bounded return requires:

1. exact derivation from `W=Q(SY+Z)` and the Jacobi equation;
2. exact analytic agreement for all declared constant-tidal controls;
3. independent numerical Jacobi-versus-Riccati agreement;
4. gauge-rotation and passive-factorization hostile tests;
5. saved-artifact recomputation on every regular G68 row;
6. explicit classification of coincidence, caustic, nonmonotone-depth, and branch failures.

## Maximum conclusion

At most:

```text
CONDITIONAL_SCREEN_DILATION_RATE_DERIVED_FROM_PROPAGATED_PAIR_AREA
__CONSTANT_A_IS_A_SPECIAL_PROPAGATION_SUBFAMILY
__SCREEN_ROTATION_REMAINS_ZERO_ORDER_GAUGE
__METRIC_HISTORY_QUERY_INITIAL_DATA_BRANCH_AND_DEPTH_MAP_REMAIN_SUPPLIED
```

No physical coefficient, unique history, regime score, observational pattern, `X_max` value,
source, action, matter, bootstrap, or signalling result can follow.
