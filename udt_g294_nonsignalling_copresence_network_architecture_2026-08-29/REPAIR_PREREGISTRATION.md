# G294 repair preregistration

Date: 2026-08-29

## R0 — exact matrix comparator

The first production attempt stopped before writing `DERIVATION_RESULT.json`. The generic `exact`
helper simplified a zero matrix correctly but then compared the matrix object to scalar zero, which
returned false.

Repair: branch only on matrix type and use SymPy's exact `is_zero_matrix` property. Scalar
comparison, every formula, all witnesses, tolerances, scope, falsifiers, and candidate landings are
unchanged. No scientific outcome was observed beyond the comparator exception.
