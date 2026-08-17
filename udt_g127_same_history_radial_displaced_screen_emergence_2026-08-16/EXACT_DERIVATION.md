# G127 exact derivation — one metric, radial and tilted screens

Date: 2026-08-16

Status: `BLIND_VERIFIED__DERIVED_LOCALLY__PRODUCTION_26_OF_26__INDEPENDENT_17_OF_17__PACKAGE_PASS`

## 1. Result first

One supplied nonlinear reciprocal spherical metric produces both a symmetry-radial isotropic
screen and a nonisotropic tilted screen at the same finite-radius event through its own curvature
and the same G110 observer-exponential/Jacobi law.

This local radial control is consistent with G119's broader radial-isotropy result, but it is not
literally G119's center-vertex query. Separately, the same metric family admits that central query.

No angular response function, amplitude coefficient, extra `mu`, second metric history, SNe datum,
or R5 datum enters the derivation.

This is local kinematic emergence. It does not select the metric history or predict an observed
angular curve.

## 2. One exact metric history

Set `c_E=1` inside the dimensionless curvature calculation and take

\[
ds^2=-e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
\tag{1}
\]

At one regular finite-radius event use the orthonormal frame

\[
e_t=e^{\phi}\partial_t,\quad
e_r=e^{-\phi}\partial_r,\quad
e_\theta=r^{-1}\partial_\theta,\quad
e_\psi=(r\sin\theta)^{-1}\partial_\psi.
\tag{2}
\]

The following curvature scalars are computed from this one metric at this one event:

\[
\begin{aligned}
T&=R(e_r,e_t,e_t,e_r),\\
U&=R(e_\theta,e_t,e_t,e_\theta),\\
V&=R(e_\theta,e_r,e_r,e_\theta),\\
W&=R(e_\psi,e_\theta,e_\theta,e_\psi).
\end{aligned}
\tag{3}
\]

Spherical symmetry supplies the equivalent angular components. Direct Christoffel/Riemann
reconstruction gives

