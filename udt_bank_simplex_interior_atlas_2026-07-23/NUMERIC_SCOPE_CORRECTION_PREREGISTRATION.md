# Numeric-scope correction preregistration

Date: 2026-07-23

Parent preregistration: `PREREGISTRATION.md`, commit `e3c3912`

Status: `PREREGISTERED_AFTER_FIRST_IMPLEMENTATION_STOP__BEFORE_CONVERGED_LATTICE_ATLAS`

## Why this correction is required

The first implementation attempt stopped before writing an atlas because its diagnostic root
bisection assumed that the `B0-B1-B2` face was positive. A subsequent source-neutral feasibility
census found that the original broad interval boxes are also unsuitable for the registered
depth-18 recursion:

```text
J1 initial derivative-indeterminate boxes: 2,702,690
J2 initial derivative-indeterminate boxes: 2,437,426
total:                                    5,140,116
```

The broad four-variable interval extensions overestimate derivatives away from the null set.
Recursively bisecting every such box through depth 18 would grow exponentially and would not be a
credible bounded computation. This is a solver/completeness defect, not a physics result.

The original preregistration remains unchanged as historical evidence. This correction replaces
only its continuous full-cover certification claim and maximum conclusion. It does not remove a
candidate, chart, bank, carrier, mask, field, sector, sign, or observed configuration.

## Corrected frozen observation map

Every one of the same 384 groups and both charts must be evaluated on two complete symmetric
barycentric simplex lattices:

| level | `u` nodes | triangular simplex denominator | simplex nodes | `t` nodes |
|---|---:|---:|---:|---:|
| L1 | 9 | 8 | 45 | 65 |
| L2 | 17 | 16 | 153 | 129 |

The triangular nodes are all exact barycentric triples

```text
(q0,q1,q2)=(i,j,k)/Nq,  i+j+k=Nq.
```

Every node uses all four weights

```text
(w0,w1,w2,w3)=((1-t)q0,(1-t)q1,(1-t)q2,t).
```

No result may be filtered by shape or physical interpretation. The following are recorded for every
chart/group and both levels:

- positive, negative, and numerically zero node counts;
- sign-transition count on every `t` fiber;
- connected components of the base-face positive and negative node sets using the exact triangular
  lattice adjacency and `u` adjacency;
- inferred sampled null/positive/negative component counts, with `OBSERVED_LATTICE` status only;
- root-position ranges by transition interpolation;
- complete raw sign arrays, lattice coordinates, commands, environment, and hashes.

L2 must reproduce L1's qualitative component/root-count class or the sheet is
`RESOLUTION_DEPENDENT_UNRESOLVED`.

## Corrected interval and independent evidence

The original complete `8 x 8 x 8 x 16` interval pass remains in scope as a full-domain sign/
derivative enclosure census. It must:

- report every certified and indeterminate box count;
- make no continuous-topology claim from an indeterminate box;
- preserve the full deterministic cell-stream hash;
- retain any strictly opposite-sign box as an existence witness.

At least 24 deterministic load-bearing nodes/boxes must be checked with at least 80-decimal interval
arithmetic. The anchor set must span:

- both charts;
- all eight masks;
- at least twelve carriers;
- base-face sign extrema;
- lower and upper interface transitions where present;
- the narrowest recorded margins.

An independent implementation must reconstruct the complete `4 x 4` metric matrix from the
registered `h`, `q`, and shift blocks and compute `s` through determinant/adjugate or a general
matrix inverse. It must reproduce every L1/L2 node sign and transition class. Reusing the production
inverse-coframe scalar is forbidden in that independent route.

The six earlier edge sheets remain exact boundary controls. Edge agreement cannot certify the
interior.

## Corrected classifications

Continuous words such as `proved`, `unique`, `hypersurface topology`, or `full continuous
component` are forbidden unless a separate continuous certificate exists.

Allowed primary lattice classes are:

- `ONE_TRANSITION_FAMILY__ONE_SAMPLED_NULL_COMPONENT`;
- `ONE_OR_TWO_TRANSITION_FAMILIES__TWO_SAMPLED_NULL_COMPONENTS`;
- `MORE_COMPLEX_SAMPLED_TRANSITION_OR_COMPONENT_STRUCTURE`;
- `RESOLUTION_DEPENDENT_UNRESOLVED`.

Every class carries `OBSERVED_BOUNDED_LATTICE`, not `DERIVED`.

## Corrected catch-proofs

The verifier must additionally reject:

- omission of either resolution;
- a non-barycentric or incomplete triangular lattice;
- failure to evaluate all 768 chart/group sheets;
- a missing raw sign array;
- L1/L2 disagreement silently accepted;
- a sampled transition promoted to a continuous root theorem;
- a pointwise matrix agreement described as interval certification;
- an indeterminate interval box omitted or coerced to a sign;
- a connected-component count that ignores triangular or `u` adjacency;
- duplicate `r=0` or `t=1` chart coordinates counted as physical components.

## Corrected maximum conclusion

The maximum bankable conclusion is now:

`BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_WITH_INTERVAL_AND_MATRIX_CHECKS`

This is one mapped tile of the registered analytic ensemble, not a continuous arbitrary-metric
solution-space theorem. Action, EOM, dynamics, global completion, carrier, source, scale, boundary,
and physical interpretation remain unloaded and open.
