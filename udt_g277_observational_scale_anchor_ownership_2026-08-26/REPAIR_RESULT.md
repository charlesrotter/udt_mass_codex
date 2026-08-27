# G277 repair result

Date: 2026-08-26

Status: `R1_R5_ACCEPTED__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED`

## R1 — sealed primary sources

Pass. The official Pantheon+ distance README and SH0ES likelihood are local, hashed sources. Both
production and independent routes check the load-bearing semantic statements.

## R2 — actual covariance-weighted design

The original raw-symmetry gate failed and remains failed:

```text
raw max |C-C^T| = 3.0000000000038676e-08
frozen threshold = 1e-12
```

R2B then preregistered three symmetric finite-serialization interpretations. All pass Cholesky,
actual weighted rank two, and the `1e-12` eigenvalue-ratio gate:

| route | smallest/largest Fisher eigenvalue |
|---|---:|
| symmetric mean | `0.0040278223639286835` |
| reflected lower | `0.004027821634253167` |
| reflected upper | `0.004027823093623193` |

Maximum Fisher-entry route difference is `3.052768399046228e-09`; maximum eigenvalue route
difference is `1.8201574108595377e-07`, both below the frozen `1e-4` tolerance.

## R3 — independent classifications

Pass. The independent route now parses both sealed primary sources, both G79 ledgers, and the actual
covariance, together with the hashed Pantheon+, DES, G236, G258, G275, and G276 evidence. It derives
the fact vector and all six registered comparison classes from those source semantics and computed
ranks through an explicit six-criterion ownership predicate. Its weighted calculation uses
Cholesky whitening and a direct `2 x 2` determinant rather than the production
solve/eigendecomposition route.

## R4 — hostile controls

Pass. Eleven overclaims separately exercise every registered named failure criterion, including
source ownership and both `X_max` gates. There are zero unconditional-true, phrase-anywhere, or
literal-missing-column semantic controls.

## R5 — evidence wording

Pass locally. Reports retain the raw covariance failure, describe the three numerical routes, call
the controls overclaim controls, and keep the scientific conclusion conditional.

## Scientific change

None. The original bounded landing remains unchanged. No fit, numerical scale, metric/kernel change,
history, operational distance, or `X_max` was selected.

## Repair-only verdict

Accepted. The zero-context follow-up verified that R3 facts now come from hashed source semantics
and computed ranks, R4 reaches every registered acceptance criterion, and R5 wording is accurate.
It reran the registered no-write checks and found no scientific expansion.
