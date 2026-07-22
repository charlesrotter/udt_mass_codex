# Implementation Preregistration

Date: 2026-07-22

This note fixes implementation details before the new Q01/Q02 census is run.

## Q01 finite generator compression

The complete bounded table will contain one row for every codomain family registered in
`PREREGISTRATION.md` and separate rows for each primitive order-zero, order-one, and order-two
generator class. “Arbitrary smooth scalar coefficients” is represented as one explicit infinite
functional-calculus row. It may not be counted as a finite formula census.

Order-two operator coverage is accepted only by exact manifest linkage to the already complete
31-family lattice and nine-family joint invariant-subspace atlas. This package will not regenerate
those outcomes merely to inflate evidence.

## Q02 anchors and finite differences

The independent direct-covariant-derivative anchors are fixed as the following 32 identities:

- for every mask `M0` through `MF`, `R00_1_M?_B0_P0`;
- for every mask `M0` through `MF`, `V016_M?_B3_P7`.

This samples both the smallest registered radial carrier and the last interior carrier in every
structural mask without looking at a curvature outcome.

Direct centered coordinate derivatives use `h=10^-4` and `h=5*10^-5`. The independently transported
antisymmetric shell difference at the same `h` values must agree in algebra dimension and to
relative tensor residual `2*10^-5`; convergence must improve or remain below that gate when `h` is
halved. Any failure is retained.

The all-row transported-curvature shells remain `h=10^-3` and `h=5*10^-4`, with 33- and 65-node
RK4 transport. A shell row is numerically certified only when:

- the 33/65 transport matrices agree within `2*10^-9` relative;
- metric isometry at 65 nodes is within `2*10^-9` relative;
- both shell spacings give the same algebra dimension and reducibility class; and
- no decisive singular value lies in the registered `10^-11..10^-7` uncertainty band.

For configurations whose metric amplitudes are all analytically zero, the explicit family is a
constant metric. Such a row is certified exactly flat after direct zero checks on the metric first
and second jets at the base and at all eight shell endpoints. It is not inferred flat from a small
curvature norm.

## Retained classifications

Every configuration receives exactly one final class:

- `BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE`;
- `TRANSPORTED_CURVATURE_FULL_IRREDUCIBLE_BOUNDED`;
- `PROPER_COMMON_REDUCTION_OBSERVED_BOUNDED`;
- `EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS`;
- `NUMERIC_UNCERTAIN_RETAINED`; or
- `OPEN_NONFULL_BEYOND_SHELL_SCOPE`.

No class is ranked by physical merit.

