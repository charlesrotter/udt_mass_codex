# G335 exact derivation — local pair-response persistence

Date: 2026-09-03
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## 1. Conditional development and presentation

G332 supplies smooth compact boundary-free initial data `(gamma,K)` satisfying the complete active
provisional vacuum constraints. Conditional on the standard smooth local well-posedness theorem
already caveated in G303/G315/G321, each fixed datum has a smooth local marked development.

In a sufficiently small Gaussian-normal tube around the initial slice,

```text
g = -dt^2 + gamma(t),
n = partial_t,
K = -(1/2) partial_t gamma,
H = (1/2) gamma^{-1} partial_t gamma = -K^sharp.
```

Unit lapse and zero shift are gauge presentation. The interval is local and datum-dependent; no
physical duration or global Gaussian chart is assumed.

For any smooth unit spatial direction field `v(t)`, define

```text
q(t) = gamma(t)(H(t)v(t),v(t)).
```

At the initial slice G333 gives

```text
q0 = (b-C)/2 - b*mu,
mu = gamma(v,xi)^2 in [0,1].
```

Both exact G332 values `b=-C +/- sqrt(2[R+2C^2-2Lambda])` remain present.

## 2. The geometric pair response at regular local time

Gaussian-normal `n` is unit and geodesic. Consequently

```text
(L_n g)(n,n)=0,
(L_n g)(n,v)=0,
(L_n g)(v,v)=2q(t).
```

At any regular local time and any finite rapidity `z`, put

```text
u = cosh(z)n+sinh(z)v,
s = sinh(z)n+cosh(z)v.
```

The restriction of the geometric deformation tensor `L_n g` to this pair plane is therefore

```text
D_geom(t,z)
 = 2q(t) [[sinh(z)^2, sinh(z)cosh(z)],
           [sinh(z)cosh(z), cosh(z)^2]].
```

This is an exact pointwise identity throughout the regular Gaussian tube, not only at `t=0`. Its
mixed trace is `2q(t)`, its determinant is zero, and it vanishes exactly when `q(t)=0`. A finite
boost redistributes one response channel and creates none.

## 3. Per-datum local persistence

Smoothness of the metric, `H`, and the supplied smooth direction continuation makes `q(t)`
continuous. If `q0` is nonzero, choose a sufficiently small `epsilon>0` such that

```text
|q(t)-q0| < |q0|/2       for |t|<epsilon.
```

Then `q(t)` has the same sign as `q0` and `D_geom(t,z)` remains nonzero throughout that interval for
every finite boost. Thus the G333/G334 geometric response is not confined to one instant:

```text
q0 != 0
  => some datum/germ-specific nonzero-time interval retains its sign and response.
```

This is qualitative local persistence. The theorem does not supply a numerical duration, and it
does not compute the later amplitude or asymptotic behavior.

For a Lie-carried coordinate pair whose initial basis is the boosted pair, G334's component first
jet gives

```text
h(t)=eta+t D_geom(0,z)+o(t).
```

Hence the transported component increment is also nonzero for all sufficiently small nonzero `t`
when `q0!=0`. That component statement belongs to the declared carry, not to every frame.

## 4. Exact first-order silent set

For fixed `b,C`, the initial rate is affine in `mu`. If `b!=0`, its unique possible zero is

```text
mu_silent = (b-C)/(2b).
```

The endpoint rates are

```text
q(0) = (b-C)/2,
q(1) = -(b+C)/2.
```

Their product is `-(b^2-C^2)/4`. Therefore

```text
a silent unit direction exists iff |b|>=|C|.
```

When `|b|>|C|`, the silent directions have an interior overlap `0<mu_silent<1`; equality gives a
horizontal or vertical endpoint. If `b=0`, strict G332 lawfulness forbids `C=0`, and
`q0=-C/2!=0`, so no direction is silent.

The equal-weight exact control `R=12`, `C=0`, `Lambda=2` has strict root magnitude `4`, both branches
`b=+/-4`, and the silent overlap `mu=1/2`. Silent directions are therefore real members of the
lawful family, not numerical accidents or cases to discard.

