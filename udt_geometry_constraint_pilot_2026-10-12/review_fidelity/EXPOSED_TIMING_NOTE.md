# Exposed-review source timing clarification

The first direct-stage comparison (before parent integration) found all28
source-first pins unchanged. While EXPOSED_REVIEW.md was being written, the
coordinator made the authorized central integration. The final recorded
EXPOSED_CHECKS.json accordingly reports UDT_DEVELOPMENT.md changed. Parent
independently notified this reviewer of that intentional change immediately
after the record was written. No baseline source pins were refreshed.

The sentence in EXPOSED_REVIEW that all28 source-first pins still matched
refers to the initial direct-stage check, not to the later integrated edition.
The later machine receipt records the actual changed central source. Candidate
freeze checks all still match, and the source-first self-pin matches.

The direct verdict applies to the frozen INITIAL_CANDIDATE, explorer artifacts
and DESCENDANT_REVIEW inspected before that integration, using baseline central
sources. It does not apply to the new central integration. Actual integrated
bytes remain unread in this phase and require the pending final review.
