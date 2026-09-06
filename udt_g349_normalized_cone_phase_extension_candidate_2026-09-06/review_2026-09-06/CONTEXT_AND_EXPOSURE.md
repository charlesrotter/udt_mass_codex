# Review context, source freeze and exposure sequence

Review target: initial candidate commit
`f14098737a7bd571aff79bef09ccffdc22135853`, not the later method commit.
Actual reviewer: `/root/normalized_cone_adversarial_review`.

The parent spawned this agent with `fork_turns="none"`, no model override and no
conversation-history inheritance. This is a tool-created separate context, not
the author simulating a reviewer. The exact reviewer model is UNKNOWN from the
available reviewer runtime; no different-model assertion is made. The older
`g352_source_first_review` agent was not reused.

## Source-first exposure

The initial dispatch supplied the bounded question, allowed accepted source
paths, method/protection instructions, budget and scratch directory. It supplied
no candidate proof, code, result, README or prior candidate verdict. Stage A
independently reconstructed the question from the G349/G351/G352 sources and
wrote a report plus a small symbolic witness with no candidate imports. It
encountered accepted-source historical verdicts and counts, not the new
candidate's self-review. See STAGE_A_REPORT.md for the full exposure list.

Parent authenticated the source-only report and copied its bytes using
apply_patch into this review directory BEFORE the Stage B follow-up dispatch:

    STAGE_A_REPORT.md
    SHA-256 6bb4d06722a009b7958495f7e4c5eb87669bd883cff8fdd5a519884ff6ffdce3

The original and archived hashes agree. The empty stderr artifact remains
zero bytes (SHA-256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855).
The local clock at authentication/archive completion was 17:19:11 UTC on
2026-09-06. Stage B was then sent with the exact candidate path and review
questions. Hashes authenticate bytes; the sequence is documented by the
actual controller actions, not certified by an external timestamp authority.

Stage A independently used a spacelike initial-surface/characteristic argument.
Its similarity to the candidate's strategy does not establish a different
mathematical route; its source-first reconstruction did precede exposure.
Separate context, separate implementation, different method and different model
remain distinct axes.

## Candidate and source versions

Before review the original ARTIFACT_SHA256SUMS passed for all 14 payloads and
the original SOURCE_SHA256SUMS passed for all 19 entries. The parent then froze
all 15 original package files, including the original manifest itself, in
FROZEN_CANDIDATE_SHA256SUMS. A Git diff against f1409873 confirmed no changes to
those original candidate files before Stage B. No accepted scientific file has
changed.

Charles separately requested the complete-cycle instruction convention. Its
method-only commit is `b75fcc5e641702d0cae3e8740046513cbd4e8dd5`; it changes AGENTS,
the corresponding size-test ceiling and two small verification records. This
is not a premise change. The old SOURCE_SHA256SUMS intentionally retains the
AGENTS hash at f1409873:

    b9c4e7a0d90c66868281ced3e96da3a16a19797a91cb100b64b4b85620ff2f34

`git show f1409873:AGENTS.md | sha256sum` reproduced that value. The other 18
source-manifest entries match live files. The reviewer was explicitly told of
the method-only HEAD movement; its beginning-of-review observation of f1409873
is not represented as the later live HEAD.

The parent ran the fresh premise verifier once this cycle: exit 0, 335 rows,
completed output retrieved at 17:15:05 UTC. Exact command/output is preserved in
PREMISE_VERIFIER_RUN.json. The reviewer was informed of this result but did not
independently rerun it. That distinction is retained in its Stage A record.

## Preservation and pending scope

This file records provenance, not a scientific verdict. Final direct review and
any focused repair/re-review are recorded separately. A later update of the
package's current-status documentation must not be confused with editing the
initial reviewed argument. Original f1409873 files remain recoverable through
Git and the pinned manifest.

Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
ScratchDisk is an archive-only blocker and was unused. The reviewer writes only
under `/tmp/udt-cone-review-0WvbvE/`; parent archives relevant evidence. No
protected payload, disk, worktree, model configuration, accepted grade, premise,
manuscript or canon is changed by this review.
