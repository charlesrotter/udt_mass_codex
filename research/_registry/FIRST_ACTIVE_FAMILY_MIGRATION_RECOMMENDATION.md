# Ranked recommendation for the first active-family migration

This is a proposal only. R1C executes no move, rename, copy, import change, or pointer migration.

## Ranking

| Rank | Family | Current ruling | Why it ranks here |
|---:|---|---|---|
| 1 | GR→UDT selector-audit pair | Recommend as the first separately authorized active-family migration | Two Markdown files; no Python import, test, data, manifest, or six-package dependency; bounded mutable pointer closure. |
| 2 | Current foundation clarification set | Defer | Small documentation family, but it is copied/referenced throughout the immutable cold/frozen derivation record and should not be the first active move. |
| 3 | Corrected-carrier F/G/boundary-virial family | Defer | Code, JSON, logs, manifests, tests, dynamic paths, and current startup anchors form a much larger atomic closure. |
| 4 | Macro read-order anchors | Defer | Small document core but very high historical/frozen/current inbound-reference fan-out; moving it first would maximize pointer risk. |

## Rank 1 exact file set

Future destination: `research/native_action/selector_audit/`

1. `UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md`
2. `UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md`

Both must move in one commit with `git mv`, R100 detection, identical Git blob IDs, and identical SHA-256 values. The audit’s preregistration reference may remain a co-located basename after both files move.

## Dependency closure

Current operational inbound pointers requiring exact substitution:

| Source | Old target | Future target |
|---|---|---|
| `LIVE.md` | `UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` | `research/native_action/selector_audit/UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` |
| `HANDOFF.md` | same | same future target |
| `INDEX.md` | same | same future target |
| `MEMORY.md` | same | same future target |
| `INDEX.md` | `UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md` | `research/native_action/selector_audit/UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md` |

R1C navigation records containing either old path must be regenerated atomically: `research/_registry/ROOT_OWNERSHIP.tsv`, `MIGRATION_READINESS.tsv`, `CURRENT_FRONTIER_TARGETS.tsv`, and `research/native_action/ROOT_INVENTORY.tsv`; the native-action README links must also change.

After relocation, these outbound root references inside the moved pair require path qualification because their source directory changes:

- preregistration → `LIVE.md`, `HANDOFF.md`, `INDEX.md`, `MEMORY.md`, and `native_action_final_adjudication_2026-07-18/`;
- audit → `native_action_external_verifier_2026-07-18/`.

The exact relative forms from the proposed destination are `../../../LIVE.md`, `../../../HANDOFF.md`, `../../../INDEX.md`, `../../../MEMORY.md`, `../../../native_action_final_adjudication_2026-07-18/`, and `../../../native_action_external_verifier_2026-07-18/`.

There are no required Python import changes, test-path changes, runtime file-opening changes, data moves, manifest edits, or frozen-package edits. Historical `reorganization_r*` occurrences remain immutable forensic records and are excluded from the operational pointer rewrite.

## Future preregistration and safety gates

A future migration phase must freeze the then-current literal occurrence census before mutation and stop if any new runtime, manifest, test, dynamic-path, or frozen-source dependency appears. It must then:

1. verify destination collision freedom;
2. record before hashes and the exact pointer substitution plan;
3. move both files atomically with R100 and byte-identity proof;
4. apply only exact path substitutions and the relative-path qualifications above;
5. rerun corrected-boundary matching and literal `git grep`, requiring zero stale operational pointers;
6. verify every generated link and all current-frontier targets;
7. replay all six frozen manifests and prove frozen package-state identity;
8. run the full tests at the known baseline; and
9. reconfirm the 54-path dirty checkout by status/lstat metadata only.

Rollback is a single `git revert <migration-commit>` after confirming that the revert restores the two root paths, pointer hashes, and link graph. No history rewrite or destructive reset is permitted.
