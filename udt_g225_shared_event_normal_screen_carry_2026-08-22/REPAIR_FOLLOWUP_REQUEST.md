# G225 repair-only follow-up request

Date: 2026-08-22

You are the external Codex gpt-5.4 reviewer performing a repair-only follow-up. Work only inside
this sealed intake. Do not edit evidence files or continue the research.

## Original verdict

```text
G225_ACCEPT_WITH_REPAIRS
```

The original reviewer accepted the bounded scientific theorem and required one packaging repair:
the aggregate verifier had to resolve the unchanged source-manifest paths against the
intake-local `frozen_sources/` tree and exit zero inside the sealed intake.

## Frozen repair scope

Verify only:

1. `REPAIR_PREREGISTRATION.md` predates the implementation commit represented by this intake.
2. `verify_package.py` uses the repository root for normal repository replay and the
   intake-local `frozen_sources/` root when that directory exists.
3. Source paths remain contained under the selected root and all nine source SHA-256 checks remain
   enforced.
4. `python3 g225_package/verify_package.py` exits zero from the sealed intake root.
5. The replay leaves all sealed payload hashes unchanged.
6. No mathematical script, result count, theorem, premise, or scientific conclusion changed.

Do not reopen or extend the science except to confirm that the original bounded landing is
unchanged.

## Required return

Return exactly one:

- `G225_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`
- `G225_REPAIR_INCOMPLETE`
- `G225_REPAIR_INVALIDATES_ORIGINAL_LANDING`

Then state the replay exit status, exact counts, sealed-hash result, and any remaining repair. Do
not propose a next research package.
