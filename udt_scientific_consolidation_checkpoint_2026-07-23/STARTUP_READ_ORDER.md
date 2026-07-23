# Bounded startup read order

After the mandatory Git synchronization in `AGENTS.md`:

1. Read only the marked current block in `LIVE.md`.
2. Read only the marked current block in `HANDOFF.md`.
3. Read `SCIENTIFIC_CHECKPOINT.md`.
4. Read `CURRENT_STATUS_LEDGER.tsv`.
5. Read `METRIC_TO_FRONTIER_MAP.tsv`.
6. Read `REGRESSION_GUARD_LEDGER.tsv`.
7. Open the exact cited audit report, ledger, script, or raw output only when
   the active task makes it load-bearing.
8. Read the targeted `CLAUDE.md` method sections and only the protocol
   triggered by the task.
9. Use `INDEX.md` and `MEMORY.md` only as pointers; neither overrules
   `LIVE.md`.

For fixed-base artifact paths, use
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`. The R0--R1C tables remain
historical snapshots. Post-base scientific packages use their direct paths.

Before any solve or mutation, report:

- actual HEAD and dirt;
- the current honest claim;
- its decisive premises;
- the open gate;
- the bounded proposed action.

Do not preload the full historical `LIVE.md`, `HANDOFF.md`, or all evidence
packages. The checkpoint is a routing layer; cited evidence remains decisive.
