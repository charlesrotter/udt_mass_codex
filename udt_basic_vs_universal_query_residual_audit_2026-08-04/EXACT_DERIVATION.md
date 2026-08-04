# Exact derivation — basic spacetime versus universal observer-query residuals

## 1. The apparent fork contains several inequivalent questions

Let `P_g -> M` be the regular ordered observer/ruler query bundle of a metric `g`, and let

```text
L_g(q) in E_(g,q)
```

be an equivariant residual over it. The universal equation is

```text
L_g(q)=0 for every q in P_g.
```

Five different reductions must be separated.

1. `L` itself may or may not descend to a tensor on `M`.
2. Its universal zero set is automatically an observer-independent predicate on metrics:
   `Sol_forall={g | L_g(q)=0 for every q}`.
3. That predicate may or may not be equivalent to finitely many local tensor equations.
4. An equal-zero-set replacement may or may not have the same linearized constraints.
5. A universal path law may reduce only to a global relation on complete metrics, not to a finite
   local tensor equation.

Thus “basic” can mean basic operator, basic solution predicate, finite local coefficient system, or
global section-free metric relation. These are not synonyms.

The natural codomain of the unreduced universal residual is the dependent function-space fiber

```text
g |-> Gamma(P_g,E_g).
```

The equation says that this entire section is zero. No measure, average, physical observer section,
or preferred frame is needed.

## 2. Nonbasic operator, observer-independent solution set

The exact parent control remains

```text
P_01=diag(1,1,0,0),
P_02=diag(1,0,1,0),
A=diag(2,3,5,7),
L(P,A)=trace(PA).
```

It gives

```text
L(P_01,A)=5,
L(P_02,A)=7.
```

So the residual is not basic as an operator. Nevertheless, the statement that it vanish for every
valid `P` is one invariant condition on `A`. Operator non-descent does not prevent solution-set
descent.

This logical descent alone supplies no finite local tensor equation and no dynamics. It merely
defines an observer-independent subset.

## 3. Exact local algebraic coefficient extraction

Let `eta=diag(-1,1,1,1)` and let `S` be an arbitrary symmetric covariant bilinear form. Consider the
category-A query residual

```text
L_S(u,n)=S(u,u)+S(n,n)
```

for every Lorentz-orthonormal pair

```text
eta(u,u)=-1, eta(n,n)=+1, eta(u,n)=0.
```

This is a test of architecture, not a proposed UDT equation.

Use ten component variables in the order

```text
(S00,S01,S02,S03,S11,S12,S13,S22,S23,S33).
```

Nine registered queries suffice:

- `u=e0`, with `n=e1,e2,e3`;
- `u=e0`, with `n=(e1+e2)/sqrt(2)`, `(e1+e3)/sqrt(2)`, `(e2+e3)/sqrt(2)`;
- `u=(5e0+4ei)/3`, with an orthogonal axial ruler, for `i=1,2,3`.

Their coefficient matrix has exact rank nine and kernel

```text
span(1,0,0,0,-1,0,0,-1,0,-1)=span(-eta).
```

Because these nine pairs are a subset of all queries, universal vanishing implies

```text
S=lambda eta.
```

Conversely every `S=lambda eta` obeys

```text
S(u,u)+S(n,n)=lambda[-1+1]=0
```

for every normalized pair. Hence the equivalence is exact:

```text
L_S(u,n)=0 for all (u,n)
    iff
S^TF := S-(tr_eta S/4) eta = 0.
```

The coefficient map `S -> S^TF` also has rank nine, and stacking it with the nine query equations
still has rank nine. The nonbasic universal family has reduced to a finite basic tensor equation.

## 4. More content than one scalar, but not irreducible to tensors

Take

```text
S=diag(3,1,1,1).
```

Its Lorentz trace is zero, but

```text
L_S(e0,e1)=4.
```

Therefore the universal observer family is stronger than the one scalar equation `tr_eta S=0`.
But it is not irreducible to every basic equation: it is exactly the nine-component tensor equation
`S^TF=0`.

Conversely `S=-eta` is nonzero, has Lorentz trace `-4`, and satisfies every query equation. The
universal law does not force `S=0`; it leaves the metric-proportional line free.

If `S` were later supplied as a metric-derived tensor, this architecture could impose strong
directional metric content without selecting an observer. The present UDT premises do not supply
that `S` or this residual, so the control is not a native field equation.

## 5. Equal zero sets do not determine variation

For `q in {-1,+1}`, let

```text
L(x,q)=q x.
```

The universal query system, `F(x)=x`, and `G(x)=x^2` all have the same zero set `{0}`. Their
linearizations at zero have ranks

```text
rank D L_forall = 1,
rank D F        = 1,
rank D G        = 0.
```

Thus `F` is variation-equivalent while `G` is only zero-set equivalent.

