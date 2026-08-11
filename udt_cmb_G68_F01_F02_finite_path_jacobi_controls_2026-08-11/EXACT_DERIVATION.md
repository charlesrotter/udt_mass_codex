# G68 exact finite-path observer-sky Jacobi control atlas

Date: 2026-08-11

Primary landing: `FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE`

Evidence grade after fresh sealed adversarial review:
`VERIFIED_WITH_CAVEATS`

## 1. Scope

This is the complete result over the exact `21`-row analytic control universe frozen before any
trajectory was inspected. It is not a function-space census and does not select a physical metric,
profile, endpoint, CMB screen, or source.

This is not a CMB prediction.

In units `R=c_E=1`, the controls are

```text
ds^2 = -A(r)dt^2 + dr^2/A(r) + r^2(dtheta^2+sin^2(theta)dpsi^2)
       + 2h(r)sin^2(theta)dt dpsi,

A=1+a r^2,
a in {-1/4,0,+1/4},
h=epsilon r^2 f(r),
f in {1,(1-r)^2,1-2r},
epsilon in {1/20,1/5},
```

plus the matched `h=0` F01 rows. The query starts at `r=1/4`, `theta=pi/2`, with the G67
future/outward null direction and parallel screen, and ends at the first outward crossing of
`r=1`. The latter is a control surface, not `X_max` or last scattering.

## 2. Full finite system

For each supplied profile, the production code constructs the metric, its analytic first and
second derivatives, the full Levi-Civita connection, and

```text
R^rho_(sigma mu nu)
 = partial_mu Gamma^rho_(nu sigma)-partial_nu Gamma^rho_(mu sigma)
   +Gamma^rho_(mu lambda)Gamma^lambda_(nu sigma)
   -Gamma^rho_(nu lambda)Gamma^lambda_(mu sigma).
```

It integrates, without a local Taylor replacement,

```text
dx^rho/ds = k^rho,
dk^rho/ds = -Gamma^rho_(mu nu) k^mu k^nu,
dE_A^rho/ds = -Gamma^rho_(mu nu) k^mu E_A^nu,
dJ_B^rho/ds = P_B^rho-Gamma^rho_(mu nu)k^mu J_B^nu,
dP_B^rho/ds = -Gamma^rho_(mu nu)k^mu P_B^nu
              -R^rho_(sigma mu nu)k^sigma J_B^mu k^nu,
```

with `J_B(0)=0`, `P_B(0)=E_B`. The finite screen map and its covariant derivative are

```text
D_AB = g(E_A,J_B),
Ddot_AB = g(E_A,P_B).
```

The local connection/Riemann engine reproduces the exact G67 `T_F01=0` and full F02 `tau`
polynomial on all `21/21` initial jets before finite integration.

## 3. Complete outcome census

All `21/21` registered IVPs reached `r=1`:

```text
ENDPOINT_REGULAR_NO_CAUSTIC = 21
turning events               = 0
post-origin Jacobi caustics  = 0
solver/regularity failures   = 0
```

This is a result only for the bounded analytic ensemble and fixed equatorial outward query. It is
not a theorem that F02 or the complete UDT metric has no turning, caustic, cut, or alternate branch.

The minimum sampled lapse is `0.75`; the minimum sampled regular `t-psi` block quantity
`A r^2+h^2 sin^2(theta)` is `0.0615234375`.

## 4. F01 exact controls

For all three F01 lapse profiles, stationarity and nullity give constant outward radial derivative

```text
dr/ds=sqrt(A(r0)).
```

Therefore

```text
s_end = (1-1/4)/sqrt(A(1/4)),
D_end = s_end I.
```

The three numerical maps reproduce this result with maximum registered relative error
`8.08e-15`.

## 5. Finite F02 structure in the frozen ensemble

Every F02 endpoint map is diagonal within numerical error in the parallel transported registered
screen. Across the 18 rows:

```text
matched-F01 fractional area change:
    -5.8161423988e-5  to  +1.1444462381e-2

diagonal anisotropy (D_theta_theta-D_psi_psi)/mean diagonal:
    +1.7322331460e-5  to  +4.6476035742e-3

endpoint azimuthal carry psi:
    -1.2946143791e-1  to  +6.6524950428e-2

max endpoint antisymmetric-map norm: 3.81e-24
max polar rotation magnitude:         1.44e-20.
```

