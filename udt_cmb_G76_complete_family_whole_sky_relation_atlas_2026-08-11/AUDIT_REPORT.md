# G76 audit report — complete-family whole-sky relation atlas

Date: 2026-08-11

Status: `PROVISIONAL_AWAITING_FRESH_ADVERSARIAL_REVIEW`

## Landing before external review

`NUMERICALLY_UNRESOLVED_FAMILY`, with a verified bounded sub-result:

```text
587 SAMPLED_COMPLETE_ORIENTATION_PRESERVING
4 NUMERICALLY_UNRESOLVED
0 sampled missing/fold/negative/near-zero-area cases
```

The family landing remains numerical because four rows exceed the frozen time-refinement threshold.
No threshold was changed and no row was removed.

## What was learned

The complete 591-profile G75 stationary axial control family was evaluated under the exact G74
whole-sky observer query. All 591 sampled maps cross completely, have degree one, retain positive
signed face area and positive intrinsic face-map orientation, and avoid the registered near-zero
area diagnostics. The family therefore supplies a robust sampled whole-sky relation topology under
this bounded query, not a unique physical profile.

The four unresolved rows fail only the frozen `512`-versus-`1024` endpoint chord gate. Their mesh
degree, Hamiltonian backward error, reflection, crossing, orientation, and critical-area gates pass.

## Verification gates

1. **Preregistered:** yes, commits `c3c2699d` and correction `89e7a8a4`, before production.
2. **Full or bounded scope:** full `591/591` frozen G75 family; bounded to the stated stationary
   metric, observer query, meshes, and endpoint.
3. **Independent load-bearing verification:** direct Christoffel replay passes on all eight exact
   G75 strata; saved-artifact census and nine frozen G74 replays pass. Fresh external review pending.
4. **Premise audit:** complete in `PREMISE_LEDGER.tsv` and `OWNERSHIP_LEDGER.tsv`; no profile,
   endpoint, scale, source, polarization law, or physical owner is selected.

## Numerical facts

See `EXACT_DERIVATION.md` and machine-readable outputs. Decisive extrema are:

- degree: `[0.9999999999999999, 1.0000000000000002]`;
- signed area ratio: `[0.48488311917529653, 2.8720295134891574]`;
- tangent-map singular values: `[0.596894470340065, 1.8877867031540811]`;
- maximum shear ratio: `1.5944554891818246`;
- maximum Hamiltonian error: `3.3559291523488355e-7`;
- maximum frozen G74 replay chord: `3.3306690738754696e-16`.

## Limits

This is not continuum proof of global injectivity, generic complete-metric behavior, a selected CMB
background, a source law, peak prediction, polarization transport, universe size, `X_max`, action,
matter, or bootstrap selection. The endpoint tangent map does not replace G72's path-carried screen
transport.

## Proposed bounded next action after review

If the external review accepts the type and algebra, freeze and bank G76 as a
`VERIFIED_WITH_CAVEATS` whole-family atlas. The next scientific step should use this robust relation
family to separate source-independent angular response from source/population freedom; it should
not fit peaks or choose a profile before that ownership audit.
