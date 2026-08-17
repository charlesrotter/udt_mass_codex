# G133 exact derivation — fixed-`K` two-density and overlap descent

Date: 2026-08-16

## 1. Result first

The fixed founding pairing owns an internal reciprocal-channel structure, not by itself a
query-independent two-form or physical scale field on spacetime.

Three exact positive results nevertheless join cleanly:

1. `D(delta)` preserves both `K` and the determinant line of the abstract two-channel space.
2. Every supplied regular pair metric `h=F* g` has an intrinsic positive Lorentzian area density
   that descends on genuine overlaps of that pair surface.
3. The full ambient metric `g` supplies one query-independent quadratic area bilinear on the bundle
   of bivectors. Its restriction evaluates every supplied clock/ruler plane.

These are different mathematical types. The third requires the full metric, while the first does
not canonically solder its abstract channel space into every timelike two-plane. The fixed numeric
matrix `K` can be used consistently across charts only after an `O(K)` transition local system has
been supplied. General complete pair-coordinate transitions need not lie in `O(K)`.

The bounded landing is

```text
FIXED_K_INTERNAL_UNIMODULAR_DENSITY_DERIVED;
SUPPLIED_PAIR_VOLUME_DENSITY_DESCENDS_ON_GENUINE_COMMON_ATLAS;
KAPPA_IS_A_LOG_DENSITY_COEFFICIENT_REQUIRING_MATCHED_CALIBRATION;
AMBIENT_AREA_BILINEAR_IS_DERIVED_FROM_FULL_g;
NO_FIXED_K_ONLY_QUERY_INDEPENDENT_BASE_TWO_FORM_OR_PHYSICAL_VALUE_LAW.
```

## 2. Internal reciprocal channel structure

Let the abstract clock/ruler channel space be `E=R^2` with

```text
K=[[0,1],[1,0]],
D(delta)=diag(exp(-delta),exp(+delta)).
```

Then exactly

```text
D(delta)^T K D(delta)=K,
det D(delta)=1.
```

The first equation makes `D(delta)` a `K`-isometry. The second says its induced action on the
one-dimensional determinant line `Lambda^2 E` is the identity. If `epsilon_E` is a chosen oriented
generator, then

```text
D(delta) epsilon_E=epsilon_E.
```

Without orientation, its absolute determinant line is still preserved. This is the internal
two-density genuinely owned by the founded representation.

Two type cautions are load-bearing:

- `K` is symmetric, not alternating, so it is not itself a two-form.
- `E` is an abstract channel space. A spacetime two-plane or pair-surface tangent space must be
  identified with `E` before `K` or its determinant generator can be pulled back.

## 3. The supplied pair metric owns its intrinsic area density

For a supplied regular timelike immersion

```text
F: Sigma^2 -> (M^4,g),
h=F* g,
```

the positive Lorentzian area density is

```text
nu_h=sqrt(-det h_ij) |dy0 wedge dy1|.                 (1)
```

Let `y=J y'`, so the metric components in the primed chart are

```text
h'=J^T h J.
```

Then

```text
det h'=(det J)^2 det h,
sqrt(-det h')=|det J| sqrt(-det h),
|dy0 wedge dy1|=|det J| |dy'0 wedge dy'1|.
```

Equation (1) therefore defines one coordinate-independent density on the supplied pair surface.
The equality is equality of geometric densities, not equality of their coordinate coefficients.

## 4. `kappa_pair` is a log-density coefficient

The terminal decomposition gives

```text
kappa_pair=(1/4) log(-det h).
```

Under the recharting above,

```text
kappa_pair' = kappa_pair + (1/2) log|det J|.          (2)
```

Thus `kappa_pair` is not an unrestricted scalar under arbitrary pair-domain reparameterization.
It is the logarithmic coefficient of the intrinsic density:

```text
nu_h=exp(2 kappa_pair)|dy0 wedge dy1|.
```

This does not invalidate the matched two-density character result of the ordered-query audit. It
states its exact hypothesis. A difference `Delta kappa` telescopes only after the endpoint density
lines have been identified by one calibrated query/local system. Independent endpoint
re-trivializations add

```text
(1/2) log|det J_q|-(1/2) log|det J_p|.
```

The actual density remains geometric; the scalar coefficient comparison requires calibration
carry.

Under a physical conformal change `h -> Omega^2 h`, rather than a coordinate change,

```text
nu_h -> Omega^2 nu_h,
kappa_pair -> kappa_pair+log Omega.
```

The common scale is therefore retained, not gauge-erased.

## 5. Genuine common-atlas overlap descent

Use the banked convention

```text
h_A=J_AB^T h_B J_AB,
h_B=J_BC^T h_C J_BC,
J_AC=J_BC J_AB.
```

The density coefficients obey

```text
n_A=|det J_AB| n_B,
n_B=|det J_BC| n_C,
```

so

```text
n_A=|det J_AB||det J_BC|n_C
   =|det J_AC|n_C.
```

