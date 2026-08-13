# R3 data-only spatial covariance atlas — preregistration

Date: 2026-08-13
Status: `PREREGISTERED__NO_SPATIAL_COVARIANCE_EVALUATED`
Parents: root `PREREGISTRATION.md`; `R2_OUTCOME_REPORT.md`

## Whole question

What covariance, numerical-rank, and block-resolution dependence do the complete R2 observer-
coordinate angular curves exhibit under exact leave-one-spatial-block resampling generated only
from the official survey random catalogs?

This is a data-only uncertainty map. It does not search for, rank, fit, or assign significance to an
angular feature. It does not import a cosmological mock, distance conversion, ruler, acoustic model,
UDT response, CMB result, SNe profile, or `X_max`.

## Outcome-blindness caveat

The root preregistration said the spatial geometry would be generated before galaxy-pattern outputs
were opened. That timing was missed: R2 was completed before exact block IDs and NSIDE values were
frozen. R3 therefore cannot claim perfect pre-R2 blindness.

The repair is bounded rather than rhetorical:

- block geometry is generated from official random catalogs only;
- the fixed resolutions below are justified by nested HEALPix geometry and the 119-bin rank bound,
  not by any R2 extremum, lag, DCT coefficient, shell, or curve;
- no individual R2 feature enters the code, acceptance gates, or output vocabulary;
- this timing deviation remains a permanent evidence caveat.

## Exact bounded universe

R3 retains:

- all 194 R2 sample/cap/redshift selections;
- all four R2 weight lanes `W0` through `W3`;
- the preregistered high-density `20x` random readout;
- all 119 angular bins from 0.25 through 30 degrees;
- North and South separately;
- exact factor-1, factor-2, and factor-4 object-selection unions.

The `5x` and `10x` central curves remain banked R2 numerical controls. R3 does not multiply the
spatial covariance by those lower-density random replicas because `20x` was declared the high-
density readout before R2 and all 776 R2 comparisons moved monotonically toward it.

## Frozen spatial geometry

For each sample/cap independently:

1. use all rows of its official random catalog across that sample's registered redshift envelope;
2. map sky positions to nested HEALPix pixels at `NSIDE=16`;
3. retain every occupied pixel, ordered by integer nested pixel ID;
4. obtain `NSIDE=8` and `NSIDE=4` blocks by exact nested-parent mapping of those same pixels;
5. for an individual redshift selection, call a block active only when its selected deterministic
   `20x` random catalog contains at least one row;
6. require every selected galaxy to lie in an active random block.

The blocks are not declared equal-area survey regions: edge pixels can have partial footprint
coverage. Full-random and selected-random occupancy, data occupancy, coefficient of variation,
minimum, median, and maximum are retained. Occupancy imbalance is a limitation to characterize, not
a reason to merge or discard blocks after seeing covariance.

## Exact resampling estimator

TreeCorr `5.1.3` supplies pair counts split by the finest `NSIDE=16` patch labels. Coarser deletions
are exact sums over nested parents. For each active block `b`, every pair with either endpoint in
`b` is removed. Pairs internal to `b` are removed once. This is the literal delete-one-subcatalog
(`simple` cross-patch) rule; no `match`, bootstrap, mock, or fitted covariance correction enters.

Weighted Landy--Szalay normalization is recomputed for every retained subcatalog:

```text
DD_total(-b) = ((sum w_D(-b))^2 - sum(w_D(-b)^2))/2
DR_total(-b) = sum w_D(-b) * N_R(-b)
RR_total(-b) = N_R(-b)(N_R(-b)-1)/2
```

and every leave-one curve retains the complete 119-bin vector.

For `K` active blocks at a resolution, the registered jackknife covariance is

```text
mean = (1/K) sum_b w_(-b)
C = ((K-1)/K) sum_b (w_(-b)-mean)(w_(-b)-mean)^T.
```

This is a standard equal-block delete-one formula applied transparently to unequal-coverage
HEALPix blocks. R3 reports the resulting resolution and occupancy dependence and does not claim it
is an exact sampling distribution.

## Numerical rank rule

