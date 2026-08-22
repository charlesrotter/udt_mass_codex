# G209 exact derivation — time-space shift robustness

Date: 2026-08-21

## Bounded landing

```text
FULL_LOCAL_TIMESPACE_SHIFT_IS_AN_EXACT_INDEPENDENT_METRIC_SECTOR
__IT_TRANSLATES_THE_CAUSAL_ELLIPSOID_WITHOUT_CHANGING_SIGNATURE_OR_AMBIENT_DETERMINANT
__GROWTH_CONTROLLED_AND_UNIFORMLY_SUBLUMINAL_G205_CLASSES_SURVIVE
__A_SMOOTH_BOUNDED_COORDINATE_SHIFT_CAN_PRESERVE_GLOBAL_HYPERBOLICITY_WHILE_DESTROYING_NULL_COMPLETENESS
__COMPLETED_PAIRS_HEAR_SHIFT_BEFORE_READOUT
__NO_PHYSICAL_SHIFT_HISTORY_OR_XMAX_SELECTION
```

This is a conditional metric classification. It does not select a shift or a physical UDT history.

## 1. Complete local shift sector

Let the supplied metric have positive lapse square `f` and positive spatial metric `h_A`. Relative
to its declared time foliation, write every tangent vector as

\[
X=\alpha\partial_t+v.
\]

The full three-component shift vector `b` enters by

\[
\boxed{g_b(X,X)=-f\alpha^2+h_A(v+\alpha b,v+\alpha b).}
\]

In a spatial basis with matrix `H`,

\[
g_b=
\begin{pmatrix}
-f+b^THb&(Hb)^T\\
Hb&H
\end{pmatrix}.
\]

It factors by congruence as

\[
g_b=P_b^T
\begin{pmatrix}-f&0\\0&H\end{pmatrix}P_b,
\qquad
P_b=\begin{pmatrix}1&0\\b&I_3\end{pmatrix},
\qquad \det P_b=1.
\]

Sylvester inertia and the determinant therefore give

\[
\operatorname{inertia}(g_b)=(-,+,+,+),
\qquad
\boxed{\det g_b=-f\det H.}
\]

The inverse is

\[
\boxed{
g_b^{-1}=
\begin{pmatrix}
-1/f&b^T/f\\
b/f&H^{-1}-bb^T/f
\end{pmatrix}.}
\]

In particular,

\[
\boxed{g_b^{-1}(dt,dt)=-1/f<0.}
\]

Thus `t` remains temporal for every smooth finite shift. Shape and shift are independent local
metric sectors: arbitrary positive `H` determines the ellipsoid shape, while `b` translates it.
Trace-changing spatial shape does not need to be frozen for this theorem.

## 2. Exact shifted causal cone

Parameterize a causal curve by `t`, so its tangent is `partial_t+v`. Then

\[
g_b(\partial_t+v,\partial_t+v)\le0
\quad\Longleftrightarrow\quad
\boxed{h_A(v+b,v+b)\le f.}
\]

The causal-velocity ellipsoid is centered at `v=-b`; its width remains set by `f` and `h_A`. For
any spatial covector `ell`, Cauchy-Schwarz gives

\[
|\ell(v)+\ell(b)|
\le \sqrt f\,|\ell|_{h_A^{-1}}.
\]

With `ell=dr`,

\[
\boxed{|dr(v)+dr(b)|\le\sqrt f\,|dr|_{h_A^{-1}}.}
\]

On the G205 spatial metric

\[
h_0=f^{-1}dr^2+r^2d\Omega^2,
\]

this becomes

\[
\boxed{\left|\frac{dr}{dt}+b^r\right|\le f.}
\]

On the G208 radial-screen mixing tile,

\[
|dr|_{h_A^{-1}}=\sqrt{f\cosh(2s)},
\]

so the width is

\[
f\sqrt{\cosh(2s)}.
\]

This shows explicitly how the sectors interlock: shape changes width; shift changes center.

## 3. Growth-controlled Cauchy theorem

