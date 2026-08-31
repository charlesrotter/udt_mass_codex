# G309 evidence-race repair preregistration

Date: 2026-08-31
Frozen banked parent: `4cc2ed0c`

## Discovery

During the first sealed-intake replay, `verify_package.py` reported 17 production checks even
though the current optimized production source defines 13. A pre-optimization symbolic process had
continued after the visible session was interrupted and later overwrote `DERIVATION_RESULT.json`
with its older nine-limit/17-check representation. The scalar curvature, residual values, landing,
and all scientific claims were unchanged.

## Exact bounded repairs

R1. Regenerate `DERIVATION_RESULT.json` from the currently banked optimized production source. It
must contain five registered flat-join limit checks and `symbolic_checks=13`.

R2. Strengthen `verify_package.py` to require exactly 13 production checks and exactly derivative
orders 0--4, so a stale concurrent output is rejected.

R3. Make `build_review_intake.py` run the no-write package verifier before copying evidence and
include this repair preregistration in the sealed intake.

R4. Amend `RUN_RECORD.md` to record the late-process overwrite and repair. No formula, witness,
candidate landing, premise grade, or scientific statement may change.

## Acceptance

- current production replay returns 13;
- package verifier passes the strengthened exact checks;
- independent and hostile outcomes remain byte-unchanged;
- fresh intake manifest is rebuilt after the repair;
- repository premise verifier still passes.

