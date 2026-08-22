# G210 exact derivation — spatial-volume robustness

Date: 2026-08-21

## Bounded landing

```text
FULL_LOCAL_SPATIAL_VOLUME_SCALAR_IS_THE_UNIQUE_RELATIVE_DETERMINANT_MODE
__IT_RESCALES_CAUSAL_WIDTH_WITHOUT_MOVING_THE_SHIFT_CENTER
__LOWER_BOUNDED_STATIC_AND_CONTROLLED_COMPACT_LIVE_G205_CLASSES_SURVIVE
__SIGMA_EQUALS_MINUS_PHI_IS_GLOBALLY_HYPERBOLIC_BUT_RADIAL_NULL_INCOMPLETE
__COMPLETED_PAIRS_HEAR_SPATIAL_VOLUME_BEFORE_READOUT_ON_SPATIAL_BEARING_STRATA
__NO_PHYSICAL_SIGMA_HISTORY_OR_XMAX_SELECTION
```

This is a conditional metric classification. It does not select `sigma` or a physical UDT
history.

## 1. Unique relative spatial-volume scalar

Let `H` be a supplied positive reference spatial metric and `K` any other positive spatial metric
on the same three-dimensional space. Define

\[
\boxed{\sigma=\frac16\log\frac{\det K}{\det H}},
\qquad
\overline K=e^{-2\sigma}K.
\]

Then

\[
\det\overline K=e^{-6\sigma}\det K=\det H.
\]

If also `K=e^{2\tau}\widetilde K` with `det(tilde K)=det H`, determinants give
`e^{6 tau}=det K/det H=e^{6 sigma}` and therefore `tau=sigma`. Thus the one-dimensional relative
volume scalar and determinant-one remainder are unique after the reference `H` is supplied.

This does not assert that G207/G208 exhaust all determinant-one spatial histories. It identifies
only the missing scalar determinant mode.

## 2. Complete local scalar algebra

Let `a=e^sigma>0`, keep the positive lapse square `f` fixed, and allow an arbitrary supplied shift
`b`. For `X=alpha partial_t+v`, define

\[
\boxed{
g_{\sigma,b}(X,X)
=-f\alpha^2+a^2h_A(v+\alpha b,v+\alpha b).
}
\]

In a spatial basis with matrix `H`,

\[
g_{\sigma,b}=
\begin{pmatrix}
-f+a^2b^THb&(a^2Hb)^T\\
a^2Hb&a^2H
\end{pmatrix}.
\]

The same unit-determinant shift congruence as G209 gives

\[
\operatorname{inertia}(g_{\sigma,b})=(-,+,+,+),
\qquad
\boxed{\det g_{\sigma,b}=-f a^6\det H.}
\]

The inverse is

\[
\boxed{
g_{\sigma,b}^{-1}=
\begin{pmatrix}
-1/f&b^T/f\\
b/f&a^{-2}H^{-1}-bb^T/f
\end{pmatrix}.}
\]

Hence

\[
\boxed{g_{\sigma,b}^{-1}(dt,dt)=-1/f<0.}
\]

Spatial volume changes the ambient determinant but neither the Lorentz signature nor temporal
status of `dt`.

## 3. Exact causal law and composition with shift/shape

For a causal curve parameterized by `t`,

\[
\boxed{a^2h_A(v+b,v+b)\le f.}
\]

Thus `b` still fixes the center `v=-b`, while `a` multiplies every ellipsoid radius by `a^{-1}`.
For any spatial covector `ell`,

\[
\boxed{
|\ell(v)+\ell(b)|
\le \sqrt f\,e^{-\sigma}|\ell|_{h_A^{-1}}.
}
\]

On G205,

\[
\boxed{
\left|\frac{dr}{dt}+b^r\right|
\le f e^{-\sigma}.
}
\]

If the G208 radial-screen shape is also supplied, its width becomes

\[
f e^{-\sigma}\sqrt{\cosh(2s)}.
\]

The sectors therefore interlock exactly: shape sets directional width, spatial volume rescales all
widths, and shift translates the center.

## 4. Growth-controlled Cauchy theorem

On the declared G205 `R x R3`, suppose on every finite time slab `I` that

\[
|dr(b)|+\sqrt f\,e^{-\sigma}|dr|_{h_A^{-1}}\le q_I(r),
\qquad
\int^\infty\frac{dr}{q_I(r)}=\infty.
\]

Then every causal curve obeys `|dr/dt|<=q_I(r)`. Osgood comparison prevents spatial escape at
finite `t`. If `r` stays bounded, the curve remains in a compact finite G205 slab; smoothness,
positivity, and the causal inequality give a uniform auxiliary Riemannian speed bound, so the
curve extends. Consequently `t` is Cauchy and the metric is globally hyperbolic.

For unshifted G205, if `sigma>=sigma_min` globally, then

\[
\left|\frac{dr}{dt}\right|\le e^{-\sigma_{\min}}f.
\]

Every registered G205 `f` is smooth and globally bounded, so a constant `q_I` is available and the
Osgood integral diverges. Every such lower-bounded member is therefore globally hyperbolic.

## 5. Lower-bounded static null survivor

Now take smooth static `sigma>=sigma_min` on G205 with `b=0`. For a future null geodesic,

\[
E=f\dot t>0
\]

is conserved and the null equation is

