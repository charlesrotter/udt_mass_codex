# G159 preregistration — complete score to calibrated terminal first jet

Date: 2026-08-18

Status at registration: `PREREGISTERED__NO_G159_OUTCOME_EXECUTED`

## Whole question

For one supplied smooth regular calibrated pair family, join the G158 score

\[
V=EJ,
\qquad
\dot V=\Omega_RV+E\dot J
\]

to the complete pair metric $h=V^T\eta V$. Does the complete score descend exactly, with all
coframe and query channels live, to

\[
\dot h,
\quad \dot\kappa_{\rm pair},
\quad \dot\phi_{\rm pair},
\quad \dot\beta_{\rm pair},
\quad \partial_\lambda\log(c_{\rm eff}/c_E)?
\]

Which outputs are invariant under a live Lorentz coframe-gauge change, which are merely covariant
under a pair-chart change, and which require fixed or lawfully carried clock/ruler calibration?

## Bounded regime

- one smooth regular rank-two pair family with $h_{00}<0$ and $\det h<0$;
- the supplied G158 oriented regular gauge-fixed $E(B,Q,S)$ score;
- arbitrary supplied $\dot J$, with no frozen query sector;
- live left coframe changes $E'=\Lambda(\lambda)E$ with $\Lambda^T\eta\Lambda=\eta$;
- live pair-domain recharting $J'=JA(\lambda)$ with $A\in GL^+(2)$;
- exact first derivatives only.

The computation is metric-led and algebraic. Values of $E,J,\lambda$ remain supplied.

## Excluded

- physical history/query selection, regime amplitudes, fits, or loud--quiet--loud prediction;
- interpreting $\lambda$ as clock time, radial distance, affine parameter, or evolution without an
  independently supplied query;
- claiming score entries or ratios are gauge-independent observables;
- singular pair metrics, null degeneration, cut loci, topology, or global completion;
- observations, $X_{\max}$ value/profile, action, source, bootstrap, matter, mass, or signalling;
- protected packages and their contents.

## Candidate exact structure to test

Let $P=\Omega_RV+E\dot J$. Test

\[
\dot h=P^T\eta V+V^T\eta P,
\]

\[
\dot\kappa_{\rm pair}=\frac14\operatorname{tr}(h^{-1}\dot h),
\]

\[
\dot\phi_{\rm pair}
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}},
\]

\[
\dot\beta_{\rm pair}
=\frac{\dot h_{01}h_{00}-h_{01}\dot h_{00}}{h_{00}^2},
\qquad
\partial_\lambda\log(c_{\rm eff}/c_E)=-2\dot\phi_{\rm pair}.
\]

Test live Lorentz-gauge cancellation despite

\[
\Omega_R'=\dot\Lambda\Lambda^{-1}+\Lambda\Omega_R\Lambda^{-1},
\]

and derive the exact recalibration terms under $J'=JA(\lambda)$, including the positive diagonal
control $A=\operatorname{diag}(a,b)$.

## Preregistered outcome classes

Exactly one primary class will be returned:

1. `TERMINAL_FIRST_JET_TYPE_FAILURE`;
2. `SCORE_DESCENT_REQUIRES_FROZEN_QUERY`;
3. `TERMINAL_DERIVATIVES_NOT_CLOSED_FROM_H_DOTH`;
4. `CALIBRATED_PAIR_FIRST_JET_DERIVED__H_DOTH_LORENTZ_GAUGE_INVARIANT__TERMINAL_COMPONENTS_REQUIRE_CALIBRATION_CARRY`.

## Certification and falsification contract

The result must include:

1. exact symbolic descent from $E,J,\Omega_R,\dot J$ through $h,\dot h$;
2. all four terminal derivative formulas and the conditional `c_eff` derivative;
3. exact live Lorentz-gauge cancellation;
4. arbitrary-$GL^+(2)$ density/coefficient transformation and live diagonal recalibration control;
5. an explicit witness where $\dot J$ changes the terminal first jet;
6. independent implementation, mutation catches, and fresh adversarial review;
7. explicit retention of physical history, calibration carry, and global scope as open.

Any algebraic mismatch, frozen query dependence, or false gauge-invariance claim rejects outcome 4.

## Maximum conclusion

G159 may derive the calibrated terminal first jet of a supplied pair history and classify its
coframe-gauge and pair-chart behavior. It may not derive the history, query, calibration carry,
dynamics, or downstream physics.
