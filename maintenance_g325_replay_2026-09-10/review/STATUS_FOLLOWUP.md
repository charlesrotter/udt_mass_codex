# Focused documentary closeout

Date: 2026-09-10 UTC. Verdict: **VERIFIED-WITH-CAVEATS for the final status
updates and maintenance closeout. Full365 remains NOT_PASSED.** No blocking
fidelity defect found in the reviewed updates. This addendum preserves and
extends [the initial checker review](REVIEW.md); it does not replace its scope
or certify scientific promotion.

The same separate reviewer context `/root/replay_maintenance_review`, model
UNKNOWN, inspected the seven status-file diffs and final WORK_RECORD, the
completed full-audit capture, G349's relevant checker logic, and the current
research-program sentence. The reviewer independently repeated the direct G349
no-write check and preservation checks. The 273-second full365 process was not
independently rerun in this focused follow-up.

## Actual outcome and fidelity

The author's preserved `full_after_g325_g326.json` records the unmodified root
verifier exiting **1 after 273.132675 seconds**, before its 300-second timeout.
Its stderr identifies `G349 dependency-free no-write replay failed`. The root
checker executes G325 and G326 before reaching G349, so this is evidence that
the earlier stopping points were passed; it is not evidence that later gates
were reached or that the full audit succeeded.

The independent no-write G349 rerun also exited 1, with **20/21 gates true**.
The only false gate is `geometric_not_physical_union_scope`. G349's unchanged
checker requires the literal text `geometric endpoint image-union` in
CURRENT_RESEARCH_PROGRAM.md and excludes `physical image-union`. The first
phrase is absent and the second is also absent. The unchanged scientific
sentence instead reads:

> G349 finite sheet area is not endpoint image-union; that needs supplied global preimages.

The other 20 package gates, including source hashes, scientific producer replay
counts, no-write behavior, and bounded physical scope, pass. These are the
existing package checks, not a new independent proof of the area theorem.
The observed remaining failure is therefore a documentation/checker wording
mismatch at this gate; this review found no scientific-result disagreement.
The task's declared different-failure stop is respected: neither G349's code,
results, nor the quoted scientific sentence has been repaired or rewritten.

The seven edited status files truthfully replace the former G325 blocker with
G349's documentation gate. LIVE identifies the repaired G325/G326 replays and
retains no scientific banking/integration; the other pages retain NOT_PASSED or
explicitly identify the unfinished audit. INDEX links the work record.
UDT_RESEARCH_ROADMAP updates its current blocker without authorizing a new
scientific campaign, adopting a premise, or asserting full completion. The
unchanged scientific scopes and original review limitations remain intact.

WORK_RECORD distinguishes the initial uncaptured startup observation, the
artificially memory-capped failed captures, the later unrestricted completed
audit, and the reviewer's package-only baseline reproductions. It accurately
separates historical v1 aggregate JSONs from fresh v2 replay stdout, and states
that later full-audit gates remain unreached.

## Verification, pinned records, and omissions

Independent entry command, from repository root:

```text
timeout 60s python3 -B maintenance_g325_replay_2026-09-10/review/status_followup_checks.py
```

[Status follow-up results](status_followup_results.json) preserve the exact
G349 argv, environment overrides (`UDT_NO_WRITE=1`,
`PYTHONDONTWRITEBYTECODE=1`), cwd, exit code, complete stdout/stderr, duration,
full final status diff, and SHA-256 values for all seven status files and the
work record. The G349 child was bounded at 40 seconds and completed normally.

All **33 tracked G349 files** were independently checked byte-identical to
baseline `51f189679d4029d750e375be949f41e2f15420fa`, before and after replay.
The two G325/G326 executable hashes still match the initial reviewed candidates.
The root full verifier, exact registry, CANON, fixed manuscript, and coverage
TSV also remain byte-identical to baseline. The initial REVIEW.md was preserved
with SHA-256 `09e7141d4c733a7c0cb7d517eb6ba1a59693df07c7177ea0e1617a5802b33940`.

The final reviewed WORK_RECORD SHA-256 is
`0dd7abc5e95ff7b6056566c2bac6593115dda840efd3828ed96fb44041b52238`.
The final CURRENT_RESEARCH_PROGRAM.md SHA-256 is
`ef41f98e423009b3dd06a9269bf3fde3a0e4d92ddd3b552c783afefcdb2cb6bc`;
all remaining final document hashes are in the machine-readable result.
No unexpected tracked modification was present: the changed tracked set was
exactly the seven status files and two previously reviewed checkers.

The author-side post-edit startup check initially caught a one-word orientation
limit overflow (1101 versus 1100). Its failed capture is preserved. The final
one-word shortening affected only the new status sentence. The reviewer
inspected `startup_checks_repaired.json`: **353 passed, one explicitly deselected,
exit 0**. The deselected full-premise test was run separately and failed at G349;
the focused startup suite is not a waiver or full365 pass. `git diff --check`
also passes. Those startup tests were inspected, not independently repeated by
this reviewer.

No protected payloads were read, no G349 repair was attempted, and no full
scientific proof, downstream gate, external backup, or remote-publication
claim is added. The bounded maintenance repair and its honest status closeout
are reviewed; the distinct G349 documentation gate remains open.
