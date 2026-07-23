# Preregistration — angular-generator complete-branch census

Date: 2026-07-23
Base: `2fb3fd59207acd6da3c85b81dd320ce551888997`
Mode: metric-led, CPU exact algebra plus bounded analytic branch controls

## Whole question

For every one of the twelve already registered complete finite-cell
completion families, determine whether its own metric and global data define
an angular deformation generator and force its CSN-reduced eigenvalues to be
`-1,+1` throughout the complete regular cell.

This is not a search for a reciprocal branch. Every completion family,
failure of definition, degeneracy, unmatched profile, and matched profile is
retained.

## Intrinsic object to be tested

On a regular stratum, suppose the branch supplies:

1. a rank-two angular bundle `A`;
2. its positive induced metric `q`;
3. a metric-defined depth flow `T` normalized by `T(phi)=1`; and
4. an identification of angular fibers along that flow.

The metric strain endomorphism is

```text
H = (1/2) q^{-1} Lie_T(q).
```

Its Common-Scale-Neutral part is

```text
J = H - (trace(H)/2) I.
```

The exact reciprocal-pattern predicate is

```text
trace(J)=0,
det(J)=-1,
equivalently J^2=I with eigenvalues {-1,+1}.
```

This definition measures the metric-determined symmetric angular strain.
The skew angular-frame rotation is not silently inferred from `q`; it
requires a connection or frame-transport premise and is recorded separately.

If `dphi=0`, the angular rank changes, `q` degenerates, no angular bundle is
selected, or no fiber identification is supplied, `J` is `UNDEFINED` rather
than assigned a desired value.

## Branch universe

The universe is frozen to the twelve rows of
`udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv`:

```text
FC01_BOUNDARY_BOUNDARY
FC02_ONE_CAP_BOUNDARY
FC03_TWO_CAP_P0
FC04_TWO_CAP_P1
FC05_TWO_CAP_P_GT1
FC06_NONPRIMITIVE_CAP
FC07_PERIODIC_TORUS_BUNDLE
FC08_MIRROR_DOUBLE
FC09_NONORIENTABLE_GLUE
FC10_STRATIFIED_PROJECTOR
FC11_NONINTEGRABLE_DISTRIBUTION
FC12_RECIPROCAL_TORIC_DIAGONAL
```

No branch may be removed because it lacks a metric profile or fails to
resemble the desired universe.

## Required calculations

1. Derive `H` and `J` for a general positive `2x2` angular metric.
2. Derive an exact shape/rotation parameterization and the complete
   pointwise `{-1,+1}` criterion.
3. Distinguish raw scale rate, CSN-reduced strain, and unsupplied skew
   rotation.
4. Test diagonal matched, inverse, spectator, common-scale, variable-shear,
   rotating-axis, critical-`phi`, and degenerating-rank controls.
5. For each completion family record:
   - whether `A`, `q`, `T`, and fiber identification are supplied;
   - interior generator class;
   - endpoint/seal/glue/monodromy restrictions;
   - a matched witness if admitted;
   - an unmatched witness or compactly supported deformation if admitted;
   - whether the pattern is forced, merely allowed, excluded, or undefined;
   - whether it persists through every regular point and whether it extends
     through singular/cap strata.
6. Test all registered mirror lifts separately.
7. Test periodic and nonorientable monodromy compatibility without replacing
   the full `GL(2,Z)` families by a few examples.
8. Preserve `c` explicitly in the complete metric bookkeeping. `c` is the
   observed clock-ruler conversion and may not be set to one. The angular
   generator is dimensionless because it is differentiated with respect to
   dimensionless `phi`; this does not remove `c` from the complete metric or
   determine angular size.

## Classification contract

Each family receives exactly one branch-level ruling:

- `FORCED_PERSISTENT_REGULAR`;
- `CONDITIONAL_SUBFAMILY_PERSISTENT_REGULAR`;
- `ALLOWED_NOT_FORCED`;
- `OBSTRUCTED_BY_GLOBAL_GLUE`;
- `UNDEFINED_AT_REQUIRED_STRATUM`;
- `INSUFFICIENT_METRIC_DATA`.

A family is `FORCED_PERSISTENT_REGULAR` only if every admissible profile
within its registered definition has the reciprocal `J` at every regular
point. One successful witness is never enough.

## Falsification and catch contract

The verifier must reject:

1. a missing or duplicate completion row;
2. treating topology alone as a supplied metric profile;
3. testing raw `H` where CSN requires `J`;
4. silently setting the common angular scale constant;
5. silently setting angular-frame rotation to zero;
6. treating a chosen toric frame as metric-selected;
7. assigning a generator where `dphi=0`;
8. extending a rank-two result through a cap or projector-rank transition;
9. replacing general monodromy by identity monodromy;
10. treating mirror `+I`, `-I`, exchange, and axis lifts as equivalent;
11. calling an allowed subfamily forced when an admissible counterprofile
    remains;
12. dropping `c` from complete-metric dimensional bookkeeping; or
13. promoting a conditional control to a selected universe.

## Maximum allowed conclusion

The strongest allowed positive conclusion is:

```text
THE_CSN_REDUCED_ANGULAR_GENERATOR_IS_EXACTLY_RECIPROCAL_ON_EVERY_REGULAR_
POINT_OF_ANY_BRANCH_WHOSE_OWN_METRIC_DATA_FORCE_THE_MATCHED_ANGULAR_
CONFORMAL_PROFILE__TOPOLOGICAL_COMPLETION_OR_ONE_MATCHED_WITNESS_ALONE_
DOES_NOT_ESTABLISH_NATURAL_SELECTION_OR_EXTENSION_THROUGH_DEGENERACIES
```

No action, matter carrier, source, mass, density selection, time evolution,
physical boundary completion, or canonization may follow from this census.

