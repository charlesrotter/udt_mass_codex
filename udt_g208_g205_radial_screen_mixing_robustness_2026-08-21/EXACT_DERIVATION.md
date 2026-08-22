# G208 exact derivation — radial-screen mixing robustness

Date: 2026-08-21

## Landing

```text
RADIAL_SCREEN_MIXING_PRESERVES_SIGNATURE_AND_AMBIENT_VOLUME_BUT_REPLACES_THE_RADIAL_CAUSAL_BOUND
__GROWTH_CONTROLLED_AND_BOUNDED_STATIC_CLASSES_SURVIVE
__A_SMOOTH_CENTER_REGULAR_UNBOUNDED_STATIC_MIXER_DESTROYS_GLOBAL_HYPERBOLICITY_AND_NULL_COMPLETENESS
__COMPLETED_PAIRS_HEAR_RADIAL_MIXING_BEFORE_READOUT
__NO_PHYSICAL_MIXER_HISTORY_OR_XMAX_SELECTION
```

Status:
`EXTERNALLY_VERIFIED_WITH_CAVEATS__ANALYTIC_GLOBAL_THEOREMS__INDEPENDENT_ALGEBRAIC_CORE`.

## 1. Supplied class

Start from an exact G205 member on `M=R_t x R3`,

\[
g_0=-f(r)dt^2+h_0,
\qquad
h_0=\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f>0.
\]

On `r>0`, let `e_r` be the `h0`-unit radial vector and let `W` be an angular-screen vector. Define
the `h0`-self-adjoint pure mixer

\[
C(v)=h_0(W,v)e_r+h_0(e_r,v)W.
\]

The tensor is required to extend smoothly through the Cartesian center. Put

\[
A=e^C,
\qquad
h_C(v,w)=h_0(Av,Aw),
\qquad
g_C=-fdt^2+h_C.
\]

`C` is a supplied configuration coordinate. No equation here selects it.

## 2. Common scale and shape factorize

This dependency can be settled before the new mixing calculation. For any supplied Lorentz metric
`g_A`, smooth real `Omega`, and pair immersion `F`, define

\[
\widehat g=e^{2\Omega}g_A,
\qquad
\omega=\Omega\circ F.
\]

Positive conformal rescaling preserves unparametrized null geodesics. If `lambda_A` is affine for
`g_A`, then

\[
d\widehat\lambda=e^{2\Omega}d\lambda_A
\]

is affine for `g_hat`. Pullback commutes with the rescaling:

\[
\widehat h=F^*\widehat g=e^{2\omega}F^*g_A=e^{2\omega}h_A.
\]

Consequently `T_hat=e^omega T_A` and completed-pair Dual Reciprocity gives

\[
\boxed{\widehat\Phi=\Phi_A-\omega.}
\]

Thus common scale composes exactly with any already supplied shape deformation. It can restore or
destroy affine completeness through its weight, but there is no order ambiguity or new algebraic
coupling that must precede radial-screen mixing.

## 3. Exact local mixing algebra

Let `s=|W|_h0`. In an adapted `h0`-orthonormal basis `(e_r,e_W,e_perp)`,

\[
C=\begin{pmatrix}0&s&0\\s&0&0\\0&0&0\end{pmatrix},
\qquad
A=e^C=
\begin{pmatrix}
\cosh s&\sinh s&0\\
\sinh s&\cosh s&0\\
0&0&1
\end{pmatrix}.
\]

The eigenvalues of `A` are `e^s,e^-s,1`. Hence `A` is positive and `det A=1`. The spatial metric
relative to `h0` is

\[
A^TA=
\begin{pmatrix}
\cosh 2s&\sinh 2s&0\\
\sinh 2s&\cosh 2s&0\\
0&0&1
\end{pmatrix},
\]

with eigenvalues `e^(2s),e^(-2s),1`. Therefore `h_C` is positive,

\[
\boxed{\det h_C=\det h_0,\qquad \det g_C=\det g_0,}
\]

and `g_C` remains Lorentzian. This is equality between supplied metrics, not a claim that volume
is gauge.

## 4. The radial causal law changes

For spatial velocity components `(x,y,z)` in the adapted orthonormal frame,

\[
h_C(v,v)=\cosh(2s)(x^2+y^2)+2\sinh(2s)xy+z^2.
\]

At fixed radial component `x`, minimization over `y` gives

