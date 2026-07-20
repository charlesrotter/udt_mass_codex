# Preregistration — Conditional C2 Failed-Basin Homotopy

Date: 2026-07-20

Base: `33eaed961d4601019ee59df5ee8aa59fdc105353`

## Whole question and bounded frame

The preceding nonlinear stationary census completed all 198 registered starts in the conditional
metric-only four-dimensional `C^2` tile.  It certified 147 returns to the round gauge-fixed orbit and
preserved 51 starts as `NO_RESIDUAL_DECREASING_NEWTON_STEP`.  This audit asks whether an artificial
continuation can carry each of those exact 51 starts to the unchanged stationarity equation and, if
so, whether its endpoint is round or a distinct reduced root.

This is **observing**, not targeting.  Every fold, reversal, runaway, stalled path, round endpoint,
and nonround endpoint is retained.  The audited frame is the same bounded stationary,
torus-invariant, cohomogeneity-one `N(eta), H(eta), S(eta), W(eta)` family at polynomial orders two
and four in `GENERAL`, `SEAL_EVEN`, and `SEAL_ODD_W`.  It is not the whole metric solution space.

## Frozen inputs

- `c2_nonlinear_stationary_solution_space_2026-07-20/RAW_ATTEMPTS.json`, SHA-256
  `0671c58e9684390ce82fa136dc9d2986337efcf5edc63453ecabe3b802197d55`;
- its exact 51 non-passing attempt identities and registered initial coefficient vectors;
- the metric, gauge, action integrand, quadrature, and raw stationarity implementation banked at the
  base commit;
- solve gate `1e-9`, doubled-grid/two-extra-degree validation gate `1e-7`, and branch-cluster distance
  `1e-5`.

No seed may be omitted because it appears unattractive, redundant, divergent, or difficult.

## Premise ledger

- `PINNED_BY_THEORY` within the frozen conditional action class: four-dimensional covariance and the
  complete nonlinear metric dependence retained by the declared `C^2` bulk functional.
- `CONDITIONAL`: metric-only `C^2` is unique only under the frozen pre-scale variation/locality/
  derivative premises.  It is not promoted to the native UDT action.
- `CONDITIONAL`: the reciprocal-toric smooth-cap domain and its local CSN coordinate realization.
  Its caps are a mathematical domain, not an adopted physical finite-cell wall.
- `FREE_AND_EXPLORED`: all 51 frozen failed starts, all three parity sectors, and both spectral
  orders.
- `NUMERICAL_CONTROL`: the artificial homotopy, step controls, Broyden updates, exact-Hessian
  refreshes, stopping limits, and clustering tolerances below.  They carry no physical meaning.
- `OPEN_NOT_ENTERED`: physical boundary polarization, global topology selection, unrestricted
  metric components, time dependence, carrier/source, scale, `c`, `G`, `X_max`, total mass, and
  particle mass.

The artificial continuation parameter is neither UDT depth nor physical time.

## Registered homotopy and continuation

For each frozen start `q0`, let `F(q)` be the raw Galerkin stationarity vector of the unchanged
conditional action.  Trace the zero set

`H(q, lambda) = F(q) - lambda F(q0) = 0`,

starting from the exact constructed point `(q0, 1)`.  Only the `lambda=0` endpoint is a solution of
the original equation.  Intermediate forced points are solver scaffolding and cannot be interpreted
as physics.

Use pseudo-arclength predictor/corrector in `(q, lambda)`.  The initial tangent and corrector use an
exact automatic-differentiation Hessian at `q0`; symmetric Broyden secants may be used between exact
refreshes.  Refresh the exact Hessian at least every eight accepted steps and on the first failed
corrector.  Orient the first tangent toward decreasing `lambda`; thereafter preserve tangent
continuity, allowing genuine folds and temporary `lambda` reversals.

Registered controls:

- CPU float64; 48 Gauss nodes for the path equation;
- initial arclength step `0.05`, minimum `0.002`, maximum `0.10`;
- augmented raw residual and arclength residual at most `1e-9`;
- at most 12 corrector iterations and eight step halvings per accepted point;
- at most 160 accepted steps, arclength eight, coefficient norm five, or 180 seconds per path;
- global wall budget 2,400 seconds, with strata interleaved so a hard stop cannot erase one sector;
- coefficient/arclength limits are numerical overflow and throughput guards, not physical cutoffs.

When a corrected segment reaches or crosses `lambda=0`, perform a constrained `lambda=0` solve of
the original `F(q)=0`.  Preserve the complete path ledger, including rejected steps and exact-Hessian
refreshes.  A path that fails any numerical gate remains unresolved; it is never an absent branch.

## Endpoint certification

Every `lambda=0` endpoint must pass:

1. raw 48-node stationarity norm at most `1e-9`;
2. doubled-grid and two-additional-degree projected norm at most `1e-7`;
3. deterministic clustering at coefficient distance `1e-5`;
4. round classification only when gauge-fixed coefficient norm is at most `1e-6`.

Every nonround reduced endpoint must also receive a direct coordinate Bach-tensor evaluation over
the same full metric, first on 32 interior Gauss nodes and then on 64.  Raw fixed-chart component
norm at most `1e-6` on both grids is the provisional full-equation gate.  Failure leaves a
`REDUCED_ROOT_ONLY`, not a metric solution.  The round endpoint is already an exact full Bach zero
because its Weyl tensor vanishes; its numerical anchor is replayed.

## Outcome branches

1. **All traced endpoints round:** strengthen the broad-round-basin observation for the successfully
   continued starts, while retaining every untraced or stalled path and every outer completeness
   layer.
2. **Distinct full-Bach endpoint:** bank a conditional nonround stationary branch candidate, not a
   unique UDT geometry.
3. **Distinct reduced endpoint failing Bach:** bank the reduction mismatch and do not promote it.
4. **Fold/runaway/stall:** characterize it exactly and preserve the basin as unresolved.
5. **Throughput limited:** report the interleaved completed subset only; do not infer from omitted
   paths.

## Falsification and maximum conclusion

The prior suggestion that the 51 failures are merely difficult routes back to round is falsified by
one certified distinct endpoint.  A full-Bach-pass nonround endpoint falsifies an only-round ruling
inside this bounded tile.

Maximum conclusion:

`FAILED_BASIN_HOMOTOPY_CHARACTERIZED_IN_THE_CONDITIONAL_STATIONARY_TORIC_C2_TILE`.

This audit cannot establish global uniqueness, select a coframe lift or physical boundary, make
`C^2` native, derive genuine time evolution, or derive matter, scale, `X_max`, or mass.  No GPU,
canonization, startup-control edit, repository reorganization, or follow-on solve is authorized by
this preregistration.
