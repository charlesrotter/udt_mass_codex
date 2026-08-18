# G158 audit report — complete-coframe semidirect score

Date: 2026-08-18

## Primary landing

`GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED__TEN_CHANNEL_REGULAR_GROUP_CLOSES__BASE_AND_SCREEN_BPLUS2_CHANNELS_ACT_ON_FOUR_MIXING_COMPONENTS__Y_Z_ARE_QUERY_REPRESENTATION_DATA_NOT_GROUP_COORDINATES__CHANGING_BALANCE_ALLOWED__PHYSICAL_CARRY_HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN`

## What was found

The gauge-fixed regular complete coframe is not a pile of ten unrelated gears. It is an exact
$3+3+4$ semidirect machine:

\[
E(B,Q,S)=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\]

with three base channels, three screen channels, and four mixing channels. For chronological
composition,

\[
B_{21}=B_2B_1,
\quad Q_{21}=Q_2Q_1,
\quad S_{21}=S_1+Q_1^{-1}S_2B_1.
\]

The screen and base blocks therefore act directly on how mixing accumulates. Exact composition does
not require fixed channel ratios.

## The simple time-live joint

For a supplied smooth coframe history,

\[
\Omega_R=\dot E E^{-1}
=\begin{pmatrix}
\dot B B^{-1}&0\\
Q\dot S B^{-1}&\dot Q Q^{-1}
\end{pmatrix}.
\]

This ten-component logarithmic velocity is the clean mathematical candidate for the changing score
in the chosen gauge. For the supplied pair realization $V=EJ$,

\[
\dot V=\Omega_RV+E\dot J.
\]

Metric/coframe change and query/immersion change are therefore separated exactly. Neither is set to
zero, and neither is added after terminal `phi_pair`.

## What this regrades

- All ten gauge-fixed coframe channels in the registered oriented regular
  $B^+(2)\times B^+(2)\times\operatorname{Mat}(2)$ chart can change relative strengths while
  remaining one coherent machine.
- A constant generator or one scalar melody is a special ansatz, not a consequence of composition.
- `Y,Z` remain query representation data. They affect the heard pair response but are not additional
  ambient group coordinates.
- Determinant/volume characters see only base and screen scale. They miss all four mixing notes.
- G155's history-law gap remains: the algebra evaluates the score of a supplied history but does not
  determine which $E(\lambda),J(\lambda)$ is physically realized.
- G142--G144's physical cross-query carry gap also remains.

## Evidence

- preregistration commit `d40acb4a` predates outcome execution;
- 10 exact frozen sources;
- 12 exact symbolic checks across the full regular gauge-fixed group;
- 500 independent exact-rational group/action/differential trials;
- 200 independently coded fixed-generator trials;
- 5 algebraic mutation catches and 5 metadata guard mutations; the metadata guards enforce declared
  result flags but are not independent semantic proofs;
- fresh adversarial review required six repairs; repair-only follow-up passed;
- 145-row premise, package, and repository gates passed (`118 passed, 1 xfailed`).

## Maximum conclusion

The supplied gauge-fixed complete coframe has an exact ten-channel semidirect composition and an
exact time-live logarithmic score. This is a major kinematic simplification. It is not yet a physical
cross-query functor, gauge-independent observable score, history equation, regime profile,
observation, $X_{\max}$ determination, action, source, bootstrap, matter, or completion. No
canonization is requested or performed.
