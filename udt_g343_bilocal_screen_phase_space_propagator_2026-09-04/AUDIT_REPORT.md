# G343 audit report

Date: 2026-09-04
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Result

The exact G341/G342 metric supplies a regular bilocal `4 x 4` screen phase-space propagator for all
positive endpoint pairs, all projective directions, and every separately retained compact lift.
In one affine gauge it composes exactly, is symplectic, and reverses by matrix inverse. Separately
unit-frequency endpoint normalizations are related by a derived conjugation whose position block
carries the metric frequency ratio.

## Four evidence gates

1. **Preregistered:** yes, commit `3f182b86`; dimensional chart repair and discarded-run note fixed
   before the corrected execution in commit `71db75f4`.
2. **Scope complete:** yes for every endpoint order and direction in the one supplied exact
   G341/G342 null-ray tile; not generic spacetime or nonlinear congruence stability.
3. **Independently verified:** yes within the bounded premise. Production `8888/8888`;
   implementation-distinct direct metric/Riemann/RK/fundamental-basis route `2960/2960`; hostile
   `13/13`; fresh external review authenticated 29 sealed payloads, replayed `19/19`, ran a separate
   25-case scratch reconstruction, found no issue at any severity, and accepted without repair.
4. **Premises audited:** yes locally. Supplied spacetime, reference event, affine gauge, observer,
   and path label remain explicit; no optical transfer, distance, population, matter, scale,
   `X_max`, or canon premise enters.

## Important repair history

The initial implementation used an implicit normalized `T_*=1` chart. Even though its identities
passed, the presentation could add unlike dimensionful quantities and hide a preferred scale. Those
runs were discarded. The corrected chart uses `rho=T_*^2/(T_*^2+lambda^2)` and explicitly verifies
reference-event covariance. A first corrected-chart replay then exposed a missing factor `T_0` in
the independent G342 old-chart comparison; the propagator itself passed. That comparison was
repaired and the failure is preserved in `PREREGISTRATION_EXECUTION_NOTE.md`.

## Maximum conclusion

`EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED` geometric phase-space transport on one supplied
exact spacetime. This package changes no metric,
kernel, angular sector, response equation, or premise adoption and selects no universe, topology,
route, population, observation, matter/mass, scale, `X_max`, stability, or canon.