At a silent direction G333/G334 supplies only `q0=0`. It does not determine the next nonzero jet.
The response may remain silent, turn on, or cross sign depending on higher metric and germ data.
That is an exact higher-jet boundary, not a failure of the datum.

## 5. Fixed-datum all-direction persistence

If `|b|<|C|` at one point, every direction has the same sign `-sign(C)` and

```text
min over unit v of |q0| = (|C|-|b|)/2.
```

For a fixed compact G332 datum satisfying

```text
sup over the slice |b| < |C|,
```

the initial response has a strictly positive gap over the compact unit tangent bundle. Smooth
local metric evolution and compactness then give one sufficiently small interval on which the
geometric response remains nonzero for every point and every unit direction of that fixed datum.

This does not extend uniformly over the unrestricted G332 family. The exact silent control above
already defeats a full-family all-direction gap, and directions can approach its silent overlap
with arbitrarily small nonzero `q0`. No family-wide derivative bound, calibrated clock duration,
or absolute scale is supplied by the current premises.

## 6. Geometry versus raw components and terminal Phi

For a supplied moving pair frame `e_a`, G334 gives

```text
n(h_ab) = (L_n g)(e_a,e_b) + transport_ab.
```

A continuously re-orthonormalized pair has `h_ab=eta` and can cancel every raw component derivative
with its transport term even while `D_geom` is nonzero. Thus raw component persistence is not frame-
carry independent. The complete typed state is the metric deformation together with the supplied
pair carry; zero moving-frame components do not mean zero geometry.

In the inherited Lie-carried component class,

```text
n(Phi)=q0*sinh(z)^2.
```

For `q0!=0` and nonzero boost, the same first-order continuity argument makes terminal `Phi`
locally informative. At zero boost it remains first-order blind. In a re-orthonormalized frame it
can remain componentwise constant because the response is recorded in carry instead. No universal
terminal-scalar persistence law follows without a physical germ/carry prescription.

## 7. Normal time is not boosted-observer time

For any scalar readout `f`,

```text
u(f)=cosh(z)n(f)+sinh(z)v(f).
```

At nonzero boost the normal jet alone does not determine this value. The full G332 metric determines
spatial derivatives only after a spatial extension of the pair germ is supplied, and acceleration
or carry can add further data. G335 therefore does not close general observer-time evolution.

## 8. Exact and independent controls

The production implementation uses standard-library exact rational arithmetic on 13,728
branch/direction/boost cases. It checks both branches, silent and non-silent directions,
all-direction gap controls, continuity bounds, boost identities, frame cancellation, and observer-
jet ambiguity. It records 171,124 passing checks. The analytic derivation, rather than the finite
rapidity samples, owns the all-direction/all-finite-boost statements.

As a non-load-bearing consistency control, the exact flat Einstein slicing
`a(t)=exp(Ht)`, `K=-H gamma`, `Lambda=3H^2` satisfies the Hamiltonian and evolution equations and has
`q(t)=H`. It is not used as a model for the G332 development.

The implementation-distinct verifier imports no production code and reads no production result. It
uses randomized floating strata, direct matrix algebra, and finite differences, passing 4,448
checks. Twelve preregistered hostile scientific mutations are caught.

## 9. Bounded landing

```text
NONZERO_INITIAL_GEOMETRIC_PAIR_RESPONSE_PERSISTS_ON_PER_DATUM_LOCAL_MARKED_INTERVAL
__SILENT_DIRECTIONS_REQUIRE_HIGHER_JET
__FIXED_COMPACT_ALL_DIRECTION_GAP_GIVES_UNIFORM_LOCAL_INTERVAL
__RAW_COMPONENT_AND_OBSERVER_TIME_REMAIN_CARRY_QUALIFIED
```

This changes neither the metric, reciprocal kernel, angular sector, nor adopted conditional
equation. It selects no datum, branch, topology, physical germ, history, source, matter/mass law,
observation, scale, physical `X_max`, or canon.
