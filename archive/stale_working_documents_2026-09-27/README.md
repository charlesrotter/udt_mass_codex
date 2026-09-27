# Historical working documents — archived 2026-09-27

These seven completed operational documents were removed from the active root
under Charles's instruction to remove and archive stale material. Their original
bytes, dates, instructions, caveats and failed checks are preserved. Their old
“next,” “current,” or authorization language is historical, not a new dispatch.
Use root `AGENTS.md`, `LIVE.md` and `INDEX.md` for current work.

The exact source/destination/blob/hash inventory is
[`ARCHIVE_MANIFEST.tsv`](../../udt_foundation_alignment_audit_2026-09-27/continuation/archive/ARCHIVE_MANIFEST.tsv).
Baseline: `b770dc484d4dc991644f170a3eeb3cfa4616e58d`. All seven files retain
their original basenames, so a known root basename can be found in this directory.

| Document | Retained historical role |
|---|---|
| [Atlas startup note](ATLAS_UNTRACKED_STARTUP_NOTE_PREREG_2026-08-05.md) | Old protected-work warning registration; current protection still applies |
| [Phi-orchestra startup update](PHI_ORCHESTRA_STARTUP_UPDATE_PREREG_2026-08-05.md) | Completed navigation-update work order |
| [Phi-orchestra verifier repair](PHI_ORCHESTRA_VERIFIER_LIVE_REGISTRY_REPAIR_PREREG_2026-08-05.md) | Past registry-hash repair registration |
| [Synthesis method review](UDT_SYNTHESIS_METHOD_PATCH_REVIEW_2026-09-05.md) | Completed method-fidelity receipt |
| [Agent capacity diagnostic](maintenance_agent_capacity_2026-09-10.md) | Dated partial-usability and later rehearsal evidence; general capacity was not established |
| [Restart checkpoint](RESTART_CHECKPOINT.md) | Pre-reboot record with unresolved backup/unsaved-state limitations |
| [Restart work order](UDT_Cold_Start_Rehearsal_and_Workstation_Restart.md) | Historical instructions for that particular transition |

Historical root-relative references inside these documents retain their original
meaning. Use the batch manifest for relocated names and the source commit for an
exact historical tree. Old tree inventories, source snapshots and test transcripts
were not rewritten. A similarly named package-local checkpoint is not relocated
by this manifest.

For example, recover the original root document from Git without changing files:

```sh
git show b770dc484d4dc991644f170a3eeb3cfa4616e58d:RESTART_CHECKPOINT.md
```

Or locate its new path by exact old basename:

```sh
rg -n '^RESTART_CHECKPOINT.md\t' udt_foundation_alignment_audit_2026-09-27/continuation/archive/ARCHIVE_MANIFEST.tsv
```

This is an archival lookup, not a scientific or current-frontier registry. The
older 1,114-row reorganization ledger remains unchanged. Fixed-path rehearsals,
live verifier inputs, scientific evidence and all protected/unrelated work were
excluded. Archiving does not establish backup completeness, resolve old lost-work
questions, update runtime capability, or authorize a reboot or research successor.
