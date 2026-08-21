# G206 audit report — conformal time-live/nonspherical robustness of G205

Date: 2026-08-21

## Bounded landing

```text
CONFORMAL_COMMON_SCALE_PRESERVES_G205_CAUSAL_ORDER_AND_GLOBAL_HYPERBOLICITY
__NULL_COMPLETENESS_IFF_THE_CONFORMAL_AFFINE_WEIGHT_DIVERGES
__BOUNDED_LIVE_NONSPHERICAL_SCALES_SURVIVE_WHILE_SMOOTH_DECAYING_SCALE_CAN_DESTROY_NULL_COMPLETENESS
__COMPLETED_PAIR_PHI_SHIFTS_BY_MINUS_OMEGA_PULLBACK
__NO_PHYSICAL_OMEGA_HISTORY_OR_XMAX_SELECTION
```

Grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__ANALYTIC_GLOBAL_THEOREMS__INDEPENDENT_ALGEBRAIC_CORE`.

This is a `DERIVED_CONDITIONAL` classification of a supplied extension class, not a selected UDT
history.

## Result

For any exact G205 base metric `g0` and any smooth finite real function `Omega` on the same
manifold,

\[
\widetilde g=e^{2\Omega}g_0
\]

has exactly the same causal curves as `g0`. The G205 `t=constant` Cauchy surfaces therefore remain
Cauchy, so every member is globally hyperbolic.

If `lambda` is a G205 affine parameter on an inextendible null geodesic, then a conformal affine
parameter satisfies

\[
\frac{d\widetilde\lambda}{d\lambda}=e^{2\Omega(\gamma(\lambda))}.
\]

Consequently the conformal metric is null complete exactly when this positive weight has divergent
integral at both ends of every G205 null geodesic. Global hyperbolicity alone does not guarantee
that condition.

The bounded genuinely time-live and nonspherical witness

\[
\Omega_B=\epsilon\sin t\,\frac{3z^2-r^2}{1+r^2}
\]

is bounded below and preserves null completeness. The equally smooth positive conformal metric
with

\[
\Omega_F=-r^2+\Omega_B
\]

is still globally hyperbolic but is null incomplete: an outgoing G205 radial null ray reaches
`r=infinity` in finite conformal affine parameter.

## Completed pair response

On every supplied complete pair pullback, with `omega=Omega after F`,

\[
\widetilde h=e^{2\omega}h,\quad
\widetilde T=e^\omega T,\quad
\widetilde L_\sigma=e^\omega L_\sigma,\quad
\widetilde m=e^{2\omega}m,\quad
\widetilde\beta=\beta.
\]

The arbitrary-calibration control is conformally invariant. Completed-pair Dual Reciprocity is
not: its scalar changes internally with the complete metric,

\[
\widetilde\Phi=\Phi-\omega.
\]

This confirms that common scale is one of the instruments entering before terminal readout. It
does not make arbitrary `Omega` physical.

## Evidence

- 27 production symbolic assertions passed.
- A separate direct radial-coordinate geodesic derivation plus 10,000 distinct exact-rational
  cases passed 160,006 assertions without importing production code or artifacts.
- 160-digit boundary controls resolve the Gaussian tail through affine cutoff 8.
- 19 hostile mutations are rejected.
- Seven frozen source hashes pass the separate repository-context provenance gate.
- A fresh external reviewer returned `VERIFIED_WITH_CAVEATS`, found no mathematical error, and
  retained the full bounded landing. The two wording repairs were to state explicitly that the
  completed scalar shifts by `omega=Omega composed F` and to remove an unsupported novelty
  adjective.

The first 80-digit boundary run failed closed because quadrature rounded the cutoff-8 partial
Gaussian integral to the full integral. The diagnostic alone was repaired to evaluate the
positive tail directly at 160 working digits. No formula, witness, theorem, or parameter changed.

## Gates and open scope

The algebraic core is mechanized. Conformal transfer of the Cauchy property and the universal
all-null integral criterion are analytic theorems, not finite-census claims. External review
accepted those analytic arguments while retaining that evidence distinction.

G206 does not classify timelike or spacelike completeness of the conformal family, turn on
trace-free screen or mixing modes, select `Omega`, derive an action/source/transfer law, fit data,
or identify any limit with `X_max`.
