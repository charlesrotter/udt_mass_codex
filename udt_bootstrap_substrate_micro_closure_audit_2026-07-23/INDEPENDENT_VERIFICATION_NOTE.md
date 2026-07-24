# Independent verification note

The independent verifier uses Python standard-library arithmetic and
`fractions.Fraction`. It does not import SymPy or the production controller.

It independently checks:

- fixed-embedding pullback variation with rational matrices;
- `q` and `q^-1` conformal weights;
- the nonconstant conformal Laplacian identity using rational polynomials;
- constant-homothety stationarity and physical-radius cancellation;
- the `+1/-1` metric trace weights;
- phase-covariant derivative and curvature-gauge cancellation;
- all candidate, regrade, fixed-point, completion, and authority counts;
- fail-closed mutations promoting density insertion, the stronger local fork,
  a completion, a density-curvature relation, or pure homothety.

Result:

```text
exact 11/11
table/authority agreement 13/13
fail-closed catches 11/11
```

No fresh zero-context model review was launched because additional agents
were not authorized for this audit. The final grade therefore remains
`VERIFIED-WITH-CAVEATS`.
