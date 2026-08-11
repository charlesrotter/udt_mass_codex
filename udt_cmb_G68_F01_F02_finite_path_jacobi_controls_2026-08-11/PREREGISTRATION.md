# G68 F01/F02 finite-path observer-sky Jacobi controls — preregistration

Date: 2026-08-11

Base commit: `de3f8e922ac852ce92e92b22a124afcb09bf1dd1`

Mode: `MAP -> OBSERVE`; metric-led after explicitly `CHOSE` control profiles; CPU float64 plus
independent geodesic-bundle checks; no fit or eigensolve

## Whole question

For the already verified observer-sky query, what finite-path geodesic, parallel-screen, and Jacobi
maps occur across a small preregistered ensemble of complete analytic F01/F02 control profiles?
Which runs reach the declared control endpoint, turn, encounter a caustic, or leave the regular
chart? How do endpoint area, shear, possible screen rotation, and azimuthal carry vary across the
whole frozen ensemble?

This observes the supplied metrics. It does not choose F01 or F02, a physical CMB profile, a last-
scattering surface, or a source population. Profile dependence is an output, not a nuisance to be
tuned away.

## Bounded profile universe

Use dimensionless `x=r/R` on `x in [1/4,1]`. `R` is a declared numerical comparison scale and is
set to one in the solver; it is not `X_max`, a fitted distance, or a physical CMB endpoint. Algebra
uses `c_E=1`, with `c_E` remaining the observed clock/ruler calibration and dimensions restorable.

The complete frozen cross-product is in `PROFILE_UNIVERSE.tsv`:

```text
A_a(x) = 1+a x^2,                      a in {-1/4,0,+1/4};
h(x)   = epsilon R x^2 f(x),
f_P=1,  f_T=(1-x)^2,  f_S=1-2x,
epsilon in {1/20,1/5};
h=0 as the matched F01 control.
```

There are exactly `3 F01 + 18 F02 = 21` rows. All `A`, `h`, endpoint, start, amplitude, and shape
choices are `CHOSE_CONTROL`, frozen before trajectory inspection. They are not pinned by theory or
habit and will not be fitted. The three `h` shapes deliberately retain persistent, endpoint-
tapered, and sign-changing profile behavior; no row may be removed for producing an unattractive,
singular, turning, or caustic outcome.

The ensemble is a bounded slice of function space, not a complete profile census. It releases
background-lapse curvature, mixing strength, and mixing-jet shape only inside the stated analytic
family. General angular screens, non-equatorial queries, time-dependent profiles, physical source
states, other metric branches, and all unregistered profiles remain outside scope.

## Identical query and endpoint policy

For every row start at

```text
p=(t=0,r=R/4,theta=pi/2,psi=0)
```

with the same metric-derived tetrad, future/outward `k=u+n`, parallel screen, and two Jacobi fields
defined in the G67 package. Integrate the full nonlinear coordinate geodesic, both parallel screen
vectors, and the two first-order Jacobi systems. No local Taylor truncation is used as the finite
map.

The endpoint is the first outward crossing of the declared control surface `r=R`. Continue through
a Jacobi caustic while the metric/geodesic system remains regular, but record the first post-origin
zero of `det(D)`. If `dr/ds` reaches zero before the endpoint, record the turning event and continue
the unique IVP until endpoint, regularity loss, or the numerical affine cap. The cap `s/R=10` is a
category-A bounded-computation stop, not a physical boundary. Return the outcome rather than
filtering it.

The fixed initial-value query supplies one local branch per profile until ordinary ODE uniqueness
fails. It does not claim to enumerate other endpoint-connecting geodesics or cut-locus branches.
Cut/focal behavior is reported through endpoint multiplicity where observed and Jacobi rank loss;
it is not repaired by selecting another route.

## Premise ledger

- F01/F02 metric forms: `CHOSE` controls inherited unchanged from G67.
- `c_E`: `OBSERVED` clock/ruler calibration; unit convention only.
- `R=1`, `x0=1/4`, `x1=1`, lapse coefficients, mixing shapes, and amplitudes:
  `CHOSE_CONTROL`, frozen in `PROFILE_UNIVERSE.tsv`, not physical values.
