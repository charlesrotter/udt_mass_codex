# Preregistration clarification — direction ownership

Date: 2026-08-15

Recorded after the first preregistration commit and before any derivation script or synthetic
witness was written or run.

The original candidate formula correctly constructs a normalized spacelike direction in each
supplied clock/ruler pair plane. It did not separate two ownership statements sharply enough:

1. orthogonalizing and normalizing the supplied ruler channel is metric-derived;
2. declaring that oriented channel to be the observer-to-source direction recorded as RA/DEC is
   part of the ordered measurement query.

The second statement is not derived from a bare metric or pair plane. The ordered query must also
fix the outward sign; otherwise the same unoriented ruler line represents antipodal sky directions.

This clarification narrows the certification ceiling and adds gate `C-ORIENT`. It changes no
source, numerical tolerance, outcome, or data access because no derivation or observational result
has yet been evaluated.
