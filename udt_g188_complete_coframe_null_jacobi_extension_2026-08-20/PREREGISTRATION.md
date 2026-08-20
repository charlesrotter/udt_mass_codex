# G188 preregistration — complete-coframe null-screen/Jacobi extension

Date: 2026-08-20

## Whole question

For an arbitrary supplied smooth Lorentzian complete coframe, one supplied regular affinely
parametrized null query, one normalized source observer, and one initial screen orientation, does
the metric uniquely determine:

1. the rank-two positive quotient screen;
2. its carried metric connection;
3. the full symmetric screen-tidal operator, including off-diagonal mixing; and
4. the finite vertex-normalized Jacobi map?

If so, is G187 the symmetry-diagonal specialization of this general construction rather than a
separate spherical mechanism?

This is `METRIC_LED` and observing rather than targeting. It tests the complete metric as supplied;
it does not search for a fitted angular response or observational pattern.

## Bounded arena

Supply:

- a smooth Lorentzian four-metric represented by an invertible complete coframe
  `g=E^T eta E` on one regular neighborhood;
- one future affinely parametrized null geodesic branch `gamma` with generator `k`;
- one future unit source observer `u_o` with `-g(u_o,k_o)=1`;
- the source pair plane `span(u_o,k_o)` and one orientation of its positive orthogonal screen;
- vertex data `D(0)=0`, `D'(0)=I`.

The abstract theorem may use an arbitrary `E`. One explicit nonspherical mathematical witness may
be chosen solely to prove that a live off-diagonal tidal term survives without a coefficient. That
witness is not a physical UDT history.

## Premise ledger

| Input | Tag | Role |
|---|---|---|
| complete coframe `E` | `free-and-explored` supplied metric history | full regular local arena |
| `g=E^T eta E` | `DERIVED` metric readout | all coframe channels precede connection/curvature |
| null branch and source event | `free-and-explored` query | no physical ray population |
| affine and observer normalization | `CHOSE` query calibration | fixes screen-map units |
| initial screen orientation | `CHOSE` | final result must be endpoint-`O(2)` covariant |
| Levi-Civita connection, curvature, Jacobi equation | category-A geometry | evaluator, not dynamics |
| explicit nonspherical witness coefficients | `free-and-explored` exact controls | liveness/falsification only |

No `X_max`, `R(Z)`, observation, fit, source, flux, luminosity, electromagnetic law, action,
matter, bootstrap, or added angular coefficient is allowed.

## Dropped sectors and strata

- physical query/ray population and branch aggregation;
- accelerated nongeodesic propagation;
- caustic inversion, cut-locus selection, multiple-image weights, and global completion;
- emission, absorption, scattering, frequency/energy transfer, flux, and luminosity;
- singular coframes, non-affine branches without declared conversion, and null-normalization failure;
- selection or evolution of the supplied complete metric history.

Time dependence and coframe mixing are not to be frozen in the abstract theorem. The explicit
witness may be a bounded nonspherical slice, but it cannot set the theorem's generality.

## Required derivation and certification

1. Construct the quotient screen `S=k^perp/span(k)` and prove its induced metric is positive.
2. Prove Levi-Civita transport induces a metric connection on `S`, independent of null-gauge
   representatives.
3. Prove `T([X])=[R(X,k)k]` is a well-defined self-adjoint screen endomorphism.
4. Prove the matrix Jacobi initial-value problem has a unique finite propagator on every regular
   branch and transforms as `D -> Q_s^T D Q_o` under endpoint screen frames.
5. Show all complete-coframe channels enter upstream through `g`, its connection, and curvature;
   no scalar coefficient is available or needed.
6. Reproduce G187 as the static-spherical reflection-diagonal subcase.
7. Supply one exact nonspherical witness with nonzero off-diagonal screen tide and verify its finite
   matrix response independently from the production implementation.
8. Catch deletion of the off-diagonal term, scalarization/diagonalization by assumption, a curvature
   sign flip, null-gauge dependence, coframe-gauge dependence, and promotion to flux or ray selection.

## Preregistered landings

- `GENERAL_COMPLETE_COFRAME_NULL_JACOBI_FUNCTOR_DERIVED_CONDITIONALLY`: the supplied metric and null
  query uniquely fix the quotient-screen connection, full tidal operator, and finite Jacobi map;
  G187 is a symmetry-reduced subcase.
- `GENERAL_SCREEN_FUNCTOR_DERIVED__COMPLETE_COFRAME_LIVENESS_UNCERTIFIED`: the abstract theorem closes
  but the explicit full-channel witness or independent replay fails.
- `INITIAL_SCREEN_DERIVED__FINITE_COMPLETE_COFRAME_PROPAGATION_REQUIRES_EXTRA_CARRY`: an additional
  non-metric transport datum survives.
- `DERIVATION_OR_CERTIFICATION_FAILURE`: a required identity or independent gate fails.

## Maximum conclusion

At most G188 may derive the finite quotient-screen/Jacobi evaluator for supplied smooth regular
complete metrics and supplied affine null queries, with an exact nonspherical mixing witness. It may
not select the physical metric, ray population, source state, observed angular pattern, transfer or
flux law, global completion, `R(Z)`, or `X_max`.
