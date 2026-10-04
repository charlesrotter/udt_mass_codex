# Numerical scope clarification

All 40 incidence solves and their quadratures use the two frozen precisions,
36 and 60 decimal digits. The script sets 65 digits only when parsing/subtracting
the saved decimal strings for the final comparison of those two levels. It
performs no new incidence solve, quadrature, parameter case or refinement at 65.
This comparison arithmetic is not a third solution-precision study. Both genuine
solution levels and the comparison setting are retained in the source.

The code symbol b is declared positive for symbolic simplification, but the
identities are algebraic in b and the numerical examples explicitly include
both signs. The actual outward/null-domain inequalities, not b's sign, control
the construction. Numerical spot directions remain equatorial two-component
examples; they do not certify a two-dimensional astronomical image map.
