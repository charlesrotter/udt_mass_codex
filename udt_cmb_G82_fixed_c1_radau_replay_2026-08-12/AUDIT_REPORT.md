# G82 audit report — fixed-C1 Radau replay

## Landing

`INTERNALLY_VERIFIED_NUMERICAL_METHOD_REPLAY__EXTERNAL_REVIEW_PENDING`.

The exact frozen G81 control `C1_FULL_ANGULAR` passes every preregistered gate when the
direct-Christoffel neighboring-ray calculation uses implicit `Radau` instead of `DOP853`.

The largest relative difference between the fine Radau and frozen DOP853 screen matrices is
`9.459627107202695e-12`, against the preregistered `2e-4` gate. The Radau screen-covariance
residuals are:

```text
unrotated matrix reciprocity   1.139757402684705e-8
rotated matrix covariance     1.1582146620151037e-8
area reciprocity              1.2229577572853145e-8
```

The largest Radau coarse/fine finite-difference change is `3.449865616964161e-8`. Frequency,
endpoint return, nullness, production-map agreement, covariance, and area gates all pass without
retuning.

## What changed and what did not

Only the integrator family changed: SciPy `Radau` replaced `DOP853`. The metric, Christoffels,
profile, observer query, C1 direction, endpoint, screens, rotations, finite-difference sizes,
projection implementation, and pass thresholds are shared with G81. This is therefore a clean
integrator-family sensitivity check, not an independent geometry implementation.

The allowed G82 statement is:

`G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`.

The scientific maximum remains unchanged:

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

## Four evidence gates

1. **Preregistered:** yes, at commit `88afa190`, before executing G82.
2. **Full space or bounded scope:** full exact one-control universe; the scope is explicitly one
   frozen angular control and one alternative integrator family.
3. **Independently verified:** yes at the saved-artifact level. A separate verifier reopened all
   six frozen source rows, independently recomputed the three Radau/DOP853 matrix differences and
   the unrotated, rotated, and area residuals, and passed. This is not independent metric code.
4. **Every premise audited:** yes in `PREMISE_LEDGER.tsv`; fifteen hostile mutations are rejected.

Fresh external adversarial review remains pending before the package is promoted beyond internal
verification.

## Authority boundary

G82 does not prove absolute method independence, a generic all-direction theorem, or a UDT-specific
selector. It selects no physical profile, endpoint, scale, `X_max`, SNe/CMB observable,
`cmb_temp`, source, action, matter, bootstrap closure, signalling law, or future signal.

## Next gate

Seal this exact package for read-only adversarial review. If review upholds it, close the G81
integrator-family caveat and return to the deferred physical endpoint/`X_max` curve or thermal-map
question; do not add more directions or numerical methods merely to accumulate confirmations.
