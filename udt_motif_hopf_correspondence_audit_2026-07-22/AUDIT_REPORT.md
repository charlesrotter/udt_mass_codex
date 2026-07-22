# UDT Motif-to-Hopf Correspondence Audit

Date: 2026-07-22

Status: `CORRECTED_VERIFIED_WITH_REGISTERED_SCOPE`

Maximum conclusion:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The overall motif-to-Hopf correspondence remains a `LEAD`.

## Result first

The new motif vocabulary does connect to the Hopf program, but at two sharply different levels.

First, the complete registered local analytic ensemble contains abundant sampled projector motifs
and nonzero Frobenius obstruction in the registered chart. Of 95,232 instrument-family paths,
93,920 have the same classified motif and matchable projector sets at all 17 sampled nodes. This is
not a continuous-bundle theorem. At the path midpoints, 8,205 families carry the `1+1+2` motif. Its
primitive Lorentzian rank-two plane is numerically nonintegrable in 6,669 cases and integrable in
1,536 in that chart. The 1,395 four-line midpoints have three complementary rank-two splittings;
all 8,370 tested split sides are numerically nonintegrable there.

Second, in the already conditional reciprocal-toric class,

```text
g = -dt^2 + A(phi)^2 dphi^2
    + Omega(phi)^2[exp(-2phi) dxi1^2 + exp(2phi) dxi2^2],
```

the metric `phi` Hessian plus the unnormalized gradient dyad generically recovers the four intrinsic
axes `(t,phi,xi1,xi2)` without an `S2` carrier. The two angular Hessian eigenvalues differ exactly by
`2/A^2`; the dyad distinguishes depth from time. Axis recovery fails only at disclosed degeneracies
`Omega'/Omega=+/-1` unless another intrinsic instrument resolves them.

Once periodic circles, a free diagonal/anti-diagonal action, full reciprocal range, and opposite
primitive caps are separately supplied, the metric-dual connection is independent of `Omega` and
has conditional unit Hopf class. Its quotient map is exactly the same degree-one Hopf map used by
the historical `hopf_seed` code after `tan(eta)=exp(2phi)`.

This is a direct vocabulary-to-Hopf `LEAD`: the registered metric instruments exhibit local
twisting candidates, and the separately supplied reciprocal-toric specialization turns its angular
axes into the exact Hopf seed geometry. It is a geometric precursor and conditional compatibility
witness, not native carrier or matter emergence.

## Complete sampled continuation census

The scan used all

```text
4 banks * 48 carrier vectors * 16 structural masks = 3,072
```

analytic identities. Each identity was followed along its preregistered point pair at 17 affine
nodes. Every one of the 31 nonempty subsets of `R,H,D,RG,WG` was classified at every node:

```text
52,224 metric/phi two-jets
1,618,944 family classifications
95,232 family paths
```

Same-motif, matchable-projector paths at all 17 nodes:

| motif | stable paths |
|---|---:|
| full irreducible weave | 70,812 |
| scalar/silent | 11,328 |
| `1+1+2` | 7,845 |
| `1+3` | 2,880 |
| four lines | 1,055 |

The remaining 1,312 paths contain a motif transition or numerical margin. None was dropped. The
complete transition census is `FAMILY_TRANSITION_CENSUS.tsv`.

The endpoints reproduce all 190,464 corresponding rows of the frozen pointwise motif atlas with
zero classification disagreement.

These paths are coherent analytic configurations, not EOM solutions or physical evolution. Their
17 nodes establish sampled matching only. They do not establish a continuous projector bundle,
global continuation, or holonomy. Under the explicit zero-constant cubic polynomial maps defined by
the stored nonlinear jets, all `63,488` possible adjacent-edge cases were accounted for: `63,438`
admitted assignments and had zero transport discordance, while 50 were retained as mutually
unmatched transition edges. Of 67,456 point comparisons, 67,396 were classified on both sides, 33
were uncertain on one side, and 27 were uncertain on both. The node-dependent projector-set
covariance residual was at most `1.1807795359652391e-11`; the map inversion residual was at most
`1.1102230246251565e-16`, and the minimum sampled absolute Jacobian determinant was
`0.9643147372973677`.

## Local distributions

Every midpoint received complete `h=1e-4` and `h/2` four-coordinate stencils in the registered
chart. The largest derivative
convergence residual is `0.0031622520541422948`, below the preregistered `0.005` gate. Only 13
identity/family stencils are retained as degenerate or numerically uncertain; independent replay
reproduces all 13.

The main distribution observations are:

- `1+1+2`: 6,669 primitive Lorentzian planes locally nonintegrable; 1,536 integrable.
- Four lines: 8,370 complementary rank-two split sides locally nonintegrable; zero integrable.
- `1+3`: 2,879 rank-three complements locally integrable and one uncertain. This agrees with the
  hypersurface-orthogonal character expected of the nonzero `phi`-gradient dyad and reinforces that
  the gradient alone is not a generic Hopf carrier.
