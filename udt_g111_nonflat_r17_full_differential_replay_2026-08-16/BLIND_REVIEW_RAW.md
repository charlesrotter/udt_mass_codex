# Fresh zero-context blind review — raw return

Landing: `REPAIRS_REQUIRED`

No core sign or geometric error was found, but the package did not satisfy its own preregistered
certification contract.

## Decisive failures

- F03 required independent brackets, connection, and Riemann agreement “exactly.” The independent
  route compared only downstream floating-point invariants and pair coefficients under tolerances;
  it never componentwise compared brackets, connection, or Riemann.
- The numerical tolerances were not frozen in the preregistration. The default replay passed, but a
  half-step probe failed trace and norm thresholds; larger steps improved residuals. This supported
  production but was not a preregistered convergence certificate.
- F10 required actual same-`W`, twist-sign, Riemann-contraction, and vertex mutations. The original
  catch script mostly asserted saved-output properties: no Riemann-contraction mutation existed,
  the same-`W` catch was only a nonzero tidal norm, and the vertex catch tested a literal string.
- F05 normalization was true for the hard-coded axial bases, but no exact residual was recorded.
  The mixed zero residual subtracted an expression from itself, and the vertex condition was
  registered as a string rather than evaluated.

## What verified

- Maurer--Cartan signs and the six-independent-component scalar two-jet are correct.
- Koszul, Riemann index order, the noncoordinate bracket term, tensor symmetries, and Jacobi sign
  are correct.
- The pair series and `phi_pair'(0)=<U,A>` are correct.
- The optical tidal contraction, cubic Jacobi coefficient, and oriented axial screens are correct.
- The pair-screen rank-at-most-one theorem is correct.
- The census has 1,152 unique keys with the preregistered cardinalities.
- R17, profile, observer carry, and query remain supplied/conditional; no hidden physical selection
  or observation entered.

## Required repairs

1. Add an implementation-distinct exact componentwise bracket/connection/Riemann verifier.
2. Replace F10 assertions with executable mutations, especially the missing Riemann contraction.
3. Add exact null/screen/vertex residuals and independently form the mixed coefficient.
4. Treat the finite-difference replay as supplementary unless a new preregistered tolerance and
   convergence contract is supplied.

Maximum justified pre-repair claim: `LEAD`.

The reviewer ran the pre-blind package verifier and all three calculation scripts in an isolated
temporary copy. It did not edit the repository or inspect sources outside the manifest.
