# G172 exact derivation — smooth primary-metric pair families

Date: 2026-08-19

## Landing

`SMOOTH_FAMILY_CLOSURE`

For every supplied smooth time-independent angular curve on a connected interval inside the
regular primary static-spherical metric domain, with nonzero radial component calibrated by areal
radius, the complete metric pullback gives a smooth regular reciprocal scalar response. Reversal
and telescoping are exact within that one family. No angular profile, coefficient, `X_max`, or
scaffolded carry rule is required.

This is a bounded family theorem. It does not select one physical angular curve, prove a global
completion, or close non-scalar transport.

## 1. Declared primary metric and family

Use dimension-matched static time (x^0=c_Et):

\[
g=-e^{-2\phi(r)}(dx^0)^2+e^{2\phi(r)}dr^2+r^2\gamma_{S^2}.
\]

The registered family is

\[
F(x^0,r)=(x^0,r,\gamma(r)),
\]

where \(\gamma:I\to S^2\) is arbitrary and smooth on a connected interval \(I\) with \(r>0\).
No angular melody is chosen. Its complete invariant contribution is the nonnegative scalar

\[
a^2(r)=\gamma_{S^2}(\gamma'(r),\gamma'(r)).
\]

In standard sphere coordinates,

\[
a^2=(\theta')^2+\sin^2\theta\,(\psi')^2.
\]

## 2. Complete pullback before reciprocal readout

The tangent vectors are

\[
F_*\partial_{x^0}=\partial_{x^0},\qquad
F_*\partial_r=\partial_r+\gamma'(r).
\]

Therefore

\[
h=F^*g=
\begin{pmatrix}
-e^{-2\phi} & 0\\
0 & e^{2\phi}+r^2a^2
\end{pmatrix}.
\]

Define

\[
W(r)=1+r^2e^{-2\phi(r)}a^2(r)>0.
\]

Then

\[
\det h=-W<0.
\]

Thus every member of the registered smooth finite family is Lorentzian and nondegenerate at every
interior point of the supplied metric interval. The angular Gram contribution is already inside
the pair metric; it is not bolted onto a radial answer afterward.

## 3. Exact reciprocal response

The terminal pair readout is

\[
\Phi(r)=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right)
=\phi(r)+\frac14\log W(r).
\]

The conditional inter-observer frame ratio is consequently

\[
\frac{c_{\mathrm{eff}}^{(\mathrm{pair})}}{c_E}
=e^{-2\Phi}
=\frac{e^{-2\phi}}{\sqrt{W}}.
\]

This is a frame readout, not a derived local signal speed. Since \(W\ge1\), the angular sector
modulates the same reciprocal response without a fitted amplitude. The radial family is recovered
exactly when \(a^2=0\):

\[
\Phi=\phi,
\qquad
\frac{c_{\mathrm{eff}}^{(\mathrm{pair})}}{c_E}=e^{-2\phi}.
\]

No sign or monotonicity claim for the derivative follows merely from \(W\ge1\), because the
angular speed itself is allowed to vary.

## 4. Smooth evolution along one family

For smooth \(\phi\) and \(a^2\),

\[
W'=e^{-2\phi}
\left(2ra^2+r^2(a^2)'-2r^2\phi'a^2\right),
\]

and

\[
\Phi'=\phi'+\frac{W'}{4W}.
\]

For endpoints \(r_1,r_2\) on this same calibrated family, define

\[
\delta(r_1,r_2)=\Phi(r_2)-\Phi(r_1).
\]

Then same-family reversal and telescoping are identities:

\[
\delta(r_2,r_1)=-\delta(r_1,r_2),
\]

\[
\delta(r_1,r_2)+\delta(r_2,r_3)=\delta(r_1,r_3).
\]

This scalar telescoping statement is not complete non-scalar transport closure. It does not erase
screen rotation, mixing, or path-labelled holonomy when those channels are queried.

## 5. Integrability is explicit, not postulated

The map \(F\) itself is a smooth immersion on the registered domain, so it directly constructs the
pair surface. There is also an independent Frobenius check. Let

\[
K=\partial_{x^0},\qquad S=\partial_r+\gamma'(r).
\]

Because the primary metric and the supplied curve are time independent,

\[
[K,S]=0.
\]

Hence \(\operatorname{span}(K,S)\) is involutive and integrates into the displayed family. This
uses neither co-presence nor an observer ontology. It follows from the declared metric chart and
the supplied smooth family type.

On any connected interval lying inside the regular metric domain, finite smooth \(\phi\) and
finite smooth \(\gamma'\) suffice for extension throughout that interval. This is not a theorem of
global spacetime completion.

## 6. Why areal-radius calibration matters

For a general family parameter \(\sigma\), write

\[
v=\frac{dr}{d\sigma},
\qquad
b^2=\gamma_{S^2}\!\left(\frac{d\gamma}{d\sigma},\frac{d\gamma}{d\sigma}\right).
\]

Then

\[
h_{\sigma\sigma}=e^{2\phi}v^2+r^2b^2.
\]

Under a positive rescaling of the spatial pair tangent by \(\lambda\), the raw chart readout shifts
by \(\tfrac12\log\lambda\). It is not invariant under an independently rescaled pair coordinate.
When \(v\ne0\), the metric-owned areal radius supplies the calibration

\[
a^2=\frac{b^2}{v^2},
\]

and division by \(v^2\) recovers the registered formula. At a turning point \(v=0\), that
calibration fails. Pure-angular and turning families therefore require a different chart or
calibration and are outside this theorem; they are not negatives.

## 7. Center limit and first obstructions

If \(\phi\) is finite and \(a^2\) remains bounded as \(r\to0^+\), then

\[
W\to1,
\qquad
\Phi-\phi\to0.
\]

This is only a one-sided spherical-chart limit. It is not a smooth-center theorem.

The first exact boundaries of the result are:

1. loss of smoothness or finiteness of the supplied metric profile or angular curve;
2. loss of Lorentzian metric regularity in the ambient history;
3. loss of monotone areal calibration at \(dr/d\sigma=0\);
4. leaving the static time-orthogonal family class;
5. reaching an endpoint not contained in the supplied regular metric interval.

## 8. Ownership and maximum conclusion

- `DERIVED_BOUNDED`: the pullback, \(W\), \(\Phi\), conditional frame ratio, derivative,
  integrability, reversal, telescoping, radial recovery, and bounded center limit.
- `CHOSE_BOUNDED_CLASS`: static, time-orthogonal, monotone-areal pair families.
- `FREE_AND_CHARACTERIZED`: the complete smooth angular curve through \(a^2(r)\).
- `SUPPLIED`: the primary metric profile \(\phi(r)\) and its regular interval.
- `OPEN`: which family is physically realized, turning/pure-angular strata, time-live and
  nonspherical metrics, global completion, and non-scalar transport.
- `INACTIVE`: co-presence, `X_max`, G142--G160 carry/score machinery, fitting, matter, sources,
  actions, bootstrap, and observational selection.

The result establishes robustness of the metric-native reciprocal scalar kernel across the whole
registered smooth family. It does not turn the family parameter into a preferred path or a new
physical law.
