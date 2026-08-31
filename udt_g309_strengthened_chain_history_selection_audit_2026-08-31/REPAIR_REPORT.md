# G309 evidence-race repair report

Date: 2026-08-31
Preregistered at: `3344ef0e`

R1 passed: `DERIVATION_RESULT.json` was regenerated from the current optimized source and now
records five flat-join derivative limits and 13 symbolic checks.

R2 passed: `verify_package.py` now rejects any result whose check count is not exactly 13 or whose
flat-join orders are not exactly 0--4.

R3 passed: the intake builder runs the no-write package verifier before copying evidence and
includes the repair preregistration and this report.

R4 passed: `RUN_RECORD.md` records the late-process overwrite.

Independent verification and hostile-catch files did not change. The metric formulas, numerical
witnesses, premise grades, candidate-B landing, and scientific conclusion did not change.

