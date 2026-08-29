# G292 preregistration — orientable screen differential-character descent

Date: 2026-08-28
Outcome status: `FROZEN_BEFORE_DERIVATION_OR_WITNESS_EXECUTION`

## Candidate exact statements

For a supplied smooth oriented positive rank-two screen bundle `S -> W` and its G290 metric
connection `D`:

1. closed-loop holonomy and curvature define a degree-two differential character;
2. up to the frozen orientation convention,
   `[F_D/(2 pi)] = e(S)` and closed oriented two-cycle periods are integral;
3. a smooth fixed-rank continuation over `W x I` preserves that characteristic class;
4. after identifying two oriented metric screen bundles isometrically, their connections differ by
   `b J`, so their curvatures differ by `db` and retain the same Euler class;
5. full thin-path holonomy reconstructs the supplied connection up to gauge but does not select it;
6. on the G225 complete celestial sphere, `S = TS^2` and the Euler number has magnitude two;
7. a supplied direction map/bundle isometry is required before calling that celestial connection
   the same object as a G290 pair-base connection.

## Frozen global metric witness

On

`M = R_t x R_z x S^2`, take the free family

```text
g_(R,epsilon) = -c_E^2 dt^2 + dz^2
                + R^2 exp(2 epsilon cos(theta)) q_unit,
R > 0, epsilon in R.
```

Use the supplied `t-z` null pair direction and the oriented `TS^2` screen. The preregistered target
calculations are:

```text
terminal completed-pair Phi = 0 for every R,epsilon
F_epsilon = (1 + 2 epsilon cos(theta)) dA_unit       [up to orientation sign]
integral_(S^2) F_epsilon = 4 pi                      [same sign convention]
Delta cap flux(theta_0) = 2 pi epsilon sin(theta_0)^2
```

The family is to be checked for smoothness, positive screen metric, completeness, and global
hyperbolicity. `R` and `epsilon` are `free-and-explored`; no numerical value is physically pinned.
`c_E` is `OBSERVED`. The unit sphere is the G225 normalized direction sphere, not a physical-radius
choice; `R` retains the free dimensionful screen scale in the product witness.

## Certification contract

Production must derive the screen connection and curvature directly from the metric/coframe, not
assume the conformal-curvature formula as the tested conclusion. Independent verification must use
a separately typed connection/curvature calculation and numerical quadrature across positive and
negative `epsilon`, multiple `R`, and loops away from coordinate poles.

The following hostile claims must fail:

1. local flux is fixed by the Euler number;
2. a single loop phase uniquely determines unwrapped flux;
3. scalar reciprocal closure forces screen holonomy to be identity;
4. the G225 sky connection and a G290 pair-base connection are automatically identical;
5. smooth characteristic-class persistence is a physical dynamics/conservation law;
6. the orientable calculation closes nonorientable reflection/twisted-Euler strata;
7. nonintegral total curvature is admitted as a connection on the claimed `TS^2` bundle;
8. a fixed topological class selects one metric history.

## Candidate landings

1. `ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY__SAME_CLASS_METRIC_HISTORY_FREEDOM_SURVIVES`
2. `ONLY_LOCAL_OR_RECONSTRUCTIVE_IDENTITIES_RECOVERED__G291_GLOBAL_LEAD_NOT_ESTABLISHED`
3. `GLOBAL_METRIC_WITNESS_FAILS__CONNECTION_LEVEL_RESULT_ONLY`
4. `DERIVATION_OR_CERTIFICATION_DEFECT__NO_SCIENTIFIC_LANDING`

## Evidence gates and maximum claim

- preregistration banked before witness execution;
- bounded orientable stratum stated rather than promoted to the whole `O(2)` arena;
- production, independent implementation, and hostile catches must agree;
- premise and native-provenance audits must pass;
- any missing gate yields `LEAD` or `VERIFIED_WITH_CAVEATS`.

At most G292 can close the conditional orientable topology/continuous-connection split. It cannot
derive physical flux evolution, a unique metric history, population, mass, observation, scale,
`X_max`, source, action, or field equation.
