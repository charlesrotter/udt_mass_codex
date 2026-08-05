# Exact derivation — one reciprocal arrow, two intrinsic readouts

## 1. The bounded question

Let the founded ordered reciprocal comparison be

```text
D(delta)=diag(exp(-delta),exp(+delta)).
```

The question has two mathematically different levels:

1. Does a supplied founded arrow contain both an oriented depth and an unoriented magnitude?
2. Does the bare complete metric canonically identify that magnitude with physical separation for
   arbitrary observer pairs?

The first answer is yes. The second answer is no under the presently active premises. This is a
split theorem, not a rejection of the proposed holistic interpretation.

## 2. Exact signed-depth extractor

For any positive reciprocal arrow `A=D(delta)`, define

```text
delta(A) = (1/2) log(A_22/A_11).
```

Because `A_22/A_11=exp(2 delta)`, this returns the supplied signed depth exactly. It obeys

```text
delta(I)=0,
delta(A^-1)=-delta(A),
delta(A_2 A_1)=delta(A_2)+delta(A_1).
```

It is faithful: `delta(A)=0` if and only if `A=I` within the positive founded subgroup. Any
continuous additive real coordinate on this one-dimensional group is `a delta`; the registered
sign/unit convention fixes `a=1`. Thus the signed coordinate is unique after the already recorded
normalization choice.

## 3. Exact symmetric magnitude

The reversal-even half trace is

```text
Gamma(A)=Tr(A)/2=cosh(delta).
```

Therefore

```text
rho(A)=arcosh(Gamma(A))=abs(delta).
```

It obeys

```text
rho(A)>=0,
rho(A)=0 iff A=I,
rho(A^-1)=rho(A),
rho(A_2 A_1)=abs(delta_2+delta_1)<=rho(A_2)+rho(A_1).
```

This is exactly the geodesic distance from the identity for the invariant quadratic group metric
`(1/2)Tr(J^2)=d(delta)^2`, after fixing its overall unit. The result is intrinsic to the founded
one-dimensional reciprocal group.

Hence a single supplied arrow already has the desired orientation split:

```text
ordered component       delta(A)  (signed, reversal odd)
unoriented magnitude    rho(A)    (nonnegative, reversal even)
```

This proves the algebraic core of the proposed interpretation. It does not yet prove that `rho` is
the complete physical distance between arbitrary observers.

## 4. Why reciprocal magnitude is not yet physical positional separation

`rho=abs(delta)` is dimensionless and unbounded. The owner-ratified `X_max` frame instead requires a
nonnegative positional separation `s` with

```text
0 <= s < X_max,
s -> X_max from below implies rho -> infinity.
```

Identifying the two readings therefore needs a calibration/profile

```text
s = F(rho),
F(0)=0,
F'(0)=ordinary-regime calibration,
lim_(rho->infinity) F(rho)=X_max.
```

Reciprocity, `c_E`, and the asymptote do not uniquely choose `F`. For positive `kappa`, both

```text
F_1(rho)=X_max tanh(kappa rho),
F_2(rho)=X_max[1-exp(-kappa rho)]
```

are continuous, strictly increasing, subadditive, have the same value and slope at the origin, and
have the same `X_max` limit. They differ already in their second derivative at the origin:

```text
F_1''(0)=0,
F_2''(0)=-X_max kappa^2.
```

The common local slope can be set by the observed clock/length calibration. The exact counterfamily
still survives. Thus ordinary `c_E` calibration plus `X_max` fixes endpoint behavior, not the whole
distance-depth profile.

## 5. The angular sector is a decisive type check

Take two distinct events at equal reciprocal depth and equal spherical radius, separated by a small
equatorial angle `alpha`. Their scalar reciprocal difference is zero, while the supplied angular
metric sector has nonzero arc length `R abs(alpha)`.

Therefore `abs(delta)` alone cannot be the complete spatial separation in a metric with a live
angular sector. Either:

1. the fundamental physical distance is the **complete observer-pair comparison**, with reciprocal
   magnitude as one component and angular/mixing transport as other components; or
2. an additional rule must reduce the complete comparison to one scalar separation.

This is exactly the user's orchestra point in mathematical form. It rules out reducing holistic
distance to one scalar reciprocal instrument while leaving the rest of the metric live.

## 6. Complete-coframe extraction has an exact reference obstruction

On the supplied factorization write

