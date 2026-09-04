# G344 audit report

Date: 2026-09-04
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Result

On every noncoincident positive-time segment of each supplied fixed labelled G343 ray, the full
screen position block is invertible. The exact symplectic propagator therefore has one homogeneous
quadratic type-I endpoint generator. Its negative mixed Hessian is `B^-T`, and its positive
determinant density is `1/abs(det B)`.

The generator and density obey exact stationary composition, common-affine reversal, reference-
event covariance, and endpoint screen-basis covariance. The generator has affine weight one and
the density affine weight two. Independently normalized endpoint derivative units are conformally
symplectic, not one unweighted canonical chart. Both principal limits remain regular away from
coincidence; compact lifts remain separate path labels.

## Qualification found before rerun

The frozen uniqueness wording was too strong when endpoint times vary. The map fixes the complete
homogeneous quadratic representative, but it is blind to an additive function `k(T1,T0)`. Exact
composition and reversal reduce this to an endpoint coboundary `f(T1)-f(T0)`. Commit `9701e595`
records the correction and zero homogeneous normalization before the accepted reruns. The mixed
Hessian and determinant are unaffected.

## Gates

- Preregistered at `5c16ca60` before evaluation.
- Qualification banked at `9701e595` before accepted reruns.
- Production: `13580/13580`.
- Implementation-distinct reconstruction: `4882/4882`.
- Hostile mutations: `14/14` caught.
- Full noncoincident endpoint-order and direction tile covered analytically; finite checks certify
  implementations rather than replacing the proof.
- Fresh external adversarial review: authenticated all 29 payloads, replayed `19/19`, independently
  reconstructed the core formulas, found no blocking defect, and accepted without repair.
- Non-blocking external caveats: compact-lift executable coverage is documentary because no
  aggregation path exists; text-token gates protect packaging and do not replace analytic proof.

## Ownership boundary

This is one metric-derived screen endpoint generator and affine-weighted bidensity, conditional on
the supplied G343 spacetime, ray, screen, affine gauge, and compact lift. It is not a selected
spacetime action, electromagnetic or light law, flux/luminosity relation, probability amplitude,
observational distance, path/population selector, stability result, matter/mass law, scale,
`X_max`, or canon.
