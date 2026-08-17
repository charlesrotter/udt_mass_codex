# G128 external-review adjudication

Date: 2026-08-16

Sealed intake: `/tmp/udt_g128_review_odwiaxsg`

`REVIEW_SCOPE.json` SHA-256:
`b1e3371cdce5033368095f5923eeaf5173c0c5d70e0c4df20e29969c99832dbb`

Reviewed commit: `1275ab72febf0f7df81a4856801b472c65086ff9`

External verdict: `PASS_WITH_REPAIRS`.

## Adjudication

The reviewer found no blocking mathematical or numerical error and independently accepted the
bounded landing `FINITE_PATH_SAME_HISTORY_EMERGENCE_OBSERVED`. It also confirmed that the full
nonlinear null geodesic, parallel screen, and Jacobi phase are propagated from one supplied metric,
that optical shear is read from the propagated Jacobi system, and that no angular law is appended.

Two implementation-compliance repairs were required:

1. The independent code and prose used `h=1.5e-4` although the preregistration fixed `h=2e-4`.
2. The solvers had no explicit runtime realization of the preregistered radius, pole, positive-scale,
   and nonfinite-state stop policy.

Both are repaired without changing the test arena, histories, query, equations, integration
interval, solver tolerances, thresholds, candidate landings, or maximum conclusion:

- the independent route now uses the preregistered `h=2e-4`;
- both implementations install terminal events at `R=0.08` and `|sin(theta)|=0.2`;
- both reject nonfinite states and nonfinite/nonpositive `N,L` at runtime;
- neither boundary event fires in the declared atlas.

The corrected production replay retains 29/29 gates and the same landing. The corrected independent
route retains 7/7 gates, with maximum endpoint-Jacobi disagreement `1.263e-11`, phase disagreement
`2.442e-15`, and null/screen drift `3.997e-15`. Package verification now exercises the guard
functions directly in addition to replaying both implementations.

## Status after repair

`EXTERNALLY_REVIEWED_PASS_WITH_REPAIRS__REPAIRS_IMPLEMENTED_AND_INTERNALLY_REPLAYED__FINITE_PATH_SAME_HISTORY_SCREEN_EMERGENCE_OBSERVED__FOLLOWUP_REVIEW_OPEN__PHYSICAL_HISTORY_NONSPHERICAL_COMPLETION_AND_OBSERVATIONS_OPEN`

This is not promoted to an unqualified external `PASS` without a fresh review of the corrected
intake. The chart-local rational half-angle caveat remains explicit, as do all original scientific
scope limits.
