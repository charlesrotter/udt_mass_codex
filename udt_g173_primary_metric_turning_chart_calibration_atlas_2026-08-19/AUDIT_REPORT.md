# G173 audit report — primary-metric turning-chart calibration atlas

Date: 2026-08-19

## Primary landing

`PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE`

The declared primary metric gives a unique smooth pair tensor through a radial turn whenever the
angular tangent remains nonzero. The G172 areal-radius scalar does not extend as the same finite
calibration because its density `abs(dr/dsigma)` vanishes. A scalar chart can be restored by a
positive weight-one calibration density, but current premises do not select one uniquely.

Two metric-built witnesses,

\[
m_A^2=v^2+r^2b^2,
\qquad
m_P^2=v^2+e^{-2\phi}r^2b^2,
\]

both transform lawfully, remain positive at a genuine turn, and recover the G172 radial answer
when `b=0`. At `v=0,b>0`, however, they give `Phi_A=phi/2` and `Phi_P=phi`. This proves bounded
calibration nonuniqueness without choosing a physical ruler.

## What changed

G172's first boundary is now split exactly:

- `dr/dsigma=0`, `b>0`: coordinate/calibration failure only; the tensor stays Lorentzian;
- `dr/dsigma=0`, `b=0`: zero complete spatial tangent; the surface loses rank.

The old scalar and every finite non-areal scalar are joined by an exact calibration transition on
monotone overlaps. No finite positive calibration can be pointwise identical to G172 throughout a
punctured turning neighborhood and remain nonzero at the turn.

## Evidence

- Preregistered at commit `b015cd89` before outcome code.
- Frozen sources: 11/11 hashes verified at commit `d1f2e6f5`.
- Exact symbolic/source derivation: 32/32 checks.
- Independent stdlib/Fraction replay: 144,000 checks over 12,000 samples.
- Exact radial-turn coverage: 2,000 independent cases.
- Pure-radial controls: 1,200 independent cases.
- General nonradial controls: 8,800 independent cases.
- Mutation/semantic catches: 19/19.
- Repository premise gate: PASS on the 159-row exact registry.
- Repository regression suite: 129 passed, 1 expected xfail.
- Fresh external adversarial review: pending; no external-review grade is claimed.

## Maximum conclusion

G173 derives a bounded local calibration atlas for supplied smooth static, time-orthogonal,
non-areal pair families with `r>0`. It does not establish that physical UDT has multiple rulers,
select a calibration or pair family, prove a positive/global distance, cover time-live or
nonspherical metrics, close non-scalar transport, or derive `X_max`, observations, action, source,
matter, bootstrap, signalling, or canon.