\[
a^2h_0(\dot x,\dot x)=\frac{E^2}{f}.
\]

Since the radial part of `h_0` is `f^{-1}dr^2`,

\[
\boxed{|\dot r|\le E e^{-\sigma}\le E e^{-\sigma_{\min}}.}
\]

An escaping ray therefore needs infinite affine parameter. If `r` stays bounded near an alleged
finite affine endpoint, positive lower bounds for `f` and `a` on the compact spatial set control
`dot t` and the full spatial tangent; the smooth geodesic spray extends the curve. The Cartesian
center is not a boundary. Reversal gives the other end. Thus every declared lower-bounded smooth
static member is globally hyperbolic and null complete.

No timelike or spacelike completeness conclusion is drawn.

## 6. Controlled compact-time-live survivor

Let `sigma=0` outside `|t|<T`. Inside the live slab assume

\[
\sigma\ge\sigma_{\min},
\qquad
|\partial_t\sigma|\le K.
\]

Define `E=f dot t`. The Euler--Lagrange equation and null constraint give

\[
\boxed{
\frac{dE}{d\lambda}
=-(\partial_t\sigma)E\dot t,
\qquad
\frac{d\log E}{dt}=-\partial_t\sigma.
}
\]

Gronwall control keeps `E` finite and positive across the finite slab. The lower bound on `sigma`
gives the same radial Osgood control as above, preventing escape while `t` is finite. On a bounded
spatial slab the energy and cone bounds control the full tangent, so geodesic-spray extension
applies. The curve then enters exact G205 regions in both time directions. This class is globally
hyperbolic and null complete. It is not an unrestricted live theorem.

## 7. Smooth globally hyperbolic but radial-null-incomplete witness

For every registered G205 profile set

\[
\boxed{\sigma=-\phi.}
\]

Because G205 has `phi=O(r^2)` and is analytic in `r^2` at the center, this scalar and the resulting
metric are Cartesian smooth there. Since `a^2=e^{-2\phi}=f`,

\[
g_{-\phi}=-fdt^2+dr^2+fr^2d\Omega^2.
\]

The coordinate radial light speed is

\[
\left|\frac{dr}{dt}\right|=\sqrt f=e^{-\phi},
\]

which is globally bounded and tends to zero at the outer end. The growth theorem makes `t`
Cauchy, so this metric is globally hyperbolic.

For an outgoing radial null geodesic,

\[
\boxed{
\dot r=E e^{-\sigma}=E e^\phi,
\qquad
\frac{d\lambda}{dr}=\frac{e^\sigma}{E}=\frac{e^{-\phi}}{E}.
}
\]

Every registered profile has positive even-power growth of `phi` at infinity, hence

\[
\int^\infty e^{-\phi(r)}dr<\infty.
\]

The radial null geodesic reaches the outer end in finite affine parameter. Meanwhile

\[
\frac{dt}{dr}=e^\phi
\]

has divergent integral, so the result is consistent with `t` remaining Cauchy. This is an exact
globally-hyperbolic but null-incomplete counterclass, not a selected history.

## 8. Completed observer-pair response

For supplied pair tangents `J_i=alpha_i partial_t+v_i`,

\[
\boxed{
(h_{\sigma,b})_{ij}
=-f\alpha_i\alpha_j
+e^{2\sigma}h_A(v_i+\alpha_i b,v_j+\alpha_j b).
}
\]

On the regular clock stratum,

\[
T_{\sigma,b}^2
=f\alpha_0^2
-e^{2\sigma}h_A(v_0+\alpha_0b,v_0+\alpha_0b),
\qquad
\boxed{\Phi_{\sigma,b}=-\frac12\log T_{\sigma,b}^2.}
\]

Exact strata are:

1. An unshifted coordinate-static clock (`b=0,v_0=0`) is clock/depth blind, although its ruler or
   pair area may respond.
2. A shifted coordinate-static clock hears `e^{2 sigma}h_A(b,b)`.
3. An Eulerian-normal clock (`v_0=-alpha_0 b`) is clock/depth blind by construction.
4. Every generic spatially bearing clock hears the volume mode before readout.

Ambient determinant change therefore does not imply universal pair response, and a controlled
blind stratum does not erase the sector.

## 9. Dependency boundary with G206 and the remaining lapse mode

Algebraically,

\[
g_{\sigma,b}
=e^{2\sigma}
\left[
-e^{-2\sigma}fdt^2
+h_A(dx+b\,dt,dx+b\,dt)
\right].
\]

Thus spatial-only scale equals a G206-type common conformal rescaling plus a compensating lapse
rescaling. At fixed lapse it is independent of G206; once the lapse is released, the two diagonal
scalars can be recombined. This is a dependency identity, not a field equation or physical
history law.

## 10. What is and is not established

The local theorem closes the unique one-dimensional relative spatial-determinant mode for arbitrary
positive supplied `h_A` and supplied shift. The global theorems classify only the stated G205
subclasses.

No action, source, transfer, observation, matter model, profile, physical `sigma`, complete
history, lapse law, or `X_max` is selected. Arbitrary determinant-one spatial histories,
unrestricted live fields, timelike/spacelike completeness, and maximal extension remain open.

## Evidence precision

The production identities, independent exact-rational census, and high-precision controls certify
finite algebra and boundary anchors. The quantified global conclusions above are analytic proofs;
the scripts do not independently mechanize them.