The pair area density therefore has identity triple-overlap obstruction on one genuine common
pair atlas. This is ordinary tensor-density descent. It does not select the atlas, its numerical
metric, or the physical observer queries.

## 6. Why one fixed numeric `K` does not automatically descend

Suppose two channel trivializations both write the numeric matrix `K`. If their transition is
`J`, the two pulled-back tensors agree only when

```text
J^T K J=K.                                             (3)
```

For the scale transition

```text
J_s=diag(2,1),
```

one finds

```text
J_s^T K J_s=2K.
```

Even determinant-one is insufficient. For

```text
J_u=[[1,1],[0,1]],
```

the determinant line is preserved but

```text
J_u^T K J_u=[[0,1],[1,2]] != K.
```

Consequently fixed `K` defines a shared tensor only on a supplied reduction whose transition maps
lie in `O(K)`. The reciprocal matrices `D(delta)` do lie in that group and close under composition.
The founding representation therefore gives a lawful conditional local system, but it does not
provide the solder or prove that arbitrary complete observer-query transitions use it.

This is stricter than determinant-density descent. General pair metrics and their densities
descend under all invertible coordinate transitions; a common fixed numeric `K` requires the
smaller `O(K)` transition group.

## 7. The full metric supplies the cross-query area object

The ambient Lorentz metric canonically induces a symmetric bilinear form on bivectors:

```text
A_g(u wedge v,w wedge z)
  =g(u,w)g(v,z)-g(u,z)g(v,w).                         (4)
```

For one simple bivector `B=u wedge v`,

```text
A_g(B,B)=g(u,u)g(v,v)-g(u,v)^2=det(F* g).
```

For a timelike pair plane this is negative, and its positive area norm is

```text
|B|_g=sqrt(-A_g(B,B)).
```

Equation (4) is a section of

```text
Sym^2(Lambda^2 T* M),
```

often described as the metric-induced area bilinear. It is query-independent once the complete
metric `g` is supplied: every observer plane is evaluated by restriction. Equivalently, over the
bundle of timelike two-planes, the tautological rank-two plane bundle inherits a canonical
positive density from `g`.

It is not:

- a differential two-form;
- a scalar density on base spacetime;
- derived from fixed `K` without the full metric; or
- a law selecting the numerical metric history.

Under `g -> Omega^2 g`,

```text
A_g -> Omega^4 A_g,
|B|_g -> Omega^2 |B|_g.
```

It therefore retains exactly the common scale invisible to the G131 reciprocal scalar network.

## 8. No alternating two-form reproduces all observer-plane areas

In Minkowski space choose one clock vector `e0` and orthonormal rulers `e1,e2`. Suppose an
alternating two-form `omega` reproduced unit oriented area on both planes:

```text
omega(e0,e1)=1,
omega(e0,e2)=1.
```

For the normalized diagonal ruler

```text
r=(e1+e2)/sqrt(2),
```

linearity forces

```text
omega(e0,r)=sqrt(2).
```

But the metric area of `span(e0,r)` remains one. Contradiction. Hence no single alternating
two-form can be the metric area readout for every clock/ruler plane. The quadratic bivector object
in (4), not a two-form, is the correct common type.

## 9. Three-observer carry

If supplied transitions obey (3), then for composable arrows

```text
J_AB in O(K),
J_BC in O(K),
```

their composite also lies in `O(K)`. Determinant densities compose by multiplication, and the
usual triple-overlap law follows.

If the outgoing and incoming calibrations at observer `B` are independently rebuilt, an explicit
middle transition `M_B` is still required. The composite is

```text
J_BC M_B J_AB.
```

Fixed `K` is preserved only if the supplied `M_B` also respects the reduction. Setting `M_B=I`
without identifying the two middle states is the same hidden premise already isolated by the
three-observer carry audit.

## 10. Ownership and observational anchors

This audit is purely geometric. Observed `c_E` calibrates clock and ruler units but does not solder
the abstract channel bundle to every pair plane. `G_obs` is a valid observational anchor but has
no role until a lawful mass/energy/density-to-geometry bridge is supplied. No value is fitted here.

The result narrows the scale question:

- there is no missing algebraic area slot;
- full pair data carry area scale and descend on supplied compatible overlaps;
- the full metric assembles all plane areas into one quadratic bivector structure;
- the remaining open item is ownership and valuation of the physical metric/query network, not a
  new two-form manufactured from `K`.

## 11. Maximum conclusion

`DERIVED`, in the bounded regular types: internal determinant-density preservation by the founded
reciprocal representation; intrinsic pair-volume-density covariance and common-atlas descent;
the log-density transformation of `kappa_pair`; the full-metric area bilinear on bivectors; and the
no-single-two-form counterexample.

Still `OPEN`: a founding solder from the abstract reciprocal channel space to the complete
physical observer network; ownership and numerical values of that network; global/singular
completion; a law connecting `c_E,G_obs` and matter/energy data to metric scale; physical history,
`X_max`, bootstrap closure, action, source, matter, observations, and signalling.
