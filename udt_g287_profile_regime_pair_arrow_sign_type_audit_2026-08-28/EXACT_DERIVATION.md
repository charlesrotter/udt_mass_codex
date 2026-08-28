# G287 exact derivation — two independent signs

Date: 2026-08-28

## 1. The two typed objects

The primary profile is a scalar presentation of one supplied metric:

\[
g_\phi=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
\]

An ordered pair depth is a coordinate on one supplied comparison arrow:

\[
D(\delta_{AB})=\operatorname{diag}(e^{-\delta_{AB}},e^{+\delta_{AB}}).
\]

They are different types. The pointwise profile belongs to the ambient metric; the directed depth
belongs to an ordered relation in that metric.

## 2. Pair reversal does not reverse the profile

Endpoint reversal is

\[
R_{\rm pair}:(g_\phi,A,B,\delta_{AB})
\longmapsto(g_\phi,B,A,-\delta_{AB}).
\]

Therefore

\[
R_{\rm pair}(g_\phi)=g_\phi,
\qquad
R_{\rm pair}(\phi(r))=\phi(r).
\]

Whole-profile sign conjugation is instead

\[
C_\phi:g_\phi\longmapsto g_{-\phi}.
\]

For finite nonzero `phi`, its clock and radial coefficients change from
`(exp(-2 phi),exp(+2 phi))` to `(exp(+2 phi),exp(-2 phi))`, while the areal sphere stays fixed.
G263's exact zero-tide separator further proves that the two metrics generally have different
angular response. Hence `R_pair` and `C_phi` are not the same operation.

## 3. Why arrow sign cannot classify a symmetric regime

Any physical classifier of the same unordered pair must obey

\[
\mathcal R(A,B)=\mathcal R(B,A).
\]

If it depended only on the sign of directed depth, reversal would require

\[
\operatorname{sgn}\delta=\operatorname{sgn}(-\delta),
\]

which is false for every nonzero depth. Thus no reversal-invariant micro/cosmological classifier
can be `sign(delta_AB)` alone.

An explicit matched-reference example makes the distinction concrete. Let a quiet endpoint have
`V(A)=0`. A positive-profile endpoint with `V(B)=+3` gives `delta_AB=+3` and `delta_BA=-3`; the
ambient value at `B` remains positive in both orientations. A negative-profile endpoint with
`V(C)=-2` gives `delta_AC=-2` and `delta_CA=+2`; its ambient profile remains negative. Both signs of
directed depth therefore occur in both physical profile sectors after arrow reversal.

## 4. The exact matched reduction

When an endpoint-potential description is available,

\[
\delta_{AB}=V(B)-V(A).
\]

On a matched primary radial relation with `V=phi` and a quiet reference `phi(A)=0`, one obtains

\[
\delta_{AB}=\phi(B).
\]

This is an oriented reference reduction. Reversing the arrow gives
`delta_BA=-phi(B)` without changing `phi(B)` or the metric. The equality therefore cannot be
globalized into an identity of types.

## 5. Odd orientation and even mutual magnitude

Writing `t=exp(delta)>0`, the bounded pair coordinates are

\[
\chi=\frac{t^2-1}{t^2+1}=\tanh\delta,
\qquad
M=\frac{2t}{1+t^2}=\operatorname{sech}\delta.
\]

Under reversal `t -> 1/t`,

\[
\chi\mapsto-\chi,
\qquad
M\mapsto M.
\]

Thus `chi` carries arrow orientation, while `|chi|`, `cosh(delta)`, and `sech(delta)` are
orientation-even. G267's two infinite-depth ends are the two orientations of the reciprocal
relation space. They do not, without a separately supplied profile embedding, prove that one end
is micro and the other cosmological.

By contrast, G201's two signed extremes are explicitly extremes of the pointwise profile and its
jets. They can represent two geometric regimes of one supplied metric history. G202--G204 show a
quiet crossing, a negative inner trough, and a positive outer branch are mathematically available;
they do not select that history. Smooth-center regularity also returns `phi` to zero at the exact
center, so a regular negative inner sector is generally a finite trough rather than a monotone
`phi -> -infinity` center.

## 6. Consequence for mass and history

A future mass-emergence law may distinguish a negative **profile** sector because profile
conjugation generally changes the metric. Such a law must be covariant and compatible with pair
reversal; it cannot be triggered by negative directed depth alone.

The sign correction does not close G286. It preserves a possible macro--micro coupling that could
participate in a later complete propagation law, but no such feedback or admissibility condition is
derived here.

## Landing

```text
PROFILE_REGIME_SIGN_AND_PAIR_ARROW_ORIENTATION_ARE_ALREADY_TYPE_DISTINCT
__NO_NATIVE_KERNEL_REGRESSION
__RECENT_EXPLANATION_CONFLATED_THEM
```
