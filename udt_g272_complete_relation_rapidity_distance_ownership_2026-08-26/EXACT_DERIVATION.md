# G272 exact derivation — complete relation rapidity versus physical distance

Date: 2026-08-26

## Primary landing

```text
COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_TRANSPORTED_RAPIDITY_STATE
__PLANAR_TANH_DELTA_IS_EXACT_STRATUM
__SCREEN_STATE_PREVENTS_DELTA_ONLY_COMPLETENESS
__CONVENTIONAL_DISTANCE_SCALE_PROFILE_HISTORY_AND_XMAX_REMAIN_OPEN
```

This selects preregistered alternative
`B__COMPLETE_METRIC_DERIVES_QUERY_RELATIVE_RAPIDITY_STATE_ONLY`.

## 1. Complete supplied relation

For one supplied regular affine null relation, G269 gives

\[
r=e^{-\delta}>0,
\qquad
\Gamma_{\rm PT}
=\cosh\delta+\frac r2\lVert W\rVert^2,
\qquad
M_{\rm PT}=\Gamma_{\rm PT}^{-1}.
\]

Here `W` is the ambient transported endpoint-clock screen mismatch. It is not an appended angular
coefficient, a Jacobi area, or a holonomy scalar. G271 derives its local source from the same
primary-metric first jet as the direct depth channel.

The exact factorization

\[
\Gamma_{\rm PT}-1
=\frac{(r-1)^2+r^2\lVert W\rVert^2}{2r}
\ge0
\]

proves that `Gamma_PT>=1` on the whole finite regular supplied relation.

## 2. Metric-owned transported rapidity

The transported source clock and target clock are unit future timelike vectors at the same endpoint
after Levi-Civita transport. Their hyperbolic separation is therefore the natural nonnegative
rapidity magnitude

\[
\boxed{
\eta_{\rm PT}=\operatorname{arcosh}\Gamma_{\rm PT}\ge0.
}
\]

This gives the exact bounded magnitude

\[
\boxed{
\rho_{\rm PT}=\tanh\eta_{\rm PT}
=\sqrt{1-M_{\rm PT}^2},
}
\]

and hence

\[
\boxed{
M_{\rm PT}=\operatorname{sech}\eta_{\rm PT},
\qquad
M_{\rm PT}^2+\rho_{\rm PT}^2=1.
}
\]

Unlike the provisional G267 circle, this is not obtained by declaring a function of `delta` to be
the complete response. `Gamma_PT` is independently evaluated by the supplied metric, clocks,
branch, and transport. Calling `M_PT` a physical mutual-clock observable remains a
`WORKING_OPERATIONAL_READOUT`, but the scalar and its rapidity are ordinary exact metric data.

## 3. The full bounded state is a transported-frame vector

G269 decomposes the target clock as

\[
U_B=\Gamma_{\rm PT}\widetilde U_A+a\widetilde n_A+W,
\qquad
a=\Gamma_{\rm PT}-r^{-1}.
\]

Divide the spatial coefficients by `Gamma_PT`:

\[
v_\parallel=\frac a{\Gamma_{\rm PT}},
\qquad
v_\perp=\frac W{\Gamma_{\rm PT}}.
\]

Unit normalization gives

\[
\boxed{
v_\parallel^2+\lVert v_\perp\rVert^2
=1-\Gamma_{\rm PT}^{-2}
=\rho_{\rm PT}^2.
}
\]

These are coordinates of the endpoint clock on the transported unit-timelike hyperboloid. They are
not automatically a local signal velocity or an ordinary spatial displacement. The complete
bounded relation state is vector-valued; `rho_PT` is only its magnitude.

## 4. The exact planar and radial stratum

When `W=0`,

\[
\Gamma_{\rm PT}=\cosh\delta,
\qquad
\eta_{\rm PT}=|\delta|,
\]

\[
\boxed{
M_{\rm PT}=\operatorname{sech}\delta,
\qquad
\rho_{\rm PT}=|\tanh\delta|.
}
\]

The signed coordinate

\[
\chi=\tanh\delta
\]

retains the observer-order arrow that the nonnegative rapidity magnitude discards. On the primary
static radial branch,

\[
\delta_{AB}=\phi_B-\phi_A,
\]

so the exact one-dimensional relation-space profile is

\[
\boxed{
\chi_{AB}=\tanh(\phi_B-\phi_A).
}
\]

This is exact and coefficient-free. It is a profile in intrinsic reciprocal relation space, not yet
a profile in metres, areal radius, slice distance, optical distance, or radar distance.

## 5. Why signed depth alone is not the complete nonradial distance state

At fixed `delta`,

\[
\frac{\partial\Gamma_{\rm PT}}
{\partial\lVert W\rVert^2}
=\frac r2>0.
\]

Therefore two supplied relations with the same `delta` but different screen mismatch have different
`eta_PT`, `rho_PT`, and `M_PT`. In particular,

