# G170 second repair preregistration

Date: 2026-08-19

Trigger: repair-only follow-up retained
`ENDPOINT_RELATIVE_REPAIR_VALID_BUT_CALIBRATION_CARRY_STILL_LOAD_BEARING` but found that the sealed
replay invoked the SymPy production controller, while the minimal external sandbox did not expose
SymPy.

## Registered repair

1. The sealed verifier will use only Python-standard-library code to replay the independent exact
   rational census and mutation suite.
2. It will hash-verify the stored 40/40 SymPy production artifact but will not claim to rerun SymPy
   inside the dependency-minimal sealed sandbox.
3. The SymPy production controller and repository premise/regression gates remain separately rerun
   in the outer repository environment.
4. Every document claiming a self-contained 40/40 sealed production replay will be corrected.
5. The scientific calibration-scope repair and endpoint-relative theorem must remain unchanged.

The corrected verifier must pass with `python3 -S`, which disables environment site packages. A
final repair-only external follow-up remains required before banking.

