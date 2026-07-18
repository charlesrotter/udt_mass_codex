# Phase R1C preregistration — lane ownership and navigation overlay

**Fixed base:** `07c67bfbe661705c6b936243fa1ed697f23c1644`

**Branch:** `codex/reorg-r1c-lane-index-2026-07-18`

**Mode:** additions-only navigation and organization metadata

## Authorized scope

R1C may add records only under `research/` and `reorganization_r1c/`. It may add one exact navigation link from root `README.md` to `research/README.md`, provided the existing startup-order paragraph remains byte-identical. It may not move, rename, duplicate, or delete a research artifact; alter physics prose or claim labels; move code or data; modify a manifest or frozen package; canonize; continue native-action work; or launch CPU/GPU research computation.

The complete tracked-root universe is frozen from the fixed Git tree in `FROZEN_ROOT_INVENTORY.tsv`. Generated R1C files are outside that universe and cannot affect selection, ownership, readiness, or ranking.

## Fixed classifications

Every frozen root path receives exactly one primary owner from:

- `CONTROL_ROOT`
- `FOUNDATIONS`
- `NATIVE_ACTION`
- `PARTICLE_MASS`
- `MACRO`
- `LEGACY_FROZEN`
- `CROSS_LANE_SHARED`
- `UNKNOWN_BLOCKED`

Secondary consumers are recorded separately and may contain zero or more lane labels. They never alter the single primary owner.

Every path receives exactly one migration-readiness value from:

- `RETAIN_ROOT`
- `IMMUTABLE_PATH`
- `MOVE_READY`
- `POINTER_MIGRATION_REQUIRED`
- `IMPORT_MIGRATION_REQUIRED`
- `MANIFEST_MIGRATION_REQUIRED`
- `BLOCKED`

## Evidence priority

Ownership and readiness are controlled, in order, by the topmost current blocks in `LIVE.md` and `HANDOFF.md`; `CANON.md`, `NEGATIVES_REGISTRY.md`, and the July-1 provenance firewall; all six frozen manifests and their package boundaries; the corrected R1A/R1B dependency censuses; current startup instructions and tests; then explicit content/status banners and commit provenance. Filename prefixes are candidate hints only and cannot decide a row.

No new physics judgment is authorized. Lane indexes may reproduce an existing label only verbatim and must name its source. Ambiguous evidence resolves to `UNKNOWN_BLOCKED` or a blocking readiness class rather than inference.

## Artifact and dependency fields

The ownership registry will record current path, artifact type, first/last commit dates, physics-status source, frozen/manifest status, runtime/import/test dependency summary, one primary owner, and secondary consumers. The readiness registry will preserve the same path key and give one readiness value plus the exact blocking dependency/pointer closure.

## Migration recommendation gate

R1C may recommend, but not execute, a first active-family migration. A recommendation must enumerate exact files, complete dependency closure, exact pointer/import changes, collision checks, frozen/manifest exclusions, rollback command, and verification gates. Ranking may use only the frozen evidence and generated mechanical registries; it cannot strengthen or reinterpret a physics claim.

## Fail-closed verification

The phase fails unless all of the following hold:

1. the frozen inventory exactly equals the root blobs at the fixed base;
2. ownership and readiness each contain exactly one row for every frozen root path and no other path;
3. every primary owner and readiness value belongs to its fixed vocabulary;
4. every generated link resolves, every current-frontier target is represented, and lane inventories point only to existing paths;
5. no fixed-base path changes except the authorized root README link;
6. all six frozen manifests replay and complete package states remain unchanged;
7. the full test suite matches the known baseline;
8. the original dirty checkout retains the same 54 status/lstat rows and its content remains `NOT_READ`;
9. independent catch-proofs reject a missing row, duplicate owner, bad lane, bad readiness, broken link, altered startup order, unauthorized modification, and manifest mutation.

R1C stops after commit and push, before R1D or any content migration.
