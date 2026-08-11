# Numeric-detail preregistration for the external-review closure replay

Date: 2026-08-11

Parent preregistration commit: `0d5a57ad`

This additions-only record fixes implementation details that were not numerically explicit in the
first external-review adjudication preregistration. It is committed before the new verifier exists
or returns any value.

## Fixed finite-difference details

- Surface first and second jets use the centered fourth-order five-point formulas with fixed step
  `5e-4` in query coordinates.
- Outer Codazzi derivatives use the registered scale itself in the centered fourth-order five-point
  first-derivative formula.
- Intrinsic and normal connection coefficients at the evaluation point use centered fourth-order
  five-point derivatives with step `5e-4`.
- Ambient Christoffel symbols use fourth-order metric derivatives with step `1e-5`.
- Ambient curvature uses fourth-order Christoffel derivatives at `5e-4`, repeated at `2.5e-4` for
  the registered control.

## Fixed normal-loop details

- The independently reconstructed raw normal connection is integrated around the counterclockwise
  square of half-width `0.01`.
- Each straight-edge substep uses a midpoint matrix exponential `exp(-omega_i dq^i)`, with exactly
  `16`, `32`, and `64` subdivisions per edge.
- The raw connection is used. No polar projection, antisymmetrization, or post-hoc orthogonalization
  is allowed.
- The reported area is exactly `(2*0.01)^2 = 0.0004` in query coordinates.
- The frozen comparison value is the production Q2 normal-loop Frobenius norm
  `6.019832007454665e-06`; it is a comparison target only and is not read by the verifier.

No numerical value may be retuned after the return.

