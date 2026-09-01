# G313 exact derivation — the active equation is a multi-branch arena

Date: 2026-09-01
Scope: regular local smooth metric-only scale-free vacuum, with explicitly stated global witnesses

## 1. The adopted bounded equation

Write

\[
S_{ab}=R_{ab}-\frac14R g_{ab}.
\]

The owner-adopted provisional premises activate `S_ab=0` only inside G312's registered bounded
arena. Contracted Bianchi gives

\[
\nabla^aS_{ab}
=\left(\frac12-\frac14\right)\nabla_bR
=\frac14\nabla_bR=0.
\]

Therefore, on each connected regular solution region,

\[
R=4\Lambda,\qquad d\Lambda=0,\qquad R_{ab}=\Lambda g_{ab}.
\]

This fixes a local vacuum response law. It does not fix the value of `Lambda`, Cauchy data, global
topology, or which solution is physically populated.

## 2. Constant curvature is a proper subset

For a four-dimensional Einstein metric,

\[
R_{abcd}=C_{abcd}
+\frac{\Lambda}{3}(g_{ac}g_{bd}-g_{ad}g_{bc}).
\]

The equation fixes the Ricci channel but leaves the Weyl tensor `C_abcd` free subject to its own
geometric identities and evolution. Only the subfamily `C_abcd=0` has constant sectional curvature.
Thus trace-free Ricci does not imply that every solution is round de Sitter, flat Minkowski, or
anti-de Sitter.

For the constant-curvature subfamily,

\[
R_{abcd}R^{abcd}=\frac83\Lambda^2,
\qquad C_{abcd}C^{abcd}=0.
\]

The positive round G309 solution

\[
a(T)=X\cosh\!\left(\frac{T-T_0}{X}\right),
\qquad \Lambda=\frac3{X^2},
\]

is one exact member of this conformally flat subfamily.

## 3. Exact positive Weyl-active compact witness

For `Lambda>0`, consider the product metric

\[
ds^2=\Lambda^{-1}
\left[-d\tau^2+\cosh^2\tau\,d\chi^2+d\Omega_2^2\right],
\qquad \chi\sim\chi+2\pi.
\]

Each two-dimensional factor has `Ric=Lambda g`, so the product has

\[
R_{ab}=\Lambda g_{ab},\qquad R=4\Lambda.
\]

Its curvature invariants are

\[
R_{abcd}R^{abcd}=8\Lambda^2,
\qquad
C_{abcd}C^{abcd}=\frac{16}{3}\Lambda^2\ne0.
\]

It is smooth, time-live, and has compact `S1 x S2` Cauchy slices. It satisfies the same active local
equation as the round positive history but is neither round nor constant-curvature. This exact
witness alone rejects the preregistered unique-round-history landing. It does not claim that this
history is physically populated.

## 4. Same-topology non-round Cauchy data

The Gauss--Codazzi constraints for `Ric=Lambda g` are

\[
{}^{(3)}R+K^2-K_{ij}K^{ij}=2\Lambda,
\qquad
D^j(K_{ij}-\gamma_{ij}K)=0.
\]

For pure-trace homogeneous data `K_ij=h gamma_ij`, these reduce to

\[
{}^{(3)}R+6h^2=2\Lambda,
\qquad M_i=0.
\]

Fix `Lambda=3`. The round unit `S3` bounce has `R3=6` and `h=0`. Now take the Berger `S3` metric
whose left-invariant orthonormal lengths are `(1,1,3/2)`. A direct Koszul calculation gives

\[
\operatorname{Ric}^{(3)}
=\operatorname{diag}\!\left(-\frac12,-\frac12,\frac92\right),
\qquad {}^{(3)}R=\frac72.
\]

It is non-round. Choosing

\[
h^2=\frac5{12}
\]

gives `R3+6h^2=6=2Lambda`; homogeneity makes the momentum constraint vanish. G303's explicitly
conditional standard local Cauchy theorem then supplies a local development. Hence even fixed
positive `Lambda` and `S3` topology do not force the round cosh data.

At the time-symmetric slice of the product witness, `R3=6` and `K_ij=0` at the same `Lambda=3`, but
the topology is `S1 x S2`. The equation therefore leaves both shape data and topology open.

## 5. Zero and negative branches

The scalar sign is not selected by the equation. For `Lambda=0`, the exact plane-wave family

\[
ds^2=-2\,du\,dv+dx^2+dy^2+A(x^2-y^2)du^2
\]

has

\[
R_{uu}=-\frac12(H_{,xx}+H_{,yy})=0
\]

while retaining nonzero tidal/Weyl curvature for `A!=0`. Negative Einstein and Weyl-active product
sectors are likewise algebraically admitted. Their global boundary and causality completions must
be classified separately; G313 does not promote one.

## 6. The equation cannot set its own absolute scale

Under a constant homothety

\[
\widetilde g_{ab}=s^2g_{ab},
\]

the Levi--Civita connection and lower-index Ricci tensor are unchanged, while

\[
\widetilde R=s^{-2}R,
\qquad
\widetilde R_{ab}-\frac14\widetilde R\widetilde g_{ab}
=R_{ab}-\frac14Rg_{ab}.
\]

Thus `Lambda` transforms to `s^-2 Lambda`. The equation selects neither its magnitude nor an
absolute length. A curvature radius is a parameter of a supplied solution, not automatically
physical `X_max`.

## 7. Exact type of the remaining bootstrap bridge

Let `Sol` be the class of complete histories admitted by the local equation and the declared
regularity/causal scope. A compatible global bootstrap has the type

\[
\mathcal A:\operatorname{Sol}/\operatorname{Diff}\longrightarrow\{0,1\}.
\]

It is a diffeomorphism-invariant acceptance predicate on entire histories. It may test topology,
global completion, boundary data, relation-network consistency, or another whole-history property.
This does not violate Local Metric Sufficiency: after `A` accepts a metric, the local vacuum
response is still determined by that metric's finite jet. The forbidden alternative would be two
accepted histories with identical admitted local jets but different local responses solely because
of an extra hidden remote-history label.

No existing UDT premise supplies a nonidentity instance of `A`. W5/W6 and the relation network type
and evaluate histories; G305--G308 characterize the round positive Hopf branch but do not declare
that branch physically populated or reject the other Einstein branches.

## 8. Scientific landing

```text
ACTIVE_EQUATION_DEFINES_MULTIBRANCH_EINSTEIN_ARENA
__GLOBAL_ADMISSIBILITY_REMAINS_OPEN
```

The earlier “who writes phi?” problem has split cleanly:

1. the adopted bounded local equation now propagates complete metric data;
2. initial/boundary data and a still-open global admissibility rule choose a particular history;
3. observation may later calibrate or discriminate surviving constants, but is not used here.

`phi` is a presentation potential extracted from a supplied metric or completed pair. It is not one
universal radial function common to all solutions of the covariant equation.
