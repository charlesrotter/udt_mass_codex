# UDT frame/bivector equivariance audit

Date: 2026-07-23

Preregistration commit: `94c32e2`

Mode: metric-led, CPU-only exact algebra

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The audit finds a stronger and cleaner join than simple numerical
compatibility, but only on the timelike nonzero-`dphi` stratum.

There, `dphi` selects a local timelike line. With the recorded time
orientation, that line defines a conditional observer and divides the six
local frame generators into

```text
3 boost generators + 3 rotation generators.
```

This is exactly the previously derived real `3+3` split of two-forms:

```text
Pi_parallel Lambda2 = span(e0i) = boost sector K,
Pi_transverse Lambda2 = span(eij) = rotation sector J.
```

The frame algebra closes as

```text
[J,J] lies in J,
[J,K] lies in K,
[K,K] lies in J.
```

The exact verifier finds that the commutators of the three boost
directions span the entire three-dimensional rotation sector. In
particular,

```text
[Kx,Ky] = Jz
```

in the registered convention. The finite non-collinear boost witness from
the parent audit leaves precisely a `Jz` screen rotation.

Thus the angular rotation is not an unrelated mechanism added to the
reciprocal frame geometry:

> On timelike nonzero `dphi`, angular frame rotation is the
> noncommutative closure of the boost half of the metric's intrinsic
> `3+3` frame-algebra decomposition.

That is an exact local structural result. It is not yet dynamics, force,
curvature, matter, or a Hopf carrier.

## The equally important obstruction

The scalar reciprocal exponential does **not** extend unchanged to the
full observer group.

On a selected collinear boost plane, the two null directions have exact
weights

```text
k+ -> exp(+chi) k+,
k- -> exp(-chi) k-.
```

For the rational witness `cosh(chi)=5/4`, `sinh(chi)=3/4`, these are
exactly `2` and `1/2`.

But the full connected local observer group `SO+(1,3)` has no nontrivial
continuous real one-dimensional character. Its six-dimensional Lie
algebra is equal to its own commutator algebra. Any scalar character's
differential must vanish on every commutator and therefore everywhere.

The full real two-form representation does extend the collinear action,
but its exact collinear spectrum is

```text
exp(+chi) with multiplicity 2,
1         with multiplicity 2,
exp(-chi) with multiplicity 2.
```

That is `2+2+2`, not the `dphi`-assisted `3+3`. A non-collinear frame
change mixes the fixed collinear eigenspaces.

So the full-frame completion of reciprocal kinematics is necessarily
nonabelian. It cannot be one scalar `phi` simply applied in every
direction.

## What joins and what does not

Three statements must remain separate.

### 1. The sector decomposition joins exactly

On timelike nonzero `dphi`, the real Hodge-exchanged `3+3` split is exactly
the Cartan/symmetric-pair split of the local Lorentz frame algebra into
boosts and rotations.

The timelike `dphi` stabilizer is `SO(3)`. The exact residual screen
rotation

```text
R =
[[1, 0,     0,    0],
 [0, 40/41, 9/41, 0],
 [0,-9/41, 40/41, 0],
 [0, 0,     0,    1]]
```

preserves the two rank-three sectors. Four-dimensional Hodge duality
intertwines its action on them.

### 2. The reciprocal weighting is compatible but is not a frame-group automorphism

On a fixed nonnull-`dphi` split,

```text
D(q) = q Pi_parallel + q^-1 Pi_transverse
```

forms an exact multiplicative one-parameter flow:

```text
D(q)D(p)=D(qp).
```

However, it does not preserve the Lorentz bracket unless `q=1`. For
example,

```text
D[Kx,Ky] = q^-1 Jz,
[D Kx,D Ky] = q^2 Jz.
```

Bracket preservation requires `q^-1=q^2`. For a positive real weight,
that gives only `q=1`.

Therefore the reciprocal weighting is a real polarization/dilation of the
two sectors, not a nontrivial Lorentz-frame transformation. This prevents
an invalid identification of metric `phi` with observer rapidity.

### 3. The screen rotation is not the reciprocal operator

At `phi=0`, the `dphi` reciprocal operator is the identity, while the
exact non-collinear screen rotation above remains nontrivial. The two
objects therefore cannot be identical.

The correct ruling is:

```text
sector-level identity on the timelike stratum;
exact stabilizer compatibility of the angular action;
no identity between the reciprocal weight and observer-frame action.
```

## Lorentz equivariance versus invariance

For nonnull `alpha=dphi`,

```text
P(alpha)=alpha_sharp tensor alpha / g^-1(alpha,alpha)
```

