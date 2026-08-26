# G269 audit report — metric-owned null-transport mutual clock

Date: 2026-08-26

## Primary landing

```text
METRIC_OWNS_A_QUERY_RELATIVE_NULL_TRANSPORT_MUTUAL_CLOCK_SCALAR
__M_PT_IS_BOUNDED_ABOVE_BY_SECH_DELTA
__EQUALITY_IFF_THE_TARGET_CLOCK_IS_IN_THE_TRANSPORTED_NULL_PAIR_PLANE
__NONZERO_SCREEN_MISMATCH_MAKES_THE_INEQUALITY_STRICT
__NO_QUERY_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

## Result

G269 finds the independent metric construction that G268 required. On one supplied regular affine
null relation, transport `A`'s metric-unit clock to `B` and define

\[
M_{\rm PT}=\frac1{-g(P_{AB}U_A,U_B)}.
\]

This construction does not use `delta`. The directional null-frequency ratio independently gives
`r=exp(-delta)`. Their exact relation is

\[
\boxed{
\frac1{M_{\rm PT}}
=\cosh\delta+\frac r2\lVert W\rVert^2,
}
\]

where `W` is the target clock's component perpendicular to the transported clock/null plane.
Consequently

\[
0<M_{\rm PT}\le\operatorname{sech}\delta,
\]

with equality exactly when `W=0`.

The primary static-radial and moving-flat controls are planar, so the provisional sech formula is
derived there. A flat transverse family preserves `r` while changing `M_PT`; at `r=2,w=1`, sech is
`4/5` but the transport mutual value is `4/9`. This proves that G269 has not merely renamed the old
depth.

## Qualification

The bilocal scalar is metric-owned after a null path and endpoint clocks are supplied. Its
interpretation as Nature's physical mutual-clock readout remains working rather than canonized.
The theorem does not populate null queries or select a history, distance law, `X_max`, source,
matter model, observation, or signalling mechanism. `W` is a transported clock-screen mismatch,
not a Jacobi sky-area distortion.

Current grade: `FRESH_EXTERNAL_REVIEW_ACCEPTED_NO_REPAIRS__VERIFIED_WITH_CAVEATS`.
