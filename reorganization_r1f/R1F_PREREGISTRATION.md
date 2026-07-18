# R1F active macro SymPy verifier quartet preregistration

Date: 2026-07-18

Base: `14ba31a77aed1553c5df8ecd59b0f7a000c10e20`

Branch: `codex/reorg-r1f-macro-verifier-quartet-2026-07-18`

Authorized batch: `B01_ACTIVE_MACRO_SYMPY_QUARTET`

## Scope frozen before mutation

R1F may move exactly the four rows frozen in `PREREGISTERED_BATCH.tsv` from repository root to
their matching paths under `research/macro/`. The paths, destinations, atomic family IDs, Git blobs,
SHA-256 values, and byte-identical-only policy are copied mechanically from the R1E file plan at
base. No other artifact may move, rename, duplicate, be deleted, or be content-edited.

Before mutation, each source is run once from repository root as a bounded CPU process with the exact
command template recorded in `PREREGISTERED_INPUTS.json`. Python and SymPy versions, exit code, and
raw stdout/stderr bytes and SHA-256 values are retained. After the four-file `git mv`, the same
process is run with only the script path changed to its destination. Acceptance requires identical
exit codes and byte-identical stdout and stderr for each script.

## Dependency and mutation contract

The R1E audit is challenged again before movement. Every script must have only the external SymPy
import, stdout-only behavior, no file open, no generated output, no runtime-relative path, and no
frontier, manifest, test, frozen-package, or operational-inbound dependency. Any contrary evidence
stops the phase.

The four `git mv` operations form one atomic batch. The migration/navigation commit may contain only:

- four R100 renames to the registered destinations;
- four `CURRENT_ARTIFACT_PATHS.tsv` current-path/status changes to `MIGRATED_R1F`;
- four `research/macro/ROOT_INVENTORY.tsv` current-path substitutions;
- R1F operational evidence and verification records that do not alter historical records.

R0–R1E records are immutable. No scientific prose, equations, claim labels, result, `CANON.md`,
evidence, data, control, solver, or unrelated artifact may change.

## Two-commit provenance contract

The migration/navigation update is committed first. Only after that commit exists may
`research/_registry/MIGRATION_LEDGER.tsv` be created with four rows conforming to the R1E registered
schema. Each ledger row names the completed migration commit; `rollback_parent` is exactly that
commit's first parent. The ledger and final audit are a later commit, preventing a self-referential
commit hash.

## Fail-closed acceptance

Acceptance requires four R100 renames; identical source/destination blobs and SHA-256 values; old
paths absent; destinations present; no duplicate copies; pre/post behavioral identity; exactly 1,109
`ROOT_RETAINED`, one `MIGRATED_R1D`, four `MIGRATED_R1F`; 1,114 unique original/current paths; zero
stale current-navigation pointers; valid ledger commit/parent fields; all links and frontier targets;
all six frozen manifests and package states; the known test baseline; and unchanged 54-path original
dirty-checkout status/lstat metadata with content recorded as `NOT_READ`.

Catch-proofs must reject a missing move, artifact mutation, wrong destination, behavioral-output
mismatch, duplicate current path, stale pointer, and invalid ledger commit.

Maximum conclusion: B01 migrated byte-identically with behavior and navigation preserved. Stop before
B02/B03, `grok` integration, physics work, canonization, or GPU work.

