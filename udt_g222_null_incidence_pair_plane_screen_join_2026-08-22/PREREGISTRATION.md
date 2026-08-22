# G222 preregistration

Date: 2026-08-22

## Hypotheses

Let `F(y,lambda)` be one supplied smooth two-parameter null-geodesic variation. Define

\[
K=F_*\partial_\lambda,
\qquad
J=F_*\partial_y.
\]

Require

\[
g(K,K)=0,
\qquad
\nabla_KK=0,
\qquad
[J,K]=0.
\]

Use `y=tau_A` and fixed source/target boundary labels so that

\[
J_A=U_A,
\qquad
J_B=r_{AB}U_B,
\qquad
r_{AB}>0.
\]

The endpoint observers are future timelike and the supplied future covector/tangent has positive
measured frequency.

## Preregistered derivation

The variation field must obey

\[
\nabla_K\nabla_KJ+R(J,K)K=0.
\]

The scalar

\[
a=-g(J,K)
\]

must be constant in `lambda`. At the boundaries it must satisfy

\[
a=\mathcal W_A=r_{AB}\mathcal W_B,
\qquad
r_{AB}=\frac{\mathcal W_A}{\mathcal W_B}.
\]

The induced pair metric in `(y,lambda)` must be

\[
h=
\begin{pmatrix}
g(J,J)&-a\\
-a&0
\end{pmatrix},
\qquad
\det h=-a^2<0.
\]

Therefore the same supplied null family must give a regular rank-two Lorentzian pair plane whenever
`a>0`, independently of a transverse-screen caustic.

On the clock-regular stratum `g(J,J)=-T^2<0`, the unique shifted decomposition must give

\[
\beta_\lambda=\frac{a}{T^2},
\qquad
L_\lambda=\frac{a}{T},
\qquad
m=T L_\lambda=\sqrt{-\det h}=a.
\]

In the calibrated vertical coframe `vartheta=a d lambda`, the completed metric must be

\[
h=-T^2\left(dy+T^{-2}\vartheta\right)^2+T^{-2}\vartheta^2.
\]

At the target boundary, `T_B=r_AB`, so the completed depth must remain

\[
\Phi_{AB}=-\log T_B=-\log r_{AB}=\delta_{AB}.
\]

The vertical density class `a[d lambda]` must be invariant under positive affine reparameterization.
It may be represented by one local scalar ruler coordinate `s` with `ds=a d lambda` only where that
one-form is closed. In a fixed `(y,lambda)` chart, constancy along each ray gives

\[
d(a d\lambda)=(\partial_y a)dy\wedge d\lambda.
\]

Thus a global pair-surface ruler coordinate is not to be asserted when `partial_y a` is nonzero.

For the G188 quotient screen

\[
\mathcal S=K^\perp/\langle K\rangle
\]

and pair normal plane `N=span(J,K)^perp`, the map

\[
\iota_J([X])
=X-\frac{g(X,J)}{g(K,J)}K
\]

must be representative-independent and an isometry. It must intertwine the quotient connection and
tidal operator with their normal projections along `K`. This joins G188 to the same pair plane but
must not collapse its matrix Jacobi map into `r_AB`.

## Mandatory controls

1. Exact source and target boundary frequency identities.
2. Exact determinant, shifted decomposition, and G176 density.
3. Positive affine-rescaling cancellation of the geometric vertical density.
4. Null-generator shifts `J -> J+cK` preserve the plane, `a`, and screen identification.
5. Screen representative shifts `X -> X+bK` preserve `iota_J([X])`.
6. The screen identification preserves inner products.
7. A nonconstant `a(y)` must fail the global-exact-coordinate test while retaining the local
   vertical density.
8. `a=0` must fail rank two; `g(J,J)=0` must leave the clock chart without falsely degenerating the
   pair plane.
9. A transverse G188 caustic must not be equated with degeneration of the longitudinal pair plane.

## Falsification contract

The landing fails if any retained regular witness violates conservation, boundary frequency,
determinant, calibration, reparameterization, screen-isometry, or type-separation identities. It
also fails if a global ruler coordinate is asserted without the closedness condition, if null is
promoted to a universal protocol, or if the G188 matrix response is scalarized.

## Maximum conclusion

At most:

```text
SUPPLIED_NULL_FAMILY_OWNS_FULL_RANK_TWO_PAIR_PLANE_CONDITIONALLY
__CONSERVED_NULL_AREA_DENSITY_COMPLETES_RECIPROCAL_RULER
__G188_SCREEN_IS_CANONICAL_NORMAL_CHANNEL
__GLOBAL_RULER_COORDINATE_AND_PHYSICAL_PROTOCOL_REMAIN_OPEN
```
