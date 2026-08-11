# G74 symbolic-scale observer-sky relation topology atlas — preregistration

Date: 2026-08-11

Base commit: `6cc3f29b5b873729f0f8561aefc64aa1a16771be`

## Whole question

For the complete initial celestial sphere of the already registered G68 observer event, what
global relation does each of the exact 21 analytic control metrics produce at the first crossing of
the registered comparison sphere? Classify every profile as globally evaluable, incomplete at the
center, endpoint-missing, branch-valued, sampled-regular, parity-changing, or critical. Do not
select or repair a profile because it resembles a CMB sky.

This is a metric-led global-relation classification. It is not a source ensemble, fit, spectrum,
physical last-scattering construction, bootstrap calculation, or `X_max` determination.

## Exact query and candidate universe

- Candidate universe: all 21 frozen rows of
  `udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/PROFILE_UNIVERSE.tsv`, exactly once.
- Observer event: the registered dimensionless point `r/R=1/4`, `theta=pi/2`, `psi=0`.
- Initial sky: every future null direction `u+n^i e_i`, `n in S^2`, in the complete local
  orthonormal tetrad of each metric.
- Relation target: the first outward crossing of the declared comparison surface `r/R=1`.
- Branch policy: return every encountered outcome. Do not replace missing endpoints, turns,
  multiple crossings, chart/metric incompleteness, or critical directions with a preferred branch.
- Scale: `R>0` remains symbolic. The solve uses dimensionless coordinates `x=r/R`; topology,
  degree, parity, and normalized criticality must be shown invariant under positive common
  rescaling before any dimensionless result is interpreted.
- Generator: null geodesics are a `CHOSE_QUERY_CONTROL`, not material signals in the co-present
  interpretation.

The query is a complete sky for this frozen control ensemble. It is not the function-space census
of all complete UDT metrics.

## Pre-solve center-completion gate

Every profile is first rewritten in Cartesian spatial coordinates. It may enter the whole-sky
solve only if the supplied metric is at least `C2` through `r=0`, because a complete sky contains
inward directions and the curvature/Jacobi interpretation requires second derivatives. Failure is
classified `BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER`; it is not repaired, discarded, or called a
failure of UDT.

No even extension, absolute-value smoothing, core splice, cutoff, reflected ray, outward-hemisphere
restriction, or fitted center completion is allowed.

## Exact topology/critical calculus to test

For every supplied regular branch `f_b:S_o^2 -> S_s^2`:

1. derive the endpoint-variation factorization through the metric Jacobi field and the transverse
   endpoint projection;
2. distinguish a Jacobi caustic, an endpoint-grazing degeneracy, and a chart/source-screen
   degeneracy;
3. compute the oriented local Jacobian, parity, degree, image multiplicity, and branch label without
   conflating them;
4. verify the whole-sphere theorem that an everywhere-regular connected `S2 -> S2` local
   diffeomorphism is a degree `+1` or `-1` diffeomorphism;
5. verify exact axisymmetric witnesses for a diffeomorphism, orientation reversal, degree-`m`
   critical map, degree-zero fold, and twist/carry that changes orientation data without changing
   the area Jacobian;
6. retain regular multicover examples only under topology/domain types where they actually exist.

## Numerical method for center-eligible G68 profiles

- Production: complete-sky Cartesian Hamiltonian null-geodesic integration on nested icospheres.
- Resolution levels: subdivisions `2`, `3`, and `4` (`162`, `642`, and `2562` vertices). These are
  solver-resolution choices, not physics premises.
- Time integration: float64 fixed-step RK4 with `512` and `1024` steps over affine cap `4R`;
  crossings are interpolated inside the first crossing step.
- Hardware: one GPU process if CUDA float64 is available; otherwise vectorized CPU. Hardware is a
  numerical technique only.
- Independent route: SciPy `DOP853` in Cartesian Hamiltonian variables on the full subdivision-2
  vertex set, with independent event localization and direct endpoint comparison.
- Mesh characterization: record endpoint coverage, signed face area, minimum normalized area
  ratio, orientation classes, topological degree estimate, nearest non-neighbor image separation,
  and resolution drift. Do not turn absence on a finite mesh into a global no-caustic proof.

## Premise ledger summary

- `pinned-by-THEORY`: Lorentz metric, null cone, metric geodesic/Jacobi construction once the query
  is supplied, endpoint transversality calculus, degree/parity identities.
- `pinned-by-HISTORICAL_CONTROL`: the 21 profiles, observer event, tetrad convention, and comparison
  sphere.
- `free-and-explored`: all initial sky directions and every returned relation class.
- `CHOSE_NUMERIC`: icosphere levels, affine cap, step counts, tolerances, and hardware.
- `OBSERVED_CALIBRATION`: `c_E`; it fixes clock/length units but is absent from the dimensionless
  topology classification.
- `WORKING_INACTIVE`: co-presence interpretation, `X_max`, SNe compatibility, bootstrap, deep-sky
  survey structure.
- `OPEN_INACTIVE`: physical CMB endpoint/profile/source, detector/readout, branch combination,
  action, carrier, and native matter source.

## Falsification and certification contract

- Reject a whole-sky classification for any profile whose supplied metric is not `C2` through the
  center.
- Reject `GLOBAL_BIJECTION` from mesh sampling alone; reserve it for an exact theorem or state
  `OBSERVED_SAMPLED_REGULAR`.
- Reject a caustic claim unless the metric-derived endpoint differential loses rank or a convergent
  signed-area diagnostic reaches zero; face inversion alone on a coarse mesh is a candidate.
- Reject conflation of endpoint grazing with Jacobi rank loss.
- Reject a regular nontrivial whole-sky `S2` self-cover.
- Reject any statement that twist/carry changes degree unless the oriented Jacobian or global map
  actually changes it.
- Reject any source, matter distribution, CMB feature, coefficient fit, physical endpoint, global
  scale, or branch weight.
- Preserve every blocked, missing, multiple, critical, and regular class in the census.

## Preregistered landing classes

- `COMPLETE_CONTROL_SKIES_REGULAR_WITH_DEGREE_ONE`;
- `GLOBAL_RELATION_BRANCH_OR_CRITICAL_STRUCTURE_OBSERVED`;
- `EXISTING_CONTROL_PROFILES_INCOMPLETE_FOR_WHOLE_SKY`;
- `MIXED_GLOBAL_COMPLETION_CLASSES`;
- `NUMERICALLY_UNRESOLVED`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`.

## Maximum conclusion

A complete classification of the exact 21-profile control universe under the declared whole-sky
query, plus the exact topology/critical calculus that any later physical sky relation must obey.
No physical CMB source, anisotropy, spectrum, last-scattering surface, universe size, `X_max`,
bootstrap selector, action, or matter law may be claimed.
