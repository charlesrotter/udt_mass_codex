# G346 map — directional angular-area reciprocity

Date: 2026-09-04
Status: preregistration stage

## Whole question

Starting only from G342--G345, does the supplied metric determine the two directional infinitesimal
Jacobians

```text
metric screen area at endpoint 1 / metric celestial solid angle at endpoint 0
metric screen area at endpoint 0 / metric celestial solid angle at endpoint 1
```

on each fixed labelled null ray? If so, does endpoint reversal relate them by the already-derived
metric frequency ratio, is the inverse G345 symmetric scalar exactly their geometric mean, and how
do they sew through a stationary intermediate screen?

This is `METRIC_LED` and observing rather than targeting. It attaches the G342/G343 Jacobi map to
the metric sky and metric screen area structures already present at its endpoints. It does not add
brightness, flux, luminosity, probability, an electromagnetic field, a detector response, an
observational-distance convention, a path population, a source, an action, a scale, or an
observational datum.

## Exact bounded arena

Use one supplied G323/G324 Taub/Kasner spacetime, the supplied G340 normal-observer congruence, one
supplied fixed labelled G340--G345 null ray and compact lift, arbitrary distinct positive endpoint
times, all projective directions including both principal limits, and the complete two-screen
bilocal position block `B_10`. Every common positive affine rescaling, endpoint unit-frequency
reset, marked ray event, and arbitrary invertible passive endpoint screen-coordinate change remains
live.

At endpoint `i`, let `q_i` be the positive metric screen form and
`omega_i=-g(k,n_i)>0`. A small celestial direction vector `theta_i` at fixed observer-measured
frequency is converted into canonical Jacobi opening by the metric musical map

```text
p_i = omega_i q_i theta_i.
```

The corresponding infinitesimal metric solid angle and endpoint screen area are

```text
dOmega_i = sqrt(det q_i) d^2 theta_i,
dA_i     = sqrt(det q_i) d^2 x_i.
```

No radiative intensity or source luminosity is involved in either definition.

## Frozen candidate objects

At fixed source position `x_0=0`, `x_1=B_10 p_0`. Test

```text
J_1<-0 = dA_1/dOmega_0
       = omega_0^2 abs(det B_10) sqrt(det q_1 det q_0),

J_0<-1 = dA_0/dOmega_1
       = omega_1^2 abs(det B_01) sqrt(det q_0 det q_1).
```

In one common affine gauge G343 gives `B_01=-B_10^T`. Freeze

```text
J_1<-0 / J_0<-1 = (omega_0/omega_1)^2,
sqrt(J_1<-0 J_0<-1) = 1 / Dhat_10,
```

where `Dhat_10` is exactly G345's accepted observer-calibrated scalar.

For three endpoints in one common affine gauge, freeze the stationary sewing candidate

```text
J_2<-0 = hhat_1 J_2<-1 J_1<-0,
hhat_1 = abs(det H_1)/(omega_1^2 det q_1).
```

Naive multiplication without `hhat_1` is an explicit hostile alternative.

## Pure and easy routes

- Pure route used here: derive the sky-opening musical map, solid-angle form, screen-area form,
  reversal, and sewing directly from the G342--G345 metric and canonical endpoint blocks.
- Easier but forbidden as proof: quote angular-diameter distance, Etherington reciprocity, Van
  Vleck, geometric optics, inverse-square flux, or luminosity formulas and identify the result by
  familiarity.

## Required classifications

1. Derive both directional Jacobians in arbitrary endpoint `GL(2)` screen coordinates and separate
   positive area ratios from oriented determinant signs.
2. Prove or refute invariance under common affine rescaling, marked-event conversion, and passive
   screen-coordinate changes.
3. Prove or refute the squared frequency-ratio reversal law in both one common affine gauge and
   separately source-normalized endpoint gauges.
4. Prove or refute that the inverse G345 scalar is the exact geometric mean, not merely a matching
   principal-limit expression.
5. Derive the stationary sewing law for all nonidentity endpoint triples and explicitly reject bare
   scalar multiplication.
6. Recover mixed-direction, longitudinal, transverse, and coincidence formulas without deleting a
   screen direction.
7. Retain every compact lift separately. No route sum, weight, preferred path, or population may
   appear.
8. State exactly what remains observer-, ray-, path-, and spacetime-dependent. A metric angular-area
   Jacobian must not be promoted to brightness, luminosity, or a selected observational distance.

## Maximum conclusion

At most G346 may derive two positive directional infinitesimal metric angular-area Jacobians on the
supplied G340--G345 observer/ray family, their exact frequency-ratio reversal, their G345 geometric
mean, and typed stationary sewing. It may not establish a finite-beam law, brightness, flux,
luminosity, probability, amplitude, native electromagnetic theory, selected observational distance,
physical route or observer population, generic spacetime theorem, stability, matter/mass, physical
scale, `X_max`, or canon.
