# G199 exact derivation — both radial null directions in the primary metric

Date: 2026-08-21

## 1. Scope and ownership correction

The tested metric is the declared primary static-spherical UDT slice, in dimension-matched time
\(x^0=c_Et\):

\[
\boxed{
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0.}
\]

This calculation does not use the G191--G198 exploratory coframe term
\(M X(d\eta+dz)\).  That term was explicitly introduced as a chosen mathematical family.  G199
asks what the primary metric already does before any such extension.

## 2. The completed radial pair supplies two null germs

At a regular event, the static unit clock and outward unit ruler are

\[
U=f^{-1/2}\partial_0,
\qquad
N=f^{1/2}\partial_r.
\]

They obey

\[
g(U,U)=-1,\qquad g(N,N)=1,\qquad g(U,N)=0.
\]

Therefore the two normalized future null directions in the pair plane are

\[
\ell_\pm=U\pm N.
\]

Ruler reversal exchanges them.  There is no continuous direction coefficient.

## 3. Exact affine radial branches

Let \(\epsilon=+1\) or \(-1\), and normalize at a source radius \(r_o\) so that
\(-g(U_o,k_o)=1\).  The conserved static energy is

\[
E=f\dot x^0=\sqrt{f_o}.
\]

The null condition and radial geodesic equation give

\[
\boxed{
k_\epsilon
=\frac{E}{f}\partial_0+\epsilon E\partial_r,}
\]

and direct Christoffel reconstruction gives

\[
\nabla_{k_\epsilon}k_\epsilon=0.
\]

Hence

\[
\boxed{r(\lambda)=r_o+\epsilon\sqrt{f_o}\,\lambda}
\]

on every connected regular interval.  The signs differ only by radial orientation.

## 4. Endpoint frequency

For the static unit clock at radius \(r\),

\[
\omega_\epsilon(r)=-g(U,k_\epsilon)=\frac{E}{\sqrt f}.
\]

It is independent of \(\epsilon\) at a fixed metric event.  With the source normalization,

\[
\boxed{
Z_{o\to s}
=\frac{\omega_s}{\omega_o}
=\sqrt{\frac{f_o}{f_s}}
=e^{\phi_s-\phi_o}.}
\]

The two orientations can of course encounter different endpoint values of \(f\).  That is
endpoint sampling, not a different local law.

## 5. Metric-derived screen and curvature

At the equator use the angular orthonormal screen

\[
s_1=r^{-1}\partial_\theta,
\qquad
s_2=r^{-1}\partial_\varphi.
\]

For both signs, direct connection evaluation gives

\[
\boxed{\nabla_{k_\epsilon}s_A=0.}
\]

Using the G188 convention

\[
\mathcal T_{AB}=g(s_A,R(s_B,k_\epsilon)k_\epsilon),
\]

full Riemann reconstruction gives

\[
\boxed{\mathcal T_+=\mathcal T_-=0_{2\times2}.}
\]

This is not a flat-space substitution.  For example, with the recorded curvature convention,

\[
R^0{}_{101}=-\frac{f''}{2f}
\]

is generically nonzero.  The radial screen contraction cancels because of the reciprocal
\(g_{00}g_{rr}=-1\) structure and areal spherical sector.  G187's exact nonradial tides are
proportional to the squared angular momentum and reduce to zero at the strict radial locus.

## 6. Finite Jacobi map

The quotient-screen equation is

\[
\mathcal D_\epsilon''+\mathcal T_\epsilon\mathcal D_\epsilon=0,
\qquad
\mathcal D_\epsilon(0)=0,
\qquad
\mathcal D_\epsilon'(0)=I.
\]

Therefore, for both radial directions,

\[
\boxed{\mathcal D_\epsilon(\lambda)=\lambda I,}
\qquad
\boxed{|\det\mathcal D_\epsilon|=\lambda^2.}
\]

At a regular calibrated center with \(f_o=1\), the outgoing relation has \(r=\lambda\), recovering
the primary areal-screen result.  G199 itself is formulated at \(r_o>0\) so that the spherical
screen basis is nonsingular; the center statement is the regular limit, not an extra premise.

## 7. Exact reconciliation with G198

G198 remains correct inside the G196 coframe

\[
\theta_{\rm screen}
=a[dX+M(\eta,z)X(d\eta+dz)].
\]

That metric contains a one-sided screen connection along \(d\eta+dz\) and no independent
\(d\eta-dz\) component.  Its loud/quiet split is therefore genuinely encoded by that supplied
metric family.

But the ownership chain shows that the chiral term was chosen at G191; it was not derived from the
primary static-spherical metric.  G199 consequently establishes:

\[
\boxed{
\text{the primary radial null pair is reversal-related and has no intrinsic chiral screen split}.}
\]

This does not mean the angular sector is disabled.  Nonradial primary-metric queries have the two
metric-fixed G187 tidal modes, and a genuinely derived nonspherical or time-dependent metric may
produce a full G188 matrix response.  What is excluded is promoting G198's chosen-family
directionality into a primary-metric theorem.

## 8. Bounded landing

```text
PRIMARY_METRIC_RADIAL_NULL_PAIR_IS_REVERSAL_SYMMETRIC
__NO_NATIVE_CHIRAL_SPLIT
__G198_ASYMMETRY_REMAINS_CHOSEN_COMPLETE_COFRAME_CONTROL
```

The theorem is complete for the two radial null germs of the supplied smooth positive primary
static-spherical metric on a regular interval.  It does not derive the profile \(f(r)\), a
nonspherical/time-live extension, physical observer population, transfer, observations,
\(X_{\max}\), global completion, dynamics, sources, matter, mass, bootstrap, or signalling.
