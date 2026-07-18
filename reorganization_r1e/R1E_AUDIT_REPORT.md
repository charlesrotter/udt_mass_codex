# R1E batch-plan audit report

Date: 2026-07-18

Base: `b59005dba9acaf6c575185876655bd6a5c792094`

Branch: `codex/reorg-r1e-batch-plan-2026-07-18`

## Outcome

R1E produced ranked proposals only. No research artifact was moved, renamed, copied, deleted, or
content-edited. No migration, physics work, GPU work, deletion, canonization, or `grok` integration
is authorized.

The exact 119-candidate universe was committed at `2755abb` before candidate content inspection.
It contains all 120 fixed-base `MOVE_READY` rows resolved through
`CURRENT_ARTIFACT_PATHS.tsv`, less the already migrated S8 artifact. The frozen candidate TSV SHA-256
is `7fc413f8046de195f56424b12fa6607fed690dbd0a72064f5118e9c958f47141`.

## Mechanical result

`COMPLETE_CANDIDATE_LEDGER.tsv` has one unique row per candidate. `ATOMIC_FAMILY_GRAPH.json` has
119 candidate nodes in 71 atomic families. The entire tracked operational census has zero inbound
edges to a candidate. The separate forensic census has 726 occurrences from 10 generated
reorganization-history sources; it is retained in the ledger and does not affect selection. Candidate
dispositions are:

| Disposition | Files |
|---|---:|
| SAFE_BYTE_IDENTICAL | 36 |
| BLOCKED_IMMUTABLE_COMPANION | 37 |
| BLOCKED_RUNTIME_OR_MISSING_INPUT | 42 |
| BLOCKED_TEST_SCOPE | 1 |
| NEEDS_MANUAL_ADJUDICATION | 3 |

The leading active family is the four standalone macro SymPy verifiers. The cascade audit separates
19 standalone scripts from 61 files in blocked coherent import/runtime/output families. The
particle audit leaves all four particle scripts blocked; no data, output, or retained-module closure
was assumed complete.

The ranked proposals are 4 active files, 18 legacy files, and 14 legacy files. Active and legacy
artifacts never mix. Exact paths and hashes are in `PROPOSED_BATCH_FILE_PLAN.tsv`; common and
batch-specific rollback/verification gates are in `R1E_BATCH_PROPOSALS.md`.

## Fail-closed verification

`verify_r1e_batch_plan.py` independently rejects a missing candidate, duplicate candidate, split
dependency component, immutable companion, destination collision, unresolved runtime path, stale
current pointer, and active/legacy mixed batch. It also verifies candidate blobs/bytes,
preregistration ordering, plan-only diffs, the 1,114-row current-path registry, Markdown links,
306 frontier rows / 101 targets, all six frozen manifests and package blobs, the known full-test
baseline, and the original 54-path dirty checkout by metadata only. The dirty contents remain
`NOT_READ`.

The generated `VERIFY_RESULT.json` and test transcript/JSON are the final mechanical record.
