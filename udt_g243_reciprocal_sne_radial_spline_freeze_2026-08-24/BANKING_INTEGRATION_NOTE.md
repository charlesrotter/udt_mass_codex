# G243 banking integration note

G243 was preregistered and externally reviewed against the exact 224-row premise registry recorded
in `SOURCE_MANIFEST.tsv`. Banking the accepted result appends G243 as row 225; it must not rewrite
that historical manifest.

The production replay, package verifier, and review-intake builder remove at most one live `G243`
row in memory and require the reconstructed registry bytes to match the preregistration hash. A
later sealed replay can therefore distinguish the authorized G243 row from any other registry
mutation.

This integration changes no spline basis, alpha value, covariance, transfer assumption, numerical
tolerance, candidate, turning interval, classification, or scientific landing.
