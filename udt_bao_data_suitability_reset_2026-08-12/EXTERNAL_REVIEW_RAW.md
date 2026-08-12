SUSTAINED_VERIFIED_WITH_CAVEATS

**Evidence**
- The intake is internally consistent with a pre-inspection freeze: `PREREGISTRATION.md` states that
  no DR2 numerical value or covariance entry was inspected before registration,
  `CANDIDATE_LEDGER.tsv` marks only `OFFICIAL_DR2_GAUSSIAN` as `blind_numeric_audit=YES`, and the
  executed landing stays within the preregistered menu and no-fit/no-`X_max` scope.
- The official DR2 lane is strongly supported by source bytes and replay.
  `OFFICIAL_DR2_AUDIT_RESULT.json` pins the data/code commits, exact SHA-256s, 13 measurements,
  symmetric positive-definite 13x13 covariance, zero off-block entries, and Cobaya-vs-manual
  Gaussian replay agreement at `2.13e-14`; `INDEPENDENT_GAUSSIAN_REPLAY.json` adds a stdlib
  `Decimal` replay with `5.33e-15` delta; the copied public files are the released mean and
  covariance, and Cobaya points directly at them in `desi_bao_all.yaml`.
- The Table 4 width discrepancy is disclosed as a representation/type caveat, not hidden retuning.
  The mean values match Table IV to `<0.001` while `sqrt(diag(cov))` differs from the paper's
  marginalized widths by up to `0.0098`; the package does not alter bytes or exclude rows, and
  instead narrows the claim to "released Gaussian product with caveat." The intake paper also states
  that the distances are derived after template fitting and fiducial conversion, and that basis
  choice between `(DV/rd, DM/DH)` and `(DM/rd, DH/rd)` is mathematically immaterial for consistency
  calculations.
- The bounded classification is supported. `ONTOLOGY_CORRECTION.md` explicitly reinterprets `r_d`
  as a published packaging normalization only, and `GATE_RESULTS.tsv` records the resulting pass
  structure. The six anisotropic `D_M/D_H` ratios are legitimate normalization-free pattern-shape
  coordinates, with the stated warning that their delta-method errors are characterization only.
- The package's final language does not silently import an acoustic origin, standard ruler,
  Lambda-CDM dynamics, or raw-observer-pair status. Those imports are explicitly excluded.
- The five other lineage classifications are supported at the level claimed, though not with the
  same strength as the official DR2 lane. `LOCAL_ANGULAR_M2_M3` is only `CHARACTER_ONLY` because the
  code/report use diagonal jackknife variances and the radial leg was never built.
  `LOCAL_LYA_SELF_FIT` is `UNSUITABLE_AS_FIT` but `REPROCESSABLE`. `PUBLISHED_DR1_AP` is
  comparison-grade with retained fiducial packaging. `DR1_FULL_SHAPE_BAO_LIKELIHOOD` and
  `RAW_REDUCTION_ROUTE` being only `REPROCESSABLE` is consistent with the supplied evidence.

**Strongest Counterexample Or Failure Mode**
- The weakest load-bearing point is process provenance, not the DR2 likelihood replay. This sealed
  intake does not bundle an immutable git object, signed timestamp, or equivalent third-party proof
  that the preregistration existed before first DR2 numerical inspection; it provides consistent
  internal assertions and supportive file mtimes only.

**Repairs If Any**
- Bundle the preregistration commit object or signed git-log excerpt proving the pre-inspection
  freeze.
- Bundle one short explicit note that Table IV marginalized widths are not the same object as the
  released Gaussian covariance diagonal, so later readers cannot misread the `0.0098` gap as a replay
  failure.

**Maximum Justified Conclusion**
- The maximum justified conclusion is the package's bounded one: the official DR2 13-component
  published correlation-pattern product is suitable for a later separately preregistered UDT
  comparison only as either the six normalization-free `D_M/D_H` shape coordinates or the full
  13-vector with one free `PUBLISHED_NORMALIZATION_NUISANCE`. No stronger conclusion is justified
  here: no UDT fit, no feature-origin claim, no physical-history selection, and no `X_max` result.

Raw output provenance: external Codex `gpt-5.4`; session
`019ff7d4-545c-7c21-8448-f711c714b12c`; final-output SHA-256
`f04c5bb33c18030b611b9f810439cd8b9b4a812ba5c1b925c6b818c2be2590b7`. Intake-local clickable paths
from the original output were normalized to sealed relative filenames here because the temporary
intake is not durable.
