# UDT finite-cell Cartan transport atlas — preregistration

Date: 2026-07-23

Base: `029e9d134bec1e992849f3051fcfe249411784aa`

Mode: metric-led, CPU-only exact local transport algebra plus complete
registered-family cross-classification

## Whole question

Follow the newly derived `3+3` local frame-algebra reduction through every
registered finite-cell completion family and every causal type of
`dphi`. Determine exactly:

1. where the fixed-rank reduction persists;
2. when the Levi-Civita connection preserves it;
3. which connection components mix its two rank-three sectors;
4. what geometric transport remains available when mixing is nonzero;
5. how the structure changes on spacelike strata; and
6. how it degenerates at null, zero, type-changing, singular, cap,
   mirror, and gluing strata.

## Branch universe and honesty boundary

The global universe is the exact twelve-row
`COMPLETION_CLASS_REGISTRY.tsv` inherited by
`FINITE_CELL_BRANCH_ATLAS.tsv`.

These are registered parametric completion families:

```text
FC01 through FC12.
```

They are not twelve solved universes. The frozen source ledger records:

- eleven parametric completion types with no complete `(g,phi)` witness;
- one conditional reciprocal-toric open-profile control;
- zero complete on-shell finite-cell `(g,phi)` solutions.

This audit may classify exact transport and degeneration conditions for
all twelve rows. It may not turn a completion type or local witness into a
complete branch solution.

## Complete local coframe scope

At each regular Lorentzian point, an orthonormal frame is used only as a
tensorial normal form. The full local connection retains all six
independent Lorentz-algebra components:

```text
3 spatial rotations + 3 boosts/extrinsic components.
```

No round screen, diagonal coordinate metric, zero shift, static field, or
WR-L reduction is imposed. Every arbitrary complete-coframe amplitude,
shift, and angular dependence enters through the metric, `dphi`, and the
six connection one-forms.

The local exact result must be frame-covariant before it is crossed with
the twelve completion families.

## Causal strata

All are `free-and-explored`:

- timelike nonzero `dphi`;
- spacelike nonzero `dphi`;
- nonzero null `dphi`;
- zero `dphi`;
- timelike-to-null-to-spacelike change;
- same-causal-type passage through `dphi=0`;
- metric or manifold singularity.

No causal class is a target.

## Registered inputs

| Input | Status | Limit |
|---|---|---|
| four-dimensional conformal-Lorentzian metric/coframe parent | `pinned-by-THEORY` | no selected solution |
| `alpha=dphi` | `pinned-by-THEORY` | dynamics open |
| timelike `3+3` boost/rotation Cartan join | `PARENT_DERIVED_CONDITIONAL` | timelike nonzero `dphi` |
| spacelike real `3+3` Hodge-exchanged split | `PARENT_DERIVED_CONDITIONAL` | not an observer split |
| twelve completion families | `pinned-by-REGISTERED_ATLAS` | taxonomy, not solved fields |
| Levi-Civita connection | `pinned-by-GEOMETRY` after representative | local CSN dependence audited |
| orientation | `free-and-explored` | required for ordinary Hodge |
| boundary/cap/glue profiles | `free-and-explored` | no profile invented |
| static versus time-live | `free-and-explored` | no evolution equation |
| action, source, carrier, density, scale | `OPEN_NOT_USED` | no selection |

## Exact transport tests

### T1 — general connection blocks

Compute the induced real `Lambda2` connection for the general six-component
Lorentz connection. Relative to the timelike `3+3` split, separate:

- stabilizer/rotation blocks that act within each rank-three sector;
- boost/extrinsic blocks that map between them.

Repeat for the spacelike line and its `SO+(1,2)` stabilizer/complement
decomposition.

### T2 — preservation and mixing

For the line projector `P` and induced projector `Pi`, derive:

```text
Levi-Civita preservation along T iff nabla_T P=0
                              iff nabla_T Pi=0.
```

Record the exact off-diagonal mixing rank for a generic one-direction
connection witness and retain the possibility of complete mixing from
multiple independent tangent directions.

### T3 — Kato/projector transport

For `Pi+Pi_bar=I`, test

```text
K=(nabla_T Pi)Pi+(nabla_T Pi_bar)Pi_bar,
[K,Pi]=nabla_T Pi.
```

Determine whether the corrected connection preserves the evolving
subbundles. This is geometric transport, not physical time evolution.

### T4 — Hodge and CSN

Test Hodge exchange and connection compatibility on oriented strata.
Separate:

- CSN invariance of the projector split; from
- representative dependence of Levi-Civita preservation/mixing.

An explicit positive local common-scale counterexample is required before
calling connection preservation CSN invariant.

### T5 — degeneration controls

Use exact analytic controls for:

- everywhere timelike and everywhere spacelike gradients;
- a nonzero null crossing;
- a zero-gradient point with direction-dependent limiting projectors;
- a timelike/spacelike causal sign change; and
- a same-type zero crossing with noncanonical continuation.

### T6 — complete registered-family cross

Every FC01–FC12 row must receive:

- source data level;
- static-spatial persistence ruling;
- time-live persistence ruling;
- timelike Cartan interpretation;
- spacelike symmetric-pair interpretation;
- Levi-Civita mixing status;
- Kato transport status;
- degeneration/gluing/orientation status; and
- maximum conclusion.

No generated audit record may influence family selection.

## Falsification and certification contract

The package fails if it:

- omits or duplicates a completion family;
- reports any parametric family as an on-shell solution;
- freezes boost/extrinsic or angular connection components;
- calls nonzero connection mixing degeneration;
- calls Kato transport Levi-Civita preservation or physical evolution;
- promotes the timelike boost/rotation interpretation to spacelike
  `dphi`;
- continues the normalized projector canonically through null or zero
  `dphi`;
- treats `phi=0` as `dphi=0`;
- calls the Levi-Civita mixing criterion pre-scale CSN invariant;
- drops cap, mirror, nonorientable, singular, or type-changing guards;
- selects a topology, action, carrier, boundary, density, scale, or
  physical branch; or
- changes parent or frozen evidence.

## Maximum conclusion

```text
EXACT_LOCAL_PERSISTENCE_MIXING_KATO_TRANSPORT_AND_CAUSAL_DEGENERATION_RULES_FOR_THE_DPHI_ASSISTED_3PLUS3_REDUCTION_CROSSED_WITH_ALL_TWELVE_REGISTERED_FINITE_CELL_COMPLETION_FAMILIES__ZERO_COMPLETE_ONSHELL_BRANCHES_AND_NO_PHYSICAL_SELECTION
```
