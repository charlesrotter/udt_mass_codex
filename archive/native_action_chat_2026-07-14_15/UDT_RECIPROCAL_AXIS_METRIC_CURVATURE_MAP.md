# UDT reciprocal-axis metric curvature — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic manufactured-field curvature audit; DATA-BLIND |
| Immediate predecessor | UDT_RECIPROCAL_LOOP_CLOSURE_MATTER_DERIVATION_RESULTS.md |
| Metric status | Single-axis completion is CONDITIONAL, not adopted |
| Action status | \(C^2\) is CONDITIONAL on the recorded CSN/minimality premises |
| GPU | Not authorized; exact pointwise tensor algebra first |
| Banking | None; LIVE.md and CANON.md remain untouched |

## Question

Does the metric-only conformal invariant \(C^2[g(\phi,n)]\) reduce to the historical area-only
carrier \(F^2\), or does the metric assign curvature cost to rank-one reciprocal-axis textures for
which \(F=0\)?

## Conditional metric

\[
g_{00}=-e^{-2\phi},
\qquad
g_{ij}=\delta_{ij}+(e^{2\phi}-1)n_i n_j,
\qquad
n\cdot n=1.
\]

This is used as a manufactured invariant probe, not varied as a restricted action before the full
covariant equations.

## Pre-registered decisive field

Take constant

\[
q=e^{2\phi}>0
\]

and a rank-one helical axis texture

\[
n(z)=(\cos kz,\sin kz,0).
\]

All derivatives are proportional to \(dz\), hence

\[
F_{ij}=0
\]

identically. Compute the full four-dimensional connection, Riemann tensor, Ricci tensor, scalar
curvature, and Weyl norm without linearization.

## Tests

### T1. Exact metric derivatives

At \(z=0\), derive \(g,\partial_zg,\partial_z^2g\) exactly. Verify:

- \(q=1\) gives a constant flat metric independent of \(n\);
- \(k=0\) gives a constant flat metric;
- determinant is constant.

### T2. Full curvature

Build Christoffels from the metric and compute

\[
R_{\mu\nu\rho\sigma},\quad
R_{\mu\nu},\quad
R,\quad
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}.
\]

Audit index order, signs, symmetries, contractions, and the four-dimensional Weyl subtraction.

### T3. Functional discrimination

- If \(C^2\ne0\) while \(F^2=0\), the metric-native conformal action is strictly larger than the
  area-only carrier.
- If \(C^2=0\) for every \(q,k\), the rank-one discriminator is passed but equivalence to \(F^2\)
  remains unproved.

### T4. Exact dependence

Determine the exact \(k\)- and \(q\)-dependence. Verify at multiple rational \(q\), and derive or
interpolate only after the tensor calculation fixes the functional form.

### T5. Scope

State whether nonzero curvature is Weyl or only Ricci. Do not infer a stable soliton, field equation,
or native action from one manufactured invariant.

## Acceptance gates

- No finite differences or linearization.
- The time component and full four-dimensional Weyl tensor must be included.
- \(F=0\) must be proved from rank-one dependence, not assumed from a sample point.
- Restricted substitution is an invariant diagnostic only, not a valid replacement for full metric
  variation.
- Sign-convention changes may flip \(R_{\mu\nu\rho\sigma}\) and \(R\), but not \(C^2\).
- A nonzero result falsifies area-only equivalence only inside the conditional single-axis/conformal
  branch.

## Possible outcomes

1. **RANK-ONE WEYL COST:** \(F=0\) but \(C^2>0\).
2. **RICCI-ONLY RANK-ONE COST:** \(F=0\), \(C^2=0\), but Ricci curvature is nonzero.
3. **RANK-ONE FLAT:** all curvature vanishes.
4. **TENSOR AUDIT UNRESOLVED:** implementation or convention checks fail.

