# Preregistration — observer-pair query-bundle section/descent audit

Date: 2026-08-04
Base: `b3a282725ba6eba088c2cb3e52e6163081ed9ad3`
Compute: bounded CPU exact algebra, type checking, and evidence synthesis only

## Whole question

For every open law slot in the factorized whole-spacetime skeleton, can the relevant object be
defined equivariantly on the total ordered observer-pair query bundle and then descend to a tensor
or operator on spacetime without choosing one reciprocal plane? Or does the object genuinely need
a realized smooth section, a branch-derived section, or stratified section data?

This is metric-led and ontology-led. It does not search for an action, source, carrier, desired
particle, or preferred cosmological branch.

## Frozen bounded universe

`LAW_SLOT_UNIVERSE.tsv` freezes all eight open skeleton slots `L01`–`L08` and their audit facets.
`DESCENT_TEST_UNIVERSE.tsv` freezes the object classes and controls used to decide them. The audit
must include:

- founded reciprocal comparison and path-groupoid composition;
- the tautological reciprocal plane, screen metric, and base-screen mixing over the query bundle;
- ambient versus plane-projected curvature and connection observables;
- physical configuration/variation ownership and base-boundary versus pair-resolved boundary data;
- branch-derived selectors on regular strata and their collision, defect, zero, causal-type-change,
  and rank-change loci; and
- the consequences for native law, constraint/evolution, bootstrap, `X_max`, and matter slots.

Every frozen row must receive exactly one primary descent class. A row may retain a separately typed
query-bundle law while failing spacetime descent.

## Definitions frozen before outcomes

Let `pi:P->M` be the ordered observer-pair query bundle. It has the tautological rank-two reciprocal
plane `N_tilde` in `pi*TM` and screen `Q_tilde=N_tilde^perp`.

- `QUERY_EQUIVARIANT`: the object is well typed on `P` and transforms covariantly under a vertical
  change of ordered pair. This alone does not make it an object on `M`.
- `BASIC_DESCENT`: the query-bundle object is invariant under vertical pair changes and, for
  differential forms, horizontal (zero on vertical vectors), so it is the pullback of a unique
  spacetime object.
- `SECTION_PULLBACK`: a section `s:M->P` turns query-bundle data into spacetime data, but the result
  may depend on `s`; section independence is equivalent to basic descent.
- `BRANCH_DERIVED_PULLBACK`: a regular intrinsic construction `s[g]` supplies a section on a branch;
  its variation follows from the parent metric by the chain rule wherever regular.
- `STRATIFIED_OR_SET_VALUED`: collision, defect, or rank-change loci do not supply a unique smooth
  fixed-rank section. These loci must be retained rather than discarded.
- `FIBER_AGGREGATION_OPEN`: averaging or integrating query data over the fiber requires a measure,
  weight, or quotient rule; none may be invented in this audit.

## Physical and mathematical choices

All choices are stamped in `PREMISE_LEDGER.tsv`.

- `pinned-by-THEORY`: Lorentz signature, founded reciprocal character, observer-frame equivariance,
  exact typed path-groupoid composition, Levi-Civita geometry of a supplied metric, and the frozen
  whole-spacetime/globalization/selector ledgers.
- `free-and-explored`: object variance, vertical invariance, horizontality, section dependence,
  regular versus collision/defect strata, and whether a law is query-level or spacetime-level.
- `pinned-by-HABIT`: none may enter a positive result. No preferred tetrad legs, stationary time,
  radial direction, round `S^2`, fiber average, Haar measure, action, boundary polarization, or
  smooth deletion of singular strata is permitted.

## Preregistered hypotheses

1. Founded reciprocal comparison and composition can remain exact query/path-groupoid kinematics
   without a single physical reciprocal-plane field on spacetime.
2. Ambient metric curvature tensors and their scalar contractions are already spacetime objects;
   pair-plane projections, screen geometry, and mixing generally remain query-dependent unless
   they pass the vertical basicness test or a section is supplied.
3. A query-bundle section can pull data back to spacetime, but does not make the pullback intrinsic
   when different sections give different values.
4. The variation domain changes with ontology: vertical query changes are not field variations;
   realized-section variations are additional field variations; branch-derived sections vary by
   the parent-metric chain rule on regular strata.
5. A branch-derived selector may close a local law on a regular stratum while failing to define a
   unique differentiable law at eigenvalue collisions, zero/defect loci, causal-type changes, or
   rank changes.
6. Base-boundary geometry can exist without a reciprocal section, while pair-resolved boundary
   polarization and projected boundary data may require a section or remain query-level.

These are source-informed hypotheses, not results of this audit until every frozen row is classified
and the load-bearing descent tests are independently replayed.

## Outcome classes

- `ALL_OPEN_LAWS_BASIC_NO_SECTION_NEEDED`: every frozen law facet descends without a section.
- `TYPED_SPLIT_QUERY_AND_SPACETIME_LAWS`: some objects are honest query laws or intrinsic spacetime
  laws, while other physical law facets require a realized/branch-derived/stratified reduction.
- `UNIVERSAL_SECTION_REQUIRED_FOR_ALL_LAWS`: no relevant law facet survives without one section.
- `INSUFFICIENT_EVIDENCE_STOP`: the frozen sources or exact tests cannot support a complete bounded
  classification.

## Certification and falsification

The exact contracts are frozen in `FALSIFICATION_CONTRACT.tsv`. At minimum the audit must:

1. prove basicness is stronger than equivariance using exact vertical-pair countercontrols;
2. show section-dependent pullbacks disagree while a basic ambient tensor does not;
3. distinguish query variation from physical field variation;
4. distinguish ambient curvature from projected/screen/extrinsic curvature;
5. retain regular, collision, defect, causal-change, and rank-change selector strata;
6. classify every law slot and every frozen object exactly once;
7. forbid an unregistered fiber average or measure from manufacturing descent; and
8. independently reconstruct all load-bearing exact checks without importing production code.

## Maximum allowed conclusion

At most, identify which future equations can be formulated as query-bundle laws, which already live
on spacetime, and which require a physical section/reduction or explicit stratified ownership rule.
The audit may sharpen the smallest missing object to a descent/ownership rule if supported.

It cannot choose a section, action, source, carrier, boundary functional, bootstrap equation,
`X_max`, matter branch, density, scale law, or dynamics. It cannot launch a solve, GPU work,
canonization, or repository reorganization.