- equatorial event, outward sign, stationary observer, screen orientation: `CHOSE` identical query
  controls inherited from G67.
- geodesic, parallel transport, Riemann curvature, and Jacobi equations: `DERIVED` from each
  supplied metric.
- endpoint/turn/caustic return policy: `CHOSE_CONTROL` classification protocol; it characterizes
  rather than accepts/rejects solutions.
- solver method, tolerances, dense sampling, and affine cap: category-A numerical controls.
- P1 SNe profile: `CONDITIONAL` low-redshift pair anchor and inactive here.
- `c_eff^(pair)`: `CONDITIONAL` terminal inter-observer readout and inactive here; never a local
  propagation speed.
- `X_max`: `WORKING` observer-pair asymptotic guard and inactive; `r=R` is not `X_max`.
- co-presence: `POSIT` interpretation; no signalling inference.
- physical profile, endpoint, screen, source/state covariance, population, boundary/operator phase,
  action, bootstrap, and native dynamics: `OPEN` and inactive.

## Required outputs

For all `21/21` rows record:

1. endpoint status and affine length, endpoint coordinates, conserved quantities, and any radial
   turning or regularity event;
2. the complete `2x2` endpoint Jacobi matrix, determinant, singular values, area factor, symmetric
   shear, antisymmetric part, and first caustic if any;
3. maximum null, screen Gram, screen-to-ray orthogonality, Jacobi Wronskian, and optical-tidal
   symmetry residuals along the path;
4. convergence under two registered tolerance levels and at least one second integration method;
5. exact F01 `D=sI` agreement and numerical `epsilon -> 0` convergence for every lapse/shape;
6. the exact `h -> -h` coordinate-reflection relation on a preregistered subset;
7. an independent finite-difference geodesic-bundle reconstruction of selected endpoint Jacobi
   columns, using null initial directions `u+n cos(delta)+E_B sin(delta)` and central differences.

## Numerical certification

Production uses float64 `solve_ivp(DOP853)` with `rtol=1e-10`, `atol=1e-12`, dense output, and
bounded `max_step<=R/200`. Convergence control uses `rtol=2e-12`, `atol=2e-14`,
`max_step<=R/400`. A second-method check uses `RK45` at the convergence tolerances. These are
category-A controls and may be tightened if they fail, but the profile universe and conclusion
rules may not be changed after inspection.

Certification targets, normalized where applicable:

```text
max null residual                  <= 2e-8
max screen Gram residual           <= 2e-8
max screen-ray orthogonality       <= 2e-8
max Jacobi Wronskian residual      <= 2e-7
max optical-tidal antisymmetry     <= 2e-8
DOP853 production/refined endpoint <= 2e-7 relative
DOP853/RK45 endpoint               <= 2e-6 relative
bundle/Jacobi selected columns     <= 2e-4 relative after delta convergence
F01 exact endpoint map             <= 2e-8 relative
```

Failure of a numerical target gives `NUMERICALLY_UNRESOLVED` for that row; it does not erase the
trajectory. Refinement may change only category-A controls and must be fully recorded.

## Falsification and allowed landings

The package fails closed if a profile is missing/duplicated/retuned, the query differs between
controls, any mixing component is suppressed, a caustic/turning/singular row is discarded, local
Taylor data is substituted for the integrated map, or a control becomes a physical CMB choice.

Exactly one primary landing will be used:

1. `FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE`;
2. `FINITE_PATH_CONTROL_ATLAS_MIXED_REGULAR_TURNING_OR_CAUSTIC`;
3. `FINITE_PATH_F02_CONTROLS_DO_NOT_REACH_ENDPOINT_IN_DECLARED_SLICE`;
4. `FINITE_PATH_QUERY_OR_REGULARITY_FAILURE`;
5. `FINITE_PATH_NUMERICALLY_UNRESOLVED`.

Maximum conclusion: a finite-path classification of this exact `21`-row control ensemble and a
tested account of which sky-map features are endpoint-, profile-, or branch-dependent. No physical
F01/F02 selection, CMB scale, peak position/height, polarization prediction, last-scattering
surface, local signal law, `X_max` value, action, source, bootstrap result, or dynamics follows.
