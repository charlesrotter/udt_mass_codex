# UDT reciprocity-regime, angular-sector, and regular-center audit

Date: 2026-07-22

Base: `11ff6f8589a5c5d674b3dca9e65ae1c0dd8d7ac3`

Preregistration commit: `0d5eb5d021bad7e3e234f967ce4b691909afa2d8`

Mode: exact CPU metric algebra; no ODE/PDE, GPU, action, carrier, source, or scale insertion

Grade: `VERIFIED-WITH-CAVEATS`; independent direct-coordinate rational tensor reconstruction passes,
while no fresh external-model semantic review was authorized

## Result first

The founded static spherical UDT metric has no invariant observer-frame flip at any regular finite
value of `phi`. For

```text
ds^2 = -A(r)c_E^2 dt^2 + A(r)^(-1)dr^2 + r^2 dOmega^2,
A=exp(-2phi)>0,
```

the coframe

```text
e0=c_E sqrt(A) dt,
e1=dr/sqrt(A),
e2=r dtheta,
e3=r sin(theta) dvarphi
```

puts the metric into `diag(-1,1,1,1)` at every regular point with finite `phi` and positive areal
radius. Its determinant is

```text
det(g)=-c_E^2 r^4 sin(theta)^2,
```

independent of `phi`. Thus the local Lorentzian frame type is unchanged throughout the regular
finite-`phi` static branch. This is compatible with the owner-directed reciprocity of macro
observational frames; it does not derive a material observer law or a micro theorem.

The new metric-led result comes from the complete angular sector. Bounded curvature at a smooth
areal center forces

```text
A(0)=1,  A'(0)=0,
phi(0)=0,  phi'(0)=0,
phi=O(r^2).
```

This is exact inside the preregistered `C^2` Taylor, static spherical, areal-radius class. It is not a
statement about every topology, time-live center, nonspherical soliton, or microscopic matter core.

## Complete exact curvature map

Direct Christoffel/Riemann contraction gives

```text
R = -A'' - 4A'/r + 2(1-A)/r^2,

K = R_abcd R^abcd
  = (A'')^2 + 4(A'/r)^2 + 4((1-A)/r^2)^2,

C_abcd C^abcd
  = (1/3)[A'' - 2A'/r + 2(A-1)/r^2]^2.
```

The exact `Ricci^2` expression is preserved in `DERIVATION_RESULT.json`. In an orthonormal frame the
four repeated curvature motifs, up to the stated Riemann sign convention, are

```text
clock-depth:          A''/2,
clock-angular:        A'/(2r),
depth-angular:       -A'/(2r),
intrinsic angular:    (1-A)/r^2.
```

The angular term is an exact nonnegative contribution to `K` in this family:

```text
K >= 4(1-A)^2/r^4.
```

This positivity statement is scoped to this static spherical expression; it is not a claim that the
Kretschmann scalar of every Lorentzian metric is positive.

## The orchestra result

For constant positive `A=a`, the time–radial block has constant coefficients and is flat after a
coordinate rescaling. The complete areal metric instead has

```text
R = 2(1-a)/r^2,
K = 4(1-a)^2/r^4,
C^2 = 4(1-a)^2/(3r^4).
```

It is flat only for `a=1`. The sphere therefore detects the mismatch between radial proper distance
and angular circumference. This is a direct phi–angular interaction produced by the metric itself,
without an action or imported field equation.

It also proves that `phi -> -phi`, or `A -> 1/A`, is not a generic symmetry of the complete static
spherical metric when the same areal angular block is held fixed. A constant-`A` scalar-curvature
witness changes under reversal unless `A=1`. Dual Positional Reciprocity remains the founded
clock–distance measurement relation; it is not promoted to an isometry between every complete
`+phi` and `-phi` geometry.

## Regular-center theorem in the bounded class

Write the `C^2` Taylor jet

```text
A(r)=A0+A1 r+(A2/2)r^2+o(r^2).
```

The three independent square types in `K` behave as

```text
(A'')^2,
4(A'/r)^2,
4((1-A)/r^2)^2.
```

Boundedness forces `A0=1` and `A1=0`. Conversely those conditions with finite `A2` give

```text
K(0)=6 A2^2.
```

Since `A=exp(-2phi)>0`, they are equivalent to `phi(0)=phi'(0)=0`, with the first possible
departure quadratic. The exact regular quadratic control `A=1+a r^2` has

```text
R=-12a,  Ricci^2=36a^2,  K=24a^2,  C^2=0.
```