Assume the spatial manifold is the declared G205 `R^3`, with its smooth Cartesian center and compact
angular spheres. On every finite time slab `I`, suppose

\[
|dr(b)|+\sqrt f\,|dr|_{h_A^{-1}}\le q_I(r)
\]

for a positive locally bounded function satisfying

\[
\int^\infty\frac{dr}{q_I(r)}=\infty.
\]

Every causal curve parameterized by `t` then obeys

\[
\left|\frac{dr}{dt}\right|\le q_I(r).
\]

The Osgood comparison integral prevents escape to `r=infinity` at finite `t`. If an inextendible
causal curve had a finite `t` endpoint while `r` stayed bounded, it would lie in
`I x {r<=R}`. Closed `r`-balls are compact in the declared G205 `R^3`; smoothness and positivity of
`f,h_A` plus the causal inequality give a uniform speed bound relative to one auxiliary Riemannian
metric on that compact slab. The curve therefore converges and extends through its alleged finite
endpoint, a contradiction. Hence `t` ranges from minus to plus infinity on every inextendible causal
curve and every `t=constant` slice is Cauchy.

Therefore the growth condition is a sufficient global-hyperbolicity criterion. It is not claimed
necessary. On G205, every bounded radial coordinate shift satisfies the criterion because `f` is
globally bounded and the right-hand side can be chosen constant.

## 4. Uniformly subluminal static survivor

Now specialize to G205 and assume `b` is smooth and static with

\[
|b|_{h_0}\le q\sqrt f,
\qquad 0\le q<1.
\]

For a future null geodesic put

\[
y=\dot x+b\dot t.
\]

The null equation gives

\[
|y|_{h_0}=\sqrt f\,\dot t.
\]

Stationarity gives the conserved positive energy

\[
E=-g_b(\partial_t,\dot\gamma)
=f\dot t-h_0(b,y),
\]

and Cauchy-Schwarz yields

\[
\boxed{(1-q)f\dot t\le E\le(1+q)f\dot t.}
\]

The causal radial bound is

\[
\left|\frac{dr}{dt}\right|\le(1+q)f.
\]

Meanwhile

\[
\frac{d\lambda}{dt}=\frac1{\dot t}\ge\frac{(1-q)f}{E}.
\]

Along an escaping ray,

\[
\left|\frac{d\lambda}{dr}\right|
\ge\frac{1-q}{(1+q)E},
\]

so infinite radius requires infinite affine parameter. For a bounded-radius null geodesic, if `t`
is unbounded then the positive lower bound for `f` and the energy inequality make affine parameter
unbounded as well. If `t` stays in a finite interval, the geodesic remains in a compact spacetime
slab; the energy bound controls its tangent in a smooth frame, so standard geodesic-spray extension
applies. The Cartesian center is not a boundary. Reversing orientation gives the other affine end.
Thus this static class is null complete and globally hyperbolic.

## 5. Compact-time-live survivor

Let `b=0` outside `|t|<T` and inside the live slab assume

\[
|b|_{h_0}\le q\sqrt f,
\qquad
|\partial_t b|_{h_0}\le K\sqrt f,
\qquad q<1.
\]

The instantaneous energy

\[
E=f\dot t-h_0(b,y)
\]

satisfies the exact geodesic identity

\[
\boxed{\frac{dE}{d\lambda}
=-h_0(y,\partial_t b)\dot t.}
\]

Consequently,

\[
\left|\frac{dE}{dt}\right|
\le Kf\dot t
\le\frac{K}{1-q}E.
\]

Gronwall control keeps `E` positive and finite while the causal radial bound prevents escape during
the finite live slab. Closed bounded-radius subsets of each finite G205 slab are compact; smoothness
and the energy/cone bounds uniformly control the full tangent there, so standard geodesic-spray
extension carries the geodesic across the live slab. It then enters an exact G205 exterior in both
time directions, where G205 is null complete. Hence this compact-live class is null complete and
globally hyperbolic. This is not an unrestricted live-shift theorem.

