# R5 covariance-range ownership repair — preregistration before rerun

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_EXTERNAL_COVARIANCE_CAVEAT__BEFORE_RERUN`

The external semantic review returned `COVARIANCE_CAVEAT_INSUFFICIENT`. The production values were
not numerically challenged. The saved schema failed to preserve the ownership classification that
the independent verifier computed.

## Frozen repair

Change no parent, transform, relation, view, rank, covariance value, eigenthreshold, gap floor,
conclusion, or census. For every covariance-subspace row, additionally save:

```text
covariance_range_relative_gap_to_threshold
covariance_range_owned
global_subspace_owned
range_overlap_owned
```

The covariance-range gap is the verifier's already frozen value:

```text
min(lambda_min_positive - tau, tau - lambda_max_nonpositive) / max(lambda_max, eps)
```

with value `1` for zero- or full-rank range projectors. Ownership uses the already preregistered
`sqrt(eps_float64)` floor. `range_overlap_owned` is true only when both the global top-`k` projector
and covariance-range projector are owned.

Every summary row also receives `ownership_status`:

- direct trace/projection quantities: `OWNED` only where the global top-`k` projector is owned;
- range overlap: `OWNED` only where `range_overlap_owned` is true;
- otherwise: `UNRESOLVED_NUMERICAL`;
- transformed-rank summaries: `NUMERICAL_BOOKKEEPING`.

Owned and unresolved values may not be mixed within one summary row. The current frozen data are
expected to retain 2,850 summary rows because each transform/grid/rank cell has one uniform range
ownership status; this is a census expectation, not a scientific target.

## Rerun and verification gate

Preserve the superseded corrected outputs before rerun. Regenerate the complete production atlas
from unchanged parents. The independent SciPy replay must reconstruct every new gap and ownership
field, rebuild ownership-separated summaries, reproduce the exact resolved/unresolved totals, and
pass the existing hostile-mutation suite. No numerical result may be interpreted until this rerun
passes.
