# R3 TreeCorr outer-guard correction

Date: 2026-08-13
Status: `PREREGISTERED_CORRECTION__BEFORE_COVARIANCE_OUTCOME_REVIEW`

## Trigger

The persistent retry validated and reused the first 17 support-corrected cells, then the eighteenth
selection stopped at the frozen exact-count gate:

```text
R2 central mismatch CMASS_North_f1_g17/DD/W0_UNIT:
exact=False abs=1.0 rel=1.199552806713657e-06
```

The difference is exactly one unit-weight pair in analysis bin 118 (29.75 to 30.00 degrees). No R3
covariance value, rank, eigenspectrum, scale, feature, or comparison was opened.

## Exact diagnosis

- Corrfunc central count through 30 degrees: 61,200,334 pairs.
- Unpatched TreeCorr, tree traversal: exact agreement.
- Unpatched TreeCorr, brute traversal: exact agreement.
- Patched TreeCorr, tree traversal: 61,200,333 pairs.
- Patched TreeCorr, brute traversal: 61,200,333 pairs.

An incident-patch replay located deficits of one at patches 423 and 476. Their unique omitted
last-bin pair is catalog rows 85,258 and 30,664, with independently evaluated 80-digit separation

```text
29.999822437658545938293166127257308443174567484882 degrees.
```

Direct unpatched correlation of the two patches includes the pair. TreeCorr's patched path skips the
entire patch relation through its pre-count `_trivially_zero` test. This is patch prefilter geometry,
not bin-edge rounding or pair-count arithmetic.

## Frozen correction

TreeCorr receives 120 linear 0.25-degree bins from 0.25 through 30.25 degrees. Only the original
first 119 bins, ending at 30.00 degrees, enter components, removals, curves, covariances, outputs, or
verification. The added 30.00-to-30.25-degree bin is an operational outer guard that keeps nearby
patch relations alive long enough for exact pair classification; it is always discarded.

On the trigger component, the guarded patched calculation restores exact agreement in all 119
analysis bins and stores the omitted pair in bin 118 of patch relation (423,476). The guard-bin count
is separately observed but never enters the analysis.

No angular analysis edge, bin width, catalog row, random subset, block, weight, estimator,
normalization, rank rule, tolerance, or conclusion ceiling changes. Exact equality remains the gate.

## Restart and provenance

Because the guard can change patch relations even when a cell's central total happened to pass, all
17 earlier cells are provenance only. They remain preserved under
`/tmp/udt_boss_r3_checkpoints_union/` and will not be reused. Corrected production must begin in a
fresh checkpoint directory under the new script hash.

The 30-minute persistent health monitor records worker state and checkpoint progress without
automatic restart. Scientific or numerical failures remain manual stop gates.

## Full trigger-cell production gate

After the correction was committed at `d87068d7`, the unchanged production `execute_selection`
function completed the exact formerly failing `CMASS_North_f1_g17` cell:

- all nine central component comparisons passed;
- all twelve lane/resolution covariance records completed structurally;
- stored central curve shape is `(4,119)` and every covariance shape is `(4,119,119)`;
- wall time was 174.713 seconds and peak RSS was 3.341 GiB;
- no covariance value, rank, eigenspectrum, scale, or feature was printed or reviewed.

The helper and output remain under `/tmp/udt_r3_guarded_g17_smoke_QydtB9/`. Corrected full
production is authorized in fresh `/tmp/udt_boss_r3_checkpoints_guarded/` checkpoints.
