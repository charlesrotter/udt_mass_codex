# Metric-native observer-separation asymptote audit

Date: 2026-07-24

Preregistration commit: `2872f58`

Compute: exact CPU algebra; no GPU, ODE/PDE, fit, action, or matter solve

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's proposed route is substantially correct, with one necessary
qualification:

> Once a complete physical metric branch and its observer-rest geometry are
> supplied, the separation corresponding to clock dilation is directly
> calculable from the metric. It need not be `tanh`.

The exact metric-native object is the spatial squared gradient of reciprocal
depth,

```text
B = h_u^-1(dphi,dphi),
```

where `h_u` is the positive observer-rest geometry obtained from the
complete coframe, including every angular and shift term. If physical
distance is a single-valued function of clock depth, the distance eikonal
equation forces

```text
dD/dphi = 1/sqrt(B(phi)).
```

Accordingly, the infinite-dilation depth reach is

```text
X_phi = integral(phi0,infinity) dphi/sqrt(B(phi)).
```

This is a direct consequence of the metric. The integral may converge or
diverge; the answer is decided by the complete branch's `phi` gradient.

## The newly exposed selector gate

A universal `D(phi)` exists only if `B` is positive and is a function of
`phi` alone on the relevant branch. If `B` varies around a common `phi`
level, the angular/shift sectors make distance path-dependent. Thus the
complete metric gives an exact, falsifiable criterion:

```text
TRANSNORMAL:
h_u^-1(dphi,dphi)=B(phi)>0.
```

This criterion was not present in the earlier `tanh` discussion. It is the
smallest metric-native join currently visible between clock dilation and
physical separation.

## Complete-coframe result

For the registered ten-slot triangular coframe, imposing only the supplied
observer's clock-horizontal condition gives

```text
dell^2
 = (w dx1)^2
 + (k2 dx1+r dx2+e dx3)^2
 + (k3 dx1+t dx3)^2,
```

with

```text
k2=r a21+e a31-(b/u)(r a20+e a30),
k3=t[a31-(b/u)a30].
```

Its determinant is `w^2 r^2 t^2>0`. The exact `B` contains all angular
derivatives and every base/screen shift. This is the requested
`phi`-angular orchestra in the distance law, not a radial truncation.

## What happens in the conditional WR-L slice

For

```text
A=exp(-2phi)=1-r/X,
```

the direct radial proper distance is

```text
D(phi)=2X[1-exp(-phi)]
```

and its infinite-dilation endpoint is `2X`.

That fixed metric simultaneously has:

- coordinate endpoint `X`;
- proper radial endpoint `2X`;
- infinite optical depth; and
- projective `tanh` endpoint `X`.

They are inequivalent metric/readout objects. In particular, `tanh(phi)` is
not the WR-L proper-distance law.

## Why this does not yet yield global `X_max`

Two independent obstructions survive.

First, the reciprocal block fixes the clock/ruler imbalance but not the
profile. Exact controls with the same ordinary anchor and same local
calibration realize bounded `tanh`, bounded exponential, and unbounded
linear proper-distance laws. The selected complete branch must determine
`B`.

Second, the maximum separation between any two observers is a global
diameter, not merely a radial depth. Exact complete product controls have
the same clock law and same finite radial asymptote but different angular
radii and therefore different global diameters. Angular/global completion
must be included.

The current complete metric parent is a configuration class, not one
selected complete solution. It therefore supplies the evaluator and the
certification gate, but not yet the numerical global result.

## Observer and ontology scope

The spatial geometry `h_u` requires a supplied observer clock leg or
congruence and an event-pairing convention. The founding reciprocal coframe
supplies this in the declared pair, but the full nonspherical/time-live
assembly and symmetric global pairing remain open. Observer reciprocity
requires covariance of the construction; it does not make different
simultaneity pairings identical.

Absolute distance also requires the calibrated physical metric. A constant
common rescaling preserves clock ratios but rescales `D` and its asymptote.
The strong local-CSN premise was recently shown to be an owner postulate,
not derived. This audit therefore uses the calibrated physical-metric
ontology as `WORKING`, while retaining the conformal branch as a
countercontrol.

## Status rulings

- reciprocal clock factor `exp(phi)`: `DERIVED_CONDITIONAL`;
- complete clock-horizontal spatial quadratic form:
  `DERIVED_CONDITIONAL_ON_SUPPLIED_CLOCK_LEG`;
- transnormal distance law: `DERIVED`;
- finite infinite-dilation depth: `CONDITIONAL_INTEGRAL_TEST`;
- `tanh` as physical distance: `NOT_DERIVED`;
- WR-L proper endpoint `2X`: `DERIVED_CONDITIONAL_IN_WRL_SLICE`;
- clock dilation alone fixing global `X_max`:
  `REFUTED_IN_CURRENT_CONFIGURATION_CLASS`;
- unique `D(phi)` in the current complete parent: `OPEN_NOT_SELECTED`;
- equality of `X_phi` with the global observer-pair diameter:
  `OPEN_GLOBAL_JOIN`;
- numerical `X_max`: `NOT_YET_EVALUABLE`;
- use of `G_obs`: not needed for the kinematic extraction; reserved for
  later independent mass/density/bootstrap consistency.

## Evidence

- preregistered source, premise, candidate, and falsification universe;
- 39 exact SymPy checks;
- 30 independent standard-library/Fraction checks;
- 10/10 exercised corruption catches;
- three same-anchor radial profile controls;
- four inequivalent readings in one fixed WR-L metric;
- exact complete-coframe pullback and inverse-metric agreement;
- exact angular/global diameter countercontrol;
- exact observer-pairing and common-scale controls.

No fresh external-model review was authorized, so the grade remains
`VERIFIED-WITH-CAVEATS`.

## Maximum conclusion

```text
THE_COMPLETE_COFRAME_DERIVES_AN_EXACT_TRANSNORMAL_DISTANCE/ASYMPTOTE
EVALUATOR FROM PHI AND ALL ANGULAR/SHIFT SECTORS.

THE_CURRENT CONFIGURATION PARENT DOES NOT YET SELECT THE COMPLETE
BRANCH, CLOCK/EVENT PAIRING, OR GLOBAL-DIAMETER JOIN NEEDED TO TURN
THAT EVALUATOR INTO A NUMERICAL UNIVERSAL X_MAX.
```

No action, source, carrier, mass, density, boundary charge, canon, or
navigation control is changed.
