# Complete-metric intrinsic reciprocal/Hopf object audit

Date: 2026-07-23
Mode: preregistered, metric-led, CPU exact algebra and frozen-evidence replay

## Result first

The audit finds one new exact, frame-independent, **real** reciprocal-shaped
reduction, but only on a disclosed local stratum of the complete registered
`(g,phi)` data.

Let

```text
alpha = dphi,
v = alpha sharp,
s = g inverse(alpha,alpha).
```

Where `alpha` is nonzero and `s` is nonzero, define the metric projector

```text
P = v tensor alpha / s.
```

For a two-form `F`, define

```text
Pi_parallel(F)(X,Y) = F(PX,Y) + F(X,PY),
Pi_transverse = I - Pi_parallel.
```

Because `P` has rank one, `Pi_parallel` and `Pi_transverse` are complementary
real rank-three projectors on `Lambda2`. They separate two-forms with one leg
along the `phi` direction from two-forms entirely transverse to it. Set

```text
J_phi = Pi_parallel - Pi_transverse,
D_phi = exp(phi) Pi_parallel + exp(-phi) Pi_transverse.
```

Then exactly

```text
J_phi squared = I,
star Pi_parallel star inverse = Pi_transverse,
star D_phi star inverse = D_phi inverse.
```

The construction is tensorial, independent of coframe labels, and invariant
under positive common-scale rescaling. Exact timelike and spacelike controls
both pass. The inverse assignment

```text
D_phi inverse = exp(-phi) Pi_parallel + exp(phi) Pi_transverse
```

is equally compatible. Current UDT does not select which sector physically
owns the positive reciprocal character.

Maximum conclusion:

`EXACT_FRAME_INDEPENDENT_FIELD_ASSISTED_REAL_RECIPROCAL_3PLUS3_TWO_FORM_REDUCTION_IDENTIFIED_ON_NONNULL_DPHI_STRATA__HODGE_EXCHANGES_THE_SECTORS__GLOBAL_EXTENSION_PHYSICAL_OWNERSHIP_AND_HOPF_SECTION_REMAIN_OPEN`

## What is genuinely new

Earlier work established:

- the abstract reciprocal character;
- no universal physical reciprocal tangent two-plane;
- a conditional celestial null-direction `S2` bundle;
- no selected celestial section;
- an exact conditional reciprocal-toric/Hopf crosswalk; and
- no selected global completion.

Those results left open whether the complete metric carried the reciprocal
pair in a different representation. The present construction answers that
question positively on nonnull-`dphi` strata: the natural real carrier is not
a pair of named tangent axes, but a Hodge-exchanged pair of rank-three
two-form sectors.

This is a representation-level result. The projectors are derived from
`(g,dphi)` on their domain. Applying the already-derived reciprocal weights
to those sectors is an exact compatible realization, with `D_phi` and
`D_phi inverse` forming an unselected inverse pair. Current UDT does not yet
state which, if either, is the physical owner of the founding reciprocal
character.

## Why metric-only Hodge structure was close but insufficient

For an oriented Lorentzian four-metric,

```text
star squared = -I
```

on real two-forms. The exact commutant of the connected,
orientation-preserving Lorentz symmetry on real `Lambda2` is two-dimensional
and is spanned by `I` and `star`. Any real equivariant map for that symmetry
is therefore

```text
a I + b star,
```

with characteristic polynomial

```text
[((lambda-a)^2+b^2)]^3.
```

It has no nontrivial pair of distinct real reciprocal eigenspaces.

For the full Lorentz group including orientation-reversing transformations,
`star` changes sign and is not equivariant; the real commutant reduces to
scalar `I`. Thus the orientation qualification weakens rather than evades the
metric-only obstruction.

After complexification, `i star` is an involution with two rank-three
eigenspaces, and

```text
exp(phi i star)
```

does give exact reciprocal weights. But unequal weights break the conjugacy
condition needed for a real two-form. The complex construction is intrinsic
and exact, but it does not descend to real geometry.

The nonnull `dphi` line supplies the missing real involution. This is why the
new construction is field-assisted rather than metric-only.

## Domain and global obstruction

The denominator `s` is load-bearing.

- If `dphi` is timelike or spacelike and nonzero, the real `3+3` split exists.
- If `dphi` is null, the unnormalized endomorphism
  `v tensor alpha` is nonzero and rank one but squares to zero. It is
  nilpotent, not a projector. Its induced map on two-forms is likewise
  nonzero and nilpotent, with rank two rather than a semisimple `3+3`
  eigensplitting.
- If `dphi=0`, no direction or split is available.
- A continuous causal-type change must pass through a null or zero stratum,
  where the semisimple split degenerates.

The current foundation admits zero, spacelike, timelike, null, and
type-changing possibilities. In the frozen 6,144-row two-jet ensemble,
`dphi` is zero in 3,072 configurations, spacelike in 2,304, and timelike in
768; no null parent occurs in that bounded sample. Those counts characterize
the registered atlas, not solution frequencies or complete on-shell
universes.

A global bundle reduction would follow on any supplied complete branch where
`dphi` remains nonzero, nonnull, and compatible with the gluing. Current
Reciprocity, CSN, seal, finite-cell, and bootstrap statements do not prove
that global condition or select such a branch.

At the registered seal, `phi=0` does not imply `dphi=0`; the normal derivative
remains open. If the reduction reaches the seal, its two reciprocal weights
coincide there. Whether that occurs is a global field question, not a
consequence of the seal value alone.

