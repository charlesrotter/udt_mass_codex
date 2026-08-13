# Raw observer-coordinate angular-pattern restart — preregistration

Date: 2026-08-12  
Status: `PREREGISTERED__NO_PATTERN_EVALUATED`  
Lane: observational data preparation and pattern characterization only

## Whole question

Do the final BOSS DR12 galaxy catalogs contain angular correlation structure that is reproducible
across observed-redshift shells, Galactic caps, observational-weight treatments, random-catalog
density, and angular resolution when the calculation uses only observed sky direction and observed
redshift?

This is metric-led only in the limited sense that it prepares an observer-coordinate pattern for a
later UDT comparison. It does **not** fit UDT, infer a ruler, assign an acoustic origin, convert the
catalog to comoving distance, estimate `X_max`, or select a physical UDT history.

## Exact bounded data universe

- Final BOSS DR12 `LOWZ` and `CMASS` pre-reconstruction clustering catalogs.
- North and South Galactic caps remain separately visible.
- `LOWZ`: `0.15 <= Z < 0.43`.
- `CMASS`: `0.43 <= Z <= 0.70`.
- Fine observed-redshift grid: fixed origin `Z=0.15`, width `0.01`.
- Coarser views are exact adjacent-bin **object-selection unions** at widths `0.02` and `0.04`, with
  their pair counts recomputed so cross-fine-bin pairs are retained; shell centers are never shifted
  to improve a pattern.
- Angular separation grid: fixed linear edges from `0.25` to `30.00` degrees in `0.25`-degree
  increments.
- Only `RA`, `DEC`, and `Z` define an object's observer-coordinate location.

The exact eight input files, byte counts, row counts, and SHA-256 values are frozen in
`DATA_MANIFEST.tsv`.

## Weight ensemble

All four lanes are computed and retained:

1. `W0_UNIT`: unit data weights.
2. `W1_SPECTRO`: `WEIGHT_CP + WEIGHT_NOZ - 1`.
3. `W2_IMAGING`: `WEIGHT_SYSTOT`.
4. `W3_OFFICIAL_OBS`: `WEIGHT_SYSTOT * (WEIGHT_CP + WEIGHT_NOZ - 1)`.

No lane may be selected or discarded after seeing the pattern. `WEIGHT_FKP` and `NZ` are excluded:
they belong to a three-dimensional/FKP optimization and are not required for an angular
observer-coordinate measurement. Random-catalog weights are unity; their angular density already
encodes the survey footprint/completeness supplied by the collaboration.

## Estimator map

The first implementation will use the Landy-Szalay angular estimator

```text
w(theta) = (DD - 2 DR + RR) / RR
```

with every pair count normalized by its available weighted pair total. This is a borrowed numerical
estimator, not imported cosmological physics.

The official random catalog is deterministically hash-thinned within each sample/cap/shell to
nominal random-to-data ratios `5`, `10`, and `20`. The `20x` curve is the registered high-density
readout; the lower-density curves are numerical convergence controls. No seed may be retuned.

North and South are first evaluated separately. Their combined curve, if reported, is the exact
Landy-Szalay estimator on the union, reconstructed from the cap-wise raw pair counts and the union's
weighted pair-normalization totals; it is not an average chosen to favor the quieter cap.

## Uncertainty posture

No cosmology-generated mock covariance enters the primary result. Spatial resampling regions will be
constructed from the random catalog alone, before opening galaxy-pattern outputs. Multiple fixed
HEALPix block resolutions will be retained rather than choosing the one that maximizes significance.

The first outcome may characterize the measured central curves and their empirical stability. It may
not quote a discovery significance unless:

- the full-resolution covariance is nonsingular on the declared comparison subspace;
- block-resolution dependence is recorded;
- North/South and random-density controls are retained;
- the load-bearing covariance is independently reproduced.

## Explicit exclusions

- no published `D_M`, `D_H`, `D_V`, `r_d`, acoustic scale, standard ruler, or yardstick;
- no conversion of angle/redshift into comoving distance or wave number;
- no post-reconstruction catalog;
- no FKP weighting;
- no Lambda-CDM, GR field equation, fluid, early-universe, or acoustic interpretation;
- no mock-derived correction or covariance in the primary lane;
- no digitized plot as primary evidence;
- no old repository BAO result as an input, bin selector, covariance, or expected feature location;
- no UDT parameter fit or `X_max` estimate in this phase.

## Outcome blindness

The computation must not be supplied with an expected peak angle, oscillation period, published
angular-BAO location, SNe scale, `X_max`, or UDT response curve. Pattern descriptors, if later used,
must be defined before the first measured curve is inspected.

## Certification ceiling

Maximum allowed conclusion:

> `OBSERVED`: within the frozen BOSS DR12 observer-coordinate atlas, the measured angular correlation
> pattern has the recorded dependence on redshift resolution, cap, observational weights, random
> density, and spatial resampling.

Even a strong reproducible pattern would not derive its origin, identify it with UDT, establish a
physical ruler, select a UDT history, or determine `X_max`.

## Execution gate

No pair-count output or pattern plot may be produced until:

1. `verify_preregistration.py` passes;
2. the input hashes have been independently checked;
3. the pair-count implementation and output names are frozen;
4. the numerical memory/runtime estimate is recorded;
5. Charles authorizes the registered execution.
