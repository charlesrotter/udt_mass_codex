# G68 F01/F02 finite-path observer-sky Jacobi controls — audit report

## Landing

`FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE`.

Evidence grade after fresh sealed adversarial review:
`VERIFIED_WITH_CAVEATS`.

All `21/21` preregistered F01/F02 control trajectories reach the declared finite endpoint without a
turning event, caustic, chart failure, or solver failure. F01 reproduces `D=sI`. Every nonzero F02
row develops finite one-axis anisotropy and profile-dependent area/azimuthal carry, while the
registered finite screen-rotation channel remains zero to numerical precision.

## What was learned

- The local G67 effect accumulates into a stable finite-path geometric map in this bounded profile
  ensemble.
- The accumulated area correction is not determined by mixing amplitude alone: persistent,
  tapered, and sign-changing profiles give different magnitudes and even different area signs.
- The finite map approaches F01 quadratically in all nine preregistered small-mixing checks.
- Reversing `h` reverses azimuthal carry and obeys exact screen conjugation without changing the
  underlying diagonal area/shear readout.
- No screen rotation appears in this stationary equatorial ensemble. That does not decide general
  angular, time-live, holonomy, or polarization behavior.

## Evidence gates

1. **Preregistered:** yes—main universe at `05654f24`, all-profile bundle/reflection checks at
   `76938822`, and epsilon controls at `b8360f40`, all before trajectory inspection.
2. **Full or bounded:** full over exactly `21` registered atlas rows, `18` sign-reflection controls,
   `18` epsilon-limit auxiliaries, and both bundle directions/deltas on all `21` rows. It is a
   bounded analytic profile slice, not all profiles or queries.
3. **Independent:** separate geodesic-bundle differentiation agrees `21/21`, with maximum relative
   map error `8.93e-11`; DOP853 refinement and RK45 also agree. A fresh sealed gpt-5.4 reviewer
   independently reconstructed the equations, reran representative paths, densely sampled all
   paths for rank loss, and returned `VERIFIED_WITH_CAVEATS`.
4. **Premises:** audited. Every profile, endpoint, amplitude, chart, and query choice remains a
   declared control; no physical family/profile/source was selected.

Internal package checks pass `18/18`; the sealed pre-review mutations pass `19/19`; after adding
exercised guards for both accepted caveats, the current post-review mutations pass `21/21`. These
certify artifact, algebra, scope, and validator sensitivity. They do not replace fresh adversarial
semantic review.

The caveats are exact and bounded. The caustic detector uses sign changes of `det(D)` and can in
principle miss an even-multiplicity tangential zero, although hostile dense sampling found
`dr/ds >= 0.9654696034` and post-origin `sigma_min(D) >= 1.4884168151e-4` on every sealed row. The
bundle verifier independently reconstructs the endpoint Jacobi columns without Riemann/Jacobi
assembly, but shares SciPy, float64, profiles, the endpoint affine time, and endpoint screen
projection; it does not independently certify screen transport or endpoint selection.

## Authority boundary

This return is a finite-path control atlas, not a CMB prediction. It does not choose the physical
profile, endpoint, source scale, operator/boundary phase, population, TT power, polarization,
`X_max`, action, source law, bootstrap tuning, dynamics, or local signalling interpretation.

## Next gate

Re-ponder the CMB query architecture to decide whether the next bounded missing object is profile
ownership, endpoint ownership, or source/state structure. Do not select a control profile or
restart FD2 merely because this atlas is regular.
