# G196 independent-verification preregistration

Date: 2026-08-20

This freezes the independent numerical leg before its first outcome-producing run. The verifier may
not import `derive_longitudinal_screen_mixing.py` or read `PRODUCTION_RESULT.json`.

## Independent method

- reconstruct the full four-dimensional coframe metric with Torch `float64` automatic
  differentiation through second metric jets;
- assemble inverse metric, Christoffel symbols, connection derivatives, and Riemann curvature by
  explicit index contractions in an implementation independent of SymPy;
- contract the central outgoing null ray and normalized screen directly from that reconstructed
  metric;
- compare against a separately coded candidate using
  `D_plus M = partial_eta M + partial_z M`;
- integrate the direct second-order coordinate Jacobi equation and the ordered `L,K`
  representation with SciPy `DOP853` and compare them pointwise.

## Frozen census

- seed: `1960820`;
- 12 named histories;
- 192 seeded random histories;
- total: 204 histories;
- three off-origin curvature points whose `eta-z` values are not all equal;
- forward and backward IVP intervals on multiple outgoing-ray offsets.

Every random matrix entry contains independently drawn `eta`, `z`, `eta^2`, `z^2`, `eta*z`, and
oblique sinusoidal terms. The common scale remains a positive exponential function of `eta` only,
as declared in the G196 family.

Named controls must include:

1. zero mixing;
2. the `z`-independent G195 limit;
3. pure longitudinal-gradient strain;
4. a field depending on `eta-z`;
5. pure spacetime-dependent antisymmetric rotation;
6. a fully noncommuting strain/rotation field;
7. a rank-transition field;
8. a rotation-zero-crossing field;
9. an active `eta*z` cross-term field;
10. a large-but-regular field;
11. a same-ray base history;
12. an off-ray alias that differs from the base by a nonzero multiple of `(eta-z)^2` and is
    therefore identical, together with its `D_plus` jet, on the `eta=z` ray.

## Frozen numerical gates

- tensor ceiling: `3e-8`;
- algebra ceiling: `3e-10`;
- `DOP853` relative tolerance: `2e-12`;
- `DOP853` absolute tolerance: `2e-13`;
- every sampled central pair metric, frequency, affine-ray residual, screen connection, and optical
  tide must pass;
- direct and ordered-factor Jacobi maps must agree below the tensor ceiling;
- every sampled nonvertex determinant must be positive;
- the same-ray alias pair must agree on the selected ray below the algebra ceiling and differ at a
  preregistered off-ray point by more than `1e-4`;
- the noncommuting, rank-transition, rotation-crossing, independent-`z`-gradient, and mixed-jet
  controls must each be demonstrably active.

The implementation will freeze its exact assertion and hostile-catch counts in an execution note
before the first outcome-producing run.

## Falsification

The production landing fails if the independent reconstruction finds any separately weighted
`partial_z`, `partial_eta-partial_z`, or other spatial jet in the central tide; if affine or pair
typing fails; if direct and ordered factor maps disagree; or if a nonvertex determinant reaches
zero on a declared regular interval.

## Maximum conclusion

Passing certifies only the declared `M(eta,z)`, `a(eta)`, central outgoing affine-germ family. It
does not select a physical profile, another null direction, an observer population, a global
completion, a transfer law, observational coefficients, or `X_max`.
