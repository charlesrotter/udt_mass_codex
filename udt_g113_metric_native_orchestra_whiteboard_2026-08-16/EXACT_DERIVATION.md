# G113 exact derivation — bounded spherical chord and center test

Date: 2026-08-16

## 1. Local metric-native assembly

For a supplied smooth time-oriented metric `g`, observer `z(tau)`, and normalized celestial field
`k(tau,n)`, G110 defines

\[
F(\tau,\lambda,n)=\operatorname{Exp}_{z(\tau)}[\lambda k(\tau,n)],
\qquad dF=(T,K,J_1,J_2).
\]

The basis-independent pullback is

\[
\mathcal H=F^*g=
\begin{pmatrix}
h_\parallel&C\\
C^T&h_\angle
\end{pmatrix}.
\]

`h_parallel` and the screen projection of `(J1,J2)` have different domain types. Along a fixed
ray, the Jacobi equation is second order, so the closed propagation state is

\[
\left(J,D_KJ\right),
\]

not `J` alone and not terminal `phi_pair`. This is an `ARGUMENT` identifying the minimal closed
transport state; no physical-history selector follows.

## 2. Static spherical radial-null pullback

Take the conditional metric

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f(r)>0,
\]

where `f=exp(-2 phi)`. An outgoing radial null graph satisfies

\[
\frac{dt}{dr}=\frac{1}{c_E f(r)}.
\]

Let

\[
t(\tau,r)=\tau+\frac1{c_E}\int_0^r f(s)^{-1}ds,
\qquad y^0=c_E\tau,quad y^1=r.
\]

Its pair pullback is

\[
h_{00}=-f,qquad h_{01}=-1,qquad h_{11}=0,
\]

so

\[
\det h_\parallel=-1
\]

and the terminal reciprocal readout is

\[
\phi_{\rm pair}
=\frac14\log\frac{-\det h_\parallel}{h_{00}^2}
=-\frac12\log f
=\phi.
\]

At a smooth spherical center, varying the initial sky angle rotates the radial geodesic by the
`SO(3)` action. In matched sky and parallel screen bases its angular Jacobi map is

\[
\mathcal D_{\rm sky}=r I_2.
\]

This proves a conditional one-function chord. It assumes staticity, a central observer, spherical
symmetry, areal radius, radial null rays, matched bases, and the displayed reciprocal gauge.

## 3. P1 inversion

The frozen P1 chord is

\[
r(\Phi)=nX_{\rm eff}\left(1-e^{-2\Phi/n}\right).
\]

If one additionally identifies `Phi=phi_pair=phi(r)` on the static chord, then

\[
\phi(r)=-\frac n2\log\left(1-\frac{r}{nX_{\rm eff}}\right),
\]

and

\[
f(r)=e^{-2\phi(r)}
=\left(1-\frac{r}{nX_{\rm eff}}\right)^n.
\]

The origin derivatives are

\[
\phi'(0)=\frac1{2X_{\rm eff}},
\qquad f'(0)=-\frac1{X_{\rm eff}}.
\]

They violate the even-in-radius expansion required of smooth rotationally invariant center data.

## 4. Direct curvature certificate

For

\[
g=\operatorname{diag}\left(-f,f^{-1},r^2,r^2\sin^2\theta\right),
\]

direct construction of all Christoffel symbols and the Ricci tensor gives

\[
R=-f''-\frac{4f'}r+\frac{2(1-f)}{r^2}.
\]

Substitution of the P1 `f(r)` yields

\[
\lim_{r\to0}rR=\frac6{X_{\rm eff}}.
\]

The orthonormal angular sectional curvature is

\[
R_{\hat\theta\hat\varphi\hat\theta\hat\varphi}
=\frac{1-f}{r^2},
\]

so

\[
\lim_{r\to0}r
R_{\hat\theta\hat\varphi\hat\theta\hat\varphi}
=\frac1{X_{\rm eff}}.
\]

The divergence is curvature, not spherical-coordinate degeneracy.

## 5. Null-cone versus spatial-profile type

The SNe chord supplies `r(Phi)` only after conditional redshift, screen, and transfer typing. It
does not say that `Phi` is a time-independent spatial scalar. A time-live geometry can have smooth
spatial center data while the derivative along a past null cone is nonzero because temporal,
source-congruence, or intersection data contribute.

The present result therefore excludes only:

```text
exact P1 chord + static central identification + smooth point-observer vertex.
```

It does not exclude a regular time-live realization, an annular static witness over the observed
domain, or the P1 chord as an empirical calibration.
