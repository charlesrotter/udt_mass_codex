# UDT reciprocal-axis functional structure — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic off-shell provenance and exact principal-jet audit; DATA-BLIND |
| Immediate predecessor | `UDT_RECIPROCAL_AXIS_METRIC_CURVATURE_DERIVATION_RESULTS.md` |
| Locked foundation | Reciprocal-c Identity; Reciprocity; Common-Scale Neutrality |
| Conditional branch | Four-dimensional, local, parity-even, metric-only, lowest-order conformal action `S_C proportional to integral sqrt(-g) C^2` |
| Axis completion | CONDITIONAL diagnostic parametrization, not adopted field content |
| GPU | Not authorized; continuum operator must be fixed first |
| Banking | None; `LIVE.md` and `CANON.md` remain untouched |

## 1. Questions

1. Does substituting the conditional reciprocal-axis metric into `C^2` yield a first-derivative
   quartic carrier, or does it contain irreducible second derivatives of the axis/depth variables?
2. Is the axis `n` an independent covariant field, or only a restricted parametrization of the
   metric?
3. What exact positive/indefinite structure occurs in the simplest unrestricted one-coordinate
   jet `q(z), theta(z)`?
4. Can any carrier numerics be justified before the full off-shell field space and boundary
   variation are specified?

## 2. Conditional metric probe

Use

\[
g_{00}=-q^{-1},
\qquad
g_{ij}=\delta_{ij}+(q-1)n_i n_j,
\qquad
q=e^{2\phi}>0,
\]

and, for the exact one-coordinate principal-jet audit,

\[
n(z)=(\cos\theta(z),\sin\theta(z),0).
\]

At a chosen point rotate the spatial calibration basis so that `theta=0`, and denote

\[
u=q',\qquad v=q'',\qquad p=\theta',\qquad s=\theta''.
\]

Compute the full four-dimensional curvature before making any action or field-equation claim.

## 3. Pre-registered tests

### T1. Off-shell provenance

Distinguish explicitly:

- unrestricted metric variation of `S_C[g]`;
- substitution `g=g(q,n)` as an invariant/solution diagnostic;
- treating `q,n` as independent fields and varying a reduced action.

The third operation is not equivalent to the first unless the conditional parametrization spans
the required metric variations or a separate constrained-field principle is supplied.

### T2. Principal second-jet discriminator

At `u=p=0`, allow `v` and `s` independently. If `C^2` contains nonzero `v^2` or `s^2`, then the
reduced carrier is genuinely second-derivative squared and its Euler equation is generically fourth
order. It cannot be identified with the historical first-derivative area norm by integration by
parts alone.

### T3. Full one-coordinate jet

Derive exact expressions for

\[
R,\quad R_{\mu\nu}R^{\mu\nu},\quad
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma},\quad C^2
\]

as functions of `(q,u,v,p,s)`. Audit tensor identities and at least twelve exact manufactured jets.

### T4. Limiting sectors

Check:

- `q=1` with variable axis;
- constant `q` with general `theta(z)`;
- constant axis with variable `q(z)`;
- affine constant-depth twist;
- vanishing first jets but nonzero second jets.

### T5. Variational consequence

For constant `q`, derive the exact reduced Euler operator for `theta(z)`. State boundary data needed
for differentiability. Do not promote the reduced equation to the unrestricted metric equation.

### T6. Scale/topology discipline

Check common-scale weight and derivative scaling. Do not infer a stable three-dimensional
topological carrier from a one-coordinate sector.

## 4. Acceptance gates

- Full nonlinear metric inverse and four-dimensional Weyl tensor.
- No finite differences or linearization.
- Exact arithmetic or independently simplified symbolic expressions.
- Riemann symmetries, Bianchi identity, Ricci symmetry, Weyl trace, and `C^2` contraction identity.
- Every use of the axis target marked CONDITIONAL; native target remains `RP^2` for an unoriented
  metric axis, with `S^2` only an oriented lift.
- No numerical carrier search until the continuum field space, functional, boundary terms, and raw
  stability gate are fixed.

## 5. Possible outcomes

1. **IRREDUCIBLE SECOND-JET SECTOR:** `C^2` contains nonzero quadratic second-jet terms.
2. **FIRST-JET REDUCTION:** all second-jet terms cancel or become boundary terms.
3. **DEGENERATE CONDITIONAL PARAMETRIZATION:** the reduced functional loses required metric
   equations and cannot define native dynamics.
4. **ALGEBRA UNRESOLVED:** tensor checks or independent formulas fail.
