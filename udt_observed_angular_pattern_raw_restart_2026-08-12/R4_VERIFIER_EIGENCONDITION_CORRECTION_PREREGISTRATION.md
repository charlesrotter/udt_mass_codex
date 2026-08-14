# R4 verifier eigencondition correction — preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_THIRD_VERIFIER_FAILURE__BEFORE_RERUN`

## Third return

The corrected replay again passed the complete relation/lag surface and the registered
range-projector checks, then stopped at:

```text
record: CMASS / factor 1 / group 8 / W1_SPECTRO / NSIDE 4
metric: positive_condition
saved production value:       15267446.703116551
independent SciPy-eigh value: 15267446.698380202
absolute difference:          0.004736349
relative difference:          about 3.10e-10
```

No verification result was written and no angular structure was interpreted.

## Diagnosis and frozen correction

`positive_condition = lambda_max/lambda_min_positive` is itself an eigensystem-conditioned
quantity. Applying the generic `3e-10` relative tolerance to this ratio while using a
condition-aware tolerance for downstream range fields is inconsistent.

Add `positive_condition` to the same condition-aware comparison class:

```text
condition_bound = max(3e-10, 2048 * eps_float64 * positive_condition).
```

Use `rtol=condition_bound`, `atol=3e-12` for this field. Keep `rank`, `rank_tau`, direct eigenvalue
endpoints, raw/diagonal covariance scales, and all other nonprojector descriptors at their existing
tolerances. Record the realized condition-number discrepancy.

This is the last a-priori member of the thresholded eigensystem-sensitive class. It changes no
production output, relation, covariance, rank rule, premise, count, or scientific conclusion.
