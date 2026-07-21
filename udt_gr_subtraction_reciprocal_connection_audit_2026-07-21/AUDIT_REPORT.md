# GR-to-UDT structural subtraction and reciprocal-connection audit

Date: 2026-07-21

## Result first

The GR comparison was productive. It exposed one elegant structural fork that organizes several
previously separate UDT clues.

For one supplied metric, torsion freedom plus exact metric compatibility uniquely gives its
Levi-Civita connection. Replacing that metric by UDT's CSN conformal class leaves the familiar
four-component Weyl one-form freedom. Adding a normalized reciprocal endomorphism removes that
freedom completely:

> Within the torsion-free conformal class, a connection preserving normalized reciprocal structure
> is unique if it exists.

Existence is the decisive gate. It distinguishes two possible meanings of complete Reciprocity:

1. **Longitudinal-only reciprocity:** the founding clock/radial pair acts reciprocally and the two
   transverse directions are untouched. This is the direct faithful four-vector extension already
   registered by the repository. Exact reciprocal-compatible Weyl transport is generically
   obstructed by the angular sector.
2. **Full two-pair reciprocity:** the transverse plane carries a second reciprocal pair. This is not
   derived, but in the tested static class it removes the local obstruction. Adding determinant-one
   angular reciprocity then produces exactly

   ```text
   diag(exp(-2 phi),exp(+2 phi)),
   ```

   the independently discovered conditional Hopf orbit block.

This convergence is a strong `WORKING` lead, not closure. Current UDT does not derive that the
internal reciprocal pair becomes a full spacetime endomorphism, much less that it duplicates into
two transverse physical directions. Torsion freedom is also a tested comparison premise rather than
a separately founded UDT law.

The smallest missing elegant principle is therefore sharper:

> Is UDT Reciprocity fundamentally one longitudinal dual pair, or a complete two-pair reduction of
> the four-dimensional conformal frame bundle?

## Lay interpretation

GR chooses how rulers are carried by requiring one metric to remain unchanged. UDT begins one step
earlier: overall ruler size is calibrational, so the conformal metric alone leaves a small freedom in
how rulers are compared.

We asked whether UDT's reciprocal clock/ruler relation removes that freedom. It does—completely—if
the reciprocal structure can be consistently attached to the whole metric.

The surprise occurs in the two angular directions. If Reciprocity is attached only to clock and
radius, the angular sector fights the proposed transport except in a special scaling. If the angular
sector itself contains a second grow/shrink pair, all four directions fit into one coherent pattern.
That pattern is exactly the angular pattern previously found inside Hopf geometry.

This does not prove that the universe uses the second pair. But it explains why the Hopf clue keeps
reappearing: the same completion simultaneously makes reciprocal transport coherent and produces
the geometry capable of supporting the conditional Hopf structure.

## The GR subtraction

Two torsion-free connections differ by a tensor symmetric in their lower connection slots. If both
preserve the same nondegenerate metric, the metric-compatibility equations have rank 40 on the 40
independent difference components. The difference vanishes. This is the connection-uniqueness
content used here; no Einstein equation is involved.

For a conformal class, every torsion-free compatible connection differs from the Levi-Civita
connection of representative `g` by a one-form `A`:

```text
C^a_bc(A)=delta^a_b A_c + delta^a_c A_b - g_bc A^a,
nabla^A g=-2 A tensor g.
```

Under a CSN representative change

```text
g -> exp(2 sigma) g,
A -> A-d sigma,
```

the affine connection is unchanged. Thus `A` is representative bookkeeping until further UDT
structure fixes the connection.

## Reciprocal compatibility removes the Weyl freedom

Let two torsion-free conformal connections differ by `B`. Their effects on a normalized reciprocal
endomorphism differ by

```text
[C(B),L].
```

For the conditional complete direct generator

```text
L=diag(-1,+1,0,0),
```

the linear map from the four components of `B` to the complete tensor has rank four. Its kernel is
zero. The same holds for the reciprocal-plane projector `P=L^2`.

This was repeated on all eight nonzero-cross witnesses: four seal lifts, each at `mu=4` and `mu=9`.
Every `L` and `P` difference map again has rank four. Angular coupling does not create hidden
connection freedom.

This establishes `RECIPROCAL_COMPATIBILITY_UNIQUE_IF_IT_EXISTS`. It does not establish existence.

### Recurrent transport is not an escape

Suppose normalized `L` is only recurrent:

```text
nabla L=alpha tensor L.
```

Because `tr(L^2)=2` is a fixed nonzero scalar,

```text
d tr(L^2)=2 alpha tr(L^2)
```

forces `alpha=0`. The complete linear system independently has rank eight on the eight unknown
components `(B,alpha)`. Recurrent or weighted language does not weaken exact parallelism for the
normalized weight-zero generator. A separately weighted unnormalized coframe can rescale, but its
normalized reciprocal ratio returns to this result.

## The angular obstruction in the direct extension

At a normalized point write the static diagonal metric jet as

```text
g=diag(-1,+1,+1,+1),
partial_r g=diag(2p,2p,2h2,2h3).
```

Here `p=partial_r phi`, while `h2,h3` are the logarithmic rates of the two transverse coframe
scales. Solving the full tensor equation

```text
nabla^LC L + [C(A),L]=0
```

for direct `L` gives exactly

```text
A_t=A_2=A_3=0,
A_r=p,
h2=h3=-p.
```

