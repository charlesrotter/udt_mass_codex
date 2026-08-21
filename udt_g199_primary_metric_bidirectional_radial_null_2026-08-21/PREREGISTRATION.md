# G199 preregistration — primary-metric bidirectional radial null response

Date: 2026-08-21

Status: `PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION`

## Whole question and bounded regime

Starting only from the declared primary static-spherical metric

\[
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

one static unit source clock, the radial completed-pair ruler, and the two normalized future null
initial directions, derive both affine radial germs, their source-to-endpoint frequency ratios,
their quotient-screen connections, tidal operators, and vertex-normalized Jacobi maps.

The test is local/branchwise on any smooth interval with `r>0` and `f>0`.  It is metric-led and
observing, not target-led.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| observed `c_E`, absorbed into `x0=c_E t` | `OBSERVED` calibration | dimension matching only |
| reciprocal primary metric form | `pinned-by-THEORY` in declared static-spherical slice | full tested metric |
| smooth positive supplied `f(r)=exp(-2 phi(r))` | `FREE_AND_EXPLORED` history within slice | no profile selected |
| completed-pair Dual Reciprocity after full pullback | `WORKING_FOUNDATIONAL_CLARIFICATION` | fixes pair ruler normalization |
| source event, static clock, radial ruler orientation | `SUPPLIED_QUERY` | seeds the two null germs |
| affine normalization `-g(U,k)=1` at source | `SUPPLIED_QUERY_CALIBRATION` | fixes affine scale |
| Levi-Civita connection, curvature, frequency, quotient screen, Jacobi equation | `DERIVED_CONDITIONAL` | metric evaluators |
| G191--G198 one-sided complete-coframe family | `OMITTED_CONTROL` | provenance comparison only |

No value is pinned by habit.

## Required calculations

1. Derive the pair frame
   \(U=f^{-1/2}\partial_0\), \(N=f^{1/2}\partial_r\) and null directions
   \(\ell_\pm=U\pm N\).
2. Solve the radial affine geodesic first integrals for both signs from the same source
   normalization.
3. Derive the static-clock frequency ratio at any regular endpoint.
4. Construct an orthonormal angular screen and compute its quotient connection and the full
   two-by-two curvature tide directly from the metric.
5. Solve the vertex-normalized Jacobi equation on each germ.
6. State exactly which differences are orientation/endpoint effects and whether any intrinsic
   outgoing/incoming loud/quiet split survives.
7. Reconcile the result with G198 without weakening G198's theorem inside its chosen family.

## Certification and falsification contract

- exact symbolic reconstruction of the metric inverse, Christoffels, affine geodesic residual,
  frequency, screen connection, Riemann tensor, tidal matrix, and Jacobi residual for both signs;
- an implementation-independent exact-rational metric-jet replay over at least 1,000 smooth
  positive local jets, with neither production imports nor production artifacts;
- explicit nonflat controls with nonzero `f'` and `f''` so a zero tide cannot pass vacuously;
- hostile mutations that delete the areal derivative, reverse the curvature sign, drop one null
  sign, or import the G196 chiral coupling must fail;
- premise verifier, repository tests, package replay, source hashes, and `git diff --check` before
  banking.

The candidate is falsified if either null direction is not affine after the derived scaling, if
the direct screen tide differs between signs at the same local metric jet, or if the claimed finite
Jacobi law fails direct substitution.

## Preregistered landings

One of:

- `PRIMARY_METRIC_RADIAL_NULL_PAIR_IS_REVERSAL_SYMMETRIC__NO_NATIVE_CHIRAL_SPLIT`;
- `PRIMARY_METRIC_RADIAL_NULL_PAIR_HAS_METRIC_DERIVED_DIRECTIONAL_ASYMMETRY`;
- `PRIMARY_METRIC_TWO_DIRECTION_RESPONSE_DEPENDS_ON_ADDITIONAL_QUERY_CARRY`;
- `DERIVATION_OR_CERTIFICATION_FAILURE`.

## Omitted sectors

Nonradial rays, nonspherical/time-dependent ambient metrics, arbitrary complete-coframe mixing,
observer population, later endpoint intersection, caustics beyond the tested regular branch,
radiative transfer, flux, luminosity, observations, `X_max`, global completion, action, sources,
matter, mass, bootstrap, and signalling.

## Maximum conclusion

At most G199 can classify the two radial null screen/frequency responses of the declared primary
static-spherical metric and correctly type the G198 asymmetry as either primary-metric native or
chosen-family specific.  It cannot select a physical profile or cosmology.
