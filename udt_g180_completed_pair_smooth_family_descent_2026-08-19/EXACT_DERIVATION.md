# G180 exact derivation — completed-pair smooth-family descent

Date: 2026-08-19

## 1. Domain and premise boundary

Let `I` be a connected interval and let a supplied smooth regular pair family have auxiliary pair
metric

\[
h_\sigma(\sigma)=
\begin{pmatrix}
h_{00}&h_{01}\\
h_{01}&h_{11}
\end{pmatrix},
\qquad h_{00}<0,\quad \det h_\sigma<0.
\]

The metric and pair family are supplied. The only nonidentity physical premise is the provisional
`WORKING_FOUNDATIONAL_CLARIFICATION`: completed-pair Dual Reciprocity is applied after the full
metric pullback. G180 does not select observers, events, germs, families, or a global completion.

## 2. The pointwise density glues on every regular interval

G176--G179 give the unique positive completed ruler density

\[
\boxed{m(\sigma)=\sqrt{-\det h_\sigma(\sigma)}}.
\]

Because the determinant is smooth and strictly negative, `m` is smooth and strictly positive.
Choose only a ruler origin `s_0` and orientation and define

\[
\boxed{
s(\sigma)=s_0+\int_{\sigma_0}^{\sigma}m(u)\,du.
}
\]

Then

\[
\frac{ds}{d\sigma}=m>0.
\]

Hence `s` is a smooth strictly monotone coordinate on `I` and a diffeomorphism from `I` onto its
image. The additive origin does not enter local metric coefficients or endpoint differences. This
is ordinary one-dimensional integration of the already derived density, not a new carry law.

Write the auxiliary metric uniquely as

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2.
\]

Under `ds=m d\sigma`,

\[
h_s=-T^2\left(dy^0+\frac{\beta}{m}ds\right)^2
+\frac{L_\sigma^2}{m^2}ds^2.
\]

Since `m=T L_\sigma`,

\[
\boxed{
T_s=T,\qquad L_s=T^{-1},\qquad
\beta_s=\frac{\beta}{m},\qquad
\det h_s=-1.
}
\]

The completed depth is therefore

\[
\boxed{
\Phi=-\log T=-\frac12\log(-h_{00}).
}
\]

No extra family scalar survives after the full pair metric and completed normalization are used.
The shift is retained.

## 3. Reparameterization and orientation

For a smooth orientation-preserving auxiliary reparameterization
`\sigma=f(\widetilde\sigma)` with `k=f'>0`,

\[
h_{01}\mapsto k h_{01},\qquad
h_{11}\mapsto k^2h_{11},\qquad
m\mapsto k m.
\]

Thus `m d\sigma`, `h_s`, and `\Phi` are unchanged. For `k<0`, the positive density transforms by
`|k|` while the oriented ruler one-form changes sign. This is auxiliary spatial orientation, not
observer-pair reversal. Same-pair reversal remains the endpoint theorem of G170--G171.

## 4. The completed kernel retains common metric scale

For a positive smooth common rescaling on the pair family,

\[
\widehat h_\sigma=e^{2\omega}h_\sigma,
\]

the completed quantities obey

\[
\boxed{
\widehat m=e^{2\omega}m,
\qquad
\widehat\Phi=\Phi-\omega,
\qquad
\det\widehat h_s=-1.
}
\]

Thus the completed kernel is not blind to the metric common scale. The conformal cancellation in
the older arbitrary-coordinate readout

\[
\phi_{\rm control}=\frac14\log\frac{-\det h}{h_{00}^2}
\]

belongs to that control query. It is not a freedom left inside the completed reciprocal pair. This
does not select a common-scale profile; it says that any common scale present in the supplied
metric is heard by the completed tape and depth.

## 5. Primary static-spherical family

Use dimension-matched time in the declared primary metric,

\[
g=-e^{-2\phi(r)}(dx^0)^2+e^{2\phi(r)}dr^2+r^2\gamma_{S^2}.
\]

For a supplied time-orthogonal family

\[
F(x^0,\sigma)=\bigl(x^0,r(\sigma),\gamma(\sigma)\bigr),
\]

define

\[
v=\frac{dr}{d\sigma},
\qquad
b^2=\gamma_{S^2}(\dot\gamma,\dot\gamma).
\]

The full pullback is

\[
h_\sigma=
\operatorname{diag}\!\left(
-e^{-2\phi},
e^{2\phi}v^2+r^2b^2
\right).
\]

Set

\[
H=e^{2\phi}v^2+r^2b^2.
\]

The completed density is

\[
\boxed{
m^2=e^{-2\phi}H
=v^2+e^{-2\phi}r^2b^2.
}
\]

Whenever the complete spatial tangent is nonzero, `H>0`, so `m>0`. In the completed ruler
coordinate,

\[
\boxed{
h_s=operatorname{diag}(-e^{-2\phi},e^{2\phi}),
\qquad
\Phi=\phi.
}
\]

