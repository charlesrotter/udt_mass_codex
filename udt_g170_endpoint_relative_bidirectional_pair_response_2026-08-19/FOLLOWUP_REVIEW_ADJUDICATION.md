# G170 repair-only follow-up adjudication

Date: 2026-08-19

## Return

```text
ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING
```

## Adjudication

The scientific result and calibration-domain repair pass without a finding. The reviewer confirmed
that the theorem is now restricted to one consistently calibrated endpoint family, independent
reciprocal recalibration remains load-bearing, and the stored production and independent outputs
retain the bounded landing.

The evidence-packaging finding is accepted. The first corrected sealed verifier invoked the SymPy
controller, but SymPy was not available in the dependency-minimal external sandbox. The host-side
replay therefore did not justify the word "self-contained" for that controller.

The second repair separates the gates honestly: the sealed sandbox replays the standard-library
independent and mutation evidence and hash-verifies the saved SymPy artifact; the outer repository
environment reruns the SymPy controller, premise verifier, and regression suite.

No scientific formula, calibration scope, or ownership status changes.

