# G271 audit report — primary-metric null screen first-jet interlock

Date: 2026-08-26

## Primary landing

```text
NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT
__ONE_PRIMARY_METRIC_GRADIENT_GENERATES_DEPTH_AND_TRANSPORTED_SCREEN_CHANNELS
__RADIAL_AND_QUIET_STRATA_EXACT
__NO_FINITE_PATH_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

## Result

On every arbitrary smooth regular primary static reciprocal metric, the static-clock acceleration is

\[
a_{\hat r}=-e^{-\phi}\phi'.
\]

For a supplied affine null germ meeting the radial direction at angle `alpha`, the affine-normalized
first jets are

\[
\boxed{
\frac{\dot\delta}{\omega}=e^{-\phi}\phi'\cos\alpha,
\qquad
\frac{\dot W_s}{\omega}=e^{-\phi}\phi'\sin\alpha.
}
\]

Hence

\[
\boxed{
(\dot\delta/\omega)^2+(\dot W_s/\omega)^2=e^{-2\phi}(\phi')^2.
}
\]

This is a metric-native interlock: direct reciprocal redshift and the G269 transported-screen
mismatch are longitudinal and transverse projections of one primary-metric gradient. `W` is not an
added fitted orchestra coefficient on this family.

The exact finite-path evaluator is

\[
W_I(B)=\int_A^B\omega\,g(a,E_I)\,d\lambda,
\]

where `E_I` is the source screen parallel transported along the supplied branch. A radial branch has
`W=0` exactly; a quiet first jet makes both channels vanish; a nonradial nonquiet germ generates
`W` immediately.

The resulting leading mutual-clock gap is

\[
\operatorname{sech}\delta-M_{\rm PT}
=\tfrac12\dot W_s(A)^2\lambda^2+O(\lambda^3).
\]

## Scope

The theorem is arbitrary-profile but local in its closed angular split. Its integral evaluator is
exact but still requires a supplied profile and null branch. It does not derive a finite path,
physical history, branch population, distance, `X_max`, observation, dynamics, source, matter,
action, transfer, or canon.

## Evidence

- 30/30 direct symbolic checks;
- independent generic-static calculation;
- 20,000/20,000 exact rational cases;
- 6/6 implementation mutations caught;
- 6/6 typed overreach catches;
- no GPU, fit, linearized metric, or chosen profile.

Current grade: `INTERNALLY_VERIFIED_LEAD__EXTERNAL_REVIEW_OPEN`.
