# G209 audit report — time-space shift robustness

Date: 2026-08-21

## Landing

```text
FULL_LOCAL_TIMESPACE_SHIFT_IS_AN_EXACT_INDEPENDENT_METRIC_SECTOR
__IT_TRANSLATES_THE_CAUSAL_ELLIPSOID_WITHOUT_CHANGING_SIGNATURE_OR_AMBIENT_DETERMINANT
__GROWTH_CONTROLLED_AND_UNIFORMLY_SUBLUMINAL_G205_CLASSES_SURVIVE
__A_SMOOTH_BOUNDED_COORDINATE_SHIFT_CAN_PRESERVE_GLOBAL_HYPERBOLICITY_WHILE_DESTROYING_NULL_COMPLETENESS
__COMPLETED_PAIRS_HEAR_SHIFT_BEFORE_READOUT
__NO_PHYSICAL_SHIFT_HISTORY_OR_XMAX_SELECTION
```

## Result

For every supplied positive spatial metric `h_A`, the full three-component time-space shift enters
exactly as

\[
g_b(\alpha\partial_t+v,\alpha\partial_t+v)
=-f\alpha^2+h_A(v+\alpha b,v+\alpha b).
\]

It preserves Lorentz signature, ambient determinant, and temporal `dt`. It translates the causal
velocity ellipsoid by `-b`; the supplied spatial metric controls the ellipsoid's shape and width.
Thus shift is a complete independent local sector and does not require trace-changing spatial shape
to be frozen first.

On G205:

- a radial growth condition is sufficient for `t` to remain Cauchy;
- every uniformly metric-subluminal smooth static shift is null complete;
- compact-time-live shifts with the stated relative magnitude and derivative bounds are null
  complete;
- the smooth bounded-coordinate radial shift
  `b(r)=v r/sqrt(R^2+r^2)` remains globally hyperbolic but is null incomplete for nonzero angular
  momentum.

The last witness proves that global hyperbolicity and null completeness do not move in lockstep.
It also proves that a bounded coordinate shift is not the same as a uniformly subluminal shift in
the physical spatial norm.

For supplied pair tangents, the shift enters the complete pair pullback before the clock norm and
completed reciprocal scalar are read. Coordinate-static and generic germs hear it; the
Eulerian-normal germ is a lawful blind stratum because it moves with the translated causal center.

## Status

This is a metric-led conditional classification, not a selected UDT shift or history. The global
theorems are restricted to the declared G205 subclasses. They do not classify arbitrary live
shifts, timelike/spacelike completeness, lapse freedom, trace-changing/full spatial histories,
maximal extension, observations, transfer, matter, or `X_max`.

## Evidence gates

- Preregistered: **PASS** (`b5c40cc2`, pushed before outcomes).
- Bounded scope: **PASS** (whole local sector; explicit G205 global subclasses).
- Independent finite-dimensional verification: **PASS** (10,000 exact-rational cases, no
  production import).
- Premise audit: **PASS** (192-row registry before the solve).
- External adversarial review: **PASS WITH CAVEATS** (`VERIFIED_WITH_CAVEATS`; all 33 hashes and
  registered replay passed; no mathematical refutation).
- Repair-only external follow-up: **PASS**
  (`G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`; all 37 scoped payload hashes and the
  registered no-write replay passed).

The reviewer requested two bounded repairs: expose the compact-slab extension step in the analytic
global proofs and fix one TeX typo. Both were registered and accepted without changing the
scientific landing.
