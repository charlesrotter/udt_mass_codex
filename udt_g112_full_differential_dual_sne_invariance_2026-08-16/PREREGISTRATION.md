# Preregistration — G112 full-differential dual-SNe invariance replay

Date: 2026-08-16

Mode: frozen observational replay after the G110/G111 type correction; no shape refit

## Whole question

Does the G110/G111 full observer-differential reconstruction leave the frozen G99 P1 SNe relation
numerically unchanged on both Pantheon+ and DES-SN5YR/Dovekie when pair depth and sky area are kept
as distinct blocks of one supplied observation relation?

This is an invariance and gross-compatibility test. It is not a fit of the nonflat R17 controls, a
selection of a complete metric history, or a derivation of the conditional flux law.

## Frozen typed interface

Use exactly

```text
n = 1.0559332414320268,
Z = 1+z,
Phi(z) = log Z,
lambda_A(z) = n [1-Z^(-2/n)],
D_sky(z) = lambda_A(z) I2,
dL_shape(z) = Z^2 sqrt(det D_sky) = n Z^2 [1-Z^(-2/n)].
```

`Phi` is the terminal pair-depth block. `D_sky` is a separate isotropic screen-area representative
of the already registered conditional SNe transfer. The equality `D_sky=lambda_A I2` is a
`CONDITIONAL_REPRESENTATIVE`, not a metric-derived physical history. G110/G111 requires the blocks
to remain distinct; it does not prohibit a supplied relation whose SNe-visible area happens to be
isotropic.

No angular shear, rotation, R17 parameter, twist, `lambda_R`, profile amplitude, regime score,
bootstrap variable, or `X_max` value may be appended or fitted. The inherited
`d_L=Z^2 d_A` readout remains `CONDITIONAL_OBSERVATIONAL_TRANSFER`.

## Frozen datasets and likelihood

Pantheon+:

- use `zCMB`, `m_b_corr`, `zCMB>0.023`, and `IS_CALIBRATOR==0`;
- use the registered full STAT+SYS covariance;
- hold `n` fixed and profile one additive magnitude zero point analytically;
- require the resulting prediction, offset, and chi-square to reproduce G99/G65.

DES-SN5YR/Dovekie:

- use exactly the 1,623 `IDSURVEY==10` rows, `zHD`, `MU`, and the marginal DES block of the
  registered STAT+SYS covariance;
- hold `n` fixed and profile one additive magnitude zero point analytically;
- require reproduction of the frozen G100 primary result and preserve its low-chi-square warning.

The additive offsets are survey calibrations, not metric parameters. No Lambda-CDM distance,
expansion history, cosmological chain, standard ruler, BAO, or CMB object may enter.

## Certification and falsification

1. Every source hash must match before data evaluation.
2. The typed formula and the legacy frozen P1 formula must agree pointwise to `1e-12` in magnitudes
   on every retained row of each survey.
3. `n` must remain bit-identical to G99. No shape optimizer may run.
4. Fresh Pantheon+ and DES covariance likelihoods must reproduce the registered chi-squares and
   offsets within the frozen numerical tolerances.
5. A second implementation must use a distinct covariance algebra and direct-power formula.
6. Hostile checks must reject: identifying pair and sky blocks; moving `n`; adding an orchestra
   correction; replacing marginal covariance by a precision subblock; using a forbidden cosmology
   field; or promoting the screen representative to a selected complete history.
7. Existing low-chi-square and data-reduction caveats must survive unchanged.

## Registered returns

- `DUAL_SNE_NUMERICAL_INVARIANCE_WITH_EXISTING_CAVEATS`: all gates pass.
- `G110_G111_RETYPE_CHANGES_FROZEN_SNE_PREDICTION`: pointwise equality fails.
- `DUAL_SNE_REPLAY_MISMATCH`: a raw likelihood does not reproduce.
- `SOURCE_OR_TYPE_FAILURE`: provenance or block typing fails.

## Maximum conclusion

At most G112 may show that the corrected one-observer full differential is compatible with, and
does not numerically disturb, the frozen conditional P1 middle-regime SNe relation on these two
reductions. It cannot derive P1, select a complete history, activate the nonflat R17 control as the
SNe universe, derive flux, establish UDT, infer `X_max`, or constrain BAO/CMB/bootstrap/microphysics.