\[
y_*=-\tanh(2s)x,
\qquad
\min_y h_C(v,v)=\operatorname{sech}(2s)x^2+z^2.
\]

Since `x=(dr/dt)/sqrt(f)`, every causal curve parametrized by increasing `t` obeys the sharp bound

\[
\boxed{
\left|\frac{dr}{dt}\right|\le f\sqrt{\cosh(2s)}.
}
\]

The G207 bound `|dr/dt|<=f` is recovered only at zero mixing. Determinant one does not prevent the
contracting eigenline from shortening outward optical travel.

## 5. Growth-controlled global hyperbolicity

The covector `dt` remains timelike because

\[
g_C^{-1}(dt,dt)=-\frac1f<0.
\]

Fix a finite time slab `I`. Suppose a radial envelope satisfies

\[
s(t,r,\vartheta,\varphi)\le b_I(r)
\]

throughout the slab and

\[
\boxed{
\int^\infty
\frac{dr}{f(r)\sqrt{\cosh(2b_I(r))}}
=\infty.
}
\]

The sharp causal inequality then prevents a causal curve from escaping to infinite radius in a
finite `t` interval. The Cartesian center is an included smooth point. Hence a finite-`t` segment
of any causal curve remains in a compact spacetime slab. On that slab the smooth positive `h_C` is
uniformly equivalent to a fixed Riemannian metric, so causality bounds the full spatial speed and
the curve extends through any alleged finite endpoint.

Therefore `t` ranges over all of `R` on every inextendible causal curve and each `t=constant` slice
is met exactly once:

\[
\boxed{
\text{the slab growth condition makes }(M,g_C)\text{ globally hyperbolic.}
}
\]

Every globally bounded mixer satisfies this condition because G205 has
`integral dr/f=infinity`. Smoothness alone does not: growth at the outer end matters.

## 6. Every bounded smooth static mixer is null complete

Assume `C` is static and `s<=S<infinity` globally. Write

\[
g_C=f\bar g_C,
\qquad
\bar g_C=-dt^2+H_C,
\qquad
H_C=\frac{h_C}{f}.
\]

The eigenvalue bounds give

\[
e^{-2S}H_0\le H_C\le e^{2S}H_0,
\]

where the G205 optical metric `H_0=h_0/f` is complete. Thus `H_C` is complete, and the ultrastatic
product `bar g_C` is null complete.

Let `bar lambda` be affine for a future null geodesic of `bar g_C`. Then `dt/dbar lambda=E>0` is
constant and

\[
d\lambda=f\,d\bar\lambda
\]

is affine for `g_C`. If the radius stays bounded, `f` has a positive lower bound and `lambda`
diverges with `bar lambda`. If the radius is unbounded, the null identity and lower metric bound
give

\[
\left|\frac{dr}{dt}\right|\le e^S f,
\qquad
\int f\,dt\ge e^{-S}\int|dr|=\infty.
\]

The same argument holds to the past. Hence every globally bounded smooth static member is null
complete. Timelike and spacelike completeness are not inferred.

## 7. A compact-time-live survivor class

Let `C` vanish outside `|t|<T`. Assume it is uniformly bounded there and that its induced spatial
metric obeys the relative derivative bound

\[
|\partial_t h_C(v,v)|\le K h_C(v,v)
\]

uniformly on the live slab. The bounded envelope proves global hyperbolicity by Section 5.

For a null geodesic set `E=f dt/dlambda`. The exact `t` Euler-Lagrange equation and null identity
give

\[
\frac{dE}{d\lambda}=-\frac12\partial_t h_C(\dot x,\dot x),
\qquad
h_C(\dot x,\dot x)=\frac{E^2}{f},
\]

and therefore

\[
\left|\frac{dE}{dt}\right|\le\frac K2E.
\]

Gronwall bounds keep `E` positive and finite across the slab. The causal growth bound keeps the
ray in a bounded radial region during that finite time, so it crosses the live slab regularly.
Outside it the ray is an exact G205 null geodesic with infinite affine extent. This proves a
genuinely time-live radial-screen mixing survivor class, not a theorem for unrestricted live
mixing.

## 8. Smooth center-regular static failure witness

Fix a unit Cartesian axis `a`, let `R=x^i partial_i`, and let `U=a cross x`. The fields are smooth,
`R` is radial, `U` is screen-tangent, and `h_0(R,U)=0`. Define