The angular sector has not been deleted. It has fixed how much completed ruler coordinate is
accumulated along the family:

\[
\boxed{
\frac{ds}{d\sigma}
=\sqrt{v^2+e^{-2\phi}r^2b^2}.
}
\]

Consequently, the physically completed history is

\[
r=r(s),
\qquad
\boxed{\Phi(s)=\phi(r(s))}.
\]

Angular motion changes `r(s)` and therefore changes the reciprocal response as a function of
completed separation, without an additive angular correction to `\Phi`.

## 6. Exact strata and witnesses

### Radial recovery

For `b^2=0`,

\[
m=|v|.
\]

With `\sigma=r`, the completed tape is `s=r+constant` and `\Phi=\phi`.

### Angular radial turn

At `v=0`, `b^2>0`, and `r>0`,

\[
m=e^{-\phi}r\sqrt{b^2}>0.
\]

The ruler remains regular even though areal radius turns. In the exact registered example
`e^{-2\phi}=1/4`, `r=3`, `b^2=4/9`, one gets

\[
h_\sigma=\operatorname{diag}(-1/4,4),
\qquad m^2=1,
\qquad h_s=\operatorname{diag}(-1/4,4).
\]

### Pure-angular segment

If `r` is constant and `b^2>0`, the tape accumulates positive length while `\Phi=\phi(r)` is
constant. This is not a failure: the screen/ruler sector can change separation without changing
clock-side reciprocal depth on that special germ.

### Full primary witness

For `e^{-2\phi}=1/4`, `r=3`, `v=2`, and `b^2=25/36`,

\[
h_\sigma=\operatorname{diag}(-1/4,89/4),
\qquad m^2=89/16,
\qquad h_s=\operatorname{diag}(-1/4,4).
\]

### Nonzero-shift generic witness

For `T=3/2`, `L_\sigma=5/3`, and `\beta=-2/5`,

\[
h_\sigma=
\begin{pmatrix}
-9/4&9/10\\
9/10&544/225
\end{pmatrix},
\qquad m^2=25/4.
\]

After calibration, `\det h_s=-1` and the cross-term remains `9/25`.

### Center control

For the monotone chart `\sigma=r`, finite `\phi` and bounded `b^2` give

\[
m^2=1+e^{-2\phi}r^2b^2\longrightarrow1
\quad\text{as}\quad r\to0^+.
\]

This is a spherical-chart limit, not a global smooth-center theorem.

The excluded zero-tangent case `v=b=0` has `m=0` and is outside the regular rank-two pair stratum.

## 7. Exact derivatives and endpoint response

Along the supplied family,

\[
\frac{d\Phi}{d\sigma}
=-\frac12\frac{\dot h_{00}}{h_{00}}.
\]

Where `s` is used as coordinate,

\[
\boxed{
\frac{d\Phi}{ds}
=\frac{1}{m}\frac{d\Phi}{d\sigma}.
}
\]

For the primary family,

\[
\frac{d\Phi}{ds}
=\frac{\phi'(r)v}
{\sqrt{v^2+e^{-2\phi}r^2b^2}}.
\]

This is the exact place where the angular orchestra modulates reciprocal response with completed
separation. These are kinematic chain rules, not an equation of motion or history selector.

For endpoints on the same completed family,

\[
\delta(\sigma_1,\sigma_2)=\Phi(\sigma_2)-\Phi(\sigma_1).
\]

Reversal and telescoping follow exactly. No closure is imposed between independently supplied pair
families.

## 8. Regrading G172 without erasing it

G172's

\[
\phi_{\rm control}=\phi+\frac14\log\!\left(1+r^2e^{-2\phi}a^2\right)
\]

is correct for the auxiliary areal-radius calibration used there. Under the later G176 working
clarification it is a control readout, not the completed physical reciprocal scalar. The same
factor becomes the completed ruler density

\[
m^2=1+r^2e^{-2\phi}a^2,
\]

while `\Phi=\phi`. Thus G180 changes the interpretation, not G172's algebra.

## 9. Evidence and landing

- preregistration commit: `ae24ebbc`;
- nine frozen source hashes: exact;
- production symbolic checks: 29/29 pass;
- independent stdlib exact-rational replay: 20,000 families and 341,579 assertions;
- independent turning controls: 1,461; pure-angular controls: 1,461; radial controls: 118.

Primary landing:

```text
COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP
```

Grade before fresh review:
`DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS_PENDING_FRESH_ADVERSARIAL_REVIEW`.

Maximum conclusion: the accepted pointwise completed-pair kernel glues on every supplied connected
smooth regular interval, and in the primary time-orthogonal family the angular orchestra changes
the completed separation map rather than adding a scalar depth term. Physical family realization,
cross-family matching, singular/global completion, non-scalar transport, `X_max`, observations,
dynamics, sources, matter, and signalling remain open or outside scope.
