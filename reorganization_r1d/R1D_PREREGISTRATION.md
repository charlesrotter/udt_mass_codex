# R1D S8 byte-identical canary preregistration

Date: 2026-07-18  
Base: `b3c50109df90658378d157c65fc723b1265c48c8`  
Branch: `codex/reorg-r1d-s8-canary-2026-07-18`

## Bounded action

R1D may migrate exactly one research artifact, using `git mv`:

`simple_metric_S8_action_provenance_note.md`
→ `research/macro/simple_metric_S8_action_provenance_note.md`

The artifact must remain byte-identical: Git blob
`94b494cd326a27aacbbbedbd9aa91febb8acf471` and SHA-256
`a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9`.
No other research artifact may move, be copied, be deleted, or be edited.

## R1C refinement frozen before mutation

Line 10's code-span token `simple_metric_solution_space_ZOOM.md` is repository-root
informational provenance. It is neither a Markdown link nor a runtime-relative file open. R1D
will preserve that token and the complete artifact unchanged; it will not substitute a `../../`
path.

## Fixed-history/current-navigation contract

Every tracked file already present at the base under `reorganization_r0/`,
`reorganization_r1a/`, `reorganization_r1b/`, or `reorganization_r1c/`, and every existing base
file under `research/_registry/`, is fixed history. `FIXED_HISTORY_SHA256.tsv` freezes each byte
sequence. R1D may add new records but may not modify any frozen record.

R1D will add `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`, one row for each of the 1,114 paths
in `reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv`. Exactly 1,113 rows will be
`ROOT_RETAINED`; the S8 row will be `MIGRATED_R1D`. Original paths remain the fixed-base identity;
current paths are the live navigation identity. Each row must resolve to exactly one existing path,
each current path must be unique, and every current byte sequence must match its fixed-base blob.

Only these existing navigation records may change:

- `research/README.md`;
- the S8 row, and only that row, in `research/macro/ROOT_INVENTORY.tsv`.

R1D may add `research/_registry/README.md`, the current-path table, and records under
`reorganization_r1d/`. Historical old-path occurrences in fixed R0–R1C records remain valid;
current-navigation records must contain no stale old-path pointer except the explicit
`original_path` identity column of the new map.

## Preregistered gates

The final verifier must require: an R100 rename; exact blob and SHA-256 identity; old path absent;
new path present; no duplicate copy; 1,114 mapped originals with 1,113/1 status counts; no duplicate
ownership; preserved fixed-history hashes; the unchanged informational token; zero stale current
navigation pointers; all Markdown links and current-frontier targets resolving; all six frozen
manifests passing; the known 69-passed/1-failed/1-xfailed test baseline; and the original dirty
checkout's 54-path metadata inventory remaining identical. Catch-proofs must make the verifier reject
artifact mutation, duplicate/missing current paths, fixed-history mutation, stale navigation, and
the forbidden token substitution.

This is one organization tile. It covers current path navigation for the fixed R1C root universe and
drops all further migrations and every physics/solver question. No R1E, physics work, carrier work,
GPU work, canonization, or repository reorganization beyond this canary is authorized.
