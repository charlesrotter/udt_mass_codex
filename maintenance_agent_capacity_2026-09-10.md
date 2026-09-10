# Agent-capacity diagnostic and preservation checkpoint — 2026-09-10

Status: **partial agent usability observed; capacity cleanup NOT verified**.
This is an operational record, not a scientific result or successor work order.
Charles authorized focused cleanup after the prior whiteboard encountered a thread limit.

Repository baseline: `grok`, `443f34ab97f343cc4cdaa55520f2b322a6adc10e`.
Fetch and fast-forward-only pull succeeded; already up to date. Before these documentation
edits, tracked/index changes were absent and `git status --porcelain=v1` had 46 untracked
entries. Its SHA-256 was `55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2`.
This fingerprints status text, not protected payloads or backup completeness.

## Findings and exact limits

- The available collaboration controls are spawn, follow-up, send, interrupt, list and wait.
  No close/release control was exposed, including in deferred-tool discovery. Interrupt
  explicitly leaves an agent available; it is not a documented capacity-release operation.
- The earlier fresh `whiteboard_geometry` allocation succeeded, but another fresh spawn
  and an older completed reviewer's follow-up returned `agent thread limit reached`.
  A later geometry follow-up did succeed. This was not a permanent one-agent rule.
- In this cleanup, fresh `/root/runtime_cleanup_review` with `fork_turns: "none"` succeeded.
  While it ran, `followup_task` on `whiteboard_geometry`, asking only to preserve its existing
  advice, returned exactly `collab tool failed: agent thread limit reached`.
- The initial roster contained root running and `ors_step1_review`, `tri_step04_review`,
  `whiteboard_geometry` completed. The runtime reviewer subsequently saw root and itself
  running, the first two older reviewers completed, and no geometry entry. Neither this
  disappearance nor the earlier guard-review disappearance proves deletion, closure or
  capacity release. No such operation was requested. No additional allocation probes followed.
- The advertised concurrency allowance and documented open-thread setting are not proven to
  have identical accounting. Retained completed threads are a plausible explanation, not a
  demonstrated root cause. Multiple simultaneous specialist contexts were NOT demonstrated.

Local CLI: `codex-cli 0.153.4`, resolved from `/home/udt-admin/.local/bin/codex` to
the installed standalone package. A scoped search found no agent/thread-cap entries in
the user config; it did not establish the effective configuration of this chat.
Read-only help covered `agents`, `archive`, `app-server`, `app-server daemon` and
`app-server proxy`. No saved session was opened, resumed, forked, archived or deleted.

`codex app-server daemon version` first failed in the sandbox with `Operation not permitted`.
The authorized read-only escalated retry exited 1 with:

```text
Error: failed to connect to /home/udt-admin/.codex/app-server-control/app-server-control.sock

Caused by:
    No such file or directory (os error 2)
```

Only that default endpoint was tested; the CLI was not established as this chat's controller.
Read-only help/version commands also emitted a sandbox PATH-alias warning; this is not evidence
of the thread-limit cause. A help-directed diagnostic found `daemon status` unsupported;
the supported `version` check above replaced it. No daemon was started or restarted.

