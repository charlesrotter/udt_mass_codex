# Preregistration — BAO data suitability reset

Date: 2026-08-12
Mode: `MAP -> OBSERVE`, no fit, data/provenance-led
Outcome status at registration: **NOT YET EVALUATED**

## 1. Whole question

Which, if any, existing or newly public BAO product is suitable to constrain the same complete
observer-pair relation used by the native SNe and CMB lanes?

This is a data-typing and provenance audit. It does not assume the conventional physical origin of
the measured clustering feature, import a GR/FLRW field equation, or fit a UDT profile. It asks only
whether the published or locally reduced quantities have a documented observational meaning,
covariance, fiducial-coordinate dependence, and likelihood sufficient for a later UDT prediction of
the same typed quantity.

## 2. Reconnaissance already seen before this freeze

The following coarse facts motivated the audit and are not blind outcomes:

- the local M2/M3 angular-correlation lineage used diagonal jackknife errors, found unstable
  single-ruler parameters, and never built its triggered radial estimator;
- older local Ly-alpha self-fits explicitly failed their absolute-fit gate;
- older AP tables used published distance summaries and were comparison-grade, not a native raw
  reduction;
- DESI now exposes a DR2 Gaussian BAO likelihood through the Cobaya BAO data package, and a DESI
  representative has stated that its measurement and covariance files are byte-identical to those
  used for the public DR2 chains.

No DR2 numerical value or covariance entry has been inspected for this audit before registration.

## 3. Candidate lineages

Every candidate must be classified independently:

1. `LOCAL_ANGULAR_M2_M3`: custom DESI DR1 angular Landy--Szalay shell search.
2. `LOCAL_LYA_SELF_FIT`: local Ly-alpha correlation-function reductions and templates.
3. `PUBLISHED_DR1_AP`: published DR1/eBOSS `D_M/r_d`, `D_H/r_d`, or their ratio.
4. `OFFICIAL_DR2_GAUSSIAN`: DESI DR2 measurement vector and covariance distributed through the
   Cobaya BAO package and confirmed by DESI provenance.
5. `DR1_FULL_SHAPE_BAO_LIKELIHOOD`: public observable/window/covariance products, if a bounded
   UDT-compatible readout can be typed without importing the conventional dynamics.
6. `RAW_REDUCTION_ROUTE`: raw/catalog/correlation products sufficient to reconstruct an angular and
   radial observable under a new preregistered pipeline.

## 4. Fixed suitability classes

- `PAIR_READY`: the data product exposes an observer-pair observable that the complete UDT relation
  can predict directly, with full covariance and documented transformations.
- `AP_READY_WITH_FIDUCIAL_MAP`: the product supplies a transverse/radial ratio or equivalent with
  covariance; the fiducial coordinate map remains a declared comparison/readout layer.
- `SCALE_READY_WITH_NUISANCE_RULER`: the product supplies calibrated transverse/radial distances
  divided by an unknown common ruler. It may be used only with that ruler as a nuisance or external
  observational anchor, never as a UDT-derived mechanism.
- `CHARACTER_ONLY`: sufficient for qualitative shape or consistency checks, not a likelihood.
- `REPROCESSABLE`: unsuitable as shipped but contains adequate raw ingredients for a new,
  separately preregistered reduction.
- `UNSUITABLE`: missing or failed provenance, covariance, observable typing, estimator validation,
  or an essential channel.

Classes are not ordered by whether they favor UDT.

## 5. Fixed gates

A product may enter a later calibration only if every gate required by its claimed class passes:

1. `G-PROVENANCE`: release, version/tag or immutable content hash, primary paper, and data owner are
   recorded.
2. `G-OBSERVABLE`: each vector component is defined operationally; model parameters and raw
   observables are not conflated.
3. `G-COVARIANCE`: full within-bin covariance is supplied and positive definite on the used subspace;
   cross-bin/tracer covariance is supplied or its omission is justified by the release.
4. `G-FIDUCIAL`: the fiducial coordinate cosmology, reconstruction convention, and transformation to
   the published summary are documented. They may be readout tools, not UDT premises.
5. `G-TWOLEG`: anisotropic use requires both transverse and radial legs with their covariance.
   Isotropic-only points remain isotropic-only.
6. `G-LIKELIHOOD`: an independent implementation reproduces the released Gaussian quadratic form on
   fixed test vectors.
7. `G-RULER`: `r_d` or another feature scale is typed as observed nuisance/external calibration unless
   UDT later derives it; it is never silently fixed by Lambda-CDM.
8. `G-NO-ORIGIN-IMPORT`: the conventional acoustic-origin interpretation may identify the public
   dataset but cannot enter the UDT metric derivation.
9. `G-NO-FAVORABLE-SELECTION`: all released DR2 bins and all covariance-coupled components are kept
   unless an exclusion is fixed before inspecting UDT residuals.
10. `G-REPRODUCIBLE`: exact input bytes, hashes, parser, derived vector, covariance, and checks are
    preserved.

## 6. Falsification and maximum conclusion

The current BAO corpus is calibration-ready only if at least one lineage passes its claimed class
without repairing it after seeing UDT residuals.

The audit must return one primary landing:

1. `OFFICIAL_PRODUCT_READY_FOR_TYPED_UDT_LIKELIHOOD`;
2. `OFFICIAL_PRODUCT_READY_ONLY_WITH_DECLARED_FIDUCIAL_OR_RULER_NUISANCE`;
3. `RAW_PRODUCTS_REQUIRE_NEW_PREREGISTERED_REDUCTION`;
4. `NO_CURRENT_BAO_PRODUCT_IS_CALIBRATION_READY`;
5. `TYPE_FAILURE`.

Even landing 1 does not validate UDT, derive the origin or scale of the feature, select a physical
pair history, or determine `X_max`. It only authorizes a later preregistered comparison. No SNe--BAO
fit or `X_max` estimate may be produced in this package.
