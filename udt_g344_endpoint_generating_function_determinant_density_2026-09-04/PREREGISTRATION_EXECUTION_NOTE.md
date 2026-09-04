# G344 preregistration execution note

Date: 2026-09-04

## Additive endpoint-function qualification

After the frozen production and independent checks passed, analytic proof-writing exposed a type
qualification in preregistration requirement 2. The G343 canonical map fixes every coefficient of
the homogeneous quadratic endpoint generator. A general generating function, however, may also
contain an arbitrary screen-position-independent function `k(T1,T0)`. Endpoint derivatives with
respect to screen position, the recovered phase-space map, the mixed Hessian, and its determinant
density cannot detect that function.

Therefore the preregistered phrase “unique ... up to an additive endpoint-independent constant in
each connected endpoint-order component” is too strong if `T0,T1` are allowed to vary. The exact
classification to be tested on rerun is:

- the homogeneous quadratic representative is unique and is normalized by `k=0`;
- the unrestricted generator retains `k(T1,T0)`;
- exact composition requires `k(T2,T0)=k(T2,T1)+k(T1,T0)`;
- reversal requires `k(T0,T1)=-k(T1,T0)`;
- on a one-dimensional ray interval such a regular cocycle is an endpoint coboundary
  `k(T1,T0)=f(T1)-f(T0)`;
- this endpoint gauge does not alter any G344 Hessian or density result.

This qualification does not change the frozen block formula, endpoint domain, primary alternatives,
tolerances, samples, or maximum physical conclusion. It weakens only the uniqueness wording and
adds an explicit `CHOSE_GENERATOR_NORMALIZATION` stamp. All production, independent, and hostile
checks will be rerun after this note is committed. Nonmonotone ordered triples will also be added as
coverage of the already-frozen arbitrary-triple domain; they do not alter a candidate or tolerance.
