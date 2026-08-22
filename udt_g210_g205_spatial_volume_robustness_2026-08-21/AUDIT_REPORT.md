# G210 audit report — spatial-volume robustness

Date: 2026-08-21

## Landing

```text
FULL_LOCAL_SPATIAL_VOLUME_SCALAR_IS_THE_UNIQUE_RELATIVE_DETERMINANT_MODE
__IT_RESCALES_CAUSAL_WIDTH_WITHOUT_MOVING_THE_SHIFT_CENTER
__LOWER_BOUNDED_STATIC_AND_CONTROLLED_COMPACT_LIVE_G205_CLASSES_SURVIVE
__SIGMA_EQUALS_MINUS_PHI_IS_GLOBALLY_HYPERBOLIC_BUT_RADIAL_NULL_INCOMPLETE
__COMPLETED_PAIRS_HEAR_SPATIAL_VOLUME_BEFORE_READOUT_ON_SPATIAL_BEARING_STRATA
__NO_PHYSICAL_SIGMA_HISTORY_OR_XMAX_SELECTION
```

## Result

Relative to a supplied positive spatial reference metric, every positive spatial metric has one
unique determinant scalar

\[
\sigma=\frac16\log\frac{\det K}{\det H}
\]

and a determinant-one remainder. Turning on only this scalar preserves Lorentz signature and
temporal `dt`, changes ambient volume by `exp(6 sigma)`, leaves the G209 shift center fixed, and
rescales every causal width by `exp(-sigma)`.

On the supplied G205 family, every smooth static globally lower-bounded `sigma` is globally
hyperbolic and null complete. A lower-bounded compact-time-live class with bounded time derivative
also survives. The exact smooth control `sigma=-phi` remains globally hyperbolic but compresses an
outgoing radial null geodesic to finite affine length.

Completed pairs hear the mode before reciprocal readout whenever their clock has spatial content;
unshifted static and Eulerian-normal clocks are lawful blind strata.

## Status

This closes one local metric degree of freedom and bounded G205 global subclasses. It does not
select a spatial-volume profile, lapse, arbitrary determinant-one history, physical universe,
transfer law, or `X_max`. The global theorems are analytic; finite scripts certify algebra and
boundary anchors only.

## Evidence gates

- Preregistered: **PASS** (`d1458d37`, pushed before outcomes).
- Full space or bounded scope: **PASS WITH CAVEATS** (whole local scalar; declared global classes).
- Independent finite-dimensional verification: **PASS** (10,000 distinct exact cases and 250,001
  assertions; no production import).
- High-precision boundary controls: **PASS** (four profiles at 120 digits).
- Premise audit: **PASS** (193-row registry before solve).
- Hostile catches: **PASS** (25 determinant, cone, affine, pair, and scope mutations).
- Fresh external adversarial review: **PASS WITH CAVEATS** (`VERIFIED_WITH_CAVEATS`; all 35
  scoped payload hashes and the registered no-write replay passed; no mathematical refutation and
  no repairs required). The reviewer retained the bounded landing while confirming that finite
  scripts independently verify only the local algebraic core, not the global analytic theorems.
