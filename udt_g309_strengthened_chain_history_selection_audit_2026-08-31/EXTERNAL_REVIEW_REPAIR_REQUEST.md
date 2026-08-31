# G309 repair-only external follow-up request

## Role and frozen landing

Verify only the repairs preregistered in `EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md`. The bounded
scientific landing was accepted by the first review and must not be changed or extended.

## Required checks

1. Run all four package-local commands under `python3 -S` in a writable ephemeral copy.
2. Confirm that the production derivation uses no third-party dependency and checks the same exact
   rational identities, flat-join structure, and high-precision witness.
3. Confirm that `verify_package.py` executes the live production builder and requires exact equality
   with `DERIVATION_RESULT.json`.
4. Confirm that repository-only gates are now explicitly reported as provenance and are not promised
   as sealed-intake replays.
5. Confirm that formulas, witnesses, premise grades, ownership, and scientific landing did not change.

Return exactly one of:

- `G309_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`
- `G309_REPAIRS_INCOMPLETE`

Do not edit files, continue the research, select a UDT law or history, or inspect outside the intake.
