# UDT Bank-Simplex Interior Atlas

Date: 2026-07-23

Status: `VERIFIED_WITH_REGISTERED_LATTICE_AND_CONTINUITY_CAVEAT`

Maximum conclusion:

`BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_WITH_INTERVAL_AND_MATRIX_CHECKS`

## Result first

The complete four-bank interior contains structure that the six pairwise edges do not determine.

At both frozen resolutions, all 384 J1 generator/coefficient sheets have:

- one connected negative component on the `B0-B1-B2` base lattice;
- one connected positive base complement;
- exactly two `t` transitions above every negative base node;
- exactly one `t` transition above every positive base node;
- a sampled inference of two null transition families, one positive sign-node component, and two
  negative sign-node components.

Every pairwise edge on that base remains positive. The additional negative component is therefore a
genuine three-bank interior property of the registered J1 configuration chart, not an edge effect.

All 384 J2 evaluated-cofield sheets instead have:

- a wholly positive `B0-B1-B2` base lattice;
- exactly one transition on every sampled radial fiber;
- a sampled inference of one null transition family, one positive sign-node component, and one
  negative sign-node component.

There are zero numerically-zero nodes. L1 and L2 reproduce the same qualitative class for all 768
chart/group sheets.

The chart disagreement is load-bearing. It means that the registered endpoints and their edge
adjacency do not determine the interior causal organization. J1 and J2 are chosen configuration
charts; neither has been derived as UDT's physical coframe-composition law. The pocket therefore is
`OBSERVED_BOUNDED_LATTICE`, not a selected physical sector.

## Domain and counts

The identity universe is all 48 deformation vectors times all eight active masks, giving 384
matched groups. Both charts retain all ten coframe fields, `phi`, the angular block, and all four
base-angular shifts.

The two symmetric triangular lattices are:

| level | `u` nodes | simplex denominator | simplex nodes | `t` nodes | nodes/sheet |
|---|---:|---:|---:|---:|---:|
| L1 | 9 | 8 | 45 | 65 | 26,325 |
| L2 | 17 | 16 | 153 | 129 | 335,529 |

Across both levels and charts the independent route checked 277,903,872 saved node signs.

At L2, J1 has 154–199 negative base nodes per sheet and the same number of two-transition fibers.
The remaining 2,402–2,447 fibers have one transition. J2 has 2,601 positive base nodes and 2,601
one-transition fibers in every sheet.

The root ranges in `CHART_COMPARISON.tsv` are linear lattice-bracket interpolants. They describe
sampled shape only and are not exact roots.

## Exact and interval controls

For both charts the registered coframe has

```text
det(g) = -exp(2*(a+c+d+f)) < 0
```

at every finite latent configuration. No metric degeneracy or signature change is introduced by
the barycentric charts.

The original broad `8 x 8 x 8 x 16` interval cover was retained as a complete enclosure census. It
contains 6,291,456 initial domain boxes. Of those, 5,140,116 are derivative-indeterminate because
the broad four-variable interval extension overestimates variation. There are 342,811
base-face-indeterminate boxes and zero B3-vertex-indeterminate boxes. No indeterminate box was
coerced to a sign or used as a continuous-topology proof.

The original depth-18 recursion was withdrawn in a separately committed numeric-scope correction
because splitting more than five million broad boxes exponentially was not a credible bounded
certificate. The maximum conclusion was downgraded before the converged L1/L2 production map.

## Independent reconstruction

The independent verifier does not import the production scalar:

1. it rebuilds the four bank coefficient tensors and carriers;
2. reconstructs the full `h`, angular `q`, and shift blocks;
3. evaluates `s` through the block-metric Schur inverse at every saved node;
4. checks the block determinant independently;
5. uses 80-decimal interval arithmetic and a general full `4 x 4` determinant/adjugate route at 34
   anchors spanning both charts, all masks, sixteen carriers, base extrema, both true global
   narrowest L2 nodes, and both transition directions where present.

Results:

```text
node signs checked:             277,903,872
node-sign mismatches:                     0
transition-count mismatches:              0
nonnegative determinants:                 0
mpmath80 full-matrix anchors:            34 / 34 PASS
end-to-end mutation catches:             10 / 10 PASS
```

The boundary replay checks 792,576 same-sign edge nodes and 59,904 cross-sector radial fibers with
zero failures. It also reproduces the prior 4,608-sheet adjacency census exactly: 2,304 uniformly
spacelike sheets and 2,304 single regular null graphs.

## What is and is not invariant

The following survive both charts:

- all registered endpoints and edge classes;
- Lorentzian nondegeneracy;
- at least one sampled transition from the `B0-B1-B2` side toward `B3`;
- one connected sampled positive region.

The following are chart-dependent:

- whether the three-bank base has an interior negative pocket;
- whether some radial fibers cross twice;
- the sampled null and negative component count;
- transition location and shape.

This is scientifically useful precisely because it identifies the missing join: UDT does not yet
supply a native rule for composing complete coframes across this configuration family.

## Completeness and premise audit

This package is one tile, not the whole theory.

- `FIELDS`: all registered ten coframe fields and `phi` are retained subject to each frozen mask.
- `DOMAIN`: the complete bank-weight tetrahedron and full registered source path are sampled.
- `BRANCH`: all 384 registered groups and both charts are accounted for.
- `REGIME`: the frozen analytic polynomial/coframe ensemble only.

It does not contain an action, Euler-Lagrange equations, physical boundary selection, global
finite-cell completion, topology selection, dynamics, stability spectrum, source, carrier, scale,
density, or matter interpretation.

No physical value, boundary condition, mechanism, or empirical target was used as an acceptance
filter. The complete premise ledger is `PREMISE_STATUS_LEDGER.tsv`.

## Four banking gates

1. Preregistered: **YES**, initial commit `e3c3912`, numeric-scope correction `ac6e425`, and lattice
   implementation freeze `cd2d315`.
2. Full space or bounded scope justified: **YES FOR BOTH COMPLETE REGISTERED LATTICES**, not the
   continuous or arbitrary-metric configuration space.
3. Independently verified on the load-bearing premise: **YES INTERNALLY**, through a separate
   block-metric route plus 80-decimal full-matrix anchors, and **YES FRESH-ADVERSARIALLY**. The
   zero-context review returned `PASS-WITH-CAVEATS`; its requested source-hash gates, two global
   narrowest-node anchors, real end-to-end mutation catches, and bounded null-family wording were
   applied and reverified before banking.
4. Every premise audited: **YES FOR THE DECLARED LATTICE ATLAS**; physical realization remains open.

Final grade: `VERIFIED-WITH-CAVEATS`, where the caveat is continuous topology and chart selection—not
a hidden physical interpretation.
