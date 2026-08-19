# G173 evidence gates

## Gate 1 — preregistration

PASS. `PONDER_MAP.md`, `PREREGISTRATION.md`, and the 11-source manifest were committed at
`b015cd89` before outcome code or result artifacts.

## Gate 2 — bounded solution-space coverage

PASS WITH BOUNDED SCOPE. The tensor/rank theorem covers every smooth static time-orthogonal family
`F(x0,sigma)=(x0,r(sigma),gamma(sigma))` with `r>0` and nonzero complete spatial tangent. The
calibration theorem classifies an arbitrary positive weight-one density and uses two inequivalent
metric-built witnesses to decide uniqueness. It does not select one by merit. Time-live,
nonspherical, center, singular, global, and non-scalar sectors are excluded.

## Gate 3 — independent verification

PASS LOCALLY. Production passes 32 exact checks. A separate standard-library Fraction
implementation imports no production code or SymPy and passes 144,000 checks over 12,000 samples,
including 2,000 exact radial turns. The 19 mutation/semantic catches pass. Fresh external gpt-5.4
review reproduced the sealed replay and returned `G173_ACCEPTED_WITH_STATED_BOUNDS`.

## Gate 4 — premise audit

PASS INTERNALLY. The 159-row premise verifier and repository regression suite pass (129 passed,
1 expected xfail). The result retains supplied `phi` and pair family, labels the static
time-orthogonal arena as chosen/bounded, and excludes co-presence, `X_max`, G142--G160,
observations, action, source, matter, bootstrap, and signalling.

The external sealed review did not and could not rerun the repository-only Git/premise gate. It
instead passed the separate dependency-free `verify_sealed_intake.py`. These are distinct gates.

## Current grade

`VERIFIED_WITH_CAVEATS__EXTERNAL_GPT54_ACCEPTED_WITH_STATED_BOUNDS`
