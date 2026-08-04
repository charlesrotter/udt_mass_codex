# Audit report — metric-natural reciprocal/screen split selectors

Date: 2026-08-04

Grade: `VERIFIED_WITH_CAVEATS_BOUNDED_METRIC_NATURAL_SELECTOR_ATLAS`

## Result first

The complete metric can select a reciprocal clock/ruler plane on some broken-symmetry strata, but
it cannot select one unique smooth plane on the full retained metric domain.

The obstruction is exact on the registered round complete `R x S3` control. Its metric selects the
ultrastatic time line, while spatial `SO(3)` symmetry selects no ruler line. The full commutant
calculation admits invariant projector ranks only

```text
0, 1, 3, 4,
```

not the rank two required by a Lorentzian clock/ruler plane. This rules out one universal unique
metric-natural split on any retained domain containing that branch. It does not prove that a future
native law cannot exclude or add structure to the branch.

The positive side is equally exact. A metric-self-adjoint curvature operator with distinct causal
simple eigendirections gives a polynomial rank-two projector. The construction is idempotent,
metric-self-adjoint, and equivariant under an exact rational Lorentz boost. The squashed complete
`S3` control realizes this geometry conditionally: ultrastatic time plus its unoriented simple
Ricci/Hopf line. In the reordered homogeneous frame its Ricci spectrum is
`(0,1/2,3/2,3/2)`, and the exact algebraic control is `A=2I+2 Ric#`. The branch is off shell and
does not select physics.

The selector cannot be continued uniquely through the round limit. Two simple-spectrum families,
related by the round spatial isometry rotating the squashing axis, reach the same round curvature
operator with different limiting rank-two projectors. At the collision, the natural object is the
two-dimensional orbit of all unoriented spatial lines, not one member.

The frozen intrinsic two-form family supplies a second branch-local positive result: six candidates
have an exact rank-two kernel on their nonzero loci. The same construction becomes rank four on its
zero graph and fails unique projective continuation on three great circles. The zero, blocked, and
degenerate controls remain in the census.

## The three architectures are now distinct

1. **Query bundle:** every ordered observer/ruler query carries a tautological reciprocal plane on
   the total pair-frame bundle. This is already derived and does not itself derive a natural
   spacetime section; smooth sections can exist without being selected.
2. **Branch-derived split:** curvature, Hessian, symmetry, holonomy, or intrinsic forms can derive a
   plane where their spectra/ranks are regular. These are stratified and can fail at ties or zeros.
3. **Realized universal field:** one smooth `N` over spacetime would require an additional rule or a
   domain that removes the certified symmetry/defect obstructions. It is not currently derived.

A chosen coframe's first two legs constitute a fourth, conditional input architecture. They are not
metric-natural if local Lorentz-related coframes represent the same metric.

## Why this is not another generic underdetermination

The audit gives a positive mechanism, a negative theorem, and their exact join:

```text
broken symmetry / simple spectrum / nonzero intrinsic form
    -> branch-local natural plane;

round symmetry / eigenvalue collision / zero or rank change
    -> no unique smooth member;

all observer queries
    -> tautological total-space plane, no natural spacetime section selected.
```

The missing question is no longer merely “which plane?” It is whether UDT's still-open laws need a
single spacetime plane at all, or can be formulated on the query bundle and descend without one.

## Complete candidate disposition

`SELECTOR_OUTCOMES.tsv` classifies all 18 preregistered routes. It retains zero-jet metric data,
coframe presentation, query data, `phi` jets, Ricci and Riemann/Weyl spectra, scalar gradients,
Killing symmetry, holonomy, intrinsic forms, round and squashed complete controls, whole-solution
and boundary/topology operations, set-valued outputs, rank-changing atlases, and excluded
action/dynamical selection.

Riemann/Weyl, joint-gradient, Killing, and holonomy routes are conditional capabilities, not frozen
complete witnesses. The round isometry obstruction reaches every unique metric-natural nonlocal or
whole-solution construction on that exact control; positive nonlocal capability on less-symmetric
branches remains unclassified. Boundary/topology routes may decorate or change the domain but have
no registered selector operation. Action/dynamical selection remains downstream and excluded.

## Evidence gates during repair replay

1. **Preregistered:** yes, commit `ae8afa98`, with 18 selectors, 18 premises, 10 falsification
   contracts, and 28 source hashes frozen before outcome algebra.
2. **Full or bounded:** complete for the frozen 18-class universe at each class's documented
   evidence level; not every natural operation on every Lorentzian manifold.
3. **Independent:** SymPy 1.13.1 production and a separate standard-library `Fraction`
   implementation independently reconstruct the commutants, projector, boost covariance, rotated
   collision, and orbit dimension. The intrinsic-form theorem is inherited from its previously
   fresh-reviewed parent and is replayed here only by frozen hash and census, not independently
   rederived. The fresh semantic adversary returned `PASS_WITH_REQUIRED_REPAIRS`, then
   `REPAIRS_ACCEPTED` after all five repairs and six added semantic catches were replayed.
4. **Premises:** all are stamped; `CORRECTION_LAYER.md` narrows the committed preregistration's
   shorthand section wording without rewriting it.

Repository gates pass: six frozen manifests, 127 members/133 paths, 1,114 current paths, 101
frontier targets, current premise guards, 83 metadata-identical unrelated untracked paths, and tests
`70 passed, 1 xfailed`.

## Maximum conclusion

Maximum conclusion retained by the fresh review:

```text
BRANCH_LOCAL_SELECTORS_ONLY_UNIVERSAL_OBSTRUCTED
```

within the exact retained domain and caveats above.

No physical split, branch, profile, action, source, carrier, boundary, bootstrap equation, density,
`X_max`, matter, mass, stability, dynamics, phenomenology, or canon follows.
