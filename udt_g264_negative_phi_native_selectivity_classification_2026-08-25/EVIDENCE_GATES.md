# G264 evidence gates

## Gate 1 — preregistration

`PASS`. `MAP.md`, `PREREGISTRATION.md`, `PREMISE_LEDGER.tsv`, and `SOURCE_MANIFEST.tsv` were committed
and pushed at `8af24ad6` before the outcome algebra was run.

## Gate 2 — bounded solution space

`PASS_WITH_SCOPE`. The finite local sign question is answered by an explicit smooth counterfamily.
The asymptotic classification covers the preregistered power-law family for all `alpha>0`. It is not
a census of all possible negative ends or of the time-live metric.

## Gate 3 — independent verification

`PASS_AFTER_REGISTERED_REPAIR`. The production derivation constructs the full four-dimensional
connection and curvature in SymPy. A separate dependency-free metric-first verifier begins from
metric component jets, constructs the inverse metric, differentiated Christoffels, Riemann, Ricci,
scalar and Kretschmann curvature, and two mixed Einstein channels, and only then compares with the
registered forms. It passed 1,000 exact assertions on 250 arbitrary regular jets. The older
standard-library script is now explicitly classified as a result-blind implementation-distinct
consistency replay, not a second metric-first derivation.

## Gate 4 — premise audit

`PASS`. Every asymptotic, completeness, and regularity gate remains conditional. No physical mass,
source, action, field equation, energy condition, observational result, or `X_max` profile was
introduced. The 245-row current-premise verifier passed. The repository regression suite returned
167 passed and one registered expected xfail. All 18 preregistered artifact mutations were caught.

## Gate 5 — adversarial review

`PASS_EXTERNAL_ACCEPT_PACKAGING_REPAIR__SYMPY_RUNTIME_CAVEAT`. The fresh reviewer independently
accepted the bounded scientific landing and requested R1--R3. The first repair-only follow-up then
accepted all three repairs but returned `REJECT_REPAIR` because the repaired seal omitted
`SOURCE_MANIFEST.tsv`, preventing the package verifier from rerunning inside the seal. The defect is
mechanical. The final packaging-repair reviewer accepted the corrected repository-shaped
`replay_root/` after verifying all 133 files, seven sealed sources without Git, R1--R3 continuity,
the unchanged landing, and three fail-closed packaging mutations. Its isolated runtime lacked
SymPy, so the already locally certified 27-check production script was not rerun externally; the
dependency-free metric-first verifier and every packaging-specific gate did rerun.
