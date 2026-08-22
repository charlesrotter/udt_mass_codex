# G207 exact derivation — trace-free angular-screen time-live robustness

Date: 2026-08-21

## Landing

```text
TRACEFREE_SCREEN_SHEAR_PRESERVES_AMBIENT_VOLUME_SIGNATURE_RADIAL_CAUSAL_BOUND_AND_G205_GLOBAL_HYPERBOLICITY
__ALL_SMOOTH_STATIC_MEMBERS_AND_COMPACT_TIME_LIVE_WITNESSES_RETAIN_NULL_COMPLETENESS
__UNRESTRICTED_SMOOTH_TIME_LIVE_SHEAR_CAN_AFFINELY_COMPRESS_A_G205_CIRCULAR_NULL_ORBIT_TO_FINITE_LENGTH
__COMPLETED_PAIR_KERNEL_HEARS_SHEAR_EXACTLY_WHEN_THE_SUPPLIED_CLOCK_GERM_HAS_SCREEN_CONTENT
__NO_PHYSICAL_S_HISTORY_OR_XMAX_SELECTION
```

Status: `DERIVED_CONDITIONAL__FRESH_EXTERNALLY_VERIFIED_WITH_CAVEATS`.

## 1. Supplied class

Start from any exact G205 member on `M=R_t x R3`,

\[
g_0=-f(r)dt^2+h_0,
\qquad
h_0=\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f>0.
\]

On `r>0`, let `S` be an `h0`-self-adjoint spatial endomorphism satisfying

\[
S(\partial_r)=0,
\qquad
\operatorname{tr}_{\rm screen}S=0,
\]

and require the resulting tensor to extend smoothly through the Cartesian center. Define

\[
A=e^S,
\qquad
h_S(v,w)=h_0(Av,Aw),
\qquad
g_S=-fdt^2+h_S.
\]

This is one exact complete-metric deformation tile. `S` is `CHOSE_EXTENSION_CLASS`; no equation in
G207 selects it.

## 2. Signature, volume, and radial channel

In an `h0`-orthonormal frame adapted to the radial line and the two screen eigenlines,

\[
S=\operatorname{diag}(0,s,-s),
\qquad
A=\operatorname{diag}(1,e^s,e^{-s}).
\]

Therefore `A` is positive and

\[
\det_{\rm screen}A=1.
\]

Because `h_S=A^*h_0`,

\[
\det h_S=(\det A)^2\det h_0=\det h_0,
\qquad
\boxed{\det g_S=\det g_0}.
\]

This is an equality of supplied histories, not a claim that volume is gauge. Positivity of `A`
also makes `h_S` positive definite, so `g_S` remains Lorentzian.

The radial direction is fixed:

\[
h_S(\partial_r,\partial_r)=\frac1f,
\qquad
h_S(\partial_r,X_{\rm screen})=0.
\]

Any causal curve parametrized by increasing `t` therefore satisfies

\[
-f+h_S\!\left(\frac{dx}{dt},\frac{dx}{dt}\right)\le0
\quad\Longrightarrow\quad
\boxed{\left|\frac{dr}{dt}\right|\le f}.
\]

The angular cones can change. Only the radial causal inequality is unchanged.

## 3. Every smooth declared `S` preserves the G205 Cauchy slices

The covector `dt` remains timelike because

\[
g_S^{-1}(dt,dt)=-\frac1f<0.
\]

Thus `t` is strictly monotone on every nonconstant future causal curve. Suppose such a curve had a
finite upper `t` endpoint. The unchanged radial inequality and the G205 divergence

\[
\int^\infty\frac{dr}{f}=\infty
\]

keep its radial coordinate bounded during a finite `t` interval. The curve therefore remains in a
compact spacetime slab. On that slab the smooth positive metric `h_S` is uniformly equivalent to a
fixed smooth Riemannian metric, and causality uniformly bounds its spatial speed. Its spatial
projection converges, so the causal curve extends past the alleged endpoint. This is a
contradiction.

The same argument works to the past. Hence `t` ranges over all of `R` on every inextendible causal
curve, and each `t=constant` slice is met exactly once. Therefore

\[
\boxed{(M,g_S)\text{ is globally hyperbolic for every smooth declared }S.}
\]

Unlike G206, this is not a conformal transfer theorem: the angular causal cones genuinely change.

## 4. Every smooth static member is null complete

For time-independent `S`, write

\[
g_S=f\,\bar g_S,
\qquad
\bar g_S=-dt^2+H_S,
\qquad
H_S=\frac{h_S}{f}.
\]

The radial component of `H_S` is `dr^2/f^2`. Every spatial curve escaping compact sets has
unbounded radius and length at least

\[
\int\frac{|dr|}{f}=\infty.
\]

The center is smooth, and on every bounded ball `H_S` is a smooth positive metric. Thus `H_S` is
complete. The ultrastatic product `bar g_S` is null complete.

Let `bar lambda` be an affine parameter for a future null geodesic of `bar g_S`. Then

\[
\frac{dt}{d\bar\lambda}=E>0,
\qquad
d\lambda=f\,d\bar\lambda
\]

is an affine parameter for `g_S`. If the geodesic has bounded radius, `f` has a positive lower
bound and `integral f dt` diverges as `t` tends to infinity. If its radius is unbounded, the null
condition in `bar g_S` gives

\[
\left|\frac{dr}{dt}\right|\le f
\quad\Longrightarrow\quad
\int f\,dt\ge\int|dr|=\infty.
\]

Both affine directions are infinite. Therefore

\[
\boxed{\text{every smooth static member of the declared screen class is null complete}.}
\]

No statement about timelike or spacelike completeness of the deformed class is made.

