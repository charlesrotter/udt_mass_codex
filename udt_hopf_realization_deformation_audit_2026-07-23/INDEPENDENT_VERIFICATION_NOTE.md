# Independent verification note

`verify_hopf_realization_deformations_independent.py` uses only the Python
standard library and exact `Fraction` arithmetic. It imports neither SymPy
nor the production controller.

It independently:

- evaluates the seed and both tangent directions at four exact rational
  stereographic/polar samples;
- verifies unit norm, tangency, orthogonality, and both exact tangent norms;
- checks exact and nonexact phase-connection witnesses;
- verifies curvature invariance under an exact gauge shift;
- checks angular-eigenaxis degeneracy at isotropy and spin-two basis
  covariance;
- parses all twenty deformation and twelve completion outcomes; and
- exercises all fifteen preregistered fail-closed catches.

Result:

```text
11/11 exact checks
15/15 catch-proofs
6/6 cross-result agreements
```

This is an independent exact implementation, not a fresh zero-context model
review or a second physical model family. The evidence grade retains that
caveat.
