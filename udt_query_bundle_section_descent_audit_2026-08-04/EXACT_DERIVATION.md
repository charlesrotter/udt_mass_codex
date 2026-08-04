# Exact derivation — query-bundle descent and section necessity

Date: 2026-08-04

## 1. Three distinct questions

Let `pi:P->M` be the ordered future-timelike-unit observer / orthogonal unit-ruler query bundle of a
regular Lorentzian spacetime `(M,g)`. At `p=(x,u,n)` the tautological reciprocal plane is

```text
N_tilde_p = span(u,n) subset T_x M,
Q_tilde_p = N_tilde_p^perp.
```

Three properties must not be conflated.

1. **Frame covariance:** changing components of the same geometric data changes all components by
   the tensor law.
2. **Query equivariance:** changing the actual ordered pair `(u,n)` at fixed `x` changes a
   pair-dependent object naturally.
3. **Basic descent:** an object over `P` is the pullback of one object on `M`; consequently it does
   not change when only the query pair changes.

For an ordinary scalar or tensor valued in a pulled-back base bundle, basic descent means constancy
on each fiber after the canonical identification at fixed `x`. For differential forms it also
requires horizontality: insertion of a vertical vector gives zero. Equivariance alone is weaker.

If `s:M->P` is a section, any query object can be evaluated on `s`. But two sections `s_1,s_2` give
the same pullback for every `x` only when the object is basic. Existence of some section therefore
does not make a pair-dependent construction intrinsic.

## 2. Exact vertical-pair control

Use

```text
eta = diag(-1,1,1,1),
u=e_0,
n_1=e_1,
n_2=e_2.
```

For a unit non-null vector `v`, its metric-orthogonal line projector is

```text
P_v = v (v^T eta) / eta(v,v).
```

Thus the reciprocal-plane projectors are

```text
P_01 = P_e0 + P_e1 = diag(1,1,0,0),
P_02 = P_e0 + P_e2 = diag(1,0,1,0).
```

Both are rank-two, idempotent, and `eta`-self-adjoint. A spatial Lorentz rotation `R_12` satisfies

```text
R_12^T eta R_12 = eta,
P_02 = R_12 P_01 R_12^-1,
P_02 != P_01.
```

This is the exact distinction: `P_N` is equivariant as the query changes, but is not vertically
invariant. It is a canonical tensor over the query bundle, not one projector on spacetime.

The ambient identity is the positive control:

```text
R_12 I R_12^-1 = I.
```

The metric and any ambient tensor defined without `(u,n)` similarly remain the same base object.

## 3. Screen dependence

Let `Q_01=I-P_01` and `Q_02=I-P_02`. For the fixed vector `v=e_2`,

```text
g(Q_01 v,Q_01 v)=1,
g(Q_02 v,Q_02 v)=0.
```

So even the metric-induced screen readout depends on the chosen pair plane. An additional positive
screen metric `h in SPD(Q_tilde)` is legitimate associated-bundle data, but does not become a
pair-independent spacetime screen unless it is basic or a section is supplied.

A general mixing map `sigma in Hom(N_tilde,Q_tilde)` has the same typing. The zero section is an
important exception: zero maps to zero under every transition and can be embedded as the ambient
zero tensor. But that trivial value neither selects `N` nor proves that physical mixing is zero.

## 4. Ambient versus projected curvature

Take the exact self-adjoint curvature-model endomorphism

```text
A = diag(2,3,5,7).
```

Its ambient trace is always

```text
tr(A)=17.
```

The pair-projected traces are

```text
tr(P_01 A)=5,
tr(P_02 A)=7.
```

This is not a coordinate effect: `A` is held fixed while the actual observer/ruler query changes.
Under a mere change of components, both `A` and `P` would conjugate and the scalar would be
unchanged. Therefore ambient curvature tensors and their contractions live on `M`, while generic
pair-projected curvature observables live on `P`.

The failure is infinitesimal as well. Set

```text
n=(3/5)e_1+(4/5)e_2,
m=-(4/5)e_1+(3/5)e_2,
delta P = m n^T eta + n m^T eta.
```

Here `m` is the infinitesimal spatial rotation of `n`. Exact algebra gives

```text
rank(delta P)=2,
delta tr(P A)=tr(delta P A)=48/25 != 0.
```

So the projected scalar has a nonzero derivative in a vertical query direction and is not basic.

