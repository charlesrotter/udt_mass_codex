# Performance-refinement preregistration

Date: 2026-08-11

Parent preregistration commit: `d1713018`

## Trigger

The first production invocation was manually interrupted with exit code `130` after approximately
ten minutes and before any result file or stdout result was produced. Adaptive loop integration was
reconstructing the same nested Fermi-surface jets many times. No outcome was available to inspect.

## Frozen scientific object

The two witnesses, query definitions, coframes, metric, connection, pair immersion, derivative
scales, loop widths, tolerances, output channels, falsification contract, and maximum conclusion in
`PREREGISTRATION.md` remain unchanged.

## Mechanical refinement

1. Cache each surface point and each complete base jet by query coordinates.
2. Retain adaptive DOP853 for the observer geodesic, ruler transport, and spacelike exponential
   rulings with the registered tolerances.
3. Replace nested adaptive integration of already-evaluated loop connections by path-ordered
   midpoint matrix exponentials on each of the four registered rectangle edges.
4. Evaluate loop transport at `8`, `16`, and `32` subdivisions per edge. The `32`-subdivision value
   is the production readout; `8->16->32` differences are recorded as quadrature convergence.
5. Compute ambient and normal transport from the same cached surface points. No curvature-derived
   shortcut may replace either finite loop return.

This is a numerical reuse/refinement only. A failure to converge remains
`NUMERICALLY_UNRESOLVED_COMMON_IMMERSION_TEST` and may not be repaired by dropping a channel.
