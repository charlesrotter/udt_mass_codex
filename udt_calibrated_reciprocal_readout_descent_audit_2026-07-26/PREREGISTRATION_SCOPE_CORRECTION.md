# Preregistration scope correction

Date: 2026-07-26

Base preregistration commit: `9cf083e`

This correction is recorded before outcome-bearing algebra. The original
preregistration files remain unchanged as historical evidence.

`ROUTE_UNIVERSE.tsv` row R10 and `READOUT_STRATUM_UNIVERSE.tsv` row Q16 use
abbreviated tokens that could be misread as limiting the ordinary-holonomy
survivors to `lambda=+1`, `-1`, and `0`. The corrected complete scope is:

- trivial holonomy preserves every `lambda`;
- ordered-pair screen-only `SO(2)` holonomy preserves every `lambda`;
- the larger timelike-line `SO(3)` reduction conditionally singles out
  `lambda=+1`;
- the larger spacelike-line `SO+(1,2)` reduction conditionally singles out
  `lambda=-1`; and
- `lambda=0` is distinguished only by the separate odd reciprocal-inversion
  route, not by ordinary screen holonomy.

The audit must therefore retain generic ordinary screen-only branches after
testing the physical twisted-isometry route. Rejecting that twisted route may
not be used to eliminate `lambda=0` or any other `lambda` from ordinary
trivial/screen-only holonomy.
