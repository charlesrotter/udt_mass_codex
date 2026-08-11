# G70 external-review adjudication

Date: 2026-08-11

External landing: `VERIFIED_WITH_CAVEATS`.

Effective evidence state:
`EXTERNALLY_VERIFIED_WITH_REPOSITORY_PROVENANCE_CAVEAT_CLOSED_LOCALLY`.

The reviewer found no scientific, algebraic, numerical, type, scope, or ownership defect. Its only
caveat was that a deliberately sealed non-git intake cannot inspect the source checkout's untracked
file state. The live read-only repository replay closes that provenance gate: all seven protected
draft paths remain untracked, their contents were not opened, and no unexpected path lies outside
the additions-only G70 adjudication layer.

The `33` paths frozen by `REVIEW_MANIFEST.tsv` remain byte-identical. This file is an additions-only
status layer and does not rewrite the reviewed result.

## What the reviewer independently reproduced

- `33/33` review-manifest hashes before source use;
- a clean-room eigen-based SPD logarithm and all `285` sensitivity matrices without importing the
  production builder;
- maximum matrix discrepancy `1.4489e-15` and maximum singular-ratio discrepancy `5.37e-13`;
- exact census: `46` full, `224` deficient, and `15` unresolved rows;
- exact rectangular-rank padding and every full and two-parameter classification;
- `R04` correlated branch: exactly `1/15` full, `11/15` unresolved, and `3/15` deficient, with the
  sole full row at ratio `1.627658e-6` and condition number `6.1438e5`;
- `R05`: `45/45 FULL_RANK_OBSERVED`, minimum ratio `7.443928959894951e-6`, maximum condition number
  `1.3433766031186198e5`;
- exact unknown-amplitude removal of the trace/log-area coordinate;
- exact unrestricted-source congruence compensation for every invertible screen map;
- all `315` G69 maps invertible, minimum singular value `0.04961347467704763`;
- the complete ownership ledger, including open physical source covariance, endpoint/profile,
  scalar-TT carry access, and polarization/orientation-sensitive access.

## Adjudication

The strict scientific landing remains `IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`. The `15` unresolved
weaker-model rows prevent a stronger atlas-wide conclusion. This does not erase the robust bounded
`R05` sub-result.

`R05` is a conditional algebraic sufficiency statement only. It assumes a known source covariance,
including normalization, plus independently observable azimuthal carry. Current UDT evidence owns
neither premise for the physical CMB query. No fit, source law, last-scattering endpoint, physical
profile, coefficient, spectrum, or polarization law follows.

## Exact status ledger

- `DERIVED`: SPD logarithmic coordinates; unknown-amplitude trace removal; unrestricted-source
  congruence theorem; screen map and geometric carry conditional on the supplied control query.
- `OBSERVED`: the frozen `19`-variant, `285`-row rank census and all numerical values above.
- `CHOSE_CONTROL`: screen basis, G68 query, endpoint grid, source examples, normalization premises,
  multiple-channel controls, finite-difference conventions, column normalization, and thresholds.
- `CONDITIONAL`: pairwise identifiability after independently fixing one parameter; low-redshift SNe
  compatibility anchor; any physical use of a carry-reading channel.
- `WORKING`: `X_max` as an inactive observer-pair asymptotic guard, not a CMB endpoint or profile
  selector.
- `OPEN`: physical CMB query, endpoint/profile, source covariance and normalization, scalar-TT carry
  access, polarization/source transport, action, bootstrap/source law, and local signalling.

## Evidence gates

1. Preregistered: yes, original G70 commits `79a72836` and `cb5cfae0`; external adjudication
   preregistered at `c89d2a20` before adding this layer.
2. Full or bounded: complete for the frozen `315` maps, `15` centers, `19` variants, and `285` rows;
   not a function-space or physical-CMB census.
3. Independent: separate internal SciPy route plus sealed cold external eigen-log replay.
4. Premises: all physical restrictions remain explicitly unowned.

Live repository replay: `66` premise guards; `98 passed, 1 xfailed`; six frozen manifests with `127`
members and `133` package paths; `1,114` unique current paths; `306` frontier rows resolving to `101`
unique targets; seven protected untracked paths present by metadata only.

## Next gate

Do not fit. The next bounded metric-led question is whether a complete physical observer-sky query or
global metric completion supplies any one of: source normalization/state restriction, physical
endpoint/profile selection, or an independently observable orientation/carry channel. Failure to
own one is not permission to invent it.
