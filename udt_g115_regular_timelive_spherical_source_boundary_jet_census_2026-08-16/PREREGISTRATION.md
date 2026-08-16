# G115 preregistration — regular time-live spherical source-boundary jet census

Date: 2026-08-16

Base: `9e48ff70bf7ff8c4b588fe461226286f8afff34a`

Mode: metric-led exact symbolic CPU jet census; no observation exposure, fit, ODE/PDE history solve,
GPU, action, source dynamics, bootstrap, matter, mass, `X_max`, or physical selection

## Whole question and bounded regime

For the G114 common-source architecture, what does the most general smooth central time-live
spherical metric determine at the first nontrivial radial order about one central observer event?
In particular:

1. what are the radial-null pair block, angular Jacobi phase plane, and mixed block of the same
   observer exponential;
2. which leading coefficients are metric-history data and which are observer/source-query data;
3. how do point-event, resolved-screen, and source-worldtube boundary queries differ;
4. for a supplied regular source phase boundary, when is the observer beam-intersection dimension
   `0`, `1`, or `2`; and
5. do time-live regularity and spherical symmetry themselves select a common-source physical
   relation?

This is one local central tile. It does not cover nonspherical histories, finite-radius arbitrary
jets, cut-locus multiplicity, global completion, or the observed SNe domain.

## Metric family and gauge ledger

Use dimension-matched central proper time `T=c_E t` and local areal radius `R`. On the regular
`X>0` center patch,

```text
g = -N(T,R)^2 dT^2 + L(T,R)^2 [dR + beta(T,R)dT]^2 + R^2 dOmega^2.
```

Smooth rotational invariance and elementary flatness give

```text
N(T,R)    = 1 + n(T) R^2 + O(R^4),
L(T,R)    = 1 + l(T) R^2 + O(R^4),
beta(T,R) = b(T) R + O(R^3).
```

The central values `N(T,0)=L(T,0)=1` are `pinned-by-THEORY/GAUGE`: central proper-time
normalization and regular areal radius. Even/odd parity is `pinned-by-THEORY`: smooth spherical
center regularity. The functions `n(T)`, `l(T)`, `b(T)` and all of their time derivatives are
`free-and-explored` history jets. No staticity, P1 slope, field equation, source density, or
observed coefficient is inserted. The omitted `O(R^3)`/`O(R^4)` radial terms remain live beyond
the declared order.

The observer is the regular central worldline. A normalized celestial field may rotate with
observer time. Its transverse drift `w_A=(partial_T n_sky)_A` is query/frame data and remains live;
it is not identified with the historical `mu_lock` scalar.

## Declared jet order

- metric: complete smooth fixed-time central two-jet;
- outgoing radial-null graph: through `O(R^3)` in `T(tau,R)`;
- terminal pair, areal, and source-frequency scalars: through `O(R^2)`;
- vertex Jacobi solution and full phase carrier: through the first curvature-sensitive order,
  `O(lambda^3)` in position and `O(lambda^2)` in momentum;
- source-boundary rank: exact finite-dimensional algebra, not a series approximation.

No conclusion may be generalized beyond these orders.

## Source-query classes — frozen separately

### Q0: marked point event

The transverse endpoint condition is `J_s=0`. It supplies no source rest frame, resolved image,
emission covector, or phase graph. Its phase boundary is the vertical subspace only when endpoint
momentum is deliberately retained as free boundary data.

### Q2: resolved two-screen germ

Supply a source event, source four-velocity, and a two-dimensional resolved source tangent screen.
This owns allowed endpoint **positions**. It does not by itself own a two-dimensional phase plane
or a momentum-versus-position law. A phase-intersection rank is therefore not assigned unless a
covector, transfer law, or equivalent phase boundary is additionally supplied.

### QW: source worldtube germ

Supply a timelike source worldtube, its unit flow, cross-section screen, orientation, and a chosen
future/past null-normal branch. These data may induce a phase graph through the differential of
the chosen null-normal field. The worldtube and branch are query data, not metric-selected source
physics.

### QB: abstract regular phase boundary control

For exact classification, supply a two-dimensional Lagrangian source boundary plane. Away from a
vertical chart it is `B_H={(x,Hx)}` with real symmetric `H`. This is a mathematical control and a
type for QW output, not a newly posited universal source law.

## Exact calculation plan

1. Derive the outgoing radial-null graph from the complete lapse/radial/shift metric.
2. Pull back the full observer map while retaining celestial drift; report pair, angular, and mixed
   blocks separately.
3. Derive terminal `phi_pair`, conditional areal `phi_areal`, and the source-frame frequency for a
   general smooth spherical source congruence. Do not identify these scalars by name or habit.
4. Derive the radial affine tangent, optical tidal coefficient, vertex Jacobi solution, and a full
   symplectic phase fundamental matrix from the same metric jet.
5. Derive observer image planes at the source and classify their intersection with Q0 and QB.
6. Determine what Q2 and QW do or do not add without inserting source dynamics.
7. Test flat, exact static reciprocal, genuinely time-live, celestial-drift, caustic, and
   observer/source-frame covariance controls.

## Design-stage pilot disclosure

Before this file was written, bounded scratch algebra was used only to choose a tractable complete
jet order. It indicated candidate leading combinations involving `n`, `l`, `b`, and `dot b`.
Those candidate formulas are not counted as preregistered discoveries. The bankable result requires
the independent constructions, exact residuals, mutation catches, and blind adversarial review
declared below.

## Candidate outcomes retained

- regular time-live coefficients create a leading nonzero terminal reciprocal jet;
- smooth-center parity delays the terminal reciprocal jet while a source-frequency channel has a
  lower-order term;
- angular/mixed query data change the fixed-label terminal pair readout;
- complete pullback data remain multichannel with no unique scalar collapse;
- nonzero source-boundary intersections exist only on coefficient/query subloci;
- spherical symmetry collapses the rank-one stratum;
- point-event, screen, and worldtube queries remain inequivalent;
- regularity and the metric jet do not select a physical history or source boundary.

No listed outcome is preferred.

## Certification and falsification contract

The result fails if any of the following occurs:

1. an allowed smooth central coefficient at the declared order was silently omitted;
2. direct Christoffel/Riemann reconstruction disagrees with the warped-product/Jacobi route;
3. the pulled-back metric reconstructed from its pair/mixed/angular blocks differs from direct
   substitution;
4. the full phase determinant or symplectic identity fails at the retained order;
5. an independently implemented source-boundary rank disagrees with the exact nullity calculation;
6. the static reciprocal or flat controls fail;
7. a query-owned source or celestial coefficient is mislabeled metric-derived; or
8. an observational outcome, desired P1 slope, or physical selector enters before the result is
   frozen.

The production script must emit exact symbolic residuals. A separate implementation must rebuild
the load-bearing formulas rather than import production expressions. Hostile mutations must make
the relevant checks fail. A fresh blind adversarial verifier is required before banking.

## Maximum conclusion

G115 may classify the first nontrivial regular-center time-live metric/query jet, its conditional
observer/source ray and phase data, and exact source-boundary intersection strata. It may establish
existence, obstruction, or remaining coefficient freedom in this bounded class.

It may not select the universe's history, observer protocol, source state, transfer, branch,
weights, global completion, `X_max`, SNe/BAO/CMB result, bootstrap, action, matter, mass, or
signalling law.
