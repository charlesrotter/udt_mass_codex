# UDT Instrument-Motif Atlas — Preregistration

Date: 2026-07-21

Parent commit: `8e6b425b08889dd8e0b5f8d7b0ae3945dc1dcacf`

## Observing question

Across every retained pointwise metric/phi two-jet in the immutable 6,144-configuration structural
ensemble, what primitive directional motifs are carried by every nonempty combination of the five
available intrinsic instrument groups, and how do those motifs change when exactly one additional
instrument joins?

The five groups are mixed Ricci `R`, mixed covariant phi-Hessian `H`, unnormalized phi-gradient dyad
`D`, the six Riemann curvature generators `RG`, and the six Weyl curvature generators `WG`.
`INSTRUMENT_SUBSET_REGISTRY.tsv` freezes all 31 nonempty subsets. No combination may be dropped,
promoted, or ranked after outcomes are inspected.

This is metric-led building-block mapping. It does not ask which combination resembles matter, an
angular sector, a carrier, a preferred universe, or a successful action. A rare configuration has
the same ledger weight as a common one; neither is selected as physics.

## Known anchors before this test

The parent joint atlas already observed, for nine named families, recurring primitive ranks
`1;1;2`, four-line ambiguity, a phi-dyad `1+3` tendency, and full mixing in the registered complete
curvature-plus-phi families. A post-atlas readout also counted some Ricci/Hessian/dyad transition
classes. Those are prior observations, not blind predictions from this preregistration.

The new load-bearing questions are the complete 31-family subset lattice, the previously absent
`R+D`, `H+D`, partial-curvature and dual-curvature combinations, primitive-block metric signatures,
unique-plane/gradient incidence, Ricci-versus-Hessian split alignment, and all 80 one-instrument
addition edges.

## Immutable inputs

The builder must hash-check these manifests before reading raw configurations or parent outcomes:

| path | required SHA-256 | role |
|---|---|---|
| `udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt` | `3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757` | 6,144 complete metric/phi two-jets |
| `udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt` | `b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad` | canonical two-jet geometry evaluator |
| `udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt` | `973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2` | corrected invariant-subspace algorithms and historical anchor |

No input or prior package may be edited.

## Complete subset and edge coverage

Bits are frozen as `R=1`, `H=2`, `D=4`, `RG=8`, and `WG=16`. Every integer mask 1 through 31 occurs
exactly once in the subset registry. This deliberately retains algebraically redundant-looking
Ricci/Riemann/Weyl combinations so redundancy itself can emerge as a property.

For each configuration, classify all 31 families. Also construct every directed Hasse edge
`source -> source plus one absent bit`. There are exactly 80 registered edge types and therefore:

- 6,144 configuration rows;
- 190,464 original family rows;
- 491,520 original one-instrument edge rows.

No physical-merit filter or outcome-dependent compression is allowed.

## Motif classification

For each family retain the full algebra/commutant/center classification from the corrected parent
algorithm and additionally record every certified primitive metric-self-adjoint central block:

- rank and metric signature `Nn_Pp_Zz`;
- whether the primitive rank pattern is `4`, `1+3`, `2+2`, `1+1+2`, `1+1+1+1`, another retained
  pattern, noncentral ambiguity, full-algebra irreducibility, or numerical uncertainty;
- for every unique complementary rank-two split, the unordered pair of plane signatures;
- whether nonzero `grad(phi)` lies wholly in one plane, wholly in its complement, is split across
  both, or is numerically unresolved;
- for a primitive rank-two block, the real/complex/repeated discriminant class of every included
  self-adjoint scalar instrument `R`, `H`, and `D` restricted to that block.

The words `plane`, `line`, and `block` describe tangent-space algebra at one point. They do not name
a spatial object, solution profile, foliation, or physical sector.

## Interaction classifications

For each one-bit addition edge, compare the complete source and destination classifications and
projector sets. Report without merit ranking:

