# Domain-boundary implementation correction

Date: 2026-07-23

Status: `RECORDED_BEFORE_CORRECTED_FULL_CENSUS`

The first complete implementation pass was not banked. Inspection found that applying
`nextafter` after clipping a computed root envelope to `[0,1]` could produce the binary64 bounds
immediately below zero or immediately above one. The same ordering appeared when full regional
lambda boxes were passed to the interval evaluator.

This is a computational-domain defect, not a physical or candidate-set change. The correction is
fail-closed:

1. form the algebraic bound;
2. apply directed outward rounding;
3. clamp the final evaluation bound to the registered closed sheet `[0,1]`.

The endpoint universe, charts, refinement ladder, classifications, tolerances, premise ledger, and
maximum conclusion are unchanged. The complete census is rerun from source after this correction.
No classification from the unbanked diagnostic pass is accepted as evidence.
