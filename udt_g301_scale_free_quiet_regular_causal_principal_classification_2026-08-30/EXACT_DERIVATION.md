# G301 exact derivation — scale-free quiet-regular principal class

Date: 2026-08-30

## 1. Internal bounded landing

```text
TWO_INEQUIVALENT_FULL_METRIC_QUIET_PRINCIPAL_CLASSES_SURVIVE
__GENERIC_RICCI_FLAT_AND_TRACEFREE_RICCI_WITH_ONE_CONSTANT_SCALAR_DATUM
```

Status before fresh external review:
`INTERNALLY_VERIFIED_BOUNDED_PRINCIPAL_CLASS_LEAD_WITH_CAVEATS`.

This is a conditional classification inside the frozen G301 lane. It is not a UDT field equation
and does not promote locality, second metric order, symmetric rank two, smooth quiet extension,
curvature-weight-one scale freedom, or principal completeness into founded premises.

## 2. Why smooth scale freedom removes nonlinear curvature dressings

At one event, let `K` denote an algebraic curvature tensor and let

\[
F:K\longmapsto F(K)
\]

be the curvature-dependent part of the candidate residual. In the preregistered scale-free lane,

\[
F(\lambda K)=\lambda F(K),\qquad \lambda>0,
\]

and `F` is differentiable at the flat quiet origin with `F(0)=0`. For any fixed `K`,

\[
DF_0(K)
=\lim_{t\to0^+}\frac{F(tK)-F(0)}{t}
=\lim_{t\to0^+}\frac{tF(K)}t
=F(K).
\]

Therefore

\[
\boxed{F=DF_0}
\]

throughout the star-shaped quiet domain: the map is exactly linear in curvature, not merely
linearized there.

This conclusion uses both hypotheses. Curvature ratios can produce nonlinear degree-one formulas,
but a nonconstant degree-one direction map is not differentiable at `K=0`. Higher curvature
powers are smooth but have the wrong physical weight unless a dimensionful coefficient is added.
G301 does not claim either excluded architecture is impossible outside this lane.

## 3. Natural linear contraction basis

The derivative `DF_0` is an unoriented Lorentz-equivariant linear map from algebraic curvature to a
symmetric covariant two-tensor.

The orthogonal invariant-tensor theorem says that a linear `O(1,3)`-equivariant map is assembled
from the metric and contractions; the orientation tensor is unavailable in the preregistered
unoriented lane. With one curvature tensor `K_abcd` and two free covariant output indices, the
contraction diagrams have only two types:

1. Two curvature indices remain free and the other pair is contracted. Antisymmetry in each
   curvature pair, pair exchange, and the first Bianchi identity reduce every nonzero symmetric
   output to a multiple of `Ric_ab`.
2. All four curvature indices are contracted to the scalar `R`, while the two output indices are
   supplied by `g_ab`, giving `R g_ab`.

A diagram in which one output index comes from an added metric and one from curvature reduces,
after contracting the metric's other index, to type 1. Contracting an antisymmetric pair vanishes.
There is no third metric contraction.

The two maps are independent: on a nonzero traceless-Ricci algebraic witness, `R g` vanishes while
Ricci does not; on a pure-trace witness `Ric=lambda g`, both are nonzero. The Kulkarni--Nomizu
Ricci decomposition realizes arbitrary symmetric Ricci data as an algebraic curvature tensor in
dimension four, so these trace and traceless witnesses genuinely lie in the domain.

The repair-only executable certificate begins from the full 20-dimensional algebraic-curvature
space, not this two-term conclusion. It imposes all six infinitesimal Lorentz equivariance
conditions on an arbitrary map to the 10-dimensional symmetric-two-tensor space. The resulting
1,200-by-200 system has modular rank 198 for two primes, while independently constructed Ricci and
scalar-times-metric maps are exact integer null vectors. Hence the rational intertwiner nullity is
exactly two. Because the full `O(1,3)` invariant space is a subspace of the connected-Lorentz
invariant space and both displayed maps also respect reflections, its dimension is exactly two.

Thus

\[
\boxed{E_{ab}=aR_{ab}+bR g_{ab}.}
\]

This is the rank-two two-jet contraction classification, not the adoption of any representative.
No scalar, pair plane, radial chart, or angular sector was deleted.

The absence of an order-zero term follows separately. The W3 flat quiet member forces its
coefficient to zero; independently, a nonzero term `c g_ab` would need a coefficient with
inverse-length-squared dimension, and the bounded lane admits no such operator scale.

