# Observer longitudinal/transverse cocycle audit preregistration

Date: 2026-07-24

Base: `dc81c489b9e27bd86b2d58d93fbacf4a4fd01496`

Compute: CPU-only exact algebra plus an independent numerical ODE check.

Mode: metric-led, observing rather than targeting.

## Whole question

For each already registered complete or residual metric branch, can the
metric put reciprocal endpoint-clock comparison and transverse angular
transport into one honest observer-to-observer transition law?

The audit must distinguish four objects that have previously been discussed
separately:

1. the positive endpoint clock/frequency ratio `Q_gamma`;
2. the reciprocal two-channel matrix `S(log Q_gamma)`;
3. the vertex Jacobi map `J_gamma`, whose determinant gives angular area;
4. the complete first-order transverse deviation propagator `M_gamma` on
   `(xi, nabla_k xi)`.

It will first test whether `J_gamma` itself composes. If it does not, the
audit will test the smallest metric-derived completion `M_gamma`, without
adding an action, matter source, carrier, topology, or empirical target.

## Fixed candidate constructions

- `Q_gamma = omega_start / omega_end`, where
  `omega = -g(u,k)` for supplied endpoint observer tangents and a supplied
  null path; for static rest observers this reduces to a lapse ratio.
- `delta_gamma = log Q_gamma` and
  `S(delta)=diag(exp(-delta),exp(delta))`.
- the two-screen Jacobi equation from the supplied metric curvature.
- the full first-order screen fundamental matrix `M_gamma`.
- the block object
  `C_gamma = S(delta_gamma) direct_sum M_gamma`.
- full coframe parallel transport as a type-control, not as an automatic
  identification with either the founding reciprocal channel or the screen
  deviation propagator.

## Fixed branch universe

Every branch is retained even when it is incomplete or physically
unselected:

- conditional complete ultrastatic round `S3_b` / B19;
- complete homogeneous squashed-`S3` off-shell control;
- local centered static WR-L residual branch;
- conditional temporal-`phi` slice family;
- constant-spatial-curvature static countercontrol;
- universal physical UDT, for which no complete metric witness is currently
  registered.

The twelve finite-cell completion types and twenty-eight equation families
remain inherited completeness controls. No result may be assembled by
taking the clock law from one branch and the transverse law from another.

## Composition and covariance gates

A candidate is a path-groupoid cocycle only if it has:

1. identity on a zero path;
2. inverse under path reversal;
3. exact multiplication under path concatenation with the same intermediate
   event, observer, screen, and path type;
4. endpoint screen-frame covariance, with the intermediate gauge cancelling;
5. continuation through a conjugate point even if the projected vertex
   Jacobi block becomes singular;
6. explicit path multiplicity at a cut locus rather than an invented unique
   path.

Global observer reciprocity additionally requires a complete branch and a
recentring rule for arbitrary observer pairs. Pathwise composition alone
does not satisfy that stronger requirement.

## Exact controls fixed before calculation

1. A constant-curvature two-screen Jacobi system.
2. A round `S3_b` geodesic, including the antipodal caustic at `pi*b`.
3. A counterexample showing that the projected vertex Jacobi block does not
   multiply under segment concatenation.
4. The WR-L radial control
   `N(D)=1-D/(2X)`, `R(D)=D-D^2/(4X)`,
   `K_rad=1/(2 X R)`.
5. Generic positive endpoint lapses/frequencies for the clock cocycle.
6. Endpoint screen rotations for the covariance law.

## Premise and value ledger

- `c_E`: `OBSERVED_FOUNDING`, calibrated clock-length conversion.
- supplied Lorentzian metric and its Levi-Civita curvature:
  `CONDITIONAL_SUPPLIED_BRANCH`.
- endpoint observer tangents and event pairing: `FREE_INPUT`.
- null versus observer-rest path: `FREE_CANDIDATE`; neither is selected.
- affine normalization and screen basis: `GAUGE`, with transformation laws
  retained.
- path family: `FREE_AND_ALL_RETAINED`.
- identification `delta_gamma = log Q_gamma` with the founding reciprocal
  depth: `CONDITIONAL_SOLDER_TO_TEST`, not assumed as native physics.
- branch scales `b` and `X`: positive symbolic parameters.
- action, source, carrier, topology, boundary completion, density,
  bootstrap, physical `X_max`, and observational fit: `OPEN/EXCLUDED`.

The complete machine-readable ledger is `PREMISE_LEDGER.tsv`.

## Falsification and certification

Certification requires:

- exact first-order Jacobi-system composition and symplecticity;
- an exercised noncomposition counterexample for the projected Jacobi map;
- exact round and WR-L controls;
- independent numerical construction that does not import production code;
- one disposition for every registered branch;
- exercised catches for projected-map promotion, cross-branch splicing,
  caustic deletion, screen-gauge dependence, clock-solder promotion, and
  global-recentring overclaim;
- deterministic replay, source hashes, frozen manifests, current paths,
  links/frontier targets, tests, and untouched dirty-checkout metadata.

## Maximum conclusion

At most this audit may derive a pathwise metric-geodesic-deviation cocycle
and identify the exact extra premises needed to call its clock block the
founding UDT reciprocal operator.

It may not select a physical event pairing, choose null over co-present/rest
comparison, derive a path-independent universal observer transformation,
splice different branches, select a profile or complete branch, calculate
physical `X_max`, or derive signal propagation, action, source, carrier,
matter, density, bootstrap closure, topology, boundary physics, or an
observational prediction.
