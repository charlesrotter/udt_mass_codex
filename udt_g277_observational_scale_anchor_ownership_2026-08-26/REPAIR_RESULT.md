# G277 repair result

Date: 2026-08-26

Status: `EXTERNAL_R1_R2_ACCEPTED__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED`

## External R1 — sealed versus repository-only evidence

Implemented. The `181 passed, 1 xfailed` suite remains valid local repository evidence, but is now
explicitly outside the sealed review scope and not externally replayed.

## External R2 — distinct same-object and bridge facts

Implemented. The independent verifier now reads G250 and G251 separately from G258 and G275,
emits distinct `same_object` and `bridge_owned` facts, and independently classifies the exact eight
production candidates. G276 and G250 remain positive type controls; the observational SNe routes
retain separate same-object and operational-distance/transfer gaps.

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
covariance, together with the hashed Pantheon+, DES, G236, G250, G251, G258, G275, and G276 evidence. It derives
the fact vector and all eight registered comparison classes from those source semantics and computed
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

The earlier zero-context follow-up verified that R3 facts came from hashed source semantics
and computed ranks, R4 reaches every registered acceptance criterion, and R5 wording is accurate.
It reran the registered no-write checks and found no scientific expansion.

The fresh external G277 review retained that science and requested the two repairs above. The
repair-only external follow-up accepted both with no remaining defect. It independently verified
52-file intake integrity, all 18 frozen sources, the three no-write replays, unchanged durable
artifact hashes, the covariance control, and exact eight-class agreement. The scientific landing
did not change.
