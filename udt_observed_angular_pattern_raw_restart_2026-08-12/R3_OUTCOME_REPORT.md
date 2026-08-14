# R3 data-only spatial covariance atlas — outcome

Date: 2026-08-14
Grade: `OBSERVED_VERIFIED_WITH_CAVEATS__COVARIANCE_RESOLUTION_OR_RANK_LIMITED`

## What completed

The complete preregistered bounded R3 universe completed:

- 194 sample/cap/redshift selections;
- four observational-weight lanes;
- nested HEALPix deletion grids at `NSIDE=4,8,16`;
- 119 observer-coordinate angular bins;
- 2,328 delete-one-spatial-block covariance matrices;
- 1,746 central TreeCorr-versus-R2 component comparisons;
- eight independently rerun full deletion anchors.

Production used TreeCorr `5.1.3`, healpy `1.19.0`, NumPy `2.2.6`, at most eight CPU threads, and no
GPU.  Maximum recorded RSS was about 6.93 GiB.  The assembly-time `R3_RESULT.json` retains its
literal `VERIFICATION_PENDING` status; `R3_VERIFICATION_RESULT.json` and `R3_FINAL_STATUS.json` are
the later closure records.

## Bounded observation

The covariance rank depends strongly and transparently on deletion resolution:

| Deletion grid | Active blocks per selection | Full-rank matrices | Rank range |
|---|---:|---:|---:|
| `NSIDE=4` | 24--51 | 0 / 776 | 23--50 |
| `NSIDE=8` | 73--169 | 388 / 776 | 72--119 |
| `NSIDE=16` | 254--623 | 776 / 776 | 119 |

At `NSIDE=8`, every North matrix is full rank and every South matrix is rank-limited by the smaller
number of active blocks.  At `NSIDE=4`, all matrices are rank-limited.  At `NSIDE=16`, every matrix
is full rank under the frozen numerical threshold.

Covariance scale also changes with deletion resolution.  Across matched selection/lane records, the
median-diagonal ratio has these ranges:

- `NSIDE=8 / NSIDE=4`: 0.612--1.319, median 0.942;
- `NSIDE=16 / NSIDE=8`: 0.646--1.021, median 0.862;
- `NSIDE=16 / NSIDE=4`: 0.464--1.086, median 0.816.

Therefore the preregistered return is
`COVARIANCE_RESOLUTION_OR_RANK_LIMITED`.  R3 records all three grids; it does not choose a preferred
one, invert a covariance, compute a significance, or filter an angular feature.

## Independent verification

`verify_r3.py` passed after two disclosed post-failure ownership corrections:

1. The original verifier added a tighter tolerance to a curve formed from DD/DR/RR components that
   had already passed the registered cross-engine component tolerance.  The corrected verifier
   keeps the frozen component gate and requires each saved central curve to reconstruct bit for bit
   from its own saved components.
2. The leave-one anchor is now typed in two stages: Corrfunc versus TreeCorr deleted components, then
   direct TreeCorr versus the saved patch-decomposition curve.  This separately checks the
   independent engine and literal deletion construction.

The corrections changed no catalog, pair count, curve, covariance, rank rule, block, physical
premise, or preregistered component tolerance.  The verifier reports the removed redundant-curve
residuals for provenance.  All 776 central curves reconstruct exactly; all 194 support unions were
independently rebuilt; all covariance, PSD, rank, and manifest identities pass; and all eight
deletion anchors pass.  Repository gates return `84 passed, 1 xfailed`.

The ignored 194-cell NPZ corpus, run log, and every other manifest-owned output are preserved at
`/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/`.  A fresh archive replay matches all 201
rows of `R3_OUTPUT_MANIFEST.tsv` by byte count and SHA-256.

## Four banking gates

1. **Preregistered:** yes.  The statistical universe, estimator, grids, ranks, anchors, exclusions,
   and conclusion ceiling were frozen before covariance outcomes.  The permanent caveat remains
   that R3 block geometry was frozen after R2 rather than before it.
2. **Full or bounded scope:** full within the declared 194-selection, four-lane, three-resolution,
   119-bin, 20x-random universe.
3. **Independently verified:** yes, with exact saved-field replay, independent support
   reconstruction, Corrfunc/TreeCorr deletion anchors, and repository tests.
4. **Premises audited:** yes.  Both post-failure verifier ownership repairs are explicit and prevent
   promotion beyond `VERIFIED-WITH-CAVEATS`.

## Maximum conclusion

`OBSERVED`: within the frozen BOSS DR12 observer-coordinate atlas, the complete central curves have
the recorded data-only delete-one-block covariance, numerical-rank, occupancy, cap, shell,
observational-weight, and block-resolution dependence.

R3 does not establish a preferred feature, oscillation, significance, physical scale, acoustic or
other origin, UDT response, CMB relation, cosmology, or `X_max`.  A later empirical-structure phase
must be separately preregistered and must retain all caps, lanes, shell resolutions, and covariance
grids rather than selecting whichever view looks most favorable.