## 4. Exact coefficient strata

Let `X_ab=R_ab`, `x=tr_g X=R`, and define

\[
T_{a,b}(X)=aX+b\,xg.
\]

The symmetric-tensor space splits into a nine-dimensional traceless subspace and a one-dimensional
pure-trace line. On those pieces `T` has eigenvalues

\[
a,\qquad \tau=a+4b.
\]

### Generic class: `a != 0` and `tau != 0`

The trace adjustment is invertible, with

\[
\boxed{
X=\frac1a\left(E-\frac b\tau(\operatorname{tr}_gE)g\right).
}
\]

Consequently every generic representative has the same zero set:

\[
E_{ab}=0\quad\Longleftrightarrow\quad R_{ab}=0.
\]

The continuum of apparent coefficients is therefore one residual-equivalence class, not a
continuum of physical laws.

### Exceptional complete-principal class: `a != 0` and `tau = 0`

This is the trace-free Ricci equation

\[
\boxed{S_{ab}=R_{ab}-\frac14R g_{ab}=0.}
\]

It is not invertibly equivalent to the generic class: the pure-trace Ricci line lies in its
kernel. The contracted Bianchi identity gives

\[
\nabla^aS_{ab}=\frac14\nabla_bR.
\]

Hence every connected solution region has

\[
R=\text{constant},\qquad R_{ab}=\frac R4g_{ab}.
\]

The operator contains no attached length, but its solutions carry one constant curvature datum.
The exact constant-curvature algebraic family

\[
R_{abcd}=K(g_{ac}g_{bd}-g_{ad}g_{bc})
\]

has `R_ab=3K g_ab` and `R=12K`, so every nonzero `K` separates this class from the Ricci-flat
class without importing an operator scale.

### Scalar-only and zero strata

For `a=0,b!=0`, the equation is only `R=0`. The trace map has rank one and admits arbitrary
nonzero traceless Ricci data. It fails the preregistered full-metric principal gate.

For `a=b=0`, the residual is the identity zero operator and selects nothing.

## 5. Quiet principal behavior of the exceptional class

The trace-free class loses one algebraic residual direction, but not a local propagating
nonzero-frequency metric mode. Linearizing its exact Bianchi consequence about a quiet background
gives, for any nonzero Fourier covector `k`,

\[
k_b\,\delta R=0.
\]

Because `k` is nonzero, `delta R=0`; then `delta S_ab=0` implies `delta R_ab=0`. Thus its local
nonzero-frequency quiet equations have the same Ricci-flat principal content. The difference is
the zero-mode/connected-region constant curvature datum.

This is a principal-class statement only. G301 does not prove a gauge-fixed nonlinear
well-posedness theorem, global hyperbolicity, boundary completion, or which data Nature supplies.

## 6. Why causal propagation does not choose between the two

For the general residual,

\[
\nabla^aE_{ab}=\left(\frac a2+b\right)\nabla_bR.
\]

Identity divergence freedom selects `b=-a/2`, a generic Ricci-flat representative. But identity
divergence freedom is exactly one of G259's explicit unowned operator-class premises. The
trace-free class instead has a lawful differential consequence that carries its scalar curvature
as one constant datum and shares the bounded quiet principal content.

Therefore G295's requirement of causal constraint propagation does not, by itself, derive
identity divergence freedom or remove the exceptional class. Selecting between the two requires
an additional statement such as:

- scalar curvature is fixed by the law (the generic class); or
- scalar curvature is a connected-history integration datum (the trace-free class).

Current UDT premises state neither.

## 7. What was actually narrowed

Within the frozen lane, the apparent infinite function freedom is gone. Smooth scale-free
two-jet rank-two laws cannot carry arbitrary nonlinear curvature dressings, and the continuum of
generic `(a,b)` formulas is one class after residual equivalence. Only one serious exceptional
full-metric quiet-principal class remains.

This is substantial conditional narrowing, but it is not the missing law. In particular, both
classes are quiet local metric classes. Neither by itself derives loud-end departures, sources,
the populated relation network, the complete global history, observations, or `X_max`.

## 8. Exact ceiling

G301 internally selects preregistered landing 2:

```text
TWO_OR_MORE_INEQUIVALENT_CLASSES_SURVIVE
```

The exact count in the bounded full-metric quiet-principal lane is two. A fresh external
adversarial review remains required. No metric component, reciprocal-kernel operator, foundational
postulate, or canon entry changed.