The clock/radial equation demands `A_r=p`. Comparison with each transverse direction demands
`A_r=-h2=-h3`. If the transverse block is locally constant while `p` is nonzero, one part demands
`A_r=p` and another demands `A_r=0`; the coefficient rank is four and the augmented rank is five.

In a diagonal areal chart with transverse radius `R`, compatibility would require

```text
d log(R)=-d phi.
```

That is not the generic founding spherical readout `R=r` with an arbitrary UDT profile. It is a
special angular-depth relation. This is an exact local obstruction inside the tested direct lift,
not a no-go against every future UDT connection.

Preserving only `P=L^2` is weaker. It requires equal transverse rates and sets `A_r=-h`, while
leaving `p` free. It preserves the reciprocal two-plane but permits the normalized clock/ruler axes
to rotate within it.

## The conditional full two-pair completion

The seal algebra itself classifies which registered angular lifts can carry a second reciprocal
generator. Requiring

```text
A_ang M A_ang=-M
```

gives:

- angular `+I` or `-I`: only `M=0`;
- axis reflection: `M=[[0,a],[b,0]]`, with `ab=1` after normalization;
- Hopf exchange: `M=[[a,b],[-b,-a]]`, with `a^2-b^2=1` after normalization.

Thus a full-rank second reciprocal pair exists only in the two orientation-preserving reflection
classes. In the Hopf-exchange basis use

```text
L_full=diag(-1,+1,-1,+1),
R=diag(J,J),
R L_full R=-L_full.
```

Exact torsion-free conformal compatibility gives

```text
A_r=p,
h2=-p,
h3 free.
```

If the angular pair is also required to obey determinant-one reciprocity, `h2+h3=0`, then

```text
h2=-p,
h3=+p.
```

Integration produces, up to positive common scale and discrete exchange,

```text
q_angular=diag(exp(-2phi),exp(+2phi)).
```

An exact all-profile metric witness

```text
g=diag(-exp(-2phi),exp(+2phi),exp(-2phi),exp(+2phi))
```

has the unique compatible Weyl one-form `A=dphi` in this representative. The connection equation
holds identically for arbitrary radial `phi`.

The normalized reciprocal character remains dynamic:

```text
D^-1 nabla D=dphi L.
```

Parallel transport of the generator therefore does not freeze positional dilation. It makes
`dphi L` the exact reciprocal group current.

## Why this is not yet the answer

The founding construction derives one internal clock/radial dual pair. The prior transverse audit
explicitly proves that its direct faithful four-vector extension is

```text
diag(exp(-phi),exp(+phi),1,1),
```

not a duplicated transverse pair. A scalar `phi` and an isotropic transverse plane cannot select
ordered transverse reciprocal axes without additional derived structure.

The full two-pair completion therefore remains
`CONDITIONAL_TRANSVERSE_REALIZATION_NOT_DERIVED`. Its exact agreement with the conditional Hopf orbit
block makes it a coherent high-priority candidate, but adopting it because it supports the Hopfion
would reverse the derivation and impose the desired matter structure.

Nor does the match derive the `S2` carrier, `L2+L4` action, periods, caps, topology, boundary, source,
or stability. The existing soliton is still `OBSERVED_CARRIER_CONDITIONAL` and statically stable only
within its declared carrier/action/box premises.

## Seal, finite cell, and bootstrap

The seal reverses `L`; it is not presently a bulk-parallel endomorphism. Requiring both `L` and a
fixed seal map to be parallel would generally force the nontrivial reciprocal gradient away. The
current seal instead supplies limited boundary parity and one local clock/radial soldering datum.

Current finite-cell and bootstrap sources provide no equation selecting direct versus full
two-pair realization, extending the reciprocal axes through the bulk, fixing angular periods, or
turning the conditional local connection into global holonomy. Bootstrap can later rank complete
solutions after the missing law exists; it cannot be used as that law now.

## Scientific consequence

The comparison with GR did reveal a candidate organizing principle:

> A complete UDT geometry may be a CSN conformal metric together with a normalized reciprocal
> reduction whose torsion-free compatible connection is unique.

The theorem is currently conditional twice: the reciprocal reduction must be realized on spacetime,
and torsion-free compatibility must be founded rather than inherited by familiarity.

The most important new clue is that the full two-pair realization simultaneously:

1. removes the tested local angular obstruction;
2. leaves no compatible-connection freedom;
3. extends the founding reciprocal character uniformly through four dimensions; and
4. reproduces the independently found Hopf angular weights.

The next step should not be another general connection census. It should be a focused derivation of
whether the **metric itself** supplies the second reciprocal pair—for example through a conformally
natural angular eigensplitting or complete-frame reduction—without using the Hopfion as the target.

No new principle, torsion, gauge field, action, topology, carrier, source, boundary law, mass, scale,
GPU result, or canon entry was adopted.

## Four evidence gates

1. **Preregistered:** yes, commit `4b52339`, before new source inspection and algebra.
2. **Full space or bounded scope:** complete torsion-free conformal connection-difference theorem,
   all registered local seal lifts, eight nonzero-cross uniqueness witnesses, and the declared
   static jet/full-profile classes; not arbitrary spacetime reductions or dynamics.
3. **Independent verification:** separate standard-library rational tensor/rank reconstruction,
   source/status replay, and exercised fail-closed mutations.
4. **Premise audit:** internal-versus-spacetime realization, torsion, CSN, direct/full extensions,
   seal, topology, carrier, and bootstrap limits are explicit.

Maximum conclusion:

`UDT_GR_SUBTRACTION_RECIPROCAL_CONNECTION_STATUS_CHARACTERIZED`.

