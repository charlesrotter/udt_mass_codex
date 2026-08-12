# G79 external adversarial-review adjudication

Date: 2026-08-11

External model: `gpt-5.4`, fresh ephemeral context, high reasoning, web disabled

Sealed intake: `37` files total (`36` payload rows plus `REVIEW_MANIFEST.tsv`)

Sealed-manifest SHA-256:
`375ebfab12f0eb091aac930ee812589d172831f3dffe5159c66f286474f3f185`

## Final status

`VERIFIED_WITH_CAVEATS__BOUNDED_SAME_GEOMETRY_REDSHIFT_AND_ANGULAR_DISTANCE_QUERY`

The reviewer found no redshift-sign, endpoint-timelikeness, Jacobi-scale, P1-role, or
thermal-scope error.  It independently reproduced the outcome-independent profile selection,
dimensional factorization, stationary endpoint ratio, complete `4096` Jacobi endpoint, refinement
ladder, residuals, and independent neighboring-ray comparison.

The bounded scientific landing survives unchanged:

```text
DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY
```

## Exact reproduced values

```text
profile                 = G75_AM_S01_E05
A(x)                    = 1-x^2/4
h(x)                    = x^6/20
1+z                     = sqrt(21)/4
phi_pair                = log(sqrt(21)/4)
d_A/R                   = 0.7559850215834019
affine/R                = 0.7560742639231726
det(D_hat)              = 0.5715133528584565
null residual           = 1.4183200820413355e-15
Killing-energy drift    = 2.6645352591003757e-15
screen Gram residual    = 9.325873406851315e-15
```

The reviewer independently reran the neighboring-ray route and obtained
`d_A/R=0.7559850216165241`, differing from the frozen packaged value by only
`1.7430501486614958e-14`; its full-map relative difference from production was
`4.381542485329791e-11`.

## Binding caveats

1. **Sealed replay portability.**  The production and independent scripts use `git show` to load
   their frozen source data.  The sealed intake contains the source bytes, but the scripts do not
   automatically fall back to those files.  The reviewer therefore reconstructed and reran the
   calculation rather than executing each shipped script unchanged inside the non-Git intake.
   This is a reproducibility caveat, not a contradiction.
2. **Method independence is bounded.**  The neighboring-ray verifier replaces the production
   Riemann/Jacobi equation with directly rebuilt Christoffels and finite-difference geodesic
   neighbors.  It still shares the metric ansatz, endpoint event, screen seed, and DOP853 method
   family.  That is sufficient for this one-ray consistency claim, not full end-to-end
   independence for a broader physical model.
3. **Route orientation.**  The integrated angular-map branch runs receiver to source.  The
   stationary redshift ratio is unaffected because conserved Killing energy and endpoint lapse
   values own it.  A reverse source-initial solve remains the smallest direct reciprocity check.

## Thermal sequencing

The reviewer accepted the temperature formula only as a conditional future readout for a supplied
one-parameter thermal spectrum.  It does not derive a source, thermalization law, last-scattering
surface, detector response, anisotropies, or power spectrum.  Project sequencing remains:

```text
same-geometry SNe join -> endpoint/X_max curve -> deferred cmb_temp application.
```

## Evidence gates

1. **Preregistered:** yes, commit `4bea21b7`.
2. **Full or bounded:** complete only for one selected stationary profile/query and one sky ray.
3. **Independently verified:** yes for the bounded algebra/numerics, with the method-sharing caveat
   above; external review hash-checked all `36/36` payload rows and reran load-bearing values.
4. **Premises audited:** yes; no physical profile, scale, endpoint, `X_max`, source, fit, CMB field,
   action, matter law, or bootstrap rule is promoted.

Repository-wide tests, frozen-manifest replay, current-path checks, and protected-dirt checks remain
local repository regression evidence.  They were represented inside the sealed intake but could
not be independently rerun without the repository and must not be called sealed scientific
evidence.

## Next bounded calculation

Preregister and run the reverse source-initial null-plus-Jacobi branch on this exact same geometry
and endpoint pair.  Test the appropriate redshift reversal and angular-distance reciprocity before
opening an `X_max`/endpoint family or applying `cmb_temp`.

