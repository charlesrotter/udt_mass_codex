# UDT frame/bivector equivariance audit — preregistration

Date: 2026-07-23

Mode: metric-led, CPU-only, exact local algebra

Base: `fb71839b8f051631c481bc0e33b0365384b6d6ad`

## Whole question

Does the complete four-dimensional conformal-Lorentzian metric make the
collinear reciprocal observer law and the nonnull-`dphi` real `3+3`
two-form reduction one intrinsic full-frame structure?

The audit must distinguish four possibilities:

1. **identity** — one construction uniquely and equivariantly determines
   the other;
2. **compatible reduction** — the structures intertwine on a stated
   stratum or stabilizer but neither determines the other;
3. **covariant transport only** — the Lorentz group moves the
   `dphi`-assisted split together with `dphi` but does not preserve a fixed
   split;
4. **obstruction** — the collinear reciprocal character cannot extend to
   the full observer group in the proposed representation.

## Bounded regime

The sampled object is the local tangent/coframe geometry at one regular
event:

```text
four-dimensional Lorentzian vector space (V,g);
proper, orthochronous local frame group SO+(1,3);
observer directions on the future unit hyperboloid;
the induced real representation on Lambda2(V*);
alpha=dphi in timelike, spacelike, null, zero, and type-changing strata.
```

Positive common scaling is audited through the registered CSN rule.
Orientation is supplied only where the Hodge operation is invoked.

This is a complete local representation audit for these named objects. It
is not a global finite-cell, solution-space, field-equation, or dynamics
audit.

## Metric-led versus template-led

`METRIC_LED`.

Lorentz transformations, induced two-form transformations, Hodge
duality, stabilizers, projectors, and connection distinctions are derived
from the supplied metric/coframe data. No desired particle, action, or
cosmology is used as a target.

## Frozen distinctions

- Observer rapidity `chi` and the local UDT field `phi` remain different
  objects unless a derivation joins them.
- A local frame-group composition rotation is not Levi-Civita curvature
  or spacetime holonomy.
- The nonnull-`dphi` `3+3` split is a conditional local reduction, not a
  carrier, Hopf section, or global bundle completion.
- A frame-component change is not a physical change of the metric tensor.
- `c_E` calibrates post-scale clock/length units; it does not choose
  `dphi`, an observer field, or a connection.

## Candidate tests

### T1 — full-group scalar character

Determine whether the collinear weights `exp(+chi)` and `exp(-chi)` can be
the restriction of a nontrivial continuous real one-dimensional character
of `SO+(1,3)`.

Both an explicit non-collinear composition control and a Lie-algebra
commutator/perfectness control are required.

### T2 — induced bivector representation

Compute the exact six-dimensional action of a collinear boost on real
two-forms. Record every weight and multiplicity. Do not relabel a
`2+2+2` weight structure as a `3+3` split.

### T3 — `dphi` equivariance

For nonnull `alpha=dphi`, test

```text
P(alpha)=alpha_sharp tensor alpha / g^-1(alpha,alpha)
```

and its induced rank-three projectors under simultaneous Lorentz
transformation of the metric data and `alpha`. Test whether a fixed split
is preserved by the whole group or only by the stabilizer of `alpha`.

### T4 — angular-screen compatibility

Use the exact rational non-collinear composition already frozen in the
parent audit. Determine whether its residual screen rotation:

- preserves the timelike-`dphi` split when `dphi` defines the reference
  observer;
- acts consistently on both Hodge-exchanged rank-three sectors; and
- remains meaningful without that alignment.

### T5 — causal-stratum atlas

Classify timelike, spacelike, null, zero, and type-changing `dphi`.
Record the stabilizer type, semisimplicity or degeneration, available
screen geometry, and maximum join ruling for each.

### T6 — CSN descent

Test the frame relation, projector, induced split, and four-dimensional
two-form Hodge exchange under a positive common scale.

### T7 — connection and holonomy separation

Distinguish:

1. finite local frame-group composition;
2. a chosen observer/`dphi` reduction;
3. a projected connection on that reduction; and
4. Levi-Civita spacetime holonomy.

No physical angular connection may be claimed unless it is intrinsic
without an unregistered observer section and survives the appropriate
transport test.

## Falsification and certification contract

An **identity** is allowed only if a natural construction in both
directions exists and is equivariant under the full local frame group.

A **compatible reduction** requires exact preservation/intertwining on a
fully stated stabilizer and exact failure or nonavailability outside that
scope.

A **full scalar extension** fails if every continuous one-dimensional
character of the connected full observer group is trivial.

The package must fail closed if it:

- identifies `chi` with `phi`;
- calls covariant transport preservation of one fixed split;
- reports the collinear bivector weights as `3+3` when their multiplicities
  differ;
- promotes a timelike result to spacelike, null, zero, or type-changing
  strata;
- calls Wigner/screen rotation spacetime curvature;
- infers a carrier, Hopf section, action, source, boundary, or dynamics;
- drops CSN or orientation qualifications; or
- changes any parent or frozen evidence.

## Maximum allowed conclusion

```text
THE_LOCAL_FULL_FRAME_GROUP_EITHER_EXTENDS_OR_OBSTRUCTS_THE_COLLINEAR_RECIPROCAL_CHARACTER_IN_EACH_TESTED_REPRESENTATION;THE_NONNULL_DPHI_3PLUS3_REDUCTION_EITHER_INTERTWINES_WITH_OR_REMAINS_DISTINCT_FROM_THE_NONCOLLINEAR_SCREEN_ROTATION_ON_EXPLICITLY_STATED_STABILIZERS;NO_RESULT_MAY_SELECT_OBSERVER_RAPIDITY_AS_METRIC_PHI_OR_DERIVE_A_GLOBAL_CONNECTION_HOLONOMY_CARRIER_ACTION_SOURCE_BOUNDARY_OR_SCALE
```

Any positive statement is limited to local representation geometry.
