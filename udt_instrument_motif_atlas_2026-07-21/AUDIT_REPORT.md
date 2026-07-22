# UDT Instrument-Motif Atlas — Audit Report

Date: 2026-07-21

Status: `COMPLETE_VERIFIED_WITH_CAVEATS`

Maximum conclusion:
`BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED`.

## Result first

The complete registered pointwise instrument lattice does not look like a search through millions
of unrelated combinations. Its 190,464 family rows reduce to five recurring certified motif types,
plus 17 retained numerical-margin rows. Only 14 complete 31-family motif fingerprints occur across
all 6,144 configurations.

The five certified building blocks are:

| motif | primitive shape | metric signature structure | rows |
|---|---:|---|---:|
| scalar/silent | `4` | Lorentzian four-space, no proper subspace selected | 22,656 |
| coupled plane plus two lines | `1+1+2` | one Lorentzian plane and two spacelike lines | 16,431 |
| four lines | `1+1+1+1` | one timelike and three spacelike lines | 2,764 |
| line plus three-space | `1+3` | gradient line and its metric-orthogonal complement | 5,760 |
| full irreducible weave | `4` | Lorentzian four-space, no proper common invariant subspace | 142,836 |

The recurring rank-two primitive block is always Lorentzian (`N1_P1_Z0`), while its two primitive
rank-one companions are spacelike. It is the real primary block of a complex-conjugate Ricci or
phi-Hessian spectrum. Thus the exact motif is `1+1+2`, not two primitive planes. Calling that block
a reciprocal clock/ruler plane is an interesting possible interpretation, but remains `OPEN`.

The strongest ensemble interaction is not rare alignment but generic crossing. In all 2,090 clean
configurations where singleton Ricci and singleton phi Hessian each possess a unique split, their
Lorentzian planes have zero pairwise intersection dimensions, commutator rank four, and a joint
full-matrix algebra. They do not preserve the same partition; together they weave all four tangent
directions. The unnormalized phi-gradient dyad contributes a different motif—a line plus an
orthogonal three-space—and in all 7,840 registered nonzero-gradient incidences with a certified
split, that gradient crosses both sides of the split rather than lying wholly in either.

The curvature-generator families are likewise simple at this resolution: Riemann and Weyl are each
full-algebra irreducible in 5,376 configurations and scalar/silent in 768. Their matched subset
families are motif/projector-equivalent throughout the ensemble, although this does **not** assert
that the curvature operators themselves are equal. Adding Ricci to a curvature-containing family is
also motif-redundant in this bounded atlas.

These are reusable local building blocks and interaction rules. They are not a selected physical
structure.

## Complete bounded coverage

- 6,144 immutable metric/phi pointwise two-jets;
- all 31 nonempty subsets of five intrinsic groups: `R`, `H`, `D`, `RG`, `WG`;
- 190,464 original family rows and 237,388 primitive-block rows;
- all 75 directed one-instrument Hasse edges and 460,800 edge rows;
- 12,288 nonlinear transformed configurations and 380,928 transformed family comparisons;
- zero discarded configurations, families, edges, or numerical margins;
- zero non-uncertain family, edge, or Ricci/Hessian-alignment discordances under the two chart probes;
- 429 transformed edge-label differences, all inside 557 explicitly uncertain comparisons;
- 145 transformed uncertain family rows, 162 numerical-margin ledger rows, and no promotion of a
  margin to a certified result.

The original preregistration's `80` edge count included five edges from the excluded empty subset.
That arithmetic error was corrected and committed before any new motif outcome; the correct
nonempty-lattice count is `75`. A later accounting correction preserved the first full return and
separated uncertain from non-uncertain transformed edge differences without changing any scientific
ledger bytes.

## Instrument and interaction grammar

Singleton Ricci yields 4,296 clean `1+1+2` rows, 1,078 four-line rows, 768 scalar rows, and two
uncertain rows. Singleton Hessian yields 3,003 `1+1+2`, 69 four-line, and 3,072 scalar rows.
Singleton dyad yields 3,072 `1+3` and 3,072 scalar rows. The parent ensemble contains 2,304
spacelike, 768 timelike, and 3,072 zero gradients; it contains no null-gradient configuration, so
this audit does not determine the dyad motif at a nonzero null gradient.

When the gradient is nonzero, `H+D` is full irreducible in 3,067 rows with five retained margins.
`R+H` is full irreducible in 2,688 rows while preserving simpler motifs elsewhere. On the complete
one-instrument edge lattice, the assembly rules are:

- full weave remains full: 313,692 edges;
- primitive blocks remain exactly preserved: 57,596;
- prior blocks mix into full algebra: 75,996;
- ambiguity becomes a certified motif: 13,437;
- numerical uncertainty: 79.

`BUILDING_BLOCK_LEDGER.tsv` records the motif vocabulary and `INTERACTION_RULE_LEDGER.tsv` records
the bounded grammar without ranking any outcome by physical resemblance.
`ADDED_INSTRUMENT_TRANSITION_CENSUS.tsv` gives the same transition counts separately for each added
instrument; every instrument occupies exactly 92,160 registered edges.

The first package-contract replay caught a readout-only ordering error in its expected text string
for the timelike `1+3` signature set. `CONTRACT_READOUT_CORRECTION.md` preserves the failure and
clarifies that the census rank and signature strings are canonically sorted, not positional pairs.
The building-block ledger now displays both `1+3` signature alternatives as unordered sets. No raw
block, census, or scientific result changed.