## What survives without `dphi`

The complete metric still intrinsically supplies, under their exact premise
stamps:

- the conformal null cone;
- the conditional celestial `S2` bundle;
- oriented Lorentzian Hodge structure on two-forms;
- Levi-Civita connection and holonomy for each supplied representative; and
- primary characteristic data for each supplied global bundle.

These are genuine geometric objects. None by itself supplies the physical
reciprocal ownership, a selected section, or a Hopf secondary invariant.

The exact tangent-space controls reproduce the earlier obstruction:

- the connected, orientation-preserving Lorentz representation has no
  invariant nonzero vector;
- it has no invariant real two-form;
- its tangent commutant is scalar;
- spatial rotations have no fixed celestial direction; and
- the admitted seal stabilizer permits invariant projector ranks only
  `0,1,3,4`, not two.

The frozen curvature evidence also remains decisive within its scope:
5,376 metric-active configurations have a full irreducible curvature
algebra, while 768 flat configurations preserve every subspace and select
none. The registered curvature operators have zero isolated real simple
eigenbivector planes in all 6,144 rows.

## Hopf ruling

The new real `3+3` split is reciprocal-bearing but not yet Hopf-bearing.

On a timelike-`dphi` stratum, the transverse rank-three geometry has a
natural unit-direction `S2` fiber. This is another intrinsic sphere bundle,
not a selected `S2`-valued field. A Hopf secondary invariant requires at
least:

1. a selected section or map over a three-dimensional compactified domain;
2. transport/trivialization or an intrinsic bundle-level replacement;
3. physical boundary/framing data; and
4. a globally admissible completion.

None is supplied by the local split.

The prior reciprocal-toric principal-circle result remains exact
conditional: with periods, a circle action, primitive opposing caps,
orientation, quotient, and normalization supplied, it has `|c1|=1`. That is
the only audited object carrying an exact Hopf bundle class. Its global
inputs remain unselected, and no current rule identifies it with the new
`dphi` two-form reduction.

Primary characteristic classes of the tangent or celestial bundle also do
not fill the gap. They are invariants of a supplied global bundle, not a
selected `S3 -> S2` map or its secondary Hopf invariant.

## Complete object census

`INTRINSIC_OBJECT_CENSUS.tsv` classifies 30 candidates separately by:

- frame descent;
- CSN behavior;
- definition domain;
- reciprocal content;
- Hopf content;
- foundation selection; and
- maximum ruling.

`DOMAIN_TRANSITION_LEDGER.tsv` records every `dphi` stratum.
`BUNDLE_DEPENDENCY_MATRIX.tsv` keeps bundle, section, connection, completion,
and Hopf-class dependencies distinct.

The census does not exhaust arbitrary future higher-jet or nonlocal
functionals. It is complete for the registered object types through two jets
and the typed global holonomy, characteristic, spectral, boundary, and
bootstrap classes named in the preregistration.

## Meaning for the broader program

This result changes the representation map without changing any particle,
action, or mass verdict.

The reciprocal structure need not be soldered to one named clock/ruler
tangent plane. The full `(g,phi)` geometry already has a natural
frame-independent place where a real reciprocal pair can live: dual
three-dimensional sectors of the two-form bundle, wherever `dphi` is
nonnull.

That observation does **not** establish physical ownership, global
persistence, a carrier, an action, or matter emergence. It does identify a
more faithful next question than choosing a coframe axis:

> Do the registered complete finite-cell equations or admissibility
> conditions force a globally nondegenerate `dphi` reduction, and if so does
> its timelike branch supply an intrinsic section or quotient compatible
> with the conditional toric Hopf bundle?

That is a future bounded audit, not launched here.

## Evidence

Production exact algebra:

- 37/37 checks pass with SymPy 1.13.1;
- 30 object candidates classified;
- 60 frozen sources replayed;
- registered counts reproduced: `5,376 + 768 = 6,144`;
- the registered `dphi` census is directly replayed as `3,072` zero,
  `2,304` spacelike, and `768` timelike;
- twelve global completion families retained unselected.

Independent exact algebra:

- standard-library `Fraction` implementation;
- no import of the production script or SymPy;
- the load-bearing local linear algebra is independently recomputed;
- frozen atlas classifications are directly parsed and hash-checked, not
  independently rederived;
- 29 independent exact controls pass;
- 30/30 object rows and 60/60 source hashes validate; and
- 25/25 exercised mutations fail closed, including five operator-level
  mutations.

## Four banking gates

1. **Preregistered:** yes, commit `334b233`.
2. **Full or bounded scope:** complete for the 30 registered/named object
   classes and the frozen two-jet/global taxonomies; arbitrary future
   higher-jet and nonlocal laws remain open.
3. **Independently verified:** exact separate implementation and mutation
   catches pass. The first fresh zero-context adversarial review returned
   `PASS-WITH-CAVEATS`, independently confirmed the theorem, and required the
   correction layer preregistered at commit `535f3c4`. The fresh
   post-correction review returned `PASS`, reproduced every load-bearing
   result, and found no required correction remaining.
4. **Premises audited:** yes in `PREMISE_LEDGER.tsv`,
   `INTRINSIC_OBJECT_CENSUS.tsv`, `DOMAIN_TRANSITION_LEDGER.tsv`, and
   `BUNDLE_DEPENDENCY_MATRIX.tsv`.

No action, carrier, source, boundary functional, mass, scale, time-live law,
GPU work, canonization, or repository reorganization occurred.
