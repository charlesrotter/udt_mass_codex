# Exact derivation

## 1. Full-frame scalar-character obstruction

Let the six generators of `so(1,3)` be three boosts `K_i` and three rotations `J_i`. Exact
commutators span all six generators. Therefore

```text
[so(1,3),so(1,3)] = so(1,3).
```

For a Lie-algebra homomorphism `ell:so(1,3)->R`, the target is abelian, so

```text
ell([A,B])=0
```

for every `A,B`. Because the brackets span the full algebra, `ell=0`. If
`chi:SO+(1,3)->(R,+)` is a continuous group homomorphism, its derivative is such an `ell`; the
derivative vanishes, and connectedness makes `chi` constant. Since `chi(identity)=0`,

```text
chi=0.
```

Thus the full connected frame-comparison group has no nontrivial continuous additive real
character.

This theorem concerns a scalar extracted from full-frame transformation alone. It does not forbid
a cocycle that also depends on base position, a supplied path, or a reduced structure.

## 2. Angular information is forced

For boosts in two distinct spatial directions,

```text
[K_1,K_2] proportional_to J_12 != 0.
```

The Baker-Campbell-Hausdorff series therefore contains an angular generator at order `ab/2` when
two non-collinear infinitesimal boosts are composed. This is the infinitesimal form of the exact
group-character obstruction: no nontrivial additive scalar can retain the full composition data.

Hence arbitrary observer-query comparison may be covariant and non-preferred, but it must retain
angular/nonabelian information. “No preferred observer” does not imply “no observer-query law.”

## 3. Pointwise full-isotropy obstruction

At a full Lorentz-isotropy control, naturality requires a pointwise selected vector, covector, or
endomorphism to be fixed by the isotropy action.

Exact ranks are:

```text
common fixed-vector equations:       rank 4, nullity 0;
common fixed-covector equations:     rank 4, nullity 0;
endomorphism commutator equations:   rank 15 in dimension 16.
```

The endomorphism commutant is therefore one-dimensional, spanned by identity. No scalar identity
has both founded eigenvalues `-1` and `+1`. A pointwise metric-only non-scalar reciprocal generator
cannot be natural on the entire unrestricted Lorentzian class.

A supplied coframe does not solve this as a metric selection if local Lorentz-related coframes are
representatives of the same metric object. It can solve it only if the coframe/reduction is declared
physical input, which is a different premise category.

## 4. Reduced stabilizer results

Let `eta=diag(-1,+1,+1,+1)` and require the generator to be metric-self-adjoint.

### Timelike observer line

Fix only a timelike line `u`. Commutation with its spatial `SO(3)` stabilizer and `Xu=-u` gives the
one-parameter family

```text
X=diag(-1,a,a,a).
```

If no spatial ruler is distinguished but the founded `+1` ruler eigenaction must occur, spatial
isotropy forces `a=+1` on the entire complement:

```text
X_u=diag(-1,+1,+1,+1).
```

This is `UNIQUE_CONDITIONAL_LAMBDA_PLUS_ONE`, conditional on a supplied or metric-derived observer
line/congruence. The observer line alone supplies neither signed depth nor global descent.

### Spacelike ruler line

Fix only a spacelike ruler line `n`. Commutation with its complementary `SO+(1,2)` stabilizer and
`Xn=+n` gives

```text
X=diag(a,+1,a,a).
```

Requiring the founded clock eigenvalue on the undistinguished complement forces `a=-1`. This is the
dual `UNIQUE_CONDITIONAL_LAMBDA_MINUS_ONE` route, not the same reduction as the observer-line route.

### Ordered clock/ruler pair

Fix an ordered orthonormal pair `(u,n)`. The residual screen stabilizer is `SO(2)`. Self-adjointness,
screen covariance, `Xu=-u`, and `Xn=+n` give exactly

```text
X_lambda=diag(-1,+1,lambda,lambda), lambda in R.
```

There is no invariant screen mixing, but one real transverse weight remains. All constant members
integrate exactly under `exp(phi X_lambda)`. Pair covariance and finite composition do not select
`lambda`.

## 5. Depth routes

Every endpoint-additive real depth has normal form

```text
delta(p,q)=f(q)-f(p).
```

This is a family, not a selection. On a homogeneous flat Lorentzian control, translation
invariance and additivity make `f(q)-f(p)` linear in `q-p`; Lorentz invariance would require a fixed
covector, whose exact nullity is zero. The metric-only invariant endpoint cocycle is therefore
trivial on that control.

The invariant interval does not replace it. It is symmetric rather than signed, and for the
timelike triple

```text
p=(0,0), q=(2,0), r=(4,1)
```

the proper-time magnitudes obey

```text
2+sqrt(3) != sqrt(15).
```

The positive escape is base dependence. If the complete metric genuinely derives a physical
scalar potential or one-form, its difference or path integral is an additive cocycle. On a
stationary branch with intrinsic Killing line,

```text
Q=sqrt(-g(K,K)),
delta_K(p,q)=log[Q(p)/Q(q)]
```

is the exact bounded example. The full-frame character theorem does not obstruct it because it is
not a character of the full Lorentz group.

## 6. Groupoid and holonomy

Once a path `gamma`, depth `delta_gamma`, pair frame, and real `lambda` are supplied,

```text
C_gamma=(D(delta_gamma),U_gamma)
```

or the intertwined transported form composes exactly. This is a real law on observer queries and
paths, not a preferred observer. Its scalar channel is abelian; its coframe channel is nonabelian.

Endpoint collapse requires loop holonomy to centralize the chosen generator. The centralizer
dimensions inside `so(1,3)` are `1,3,3,1` for generic `lambda`, `+1`, `-1`, and `0`; none equals the
full holonomy dimension six. Thus a full-holonomy control remains path-labelled for every tested
stratum.

## 7. Exact theorem boundary

The derived theorem is:

```text
full-frame-only nontrivial additive scalar depth: NO-GO;
pointwise metric-only non-scalar reciprocal generator on the full class: NO-GO;
generic non-collinear comparison without angular data: NO-GO;
reduced reciprocal cocycle plus angular groupoid: REQUIRED TYPE, conditional inputs remain;
universal higher-jet/nonlocal/whole-solution selector: NOT CLASSIFIED.
```

This exact boundary is why the primary preregistered outcome is
`NO_GO_PREMISES_INSUFFICIENT_STOP`, while the partial no-go and type constraint are derived.