The Levi-Civita connection itself is defined on `TM` from `g` and needs no reciprocal section.
Connection coefficients in a pair-adapted frame, projected connection components, screen
connections, second fundamental forms, and plane holonomies depend on the pair/reduction and must
be typed separately.

## 5. Founded comparison survives as a query law

On a supplied reciprocal plane, the founded character is

```text
D_01(rho)=diag(exp(-rho),exp(rho),1,1).
```

It obeys exactly

```text
D_01(a)D_01(c)=D_01(a+c),
D_01(-a)=D_01(a)^-1.
```

After the vertical reset,

```text
D_02(rho)=R_12 D_01(rho) R_12^-1
```

and the same composition law holds. This replays the prior path-groupoid result in the smallest
exact control. It proves that a global one-pair-per-event section is unnecessary for typed query
composition. It does not supply the physical signed-depth assignment `rho` or collapse the law to
bare events.

## 6. Boundary split

A supplied base boundary `partial M`, its base normal, and its induced metric can be defined from
base geometry without `N`. The full query boundary `pi^-1(partial M)` is also a valid container.

Pair-resolved polarization is different. With base-normal control `b=e_2`,

```text
P_01 b=0,
P_02 b=b.
```

Thus pair-projected boundary data are not basic generically. They may remain query-boundary data or
be pulled back by a realized/branch-derived section. This audit does not choose a boundary type,
polarization, functional, or charge.

## 7. Variation ownership

The three globalization architectures have different tangent rules.

```text
query architecture:
    delta_vertical(u,n) changes the question, not the spacetime field;

realized-field architecture:
    delta s belongs to Gamma(s*VP) and is a new physical tangent only if that field ownership is
    selected;

branch-derived architecture:
    s=s[g], so delta s = Ds[g] dot delta g wherever the selector is regular.
```

Consequently a vertical query derivative cannot silently be inserted into an action variation.
Conversely, if a section is declared physical, omitting `delta s` freezes a physical field. If the
section is derived from `g`, varying it independently double-counts.

## 8. Collision and defect loci

The regular branch-derived route is not a universal smooth shortcut. Consider

```text
A_1(epsilon)=diag(2,3,3+epsilon,7),
A_2(epsilon)=diag(2,3+epsilon,3,7).
```

For positive `epsilon`, the two simple spatial eigenlines pick `P_01` and `P_02`, respectively. But

```text
lim A_1 = lim A_2 = diag(2,3,3,7)
```

while `P_01 != P_02`; the two limits are related by the collision isotropy. At the collision the
natural output is an orbit/set of candidate lines, not a unique smooth projector.

The same typing issue occurs at the registered intrinsic-two-form zero graph, `dphi=0` or null
normalization loci, causal-type changes, complex/null/Jordan/tied spectra, and boundary
intersections of defects. A future law may use a stratified rule, but none is supplied here.

## 9. Why fiber averaging is not a free escape

One might try to average a pair-dependent object over every pair above `x`. That is a new operation,
not automatic descent. It requires a declared measure, weight, normalization, convergence domain,
and physical meaning. No such UDT-native object occurs in the frozen sources. In particular, the
observer part of the Lorentzian pair fiber is noncompact, so a normalized average cannot be assumed
by habit. The audit neither rules out a future derived aggregation rule nor invents one.

## 10. Slot-level consequence

The eight open skeleton slots split rather than sharing one universal dependency.

- Typed reciprocal comparison, vertical resets, path-family composition, the query container, and
  query-family returns can be formulated without a global spacetime section.
- Ambient metric laws, ambient curvature, base causal geometry, base boundary geometry, and
  pair-independent complete-solution observables can in principle live directly on `M`.
- Physical screen/mixing response, pair-projected curvature, pair polarization, a realized
  reciprocal field, and any section-evaluated source or bootstrap return require either a declared
  query interpretation or a realized/branch-derived section.
- Collision and rank-change crossings require a stratified ownership rule; a regular spectral or
  kernel selector cannot be differentiated through them by assertion.
- Fiber aggregation remains open because no native measure/weight rule is derived.

The missing joint is therefore not simply “find one reciprocal plane before doing anything.” It is
the native law's **home, codomain, and ownership rule**: whether the law is a basic spacetime law, an
equivariant query law, or a law evaluated on a realized/branch-derived/stratified reduction.

No current premise selects among those architectures.