- Rank-one distributions are locally integrable by dimension, but remain unoriented lines.

Nonzero Frobenius obstruction is a local twist/anholonomy diagnostic. The tensor formula is valid,
but its stored normalization and numerical thresholds use registered-chart component norms; the
full census is therefore certified only in that chart. It is not a Hopf integer. No local family was assigned a
compact domain, periodicity, cap, orientation lift, or global transition cocycle; therefore all
3,072 receive `GLOBAL_DATA_ABSENT`, not `Q=0`.

## Reciprocal-toric control

For the conditional toric metric, the mixed Hessian and dyad eigenvalue pairs in the coordinate
order `(t,phi,xi1,xi2)` are

```text
H: (0, -A'/A^3, (Omega'/Omega-1)/A^2, (Omega'/Omega+1)/A^2)
D: (0,  1/A^2, 0, 0).
```

Thus `H+D` as a joint instrument family distinguishes the two angular axes identically and separates
depth from time. This is generic inside that class, not universal over arbitrary positive `Omega`:
one angular line becomes degenerate with time when `Omega'/Omega=+/-1`.

The generic local ensemble supplies an important contrast. At its 3,072 `H+D` midpoints, 1,536 are
scalar, 1,530 are stably full irreducible, six are uncertain/unstable, and zero have a four-line
motif. The toric axis recovery is therefore a special commuting/cohomogeneity-one stratum, not a
generic consequence of merely turning on `H` and `D`.

With the equal-weight diagonal circle action separately supplied, the metric-dual connection is

```text
calA = f(phi) dxi1 + [1-f(phi)] dxi2,
f(phi)=1/[1+exp(4phi)].
```

`Omega` cancels. For finite endpoints,

```text
Q = f(phi_minus)-f(phi_plus),
```

so the readout is continuous and boundary-dependent, not automatically integral. Only the full
range `phi: -infinity -> +infinity`, two `2*pi` circles, opposite primitive smooth collapses,
selected free diagonal/anti-diagonal action, orientation, and normalization give `|Q|=1`.

At `phi=0` the circle fractions are equal. Reciprocal reflection exchanges the two angular
coefficients; it is a metric isometry only when `A^2` and `Omega^2` are even and the global circle
exchange is supplied. The round control has exact opposite collapse limits `(1,0)` and `(0,1)`.
Arbitrary positive `A,Omega` do not inherit periodicity or cap regularity from the local projectors.

## Comparison with the existing Hopf soliton

The quotient map is

```text
n(phi,delta) = (sech(2phi) cos(delta),
                sech(2phi) sin(delta),
               -tanh(2phi)).
```

It has unit norm and, after `tan(eta)=exp(2phi)` and `delta=xi1-xi2`, is exactly

```text
(sin(2eta) cos(delta), sin(2eta) sin(delta), cos(2eta)),
```

the degree-one Hopf map implemented by `hopf_seed` following inverse stereographic
compactification. This is exact seed-level equivalence.

It is not equality to the relaxed no-null field. The existing soliton explores deformations in an
independently posited internal `Map(S3,S2)` configuration space and is stabilized by the conditional
`L2+L4` functional. The metric audit has not derived those degrees of freedom, that action, its
coefficients, a source, time-live persistence, or mass.

## Emergence ruling

The corrected evidence supports:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS` and
`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

Their proposed correspondence is a `LEAD`, not a derived join.

It does not support `NATIVE_CARRIER_EMERGENCE_DERIVED`.

The remaining join is no longer simply “find an S2.” UDT would have to select or globally sustain:

1. the reciprocal-toric commuting projector stratum rather than the generic full weave;
2. periodic transverse circles and their global integral basis;
3. the diagonal/anti-diagonal free circle action and orientation;
4. opposite regular caps or an equivalent finite-cell completion;
5. a configuration space allowing metric-derived quotient textures to deform; and
6. a native reduced action/variation law whose stationary sector can be compared with the existing
   conditional soliton.

## Adversarial failures and corrections

The first fresh adversarial review returned `FAIL` for the draft package grade. Its complete return
and transcript are preserved. It identified an unexercised covariance gate, circular toric check,
assertion-only catches, ambiguous action provenance, and continuous-bundle wording unsupported by
17 samples. `ADVERSARIAL_REVIEW_CORRECTION_PREREGISTRATION.md` froze the repair contract before the
correction implementation.

The first correction added coordinate-covariance, symbolic metric, direct-seed, provenance, scope,
and mutation checks. A second fresh review returned `FAIL` for that correction's certification while
again accepting the scientific maximum. It exposed a fixed-J edge interpretation, omitted 60
uncertainty-bearing points and 50 skipped edges, and six unguarded result fields. Its full return is
preserved. `SECOND_REVIEW_CORRECTION_PREREGISTRATION.md` froze the next repair before mutation.