Every covariance is symmetrized before eigendecomposition. With `n=119`, float64 epsilon `eps`, and
largest eigenvalue `lambda_max`, the frozen numerical threshold is

```text
tau = n * eps * lambda_max.
```

Numerical rank is the number of eigenvalues strictly above `tau`. Eigenvalues below `-100*tau`
constitute a covariance-construction failure. No inverse, pseudoinverse, chi-square, sigma,
likelihood, feature significance, or Hartlap-like correction is computed in R3. Rank is descriptive.

## Complete output surface

- `R3_BLOCK_ATLAS.tsv` and `R3_BLOCK_RESULT.json` — random-only fixed geometry;
- `R3_COVARIANCE_CELLS/*.npz` — one immutable cell per R2 selection, containing all four central
  TreeCorr curves, all three resolution/four-lane covariance matrices, means, eigenspectra, ranks,
  occupancy data, and full leave-one curves only for frozen anchor cells;
- `R3_COVARIANCE_SUMMARY.tsv` — complete selection/lane/resolution rank and scale ledger;
- `R3_CENTRAL_ENGINE_COMPARISON.tsv` — every TreeCorr central component versus R2 Corrfunc;
- `R3_RESOURCE_OBSERVED.tsv`, `R3_RESULT.json`, `R3_RUN.log`, and SHA-256 manifests;
- `R3_VERIFICATION_RESULT.json` — post-run independent verification only.

Temporary patch-pair checkpoints are operational artifacts and are not physical outputs.

## Frozen independent anchors

The first factor-1 shell in each of `CMASS/LOWZ` x `North/South` is an anchor. For `W3`, the
lowest-integer active block at `NSIDE=4` and `NSIDE=16` is replayed by independently deleting the
objects and rerunning Corrfunc. This gives eight leave-one anchors selected by catalog order and
random geometry, not by covariance outcome.

The verifier also:

- reconstructs every covariance, mean, eigenspectrum, and rank from the saved data owned by each
  cell where available and checks all stored matrix identities;
- checks all 1,746 R3 central component families against banked R2 components;
- uses compact direct all-pairs anchors to test block assignment and deletion algebra;
- reruns the eight full leave-one Corrfunc anchors.

## Resource and restart contract

- one CPU process, at most eight pair-count threads, no GPU;
- one selection in memory at a time;
- checkpoint after every complete selection;
- validated checkpoints are reusable; final evidence files are never overwritten;
- RSS stop at 16 GiB;
- elapsed time is operational only and never a scientific stop;
- stop on input/hash mismatch, unowned data pixel, nonfinite value, nonpositive normalization,
  nonpositive leave-one RR bin, patch-sum mismatch, R2 central mismatch, covariance PSD failure, or
  checkpoint metadata mismatch.

## Certification/falsification contract

1. exactly 194 cells, 4 lanes, 3 block resolutions, and 119 bins must complete;
2. every central TreeCorr integer component must match R2 Corrfunc exactly;
3. weighted central components must agree with R2 to relative `5e-9` or absolute `1e-7`;
4. summed finest-patch components must reproduce each TreeCorr total;
5. every deletion must have positive normalizations and positive RR in all bins;
6. every covariance must be finite, symmetric, and PSD within the frozen threshold;
7. reported rank may not exceed `min(119,K-1)`;
8. all resolutions and weight lanes remain visible regardless of rank or appearance;
9. independent anchors and the repository test suite must pass before banking;
10. resolution dependence or rank loss returns `COVARIANCE_RESOLUTION_OR_RANK_LIMITED`, not a tuned
    block choice.

## Explicit exclusions and maximum conclusion

R3 excludes smoothing, fitting, bin removal, covariance tapering, shrinkage, regularization,
eigenmode selection by merit, mock corrections, feature templates, and physical interpretation.

Maximum conclusion:

> `OBSERVED`: within the frozen BOSS observer-coordinate atlas, the complete central curves have the
> recorded data-only delete-one-block covariance, rank, occupancy, weight, cap, shell-resolution,
> and block-resolution dependence.

R3 cannot establish a physical origin, ruler, cosmology, UDT agreement, CMB relation, or `X_max`.
