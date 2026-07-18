# R1E batch-migration planning preregistration

Date: 2026-07-18

Base: `b59005dba9acaf6c575185876655bd6a5c792094`

Branch: `codex/reorg-r1e-batch-plan-2026-07-18`

Mode: planning and dependency audit only; no artifact mutation

## Candidate-universe rule

Before any candidate content is inspected, derive the universe mechanically from the fixed R1C
`research/_registry/MIGRATION_READINESS.tsv` rows classified exactly `MOVE_READY`, resolve each
fixed-base path through `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`, and exclude the already
migrated `simple_metric_S8_action_provenance_note.md`. The required result is exactly 119 unique
candidates. Generated R1E records cannot enter the universe.

`PREREGISTERED_CANDIDATE_UNIVERSE.tsv` freezes each candidate's original path, current path,
fixed-base owner, artifact type, Git blob, SHA-256, and proposed destination metadata. The candidate
list is the only population R1E may adjudicate.

## Bounded audit

After this preregistration is committed and pushed, candidate contents may be inspected only to
construct dependency closure from Python imports/shared modules, runtime opens/relative paths,
producer/output/consumer edges, Markdown links/literal paths, tests/globs, startup/frontier edges,
frozen-package/manifest references, and content-confirmed filename/stem relationships.

Every candidate must appear exactly once in one atomic family and one disposition:

- `SAFE_BYTE_IDENTICAL`
- `SAFE_WITH_PATH_POINTER_CHANGES`
- `BLOCKED_IMMUTABLE_COMPANION`
- `BLOCKED_RUNTIME_OR_MISSING_INPUT`
- `BLOCKED_TEST_SCOPE`
- `BLOCKED_FRONTIER_OR_CONTROL`
- `NEEDS_MANUAL_ADJUDICATION`

An import strongly connected component, producer/output pair, or runtime-dependent family may never
be split. Active-lane and legacy/archive candidates may never share a proposed batch. A closure larger
than 25 files is deferred rather than split merely to meet the preferred 5–25-file range.

## Safe-batch gates

A proposed safe batch must contain no immutable, manifest, frontier, or control artifact; have
complete inbound and outbound closure; have collision-free destinations; preserve scientific bytes
except for separately enumerated exact path-only edits; leave zero stale current-navigation pointers;
and preserve every frozen historical record.

R1E will independently audit the four standalone macro SymPy verifiers, coherent `cascade_*` legacy
script families, and remaining particle scripts. Particle scripts remain blocked unless their full
runtime/input/output closure is demonstrated.

## Required outputs and fail-closed checks

R1E must produce `COMPLETE_CANDIDATE_LEDGER.tsv`, `ATOMIC_FAMILY_GRAPH.json`, `BATCH_RANKING.tsv`, an
exact file/destination/pointer plan for at most three safest batches, an append-only
`MIGRATION_LEDGER.tsv` schema, and per-batch rollback/verification contracts.

The final verifier must reject a missing or duplicate candidate, a split dependency component, an
immutable companion, a destination collision, an unresolved runtime path, a stale current pointer,
and an active/legacy mixed batch. It must also replay all six frozen manifests, current links/frontier
checks, the full tests, and the original dirty checkout's 54-path metadata inventory without reading
dirty contents.

Maximum conclusion: ranked batch proposals only. No move, rename, copy, deletion, artifact content
edit, R1F migration, physics work, GPU work, canonization, or `grok` integration is authorized.

This is one organization-planning tile and covers none of the physics/solver completeness map.