The second correction then:

- recomputed 67,456 all-family/node comparisons under the node-dependent cubic maps induced by both
  stored nonlinear jet sets;
- found zero non-uncertain classification discordances;
- found maximum intrinsic-object covariance residual `1.031291787265127e-15` and maximum
  projector-set covariance residual `1.1807795359652391e-11`;
- retained a complete point-status census of 67,396 both-classified, 33 one-sided uncertain, and 27
  both-uncertain cases;
- accounted for all 63,488 possible edges as 63,438 matched with zero discordance plus 50 mutually
  unmatched transition edges;
- derived Christoffels, the phi Hessian/dyad, angular gap, and diagonal connection from the metric;
- executed the frozen repository `hopf_seed` on 1,000 deterministic CPU float64 samples and agreed
  with the metric quotient to `1.3711254354120683e-14`; and
- passed 23 actual corrupted-record mutation catches through its validators.

A third fresh review independently reproduced the scientific ledger, nonlinear-map replay, symbolic
toric algebra, and direct seed compatibility, but returned `FAIL` for fail-closed certification. A
coordinated mutation could redistribute the point-status census and replace the observed
`63,438 + 50` edge split with a fabricated `1 + 63,487` split while preserving the totals. The third
review and its transcript are preserved. `THIRD_REVIEW_CORRECTION_PREREGISTRATION.md` froze the
repair before validator mutation.

The third correction now locks the exact point census, exact edge split, only admissible skip
reason, finite nonnegative residuals, finite positive sampled determinant, and exact frozen seed
path. It exercises 29 corrupted-record catches, including the third review's coordinated attack.
Because the reviewer had already probed the cubic-map outcome, the nonlinear-coordinate evidence
remains explicitly confirmatory rather than outcome-blind; no correction strengthens the scientific
maximum.

A fourth fresh review then reproduced the correction result and catches byte-for-byte, rejected the
coordinated attack and every malformed-number/provenance probe, and independently reproduced the
exact toric/seed witness. It nevertheless returned `FAIL` for immutable package closure: the raw
generated evidence had not yet been committed, and the production builder still rewrote the
ten-source corrected lineage as its older eight-source table. That review is preserved. Under
`FOURTH_REVIEW_CORRECTION_PREREGISTRATION.md`, the raw ledgers/results are now frozen and the builder
emits the exact current ten-row lineage, including the two direct production source manifests. No
scientific result changed.

The supplied equal-weight circle action is now machine-recorded separately from the absent `S2`
matter carrier and absent `L2+L4` action functional. The direct amplitude-family and
invariant-subspace source manifests are explicitly pinned in `SOURCE_LINEAGE.tsv`.

## Independent bounded replay

The frozen independent implementation imports neither the production correspondence builder nor the
production geometry/motif cores. It reconstructs the analytic metric jets directly and uses the
previously frozen nonproduction motif algebra.

- 64 outcome-blind hash-selected identities;
- 33,728 blind all-family path comparisons;
- every 1,312 transition/margin path, 22,304 more comparisons;
- 3,007 blind distribution rows;
- all 13 unstable stencils;
- zero classification mismatches;
- a separate metric-derived toric correction and direct execution of the historical seed; and
- 29/29 exercised correction mutation catches pass. The earlier 11/11 and 13/13 declaration checks
  are retained as regression/provenance only and are not counted as adversarial mutation evidence.

Package grade: `VERIFIED-WITH-CAVEATS` at the explicitly registered scope. The caveats are sampled
rather than continuous paths, registered-chart Frobenius certification, local
configuration-not-dynamics scope, absence of global data for the analytic ensemble, and conditional
inputs of the toric positive control. The overall correspondence remains a `LEAD`.

## Four evidence gates

1. Preregistered: **YES**, including the open-path correction, independent-anchor contract, and the
   successive correction contracts frozen after preserving each fresh review's `FAIL` and before
   repair.
2. Full space or bounded scope: **YES** for all 3,072 registered analytic identities, all 31
   families, all path nodes, and both stencils. Global metrics, dynamics, and arbitrary functions
   remain open.
3. Independently verified: **YES at the stated scope**. Projector covariance, path matching,
   metric-derived toric algebra, direct seed behavior, blind/adverse rows, and actual mutation catches
   were exercised. The full Frobenius census remains registered-chart only.
4. Premises audited: **YES**. The supplied circle action is separated from the absent matter carrier
   and action functional; periodicity, caps, boundary, scale, source, and mass remain explicit.

No startup control, `LIVE.md`, `CANON.md`, research artifact, prior package, or dirty-checkout file
was modified.
