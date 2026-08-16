# Preregistration — G111 nonflat R17 observer full-differential replay

Date: 2026-08-16

Mode: metric-led exact local-jet replay on a supplied globally regular analytic complete metric

## Whole question

Does the G110 observer-exponential reconstruction remain type-correct and nontrivial when replayed
on a genuinely nonflat complete UDT coframe with reciprocal, angular, and twist sectors present,
without identifying the terminal-pair screen projection with the sky Jacobi map or selecting the
metric as physical?

## Bounded geometry

Use the already registered stationary R17/W01 coframe on `R x S3`,

```text
theta0=u^-1(dt+a sigma3),  theta1=u sigma3,
theta2=v sigma1,           theta3=v sigma2,
u=exp(phi),                v=exp(lambda_R phi).
```

The supplied analytic profile is `phi(q)=epsilon*q0` on the unit-quaternion presentation of `S3`.
This is a global smooth bounded control, not an on-shell equation or physical history. Evaluate the
exact two-jet at the eight sign choices `q=(+/-1,+/-1,+/-1,+/-1)/2` with positive first component,
both `epsilon=+1/5,-1/5`, both twists `a=+1/4,-1/4`, and all six already registered R17 screen
weights `lambda_R=(-2,-1,0,1/2,1,2)`. No case may be discarded.

At each control use observer tangent `U=e0` and the six axial sky directions `n=+/- e_i`. The null
initial tangent is `K=U+n`. The celestial direction is held in the supplied orthonormal coframe
along the observer for this bounded query; that carry is query data, not a universal law.

## Exact objects

1. Derive the complete frame brackets from the coframe and the quaternion profile jets.
2. Derive all Levi-Civita coefficients by Koszul and the full ambient Riemann tensor.
3. Form the terminal-pair Jacobi data `J_tau(0)=U` and
   `nabla_K J_tau(0)=nabla_U K`.
4. Form the angular Jacobi data `D_sky(0)=0` and `D_sky'(0)=I` in matched bases.
5. Compute the exact local series through the first curvature-sensitive orders.
6. Keep the pair block, angular block, and mixed contractions distinct throughout.

## Premise ledger in words

- R17 coframe and six `lambda_R` strata: `pinned-by-SUPPLIED_CONDITIONAL_SOURCE`.
- Unit-quaternion realization and analytic profile family: `free-and-explored` controls.
- `epsilon`, `a`, evaluation points, and axial sky census: `free-and-explored`; bounded, not selected.
- Observer and coframe-held celestial carry: `QUERY_SUPPLIED`.
- Levi-Civita exponential/Jacobi construction: `DERIVED_CONDITIONAL` from the supplied metric.
- Physical metric history, observer population, global endpoint weights, SNe, and `X_max`: `OPEN`.

## Certification and falsification contract

The replay passes only if:

1. all frozen source hashes match;
2. every control metric is Lorentzian and the coframe is nonsingular;
3. independent constructions reproduce the frame brackets, connection, and Riemann tensor;
4. Riemann antisymmetry, pair exchange, and first Bianchi residuals are exactly zero;
5. the null and screen normalization residuals are exactly zero;
6. the canonical pair-screen projection has rank at most one in every control;
7. the angular map has the correct vertex data and at least one retained control has nonzero optical
   tidal curvature, so the nonflat replay is not vacuous;
8. every registered control is reported, including degeneracies;
9. hostile mutations of the same-`W` identification, twist sign, Riemann contraction, and vertex
   normalization are caught.

Any failed structural item returns `TYPE_OR_ALGEBRA_FAILURE`. A regular but zero-curvature or
degenerate control is characterized, not filtered. The package may not use an SNe value or outcome.

## Maximum conclusion

At most G111 may show that the G110 distinct-block observer differential survives this bounded
nonflat complete-metric family and expose its exact local curvature response. It cannot select R17,
choose a physical history, derive a global observer relation, validate SNe, select a regime score,
or infer `X_max`, action, source, matter, bootstrap, or signalling.
