# G200 exact derivation — both nonradial null directions in the primary metric

Date: 2026-08-21

## 1. Bounded question

Use only the declared primary static-spherical UDT metric, in dimension-matched time
\(x^0=c_Et\),

\[
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

and one supplied static clock plus one supplied oriented nonradial spatial ruler.  Determine whether
the two normalized future null germs \(U\pm N\) obey different local laws, or one law sampled in
opposite radial directions.

No G191--G198 chiral complete-coframe term, fitted radial profile, observational transfer,
\(X_{\max}\), source model, or protected payload enters.

## 2. The completed nonradial pair

At a source event \(r_o>0\), choose an equatorial spatial ruler making an angle
\(0<\alpha<\pi/2\) with the outward radial direction.  With source normalization
\(-g(U_o,k_o)=1\), set

\[
E=\sqrt{f_o},\qquad
q_o=\sqrt{f_o}\cos\alpha,\qquad
L_o=r_o\sin\alpha.
\]

Ruler reversal changes both spatial components.  The two branches are therefore

\[
L_\epsilon=\epsilon L,
\qquad
q_\epsilon(0)=\epsilon q_o,
\qquad \epsilon=\pm1,
\]

not the incomplete operation that reverses only one component.

Static and axial Killing symmetry give

\[
k_\epsilon
=\frac{E}{f}\partial_0+q_\epsilon\partial_r
+\frac{L_\epsilon}{r^2}\partial_\varphi,
\]

with

\[
q_\epsilon^2=E^2-\frac{fL^2}{r^2},
\qquad
\dot q_\epsilon=\frac{L^2(2f-rf')}{2r^3}.
\]

Direct Christoffel reconstruction verifies

\[
g(k_\epsilon,k_\epsilon)=0,
\qquad
\nabla_{k_\epsilon}k_\epsilon=0
\]

for both signs.

## 3. One endpoint-frequency law

The static unit clock is \(U=f^{-1/2}\partial_0\).  Both branches give

\[
\boxed{\omega_\epsilon=-g(U,k_\epsilon)=\frac{E}{\sqrt f}.}
\]

Thus there is no local sign coefficient in the frequency law.  Different finite endpoint shifts
can occur only when the two branches reach events with different values of \(f\), equivalently
different values of \(\phi\).

## 4. Metric-derived nonradial screen

At the equator, use the G187 quotient-screen basis

\[
s_\perp=\frac1r\partial_\theta,
\]

\[
s_{\parallel,\epsilon}
=-\frac{fL_\epsilon}{Er}\partial_r
+\frac{q_\epsilon}{Er}\partial_\varphi.
\]

It obeys

\[
g(s_A,s_B)=\delta_{AB},
\qquad g(s_A,k_\epsilon)=0.
\]

The perpendicular vector is parallel.  The in-plane screen vector is parallel in the null
quotient: its covariant derivative is proportional to \(k_\epsilon\), so it does not rotate the
physical quotient screen.

## 5. Same-event tidal chord

With the curvature convention

\[
\mathcal T_{AB}=g(s_A,R(s_B,k_\epsilon)k_\epsilon),
\]

direct full-metric contraction gives, in the matched branchwise screen bases,

\[
\boxed{
\mathcal T_+=\mathcal T_-
=\begin{pmatrix}
T_\parallel&0\\
0&T_\perp
\end{pmatrix},}
\]

where

\[
T_\parallel
=\frac{L^2(rf''-f')}{2r^3},
\qquad
T_\perp
=\frac{L^2(rf'-2f+2)}{2r^4}.
\]

Both are even in the reversed spatial direction.  Therefore the primary metric has no nonradial
version of G198's chosen-family outgoing-loud/incoming-quiet switch.

## 6. First finite directional difference

Let \(\mathcal D_\epsilon\) be vertex normalized:

\[
\mathcal D_\epsilon''+\mathcal T_\epsilon(\lambda)\mathcal D_\epsilon=0,
\qquad
\mathcal D_\epsilon(0)=0,
\qquad
\mathcal D_\epsilon'(0)=I.
\]

For either diagonal mode \(A\), Taylor expansion gives

\[
D_{A,\epsilon}(\lambda)
=\lambda-\frac{T_{A,o}}6\lambda^3
-\epsilon\frac{q_o(\partial_rT_A)_o}{12}\lambda^4
+O(\lambda^5).
\]

The common cubic term is the same local chord.  The first possible branch difference is

\[
\boxed{
D_{A,+}-D_{A,-}
=-\frac{q_o(\partial_rT_A)_o}{6}\lambda^4+O(\lambda^5).}
\]

The needed gradients are

\[
\partial_rT_\parallel
=\frac{L^2(r^2f'''-3rf''+3f')}{2r^4},
\]

\[
\partial_rT_\perp
=\frac{L^2(r^2f''-5rf'+8f-8)}{2r^5}.
\]

This is a finite-history effect: the two directions begin with the same local response, then sample
opposite sides of the same radial gradient.  It is not a second law and not a chiral coefficient.

The difference vanishes at each required control:

- strict radial limit \(L=0\), recovering G199;
- flat limit \(f=1\), \(f'=f''=f'''=0\);
- initially tangential/turning case \(q_o=0\).

An exact nonflat witness gives two nonzero \(\lambda^4\) coefficients,

\[
-\frac{139\sqrt{58}}{26880},
\qquad
\frac{7\sqrt{58}}{11520},
\]

showing that finite directional differences are genuinely permitted when the primary radial
history varies.

## 7. Bounded landing

```text
ONE_PRIMARY_NONRADIAL_LAW
__FINITE_DIRECTIONAL_DIFFERENCE_IS_RADIAL_REGIME_SAMPLING
```

This is complete for the local same-event law and the vertex series through the first possible
directional split for both reversed nonradial germs of the supplied smooth primary metric at
\(r_o>0\).  It does not select \(f(r)\), derive a loud--quiet--loud amplitude profile, construct a
nonspherical/time-live metric, choose observer populations or endpoint intersections, or derive
global completion, transfer, observations, \(X_{\max}\), action, sources, matter, mass, bootstrap,
or signalling.
