# G280 exact derivation — projective pair position versus optical area

Date: 2026-08-27

## Landing

```text
SAME_COMPLETE_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA
__OPTICAL_AREA_IS_NOT_A_FUNCTION_OF_PHI_OR_W5_STATE_ALONE
__PRIMARY_SPHERICAL_SAME_DEPTH_PROFILES_REACH_DIFFERENT_AREAL_RADII
__DIRECT_ONE_SCALE_SNE_CURVE_REQUIRES_ADDITIONAL_AREAL_IDENTIFICATION_OR_COMPLETE_HISTORY
```

Preregistered alternative B survives. Alternative C exists only after separately declaring an
areal/projective identification; it is not a theorem of the current complete metric class.

## 1. The two native objects

For a completed radial pair arrow, the current chain gives

\[
1+z=e^{\delta},\qquad \chi=\tanh\delta,\qquad x=\ell\chi.
\]

Here `chi` is the W5 normalized projective clock-column state and `x` is its conditional
dimensionful representative after one homothety is attached.

Optical area is a different metric output. On a supplied null branch the screen Jacobi map obeys

\[
\mathcal D''+\mathcal T\mathcal D=0,\qquad
\mathcal D(0)=0,\qquad \mathcal D'(0)=I,
\]

and, before a caustic,

\[
d_A^2=\det\mathcal D.
\]

The question is whether the first object determines the second without a complete tidal history.

## 2. Complete-metric separator

Compare the regular Lorentz metrics

\[
g_0=-2\,du\,dv+dx^2+dy^2
\]

and

\[
g_a=-2\,du\,dv+dx^2+dy^2+a(x^2-y^2)du^2,
\qquad a>0.
\]

On the central null branch

\[
\gamma(\lambda)=(\lambda,0,0,0),
\]

the two metrics and their complete first metric jets agree. Every Christoffel symbol vanishes on
that branch in the displayed chart. Therefore the same endpoint clocks and the same assigned
longitudinal rapidity `delta` give the same full transported endpoint-frame arrow in both metrics:

\[
\Gamma=\cosh\delta,\qquad S_\parallel=-\sinh\delta,
\qquad \chi=\tanh\delta.
\]

The same null-frequency contraction gives the same oriented frequency ratio `exp(delta)`.

The second transverse metric jets do not agree. Direct curvature calculation gives

\[
R_{uxux}=-a,\qquad R_{uyuy}=+a.
\]

Thus the flat Jacobi map at affine length `L` is

\[
\mathcal D_0(L)=L I,
\qquad \det\mathcal D_0=L^2,
\]

while the second metric gives

\[
\mathcal D_a(L)=
\begin{pmatrix}
\sinh(\sqrt a L)/\sqrt a&0\\
0&\sin(\sqrt a L)/\sqrt a
\end{pmatrix},
\]

\[
\boxed{
\det\mathcal D_a(L)
=\frac{\sinh(\sqrt a L)\sin(\sqrt a L)}{a}.
}
\]

For `0<sqrt(a)L<pi` this is a regular positive screen area. Near the flat member,

\[
\frac{\det\mathcal D_a}{L^2}
=1-\frac{a^2L^4}{90}+O(a^4L^8).
\]

The completed pair arrow, reciprocal depth, redshift, and W5 state are identical, while the native
optical area differs. Therefore no universal function of `phi`, `chi`, and one constant scale can
recover the complete Jacobi area.

## 3. Primary static-spherical separator

The same nonselection occurs before any nonspherical broadening. Let `s=r/ell` and compare two
smooth-centered primary profiles

\[
\phi_A(s)=s^2,
\qquad
\phi_B(s)=s^2+s^4.
\]

Both obey `phi=O(s^2)` at the regular areal center. For any supplied `delta>0`, profile A reaches
that depth at

\[
s_A=\sqrt\delta,
\]

while profile B reaches the same depth at

\[
s_B=\sqrt{\frac{\sqrt{1+4\delta}-1}{2}}.
\]

They therefore have the same radial reciprocal and W5 states,

\[
\chi_A=\chi_B=\tanh\delta,
\]

but their central-spherical optical distances are

\[
d_{A,A}=\ell s_A,
\qquad
d_{A,B}=\ell s_B,
\qquad s_B<s_A.
\]

This is the exact radial statement of the remaining history freedom: knowing the value of `phi`
does not say at which areal radius that value occurs.

## 4. Why direct equality is an additional law

If one declares globally on the center-origin radial branch

\[
r=\ell\tanh\phi,
\]

then the profile is forced to be

\[
\phi(r)=\operatorname{artanh}(r/\ell).
\]

Its normalized center slope is one, not zero. A smooth spherically symmetric scalar at an areal
center must have zero first radial derivative. Thus the exact global identification conflicts with
the existing smooth-center class on that branch. This does not forbid a noncentral, bounded, or
otherwise differently typed operational identification; it proves that such an identification is
additional and must state its domain.

## 5. Consequence for SNe

The direct redshift relation remains native and unchanged. The transparent bridge

\[
d_L=(1+z)^2d_A
\]

remains an explicit conditional import. Cepheid-calibrated luminosities can attach units to an
optical reconstruction. But without a complete dimensionless metric history and null branch—or an
additional explicit areal/projective law—the data supply the shape of `d_A(phi)` rather than test a
shape predicted by `phi` alone.

The angular orchestra has not been lost. It is exactly the transverse tidal information that
separates the two optical areas. In a quiet regime it may be small, but current premises do not set
it identically to zero or determine it from one value of `phi`.

## Scope

No observational outcome, fitted coefficient, numerical resolution, field equation, source,
action, matter model, `X_max`, protected package, or Lambda-CDM distance entered the calculation.
This is a metric-configuration countermodel and a primary-radial countermodel, not a selection of
which history Nature realizes.
