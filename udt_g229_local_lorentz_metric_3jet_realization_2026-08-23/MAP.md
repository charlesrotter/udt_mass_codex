# G229 map — local Lorentz-metric 3-jet realization

Date: 2026-08-23

## Whole question

G227 reconstructs a supplied algebraic curvature tensor at one event. G228 classifies the exact
differential-Bianchi restrictions on its supplied first variation. G229 asks the next typed
question:

> Does every G227/G228-compatible pair `(R,nabla R)` actually occur as the curvature value and
> first curvature derivative of a Lorentz metric in normal coordinates near that event?

This is metric-led reconstruction, not a search for a desired physical profile.

## Lay picture

Curvature data are like a proposed bend and first change of bend at one point. Algebraic
compatibility says the proposal is internally consistent. Metric-jet realization asks whether one
can build an actual local piece of metric whose bend has exactly those values.

Ordinary locally inertial coordinates contain much more Taylor data than curvature can hear. That
extra data may be coordinate labeling rather than new geometry. G229 therefore keeps two ledgers:

1. the full locally inertial metric Taylor coefficients and their coordinate-gauge kernel;
2. the geodesic-normal-coordinate slice, where the gauge is fixed and curvature data should become
   the remaining coefficients.

## Bounded arena

- one supplied event;
- four-dimensional real Lorentz signature `(-,+,+,+)`;
- a fixed tangent frame at the event;
- metric Taylor data only through cubic order;
- curvature value `R` and first covariant derivative `D=nabla R` only;
- exact rational linear algebra;
- no field equation, source, action, boundary, observer population, or global history.

## Whole-space accounting

With `g(0)=eta` and `partial g(0)=0`:

- `g_(ab,cd)` has `10*10=100` coefficients;
- `g_(ab,cde)` has `10*20=200` coefficients;
- an algebraic curvature tensor has dimension 20;
- a differential-Bianchi-compatible first curvature derivative has dimension 60 by G228.

The preregistered question is whether the respective `80` and `140` remainders are exactly
coordinate freedom and whether geodesic normal gauge leaves isomorphic `20`- and `60`-dimensional
metric-jet slices.

## Dropped criteria

This tile does not cover a finite neighborhood of prescribed curvature functions, overlapping
event jets, topology, cuts, global holonomy, dynamics, stability, sources, matter, bootstrap,
`X_max`, transfer, observations, mass, or signalling. Any of those may contain further
restrictions. A local existence result is not a physical-history law.
