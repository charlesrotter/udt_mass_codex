# Reciprocal-plane projector audit

Date: 2026-07-21

Base: `ec8250935d74a2218f31a09f5611bd0e5e4f40e0`

Compute: CPU-only exact symbolic algebra plus independent standard-library rational reconstruction

## Result first

The reciprocal-plane projector is a mathematically coherent **conditional** frame reduction, and it
is strictly less restrictive than preserving four reciprocal axes. In the tested class there is at
most one torsion-free CSN/Weyl connection preserving a supplied metric-orthogonal clock/radial
two-plane. Such a connection exists exactly when:

1. the reciprocal plane and its orthogonal angular screen are both integrable; and
2. each plane changes across the other only by a common scale, with no trace-free cross-shear.

The ordinary reciprocal warped metric with arbitrary depth `phi(r)`, arbitrary positive angular
radius `R(r)`, and an intrinsically curved round screen passes exactly. Two inequivalent `phi` rates
pass the same law. All eight registered constant nonzero-cross metrics pass when each uses its own
metric-orthogonal projector. Intrinsic angular rotation and curvature remain.

The law fails for nonintegrable twist and for trace-free cross-shear. Current UDT evidence does not
yet prove those sectors absent and does not derive the supplied spacetime plane or projector
parallelism. The honest status is therefore:

```text
UNIQUE_TORSION_FREE_CSN_CONNECTION_IF_AND_ONLY_IF_INTEGRABLE_UMBILICAL_SPLIT
CONDITIONAL_NOT_DERIVED_AS_A_UDT_SELECTOR
```

No action, carrier, topology, source, boundary charge, mass, or physical `phi` profile follows.

## Exact theorem in the declared class

Let a supplied Lorentzian conformal metric have an orthogonal local split into a Lorentzian
two-plane and a positive two-dimensional screen:

```text
g = h_ij(x,y) dx^i dx^j + q_AB(x,y) dy^A dy^B
P = diag(I_2,0).
```

The tested connection is torsion-free and Weyl-compatible:

```text
nabla^A g = -2 A tensor g.
```

Solving every component of `nabla^A P=0` gives

```text
partial_A h_ij = 2 s_A h_ij,
partial_i q_AB = 2 r_i q_AB,

A_A = -s_A = -(1/4) partial_A log|det h|,
A_i = -r_i = -(1/4) partial_i log det q.
```

These conditions are necessary and sufficient locally in the nonsingular integrable `2+2` class.
The full coefficient map for a second possible Weyl one-form has rank four, so the connection is
unique whenever it exists.

“Pure trace” here has a simple meaning: as one moves in the reciprocal plane, the angular screen
may grow or shrink, but it may not be squeezed in one angular direction while stretched in the
other. The same condition holds with the two planes exchanged. This is the standard geometric
meaning of an umbilical split; the term describes the derived condition rather than a new UDT
postulate.

## Why integrability is required

If a torsion-free connection preserves a plane, then for any two vector fields `X,Y` in that plane,

```text
[X,Y] = nabla_X Y - nabla_Y X
```

must also lie in the plane. Hence the plane is Frobenius integrable. The exact counter-witness

```text
E0 = partial_t - B r partial_y,
E1 = partial_r,
[E0,E1] = B partial_y
```

has a transverse bracket for nonzero `B`, so no torsion-free `P`-parallel connection can preserve
it. The same reasoning applies to the complementary screen.

## Reciprocal warped metric and angular sector

For

```text
h = diag(-exp(-2 phi), exp(2 phi)),
q = R(x)^2 q0(y),
```

the reciprocal determinant is independent of `phi`, and the screen changes across the base only by
the common factor `R^2`. The theorem therefore gives

```text
A = -d_base log R.
```

No derivative of `phi` is constrained. Exact point witnesses with `dphi/dr=2` and `dphi/dr=11`
both pass with the same screen and connection. A round screen also passes while retaining scalar
curvature `2/R^2`. Thus:

- the projector law does not select `phi`;
- it does not flatten the angular sector;
- it does not select an angular axis, section, round target, or topology; and
- it does require the base dependence of the screen shape to be scale-only.

## CSN covariance

Under a common-scale representative change

```text
g -> exp(2 sigma) g,
A -> A - d sigma,
```

the Levi-Civita shift and Weyl-one-form shift cancel exactly, so the transported affine connection
is unchanged. This makes the candidate compatible with CSN inside the declared Weyl class. It does
not show that CSN or the UDT metric selects that connection class.

## Nonzero-cross metrics

For each of the four registered seal-lift families at `mu=4` and `mu=9`, the test constructs the
metric-orthogonal projector onto the supplied reciprocal plane:

```text
P = U (U^T g U)^(-1) U^T g.
```

All eight projectors are idempotent, metric-self-adjoint, rank two, and have a rank-four uniqueness
map. Because each witness metric and projector is constant, `LC=0, A=0` supplies an exact compatible
connection. This refutes the claim that nonzero coordinate cross-terms alone obstruct the law. It
does not cover variable cross-terms that generate twist or shear.

## Projector versus individual reciprocal axes

An explicit static jet has `nabla P=0` for arbitrary nonzero `dphi/dr` while the normalized
reciprocal generator `L=diag(-1,+1,0,0)` is not parallel. Residual base boosts and angular rotations
commute with `P`. In particular, the angular rotation does not commute with a chosen angular
reciprocal involution. The local reduction therefore retains roughly

```text
common scale + so(1,1) + so(2),
```

not a complete four-axis reciprocal framing. This is why the projector route avoids the previous
angular obstruction, but also why it cannot select the conditional second pair or Hopf axis.

## Source and premise adjudication

- `pinned-by-THEORY`: founding internal reciprocal character and CSN conformal class.
- `CONDITIONAL_REALIZATION`: a spacetime reciprocal two-plane/projector.
- `pinned-by-HABIT / CONDITIONAL_COMPARISON`: torsion-free Weyl connection class.
- `free-and-explored`: projector parallelism as a possible frame principle.
- `NOT_ASSUMED`: individual generator parallelism, round/Hopf carrier, action, source, and boundary.

The internal pair-to-spacetime type gap remains explicit. The finite-cell seal has not supplied the
global plane, a bulk transport law, or a proof that the full metric is integrable and umbilical.
Compatibility is therefore evidence for coherence, not authority to adopt the law.

## Four evidence gates

1. **Preregistered:** yes; commit `290a6cd` precedes derivation and outcome inspection.
2. **Full space or bounded scope justified:** complete local tensor solution in the declared
   nonsingular integrable orthogonal `2+2` Weyl class, with exact twist, shear, curved-screen, profile,
   and nonzero-cross witnesses; global, torsionful, and non-Weyl sectors are excluded.
3. **Independent load-bearing verification:** yes; a standard-library `Fraction` implementation
   reconstructs the twelve-variable cross-jet solution, ranks, obstructions, profile witnesses,
   eight metric projectors, holonomy commutators, and CSN cancellation.
4. **Every premise audited:** yes; conditional plane realization, connection habit, omitted
   twist/shear authority, and downstream physics boundaries are explicit.

Maximum conclusion: `UDT_RECIPROCAL_PLANE_PROJECTOR_FRAME_STATUS_CHARACTERIZED`.

## Sharpened open gate

The next question is no longer “can a projector-compatible connection exist?” It can, and the
complete local criterion is known. The smallest honest missing selector is:

> Does the complete UDT metric together with the finite-cell seal select a global integrable,
> umbilical reciprocal two-plane projector?

Until that is derived, projector preservation remains a promising conditional frame reduction,
not a completed UDT principle.
