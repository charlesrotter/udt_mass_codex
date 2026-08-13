# R3 preflight note

Date: 2026-08-13
Status: `ENGINE_FEASIBILITY_ONLY__NO_COVARIANCE_EVALUATED`

Random-only footprint reconnaissance found occupied raw HEALPix pixels as follows:

| sample/cap | NSIDE 4 | NSIDE 8 | NSIDE 16 |
|---|---:|---:|---:|
| CMASS North | 51 | 169 | 623 |
| CMASS South | 26 | 76 | 261 |
| LOWZ North | 46 | 159 | 577 |
| LOWZ South | 26 | 76 | 261 |

At NSIDE 16 every full footprint has more than 119 occupied pixels, while the coarser levels expose
the expected rank-limited regimes. Occupancy is unequal because boundary pixels have partial survey
coverage; this is retained and reported.

One engine-only benchmark used the first CMASS-North fine selection at NSIDE 16, with 8,228 data and
164,560 deterministic 20x random rows. No curve or covariance value was inspected. TreeCorr produced:

| component | seconds | patch-pair results | peak RSS after component |
|---|---:|---:|---:|
| DD | 3.20 | 177,310 | 1.732 GiB |
| DR | 9.47 | 367,115 | 1.870 GiB |
| RR | 14.75 | 190,653 | 1.870 GiB |

This supports one-selection-at-a-time CPU execution below the 16 GiB guard. The benchmark initially
encountered and corrected a local call typo in random patch-label assignment; no covariance or
scientific artifact was produced by that failed call.
