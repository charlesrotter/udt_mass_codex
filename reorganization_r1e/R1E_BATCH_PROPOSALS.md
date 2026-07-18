# R1E ranked batch proposals and contracts

Date: 2026-07-18

Base: `b59005dba9acaf6c575185876655bd6a5c792094`

Mode: PLAN ONLY — no migration authorization

The exact per-file paths, destinations, Git blobs, SHA-256 values, atomic family IDs, and future
navigation edits are in `PROPOSED_BATCH_FILE_PLAN.tsv`. `BATCH_RANKING.tsv` is the compact ranking.
Every proposed artifact is `SAFE_BYTE_IDENTICAL`; no proposed artifact has an operational inbound
edge, local runtime path, generated output, test glob, current-frontier role, required immutable
companion, unresolved input, or destination collision.

## Rank 1 — B01_ACTIVE_MACRO_SYMPY_QUARTET

Four active macro scripts: `verify_center_escape.py`, `verify_center_nogo.py`,
`verify_eos_dS_window.py`, and `verify_wrl_canon.py`, each to its exact `research/macro/`
destination. Each is a standalone SymPy/stdout verifier. The R1C closure audit and this independent
AST/dependency audit agree: zero operational inbound references, no file open, no generated output,
no test-glob match, no frozen-package inbound source, and no runtime-relative path. Retained result
documents and `CANON.md` are context, not runtime or path dependencies, and remain untouched.

This four-file batch is the sole exception to the preferred 5–25 size. Padding it with legacy files
would violate active/legacy separation; splitting or deferring the coherent verifier quartet is less
safe than preserving it as audited.

Future pointer plan: change only the four corresponding `current_path`/status rows in
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`, the four current-path cells in
`research/macro/ROOT_INVENTORY.tsv`, and append four rows to the future
`research/_registry/MIGRATION_LEDGER.tsv`. Fixed R1C ownership/readiness tables remain unchanged.
No source or scientific artifact receives a path substitution.

## Rank 2 — B02_LEGACY_STANDALONE_ALGEBRA_A

Eighteen legacy standalone algebra/CAS scripts, each to its collision-free
`archive/pre_2026-07-01/` destination. The exact list is in the file plan. These are 18 singleton
dependency components: external library imports and stdout only, with no file I/O, generated output,
test scope, operational inbound pointer, or runtime companion.

Future pointer plan: update the 18 authoritative rows in
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv` and append 18 migration-ledger rows. There is no
mutable operational source pointer to rewrite and no legacy current-lane inventory to mutate. All
fixed R0–R1C records retain their historical paths and bytes.

## Rank 3 — B03_LEGACY_STANDALONE_ALGEBRA_B

Fourteen additional legacy standalone scripts, each to its collision-free
`archive/pre_2026-07-01/` destination. This batch contains three independent th2 numeric verifiers,
three homogeneous-universe derivations, the redshift derivation, and seven universe-bv2 symbolic
checks. All 14 are singleton dependency components with the same closure proof as Rank 2.

Future pointer plan: update the 14 authoritative current-path rows and append 14 migration-ledger
rows. No artifact-content or path-substitution edit is planned.

## Common future execution and rollback contract

These are gates for a separately authorized R1F; they are not commands authorized by R1E.

1. Start from the exact committed R1E plan tip in a clean worktree and preregister the selected batch.
2. Re-run `verify_r1e_batch_plan.py`; require every catch-proof and repository gate to pass.
3. Confirm every planned old path, destination absence, blob, and SHA-256 against the file plan.
4. Use `git mv` for the whole batch in one mutation tile. Do not edit artifact bytes.
5. Apply only the exact current-navigation changes stated above and append rows conforming to
   `PROPOSED_MIGRATION_LEDGER_SCHEMA.tsv`. Do not rewrite fixed historical inventories.
6. Require an R100 record for every file, identical before/after Git blob and SHA-256, old path
   absent, new path present, and exactly one tracked copy.
7. Rebuild operational and forensic dependency censuses. Require zero stale operational pointers,
   exact family closure, no active/legacy mixture, and all destinations collision-free.
8. Replay all six frozen manifests and complete package path/blob sets; verify all current paths,
   Markdown links, and frontier targets; run the full tests; compare the original dirty checkout by
   status/lstat metadata only.
9. Commit one batch only. If any gate fails before commit, move every destination back to its exact
   old path and restore only the mutable current-navigation files from the clean pre-mutation index.
   If failure is discovered after commit, use a normal `git revert` of that migration commit; never
   rewrite history. Re-run every gate after rollback.

No batch may be partially committed. An import SCC, producer/output pair, runtime family, or atomic
family is the rollback unit even when that closure exceeds the preferred size.

## Blocked-family audit

The complete ledger classifies all 119 candidates exactly once:

- 36 `SAFE_BYTE_IDENTICAL` (the three proposals);
- 37 `BLOCKED_IMMUTABLE_COMPANION`;
- 42 `BLOCKED_RUNTIME_OR_MISSING_INPUT`;
- 1 `BLOCKED_TEST_SCOPE`;
- 3 `NEEDS_MANUAL_ADJUDICATION`.

No frozen candidate is `SAFE_WITH_PATH_POINTER_CHANGES` or `BLOCKED_FRONTIER_OR_CONTROL`: the
operational census found no inbound candidate pointer and the fixed `MOVE_READY` universe contains no
current-frontier/control row. Those dispositions remain valid fail-closed outcomes for future plans.
The separate forensic census retains 726 occurrences from 10 reorganization-history sources; those
generated records are immutable historical evidence and did not feed candidate selection.

The 80 `cascade_*` candidates resolve to 38 atomic families: 19 standalone safe scripts and 61
blocked files whose families contain retained solver modules, non-resolving unprefixed imports,
producer/output chains, dynamic scratch paths, absolute root paths, or missing generated inputs.
No coherent runtime family is split into a proposal. All four particle candidates remain blocked:
three by immutable evidence/output companions and one by an incomplete root-CWD input/output family.