The linear control `A=1+b r` instead has `R=-6b/r` and `K=8b^2/r^2`. This localizes the previously
recorded WR-L center singularity to its nonzero linear center slope and the full angular coupling.

## Causal and frame readout

Radial metric-null curves obey

```text
|dr/dt|=c_E A.
```

For a static normalized observer,

```text
d tau=sqrt(A)dt,
d ell=dr/sqrt(A),
|d ell/d tau|=c_E.
```

Thus a finite change of the coordinate slope is not a local frame-law change. Matter, photons,
clocks, and universal cone coupling remain outside this purely geometric readout.

Curvature can distinguish solution-specific eigendirections or a static congruence without making
one observer fundamental in the laws. Macro observer reciprocity concerns the law and tensorial
description, not the absence of all structure in a particular solution.

## Endpoint classification

### `A -> 0`, or `phi -> +infinity`, at finite areal radius

The angular curvature motif remains finite. Derivatives decide whether the endpoint is regular or
singular, and the static chart alone cannot decide extendibility.

For the recorded WR-L control `A=1-r/X`, the exact values are

```text
R=6/(Xr),  Ricci^2=10/(X^2 r^2),  K=8/(X^2 r^2),  C^2=0.
```

At `r=X` they are finite. The earlier independently verified ingoing extension remains decisive:
the static observer congruence terminates at a horizon, while the local Lorentzian spacetime frame
continues. This is not an invariant frame flip and does not make the surface a selected hard edge.

### `A -> infinity`, or `phi -> -infinity`, at finite areal radius

The exact angular lower bound makes `K` diverge. This endpoint is curvature-singular in the stated
static spherical class; it is not a second regular observer regime. A correlated `r -> infinity`
limit or a different complete nonspherical/time-live metric is outside the result.

### `r -> 0`

Any `A(0) != 1` gives an `r^-4` curvature divergence, and any nonzero `A'(0)` gives an `r^-2`
divergence. A regular center returns to reciprocal balance. This does not identify the areal center
with physical “micro UDT,” because no native scale/solution map has been derived.

## Consequence for the macro-to-micro question

Following the metric yields a disciplined answer rather than the requested outcome:

- no finite-`phi` invariant frame flip appears in this static spherical family;
- a smooth areal center returns to the ordinary balanced local frame;
- the positive-`phi` WR-L endpoint is a static-frame horizon, not a spacetime-frame reversal;
- the negative-`phi` infinite endpoint at finite areal radius is singular; and
- the general micro, nonspherical, and time-live frame law remains `OPEN`.

Accordingly the macro owner premise has not been silently imposed on micro UDT. The metric simply
does not produce a regular competing micro frame structure in this bounded family.

## Verification

Ten exact post-firewall sources are frozen in `SOURCE_LINEAGE.tsv`. The production route derives the
full coordinate curvature and passes 18/18 exact symbolic checks across five profile controls. A
separate implementation using only standard-library `Fraction` arithmetic constructs metric
two-jets at equatorial points, differentiates inverse metrics and Christoffels directly, rebuilds
six complete coordinate Riemann controls, passes 17/17 exact checks, and exercises 18/18 corruption
catches.

## Four evidence gates

1. **Preregistered:** yes; commit `0d5eb5d` precedes production algebra and adjudication.
2. **Full or bounded:** complete for arbitrary `C^2 A(r)` within the declared static spherical areal
   metric and enumerated endpoint controls. Nonspherical/time-live metrics and physical scale are
   excluded.
3. **Independently verified:** yes for the load-bearing curvature, center, frame, endpoint, source,
   and ledger claims. No fresh external-model semantic review was authorized.
4. **Premises audited:** metric realization, smoothness, chart, angular geometry, observer meaning,
   causal readout, scale, dynamics, matter, boundary, and global limitations are explicit.

## Stop line

No macro navigation control, canon, action, source, carrier, boundary, mass, `X_max`, scale, physical
micro identification, ODE/PDE, GPU work, or repository reorganization is changed or launched.

Maximum conclusion:

```text
NO_INVARIANT_FINITE_PHI_FRAME_FLIP_IN_THE_STATIC_SPHERICAL_CLASS;
THE_ANGULAR_SECTOR_FORCES_RECIPROCAL_BALANCE_AT_A_REGULAR_AREAL_CENTER;
THE_WRL_WALL_TERMINATES_THE_STATIC_OBSERVER_FRAME_BUT_NOT_LOCAL_LORENTZIAN_GEOMETRY;
GENERAL_TIME_LIVE_AND_MICRO_FRAME_BEHAVIOR_REMAIN_OPEN.
```