## 5. Smooth center-regular nonspherical screen tensor

Fix a unit Cartesian axis `a` only as a witness control. For position vector `x`, set

\[
u=a\times x,
\qquad
v=x\times u,
\qquad
K=v\otimes v-r^2u\otimes u.
\]

This is a polynomial symmetric tensor, and exact algebra gives

\[
Kx=0,
\qquad
\operatorname{tr}K=0,
\qquad
u\cdot v=0,
\]

\[
Ku=-r^2|u|^2u,
\qquad
Kv=+r^2|u|^2v.
\]

It is smooth and zero at the center and degenerates lawfully on the chosen axis. It supplies a
global screen tensor without choosing a singular global screen frame.

With `r0>0`,

\[
\frac{r^2|u|^2}{r_0^4+r^4}<1
\]

because

\[
r_0^4+r^4-r^2|u|^2=r_0^4+r^2(a\cdot x)^2>0.
\]

Let

\[
B_T(t)=
\begin{cases}
e\exp[-1/(1-(t/T)^2)],&|t|<T,\\
0,&|t|\ge T,
\end{cases}
\]

and choose the explicit time-live control

\[
S_B=\varepsilon B_T(t)\frac{K}{r_0^4+r^4}.
\]

It is smooth, nonspherical, center-regular, bounded, and exactly G205 outside a finite time slab.

For a null geodesic define `E=f dt/dlambda`. The `t` Euler-Lagrange equation gives

\[
\frac{dE}{d\lambda}=-\frac12\partial_t h_S(\dot x,\dot x).
\]

On the compact slab reached by the curve,

\[
|\partial_t h_S(w,w)|\le C h_S(w,w).
\]

Using the null identity `h_S(dot x,dot x)=E^2/f` yields

\[
\left|\frac{dE}{dt}\right|\le\frac C2E.
\]

Gronwall bounds keep `E` finite and strictly positive through the slab. The affine parameter and
tangent therefore cross it regularly; afterward the geodesic is an exact G205 null geodesic and
has infinite affine future. The past is identical. Thus `S_B` is a genuine time-live nonspherical
null-complete survivor.

## 6. Exact smooth time-live failure witness

Choose a supercritical G205 member and one of its exact circular-null radii `r_c`, so

\[
r_cf'(r_c)-2f(r_c)=0.
\]

Define the smooth supplied shear

\[
S_F=\left(\frac{t}{t_0}\right)^2
e^{2(1-r^2/r_c^2)}\frac{K}{r_c^4}.
\]

On the equator the azimuthal eigenvalue at `r=r_c` is `-(t/t0)^2`, while the radial profile

\[
b(X)=X^4e^{2(1-X^2)},
\qquad X=r/r_c,
\]

satisfies `b(1)=1` and `b'(1)=0`. Consequently, on the proposed circular orbit,

\[
g_{\varphi\varphi}=r_c^2e^{-2(t/t_0)^2}.
\]

The exact conserved azimuthal momentum `J` gives

\[
\dot\varphi=\frac{J}{r_c^2}e^{2(t/t_0)^2},
\qquad
\dot t=\frac{|J|}{r_c\sqrt{f_c}}e^{(t/t_0)^2}.
\]

Direct Christoffel reconstruction verifies:

- the null norm is zero;
- the `t` geodesic residual cancels exactly;
- the polar residual vanishes at the equator;
- the radial residual is proportional to `r_c f'_c-2f_c` and is therefore zero.

But

\[
\frac{d\lambda}{dt}
=\frac{r_c\sqrt{f_c}}{|J|}e^{-(t/t_0)^2},
\]

so the remaining affine future from `t=0` is

\[
\boxed{
\lambda_\infty-\lambda_0
=\frac{\sqrt\pi\,r_c\sqrt{f_c}\,t_0}{2|J|}<\infty.
}
\]

The curve runs to `t=infinity` and has no endpoint in the manifold. It is an incomplete null
geodesic. The metric remains smooth, Lorentzian, determinant-preserving, and globally hyperbolic.

Therefore determinant-one screen volume and global causality do not control null affine
completeness under unrestricted time-live shear.

## 7. Completed pair pullback

For a supplied regular pair germ

\[
J_i=\alpha_i\partial_t+v_i,
\]

the complete pullback is

\[
\boxed{
(h_S)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j).
}
\]

On the timelike clock stratum,

\[
T_S^2=-h_{S,00}
=f\alpha_0^2-h_0(Av_0,Av_0).
\]

Completed-pair Dual Reciprocity is applied only after this full metric pullback, so

\[
\boxed{
\Phi_S=-\frac12\log\!\left[f\alpha_0^2-h_0(Av_0,Av_0)\right].
}
\]

Relative to G205,

\[
\boxed{
\Phi_S-\Phi_0
=-\frac12\log
\frac{f\alpha_0^2-h_0(Av_0,Av_0)}
{f\alpha_0^2-h_0(v_0,v_0)}.
}
\]

Thus:

- if the supplied clock tangent is static, `v_0=0`, then `Phi_S=Phi_0` exactly;
- if it has screen content, the screen shear generically changes `Phi`;
- the pair determinant and shift can change even though the ambient determinant does not.

The orchestra is not bolted onto a scalar afterward. It is heard only through the complete metric
pullback of the supplied observer-pair germ.

## 8. What was and was not derived

G207 derives a conditional robustness/failure classification for one pure-screen configuration
tile. It does not select `S`, its axis, amplitude, time profile, a physical history, observer germ,
action, source, transfer law, observation, or `X_max`. It does not classify arbitrary
radial-screen mixing, common conformal scale, shift, trace-changing screen modes, or timelike and
spacelike completeness.