## 6. Smooth globally hyperbolic but null-incomplete witness

Take the static radial coordinate shift

\[
b=b(r)\partial_r,
\qquad
b(r)=v\frac{r}{\sqrt{R^2+r^2}},
\qquad v,R>0.
\]

In Cartesian coordinates,

\[
b=v\frac{x^i}{\sqrt{R^2+|x|^2}}\partial_i,
\]

so it is smooth at the center. Its coordinate component is bounded by `v`. Since

\[
\left|\frac{dr}{dt}\right|\le v+f_{\max},
\]

the growth-controlled theorem proves global hyperbolicity.

For an equatorial null geodesic, let `p_t=-E`, `p_phi=L`, and `p_r` be the radial momentum. The
inverse metric gives

\[
0=2\mathcal H
=-\frac{E^2}{f}-\frac{2bE}{f}p_r
+\left(f-\frac{b^2}{f}\right)p_r^2
+\frac{L^2}{r^2}.
\]

Hamilton's radial equation and this constraint yield

\[
\boxed{
\dot r^2
=E^2-\left(f-\frac{b^2}{f}\right)\frac{L^2}{r^2}.}
\]

For `L!=0`, sufficiently far out `b` is bounded away from zero, `f` tends to zero, and

\[
\dot r\ge\frac{|bL|}{\sqrt{2f}\,r}.
\]

Therefore the remaining affine length is bounded above by a constant times

\[
\int^\infty r\sqrt f\,dr
=\int^\infty r e^{-\phi(r)}dr.
\]

For every registered G205 profile this integral is finite because `phi` grows as a positive even
power. Hence an outward nonradial null geodesic reaches `r=infinity` in finite affine parameter.
The spacetime is globally hyperbolic but null incomplete. The shift is bounded as a coordinate
component, but it is not uniformly subluminal in the metric norm: `|b|_{h_0}/sqrt(f)=|b|/f`
diverges. That distinction is load-bearing.

## 7. Completed observer-pair response

For supplied pair tangents

\[
J_i=\alpha_i\partial_t+v_i,
\]

the full metric pullback is

\[
\boxed{
(h_b)_{ij}
=-f\alpha_i\alpha_j
+h_A(v_i+\alpha_i b,v_j+\alpha_j b).}
\]

On the regular clock stratum,

\[
T_b^2=-h_{00}
=f\alpha_0^2-h_A(v_0+\alpha_0b,v_0+\alpha_0b),
\]

and completed Dual Reciprocity gives

\[
\boxed{\Phi_b=-\log T_b=-\frac12\log T_b^2.}
\]

Three useful strata are exact:

1. A coordinate-static clock germ (`v_0=0`) hears `h_A(b,b)` and is timelike only when
   `h_A(b,b)<f`.
2. An Eulerian-normal germ (`v_0=-alpha_0 b`) has `T_b^2=f alpha_0^2` and is shift-blind by its
   defining motion with the translated cone.
3. A generic germ contains both linear cross terms and the quadratic shift term.

Thus shift enters before pullback and reciprocal readout. A controlled blind germ is not evidence
that the metric sector is absent.

## 8. What is and is not established

The local block theorem holds for arbitrary supplied positive spatial `h_A`, so trace-changing
spatial shape does not have to be solved first. The global results are deliberately narrower: they
classify the stated G205 shift subclasses only.

No action, source, transfer law, observation, matter model, physical shift, direction, amplitude,
profile, time law, complete history, or `X_max` value/profile is selected. Timelike and spacelike
completeness, unrestricted live shifts, maximal extension, and arbitrary full spatial histories
remain open.

## Evidence precision

The 21 production identities, 10,000 independent exact-rational cases, four 120-digit outer-tail
controls, and 25 hostile catches verify the finite algebra and explicit witness estimates. The
growth-controlled Cauchy theorem and the static/live affine theorems are analytic arguments; the
finite scripts do not masquerade as machine proofs of their global quantifiers.
