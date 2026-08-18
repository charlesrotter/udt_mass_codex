# G159 audit report — complete score to calibrated terminal first jet

Date: 2026-08-18

## Primary landing

`CALIBRATED_PAIR_FIRST_JET_DERIVED__COMPLETE_SCORE_DESCENDS_WITH_DOTJ_LIVE__H_AND_DOTH_LIVE_LORENTZ_COFRAME_GAUGE_INVARIANT__KAPPA_DENSITY_COEFFICIENT_AND_PHI_BETA_CEFF_REQUIRE_PAIR_CALIBRATION_CARRY__PHYSICAL_HISTORY_QUERY_LAMBDA_AND_GLOBAL_COMPLETION_OPEN`

## What was learned

The G158 complete score reaches the supplied calibrated pair coefficients through one exact object:

\[
\dot h
=2\operatorname{sym}\!\left[V^T\eta(\Omega_RV+E\dot J)\right].
\]

No coframe channel or query motion is appended after terminal readout. From $(h,\dot h)$ the
calibrated rates $\dot\kappa_{\rm pair}$, $\dot\phi_{\rm pair}$, $\dot\beta_{\rm pair}$, and
$\partial_\lambda\log(c_{\rm eff}/c_E)$ follow uniquely.

## The decisive invariance split

- A live Lorentz coframe-gauge change alters the component score inhomogeneously but cancels exactly
  from both $h$ and $\dot h$.
- A live pair-chart change acts covariantly on $(h,\dot h)$ but changes terminal coefficient values.
- `kappa_pair` is a log-density coefficient. `phi_pair`, `beta_pair`, and pair `c_eff/c_E` depend on
  the supplied clock/ruler calibration.
- An explicit fixed-coframe witness shows that $\dot J$ alone can change all three terminal rates.

This is the clean boundary between the machine and how it is read: the complete score produces a
Lorentz-coframe-gauge-independent pair first jet, while numerical terminal components require a calibrated query
or lawful carry.

## Evidence

- preregistration commit `250bbdf6` predates outcome execution;
- 7 exact frozen sources;
- 9 exact symbolic checks;
- 500 independent exact-Fraction and dual-number pair/rechart/live-Lorentz trials;
- 6 algebraic mutation catches plus 4 metadata guard mutations;
- fresh adversarial repair/follow-up PASS;
- 146-row premise/startup verifier PASS and repository suite 119 passed, 1 expected failure;
- package verifier records the final integrity gate separately.

## Maximum conclusion

The supplied complete coframe/query score descends exactly to a Lorentz-coframe-gauge-invariant pair
first jet and thence to calibrated terminal rates. This closes the local score-to-readout join. It
does not select the physical history or query, own $\lambda$, derive calibration carry, or establish
dynamics, observations, light propagation, $X_{\max}$, or global completion. No canonization is
requested or performed.
