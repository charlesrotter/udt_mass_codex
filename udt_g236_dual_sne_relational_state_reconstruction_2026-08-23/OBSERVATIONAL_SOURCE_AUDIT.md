# G236 observational-source audit

Date: 2026-08-23

## Local release facts

The Pantheon+ table provides corrected apparent magnitudes, multiple redshift fields, survey IDs,
calibrator flags, and the release covariance. G236 retains the existing `zCMB > 0.023`,
non-calibrator cut and removes all survey-10 rows for the primary cross-release test.

The DES-Dovekie release README states that:

- `zHD` includes CMB-frame and peculiar-velocity corrections;
- `MU` is constructed from fitted light-curve parameters, nuisance coefficients, a host term, and
  `biasCor_mu`;
- the tabulated distance normalization assumes `H0=70`;
- the supplied `STAT+SYS.npz` stores an inverse covariance rather than a covariance.

The additive `H0` normalization is absorbed by the catalog offset. The other release processing is
retained as observational cargo and is not reclassified as UDT geometry.

## Primary-method warning

The DES collaboration's nonstandard-cosmology audit identifies the approximate cosmology used in
bias-correction simulations as the largest potential cosmological assumption in the released
Hubble diagram. It reports that substantial shifts in the approximate matter-density parameter
produced biases smaller than the simulated statistical uncertainties and supplies a mitigation
method. That is evidence of robustness within the collaboration's tested model neighborhood, not
proof of model independence for UDT.

Pantheon+ is likewise a standardized and bias-corrected distance release. G236 therefore uses both
catalogs only as `OBSERVED_PROCESSED_CONDITIONAL` state measurements.

## Source links

- DES-Dovekie release README:
  <https://github.com/des-science/DES-SN5YR/blob/main/4_DISTANCES_COVMAT/README.md>
- DES nonstandard-model and bias-correction audit:
  <https://arxiv.org/abs/2406.05048>
- Pantheon+ full data and light-curve release:
  <https://arxiv.org/abs/2112.03863>

No Lambda-CDM luminosity-distance curve is used in the G236 transformation or reconstruction.
