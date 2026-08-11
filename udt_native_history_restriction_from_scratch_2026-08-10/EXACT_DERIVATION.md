# Exact derivation — where a native history law can and cannot come from

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU, from scratch

Preregistration commit: `e7b1beb4`

## 1. Result first

The complete regular pair-adapted coframe is not a hidden equation. After fixing only its local
screen-presentation rotation, it is a genuine coordinate chart on an open set of all ten Lorentzian
metric components. The same is true of every finite jet prolongation. Consequently neither the
factorization nor a more detailed expansion of it can select a proper subset of regular histories.

The exact source-bounded landing is

```text
COMPLETE_REGULAR_CHART_IS_LOCALLY_JET_OPEN_ON_THE_DECLARED_POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT;
NO_CURRENTLY_OWNED_NONIDENTITY_HISTORY_RESTRICTION_IS_FOUND_IN_THE_TEN_FROZEN_SOURCES.
```

This is not a universal no-go for UDT dynamics. It identifies the mathematical type of the missing
joint: an owned nonidentity relation, local or global, that says which otherwise lawful metric
histories are admissible.

## 2. Exact ten-component chart

Fix the positive lower-triangular screen presentation

```text
B=[[T,T beta],[0,L]],
Q=[[u,0],[v,w]],
S=[[s00,s01],[s10,s11]],
E=[[B,0],[Q S,Q]],
```

with `T,L,u,w>0`. This fixes the local left-`O(2)` presentation freedom but does not remove a metric
component. With `eta=diag(-1,+1,+1,+1)`, let `g=E^T eta E`. Order its ten independent components as

```text
(g00,g01,g11,g02,g03,g12,g13,g22,g23,g33).
```

Exact differentiation with respect to

```text
(T,L,beta,u,v,w,s00,s01,s10,s11)
```

gives

```text
det(dg/dq)=16 L T^3 u^5 w^6.                       (1)
```

It is nonzero everywhere on the declared regular component. The metric determinant is

```text
det g=-L^2 T^2 u^2 w^2.                             (2)
```

Thus the map is a local diffeomorphism, not a lower-dimensional ansatz.

## 3. Constructive inverse

Write the screen, cross, and base blocks as `H`, `C`, and `G`. The exact block relations are

```text
H=Q^T Q,
C=S^T H,
A=G-C H^-1 C^T=B^T diag(-1,+1) B.                  (3)
```

On the positive-screen, time-oriented Lorentzian-Schur component the inverse is

```text
w=sqrt(H33),
v=H23/w,
u=sqrt(det(H)/H33),
S=H^-1 C^T,

T=sqrt(-A00),
beta=A01/A00,
L=sqrt(det(A)/A00).                                 (4)
```

The signs are fixed by the chosen connected chart component. Equations (3)--(4) reconstruct all
ten variables and explicitly state the scope: a supplied regular reciprocal/angular split,
positive screen, and `A00<0`, `det A<0`. Nothing here selects that split globally or across null,
rank-changing, or cut-locus strata.

## 4. Why all finite jets remain open

Let `F:q -> g` denote the point transformation above. Because `DF` is invertible, the highest-order
part of every prolonged derivative has form

```text
partial_I g = DF(q) partial_I q + lower-order terms. (5)
```

Ordered by derivative degree, the Jacobian of the `k`-jet map is block triangular with one copy of
`DF` for every multi-index of order at most `k`. In four independent variables there are

```text
N_k=binomial(4+k,k)
```

such indices. Therefore

```text
det J^k F = [16 L T^3 u^5 w^6]^(N_k),               (6)
```

which is nonzero. In particular the exponents are `5` at first jet and `15` at second jet.

This closes an important loophole: curvature and every finite-order natural tensor are perfectly
valid readouts of these histories, but the chart supplies arbitrary finite metric jets. A
nonidentity equation `R(j^k g)=0` would cut that open image to a proper subset and therefore cannot
be a consequence of the parameterization alone.

## 5. The five current owner classes

### O01 — factorization and founded reciprocal character

The founded result is the exact character

```text
D(delta)=diag(exp(-delta),exp(+delta))
```

