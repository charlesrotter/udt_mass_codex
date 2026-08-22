# G222 exact derivation — null-incidence pair plane and screen join

Date: 2026-08-22

## Primary bounded result

One supplied smooth null-incidence family already contains the full local pair plane. Its two
tangents are

\[
K=F_*\partial_\lambda,
\qquad
J=F_*\partial_y.
\]

Here `K` follows each null generator and `J` compares neighboring clock incidences. The metric gives
the conserved positive area density

\[
\boxed{a=-g(J,K)>0}.
\]

That density is exactly the G176 reciprocal ruler density on the clock-regular stratum. The G188
quotient screen is canonically the positive normal bundle of this pair plane. No scalar score is
added after the pullback.

## 1. Supplied null variation

Let `F(y,lambda)` be a smooth two-parameter variation by affinely parametrized future null
geodesics. Then

\[
g(K,K)=0,
\qquad
\nabla_KK=0,
\qquad
[J,K]=0.
\]

Torsion freedom gives `nabla_K J=nabla_J K`. Differentiating once more gives the longitudinal
Jacobi equation in the G188 curvature convention,

\[
\boxed{\nabla_K\nabla_KJ+R(J,K)K=0}.
\]

Thus the missing tangent is not a new mechanism. It is the event-incidence Jacobi field of the same
query.

## 2. The conserved null area density

Differentiate the mixed product along a generator:

\[
\begin{aligned}
K\,g(J,K)
&=g(\nabla_KJ,K)+g(J,\nabla_KK)\\
&=g(\nabla_JK,K)\\
&=\tfrac12J\,g(K,K)=0.
\end{aligned}
\]

Therefore

\[
\boxed{a=-g(J,K)}
\]

is constant along each ray. Use `y=tau_A` and fixed boundary labels. At the source and target,

\[
J_A=U_A,
\qquad
J_B=r_{AB}U_B.
\]

If `K` is the metric dual of the null covector used by G220--G221, then

\[
\mathcal W=-g(U,K)>0.
\]

Consequently,

\[
a=\mathcal W_A=r_{AB}\mathcal W_B,
\]

and hence

\[
\boxed{r_{AB}=\frac{\mathcal W_A}{\mathcal W_B}}.
\]

The full-plane calculation therefore recovers the G221 clock chord rather than replacing it.

## 3. Full rank-two pullback

In the supplied `(y,lambda)` chart,

\[
\boxed{
h=F^*g=
\begin{pmatrix}
g(J,J)&-a\\
-a&0
\end{pmatrix}.}
\]

Its determinant is

\[
\boxed{\det h=-a^2<0}.
\]

Thus `J` and `K` remain linearly independent and span a Lorentzian rank-two plane everywhere on the
regular positive-frequency branch. This conclusion does not require `J` itself to stay timelike.

On a clock-regular patch write

\[
g(J,J)=-T^2,
\qquad T>0.
\]

The unique positive shifted decomposition gives

\[
\beta_\lambda=\frac{a}{T^2},
\qquad
L_\lambda^2=\frac{a^2}{T^2}.
\]

G176 completed-pair reciprocity therefore fixes

\[
\boxed{m=T L_\lambda=\sqrt{-\det h}=a}.
\]

In the calibrated vertical coframe

\[
\vartheta=a\,d\lambda,
\]

the completed pair metric is

\[
\boxed{
h=-T^2\left(dy+T^{-2}\vartheta\right)^2+T^{-2}\vartheta^2
=-T^2dy^2-2dy\,\vartheta.}
\]

At the target `T_B=r_AB`, so

\[
\boxed{\Phi_{AB}=-\log T_B=-\log r_{AB}=\delta_{AB}}.
\]

The clock, ruler density, and shift are now three entries of one pair plane.

## 4. Affine normalization and the coordinate boundary

Under a positive affine reparameterization along a ray, `K` and `a` scale together. The product

\[
a[d\lambda]
\]

in the vertical cotangent line is invariant. Adding a multiple of `K` to `J` changes the horizontal
lift but not the geometric plane or `a`.

There is nevertheless a real local-to-global distinction. Since `K(a)=0`, in one pair chart

\[
d(a\,d\lambda)
=(\partial_y a)dy\wedge d\lambda.
\]

