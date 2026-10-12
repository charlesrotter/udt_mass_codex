# Branch update workflow

Charles approved this workflow on 2026-10-12. `AGENTS.md` remains the working-method
authority. This document governs Git integration only and supplies no scientific
premises, research authorization or grade changes.

## Branch roles and cadence

- `main` is the default branch and holds the latest completed, reviewed checkpoint.
- `grok` remains the working branch. Continue the existing startup sequence there.
- At the end of each completed work order, after its required review and checks,
  update `main` from the eligible `grok` checkpoint as part of routine banking.
  Do not allow completed checkpoints to accumulate for months on `grok` alone.
- Draft or interrupted work may still be preserved on `grok` under existing rules;
  it does not automatically qualify for `main`. Record any reason an update is held.
- Keep `grok`; do not rename/delete it or change the default branch as part of an
  ordinary update. Changing the working branch requires an explicit workflow change.

## Update procedure

1. Inspect status and fetch the remote. Preserve unrelated tracked/untracked work
   and all protected payloads. Use exact commit IDs for the reviewed target.
2. Verify that the current remote `main` is an ancestor of the target and that
   the target is a completed checkpoint with the required source-relative reviews
   and matching verification evidence. Respect current permissions, protection,
   required checks and pull-request rules. Do not bypass them using admin access.
3. For a substantial catch-up or workflow transition, preserve the previous
   `main` tip with a new annotated archival tag. Never move an existing archive tag.
4. Prefer a normal fast-forward update, retaining every existing commit and
   review/provenance hash. Do not squash, rebase, force-push or rewrite history
   to make the branches agree. If `main` has independent work, stop the automatic
   update, inspect it and prepare a separately reviewed integration.
5. Publish the eligible target to `main`, keeping `grok` available. When updating
   several refs together, an atomic push can keep the branch/tag operation coherent.
   Verify remote commit IDs afterward and preserve all unrelated local work.

Checks follow the scope of the change. Scientific and source/meaning changes
retain all existing review and premise gates; operational changes need appropriate
reproducibility and unchanged-science checks. This workflow creates no bypass.
Fresh full-registry verification is required for this initial large catch-up.
Later reference-only updates may use the exact target's existing valid receipts
when no changed input or repository rule requires rerunning them.

Moving a result to `main` publishes the current research record. Conditional,
provisional, challenged and open labels retain their meanings. Only Charles can
authorize changes to `CANON.md`; integration itself is never scientific acceptance.

The initial catch-up record is [branch_integration_2026-10-12](branch_integration_2026-10-12/RECORD.md).
