# G241 banking integration note

G241 was preregistered and externally reviewed against the exact 223-row premise registry recorded
in `SOURCE_MANIFEST.tsv`. Banking the accepted result appends G241 as row 224; it must not rewrite
that historical manifest.

R5 therefore changes only repository-root replay logic. `verify_package.py` requires exactly one
live `G241` row, removes it in memory, and requires the reconstructed registry bytes to match the
sealed preregistration hash. Every other manifested source remains a direct byte-hash check. Any
other registry mutation fails lineage verification.

This integration changes no formula, coefficient, covariance, candidate, threshold,
classification, outcome boundary, or scientific landing.
