# G174 audit report — native calibrated pair-germ chart ownership

Date: 2026-08-19

## Primary landing

`CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS`

The apparent G173 scalar ambiguity was one level upstream from the kernel. In an arbitrary curve
parameter \(\sigma\), the positive density \(m\) is exactly the Jacobian to the calibrated ruler
coordinate, \(ds=m\,d\sigma\). Supplying the calibrated ruler vector fixes that Jacobian uniquely.
The terminal reciprocal scalar is then the unique readout of the one calibrated pair metric.

G173's `m_A` and `m_P` remain lawful candidate calibrations, but when they differ they define
different calibrated ruler vectors. They do not give two answers for the same complete pair germ.
No candidate is selected.

## What changed

- The tensor result did not change: angular motion keeps the pullback regular through a radial
  turn; only zero complete spatial tangent loses rank.
- The calibration atlas is retained for an unparameterized pair image or line.
- The scalar nonuniqueness is removed after the input is upgraded to the fully calibrated pair germ
  already required by the reciprocal-`c_E` terminal derivation.
- A constant ruler-unit rescaling shifts both endpoint densities equally and cancels from directed
  pair depth. A position-dependent recalibration changes the tape and may change the response.

## Evidence

- Preregistered and pushed at commit `784afa23` before outcome code.
- Frozen sources: 12/12 hashes verified at commit `9e40a840`.
- Exact symbolic/source derivation: 32/32 checks.
- Independent stdlib/Fraction replay: 156,000 checks over 12,000 samples.
- Exact radial-turn coverage: 2,000 cases.
- Pure-radial controls: 1,200 cases.
- General nonradial controls: 8,800 cases.
- Distinct-candidate controls: 9,958 cases.
- Mutation/semantic catches and repository gates are recorded separately.
- Fresh external adversarial review is still required before final banking.

## Maximum conclusion

G174 closes the local **readout type**: one supplied fully calibrated pair germ has one terminal
reciprocal scalar. It does not derive which germ/calibration is physically realized, how separate
pair tapes carry calibration, a path, a global network, time-live/nonspherical completion,
`X_max`, observations, action, source, matter, bootstrap, signalling, or canon.

Current grade: `LEAD__INTERNALLY_DERIVED_AND_INDEPENDENTLY_REPLAYED__AWAITING_EXTERNAL_REVIEW`.