```text
theta = D(z) bar_theta,   z=exp(phi).
```

For any positive local function `h`, the refactorization

```text
z' = z h,
bar_theta' = D(h)^-1 bar_theta
```

leaves `theta` exactly unchanged. Independent endpoint shifts also change `z_q/z_p` by `h_q/h_p`
while leaving both complete endpoint coframes unchanged. Consequently no function of the bare
complete coframes alone can return that representative endpoint depth ratio: the same input would
have to return arbitrarily many outputs.

This does not refute the founded comparison. It proves that its physical arrow or a rule selecting
its reciprocal component must be part of the observer-pair data; it cannot be reconstructed from an
arbitrary pointwise factorization label.

## 7. Ordinary metric transport is not the missing reciprocal operation

Levi-Civita transport is metric-isometric. In the unbalanced physical clock/ruler readout,

```text
U^T eta U=eta,
D(delta)^T eta D(delta) != eta for nonzero delta.
```

The founding matrix preserves the dual evaluation pairing `K`, not automatically the physical
interval represented by `eta` in that same basis. Their algebraic similarity after a balanced basis
change is not a license to identify their physical types.

The exact static diagonal control makes this concrete. Coordinate covector transport along its
registered spatial curve displays `D(Delta phi)`, but it maps the physical orthonormal coframe at the
first endpoint exactly to the physical orthonormal coframe at the second. The relative orthonormal
transport is the identity. Seeing the reciprocal matrix in coordinate components therefore does not
by itself establish physical inter-observer dilation.

## 8. Paths and holonomy prevent a universal endpoint collapse

For a supplied path `gamma`, generator `X_p`, additive depth `rho_gamma`, and metric transport
`U_gamma`, the previously derived complete comparison

```text
A_gamma=U_gamma exp(rho_gamma X_p)
```

composes and reverses exactly when the generator is transported to the middle object. This is a
valid path-labelled architecture, but it uses rather than derives `rho_gamma` and `X_p`.

To collapse a non-scalar generator to a path-independent endpoint object, it must commute with loop
holonomy. The exact commutator system for full `so(1,3)` holonomy has rank 15 in `End(R^4)`, leaving
only the scalar identity. Every extension of the founded base generator retains unequal clock/ruler
eigenvalues and is non-scalar. Hence it cannot descend on the registered full-holonomy control.

This is a control-scoped obstruction, not a universal no-go: reduced-holonomy on-shell branches may
permit endpoint descent. But the active premises do not select such a branch, a preferred path, or
a vertical reset rule.

## 9. The stationary branch remains a genuine positive reduction

When the complete metric possesses an intrinsic timelike Killing line `K`, its lapse norm gives

```text
delta_K(p,q)=log[N(p)/N(q)],
rho_K(p,q)=abs(delta_K(p,q)).
```

These are metric-native, compositional, reversal-covariant, and independent of constant Killing
normalization on that branch. This supplies an explicit instance of the two-readout theorem.

It remains branch-local. It does not provide a general nonstationary pair law, angular separation,
cut-locus semantics, the bounded positional profile `F`, or a complete physical comparison functor.

## 10. Precise result

The following statement is derived:

> Once the founded reciprocal observer-pair arrow is supplied, it canonically yields a signed depth
> and a symmetric nonnegative reciprocal-group magnitude. They are the oriented coordinate and
> invariant norm of one relational object.

The following stronger statement is not derived from the current metric sources:

> The bare complete metric canonically supplies that arrow for every observer pair and identifies
> its reciprocal magnitude alone with complete physical positional separation.

The strongest holistic formulation consistent with the proof is therefore:

> Physical observer separation is to be sought as a readout of one complete observer-pair
> comparison, not as a pre-existing scalar to which dilation is later attached. Signed reciprocal
> depth and its nonnegative magnitude are already exact readouts of the founded reciprocal component;
> angular, mixing, path and global data must enter the complete comparison rather than being tacked
> on afterward.

This formulation is an exact architecture plus an owner-proposed physical identification. The
remaining mathematical object is a metric-natural complete comparison map

```text
C:(complete global geometry, ordered observer/event pair, admissible path data)
  -> complete comparison arrow,
```

together with a reference-independent reciprocal projection and, if a single scalar is required, a
full-coframe separation readout satisfying the `c_E` and `X_max` gates. The metric sources presently
classify but do not select this map.
