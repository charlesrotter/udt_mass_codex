# External review dispatch — G82 fixed-C1 Radau replay

Perform a cold, read-only adversarial review of the sealed intake defined by `REVIEW_MANIFEST.tsv`.
Do not inspect files outside the intake, edit files, or continue the research.

## Central question

Did G82 honestly replay exactly the frozen G81 `C1_FULL_ANGULAR` direct-Christoffel neighboring-ray
control with the non-DOP853 `Radau` integrator family, and do the saved artifacts support only:

`G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`?

## Required checks

1. Verify every manifest hash and the committed preregistration boundary.
2. Confirm that profile, observer query, endpoint, direction, screens, rotations,
   finite-difference deltas, reverse tangent, and numerical gates are unchanged from G81 C1.
3. Inspect the implementation for actual `Radau` use, hidden DOP853 fallback, silent retuning,
   event or projection changes, or result-dependent branching.
4. Independently recompute from saved matrices:
   - Radau versus DOP853 matrix differences;
   - unrotated reciprocity;
   - rotated covariance;
   - determinant/area reciprocity.
5. If the sealed environment permits, rerun the exact G82 program and compare output bytes or
   numerical fields. Distinguish rerun evidence from independent algebra.
6. Assess the exact independence gained. The implementation deliberately shares the metric,
   Christoffels, query, projection, and finite-difference machinery with G81; only the integrator
   family changes.
7. Exercise or inspect the hostile catches and find any missing route by which one control,
   numerical agreement, or past-directed reversal could be overpromoted.
8. Return one landing: `VERIFIED`, `VERIFIED_WITH_CAVEATS`, `CORRECTION_REQUIRED`, or `FAILED`.

## Binding authority ceiling

Even a clean review cannot promote G82 beyond one frozen-control integrator-family sensitivity
check. The scientific maximum remains G81's
`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

Do not derive or select a UDT physical profile, endpoint, scale, `X_max`, SNe/CMB observable,
`cmb_temp`, source, action, matter, bootstrap closure, signalling law, or future signal.