The same effect occurs in the rank-nine tensor control. The coefficient map `S^TF` has tangent rank
nine on its solution line. The scalar sum of squares of its ten displayed components has zero
gradient everywhere on that line. Replacing a universal residual by a squared norm would erase the
first-order equations. It cannot be adopted merely because it has the same zeros.

This is why an action, least-squares functional, norm, or fiber average cannot be reconstructed from
the universal zero set.

## 6. The query fiber changes with the metric

Normalized observer/ruler pairs satisfy equations involving `g`, so `P_g` changes when `g` changes.
This does not create an independent physical `delta q`. It means the residual is a section over the
total query bundle above metric configuration space.

To differentiate one may choose a local mathematical lift of normalized queries or first perform a
faithful coefficient reduction. On a regular universal solution, two lifts differ vertically, and
the vertical derivative of the identically zero fiber section vanishes. The on-shell linearized
condition is therefore lift-independent.

The exact metric-line control makes this explicit:

```text
g_eps=diag(-(1+eps),1,1,1),
u_eps=(1/sqrt(1+eps),0,0,0),
S_eps=lambda g_eps.
```

Then `L_(S_eps)(u_eps,e1)=0` identically and its total `eps` derivative is exactly zero.

This regular argument does not settle causal-domain changes, null/zero loci, rank changes, or
boundary defects. There the query domain itself can change type and the tangent/interface owner
remains open.

## 7. Global query laws need not reduce to finite local tensors

Consider two locally Euclidean quotient controls.

1. A translation quotient has loop derivative/holonomy `I`.
2. A glide-reflection quotient generated by
   `b(x,y)=(-x,y+1)` has loop derivative/holonomy `diag(-1,1)`.

Both are locally flat. Their curvature and every local curvature derivative agree—zero—at
corresponding local germs. Yet the universal loop condition

```text
Hol_g(gamma)=I for every loop gamma
```

distinguishes them.

Therefore a universal path/groupoid relation is not reducible in general to any finite local
metric-jet equation. It remains a section-free global relation on the complete metric. The two
quotients are mathematical controls only; neither is selected as UDT topology.

## 8. Zero-jet, smooth, derived, singular, and boundary classes

With only `g` and one normalized pair `(u,n)`, every scalar contraction is built from the fixed
numbers `g(u,u)=-1`, `g(n,n)=1`, and `g(u,n)=0`. Zero-jet scalar universality therefore supplies no
nontrivial dynamics. Non-scalar projectors remain query-dependent, but demanding that every such
projector vanish gives an empty rather than a useful metric solution set.

A finite algebraic query family on a regular denominator domain can often be reduced by finite
coefficient/elimination data, as the exact rank-nine control demonstrates. An arbitrary smooth
query family is naturally a possibly infinite-rank function-space residual; the founding premises
do not guarantee a finite tensor reduction.

A regular metric-derived section yields a base composite only with its full parent-metric chain
rule. Collision, zero, null, causal-change, tie/Jordan/complex, rank, and defect strata retain
set-valued or interface ownership. At a boundary, base geometry can be basic while pair
polarization remains nonbasic. Universal quantification does not select the boundary type or glue.

## 9. What the founding postulates decide

They decide that reciprocal comparison is an equivariant typed query morphism and that valid
observer frames must be treated reciprocally. They make a universal metric-derived query residual
compatible with “the metric is the theory,” because no observer section is added.

They do not supply a nontrivial residual `L(g,q)`, decide that its quantifier is universal, choose
local versus global/path dependence, or determine a residual codomain. Founded reciprocal
composition is kinematics; by itself it is not `L(g,q)=0`.

The registered SNe identity `d_L/X=z(z+2)` still constrains only the downstream typed readout. It
does not select any residual in this audit.

## 10. Exact ruling

```text
UNIVERSAL_QUERY_OPERATOR_NEED_NOT_BE_BASIC;
ITS_ALL_QUERY_ZERO_SET_IS_AN_OBSERVER_INDEPENDENT_METRIC_PREDICATE;
THE_REGISTERED_LOCAL_ALGEBRAIC_FAMILY_REDUCES_EXACTLY_TO_A_RANK_NINE_BASIC_TRACEFREE_TENSOR_SYSTEM;
THIS_IS_STRONGER_THAN_ONE_SCALAR_BUT_NOT_IRREDUCIBLE_TO_BASIC_TENSORS;
ZERO_SET_SCALARIZATION_NEED_NOT_PRESERVE_VARIATION;
GLOBAL_PATH_QUERY_CONTENT_NEED_NOT_REDUCE_TO_ANY_FINITE_LOCAL_METRIC_JET;
NO_PHYSICAL_OBSERVER_SECTION_IS_REQUIRED;
THE_FOUNDING_POSTULATES_DO_NOT_SELECT_A_NONTRIVIAL_RESIDUAL_OR_ITS_LOCAL_GLOBAL_CLASS.
```

No native action, source, carrier, boundary functional, bootstrap equation, density, branch,
`X_max`, matter, mass, or dynamics is derived.
