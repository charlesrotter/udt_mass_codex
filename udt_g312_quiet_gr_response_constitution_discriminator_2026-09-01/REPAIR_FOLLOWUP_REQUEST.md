# G312 repair-only external follow-up request

Date: 2026-09-01

## Bounded task

Verify only preregistered repair R1 and the unchanged bounded G312 scientific landing.

1. Confirm `build_review_intake.py` is present in the repaired sealed package.
2. In a writable ephemeral copy, run `python3 -S package/verify_package.py` without repository or
   network access beyond the Codex API transport needed to launch the reviewer.
3. Confirm the replay returns 4,690 production checks, 4,824 independent checks, six semantic
   regression catches, and the unchanged landing
   `TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED`.
4. Confirm no scientific evidence, premise grade, witness, or conclusion changed during repair.

Return one exact verdict:

- `G312_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY`
- `G312_REPAIR_INCOMPLETE__LANDING_RETAINED`
- `G312_REPAIR_CHANGED_SCIENCE`
- `G312_FOLLOWUP_INCOMPLETE`

Do not edit evidence files, change the scientific question, adopt either premise, or continue the
research.
