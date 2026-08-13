# R2 complete central-pattern atlas — outcome report

Date: 2026-08-13
Grade: `VERIFIED-WITH-CAVEATS`
Parent preregistration commit: `ff7088a4`
Verifier correction commit: `ca33cdfa`
Control-summary preregistration commit: `42b62804`

## Maximum justified result

The complete bounded R2 angular central-pattern atlas is assembled and independently verified:

- 194 exact sample/cap/redshift selections;
- four retained observational-weight lanes;
- deterministic nested `5x`, `10x`, and `20x` random catalogs;
- 2,328 complete curves across 119 angular bins;
- 3,686 raw `DD`, `DR`, and `RR` component families;
- all preregistered raw curves, extrema/crossings, DCT coefficients, lags, and consistency summaries.

This is a verified descriptive catalog result. It is not a detection of an oscillation, preferred
angle, BAO feature, UDT response, physical scale, CMB relation, or `X_max`.

## Execution and verification

The production run began at 2026-08-12 22:31:38 EDT and completed all pair components at
2026-08-13 06:21:22 EDT. Peak recorded RSS was 1.634 GiB. Assembly required 6.52 seconds after the
checkpointed pair census.

The corrected independent verifier passed:

```text
PASS: R2 independent verification
(3686 components, 2328 curves, 9 TreeCorr anchors, 12 direct anchors)
```

It independently reconstructed every curve and descriptor row from the raw component atlas. All
nine full-catalog TreeCorr component anchors had exact integer pair counts. All twelve compact
direct-versus-primary anchors had exact integer counts; their maximum weighted relative difference
was `5.758092004939054e-13`, inside the frozen `5e-12` tolerance.

Repository regression result:

```text
103 passed, 1 xfailed
```

The xfail is the pre-existing documented matter-sector habit-pin test and is unrelated to R2.

## Verifier correction caveat

The first verifier execution reached the compact anchor and failed because the implementation
compared direct weighted sums to TreeCorr under the primary/direct `5e-12` tolerance. Integer bins
were exact, but TreeCorr's CMASS weighted accumulator differed at approximately `5.4e-10` through
`5.8e-9` relative.

A three-way check established before repair that direct all-pairs and the primary Corrfunc engine
agreed within `5.8e-13` relative. `R2_VERIFIER_CORRECTION_PREREGISTRATION.md` froze the repair before
rerun: only the compact comparator was redirected to the primary engine; no tolerance, production
result, selection, or other verifier gate changed. The full-catalog TreeCorr anchors remained in
place and passed. This post-failure implementation repair is why the result remains explicitly
`VERIFIED-WITH-CAVEATS`.

## Complete control observations

The post-verification summary vocabulary was frozen in
`R2_CONTROL_SUMMARY_PREREGISTRATION.md`. Its load-bearing headline values were independently
recomputed in `R2_CONTROL_SUMMARY_VERIFICATION.json`.

### Random density

For every one of 776 matched sample/cap/factor/group/weight queries, the `10x` curve was no farther
from the `20x` curve in RMS than the `5x` curve was. This is strong numerical convergence evidence
for the nested random control; it is not physical covariance.

Across all 1,552 random-density comparisons, RMS difference had:

- median `0.0018130`;
- 95th percentile `0.0062667`;
- maximum `0.0116576`.

### Weight dependence

Across all 1,746 retained weight-versus-unit comparisons, RMS difference had:

- median `0.0016853`;
- 95th percentile `0.0056897`;
- maximum `0.0111674`.

No weight lane was selected or discarded.

### North/South dependence

Across all 1,164 exactly matched North/South comparisons, RMS difference had:

- median `0.0139412`;
- 95th percentile `0.0365798`;
- maximum `0.0560326`.

This observed cap dependence is substantially larger than the random-density and weight-lane
differences. It cannot yet be called physical anisotropy, replication, disagreement, or significance
because the caps contain distinct structure and R2 has no data-only covariance.

### Exact shell unions

Median RMS control differences decreased monotonically as adjacent fine shells were combined:

| Control | factor 1 | factor 2 | factor 4 |
|---|---:|---:|---:|
| random density | 0.002703 | 0.001398 | 0.000734 |
| weight lane | 0.002256 | 0.001507 | 0.000841 |
| North/South | 0.019786 | 0.011451 | 0.006412 |

Curve RMS, total variation, and difference RMS also decreased under broader exact unions. This is
descriptive smoothing from more objects and broader redshift aggregation; it does not select a
physical scale.

## Four evidence gates

1. **Preregistered:** yes — complete R2 design banked at `ff7088a4`; post-verification summary design
   banked at `42b62804`. The verifier implementation repair is separately disclosed and banked at
   `ca33cdfa` after its first gate failure and before rerun.
2. **Full space or bounded scope justified:** yes — all 194 registered selections, four weight lanes,
   three random ratios, and 119 bins completed. The scope remains only the eight frozen BOSS DR12
   input catalogs and the registered observer-coordinate estimator.
3. **Independently verified:** yes — every saved curve/descriptor recomputed; TreeCorr full-catalog
   anchors and direct-primary compact anchors passed; control-summary headlines independently
   replayed.
4. **Premises audited:** yes for the bounded descriptive claim — input identity, observed-coordinate
   shells, weights, random construction, estimator, engine ownership, and output scope are explicit.
   No physical distance law, source model, covariance, UDT comparison, or cosmology is present.

## Open gate and next action

The open gate is R3: a preregistered, data-only covariance and replication analysis that asks which
curve structure survives spatial resampling, disjoint sky regions, shell aggregation, weight lanes,
and random density. R3 must be defined without choosing an observed R2 extremum, DCT coefficient,
lag, period, or desired pattern.

Only after R3 identifies control-supported empirical structure may a later, separately preregistered
stage compare that structure with a complete UDT observer-pair relation.
