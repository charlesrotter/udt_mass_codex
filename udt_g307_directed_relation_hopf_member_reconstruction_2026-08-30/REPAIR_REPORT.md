# G307 repair report

Date: 2026-08-31
Status: `INTERNALLY_REPAIRED_AFTER_EXTERNAL_SCIENTIFIC_SUPPORT__FOLLOWUP_PENDING`

Fresh external review returned `G307_REPAIRABLE_DEFECTS` while explicitly finding no scientific
defect and retaining the exact bounded landing. Repairs R1--R4 were preregistered and pushed at
`f91bfb85` before implementation.

## Closed internally

- **R1:** the intake builder now resolves sources uniquely in repository or sealed `frozen_*`
  layouts. Repository and sealed rebuilds produce identical scope, manifest, and detached-seal
  hashes. Missing and ambiguous source/current layouts are rejected.
- **R2:** the independent verifier now reconstructs the unique left and right members directly
  from `(p,v)` by solving against two independently built imaginary-quaternion evaluation maps.
  It recovers the closed formulas and full operators in 32,000 checks with maximum error
  `4.1389114358025836e-13` and no production import.
- **R3:** the hostile suite now catches eight exact direct mathematical corruptions in addition to
  fourteen semantic ownership/report mutations.
- **R4:** sealed package replays are distinguished explicitly from whole-repository premise and
  pytest gates.

## Unchanged

The production result remains 36 exact cases and 1,806 assertions. The member census, orientation
typing, physical-population boundary, metric, reciprocal kernel, and exact scientific landing are
unchanged. Repair-only external follow-up remains required.
