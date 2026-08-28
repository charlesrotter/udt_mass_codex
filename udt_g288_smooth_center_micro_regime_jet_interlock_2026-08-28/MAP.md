# G288 MAP — smooth-center micro-regime jet interlock

Date: 2026-08-28

## Whole question

When positive areal separation is taken inward through a negative-profile sector of the primary
UDT metric, does smooth-center regularity force the clock, acceleration, angular/tidal, curvature,
causal, and geometric mass-aspect channels to interlock, or do they remain freely specifiable?

This is not a Planck-scale fit.  It asks what the metric itself does before any absolute microscopic
scale is attached.

## Exact bounded regime

Use only

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

on an analytic even smooth-center germ

\[
f(r)=1+c_2r^2+c_4r^4+c_6r^6+\cdots.
\]

The radius remains positive away from the center.  Negative profile means \(\phi(r)<0\), not
negative distance and not reversed pair-arrow orientation.

## Frame

- `metric-led`: yes;
- `template-led`: no;
- whole frame: primary static-spherical reciprocal areal metric;
- bounded slice: one analytic even regular-center germ;
- observing, not targeting: classify exact coefficient dependence and onset order before attaching
  any physical micro scale.

## Inputs and status

- primary reciprocal areal metric: `DECLARED_READOUT / ACTIVE_BOUNDED`;
- \(f=e^{-2\phi}\): `DERIVED_PRESENTATION_IDENTITY`;
- smooth-center conditions \(f(0)=1\), \(f'(0)=0\): `DERIVED_BOUNDED_REGULARITY`;
- analytic even germ: `CHOSE_BOUNDED_METHOD`, not a physical-history premise;
- G201 angular channels: `DERIVED_CONDITIONAL`;
- G262 lapse/acceleration/mass-aspect hierarchy: `DERIVED_CONDITIONAL`;
- \(c_E\): `OBSERVED` clock/ruler calibration;
- the Planck length: omitted from the derivation; at most a future `OBSERVED_COMPARISON_MARKER`;
- all coefficients \(c_{2k}\): `FREE_AND_EXPLORED`.

## Omitted scope

No nonspherical or time-live coframe, completed arbitrary pair germ, source, matter, local rest
mass, physical total mass, action, field equation, carrier, fit, observations, quantum mechanics,
Planck cutoff, hard boundary, \(X_{\max}\), protected package, or physical history is imported.

## Evidence reset

No historical or recent audit formula is accepted as proof in G288.  `founding.md` and the exact
current premise registry supply the current metric/type declaration.  Every load-bearing curvature,
angular, acceleration, mass-aspect, and causal expression will be rebuilt directly from that metric.
The older packages in `SOURCE_SCOPE.tsv` are comparison targets only: if the fresh derivation
disagrees, G288 fails the inherited formula and records the conflict.

## Proposed bounded next action

Starting from the metric components, independently rebuild the inverse metric, connection,
curvature, orthonormal sectional channels, angular combinations, lapse acceleration, geometric
mass-aspect change of variables, and radial null normalization.  Only then derive the center
coefficient map.  Verify it by an implementation-distinct exact-arithmetic route and hostile
mutations.  Then state whether a genuine local universality class appears and exactly what remains
free.