after an ordered depth is supplied. In the complete chart, `phi=(1/2)log(L/T)` is a lawful state
coordinate. Neither statement assigns `phi(t,x)`, its derivatives, or a physical pair query. The
pure reciprocal reduction would be a proper subfamily only if it were newly imposed as universal;
current ownership does not do that. Landing: `CONDITIONAL_COMPARISON_RULE`.

### O02 — Cartan, curvature, and Bianchi structure

The metric naturally constructs the Levi-Civita connection, Riemann tensor, Ricci contractions,
Weyl tensor, and scalar invariants. Cartan structure and Bianchi relations are identities on every
smooth metric. No current source contains the mandatory statement that one of the nonidentity
tensors or contractions must vanish, be constant, equal a source, or extremize a functional.

Arbitrary algebraic curvature tensors can also be realized as second jets in normal coordinates;
this is the curvature-level expression of (6). Constructing `Ric(g)` or `C(g)` is not the same act
as imposing `Ric(g)=0` or a Bach equation. Landing: `IDENTITY_FOR_ALL_REGULAR_HISTORIES` for the
owned relations; curvature itself remains a `DERIVED_READOUT`.

### O03 — observer composition and causal order

Composition restricts how supplied comparison arrows join. It does not select the ambient metric
movie. For any object potential `f`, the endpoint rule

```text
delta(p,q)=f(q)-f(p)
```

composes exactly, while `f` remains arbitrary. Likewise the pullback cone of a supplied pair
immersion is automatically causal; global causal faithfulness is a real possible filter but is
still open and depends on the physical ambient pair construction. Landing:
`CONDITIONAL_COMPARISON_RULE`.

### O04 — `c_E` and `X_max`

`c_E` calibrates the clock/ruler conversion and terminal reciprocal readout. It supplies no
derivative or trajectory coefficient. `X_max` is the working observer-pair positional-dilation
asymptote, while its separation-depth realization, global join, all-frame theorem, and value remain
open. It is explicitly not a material wall or variational boundary. Landing:
`READOUT_OR_CALIBRATION_ONLY` in current ownership; a future complete realization may become a
global restriction.

### O05 — global descent, topology, and boundary data

Current R17/global results own conditional leaf, carry, holonomy, and topology structures but do
not select R17, one path, one query, or one physical history. More generally, boundary data without
an interior operator leave infinitely many interiors: if `g` is one regular Lorentzian metric and
`chi h` is any smooth symmetric perturbation supported away from the boundary, then

```text
g_epsilon=g+epsilon chi h                              (7)
```

has the same full boundary germ and remains Lorentzian for sufficiently small `epsilon`. If its
support is also disjoint from a chosen end, it preserves the metric germ at that end. This local
construction does **not** automatically preserve chronology, global hyperbolicity, causal
faithfulness, geodesic completeness, or a selected global-descent structure. Landing:
`GLOBAL_OR_BOUNDARY_RESTRICTION_ONLY`; the selected completion plus a response/evolution relation
remain open.

## 6. What was actually ruled out

The result rules out five recurrent shortcuts:

1. extracting an equation by expanding the same complete metric more deeply;
2. calling Maurer--Cartan or Bianchi compatibility an evolution law;
3. setting a natural curvature tensor to zero without an ownership premise;
4. treating comparison composition as a bulk field equation; and
5. treating calibration, an asymptote, topology, or boundary values as an interior operator.

It does not rule out a native response law, a global admissibility rule, a selected completion that
nonlocally restricts interior jets, or a bootstrap relation. It also does not cover other chart
components, split-changing, null, rank-changing, or cut-locus strata. It says each further
restriction must enter as a genuine nonidentity premise or be derived from an additional owned
structure—not from this chart algebra.

## 7. Smallest next joint

The smallest honest candidate is a covariant global--local admissibility relation of type

```text
R(j^k g ; G_global)=0,                               (8)
```

where `G_global` denotes owned completion data. It must be nonidentity, must reduce the open history
space, and must come with its own ownership and boundary/variation semantics. Equation (8) is a
type signature, not a proposed formula. Bootstrap could eventually be one interpretation of such
a relation, but no density, energy, curvature target, integral, or functional is invented here.

No action, source, carrier, matter, mass, `X_max` value, CMB spectrum, signalling law, or physical
regime is derived.
