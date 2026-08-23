# G225 final repair-only follow-up request

Date: 2026-08-22

You are the external Codex gpt-5.4 reviewer performing the final mechanical repair-only follow-up.
Work only inside this sealed intake. Do not edit files or continue the research.

## Prior findings

- Fresh science review: `G225_ACCEPT_WITH_REPAIRS`; bounded scientific landing accepted.
- R1 follow-up: the source-resolution repair and full sealed replay passed, but the intake lacked
  independently checkable Git ancestry evidence.

## Verify only R2 and retained R1

1. Recompute the Git object ID of every file under `git_commit_objects/` with
   `git hash-object -t commit --stdin`; each result must equal its filename.
2. Inspect the raw `parent` fields and verify:
   - R1 implementation `6db43e9606acce0bcfc41a5e7557d9f1c514d292` directly names R1
     preregistration `78818a4818fc20f2e45efbec8b844772f6901cab` as parent;
   - the intake-builder implementation commit directly names R2 preregistration
     `857b5277102e7ed874604b68a59d5cd32f2635ee` as parent.
3. Confirm `REVIEW_SCOPE.json` names those same commits and four sealed commit objects.
4. Run `python3 g225_package/verify_package.py` and require exit zero with the unchanged counts.
5. Recheck every `PAYLOAD_MANIFEST.tsv` hash after replay.
6. Confirm that mathematical scripts, results, premises, theorem, and scientific landing remain
   unchanged from the accepted review.

## Required return

Return exactly one:

- `G225_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`
- `G225_REPAIR_INCOMPLETE`
- `G225_REPAIR_INVALIDATES_ORIGINAL_LANDING`

Then report the four recomputed Git object IDs and parent relations, replay exit and counts, sealed
hash result, and any remaining repair. Do not propose further research.
