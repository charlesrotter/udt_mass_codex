# R1 ingestion and random-null execution contract

Date: 2026-08-12
Status: `PREREGISTERED__IMPLEMENTATION_FROZEN__NOT_EXECUTED`
Parent: `PREREGISTRATION.md`

## Bounded question

Can the frozen BOSS DR12 inputs be ingested over the complete registered fine-shell/cap space, and
does the registered Landy--Szalay implementation return numerical nulls when both of its input
populations are disjoint deterministic thinnings of the official random catalog?

This is an R1 numerical-readiness test. It is not allowed to compute or inspect any galaxy angular
pair count. Galaxy files contribute only row/schema/range/weight summaries and observed-redshift
shell populations.

## Frozen implementation

- Python `3.x`, NumPy, and SciPy `1.15.3`.
- FITS binary tables are streamed in row chunks. Only fields allowed by `DATA_MANIFEST.tsv` are
  decoded; the parser is checked against Astropy on small exact anchors.
- Directions are embedded as unit three-vectors. Angular edges are converted exactly by
  `d_chord = 2 sin(theta/2)`.
- Pair bins are counted by `scipy.spatial.cKDTree.count_neighbors(..., cumulative=False)`.
- Auto counts returned as ordered pairs are divided by two after the unregistered sub-0.25-degree
  bin is discarded. Cross counts are used directly.
- Every count is normalized by its exact available pair total before applying Landy--Szalay.
- A separate brute-force implementation checks the load-bearing finite-dimensional pair counts.

The pair-count engine is numerical machinery only. It supplies no distance model, cosmology,
standard ruler, acoustic interpretation, or UDT physics.

## Deterministic random partitions

For each sample/cap/fine shell, let `N_D` be the registered galaxy population, used only as a target
sample size. A SplitMix64 ordering of official-random row indices is fixed by the pinned file hash.
The lowest `12*N_D` hashes are divided without overlap into:

1. replicate 0 pseudo-data: `N_D` rows;
2. replicate 0 pseudo-random: `5*N_D` rows;
3. replicate 1 pseudo-data: `N_D` rows;
4. replicate 1 pseudo-random: `5*N_D` rows.

No random seed, shell, or subset may be changed after a null is seen. R1 tests the `5x` lane only;
the already registered `5x/10x/20x` convergence ensemble remains mandatory for R2 galaxy-pattern
work.

## Registered diagnostic gates

For each angular bin, define the deliberately conservative Poisson-like numerical proxy

```text
sigma_proxy = sqrt(1/max(DD,1) + 4/max(DR,1) + 1/max(RR,1)).
```

It is a contamination diagnostic, not a physical uncertainty or discovery significance.

- all registered fine shells must be reported, including any `UNSAMPLED` shell;
- every sampled bin must have finite normalized counts and positive `RR`;
- within each shell/replicate, `max(abs(w_null/sigma_proxy)) <= 12` and
  `rms(w_null/sigma_proxy) <= 3`;
- between the two disjoint replicates, using the quadrature sum of their proxies,
  `max(abs(delta_w/sigma_delta)) <= 12` and `rms(delta_w/sigma_delta) <= 3`;
- any breach blocks R2 and returns `RANDOM_OR_ESTIMATOR_CONTAMINATION_TO_AUDIT`; it may not be
  repaired by moving bins, replacing a shell, or changing the partition.

These thresholds are numerical stop guards, not calibrated p-values.

## Frozen outputs

- `R1_FILE_INGESTION_SUMMARY.tsv`
- `R1_INGESTION_ATLAS.tsv`
- `R1_RANDOM_NULL_ATLAS.tsv`
- `R1_RANDOM_NULL_SUMMARY.tsv`
- `R1_ENGINE_ANCHOR_INPUTS.npz`
- `R1_ENGINE_ANCHOR.tsv`
- `R1_RESOURCE_OBSERVED.tsv`
- `R1_RESULT.json`
- `R1_RUN.log`

An interrupted log is evidence of an incomplete run, not a scientific output. A final numeric output
is never overwritten.

## Resource envelope

- Device: CPU only; no GPU process.
- Available host at freeze: 8 logical CPUs, 125 GiB RAM, 116 GiB available.
- Processes: one Python process; SciPy pair counting remains single-process.
- Dtype: catalog coordinates and calculations `float64`; raw counts `int64`.
- Largest selected-column random footprint: below 1.1 GiB before tree work.
- Registered RSS stop: 12 GiB.
- Synthetic scale anchor (`N_D=25,000`, `N_R=125,000`, 119 bins): 29.98 s on this host.
- Estimated complete R1 null wall time: 2--6 hours; this is an operational estimate, not a
  scientific timeout. A sound run may continue beyond it while RSS and progress remain healthy.
- Progress checkpoint: `R1_RUN.log` is flushed after every fine shell. Numeric outputs are written
  atomically only after the complete run; an interrupted run is not resumable and must be restarted
  from the beginning without treating its log as a result.
- Stop conditions: nonfinite allowed field, row/schema mismatch, insufficient random rows for the
  frozen partitions, pair-count disagreement with brute force, nonpositive `RR`, RSS over 12 GiB,
  or explicit user interruption.

## Certification ceiling

Maximum allowed return:

> `OBSERVED`: the frozen catalogs have the recorded shell populations and the registered estimator
> passes (or fails) its deterministic random-only numerical controls over the complete fine-shell
> BOSS LOWZ/CMASS North/South R1 scope.

R1 cannot report a galaxy pattern, feature, fit, physical scale, origin, `X_max`, or UDT agreement.
