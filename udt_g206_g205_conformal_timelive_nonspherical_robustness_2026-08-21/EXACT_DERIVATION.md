# G206 exact derivation — conformal time-live/nonspherical robustness

Date: 2026-08-21

## Landing

```text
CONFORMAL_COMMON_SCALE_PRESERVES_G205_CAUSAL_ORDER_AND_GLOBAL_HYPERBOLICITY
__NULL_COMPLETENESS_IFF_THE_CONFORMAL_AFFINE_WEIGHT_DIVERGES
__BOUNDED_LIVE_NONSPHERICAL_SCALES_SURVIVE_WHILE_SMOOTH_DECAYING_SCALE_CAN_DESTROY_NULL_COMPLETENESS
__COMPLETED_PAIR_PHI_SHIFTS_BY_MINUS_OMEGA_PULLBACK
__NO_PHYSICAL_OMEGA_HISTORY_OR_XMAX_SELECTION
```

## 1. Supplied extension class

Let `g0` be any exact G205 member on its declared `R_t x R3` realization and let

\[
\widetilde g=e^{2\Omega}g_0,
\qquad \Omega\in C^\infty(M,\mathbb R).
\]

The factor is strictly positive at every manifold point, so `g_tilde` is a smooth Lorentz metric.
This turns on one complete-metric channel: a common scale that may depend on time and angle. It does
not turn on trace-free screen shape or base-to-screen mixing, and it does not select `Omega` as a
physical history.

## 2. Causal structure survives exactly

For every tangent vector `v`,

\[
\widetilde g(v,v)=e^{2\Omega}g_0(v,v).
\]

The sign is unchanged, so the two metrics have exactly the same timelike, null, causal, and
future-directed curves. G205 proved that every `t=constant` slice is Cauchy for `g0`. Since the
inextendible causal curves are the same unparametrized curves, those slices are also Cauchy for
`g_tilde`. Therefore every member of the registered conformal class is globally hyperbolic.

This does not imply affine geodesic completeness, which is not conformally invariant.

## 3. Exact null affine transformation

Write `Omega_a=partial_a Omega`. The Levi-Civita connections obey

\[
\widetilde\Gamma^a{}_{bc}-\Gamma^a{}_{bc}
=\delta^a_b\Omega_c+\delta^a_c\Omega_b-g_{bc}\Omega^a.
\]

If `k` is an affinely parametrized `g0`-null tangent, then

\[
k^b\widetilde\nabla_bk^a=2k(\Omega)k^a.
\]

Consequently

\[
\widetilde k=e^{-2\Omega}k
\]

is affine for `g_tilde`. If `lambda` and `lambda_tilde` are the corresponding affine parameters,

\[
\boxed{
\frac{d\widetilde\lambda}{d\lambda}=e^{2\Omega(\gamma(\lambda))}.
}
\]

Every unparametrized `g_tilde` null geodesic is a `g0` null geodesic and conversely. Since G205 is
null complete, the exact criterion is

\[
\boxed{
\widetilde g\text{ is null complete}
\iff
\int e^{2\Omega(\gamma(\lambda))}\,d\lambda
\text{ diverges at both ends of every inextendible }g_0\text{-null geodesic}.
}
\]

A global lower bound `Omega>=C` is sufficient because the transformed affine integral is at least
`exp(2C)` times an infinite base affine interval.

## 4. A genuine time-live/nonspherical survivor

In smooth Cartesian coordinates let `r^2=x^2+y^2+z^2` and define

\[
\Omega_B
=\varepsilon\sin t\,
\frac{3z^2-r^2}{1+r^2},
\qquad \varepsilon\ne0.
\]

This is smooth at the center, time dependent, and nonspherical. Since

\[
-1<\frac{3z^2-r^2}{1+r^2}<2,
\]

one has `Omega_B>=-2|epsilon|`. The sufficient criterion therefore proves that every G205 null
geodesic remains complete. Global hyperbolicity already follows from Section 2.

The witness proves coexistence only. Its angular axis and amplitude are not selected physics.

## 5. A smooth time-live/nonspherical counterexample

Now define

\[
\Omega_F=-r^2+\Omega_B.
\]

It is also smooth and its conformal factor is positive at every finite point. G205 radial null
geodesics obey `r(lambda)=r_s+E lambda` with `E>0`. Along any outgoing one,

\[
e^{2\Omega_F}
\le e^{4|\varepsilon|}e^{-2(r_s+E\lambda)^2}.
\]

Hence

\[
\int_0^\infty e^{2\Omega_F}\,d\lambda
\le
e^{4|\varepsilon|}
\frac{\sqrt\pi}{2\sqrt2E}
\operatorname{erfc}(\sqrt2r_s)
<\infty.
\]

The same unparametrized null ray reaches the outer end at finite `g_tilde` affine parameter, so this
metric is null incomplete. It remains globally hyperbolic because its causal curve set is unchanged.

Thus G205 global hyperbolicity is robust across the entire registered conformal class, while G205
null completeness is not. The conformal affine integral, not causal ordering alone, separates the
two classes.

## 6. The completed pair hears the common scale

For any supplied regular pair immersion `F`, put `omega=Omega composed F`. Then

\[
\widetilde h=F^*\widetilde g=e^{2\omega}h.
\]

For the auxiliary pair decomposition,

\[
\widetilde T=e^\omega T,
\qquad
\widetilde L_\sigma=e^\omega L_\sigma,
\qquad
\widetilde\beta=\beta.
\]

The arbitrary-calibration control

\[
\phi_{\rm control}=\frac14\log\frac{-\det h}{h_{00}^2}
\]

is conformally invariant. But completed-pair Dual Reciprocity acts after the pullback and gives

\[
\widetilde m
=\widetilde T\widetilde L_\sigma
=e^{2\omega}m,
\]

\[
\boxed{
\widetilde\Phi=-\log\widetilde T=\Phi-\omega.
}
\]

So the common-scale instrument is not bolted on after readout: it changes the full pair metric,
physical ruler calibration, and completed scalar internally. This is an exact evaluator statement,
not a law selecting `Omega`.

## Evidence precision and maximum conclusion

The connection, affine-power, radial-null, pair-scaling, and finite-witness algebra are mechanized.
The global Cauchy transfer and necessary-and-sufficient all-null integral criterion are analytic
theorems. Finite numerical controls do not prove their universal quantifiers.

G206 proves a bounded time-live/nonspherical common-scale robustness classification. It does
not classify timelike or spacelike completeness of the conformal family, activate trace-free
screen/mixing channels, select a physical history, derive dynamics or transfer, or identify any
limit with `X_max`.
