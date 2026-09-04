# G341 audit report — nonprincipal finite null relation and screen carry

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Result

G341 selects preregistered alternative A:

```text
EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION
__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE
__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION
__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS
__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED
```

The exact nonprincipal endpoint map has a positive local determinant and a global monotonicity and
properness proof. Every nonzero universal-cover lift has one future null leg. Both principal limits
remain full-rank in regular Cartesian direction charts. Thus this one exact future null cone has no
positive-time interior conjugate caustic. Compact multiplicity is a family of distinct lattice
lifts; branch crossings are not per-branch caustics.

Direct Levi-Civita transport closes the two screen directions. The natural screen quotient has no
rotation, but every mixed ray has a nonzero G269 endpoint-clock mismatch and hence distinct G298
transported-source and target-local pair planes. At one exact mixed direction the frequency shift
vanishes while that mismatch remains active.

## Evidence

- preregistration committed and pushed at `6f1441f6` before outcomes;
- production checks: `8992/8992`;
- implementation-distinct direct metric/Christoffel checks: `4400/4400`;
- hostile mutations caught: `16/16`;
- aggregate package gates: `20/20`, including unchanged-byte no-write replays;
- repository suite: `220 passed, 1 expected xfail` after compacting redundant startup chronology;
- full 323-row scientific-premise verifier: pass;
- standard-library, dependency-free CPU implementations; GPU not needed;
- analytic global inverse and rank proof; numerical roots are regression evidence only.
- fresh sealed external `gpt-5.4` review authenticated 30 payloads, reproduced all registered
  checks, independently rederived the bounded result, and found no defect at any severity.

## Ownership boundary

Null geodesic and Levi-Civita transport are metric analysis, not imported light dynamics. The
result is restricted to the exact supplied Taub--Kasner spacetime, its normal observers, and
supplied lattice. It does not classify perturbed/generic developments, Jacobi brightness, physical
route populations, or observations.

The metric, kernel, angular sector, and provisional equation remain unchanged. Physical protocol,
topology, occupancy, stability, matter/mass, absolute scale, `X_max`, and canon remain open.

The external reviewer correctly grades the second implementation as implementation-distinct, not
premise-independent, and the aggregate verifier as an integrity gate rather than an automated
proof. The analytic proof carries the global inverse and no-caustic conclusions.
