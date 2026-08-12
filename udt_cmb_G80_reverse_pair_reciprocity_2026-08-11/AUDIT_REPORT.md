# G80 audit report — reverse ordered-pair reciprocity

Date: 2026-08-11

Status:
`PROVISIONAL_INTERNALLY_VERIFIED__FRESH_ADVERSARIAL_REVIEW_REQUIRED`

## Outcome

On the exact G79 control metric and endpoint pair, the complete past-directed affine reversal
returns to the original event, tangent, and screen and satisfies

```text
Z_reverse = 1/Z_forward,
phi_reverse = -phi_forward,
D_reverse = Z_forward transpose(D_forward),
d_A_reverse = Z_forward d_A_forward.
```

The production full-Jacobi residual is `6.885259158085081e-15`. A separately written direct-
Christoffel neighboring-ray calculation reproduces the reverse map within
`1.4161064164681488e-08` of production and the reciprocity identity within
`1.4204869936356233e-08`, well inside the preregistered `2e-4` gate.

## Exact bounded values

```text
profile                  G75_AM_S01_E05
Z_forward                1.1456439237389628 = sqrt(21)/4
Z_reverse                0.8728715609439718 = 4/sqrt(21)
phi_forward              0.13596685774182335
phi_reverse             -0.1359668577418183
d_A_forward/R            0.7559850215834019
d_A_reverse/R            0.8660896464146981
forward affine/R         0.7560742639231726
reverse affine/R         0.8661918863589938
```

The complete `1024/2048/4096` refinement ladder, forward/reverse matrices, endpoint-return checks,
and residuals are in `DERIVATION_RESULT.json` and `REFINEMENT_ATLAS.tsv`.

## Premise and type boundary

The reversal flips the **entire** affine tangent and divides by the source frequency. It is the
past-directed reversal of the same geometric curve. It is not a future source-to-receiver signal,
and G80 derives no local information speed or causal messaging law.

The metric profile and endpoints remain `CHOSE_CONTROL`. `c_E` is the observed calibration; `R`
remains symbolic and unselected. P1, `X_max`, and `cmb_temp` are inactive. No luminosity law,
physical source, last-scattering surface, fit, spectrum, action, matter law, or bootstrap selector
enters.

## Internal evidence gates

1. **Preregistered:** yes, commit `76683fa1`.
2. **Full or bounded:** complete only for one frozen profile, one ordered endpoint pair, and the
   mathematical reversal of one null branch.
3. **Independently verified:** yes by a direct-Christoffel neighboring-ray route, with shared
   metric/query/endpoint/screen/ODE-family caveats; fresh adversarial semantic review is pending.
4. **Premises audited:** yes; `PREMISE_LEDGER.tsv`, `TYPE_LEDGER.tsv`, and ten hostile catches.

## Maximum current conclusion

```text
DERIVED_CONDITIONAL_RECIPROCITY_ON_ONE_FROZEN_GEOMETRY_AND_ONE_ORDERED_PAIR
```

Do not promote this to a physical cosmological profile, `X_max` curve, luminosity-distance law,
`cmb_temp`, CMB observable, or signal propagation claim.
