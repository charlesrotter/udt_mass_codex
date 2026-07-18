# R1C recommendation-correction preregistration

Date: 2026-07-18  
Base: `204f3637f134811f05df12aa7494ef41289ee3b4`  
Branch: `codex/reorg-r1c-correction-2026-07-18`  
Mode: organization-record correction only; additions and exact corrections; no research-artifact relocation

## Trigger and bounded question

The retained R1C overlay recommended two selector-audit files even though its controlling
`MIGRATION_READINESS.tsv` classifies both `IMMUTABLE_PATH`, with blocker
`R0_FROZEN_EVIDENCE` and destination `-`. The recommendation is therefore invalid under R1C's
own rules.

This correction asks one bounded organizational question: after a complete dependency and family
closure audit, does any one of the 13 root files that are simultaneously owned by an active research
lane and classified exactly `MOVE_READY` support a valid first-migration recommendation?

No physics claim is tested or changed. No research artifact may be moved, renamed, copied, deleted,
or content-edited in this phase. It is acceptable, and pre-authorized, to conclude `NO_MIGRATION_AUTHORIZED_YET`.

## Frozen inputs and candidate universe

The hashes in `PREREGISTERED_INPUTS.json` freeze the controlling ownership/readiness tables, both R1B
dependency censuses, the current-frontier table, and dirty-checkout metadata inventory. The exact
13-row candidate universe is frozen in `PREREGISTERED_ACTIVE_MOVE_READY_CANDIDATES.tsv`. It was derived
mechanically before opening any candidate file: `primary_owner` is one of `FOUNDATIONS`,
`NATIVE_ACTION`, `PARTICLE_MASS`, or `MACRO`, and `migration_readiness` is exactly `MOVE_READY`.
Generated correction records cannot enter candidate selection.

## Preregistered closure audit

Every candidate will receive one row and an explicit ruling. Before any recommendation, inspect:

1. all inbound references in the full forensic and operational dependency censuses;
2. a corrected-boundary filename scan and literal `git grep` cross-check across the tracked base;
3. all outbound Markdown links, explicit file paths, imports, file opens, command-line defaults,
   runtime-relative paths, and unresolved/dynamic path construction;
4. generated output names and consumers of those outputs;
5. every frozen, manifest, preregistration, historical-snapshot, and current-frontier reference;
6. family companions required for the artifact to remain intelligible or runnable after a move;
7. destination collision freedom and the exact pointer/import/path substitutions a later phase would require.

The apparent one-file candidate
`simple_metric_S8_action_provenance_note.md` is not privileged. Its outbound reference to
`simple_metric_solution_space_ZOOM.md` must be recorded and resolved in the closure audit.

## Recommendation gate

A recommended file must, without exception:

- occur exactly once in the controlling readiness table;
- be classified exactly `MOVE_READY`;
- have a destination other than `-`, identical to the recommendation record;
- belong to an active research lane;
- have no frozen or manifest prohibition in the ownership or readiness evidence;
- survive the complete closure audit above, including any required family companions.

The independent verifier will reject a recommendation that violates any gate. Its catch-proof will
substitute each selector-audit path into the recommendation record and require rejection.

## Registered outputs and maximum conclusion

- a complete 13-row candidate closure audit;
- a corrected human recommendation record;
- a machine-readable recommendation record;
- a corrected R1C audit report;
- an extended fail-closed verifier and machine verification result;
- repeated link, frontier, six-manifest, test-baseline, and dirty-checkout metadata checks.

Maximum conclusion: either one closure-audited future migration recommendation, still requiring a
separate dispatch, or `NO_MIGRATION_AUTHORIZED_YET`. R1D and content migration remain forbidden.

