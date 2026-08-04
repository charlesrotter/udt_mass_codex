# UDT extension-bundle globalization and variation-domain audit — preregistration

Date: 2026-08-04

## Whole question

Do the registered local complete-coframe extension charts define a globally coherent equivariant
configuration bundle, and what is the most general honest tangent/variation data on that bundle
before any native action or field equation is supplied?

The audit observes every transition family compatible with the current geometry. It does not target
a trivial bundle, a preferred topology, a global coframe, a particle branch, or a desired universe.

## Exact bounded frame

- Start from the founded reciprocal character and the Phase-A local factorization

  ```text
  E_i = [[A_i,       0],
         [D_i S_i, D_i]],
  ```

  with `A_i=D(phi_i)` only in a supplied local reciprocal realization.
- Treat the positive-triangular form as a local chart/trivialization, not a global physical gauge.
- Retain arbitrary chart/coframe overlaps, reciprocal-plane realization, screen transitions,
  channel reversal, topology and boundary sectors.
- Work on the smooth fixed-rank stratum. Rank-changing/defect strata are classified separately and
  not discarded.
- Use CPU-only block, bundle and exact finite-matrix algebra. No field solve, global polynomial
  elimination, ODE/PDE, GPU work or observational fit.

## Premise and choice ledger

### Pinned by current evidence

- The abstract reciprocal character `D(phi)=diag(exp(-phi),exp(phi))` and its additive composition.
- Observer-frame covariance requires equivariance, not one globally fixed generator matrix.
- The registered pointwise extension chart has three angular and four mixing directions.
- Local Lorentz/coframe and coordinate changes are presentation gauge.
- Strong local CSN is inactive; `S2`, EH, Bach, bootstrap and matter retain current stamps.

### Free and fully classified in this audit

- overlap maps for physical and reference coframes;
- labeled-channel, channel-reversing and conjugated reciprocal transitions;
- screen-frame and screen-metric transitions;
- mixing-bundle transitions;
- trivial and nontrivial global bundles;
- fixed-topology section variations, transition/moduli variations and boundary variations;
- smooth fixed-rank and rank-changing/stratified completion roles.

### Pinned by habit — forbidden

- a single global chart or global coframe;
- global parallel reciprocal/screen splitting;
- zero mixing or round/isotropic screen;
- stationarity, spherical symmetry or `R x S3` topology;
- endpoint-only transport;
- fixed boundary/seal/mirror posture;
- any action, response, source, carrier, density or desired solution.

## Preregistered transition families

1. `LOCAL_ONLY_OBSTRUCTED_OR_UNGLUED` — local reciprocal/extension charts with no global section.
2. `GLOBAL_LABELED_RECIPROCAL_REDUCTION` — a globally compatible reciprocal realization with channel
   labels retained.
3. `GLOBAL_UNLABELED_REVERSAL_REDUCTION` — overlap reversal accompanied by the exact reciprocal
   relabeling law.
4. `GLOBAL_NONTRIVIAL_SCREEN_BUNDLE` — screen frames need not globalize while their metric and mixing
   data do.
5. `GLOBAL_TRIVIAL_COFRAME_WITNESS` — a global coframe exists; retained only as a stronger witness.
6. `REDUCED_HOLONOMY_OR_PARALLEL_SPLIT` — separately conditional; not required for a configuration
   bundle.
7. `RANK_CHANGING_OR_STRATIFIED_RECIPROCAL_OBJECT` — outside the smooth fixed-rank bundle and retained
   as an open completion class.

No family may be removed because it looks nonphysical or complicates later dynamics.

## Preregistered algebraic expectations

These are falsifiable expectations, not conclusions:

1. If physical and reference coframes obey overlap maps `L_ij` and `R_ij`, local extension matrices
   must transform by the two-sided rule

   ```text
   E_j = L_ij E_i R_ij^-1.
   ```

   Compatible cocycles should make the rule associative on triple overlaps.
2. The exact right logarithmic variation should retain the block factorization

   ```text
   delta(E) E^-1 = [[delta(A) A^-1,                 0],
                    [D delta(S) A^-1, delta(D) D^-1]].
   ```

3. The three angular and four mixing variations should remain distinct local chart directions; they
   must not be promoted to propagating modes.
4. A global triangular matrix chart or global coframe should be stronger than, and unnecessary for,
   a global metric/configuration section.
5. Conditional on a global reciprocal reduction, positive screen metrics and mixing sections should
   add no independent existence obstruction: positive bundle metrics have local-to-global convex
   gluing, and the mixing vector bundle has a zero section. This must be proved rather than assumed.
6. The genuine global obstruction should reside in the reciprocal reduction/transition data,
   topology or rank-changing strata—not in solver runtime.

Any failed expectation is retained and regrades the result; no new premise may repair it.

## Variation-domain classifications

Every candidate variation receives exactly one role:

- `PRESENTATION_GAUGE`;
- `LOCAL_CONFIGURATION_TANGENT`;
- `RECIPROCAL_ASSIGNMENT_TANGENT_OPEN`;
- `TRANSITION_OR_GLOBAL_MODULUS_TANGENT`;
- `BOUNDARY_CONFIGURATION_TANGENT`;
- `DISCRETE_SECTOR_CHANGE_NOT_TANGENT`;
- `OBSERVER_QUERY_NOT_FIELD_VARIATION`;
- `CONDITIONAL_ACTION_VARIATION_ONLY`; or
- `BLOCKED_UNTYPED`.

## Completeness map for this one tile

1. **Fields/configuration slots:** complete for the Phase-A object graph; no propagating count.
2. **Action terms:** none loaded.
3. **Field equations:** none loaded.
4. **Domain/coordinates:** all local charts and overlaps in the smooth fixed-rank stratum.
5. **Boundary/regularity:** boundary variation types retained; no boundary law selected.
6. **Topological sector:** trivial, nontrivial, reversal and stratified roles retained.
7. **Dynamical character:** not covered.
8. **Branches:** all seven preregistered transition families retained.
9. **Stability:** not covered.
10. **Regime:** smooth four-dimensional fixed-rank coframe/metric configurations, with defect strata
    explicitly outside rather than filtered.

## Evidence and verifier contract

- Freeze every controlling tracked source by Git blob and SHA-256.
- Build the independent rational transition verifier before recording the final classification.
- Exercise catches for a missing family, hidden global coframe, forced zero mixing, channel-reversal
  sign failure, cocycle failure, a gauge direction counted as physical, topology change treated as a
  tangent, conditional action promotion and an invented global section.
- A fresh zero-context adversarial review is required by repository protocol before a final verdict
  or evidence commit. Because no such reviewer is currently authorized, the package must stop before
  final banking unless Charles explicitly authorizes that review.

## Maximum conclusion

At most:

```text
BOUNDED_EQUIVARIANT_EXTENSION_BUNDLE_AND_VARIATION_TYPE_CLASSIFICATION;
GLOBAL_RECIPROCAL_REDUCTION_OBSTRUCTION_LOCALIZED_OR_RETAINED_OPEN;
NO_NATIVE_LAW_OR_PHYSICAL_BRANCH_SELECTED.
```
