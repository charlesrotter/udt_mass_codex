# G185 audit report

Date: 2026-08-20

## Landing

```text
CENTRAL_SPHERICAL_SNE_QUERY_RETAINS_THE_FULL_RELEVANT_METRIC_RESPONSE
__RADIAL_PAIR_ANGULAR_TANGENT_ZERO_IS_QUERY_DERIVED
__AREAL_SKY_RESPONSE_R2_REMAINS_ACTIVE
__FROZEN_DUAL_SNE_REPLAY_IS_CONDITIONALLY_PRESERVED
```

Grade before fresh external review: `INTERNALLY_VERIFIED_CONDITIONAL_LEAD`.

## What was learned

The completed-pair kernel does not require an instruction to silence the angular sector in the
central radial SNe query. The angular tangent Gram vanishes because the supplied radial pair plane
has no angular tangent. Independently, the observed sky beam retains the exact metric-derived area
response `R^2`. These facts coexist without contradiction because they describe different objects.

With the old radiative-transfer bridge held explicitly `IMPORTED_CONDITIONAL` and the P1
radius-frequency relation held `FROZEN_HISTORICAL_CALIBRATION`, the accepted kernel reproduces both
frozen SNe likelihoods with no optimizer, no retuning, no terminal-depth insertion, and no
post-readout angular factor.

## Raw gates

- 14/14 exact source hashes passed.
- Production symbolic channel checks passed.
- Pantheon+: 1367 rows, chi-square `1260.8480887274907`.
- DES-SN5YR: 1623 rows, chi-square `1444.1864417504896`.
- Frozen curve residuals: below `3.6e-15` mag.
- Independent chi-square residuals: below `2.3e-12`.
- Deleting, duplicating, or incorrectly transferring the sky-area factor is decisively detected.
- Shape optimizer calls: zero.
- Mutation catches: 13/13; semantic guards: 11/11.
- Exact premise registry: PASS, 170 rows plus 754 historical dispositions.
- Repository regression: 130 passed, 1 expected xfail.

## Premise audit

| Object | Stamp |
|---|---|
| primary spherical metric | `pinned-by-THEORY` within declared macro slice |
| full pullback before reciprocal readout | `pinned-by-THEORY` |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` |
| central radial point-observer query | `SUPPLIED_QUERY` |
| sky area `|det D_sky|=R^2` | `DERIVED_CONDITIONAL` from supplied spherical metric/query |
| release coordinates and covariances | `OBSERVED` |
| `eta=1`, `epsilon=1/Z` | `IMPORTED_CONDITIONAL` |
| P1 `n` and radius-frequency shape | `FROZEN_HISTORICAL_CALIBRATION` |
| one magnitude offset per catalog | `DECLARED_NUISANCE_PROFILE` |

## What remains open

- native UDT radiative transfer;
- derivation of the physical `R(Z)` or `phi(r)` history;
- displaced, nonspherical, nonradial, mixed, caustic, and multiple-image queries;
- physical branch population and aggregation;
- global completion and `X_max`;
- BAO, CMB, dynamics, matter, bootstrap, and signalling.

The SNe result is a non-regression and channel-ownership result. It is not a new fit or a complete
cosmological validation.
