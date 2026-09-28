# Bounded validation identity repair

Status: DRAFT, frozen after initial fits and after the finite identity diagnostic,
before this repaired validation is evaluated. Original FREEZE, fits and original
validation outputs remain preserved. No candidate formula/coefficient estimator,
primary sample, covariance, redshift correction, optical premise, calibration,
or tolerance changes. This is a post-exposure consistency check.

The original grouping used equal CID. A post-fit finite source-schema diagnostic
found ten pairs with different CID within 5 arcsec, peak-date difference below
10 days and redshift difference below .001. Five pairs lie in the primary sample:
2012bh/370356, 2016fbk/AT2016fbk, 7876/2005ir, 17186/2007hx,
580104/1261579. These are conservative possible aliases, not a complete identity
census. They reveal that equal CID alone does not justify saying every physical
source is confined to a partition. Full covariance cross blocks were included
in the original validation, so no original score is erased or recast as blind.

Smallest repair: union all equal-CID rows with all ten diagnostic pairs (including
those outside primary), then use the lexicographically smallest CID of each
connected component as hash key. Reapply the same SHA256(key) mod5 split. This
can group unrelated sources conservatively; it does not weaken same-source
grouping. Preserve group assignments, changed rows and component members. Refit
development parameters for all six already-frozen families and recompute the
same conditional predictive Gaussian score with covariance cross blocks and
parameter uncertainty. Save in alias_validation/ and leave results/validation.json
untouched. No all-data refit is needed, because the full-data estimator is
unaffected by partition changes. Compare repaired and original scores without
selecting the more favorable split. Use repaired scores in the final summary.

No DESI, DES or other target is used to tune this repair. Budget: one CPU fit
process, <=2 threads, <=3 GiB, <=600s, then direct dense-solve anchor for F2's
repaired score. Stop on rank, covariance or alias index mismatch. Parent will
include this history in later separate-context review.