The [official subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents)
describes closing completed threads. The
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents `agents.max_concurrent_threads_per_session` for open spawned threads excluding
the primary, with `agents.max_threads` as a legacy alias. Neither establishes this chat's
effective cap or provides a missing tool. The
[app-server lifecycle reference](https://learn.chatgpt.com/docs/app-server) distinguishes
unsubscribing one's own connection from archiving/deleting persisted history; these are not
verified substitutes for releasing this chat's agent capacity. Sources checked 2026-09-10.
The OpenAI Docs skill informed this supported-control check, not any scientific conclusion.

## Separate-context check

Reviewer: `/root/runtime_cleanup_review`; fresh context, no history fork; parent model
inherited without override, exact model/version not independently attested. Exposure:
parent-supplied error history and diagnostic observations. Reviewer independently inspected
available controls, a roster snapshot and official documentation. This is an operational
conclusion review, not an independent scientific review or a replay of the parent's failures.
The final file assembly was checked by the parent; no claim of independent byte-level review.

Reviewer conclusion, retained verbatim:

> No supported close/release operation is exposed in this chat. The available controls are spawn, follow-up, send, interrupt, list, and wait; interrupt explicitly leaves the agent available. Deferred tool inspection found no additional runtime lifecycle control.
>
> This fresh review did allocate successfully. The parent’s subsequent concurrent reactivation failed with `agent thread limit reached`. That establishes partial usability, not restored capacity or a specific accounting formula. My roster snapshot showed root and this reviewer running, two older reviewers completed, and no `whiteboard_geometry`; its absence does not establish deletion or slot release.
>
> The missing default daemon socket proves only that the tested endpoint was unavailable; it does not identify this chat’s runtime. Raising config limits, launching another CLI, manipulating session files, or restarting processes would therefore be speculative.
>
> Minimal next step: complete this review normally. If required parallel work remains blocked, the missing capability must come from the owning client/runtime. A new chat in the same workspace, with this chat retained and a concise handoff, is a preservation-friendly workaround to test—not a verified cure.

These are explicitly selected paragraphs of the returned review, not a claim to have saved
its complete tool trace. No scientific evidence depended on this operational review.

## Existing whiteboard advice retained, not new research

The earlier root/geometry discussion was a two-context advisory discussion, not a panel of
independent specialists or an accepted result. Its surviving suggestion was a 60–90 minute,
repository-only data audit: freeze one ideal clock-record family, derivative order, directional
comparison rule and separately supplied observer-motion information; assess whether these can
constrain `Ric(U,U)` beyond existing source-owned relationships. Do not compute derivatives from
the fully supplied metric and call the resulting curvature independently recovered from clocks.
Compare geometries sharing exactly the declared records. An already-owned identity, a genuine
unresolved identifiability question or an explicit ambiguity would each be legitimate outcomes.
This paragraph preserves advice only; its scientific source dependencies were not re-audited
in this runtime task. It neither establishes the proposed bridge nor authorizes the audit.

## Return point and preservation

No agent limit, runtime configuration, method guardrail, scientific source, grade, canon or
fixed-snapshot manuscript was changed. No session history or temporary reviewer evidence was
deleted. Protected payloads were not opened or hashed. Original review/evidence files were
not modified; historical missing-buffer disclosures remain in force. Backup completeness and
pre-reboot unsaved-state disposition remain UNVERIFIED; ScratchDisk remains relevant only to
archive-dependent tasks. This task did not re-run the scientific full365/fast-test suites:
the existing maintenance evidence remains at its unchanged source scope.

Parent packaging checks: whitespace check passed; the only pre-existing tracked-file change
was the two-line INDEX pointer. Excluding the two authorized documentation paths, the
46-entry status-text fingerprint matched the baseline above exactly. This checks visible
repository state, not the contents or completeness of protected/untracked payloads.

Next runtime action, if a larger simultaneous panel is required: use a supported lifecycle
control in the actual owning client, if available, or test a fresh session in this workspace
while retaining this conversation. Do not resume/fork the old scientific context or delete
history as a guessed remedy. Follow normal on-disk startup; this checkpoint is not a new
scientific status authority. A fresh session is a proposed workaround, not a verified fix.
No further infrastructure work or scientific campaign is launched by this note.

## Fresh-session handoff — 2026-09-10 authorization update

Charles subsequently approved the recommended fresh Codex session and requested startup-document
updates plus a stale-content audit/archive. The conditional recommendation above is preserved as
diagnostic history; the transition is now approved, but full capacity is still UNVERIFIED.
Here, "session" means a fresh top-level Codex session in `/home/udt-admin/udt_mass_codex`, not a
required ChatGPT web chat, a resumed/forked old context or a newly launched scientific campaign.
Retain the old session history. The owning client must open the new top-level session; no available
tool here replaces the current one. Do not launch an unrelated CLI process as a substitute.

After AGENTS' normal synchronization, bounded startup reads, premise verification and orientation:

1. Inspect the new session's actual agent controls and roster. Distinguish configured model from
   what the runtime actually attests; the installed CLI alone establishes neither. Reuse this
   diagnostic; do not repeat completed CLI/documentation searches without new evidence.
2. Test availability with useful work, not dummy spawns: at most two short complementary,
   read-only handoff checks in fresh contexts, ten minutes total. One checks authorization and
   preservation wording, the other runtime/evidence wording; the primary checks the saved
   checkpoint. No sub-delegation, science, capacity increases, session deletion or daemon restart.
   Record successful allocations and any actual overlap. A completed list alone does not prove
   simultaneous capacity. Stop additional attempts on a recurring limit; report the exact blocker.
3. Return to lay discussion using the already-preserved whiteboard advice above. The suggested
   60–90 minute ideal clock-data/curvature identifiability audit is PROPOSED, NOT AUTHORIZED.
   Recheck exact source dependencies before scientific use. No solve, premise adoption, grade
   change, banking or physical identification follows from the handoff or availability test.

The full365 maintenance PASS belongs to its recorded source snapshot; normal fresh-session startup
still runs the verifier and reports the actual result. A runtime limitation blocks only the work
requiring that capability, not all repository work or UDT research. Backup completeness and
pre-reboot unsaved-state disposition remain UNVERIFIED; ScratchDisk remains archive-only.

### Startup/stale-content edit scope and review record

Baseline: `6264a10387d2abab5f996849dd1e8f9b3b2b6ac1`, synchronized `grok`.
The compact current sequence lives in HANDOFF, with LIVE/MEMORY/INDEX pointers. No method guard,
scientific source, exact premise registry, canon or fixed manuscript is edited.
Audit scope: current startup blocks, method/readme adapters, this checkpoint, the maintained
roadmap and central archive navigation; not a repository-wide historical or protected-payload scan.

Stale labels corrected: roadmap's "Authorized next campaign" and spent ND dispatch imperatives;
INDEX's previous compaction labeled "Current" and NE1 labeled "Latest" despite its NCI1 pointer;
research README's Aug31 "latest" archive pointer. The old HANDOFF "resume anchor" title is also
clarified. The roadmap's result scopes, original work orders, completed campaign evidence and
paused/open boundaries are retained. Repeated NE1 narrative in HANDOFF is shortened to its exact
UNPROMOTED/source pointer, not retracted; LIVE/INDEX retain the scope and archive retains the prose.

Pre-edit copies of seven documentation files, with exact Git baseline and SHA-256 manifest:
`archive/startup_surface_2026-09-10_pre_session_handoff/README.md`.
The first uncommitted handoff draft and its failing checks are preserved there separately.
Initial tests: 365 passed, two failed, one full-audit entry deselected. The additions exceeded
readability ceilings and put five sentences into a three-sentence next gate; repair compacts
the documents and restores that gate without changing tests. The prior INDEX runtime pointer
already exceeded its ceiling at baseline; this edit also compacts it.

Final verification: 367 targeted startup/maintenance tests PASS, one full-audit entry explicitly
deselected (10.69 seconds); seven archive copies match Git byte-for-byte; manifest and maintained-
document whitespace checks PASS. Unfiltered staged whitespace checking flags only ten required
blank-context markers in the preserved raw Git patch; its original bytes are retained and that
artifact alone is excluded from formatting lint, not from the SHA-256 manifest. Exact warning
output and scoped command are saved. No scientific/test gate is changed.
Visible unrelated status remains 46 entries with the baseline fingerprint above.
All tracked files outside the declared documentation paths are unchanged, including the exact
registry, premise checker, method instructions, tests, canon, fixed manuscript and scientific sources.
Scientific full365 was not repeated for this editorial-only edit; prior results are not relabeled
as a new run. Exact commands, tool output and limitations: archive `FINAL_HANDOFF_CHECKS.json`.

Fresh separate-context editorial review: VERIFIED-WITH-CAVEATS, no unresolved wording defect;
reviewer `/root/startup_handoff_review`, inherited parent model, exact model/version unattested.
Its source/diff exposure, actual checks and omissions are retained in archive `HANDOFF_REVIEW.md`.
The reviewer did not independently attest parent tests, archive hashes or this final receipt.
One wording repair retained "unproduced" rather than ambiguous "missing" for the old report.
The verifier-before-record protocol kept editorial fidelity distinct from scientific promotion;
OpenAI Docs kept documented lifecycle features distinct from actually exposed runtime controls.

## Subsequent simulated startup rehearsal — 2026-09-10

`startup_dress_rehearsal_2026-09-10/README.md` records a successful fresh-context rehearsal,
initial and repaired full365 runs, 367 targeted checks, and focused review of two minor repairs.
AGENTS now distinguishes top-level startup from scoped review; a summary spacing typo was fixed.
This is dated operational evidence, not a new-session PASS, capacity reset or scientific promotion.
The approved fresh-session transition and proposed-but-unauthorized scientific audit stay distinct.
