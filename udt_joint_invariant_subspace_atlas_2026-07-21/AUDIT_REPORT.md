# Joint Invariant-Subspace Atlas — Audit Report

Date: 2026-07-21

Status: `COMPLETE_VERIFIED_WITH_CAVEATS`

Maximum conclusion:
`BOUNDED_POINTWISE_JOINT_INVARIANT_SUBSPACE_ATLAS_CHARACTERIZED`.

## Result first

The corrected atlas, complete only for its nine named pointwise families, finds a sharp hierarchy
rather than a blanket negative.

Smaller metric/phi families often **do** carry a unique real central `2+2` split: 11,983 family rows
across 5,210 configurations. Each has primary-block ranks `1;1;2`; the rank-two block comes from a
complex-conjugate spectral pair whose combined real plane is canonical. Another 2,225 rows have four
real lines and therefore three competing `2+2` pairings.

But none of those unique smaller-family splits survives the complete curvature orchestra. The full
Riemann-plus-phi and Weyl-plus-phi families generate the full four-dimensional matrix algebra in
5,760 of 6,144 configurations, including every configuration where a smaller family has a unique
split. Their only common invariant subspaces are therefore zero and the full tangent space. In the
remaining 384 configurations the joint algebra is scalar and supplies no distinguished plane.

The gradient-generated orbit is never two-dimensional, and neither the Riemann nor Weyl bivector
operator has an isolated real simple eigenbivector plane anywhere in the registered ensemble.

The bounded observation is therefore:

> Individual sections can organize themselves into a real `2+2` pattern, but the complete
> pointwise two-jet orchestra does not preserve that partition.

This does not rule out a distribution selected by transport, higher jets, global integrability,
finite-cell completion, boundary data, or time-live dynamics. None of those entered this audit.

## Complete bounded coverage

- Parent configurations: 6,144 = 48 carriers x 16 masks x 8 contexts.
- Registered operator families: nine.
- Original family classifications: 55,296.
- Nonlinear coordinate three-jet probes: two per configuration.
- Transformed configurations: 12,288.
- Nonlinear family comparisons: 110,592.
- Discarded configurations or classifications: zero.
- Non-uncertain nonlinear classification discordances: zero.
- Retained uncertain nonlinear comparisons: 24.
- Worst parent-tensor residual: zero.
- Worst nonlinear covariance residual: `2.2204460492503131e-16`.

The corrected independent verifier rebuilt the metric curvature, covariant phi-Hessian, nine named operator
families, commutants, central blocks, gradient orbits, bivector tests, and nonlinear coordinate jets
on 480 original and 960 transformed preregistered anchors. All 12,960 independent family
classifications agree with the atlas. It computes every anchor before reading saved builder
classifications and constructs real primary projectors by an independent Vandermonde/CRT method.
Four anchor comparisons fall in the registered uncertainty band and are retained. All ten exercised
catch-proofs reject their mutations.

## Joint-family findings

| family | generated-algebra dimensions | rank-two central result | gradient-orbit dimensions |
|---|---|---|---|
| Ricci | 1 on 768; 4 on 5,376 | unique on 4,298; three competing on 1,078 | 0/1/4 |
| phi Hessian | 1 on 3,072; 4 on 3,072 | unique on 3,003; three competing on 69 | 0/4 |
| phi dyad | 1 on 3,072; 2 on 3,072 | none | 0/1 |
| Ricci + Hessian | 1 on 384; 4 on 3,072; 16 on 2,688 | unique on 2,533; three competing on 539 | 0/4 |
| Ricci + Hessian + dyad | 1 on 384; 4 on 2,688; 16 on 3,072 | unique on 2,149; three competing on 539 | 0/4 |
| Riemann generators | 1 on 768; 16 on 5,376 | none | 0/1/4 |
| Weyl generators | 1 on 768; 16 on 5,376 | none | 0/1/4 |
| full Riemann joint | 1 on 384; 16 on 5,760 | none | 0/4 |
| full Weyl joint | 1 on 384; 16 on 5,760 | none | 0/4 |

Across the nine named families there are 11,983 unique and 2,225 multiple central `2+2` rows, and
zero two-dimensional gradient-generated orbits. The 11,983 unique rows occur in Ricci (4,298), phi
Hessian (3,003), Ricci-plus-Hessian (2,533), and Ricci-plus-Hessian-plus-dyad (2,149). Every one maps
to `FULL_MATRIX_ALGEBRA_IRREDUCIBLE` after either complete curvature family is added. The parent
gradient is zero in 3,072 configurations, spacelike in 2,304, and timelike in 768; no null-gradient
parent occurs in this ensemble.

## Curvature-eigenbivector findings

Both curvature operators yield zero isolated real simple eigenplanes in all 6,144 configurations.
The Weyl operator has six isolated complex eigenvalues in 5,376 configurations and a sixfold
repeated eigenvalue in 768. Riemann has a mixture of complex isolated spectra, 118 real but
non-simple eigenbivector cases, and 768 sixfold-repeated cases. No vector was selected from a
repeated eigenspace, and no non-simple bivector was misreported as a tangent plane.

