# Completion-scoped realized-observable map

Date: 2026-07-26

Base: `c1036fb498c8ed009733c82ee86cf96152a5ed6e`

Grade: **VERIFIED-WITH-CAVEATS**

## Result

The twelve registered finite-cell completions and seventeen preregistered
geometric readout families now have a complete 204-row type-and-dependency
map.  It is a map of possible lock mechanics, not a selected key or a physical
solution.

The positive result is:

```text
DERIVED:
completion-scoped conditional readout schemas, exact obstruction types,
and a corrected dependency graph separating path transport, loop holonomy,
projector transport, continuous T2 holonomy, and discrete monodromy.
```

The limiting result is:

```text
OPEN:
no registered completion contains a complete metric/coframe witness;
therefore no complete realized R_geom vector or non-identity physical
bootstrap closure relation is presently available.
```

This is not another generic “underdetermined” return.  The missing inputs are
localized in `LOCK_LINKAGE_LEDGER.tsv`: a complete metric/coframe profile is
the common prerequisite for most continuous readouts; global boundary/cap/
glue data control descent; the toric ensemble needs `(H,S)` and an integral
lattice; observer separation needs a native comparison protocol; topology
needs a supplied map or bundle; and physical closure still lacks its complete
inputs, target, normalization, pairing, and operator.

## Exact coverage

- 12/12 completion classes;
- 17/17 readout families;
- 204/204 unique completion/readout rows;
- 10/10 map gates on every row;
- 10/10 preregistered candidate relations;
- 21/21 frozen source identities after one append-only hash correction;
- 256/256 cap-pair determinant controls: `P0=16`, `P1=58`, `P_GT1=182`;
- 8/8 `GL(2,Z)` monodromy determinant controls;
- 29/29 production checks;
- 31/31 independent checks;
- 22/22 exercised fail-closed mutations.

## What differs across completions

For FC01–FC09 and FC12, the same broad readout *types* exist, but their global
descent rules differ: retained boundaries, primitive or singular caps,
periodic monodromy, mirror lifts, orientation reversal, and quotient data act
on different channels.

FC10 moves lattice/cap data from a discrete family schema to a conditional
stratified schema.  FC11 is the sharp control: without a global integral torus
orbit structure, R09–R12 are unavailable rather than silently extrapolated.

The completion summaries deliberately call these entries schemas.  R17, for
example, is conditional topological data and is not thereby a native
`R_geom` component or a derived carrier.

## Transport distinctions repaired by adversarial review

The initial generated draft incorrectly inherited R06 open-path
Levi-Civita rulings from projector/Kato transport and inherited R10 continuous
`T2` holonomy rulings from shortest-character and principal-circle data.
Those conflations were corrected before banking:

1. R06 is now an endpoint-frame map from Levi-Civita transport on a supplied
   metric and path.
2. R07 remains based-loop tangent holonomy, with only its conjugacy data
   frame-independent.
3. R08 remains Kato transport of a supplied smooth fixed-rank projector.
4. R10 is continuous full-`T2` connection holonomy and requires the connection
   profile, loop, lattice trivialization, and completion lift.
5. R11 is discrete cap/glue/monodromy family data, not continuous holonomy and
   not a realized completion witness.

FC12's zero Kato generator in a coordinate projector frame therefore does not
imply zero Levi-Civita transport.  A projected principal-circle characteristic
also cannot replace full `T2` holonomy.

## Relation audit

The ten candidate relations reduce to:

- geometric identities: Q01, Q02, Q07;
- completion compatibilities: Q03, Q06, Q08;
- discrete classification rules: Q04, Q05;
- an explicit source gap: Q09;
- a not-derived physical closure proposal: Q10.

All ten have `physical_closure=NO`.  Cartan/Bianchi identities, scale weights,
cap determinants, monodromy, Reciprocity compatibility, and systole wall
crossing constrain legal assemblies, but none supplies a non-identity law
that fixes one physical state.

## Caveats and authority boundary

- The completion registry is a bounded taxonomy, not proof that it exhausts
  all imaginable global completions.
- The 204 rows classify the frozen source universe; they are not on-shell
  metric solutions.
- `X_max` remains a working observer-pair supremum type, not an attained
  maximum or computed value.
- The temporal-`phi` separation family remains derived only on its stated
  everywhere-timelike, nonzero-`dphi`, complete-level branch.
- The carrier and Hopf data remain conditional/`POSIT`-scoped.
- No completion, boundary functional, action, carrier, physical scale,
  density, mass, energy, PDE, time-live evolution, or GPU solve was selected
  or launched.

## Four evidence gates

1. **Preregistered:** yes, at `c457bc4`; the source-universe amendment was
   frozen at `b3325dd`, and the S17 transcription correction was preserved as
   an append-only layer at `4a95a7b`.
2. **Full or bounded scope:** full 12×17 frozen matrix; the completion universe
   itself remains a bounded registered taxonomy.
3. **Independently verified:** yes, by a standard-library reconstruction that
   does not import the production generator, plus a fresh adversarial review.
4. **Premises audited:** yes; exact stamps are in `PREMISE_LEDGER.tsv`.

The maximum supported grade is therefore `VERIFIED-WITH-CAVEATS`, not a
settled physical closure theorem.
