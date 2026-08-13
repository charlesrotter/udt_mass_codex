# R3 active-block support typing correction

Date: 2026-08-13
Status: `PREREGISTERED_CORRECTION__BEFORE_COVARIANCE_OUTCOME_REVIEW`

## Trigger

The first production attempt used the frozen random-only definition of an active block. It
checkpointed `CMASS_North_f1_g00` and `CMASS_North_f1_g01`, then stopped at the preregistered support
gate for `CMASS_North_f1_g02` at NSIDE 16:

```text
ValueError: data without selected-random block support CMASS_North_f1_g02/nside16
```

No covariance value, rank, eigenspectrum, scale, feature, or comparison was opened. The two old
checkpoints remain preserved in `/tmp/udt_boss_r3_checkpoints` and will not be reused because the
production script hash changes under this correction.

## Geometry-only census

A separate census read only catalog coordinates, redshift selections, the registered deterministic
20x random indices, and the frozen block atlas. It read no pair count, R2 curve/descriptor, or R3
covariance.

Across all 194 selections and three resolutions (582 records):

| NSIDE | affected selections | data-only blocks | galaxies in those blocks | maximum per selection |
|---:|---:|---:|---:|---:|
| 4 | 2 | 2 | 2 | 1 block / 1 galaxy |
| 8 | 2 | 2 | 2 | 1 block / 1 galaxy |
| 16 | 13 | 13 | 13 | 1 block / 1 galaxy |

The triggering selection has 619 selected-random-occupied NSIDE-16 blocks and one additional block
containing one galaxy but no selected random row.

## Category correction

The full official random catalog owns the frozen survey footprint. The deterministic 20x random
subset is a finite estimator catalog within that footprint; it does not own whether a spatial
subcatalog exists.

For each selection and resolution, the corrected active set is therefore

```text
active block <=> selected-data occupancy > 0 OR selected-random occupancy > 0.
```

For a data-only block, literal deletion is well-defined:

- DD removes all data-data pairs incident to its galaxies;
- DR removes all data-random pairs incident to its galaxies;
- RR removes zero pairs;
- retained random count and RR normalization are unchanged.

This changes no footprint pixels, NSIDE, object selection, random subset, weight, estimator, rank
rule, tolerance, anchor policy, or conclusion ceiling. It prevents a finite random draw from silently
dropping a valid spatial deletion.

## Falsification and restart

The corrected engine must pass a synthetic data-only-block exact deletion replay. Every production
cell must store the exact active union, including zero random occupancies where present. The
independent verifier must reconstruct that union for all 194 cells.

Production restarts in a fresh checkpoint directory. Any prior checkpoint remains provenance only.
