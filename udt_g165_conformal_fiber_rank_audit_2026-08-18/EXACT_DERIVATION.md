# G165 exact derivation

## 1. Pair-metric conformal weights

Let a supplied regular calibrated pair metric be

```text
h = [[h00,h01],[h01,h11]],
h00<0, det(h)<0.
```

Its terminal variables are

```text
beta = h01/h00,
kappa = (1/4) log(-det h),
phi_pair = (1/4) log[(-det h)/h00^2],
c_eff/c_E = (-h00)/sqrt(-det h).
```

Under a positive common rescaling

```text
h_hat = exp(2w) h,
```

the determinant scales as `det(h_hat)=exp(4w)det(h)`. Therefore

```text
beta_hat = beta,
phi_pair_hat = phi_pair,
(c_eff/c_E)_hat = c_eff/c_E,
kappa_hat = kappa+w.
```

Writing `T=exp(kappa-phi_pair)` and `L=exp(kappa+phi_pair)`, both densities scale by
`exp(w)`. Hence

```text
chi=(L-T)/(L+T)=tanh(phi_pair)
```

is invariant. The metric half-density coefficient `(-det h)^(1/4)` has conformal weight one.

## 2. Causal structure

For every tangent vector `v`,

```text
h_hat(v,v)=exp(2w)h(v,v).
```

Positive rescaling therefore preserves null directions and the timelike/null/spacelike sign. With
the time orientation retained, causal order is conformally unchanged in the bounded arena.

This is a scale-blindness theorem for causal structure, not a declaration that common scale is
gauge.

## 3. Compact-bump nonlinear catch

On a chart interval, take the standard smooth bump

```text
f(x)=0                                      outside (1/3,2/3),
f(x)=exp[-1/((x-1/3)(2/3-x))]              inside (1/3,2/3).
```

It vanishes on anchor neighborhoods near the endpoints and is positive at `x=1/2`. For a flat
four-dimensional reference metric and a spatially dependent conformal factor, the scalar curvature
of `exp(2f)g` at the symmetric center is

```text
R_hat(1/2)=15552 exp[-36-2 exp(-36)] > 0,
```

whereas the reference curvature is zero. Thus the twin is not a coordinate re-description.

More generally, any finite union of proper anchor neighborhoods that leaves a nonempty open
complement admits such a smooth compactly supported deformation. If the supplied observational
regions cover the entire domain with full function-valued information, that is no longer a finite
anchor architecture.

## 4. Dimensional-anchor rank

Using log unit rescalings `(u_L,u_T,u_M)`, fixed numerical values of `c_E` and `G_obs` impose

```text
u_L-u_T=0,
3u_L-2u_T-u_M=0.
```

The coefficient matrix has rank two and nullspace spanned by `(1,1,1)`. Consequently `c_E` and
`G_obs` alone do not form a length or fix one remaining simultaneous length/time/mass scale.

This dimensional fact is secondary to the functional obstruction: even a third dimensional datum
would calibrate only a constant unless an owned restriction first removes local smooth conformal
freedom.

## 5. Ownership filter

The complete G155 ledger supplies 41 through-G154 statements. None has the active role
`PHYSICAL_HISTORY_CONSTRAINT` or `PHYSICAL_HISTORY_EVOLUTION`.

The 18 preregistered G156--G164 and cross-cutting candidates then classify as:

- definitions/evaluators;
- representation or presentation constraints;
- supplied carry/network compatibility;
- dependency or nonselection classifications;
- valued-network reconstruction;
- calibration without a metric bridge;
- conformal-invariant readouts or unvalued incidence;
- finite anchor data; or
- an explicitly open proposal.

No row survives as an active source-owned condition on the metric values or jets. The complete
`CONDITION_CENSUS.tsv` therefore has 59 rows and zero owned metric restrictors.

## 6. Primary and secondary classifications

The preregistered primary landing is

```text
NO_OWNED_NONIDENTITY_CONDITION.
```

This is distinct from two secondary statements:

```text
current normalized/causal/finite-anchor map -> FUNCTIONAL_KERNEL,
full valued rank-complete relation network -> VALUED_NETWORK_RECONSTRUCTION_ONLY.
```

The first says the currently owned scale-blind observables admit arbitrary smooth conformal twins.
The second says complete pair determinants can reconstruct common scale because the scale function
was included in the supplied values. Neither is a native law propagating finite data.

## 7. Conditional route that remains open

G156 supplies a positive metric half-density line and a determinant character for a supplied carry.
If a future source owns a physical global scale carry, proves flatness or classifies holonomy, and
reduces local conformal freedom to a constant per connected component, one anchor could calibrate
relative scale. G165 neither derives nor excludes that architecture.