## Independent verification

An independent verifier imports neither the production core nor builder. It independently rebuilt
metric curvature, scalar Hessian, all five instrument groups, generated algebras, commutants,
centers, real-primary projectors, block signatures, gradient incidence, Ricci/Hessian alignment,
edge relations, and both nonlinear chart transformations.

The anchor set was frozen by configuration-ID hash before saved classifications were read. On 384
configurations it reproduced 11,904 original and 23,808 transformed classifications—35,712 saved
comparisons—with zero discordance. Its worst saved-projector distance was
`5.223932397768749e-12`; its worst nonlinear covariance residual was
`1.9608027118610747e-16`. Omitting the nonlinear scalar-Hessian jet term produced the required
nonzero catch residual `0.012773925363472115`.

The first independent K09 implementation compared a valid alternate linear chart with the same
pointwise Jacobian; the complete tensor transformation correctly gave zero rather than exposing an
omitted nonlinear jet. That failed transcript is preserved. The corrected K09 keeps the transformed
metric jets but deliberately omits the scalar-Hessian chain-rule term proportional to the inverse-map
second jet, producing the nonzero residual above. `VERIFIER_IMPLEMENTATION_CORRECTION.md` records the
correction; no atlas outcome or tolerance was changed.

Because the blind anchors happened to include no uncertain original classifications, a separately
preregistered post-outcome escalation targeted **every** unique identity in the complete 162-row
margin ledger. It independently replayed 124 unique original identities and 248 transformed
identities. It retained 156 uncertain classifications and found zero discordant identities. No row
was selected by scientific appearance.

All 12 production catches and 12 independent catches pass. `VERIFICATION_RESULT.json` and
`MARGIN_ESCALATION_RESULT.json` are machine-readable records.

Before final replay, an internal audit found that the edge and operator-count mutation catches used
catch-local count predicates even though they rejected the intended corruptions. The issue was
preregistered in `CATCH_VALIDATOR_STRENGTHENING.md`. The production replay now sends its real 75-edge
registry and every real family operator list through reusable validators; the edge and dropped-
operator mutations use those same validators. The independent implementation separately constructs
the exact edge set and operator count and exercises its own validators. No classification, tolerance,
input, or scientific ledger changed.

## What is and is not learned

- `OBSERVED`: a compact five-motif local algebraic vocabulary and a 14-fingerprint assembly grammar
  within the complete registered two-jet lattice.
- `OBSERVED`: the `1+1+2` motif is a Lorentzian primitive plane plus two spacelike primitive lines.
- `OBSERVED`: unique Ricci and Hessian planes cross rather than align in every clean both-unique
  configuration in this ensemble.
- `OBSERVED`: the phi-gradient dyad supplies a line/three-space motif and crosses both sides of every
  registered clean unique split with nonzero gradient.
- `OPEN`: whether the Lorentzian primitive plane has observer, reciprocal, clock, ruler, or physical
  angular meaning.
- `OPEN`: transport, integrability, global compatibility, finite-cell completion, action, source,
  carrier, boundary, scale, matter, and physical selection.

No negative here applies to higher jets, time-live dynamics, transport, topology, or a global
solution. Conversely, no attractive pointwise motif may be promoted into those structures.

## Caveats and premise audit

- The ensemble is exhaustive only for the immutable 6,144 pointwise two-jets and five registered
  groups. It does not exhaust every differential concomitant or every possible metric jet.
- No nonzero null-gradient configuration occurs; all dyad `1+3` statements are bounded to the
  registered spacelike or timelike gradients.
- Two nonlinear maps probe covariance but do not prove it over the diffeomorphism group.
- Central reducing blocks are a strict algebraic diagnostic. They need not exhaust physically
  meaningful noncentral or globally transported structures.
- Rank tolerance `1e-9`, relative eigenvalue clustering `1e-8`, and uncertainty band
  `1e-11..1e-7` are numerical choices pinned by habit; every observed margin is retained.
- No action, EOM, source, carrier, section, boundary, physical value, observational anchor, or scale
  was loaded.
- No matched generic Lorentzian or GR ensemble was evaluated. The occurrence and interaction census
  belongs to these UDT metric/phi instruments, but the abstract rank/signature motifs are not shown
  to be unique to UDT.

## Four banking gates

1. Preregistered: **YES**. The lattice arithmetic correction preceded all new motif outcomes; the
   uncertainty-accounting correction preserved the first return before corrected replay; the
   catch-validator strengthening was registered before its strengthened replay.
2. Full space or bounded scope justified: **YES**, for every registered configuration, subset, edge,
   and nonlinear probe; scope outside this finite pointwise box remains explicitly open.
3. Independently verified: **YES**, on 384 outcome-blind configurations plus every unique identity
   in the full numerical-margin ledger, with independent algebra and nonlinear-jet implementations.
4. Every premise audited: **YES**, in `ANTI_IMPOSITION_AUDIT.tsv`, `COMPLETENESS_MAP.md`, and
   `STATUS_LEDGER.tsv`. No physical interpretation is promoted.

This is a verified bounded motif atlas, not an action, matter derivation, or physical-section theorem.
