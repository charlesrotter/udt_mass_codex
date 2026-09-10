# NCI1 bounded same-premise precision repair

Date: 2026-09-10. Initial candidate SHA-256:
`a2769dd02500970475225939f0606ba212bdde6b6a54a3bebdd5023ced1385e1`.
This file plus `INITIAL_CANDIDATE.md` defines the repaired candidate. The initial bytes remain fixed.
One repair cycle; two wording/domain clarifications requested by the direct reviewer.

1. In section5's diagonal homogeneous family choose **smooth positive representatives A_i(t)>0**
   on the connected time interval. This is without loss within the nondegenerate metric written
   with A_i squared: any nonzero signed representative has constant sign on the interval and may
   be replaced by its positive absolute value. The conclusion `A_i=c_i A`, c_i>0, then has its
   precise intended domain. No physical metric, evolution law or initial-data freedom is removed.
2. In control3, replace “The directional clock-depth slope is -kappa n_x^2” by
   “The **normalized** directional clock-depth slope `(1/omega) d delta/d lambda` is
   `-kappa n_x^2` at x=0; the raw slope equals that value when the initial normalization is omega=1.”
   This agrees with equation(D) and avoids silently fixing affine frequency normalization.

No equation, proof, field hypothesis, source conclusion or physical premise is changed. Author code
already used positive `A_i=exp(q_i)` and initial omega=1 in this control. Its original output remains
evidence at that exact scope; no claim that wording review proves the checks is made.

Focused re-review must check both edits and their unchanged-metric/sign implications before the
repaired candidate is called reviewed. No further repair is authorized in this bounded work order.
