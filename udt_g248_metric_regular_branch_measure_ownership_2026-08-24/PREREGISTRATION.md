# G248 preregistration — regular branch-measure ownership

Date: 2026-08-24

## Alternatives

The audit must return exactly one primary alternative:

```text
A_UNIQUE_PHYSICAL_BRANCH_MEASURE_DERIVED
B_TYPED_CANONICAL_GEOMETRIC_MEASURES_EXIST__PHYSICAL_BRANCH_MEASURE_UNSELECTED
C_ONLY_TRANSPORTS_SUPPLIED_MEASURE
D_REGULAR_MEASURE_TYPE_FAILURE
```

Alternative A requires both a gauge-invariant construction and proof that the active premises
exclude every competing lawful branch measure and select its physical population/detection use.
Existence of a natural measure alone is insufficient.

Alternative B requires at least one derived, gauge-invariant regular branch density, plus an exact
type or nonuniqueness witness showing why it is not a universal physical branch probability.

Alternative C is selected if the metric provides only Jacobians for pushing an independently
supplied measure and no nonzero canonical density on the regular incidence space.

Alternative D is selected if the proposed density fails coordinate, screen-gauge, affine-scale,
reversal, or overlap consistency on its declared regular domain.

## Preregistered exact checks

1. Derive the density-line isomorphism for the transverse fiber product
   `I_AB = C_A x_M I_B`.
2. In an orthonormal source-sky basis, prove or refute
   `abs(vol_g(J1,J2,K,U_B)) = omega_B*abs(det D) = A/r` under source normalization.
3. Derive or refute the local coarea density `dmu_I=(r/A)d tau_A` on each regular branch.
4. Test spacetime diffeomorphism naturality, passive endpoint `O(2)` invariance, branch relabeling,
   and normalized-affine coordinate invariance.
5. From `M^T Omega M=r Omega`, derive the inverse position block and test
   `A_inverse=A/r^2` and `(r/A)_inverse=r/A` for mathematical reversal.
6. Test product descent of edge incidence densities on finite matched chains without identifying a
   chain with an independent direct edge.
7. Derive the phase-volume law `M^*nu_target=r^2 nu_source` and distinguish phase-volume transport
   from branch counting and incidence density.
8. Classify continuous positive scalar characters of `CSp+(4,R)`; test whether composition alone
   leaves the family `r^alpha`.
9. Retain G240 unit counting on finite all-image fibers as a separately typed measure and test its
   nonidentity with `r/A` on unequal regular branches.
10. Classify `A=0`, nonproper, continuous, and infinite-image strata without using an inverse
    Jacobi block.

## Finite verification contract

- production implementation: exact integer/Fraction algebra, at least 4,096 regular cases and
  40,000 assertions;
- independent implementation: no production import or saved-output read, at least 10,000 cases and
  100,000 assertions;
- fixed controls: equal-area/counting coincidence, unequal-area separation, formal inverse,
  noncommuting phase, direct-versus-chain distinction, and rank-one caustic;
- hostile mutations must include `A/r` in place of `r/A`, omission of the frequency factor,
  inversion of a caustic position block, scalarization of phase, unit counting conflated with
  coarea density, a fitted exponent, and promotion to source/detector physics;
- exact saved outputs and SHA-256 source freeze;
- fresh read-only external adversarial review before banking.

## Maximum conclusion

At most, derive and classify metric-natural measures on the supplied regular quiver and its matched
chains. Do not select a physical history, observer/source population, detector, transfer law,
observational result, `X_max`, action, matter, bootstrap, mass, or signalling law.