## Nonlinear chart audit

Both registered nonlinear maps use the complete metric and scalar chain rule through coordinate
three-jets. Every non-uncertain algebra dimension, commutant/center dimension, central-block class,
gradient-orbit class, and bivector multiplicity is unchanged. The 24 near-threshold comparisons are
recorded in `NUMERIC_MARGIN_LEDGER.tsv`; none produces a unique split or supports a physical claim.

The first atlas pass is preserved. It produced 23,994 apparent nonlinear discordances because the
classifier diagonalized an arbitrary numerical representative of a repeated scalar center. The
resulting eigenspace basis was coordinate-dependent even though the invariant algebra was not.
Replacing that diagnostic with exact scalar-identity handling and polynomial spectral projectors
removed all non-uncertain discordances. `CLASSIFIER_CORRECTION.md` records the correction, and the
failed result and transcript remain historical evidence.

A second, more important correction was forced by the first fresh adversarial review. The corrected
scalar-center classifier still rejected complex spectra, missing real primary planes made by
complex-conjugate pairs and incorrectly supporting a zero-unique-split report. That failed review,
result, transcript, and family census are preserved. The current builder uses real polynomial
spectral projectors; the verifier uses a separately implemented Vandermonde/CRT construction. Both
recover the adversarial rank pattern `1;1;2` and agree on all independent anchors.

The second fresh review confirmed that census but found a further fail-closure defect: both
implementations treated an exact Lorentzian self-adjoint nilpotent Jordan operator as classified.
It also found that the implemented projector gate was `1e-7`, not the preregistered `1e-9`, and that
several catches used catch-only predicates. That failed review is preserved. The current builder and
independent verifier separately test semisimplicity of every primary cluster, mark the exact Jordan
counterexample uncertain, enforce `1e-9` on projector acceptance and stability, and pass the saved
registries, coverage, bivector census, uncertainty ledger, and result through the same validators
used by their mutations. The full replay reproduces the prior census; a new fresh correction review
is still required before final banking.

The third fresh review independently reproduced the Jordan correction, census, full-family
escalation, Riesz-contour conjugate projector, catches, manifests, navigation, and wording. It then
found one remaining literal `1e-7` in the production bivector complementary-projector pairing test.
No saved row depended on it because the ensemble has zero candidate bivector splits, but it violated
the controlling `1e-9` contract. That failed review is preserved. The production gate now uses
`RANK_TOL`; the full atlas and independent verifier again reproduced the same census. At that
historical layer, a post-tolerance fresh review was still required before final banking.

The final post-tolerance fresh review is `PASS`. It independently rechecked every projector
threshold, both Jordan paths, the full saved census and escalation, a third Riesz-contour
construction of the conjugate rank-two plane, all ten catches, compute-before-read ordering,
manifests, navigation, and claim scope. It required no further correction.

## What survives the audit

- `OBSERVED`, bounded and independently verified: four smaller named families produce 11,983 unique
  real central splits across 5,210 configurations.
- `OBSERVED`, bounded and independently verified: the complete Riemann-plus-phi and Weyl-plus-phi
  pointwise two-jet families are full-algebra irreducible on 5,760 configurations—including every
  smaller-family unique-split case—and fully ambiguous on the remaining 384.
- `OBSERVED`, bounded and independently verified: no registered gradient orbit or isolated real
  simple curvature eigenbivector supplies a two-plane.
- `OPEN`: whether transport, higher jets, integrability, global finite-cell closure, a boundary
  functional, or time-live structure selects a distribution.
- `OPEN`: any physical angular sector, action, source, carrier, boundary, scale, or bootstrap law.

## Caveats and premise audit

- This is complete only for the nine **named** preregistered pointwise families. Joint subsets such
  as `{R,D}`, `{H,D}`, and partial curvature-plus-phi combinations were not registered. It is not
  exhaustive over all subsets or all possible differential concomitants.
- The two nonlinear coordinate maps are finite probes, not a proof over the full diffeomorphism
  group.
- Central reducing subspaces are a strict selector test. Noncentral invariant flags are retained as
  ambiguity and are not promoted to preferred physical planes.
- Rank tolerance `1e-9`, eigenvalue clustering `1e-8`, and the `1e-11..1e-7` uncertainty band are
  numerical choices pinned by habit. All threshold-near rows are retained.
- No action, field equation, source, carrier, section, boundary, physical scale, topology, or
  evolution law was loaded.

## Four banking gates

1. Preregistered: **YES**, including the exact independently verified anchor set.
2. Full space or bounded scope justified: **YES** for all 6,144 configurations, nine registered
   families, and two nonlinear probes; not exhaustive beyond that pointwise two-jet scope.
3. Independently verified: **YES** on 480 original and 960 nonlinear anchors with an independent
   real-primary implementation and ten catches. Three fresh reviews failed and forced preserved
   corrections; the final post-tolerance fresh review passed with no required correction.
4. Every premise audited: **YES** in `PREMISE_STATUS_LEDGER.tsv`; the physical selector and all
   dynamical/global structures remain `OPEN`.

This is a bounded invariant-subspace atlas, not a physical section-selection theorem.
