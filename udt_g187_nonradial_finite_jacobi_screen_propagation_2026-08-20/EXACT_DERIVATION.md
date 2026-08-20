# G187 exact derivation — finite nonradial Jacobi screen

Date: 2026-08-20

## 1. Bounded metric and query

Use dimension-matched time \(x^0=c_Et\) and the declared primary static-spherical metric

\[
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0.
\]

At an event \(o\), supply a static unit observer, a future nonradial null direction, affine
normalization \(-g(u_o,k_o)=1\), and a screen orientation. Spherical symmetry places the orbital
plane at \(\theta=\pi/2\) without choosing a physical sky axis. This is one supplied regular query,
not a selection of the physical null population.

## 2. Affine null branch

Let an overdot denote the affine derivative and define

\[
E=f\dot x^0,\qquad L=r^2\dot\varphi,\qquad q=\dot r.
\]

The Killing first integrals and null condition give

\[
\boxed{q^2=E^2-\frac{fL^2}{r^2}},
\qquad
\boxed{\dot q=\frac{L^2(2f-rf')}{2r^3}}.
\]

For the source normalization above,

\[
E=\sqrt{f_o},\qquad L=r_o\sin\alpha_o,
\qquad q_o=\sqrt{f_o}\cos\alpha_o.
\]

The strict nonradial condition is \(\sin\alpha_o>0\). Turning points \(q=0\) are allowed as long
as the metric and affine branch remain regular; no division by \(q\) occurs below.

## 3. The G186 screen propagates

Along the ray choose

\[
s_\perp=\frac1r\partial_\theta,
\]

and

\[
s_\parallel
=-\frac{fL}{Er}\partial_r+\frac{q}{Er}\partial_\varphi.
\]

Direct metric evaluation gives

\[
g(s_A,s_B)=\delta_{AB},\qquad g(s_A,k)=0.
\]

The exact connection calculation gives

\[
\boxed{\nabla_k s_\perp=0},
\qquad
\boxed{\nabla_k s_\parallel=-\frac{Lf'}{2Er}\,k}.
\]

The second equality is parallel transport in the quotient screen: adding a multiple of the null
generator does not change the screen class. At the source these two vectors span the orthogonal
complement of \(\operatorname{span}(u_o,k_o)=\operatorname{span}(u_o,n_o)\). Substitution into
the G186 projector

\[
\Pi=I-J(J^TgJ)^{-1}J^Tg
\]

returns both screen vectors, annihilates \(u_o,n_o\), and has trace two. Thus G186's local screen
is exactly the initial screen for this null query; no extra screen field is introduced.

## 4. Curvature fixes two screen modes

Use the curvature convention for which a Jacobi amplitude obeys

\[
D_A''+\mathcal T_{AB}D_B=0,
\qquad
\mathcal T_{AB}=g(s_A,R(s_B,k)k).
\]

Full Christoffel and Riemann reconstruction gives a diagonal screen tidal matrix in the propagated
orbital/reflection basis:

\[
\boxed{\mathcal T_{\perp\parallel}=0},
\]

\[
\boxed{
\mathcal T_\perp
=\frac{L^2(rf'-2f+2)}{2r^4}},
\]

\[
\boxed{
\mathcal T_\parallel
=\frac{L^2(rf''-f')}{2r^3}}.
\]

Equivalently, with \(f=e^{-2\phi}\),

\[
\mathcal T_\perp
=-\frac{L^2}{r^4}\left(rf\phi'+f-1\right),
\]

\[
\mathcal T_\parallel
=\frac{L^2f}{r^3}
\left(2r(\phi')^2+\phi'-r\phi''\right).
\]

These are two different metric-derived combinations. Their difference is not an adjustable
angular coefficient. Unless the supplied history lies on a special equality locus, the finite
screen response is anisotropic.

## 5. Finite Jacobi map

Use vertex-normalized sky data

\[
\mathcal D(0)=0,\qquad \mathcal D'(0)=I.
\]

Reflection symmetry prevents mode mixing in the propagated basis. The finite map is therefore

\[
\boxed{
\mathcal D(\lambda)
=\operatorname{diag}
\left(D_\parallel(\lambda),D_\perp(\lambda)\right)}.
\]

The in-plane entry is the unique solution

\[
D_\parallel''+\mathcal T_\parallel D_\parallel=0,
\qquad D_\parallel(0)=0,quad D_\parallel'(0)=1.
\]

It is realized exactly by differentiating the supplied one-parameter null-geodesic family with
respect to its initial angle \(\alpha_o\). The vertex derivative projects to
\(\sin^2\alpha_o+\cos^2\alpha_o=1\).

The out-of-plane entry is the rotational-Killing Jacobi field,

\[
\boxed{
D_\perp
=\frac{r\sin(\varphi-\varphi_o)}{\sin\alpha_o}}.
\]

Its affine second derivative is

\[
D_\perp''
=\frac{(\dot q-L^2/r^3)\sin(\varphi-\varphi_o)}{\sin\alpha_o},
\]

and direct substitution proves

\[
D_\perp''+\mathcal T_\perp D_\perp=0,
\qquad D_\perp(0)=0,quad D_\perp'(0)=1.
\]

This is a finite Jacobi map, not merely a local projector. It is also not a flux or luminosity
law. Those would require a separately declared radiative-transfer interface.

## 6. Endpoint-frame covariance and caustics

Under independent passive oriented screen changes \(Q_o,Q_s\in O(2)\),

\[
\boxed{\mathcal D\mapsto Q_s^T\mathcal D Q_o}.
\]

Consequently \(|\det\mathcal D|\) and the singular values are frame invariant. Generic inequality
of the two singular values is the finite nonradial shape response. A zero of either mode is a
Jacobi/caustic event, not a failure of the propagation law. The phase pair
\((\mathcal D,\mathcal D')\) remains the carried object; no inverse map is asserted through a zero.

## 7. Exact controls

For flat space \(f=1\), both tidal entries vanish and

\[
\mathcal D(\lambda)=\lambda I
\]

for every supplied nonradial angle. For the comparison metric \(f=1-2M/r\),

\[
\mathcal T_\perp=\frac{3ML^2}{r^5},
\qquad
\mathcal T_\parallel=-\frac{3ML^2}{r^5},
\]

so the trace vanishes exactly while the two modes remain nontrivial and opposite.

The production implementation passes 20 symbolic gates. An independent standard-library
implementation rebuilds the connection and curvature from the metric two-jet and passes 220,000
exact assertions on 10,000 rational witnesses. Fifteen algebraic mutation catches and fourteen
separately labelled artifact-scope mutation guards pass.

## 8. Bounded landing

```text
FINITE_NONRADIAL_JACOBI_MAP_DERIVED_CONDITIONALLY
__G186_LOCAL_SCREEN_SEEDS_TWO_METRIC_FIXED_MODES
__NONRADIAL_SHEAR_EMERGES_WITHOUT_EXTRA_COEFFICIENT
```

This is conditional on the supplied smooth positive history and nonradial null query. It does not
select a physical ray population, derive flux or luminosity, derive an observed angular pattern,
choose \(R(Z)\), establish a nonspherical or time-live history, or determine \(X_{\max}\).