is an intrinsic line projector. Under a Lorentz transformation,

```text
P(Lambda alpha)=Lambda P(alpha) Lambda^-1.
```

The induced rank-three projectors and `D(q)` obey the same conjugation
law. This is an equivariant **family** of splits.

A generic boost does not preserve one fixed `dphi` split. Only the
stabilizer of that particular `dphi` does. Calling equivariant transport
"full-group invariance of one split" would be false.

Positive common scaling leaves the line projector, the `3+3` split,
four-dimensional middle-form Hodge operation, normalized frame relation,
and dimensionless screen angle unchanged. The construction therefore
descends through the registered CSN equivalence.

## Complete `dphi` stratum ruling

### Timelike, nonzero

- Real semisimple `3+3` split: yes.
- Conditional observer line: yes.
- Stabilizer: `SO(3)`.
- Exact boost/rotation Cartan identification: yes.
- Exact screen-rotation compatibility: yes.
- Global persistence: open.

Because the observer covector is proportional to the exact form `dphi`,
its normalized congruence is hypersurface orthogonal:

```text
n=f dphi  implies  n wedge dn=0.
```

The screen rotation from frame composition is therefore not vorticity of
the `dphi` congruence.

### Spacelike, nonzero

- Real semisimple `3+3` split: yes.
- Stabilizer: `SO+(1,2)`, which includes boosts.
- Conditional observer: no.
- Canonical `SO(3)` observer screen: no.

The Hodge-exchanged sectors remain real and exact, but the timelike
boost/rotation interpretation does not transfer unchanged.

### Null, nonzero

The normalized projector is undefined. The unnormalized line map is
rank-one nilpotent, and its induced two-form map is rank-two nilpotent.
There is a two-dimensional null-screen quotient, but no semisimple real
`3+3` split.

### Zero

`dphi` supplies no line, observer, or split.

### Type-changing

The normalized projector becomes singular at a null or zero interface.
The timelike join cannot be promoted through such an interface without
additional complete-branch data.

## Connection and holonomy ruling

Four objects were kept distinct:

1. finite frame composition at one event;
2. the conditional `SO(3)` reduction supplied by smooth timelike
   nonzero `dphi`;
3. the projected spatial connection available on that reduction; and
4. Levi-Civita spacetime curvature and holonomy.

The first two are derived in their stated local scope. The third is a
conditional intrinsic definition once a smooth timelike branch and
metric representative are supplied. The full Levi-Civita connection
preserves the reduction only if `nabla P=0`; current UDT does not force
that condition.

Connection curvature, loop holonomy, and global persistence require
derivatives and a complete branch. They are not supplied by the
pointwise Wigner rotation.

## Meaning for UDT

This resolves an important part of the "orchestra" question.

The complete metric does not consist of a scalar reciprocal instrument
plus an unrelated angular instrument. On a timelike-`dphi` branch, its
local frame algebra is an inseparable six-dimensional structure:
different boost directions necessarily generate rotations.

What remains open is equally precise:

- whether complete admissible UDT cells force `dphi` to stay timelike
  and nonzero;
- whether the induced reduction is preserved or has a selected projected
  connection;
- what, if anything, makes the reciprocal sector weighting dynamical;
- whether metric `phi` has any derived relation to observer rapidity;
- and every global carrier, Hopf, action, source, boundary, scale, and
  mass conclusion.

The result is therefore a genuine geometric assembly rule, not closure.

## Evidence gates

1. **Preregistered:** yes, commit `94c32e2`.
2. **Full or bounded space:** complete for the named local
   `SO+(1,3)`, real `Lambda2`, nonnull/degenerate `dphi` representations;
   no global solution claim.
3. **Independent verification:** yes; a separate stdlib/Fraction
   implementation passes 65 checks and all 22 exercised catch-proofs
   without importing the production module.
4. **Premises audited:** metric parent, orientation, time orientation,
   CSN, `c_E`, `dphi` strata, rapidity/`phi`, connection, carrier, action,
   boundary, and scale are separated.

Maximum status:

```text
EXACT_TIMELIKE_DPHI_CARTAN_3PLUS3_FRAME_ALGEBRA_JOIN_WITH_ANGULAR_ROTATION_GENERATED_BY_NONCOLLINEAR_BOOST_COMMUTATORS;FULL_SCALAR_RECIPROCAL_CHARACTER_AND_NONTRIVIAL_WEIGHT_AUTOMORPHISM_OBSTRUCTED;GLOBAL_AND_PHYSICAL_PROMOTIONS_OPEN
```
