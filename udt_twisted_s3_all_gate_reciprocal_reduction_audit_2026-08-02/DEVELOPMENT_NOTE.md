# Development note

Two pre-outcome runs stopped on implementation assertions before any candidate determinant was
reported. The first compared algebraically equivalent Christoffel polynomials structurally; the
second checked lower-index symmetry before the transposed tensor entry had been populated. The raw
second traceback is retained in `DERIVATION_ERROR.txt`.

The initial repeated symbolic-differentiation implementation was then stopped as throughput-limited
after four minutes without an outcome. It was replaced by an exact finite-jet implementation of the
same preregistered diagnostic. No candidate, point, invariant, physical premise, or conclusion rule
changed. The successful code checks its formal inverse, Christoffel symmetry, and Ricci symmetry
exactly before emitting any determinant.