\[
C_F=
\frac{\sigma(r)\sqrt f}{r^2}
\left(R\otimes U^{\flat_{h_0}}+U\otimes R^{\flat_{h_0}}\right),
\qquad
\sigma(r)=4\phi(r).
\]

The G205 profile has `phi=r^2 psi(r^2)` with smooth `psi`, so `sigma/r^2` is smooth at the center.
All remaining factors are smooth tensor fields and both `R` and `U` vanish there. Thus `C_F`
extends smoothly through the center, is self-adjoint and trace-free, and degenerates lawfully on
the chosen axis without choosing a singular screen frame.

On the equator, the mixing magnitude is exactly `sigma`. Follow the contracting eigenline in the
outer region by imposing

\[
r\,d\varphi=-\frac{dr}{\sqrt f}.
\]

The curve escapes every compact set and its optical length in `H_C=h_C/f` is

\[
L_{m opt}
=\sqrt2\int e^{-\sigma}\frac{dr}{f}
=\sqrt2\int f\,dr.
\]

For the G205 family and `x=r/r0>=sqrt(2)`,

\[
\phi
=\frac{a}{2^n}x^2(x^2-1)^n
\ge\frac{a}{2^{2n}}x^{2n+2}.
\]

Hence the last integral is bounded by a super-exponential tail and is finite. `H_C` is therefore
incomplete. By Hopf-Rinow it has an incomplete finite-length geodesic.

The ultrastatic product `-dt^2+H_C` is not globally hyperbolic: points along a finite-length
escaping curve form a noncompact causal diamond between sufficiently time-separated endpoints.
Since `g_C=f[-dt^2+H_C]` has the same causal curves, `g_C` is not globally hyperbolic.

The incomplete unit-speed `H_C` geodesic lifts to an incomplete null geodesic of the ultrastatic
product. Its `g_C` affine length is `integral f dbar lambda`. The supplied G205 `f` has a finite
global maximum, while the `bar lambda` interval is finite, so this affine integral is finite.
Therefore

\[
\boxed{
g_{C_F}\text{ is smooth and Lorentzian but neither globally hyperbolic nor null complete.}
}
\]

This does not refute G205. It classifies a broader supplied metric deformation.

## 9. Completed pair response

For a supplied regular pair germ

\[
J_i=\alpha_i\partial_t+v_i,
\]

the complete pullback is

\[
\boxed{
(h_C)_{ij}=-f\alpha_i\alpha_j+h_0(Av_i,Av_j).
}
\]

On the timelike clock stratum,

\[
T_C^2=f\alpha_0^2-h_0(Av_0,Av_0),
\]

so completed-pair Dual Reciprocity acts only after the full mixed pullback and gives

\[
\boxed{
\Phi_C=-\frac12\log\left[f\alpha_0^2-h_0(Av_0,Av_0)\right].
}
\]

A static clock tangent is blind. A clock whose spatial part lies in the untouched one-dimensional
screen kernel is also blind. A radial clock component hears the factor `cosh(2s)`, and a generic
radial-screen clock also hears the cross term `2sinh(2s)v_r v_W`. Special nonzero equality cones
can exist, so blindness is classified by the exact quadratic form rather than by a universal
verbal rule.

The pair determinant and shift generally change even though the ambient determinant does not.
Nothing is added to `Phi` after readout.

## 10. Evidence and ceiling

The production script verifies 20 exact symbolic identities. A separately written Fraction-based
implementation passes 10,000 distinct exact local algebra/pair cases and 120,004 assertions without
importing production code or artifacts. A separate 240-digit boundary diagnostic verifies four
odd-`n` profiles, the analytic tail bound, center regularity, and five sharp-bound cancellation
controls. Twenty-three hostile mutations are caught.

The global-hyperbolicity, bounded-static null-completeness, compact-live survivor, and smooth
failure results are analytic theorems. Neither finite implementation independently proves or
mechanizes the global results. Fresh external review checked those analytic arguments and returned
`VERIFIED_WITH_CAVEATS` without mathematical refutation. Live-repository source hashes remain a
separate provenance gate and are not rerun inside the sealed no-write replay.

G208 does not select `C`, its axis, direction, amplitude, or history. It does not classify
timelike/spacelike completeness, trace-changing modes, shift, arbitrary full spatial maps,
maximal extension, observations, transfer, action/source/matter, or `X_max`.
