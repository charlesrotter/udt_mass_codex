# Independent verification note

The load-bearing differential-form and conformal-weight results were
recomputed by
`verify_hopf_transport_bootstrap_independent.py`.

It:

- uses only the Python standard library and exact `Fraction`
  arithmetic;
- does not import SymPy or the production controller;
- tests the torsion-corrected exterior-derivative identity on 17
  independently constructed exact rational cases;
- observes 16 cases in which the naive torsionful covariant rewrite
  differs from the true exterior derivative;
- independently recomputes the three-dimensional conformal weights of
  the two- and four-derivative energy terms;
- checks the primitive gauge identity and the distinction between
  principal-bundle and affine-tangent connections; and
- exercises all 13 preregistered fail-closed catches.

Result:

```text
9/9 exact checks passed
13/13 catch-proofs passed
5/5 production/result agreement checks passed
```

This is independent algebraic verification, not an independent
physical model or a new carrier derivation.
