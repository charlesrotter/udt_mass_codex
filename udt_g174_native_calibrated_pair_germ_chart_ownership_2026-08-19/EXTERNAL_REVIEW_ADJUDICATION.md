# G174 external-review adjudication

Date: 2026-08-19

## Verdict

`G174_ACCEPTED_WITH_STATED_BOUNDS`

The fresh external gpt-5.4 reviewer verified the exact sealed-intake scope, ran the sealed replay,
independently reconstructed the covariance identities and turning witness, and found no
load-bearing mathematical objection.

## Retained result

On the bounded G173 family, `m=|ds/dsigma|` is the Jacobian from an auxiliary parameter to the
already-supplied calibrated ruler coordinate. A fixed nonzero calibrated ruler vector therefore
fixes `m` and the terminal reciprocal scalar uniquely. An unparameterized line retains the G173
calibration atlas. Distinct `m_A` and `m_P` values describe distinct calibrated ruler vectors when
they differ; neither is physically selected.

Constant ruler-unit changes cancel from endpoint-relative depth. Position-dependent recalibration
changes the tape by the exact endpoint transition. The G173 tensor and rank theorem is retained:
angular motion keeps the pullback regular through a radial turn, and only zero complete spatial
tangent loses rank.

## Review finding and repair

The only issue was packaging. The repository-side outer verifier uses Git, the root premise
registry, and writes `VERIFICATION_RESULT.json`, so it was not replayable in the sealed no-edit
intake. It now detects the sealed `REVIEW_SCOPE.json` boundary and delegates immediately to the
read-only sealed verifier. A fresh corrected 39-file intake with scope SHA-256
`7ac5e2856b636d0662b6c7f5a3370bd9d11ef56b864e3d1e8ecf60270b1e2a74` passed through that exact
entry point with 38 sealed tree files, 12 source hashes, 32 production checks, 156,000 independent
checks, 2,000 turns, and 18 semantic catches. The scientific landing is unchanged.

## Grade

`VERIFIED_WITH_CAVEATS` for the bounded local typing theorem. Which calibrated pair map is physical,
how independently constructed tapes carry calibration, and all path, ambient, global, `X_max`,
observational, source, action, matter, bootstrap, signalling, and canon claims remain open.
