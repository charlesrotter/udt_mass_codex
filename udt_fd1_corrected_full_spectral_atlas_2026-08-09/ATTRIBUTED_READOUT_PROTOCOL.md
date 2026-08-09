# Full corrected atlas — attributed readout protocol

Date: 2026-08-09  
Frozen Phase-I commit: `2ef02737`  
Certified atlas SHA-256: `042138fb73cc9f3bef4faf97fc0357f2a2f079daced5e39d6532c4a6f770dfbb`

This is an attributed regrade using the already registered Planck 2018 Results I Table 5 TT
peak/trough locations.  It is not a blind prediction and the data are not newly discovered.

## Fixed readouts

For all 420 nonzero-mixing atlas rows:

1. Fit the same inherited two-parameter affine map `ell=a omega+b` separately to the first seven
   positive roots of each `m=-1,0,+1` ladder.  Also retain the one-scale/no-offset mismatch.  Report
   the complete surfaces; the historical 3.1% line is a comparison marker, not a merit filter.
2. For Neumann `m=0`, carry both `POSITIVE_ONLY` and `ZERO_INCLUDED` conventions.  The latter uses
   the exact zero plus the first six positive roots.  Do not select whichever looks better.
3. Reproduce the old same-positive-index `m=0`-centered basin/trough calculation for provenance,
   including both Neumann conventions.  Label it `HISTORICAL_PAIRING_DIAGNOSTIC`; it is not a
   metric-derived observational multiplet law.
4. Under each standalone ladder's affine map, project all 24 positive lines and count how many lie
   in each published trough basin.  This characterizes geometric line crowding only.  Without a
   native population/source law, extra or absent lines are not an exclusion.
5. Do not permute roots, choose subsequences, discard an m channel, assign weights, or refit a
   profile.  No FD2 perturbation is run.

## Gates

- 420 spectral identities and 630 convention rows exactly;
- positive affine orientation and finite readouts;
- all three standalone families retained;
- exact reproduction of the earlier six central-witness readouts to relative `2e-9`;
- a separate implementation recomputes all load-bearing counts and extrema;
- mutations of the atlas hash, row census, convention count, family inclusion, pairing caveat, and
  source attribution must fail.

## Maximum conclusion

An attributed compatibility/crowding map in the declared scalar slice.  No standalone shape match,
historical basin containment, or crowding count derives which modes are populated, a CMB source,
peak heights, polarization, a native boundary, or a physical multiplet.  Stop before FD2.
