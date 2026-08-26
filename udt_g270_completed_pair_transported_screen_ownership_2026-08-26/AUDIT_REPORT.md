# G270 audit report — completed-pair transported-screen ownership

Date: 2026-08-26

## Landing

```text
FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH
__COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK
__EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W
__NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

## Result

Completed-pair Dual Reciprocity does not force the G269 transverse mismatch `W` to vanish and does
not determine it from reciprocal depth. It normalizes the intrinsic two-dimensional pullback.

The exact flat tilted family keeps

\[
h_\sigma=
\begin{pmatrix}-1&-1/r\\-1/r&0\end{pmatrix},
\qquad
h_s=
\begin{pmatrix}-1&-1\\-1&0\end{pmatrix}
\]

for every real tilt `w`, while the ambient transported mismatch is `||W||^2=w^2`. At fixed `r=2`,
the planar and unit-tilt realizations have the same intrinsic pullback but give `M_PT=4/5` and
`M_PT=4/9`, respectively.

This variation persists in a smooth regular completed null-ribbon family. Therefore the result is
not a single-event coordinate artifact.

## Exact interpretation

There is no new fitted or independently floating scalar once a full realization is supplied:
`g`, the null branch, and the endpoint clocks evaluate `W` uniquely. What fails is the stronger
claim that the intrinsic completed-pair normalization selects one universal value across different
ambient realizations.

`W` remains distinct from Jacobi screen area and shared-event screen holonomy.

Fresh external review returned `ACCEPT_WITH_REPAIRS` and accepted the bounded scientific landing.
The two evidence repairs now pass internally: formula-level mutations are exercised separately
from typed-ledger checks, and full off-axis ribbon regularity is proved and independently sampled.

The sealed repair-only external follow-up returned `ACCEPT_REPAIRS` with no remaining scoped
defects and confirmed the scientific landing was unchanged.

Current grade: `EXTERNALLY_ACCEPTED_REPAIRS_COMPLETE`.
