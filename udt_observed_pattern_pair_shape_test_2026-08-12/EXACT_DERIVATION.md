# Exact derivation — complete-pair observed-pattern shape operator

Date: 2026-08-12
Status: `DERIVED` on a supplied regular monotone pair history; physical history remains `OPEN`

## 1. Supplied complete pair geometry

On a regular calibrated observer-pair realization, write the exact pulled-back metric as

```text
h = -T_pair^2 (dy0 + beta_pair dlambda)^2 + L_pair^2 dlambda^2.
```

The horizontal ruler direction is defined intrinsically by

```text
dy0 + beta_pair dlambda = 0,
```

and therefore has proper longitudinal source length

```text
d ell_parallel = L_pair dlambda.
```

Let the query-owned screen Jacobi map be `D`, with regular area distance

```text
d_A = sqrt(abs(det D)) > 0,
```

and let the terminal reciprocal coordinate be

```text
1 + z = exp(phi_pair).
```

No scalar, diagonal, stationary, or radial-only truncation has been made in these definitions.
Angular geometry and complete mixing can enter through `D`, `L_pair`, and `phi_pair`.

## 2. Dimensionless two-leg shape

The transverse source length subtended by a small observed angle is proportional to `d_A`. The
radial source length associated with a small redshift interval is

```text
d ell_parallel = L_pair (dlambda/dz) dz.
```

The same endpoint conversion factor multiplies both source-length legs in the released coordinate
ratio, so it cancels. The dimensionless transverse/radial shape is consequently

```text
F_pair
  = d_A / [L_pair (dlambda/dz)]
  = d_A (dz/dlambda) / L_pair
  = exp(phi_pair) d_A (d phi_pair/dlambda) / L_pair.       (1)
```

Equation (1) is a complete-pair evaluation formula, not a selected history or equation of motion.

## 3. Reparameterization

For an orientation-preserving change `lambda_new=f(lambda)` with
`q=d lambda_new/d lambda>0`,

```text
d phi/d lambda_new = (d phi/dlambda)/q,
L_pair,new = L_pair/q.
```

Thus numerator and denominator acquire the same factor `1/q`, and `F_pair` is unchanged. Under
orientation reversal the signed expression changes orientation; the unoriented released shape uses
its absolute value. Turning points, caustics, `L_pair=0`, `d_A=0`, and nonmonotone histories are
separate strata on which this coordinate readout can fail or branch.

Omitting `L_pair` destroys reparameterization invariance. Omitting `exp(phi_pair)` breaks the exact
redshift-depth conversion and the scalar control reduction.

## 4. Frozen scalar controls

Only for the conditional scalar specialization

```text
lambda = r,
L_pair = exp(phi_pair) = u = 1+z,
d_A = r(u),
r(u) = (X/n) [1-u^(-2/n)]
```

does (1) reduce to

```text
F_scalar = r/[u (dr/du)] = (n/2)[u^(2/n)-1].              (2)
```

For `n=1`,

```text
F_C0 = z + z^2/2.
```

For the independently frozen SNe-P1 value
`n=1.0559332414320268`, equation (2) gives C1. `X`, `c_E`, and the released common normalization
cancel. C0 and C1 are scalar controls only; neither is the complete-orchestra prediction.

## 5. Released-data projection

For each released two-component datum `y=(D_M/r_d,D_H/r_d)` and its full released 2x2 covariance
`C`, a predicted shape defines the ray `v=(F,1)`. Profiling the unowned along-ray publication
amplitude gives exactly

```text
a = (v^T C^-1 y)/(v^T C^-1 v),
chi2 = y^T C^-1 y - (v^T C^-1 y)^2/(v^T C^-1 v).          (3)
```

This is a normalization-free direction test. The six algebraic `a` values are not UDT coefficients,
physical scales, or fitted history parameters. Equation (3) uses the full within-bin covariance;
no delta-method ratio error enters the load-bearing result.

## 6. Exact ownership boundary

`DERIVED`:

- equation (1) on the stated regular supplied pair history;
- its orientation-preserving reparameterization invariance;
- equations (2) and the two frozen scalar reductions;
- equation (3) as the exact Gaussian projection for the released data coordinates.

`OBSERVED`:

- the numerical residuals and chi-square values in `DERIVATION_RESULT.json`.

`OPEN`:

- the physical complete history `D(lambda), L_pair(lambda), phi_pair(lambda)`;
- any complete-orchestra correction to either scalar control;
- branch aggregation at turning/caustic strata;
- feature origin, absolute normalization, and `X_max`.
