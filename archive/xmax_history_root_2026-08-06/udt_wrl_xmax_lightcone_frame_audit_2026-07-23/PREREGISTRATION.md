# Preregistration: WR-L/Xmax light-cone and observer-frame audit

Date: 2026-07-23

Base:
`3f549f4110eeeadf0c80047be5258af6a5fe1c5c`

Compute: CPU-only exact algebra; no GPU

## Whole question

On the recorded reciprocal static/spherical WR-L branch

```text
ds2 = -A(r)c_E2 dt2 + A(r)^-1 dr2 + r2 dOmega2,
A(r) = 1-r/X,
0 < r < X,
```

what causal and observer-frame structure is derived by the metric itself?

The audit will determine:

1. the exact radial null characteristics and optical coordinate;
2. whether the `r=X` surface is null and invariant under changes of
   orthonormal observer frame;
3. the distinction between static coordinate/clock unattainability and
   crossing by a regular nonstatic observer;
4. the most general local radial orthonormal-frame transformation;
5. what changes when its rapidity is an arbitrary smooth function of time
   and position, including acceleration; and
6. which older `Xmax` frame claims survive after replacing the projective
   `tanh` display with the corrected WR-L profile.

## Mode and scope

This is a metric-led `MAP -> OBSERVE -> DERIVE` audit.

Covered:

- exact radial-time block;
- the full angular block as a spectator when testing radial causality;
- static, finite-rapidity moving, and arbitrary smooth accelerated
  orthonormal observer fields;
- both sides of the WR-L null surface only where a regular chart supplies
  an algebraic continuation;
- source and claim provenance.

Not covered:

- every complete UDT metric branch;
- a global terminal boundary or quotient;
- angular topology, twist, holonomy, or a selected section;
- the Hopf carrier or `S2` posit;
- action, matter source, mass, charge, force, geodesic equation, or
  observer trajectory selection;
- quantum or phenomenological interpretation.

## Premise ledger

- `c_E`: `OBSERVED_FOUNDING_ANCHOR`.
- reciprocal metric form: `THEORY_IN_STATIC_SPHERICAL_SLICE`.
- `A=1-r/X`: `DERIVED_CONDITIONAL_WRL`.
- identification of the recorded branch's `X` with realized global
  `Xmax`: `OPEN_WITH_OWNER_WORKING_IDENTIFICATION`.
- common `Xmax` for ordinary observational frames:
  `OWNER_LOCKED_WORKING_POSTULATE`.
- observer: a future-directed unit timelike vector/coframe on the
  Lorentzian metric; `PINNED_BY_METRIC_DEFINITION`.
- rapidity field `eta(t,r)`: `FREE_AND_EXPLORED`.
- observer worldline and acceleration history: `FREE_AND_NOT_SELECTED`.
- round areal angular block in this branch: `PINNED_BY_RECORDED_SLICE`, not
  a carrier.
- global extension or prohibition on crossing: `OPEN`.

Local `O(1,1)` frame algebra may be derived from preservation of the
metric's orthonormal radial block. No SR transformation formula or GR
field equation may be assumed as a physical law.

## Required distinctions

The audit must keep separate:

```text
same invariant null surface
same coordinate labels
same measured local light speed
same static clock rate
surface unreachable by static signals
surface uncrossable by every observer
```

No one statement may silently substitute for another.

## Falsification and certification contract

The common-surface claim fails if an admissible orthonormal-frame change
moves the zero of the invariant surface norm.

The universal-uncrossability claim fails if a regular metric chart and a
timelike or null crossing witness exist without adding dynamics.

The “metric derives Lorentzian frame reciprocity” claim fails if preserving
the radial orthonormal quadratic form does not uniquely give the connected
`O(1,1)` family.

The accelerating-frame claim fails if a variable rapidity cannot be
handled by the metric-compatible Cartan connection without importing an
observer force law. A successful connection transformation may establish
covariance but may not select `eta(t,r)` or an acceleration history.

Every load-bearing formula must be recomputed independently. Mutations must
reject:

- using `tanh(phi)` as the WR-L position law;
- treating coordinate light speed as locally measured speed;
- equating a null surface with a curvature singularity;
- equating a regular crossing chart with a globally selected extension;
- claiming every observer is barred from crossing when a crossing witness
  exists;
- claiming variable rapidity is dynamically selected;
- treating the round angular block as the Hopf carrier; and
- importing a GR field equation or geodesic law.

## Maximum conclusion

The strongest permitted conclusion is:

```text
THE_WRL_METRIC_DERIVES_A_FRAME_INVARIANT_NULL_SURFACE_AND_LOCAL_LORENTZIAN_
OBSERVER_RECIPROCITY;STATIC_CLOCK_AND_OPTICAL_UNATTAINABILITY_ARE_EXACT;_
UNIVERSAL_UNCROSSABILITY_REQUIRES_ADDITIONAL_GLOBAL_UDT_BOUNDARY_CONTENT
```

If no regular crossing witness exists, the weaker or stronger result must
be reported exactly as the algebra allows.

No navigation update, canonization, Hopf comparison, action, source,
physics continuation, GPU work, or repository reorganization is
authorized in this package.
