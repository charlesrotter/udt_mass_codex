# G69 profile–endpoint–source identifiability atlas — preregistration

Date: 2026-08-11

Base commit: `b39bce04a77055e685662d4364fbf851e88c2ef0`

Mode: `MAP -> OBSERVE -> PONDER`; metric-led saved-field recomputation plus exact linear algebra;
CPU float64; no new ODE solve, fit, eigensolve, or GPU work

## Whole question

Within the exact G68 finite-path control universe, can the observer-sky Jacobi map distinguish a
change of complete metric profile from a change of endpoint surface? If the geometric map is
known, can a scalar or tensor sky covariance identify either choice without an independently
owned source/state covariance?

The calculation will separate three questions that must not be conflated:

1. **geometric sensitivity:** do the saved finite maps change with profile and endpoint?;
2. **geometric identifiability:** are those changes locally independent inside this control tile?;
3. **observational identifiability:** can an observed sky covariance select the map when its input
   source covariance is unrestricted?

This is an ownership and identifiability atlas. It does not select a physical profile, endpoint,
last-scattering surface, source, spectrum, or parameter value.

## Frozen universe

Use all `21` G68 profiles and only the already saved `501`-sample trajectories in
`FINITE_PATH_SAMPLES.npz`. No G68 trajectory will be reintegrated or filtered.

Interrogate exactly the endpoint grid

```text
x = r/R in {0.30, 0.35, ..., 1.00}
```

for `15` endpoint surfaces and `21 x 15 = 315` profile/endpoint cells. The G68 start remains
`x=0.25`. Each crossing state is reconstructed by monotone cubic interpolation of the saved state
against its saved radial coordinate. The official `x=1` G68 endpoint is the interpolation
regression check. All endpoint surfaces remain `CHOSE_CONTROL`; none is last scattering or
`X_max`.

For every cell compute from the same complete saved state:

- affine depth `s`;
- complete `2 x 2` screen Jacobi map `D`;
- `det(D)`, singular values, logarithmic anisotropy `log(sigma_max/sigma_min)`, and polar rotation;
- endpoint azimuthal carry `psi`;
- matched-F01 area residual `det(D)/s_F01(a,x)^2 - 1`, using the F01 row with the same lapse label
  and endpoint.

No source population or CMB observable is inserted into these geometric readouts.

## Bounded local sensitivity test

For each F02 shape separately, form coarse finite-difference sensitivity columns for
`(endpoint x, lapse a, mixing epsilon)` at the registered central lapse `a=0` and between the two
registered positive amplitudes `epsilon=1/20,1/5`. Use only registered cells:

- endpoint derivative: centered `Delta x=0.05` wherever both neighbours exist;
- lapse derivative: centered endpoints `a=-1/4,+1/4`;
- amplitude secant: `epsilon=1/20` to `1/5`.

The readout vector is

```text
y = (log(det(D)/s_F01^2), log(sigma_max/sigma_min), psi).
```

Report the raw `3 x 3` sensitivity matrix, its singular values, determinant, and scale-normalized
condition number at `x in {0.35,0.50,0.65,0.80,0.95}`. Because the amplitude column is a secant and
the parameter spacing is coarse, numerical full rank is only `OBSERVED` local control-tile
separation—not a theorem of physical identifiability.

## Exact source-covariance degeneracy test

For an invertible geometric transfer `D`, the generic covariance readout is

```text
C_obs = D C_src D^T.
```

For each positive-definite test covariance `C_obs` and every invertible G68 `D`, construct

```text
C_src = D^{-1} C_obs D^{-T}
```

and verify exact reconstruction and positive definiteness numerically. Use the three frozen
dimensionless observed-covariance controls

```text
I,
diag(2,1),
[[2,1/3],[1/3,1]].
```

These are algebra controls, not observed CMB covariances. The analytic congruence identity, not the
chosen examples, carries the conclusion: an unrestricted source covariance can absorb any
invertible geometric transfer. Singular maps will be separately classified and cannot be inverted.

## Observational-anchor policy

No observational coefficient is fitted in G69. A later explicitly authorized anchor phase may use
a small preregistered parameter vector only after this atlas identifies its rank and source
dependencies. Each coefficient must have one declared owner and one primary anchor; at least one
independent observable or regime must remain held out. The conditional P1 SNe result may constrain
only a low-redshift observer-pair profile after a CMB pair profile exists. CMB peak positions,
heights, and polarization cannot be treated as interchangeable anchors, because they read different
geometric and source/state channels. Parameter count may not be increased after residual inspection.

## Premise and scope ledger

- G68 profiles, paths, query, screen, and saved states: `CHOSE_CONTROL`, frozen inputs.
- `c_E`: `OBSERVED` clock/ruler calibration, dimensionless unit convention here.
- endpoint grid and covariance controls: `CHOSE_CONTROL`, preregistered above.
- Jacobi-map reconstruction and covariance congruence: `DERIVED` from the supplied metric/query and
  linear algebra.
- numerical sensitivity rank: `OBSERVED` only within the registered finite tile.
- physical CMB profile, endpoint, source/state covariance, spectrum, and polarization law: `OPEN`.
- P1 SNe profile: `CONDITIONAL` low-redshift cross-anchor and inactive in the computation.
- `X_max`: `WORKING` observer-pair asymptotic guard and inactive.
- action, native source law, bootstrap, time-live history, local signal law: `OPEN` and inactive.

Outside scope: unregistered profiles, other endpoints, non-equatorial or time-live queries, other
metric branches, singular maps, a last-scattering model, population physics, mode operators,
TT/TE/EE/BB spectra, fitting, action/source derivation, bootstrap activation, and local signalling.

## Certification and falsification

The package fails closed if:

1. any of the 21 saved profiles or 15 endpoints is omitted or duplicated;
2. a new solve silently replaces the saved trajectories;
3. interpolation fails to reproduce every official `x=1` endpoint `D` within `2e-8` relative;
4. an F01 cell has anisotropy or polar rotation above `2e-10`;
5. source-covariance reconstruction exceeds `2e-10` relative or loses positive definiteness;
6. a rank observation is promoted to physical parameter selection;
7. arbitrary source covariance is treated as physically owned;
8. an observational anchor, fit, last-scattering surface, or `X_max` value is inserted.

The independent verifier must reconstruct the cell census and covariance identity without importing
the production atlas builder. Mutation catches must exercise the census, endpoint regression,
source-degeneracy, scope, and anchor-policy gates.

## Allowed landings

Exactly one primary landing:

1. `GEOMETRICALLY_SEPARATING__OBSERVATIONALLY_SOURCE_DEGENERATE`;
2. `PROFILE_ENDPOINT_GEOMETRIC_DEGENERACY_OBSERVED`;
3. `SINGULAR_MAPS_BLOCK_GENERIC_COVARIANCE_INVERSION`;
4. `IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`;
5. `SAVED_FIELD_OR_QUERY_FAILURE`.

Maximum conclusion: a bounded profile/endpoint sensitivity map and an exact statement of what an
unrestricted source covariance prevents observations from identifying. No physical coefficient,
profile, endpoint, source, spectrum, action, bootstrap result, or dynamics follows.