- exact preservation of primitive blocks;
- merging/coarsening of source blocks;
- transition to full matrix algebra;
- transition from scalar/noncentral ambiguity to a certified block motif;
- continued or changed ambiguity;
- numerical uncertainty.

Separately, wherever both singleton Ricci and singleton Hessian possess a unique complementary
rank-two split, compare the two unordered projector pairs by similarity-invariant projector traces,
commutator rank, common-image intersection dimensions, and exact same/complementary/commuting-crossing/
noncommuting-crossing classification. No Euclidean coordinate angle may be called physical.

## Nonlinear chart probes

The two nonlinear coordinate three-jets frozen by the parent joint atlas are replayed for every one
of the 31 families. The transformed metric and scalar jets must use the complete chain rule. This
adds 12,288 transformed configurations and 380,928 transformed family comparisons. It is a bounded
two-map covariance probe, not a proof over the diffeomorphism group.

## Premise ledger

| choice | status | scope |
|---|---|---|
| four-dimensional Lorentzian metric plus scalar phi two-jet | `pinned-by-THEORY`, conditional realization | immutable structural ensemble |
| all 6,144 configurations | `free-and-explored` | zero filtering |
| all 31 nonempty subsets of five available groups | `free-and-explored` within bounded registry | exhaustive subset lattice |
| five group definitions | `pinned-by-THEORY` with parent citation | metric/phi pointwise two-jet concomitants |
| two nonlinear coordinate three-jets | `CHOSE` before new outcomes | inherited exact parent probes |
| rank/projector tolerance `1e-9` | `pinned-by-HABIT` | numerical certification only |
| eigenvalue clustering tolerance `1e-8` relative | `pinned-by-HABIT` | numerical classification only |
| uncertainty band `1e-11..1e-7` | `pinned-by-HABIT` | retained, never promoted |
| action, equations, source, carrier, section, boundary, scale | `OPEN` | absent |

No ansatz, boundary condition, physical value, action, or field equation is introduced. The sampled
parent two-jets are a finite algebraic tile, not solutions of an unspecified dynamics.

## Certification and falsification contract

A bounded verified grade requires:

1. all immutable hashes and the 31-row exact subset registry match before computation;
2. exact coverage counts above, zero discarded configurations/families/edges, and all primitive
   block ranks sum to four;
3. every retained block signature has rank equal to its projector rank, and the direct sum of block
   inertias reproduces total Lorentz signature `N1_P3_Z0`;
4. every projector passes idempotence, completeness, mutual annihilation, metric self-adjointness,
   centrality, and operator commutation at `1e-9`;
5. every unique-plane gradient-incidence label is reproduced directly from both complementary
   projectors, without normalizing zero or null gradients;
6. all 80 edge types occur 6,144 times and their source/destination masks differ by exactly one bit;
7. all non-uncertain motif, signature, incidence, alignment, and transition classifications agree
   under both nonlinear chart probes;
8. an independent implementation recomputes every family and motif invariant on a frozen anchor
   set selected by configuration-ID hash before reading saved classifications;
9. exercised catches reject a missing/duplicate subset, missing/duplicate edge, dropped operator,
   supplied coordinate plane, normalized zero/null dyad, bad block signature, mutated gradient
   incidence, omitted nonlinear map jets, uncertainty escalation, defective Jordan classification,
   and false same-split alignment;
10. frozen manifests, prior-package identities, navigation, tests, and the original dirty-checkout
    metadata gates pass.

Any numerical margin or disagreement is retained. No tolerance may be retuned after inspection.

## Maximum allowed conclusion

`BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED`.

The package may describe recurring algebraic building blocks and their interactions as `OBSERVED`
inside this complete finite subset lattice. It may not call any motif a physical angular sector,
carrier, matter seed, action selector, transport law, global structure, boundary condition, or scale
mechanism. It may not authorize a targeted search for a rare combination.

