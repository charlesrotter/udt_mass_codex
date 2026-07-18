# Corrected ranked recommendation for the first active-family migration

> **R1C correction layer (2026-07-18):** the earlier selector-audit recommendation is invalid and
> superseded by this record. R1C still executes no move, rename, copy, deletion, import change, or
> pointer migration.

The selector-audit files are not candidates: both are `IMMUTABLE_PATH`, blocked by
`R0_FROZEN_EVIDENCE`, with destination `-`. Recommending either would violate the controlling
[`MIGRATION_READINESS.tsv`](MIGRATION_READINESS.tsv).

## Corrected decision

Recommend one file for a later, separately authorized migration:

`simple_metric_S8_action_provenance_note.md`
→ `research/macro/simple_metric_S8_action_provenance_note.md`

This is a proposal, not move authority. The machine-readable ruling is
[`FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.json`](FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.json),
and the complete 13-row closure is
[`CANDIDATE_CLOSURE_AUDIT.tsv`](../../reorganization_r1c/correction/CANDIDATE_CLOSURE_AUDIT.tsv).

## Ranking of the preregistered 13 candidates

| Rank | Candidate | Closure ruling |
|---:|---|---|
| 1 | `simple_metric_S8_action_provenance_note.md` | `PASS_RECOMMENDED` |
| 2 | `verify_center_escape.py` | `PASS_DEFER_FAMILY_BUNDLE` |
| 3 | `verify_center_nogo.py` | `PASS_DEFER_FAMILY_BUNDLE` |
| 4 | `verify_eos_dS_window.py` | `PASS_DEFER_FAMILY_BUNDLE` |
| 5 | `verify_wrl_canon.py` | `PASS_DEFER_FAMILY_BUNDLE` |
| 6 | `simple_metric_legacy_double_fix_side_excursion.md` | `BLOCKED_TEST_SCOPE_AND_ACTIVE_FAMILY_MISMATCH` |
| 7 | `simple_metric_dotted_line.py` | `BLOCKED_IMMUTABLE_GENERATED_OUTPUT` |
| 8 | `simple_metric_promising_candidates_zoom.py` | `BLOCKED_IMMUTABLE_GENERATED_OUTPUT` |
| 9 | `simple_metric_relational_rooms_continue.py` | `BLOCKED_IMMUTABLE_GENERATED_OUTPUT` |
| 10 | `noNull_evidence_checker.py` | `BLOCKED_FROZEN_EVIDENCE_AND_ABSENT_INPUTS` |
| 11 | `hopfion_static_mass_hessian_256driver.py` | `BLOCKED_IMMUTABLE_IMPORT_OUTPUT_AND_ABSENT_INPUT` |
| 12 | `controlled_relax_hessian.py` | `BLOCKED_FROZEN_OUTPUT_ROOT_RUNTIME_AND_ABSENT_INPUTS` |
| 13 | `long_relax_256.py` | `BLOCKED_ROOT_RUNTIME_AND_ABSENT_INPUTS` |

The four standalone SymPy verifiers have clean individual runtime closure, but they form a coherent
verification family with immutable result companions; a later phase should adjudicate the quartet
together. The explicitly legacy side-excursion also matches a root-only hygiene-test glob, so moving
it would change test coverage before its archive-versus-active ownership is resolved. The remaining
scripts are blocked by root-relative runtime behavior, absent/local inputs, immutable generated
outputs, or immutable internal dependencies.

## Rank-1 complete closure

- **Controlling row:** owner `MACRO`; readiness exactly `MOVE_READY`; destination exactly the path
  above; frozen/manifest status `NOT_FROZEN_OR_MANIFEST`.
- **Inbound:** zero operational dependency edges. The eight forensic dependency edges are all
  historical `reorganization_r*` snapshots. Corrected-boundary scanning found 51 occurrences across
  the same 15 sources found by literal Git scanning at base `204f363`; no frozen package refers to it.
- **Outbound:** the sole file reference is line 10,
  `simple_metric_solution_space_ZOOM.md`. That companion remains at root. From the future destination,
  the exact path-only substitution is `../../simple_metric_solution_space_ZOOM.md`.
- **Runtime/tests/outputs:** no imports, file opens, generated outputs, manifests, unresolved dynamic
  paths, or matching hygiene-test glob. The proposed destination is collision-free.
- **Family:** the note is self-contained; `simple_metric_solution_space_ZOOM.md` is its one referenced
  companion and need not move.

Current R0/R1A/R1B/R1C inventories and preregistrations remain immutable historical snapshots. A later
migration must regenerate only then-live navigation tables and the macro inventory; it must not rewrite
the historical records.

## Future migration and rollback gates

A separate dispatch must preregister the then-current closure, confirm no new dependency, and:

1. prove the destination remains collision-free;
2. record the source blob and SHA-256;
3. use `git mv` and require R100 plus identical blob and SHA-256;
4. change only the line-10 path token described above;
5. regenerate current navigation records without changing historical snapshots;
6. require zero stale operational pointers and all links/frontier targets valid;
7. replay all six frozen manifests and prove package-state identity;
8. run the full test baseline; and
9. reconfirm the dirty checkout by status/lstat metadata only.

Rollback is `git revert <migration-commit>`, followed by proof that the root path, path token,
navigation records, hashes, and link graph are restored. No history rewrite or destructive reset is
permitted.
