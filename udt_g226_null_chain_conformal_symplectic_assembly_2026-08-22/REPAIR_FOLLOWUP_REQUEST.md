# G226 repair-only external follow-up request

Date: 2026-08-22

## Role and scope

Act as a fresh repair-only reviewer. Inspect only the sealed intake. Do not edit files or continue
the research.

Verify only the two preregistered repairs in `REPAIR_PREREGISTRATION.md`:

1. the aggregate verifier now replays each registered component through `/dev/null`, compares
   stdout JSON exactly with saved evidence, and completes inside the sealed read-only intake while
   preserving all evidence bytes;
2. the verifier no longer claims universal `fail-closed` coverage and accurately states its bounded
   mechanical and semantic surface.

Confirm that the production, independent, and hostile-catch evidence and the scientific landing are
unchanged. Do not reopen or extend the scientific derivation.

## Required verdict

Return exactly one:

- `G226_REPAIRS_VERIFIED__SCIENTIFIC_LANDING_RETAINED`
- `G226_REPAIRS_INCOMPLETE__SCIENTIFIC_LANDING_NOT_REOPENED`