\[
\eta_{\rm PT}\ge|\delta|,
\qquad
\rho_{\rm PT}\ge|\tanh\delta|,
\]

with equality exactly when `W=0`. The G268 coordinate `chi=tanh(delta)` is the exact oriented
longitudinal stratum, but it does not encode the complete nonradial metric relation by itself.

## 6. Affine and reversal behavior

G269 proves that `r`, the transported plane, `W`, and `Gamma_PT` are invariant under common positive
affine rescaling of the null tangent. Thus `eta_PT` and `rho_PT` are affine-invariant.

For same-path reversal,

\[
r\mapsto r^{-1},
\qquad
\lVert W\rVert^2\mapsto r^2\lVert W\rVert^2.
\]

Substitution gives the same `Gamma_PT`. Therefore `eta_PT`, `rho_PT`, and `M_PT` are reversal-even,
while `delta` and the oriented longitudinal coordinate remain reversal-odd. A nonnegative magnitude
cannot replace the signed composition variable.

## 7. Local join to G271

For a short supplied primary-static null segment,

\[
\delta=d_1\lambda+O(\lambda^2),
\qquad
W=w_1\lambda+O(\lambda^2).
\]

Then

\[
\Gamma_{\rm PT}
=1+\frac12(d_1^2+w_1^2)\lambda^2+O(\lambda^3),
\]

\[
\rho_{\rm PT}^2
=(d_1^2+w_1^2)\lambda^2+O(\lambda^3).
\]

G271 supplies

\[
\frac{d_1}{\omega}=e^{-\phi}\phi'\cos\alpha,
\qquad
\frac{w_1}{\omega}=e^{-\phi}\phi'\sin\alpha,
\]

so the complete rapidity magnitude hears the full local primary-metric gradient independently of
incidence angle at leading norm order. The angle distributes one metric effect between longitudinal
and screen components; it does not add a new volume coefficient.

## 8. The strongest conditional physical-distance profile

Suppose a future foundational adoption identifies a signed normalized physical separation with the
planar relation coordinate,

\[
\boxed{\frac{x}{X}=\chi=\tanh\delta,}
\]

where `X>0` is a dimensional scale. This identification is a `CONDITIONAL_DISTANCE_ATTACHMENT`,
not a result silently inserted into the preceding derivation. It would imply

\[
\boxed{
\delta=\operatorname{artanh}\frac{x}{X}.
}
\]

On a positively oriented radial branch with reference `phi_A`,

\[
\boxed{
\phi(x)-\phi_A=\operatorname{artanh}\frac{x}{X},
}
\]

and therefore

\[
\boxed{
e^{-2(\phi(x)-\phi_A)}
=\frac{1-x/X}{1+x/X}.
}
\]

This is the exact profile suggested by the infinite-bare-`c` / mutual-distance framing **if** that
framing owns the displayed distance identification. The bounded endpoint `|x|/X->1` would then be a
consequence of the relation coordinate. The value and physical ownership of `X`, global branch
population, and nonradial vector attachment would still require proof or calibration.

## 9. Why `c_E` does not alone attach the missing length

The quantities `delta`, `W`, `Gamma_PT`, `eta_PT`, and `rho_PT` are dimensionless. The observed
calibration has type

\[
[c_E]=L/T.
\]

Multiplying a dimensionless relation state by `c_E` does not produce a length; one also needs a
time scale. Equivalently, a universal `X` requires a length anchor or a clock interval
`T_*` through `X=c_ET_*`. A query-supplied clock interval can make a query-relative length, but does
not by itself establish one universal physical `X`.

## 10. Exact ownership result

G272 closes a distinction that the phrase “supplied metric profile” obscured:

- `DERIVED_CONDITIONAL`: after a complete null relation is supplied, the metric owns the exact
  dimensionless rapidity state `(eta_PT,v_parallel,v_perp)` and bounded magnitude `rho_PT`;
- `EXACT_STRATUM`: on radial/transported-planar relations, the signed intrinsic profile is
  `chi=tanh(delta)=tanh(Delta phi)`;
- `CONDITIONAL_DISTANCE_ATTACHMENT`: identifying `x/X=chi` produces the exact
  `Delta phi=artanh(x/X)` profile;
- `OPEN`: whether the original mutual-distance postulate physically owns that identification; the
  scale `X`; conventional-distance embedding; nonradial vector attachment; branch population;
  complete history; and `X_max` realization.

Thus the current theory has more than an arbitrary response function: it already has an exact
relation-space profile. It has not yet proved that this relation coordinate is the physical
dimensionful distance used to write one unique global `phi(r)`.

## Evidence

- 20 exact symbolic checks;
- 24,000 implementation-independent complete-pair cases;
- 168,530 exact-fraction assertions;
- 23,995 nonplanar same-depth separators;
- 270 exact planar controls;
- 11,842 negative-depth controls.
