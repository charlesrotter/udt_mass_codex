# G233 local independent-replay repair preregistration

Date: 2026-08-23

## Observed failure

The first independent exact-Fraction replay passed the metric-jet collision and the load-bearing
next-invariant difference exactly, including `560/81`. It failed only
`radial_unit_field_geodesic`.

Inspection showed that the series arithmetic is truncated at degree 12 while the test demanded
that **all** stored coefficients, including the truncation boundary contaminated by omitted higher
products, vanish. This is a harness error, not a discrepancy in the tested invariant.

## Frozen repair

- Keep `DEGREE=12`, all profile values, and every load-bearing calculation unchanged.
- Introduce `SAFE_DEGREE=8`.
- Test the geodesic acceleration identity only through coefficient 8, leaving four padding orders
  above the checked range.
- Add a guard proving at least four padding orders remain.
- Do not change the expected G233 landing or any metric/invariant comparison.

## Falsification

The repair fails if any safely supported acceleration coefficient is nonzero, if the exact
`560/81` next-invariant difference changes, or if any previously passing load-bearing check fails.