Therefore `vartheta` is the differential of a scalar ruler coordinate on the whole two-surface only
where it is closed. G176's unique positive density remains valid pointwise and along each ruler
fiber; it must not be silently promoted to a global coordinate when `partial_y a` is nonzero.

### Exact nonclosed flat witness

In flat `1+1` Minkowski space, let

\[
c(y)=1+\epsilon y,
\qquad \epsilon>0,
\]

and

\[
F(y,\lambda)=\bigl(y+\lambda c(y),\lambda c(y)\bigr).
\]

Then

\[
K=c(y)(\partial_t+\partial_x),
\]

is affine and null, while

\[
J=(1+\epsilon\lambda)\partial_t+\epsilon\lambda\partial_x.
\]

Directly,

\[
-g(J,K)=c(y),
\qquad
\det(F^*g)=-c(y)^2.
\]

The source curve is `A(y)=(y,0)`. The target curve is

\[
B(y)=(y+c(y),c(y)),
\]

whose tangent norm is `-(1+2 epsilon)`, so it is timelike. Its proper-clock slope is

\[
r_{AB}=\sqrt{1+2\epsilon}.
\]

The endpoint frequencies are

\[
\mathcal W_A=c(y),
\qquad
\mathcal W_B=\frac{c(y)}{r_{AB}},
\]

and the G221 ratio holds exactly. But

\[
d(c(y)d\lambda)=\epsilon\,dy\wedge d\lambda\ne0.
\]

This proves that the vertical reciprocal density can be fully metric-derived on a supplied null
family while a global ruler coordinate remains unavailable.

## 5. Canonical join to the G188 screen

Let

\[
\mathcal P=\operatorname{span}(J,K),
\qquad
\mathcal N=\mathcal P^\perp.
\]

Because `det h<0`, `P` is Lorentzian and its rank-two normal plane `N` is positive definite. G188's
screen is

\[
\mathcal S=K^\perp/\langle K\rangle.
\]

For `X in K^perp`, define

\[
\boxed{
\iota_J([X])
=X-\frac{g(X,J)}{g(K,J)}K.}
\]

This vector is orthogonal to both `J` and `K`. Replacing `X` by `X+bK` leaves the result unchanged,
so the map is representative-independent. Adding `cK` to `J` also leaves it unchanged. For any
`X,Y in K^perp`,

\[
g(\iota_J[X],\iota_J[Y])=g(X,Y).
\]

Thus

\[
\boxed{\mathcal S\cong\mathcal N}
\]

canonically and isometrically on the supplied pair plane.

If `X` is a screen field, `nabla_K X` remains in `K^perp`. The map above sends the G188 quotient
connection `[nabla_K X]` to the normal projection of `nabla_K iota_J[X]`. It likewise sends
`[R(X,K)K]` to the normal tidal projection. Therefore the G188 finite Jacobi matrix is exactly the
normal-screen channel of the same null pair family.

It remains matrix-valued. Neither it nor its determinant is determined by the scalar `r_AB`.

## 6. Degenerate and turning strata

- `a=0` gives `det h=0` and leaves the regular pair-plane theorem. Positive observer frequency
  excludes it on the declared boundary branch.
- `g(J,J)=0` is a turning point of the chosen clock coordinate. The pair plane remains Lorentzian
  because its determinant is still `-a^2`; the `T>0` decomposition does not continue through it in
  that chart.
- `det D=0` for the G188 transverse Jacobi map is a screen caustic. It does not by itself make the
  longitudinal pair plane degenerate.
- Multiple null branches give multiple supplied ribbons. No branch aggregation is derived.

## 7. Landing and ceiling

```text
SUPPLIED_NULL_FAMILY_OWNS_FULL_RANK_TWO_PAIR_PLANE_CONDITIONALLY
__CONSERVED_NULL_AREA_DENSITY_COMPLETES_RECIPROCAL_RULER
__G188_SCREEN_IS_CANONICAL_NORMAL_CHANNEL
__GLOBAL_RULER_COORDINATE_AND_PHYSICAL_PROTOCOL_REMAIN_OPEN
```

The result closes the local full-pair-plane joint for one supplied regular null family. It does not
select null incidence as the universal UDT pair protocol, populate observers or branches, integrate
a global ruler coordinate, select a complete metric realization, or derive `X_max`, transfer,
observations, action, source, matter, bootstrap, mass, or signalling.