The persistent-mixing controls have positive area change, the endpoint-tapered controls have small
negative area change, and the sign-changing controls have positive area change in all three lapse
families at both registered amplitudes. Thus the finite area correction is not owned by local
mixing amplitude alone; it reads the complete profile history. A one-axis shear survives every
nonzero registered F02 row, while no finite screen rotation appears on this equatorial stationary
control query.

That zero-rotation observation is not a general polarization result. Non-equatorial screens,
general angular structure, time-live geometry, path holonomy, and spin-sensitive source/state data
remain outside this slice.

## 6. Weak mixing and reflection

For all nine lapse/shape pairs, auxiliary endpoint-map errors relative to matched F01 decrease when
`epsilon` is halved from `1e-2` to `5e-3`. The large/small error ratios lie between

```text
3.9998673827 and 3.9999959216.
```

Thus the finite map approaches F01 quadratically throughout this auxiliary ensemble, matching the
local G67 parity result without imposing a fitted exponent.

For every `18/18` F02 row, the complete negative-mixing run obeys the coordinate reflection
`psi -> -psi` and screen conjugation

```text
D(-h)=S D(+h) S,  S=diag(1,-1),
```

with maximum coordinate discrepancy `2.67e-15` and maximum map discrepancy `3.36e-15` relative.

## 7. Numerical and independent evidence

Maximum production residuals across the complete registered universe are

```text
null                         1.49e-15
screen Gram                  7.55e-15
screen-ray orthogonality     2.50e-16
Jacobi Wronskian             2.77e-33
optical-tidal antisymmetry   6.69e-32
stationary p_t conservation  1.67e-15
axial p_psi conservation     1.93e-16.
```

The maximum endpoint-map disagreement is `1.05e-14` between production/refined DOP853 and
`1.48e-14` between refined DOP853 and RK45.

The independent verifier does not construct Riemann or integrate the Jacobi equation. It uses a
separate direct-loop Christoffel implementation and central finite differences of null geodesic
families for both screen directions at both preregistered deltas on all `21/21` rows. Its maximum
fine-delta disagreement with the production Jacobi map is `8.93e-11`; coarse/fine bundle
disagreement is `1.78e-10`.

This is a strong cross-check of the endpoint Jacobi columns, but not fully separate verification of
screen transport or endpoint selection. It shares the declared metric/query, float64 arithmetic,
SciPy, analytic profile ensemble, production endpoint affine time, and production endpoint screen
basis used for projection.

The caustic detector searches for sign changes of `det(D)` and could in principle miss an
even-multiplicity tangential zero. The sealed controls do not approach that ambiguity: fresh hostile
dense sampling found `dr/ds >= 0.9654696034` and post-origin
`sigma_min(D) >= 1.4884168151e-4` throughout all `21` rows.

## 8. What changed—and what did not

The local sky-map result now extends to an explicit finite map for every member of one complete
control ensemble. It demonstrates that the angular/mixing sector can accumulate into profile-
dependent area, shear, and azimuthal carry even when the local and finite screen-rotation channels
remain zero on this query.

The observer-sky Jacobi map is therefore a viable geometric replacement for an unexplained affine
projection *once* a physical profile, endpoint, and source scale are supplied. This calculation
does not supply those objects. It also does not produce the historical mode-ladder offset, TT
power, peak heights, or polarization.

## 9. Completeness and maximum conclusion

This is one stationary/equatorial observer-query tile. It keeps all four spacetime coordinates in
the geodesic/bundle calculation, all complete F02 mixing terms, and every preregistered profile
outcome. It does not solve a native action, field equation, source, boundary selection, topology,
time-live history, physical branch selection, or stability problem.

`FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE` is therefore the maximum bounded
landing. No physical F01/F02 selection, CMB scale, last-scattering surface, peak prediction,
polarization result, local signal law, `X_max` value, action, source, bootstrap result, or dynamics
follows.
