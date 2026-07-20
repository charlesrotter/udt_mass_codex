# Preregistration — Extended Continuation of the 22 Open C2 Homotopy Paths

Date: 2026-07-20

Base: `99c57d7800eee2f9f2ebabff34dc6d17a18ed847`

## Question and frame

The failed-basin homotopy audit certified 29 additional round endpoints and left exactly 22
order-four paths at positive artificial forcing after the registered 180-second limit.  This audit
continues those exact paths from their last fully replayed coefficient/tangent checkpoints.  It asks
whether they reach the unchanged `F(q)=0` endpoint, form a numerically closed homotopy loop, run into
a registered numerical safety boundary, or remain unresolved after a much longer arclength.

This is **solver housekeeping**, not a new physics mechanism.  The frame remains the conditional
metric-only four-dimensional stationary toric `C^2` `N,H,S,W` tile.  It is not the physical
finite-cell boundary, nontoric geometry, genuine time evolution, matter, or the whole metric space.

## Frozen inputs

- `c2_failed_basin_homotopy_2026-07-20/RAW_HOMOTOPY_PATHS_COMPLETE_LEDGER.json`, SHA-256
  `1a8da008545be0a65d9f25899219a9334e4afd0692d5ef1bb7b67b95a817b2e8`;
- its exact 22 `PATH_TIME_LIMIT` identities, original `q0`, final accepted coefficient state,
  positive `lambda`, and stored tangent;
- parent raw stationarity input SHA-256
  `0671c58e9684390ce82fa136dc9d2986337efcf5edc63453ecabe3b802197d55`;
- the same metric, action, homotopy `F(q)-lambda F(q0)=0`, 48-node raw equation, `1e-9` path/endpoint
  gate, `1e-7` higher-order validation gate, and `1e-6` round classification.

No open path may be dropped or stopped because its shape or direction appears unpromising.

## Premises

- `CONDITIONAL`: metric-only pre-scale `C^2` action and reciprocal-toric smooth-cap domain.
- `FREE_AND_EXPLORED`: all 22 exact open checkpoints.
- `NUMERICAL_CONTROL`: restart tangent, pseudo-arclength corrector, exact-Hessian refresh, parallel
  CPU scheduling, loop detector, arclength/time/safety limits.
- `OPEN_NOT_ENTERED`: physical boundary, topology selection, carrier/source, backreaction, time-live
  law, scale, `c`, `G`, `X_max`, and mass.

The continuation parameter and its folds have no physical interpretation.

## Extended controls

- restart each path from its final accepted full coefficient vector and positive `lambda`;
- recompute `F(q0)`, the restart residual, and an exact automatic-differentiation Hessian;
- orient the restart tangent continuously with the final stored parent tangent;
- retain full coefficients, tangents, actions, corrector histories, rejected steps, and refreshes;
- CPU float64, eight isolated single-thread worker processes;
- inherited step range `0.002` to `0.10`, corrector gate `1e-9`, at most 12 corrector iterations and
  eight halvings, exact Hessian at least every two accepted points;
- per path: at most 500 additional accepted points, additional arclength `20`, coefficient norm `5`,
  absolute artificial `lambda` `5`, or 900 seconds;
- global wall budget 3,600 seconds, processing all 22 paths in interleaved batches;
- all limits are numerical characterization gates, not physical cutoffs.

A numerically closed loop candidate requires a current state within `1e-5` Euclidean distance in
`(q,lambda)` of a stored state at least 20 accepted points earlier, tangent dot product above
`0.999`, and raw homotopy residual at most `1e-9`.  This class means only that the artificial
continuation appears to cycle; it is not a physical periodic solution.

At a `lambda=0` crossing, solve the original stationarity equation and apply the inherited raw,
higher-order, round-cluster, and nonround direct-Bach gates.  Any failed endpoint gate remains open.

## Outcome classes and ceiling

- `ROUND_ENDPOINT`: original equation reached and certified round.
- `NONROUND_FULL_BACH_ENDPOINT`: conditional nonround stationary candidate.
- `REDUCED_ENDPOINT_ONLY`: reduced root fails the direct Bach gate.
- `CLOSED_HOMOTOPY_LOOP_CANDIDATE`: artificial path cycles under the registered detector.
- `COEFFICIENT_OR_LAMBDA_SAFETY_LIMIT`, `MINIMUM_STEP_STALL`, `ARCLENGTH_LIMIT`, or
  `PATH_TIME_LIMIT`: characterized but unresolved.

Maximum conclusion:

`EXTENDED_22_PATH_CONDITIONAL_C2_HOMOTOPY_CHARACTERIZED`.

Even 22 round endpoints would strengthen only this bounded conditional tile; it would not establish
global uniqueness, make `C^2` native, select a coframe/section/boundary, or derive matter.  No GPU,
canonization, startup edit, repository reorganization, or matter-action continuation is authorized
by this preregistration.