\[
\begin{aligned}
T&=e^{-2\phi}(2\phi'^2-\phi''),\\
U&=-e^{-2\phi}\frac{\phi'}r,\\
V&=+e^{-2\phi}\frac{\phi'}r,\\
W&=\frac{1-e^{-2\phi}}{r^2}.
\end{aligned}
\tag{4}
\]

## 3. Symmetry-radial query at the shared finite-radius vertex

For

\[
k_{\rm rad}=e_t+e_r,
\tag{5}
\]

the screen is spanned by `(e_theta,e_psi)`. Its optical tidal matrix is

\[
\mathcal R_{\perp,\rm rad}=(U+V)I_2.
\tag{6}
\]

This is isotropic for every spherical metric. In the reciprocal areal subfamily (1), equation (4)
further gives

\[
U+V=0.
\tag{7}
\]

That zero is specific to this bounded subfamily; isotropy is the broader G119 result.

## 4. Tilted query at the same event on the identical history

At the same event, choose

\[
v=\cos\alpha\,e_r+\sin\alpha\,e_\theta,
\qquad k_\alpha=e_t+v,
\tag{8}
\]

with screen basis

\[
s_1=-\sin\alpha\,e_r+\cos\alpha\,e_\theta,
\qquad s_2=e_\psi.
\tag{9}
\]

The code verifies exactly that `k_alpha` is null and `(s1,s2)` is an orthonormal screen. Static
spherical curvature gives

\[
\mathcal R_{\perp,\alpha}=
\begin{pmatrix}
\sin^2\alpha\,T+\cos^2\alpha\,U+V&0\\
0&U+\cos^2\alpha\,V+\sin^2\alpha\,W
\end{pmatrix}.
\tag{10}
\]

Therefore

\[
(\mathcal R_{\perp,\alpha})_{11}-(\mathcal R_{\perp,\alpha})_{22}
=\sin^2\alpha\,\Xi,
\tag{11}
\]

where the spherically adapted curvature contrast is

\[
\boxed{
\Xi=T-U+V-W
=e^{-2\phi}\left(2\phi'^2-\phi''+\frac{2\phi'}r\right)
-\frac{1-e^{-2\phi}}{r^2}.}
\tag{12}
\]

The two queries differ only in their null direction. They use exactly the same `phi`, derivatives,
metric, curvature tensor, event, observer-exponential law, and point-vertex screen normalization.

## 5. Emergent Jacobi anisotropy and optical shear

G110 fixes point-observer data up to matched screen gauge:

\[
\mathcal D(0)=0,\qquad \mathcal D'(0)=I.
\tag{13}
\]

The Jacobi equation then yields

\[
\mathcal D(\lambda)
=\lambda I-\frac{\lambda^3}{6}\mathcal R_\perp(0)+O(\lambda^4).
\tag{14}
\]

Combining (11) and (14),

\[
\mathcal D_{11}-\mathcal D_{22}
=-\frac{\lambda^3}{6}\sin^2\alpha\,\Xi+O(\lambda^4).
\tag{15}
\]

Equation (11) is a **tidal eigenvalue contrast**, not itself optical shear. Equation (15) is the
corresponding Jacobi-map eigenvalue difference. The optical deformation matrix is

\[
\mathcal B=\mathcal D'\mathcal D^{-1}
=\frac{I}{\lambda}-\frac{\lambda}{3}\mathcal R_\perp(0)+O(\lambda^2),
\tag{16}
\]

so its trace-free part—the optical shear—is

\[
\mathcal B_{\rm TF}=-\frac{\lambda}{3}
  (\mathcal R_\perp)_{\rm TF}+O(\lambda^2),
\qquad
(\mathcal B_{\rm TF})_{11}-(\mathcal B_{\rm TF})_{22}
=-\frac{\lambda}{3}\sin^2\alpha\,\Xi+O(\lambda^2).
\tag{17}
\]

Thus the first local angular shape distortion is forced by the metric curvature. It is absent for
the symmetry-radial query and generally present for a tilted query. Exact `O(2)` screen-basis
changes preserve the trace, determinant, and squared trace-free norm.

## 6. Regular nonlinear witness

The result is not merely formal. Use the smooth-center profile

\[
\phi(r)=\frac12\log(1+q r^2),\qquad q>0.
\tag{18}
\]

Then

\[
\Xi(r)=\frac{q^2r^2(3-q r^2)}{(1+q r^2)^3}.
\tag{19}
\]

It approaches zero at the regular center but is nonzero generically. At `q=r=1`,

\[
(T,U,V,W)=\left(\frac14,-\frac14,\frac14,\frac12\right),
\qquad \Xi=\frac14.
\tag{20}
\]

For `cos(alpha)=3/5`, `sin(alpha)=4/5`,

\[
\mathcal R_{\perp,\rm rad}=0,
\qquad
\mathcal R_{\perp,\alpha}=
\begin{pmatrix}8/25&0\\0&4/25\end{pmatrix},
\tag{21}
\]

and the Jacobi cubic eigenvalue difference is exactly `-2/75`.

Equation (19)'s zeros or sign are not physical regime boundaries; this profile is a certification
witness, not a selected cosmology.

## 7. What was removed and what remains

Removed in this bounded class:

- an independently chosen angular response law;
- an independently chosen angular amplitude;
- an appended scalar `mu`;
- a separate angular metric history;
- SNe or R5 data as inputs to the angular response.

Still supplied/open:

- the metric history `phi(r)` itself;
- the observer/query and its physical universality;
- time dependence and genuinely nonspherical histories;
- finite propagation, caustics, source/branch populations, transfer, and observed curves;
- physical-history selection and every global/downstream claim.

## 8. Bounded landing

```text
SAME_HISTORY_RADIAL_AND_TILTED_SCREEN_EMERGENCE_DERIVED_LOCALLY
__SYMMETRY_RADIAL_SCREEN_AT_THE_SHARED_FINITE_RADIUS_VERTEX_IS_ISOTROPIC
__TILTED_QUERY_TIDAL_CONTRAST_IS_SIN2_ALPHA_TIMES_SPHERICALLY_ADAPTED_CURVATURE_CONTRAST_XI
__OPTICAL_SHEAR_FOLLOWS_FROM_JACOBI_PROPAGATION
__NO_APPENDED_ANGULAR_RESPONSE_OR_SECOND_HISTORY
__PHYSICAL_HISTORY_GLOBAL_QUERY_AND_OBSERVATIONS_OPEN
```
