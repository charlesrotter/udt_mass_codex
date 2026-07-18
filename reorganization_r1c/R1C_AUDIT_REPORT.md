# Phase R1C lane ownership and navigation audit

## Outcome

R1C is an additions-only organization overlay based on `07c67bfbe661705c6b936243fa1ed697f23c1644`. It moves, renames, copies, and deletes zero research artifacts. The only existing-path edit is one link in root `README.md`; the startup-order paragraph remains byte-identical.

The preregistered root universe contains 1,114 unique tracked blobs. [`ROOT_OWNERSHIP.tsv`](../research/_registry/ROOT_OWNERSHIP.tsv) and [`MIGRATION_READINESS.tsv`](../research/_registry/MIGRATION_READINESS.tsv) each contain exactly one row for every frozen path and no extra path.

## Primary ownership

| Owner | Files |
|---|---:|
| `CONTROL_ROOT` | 23 |
| `FOUNDATIONS` | 12 |
| `NATIVE_ACTION` | 27 |
| `PARTICLE_MASS` | 138 |
| `MACRO` | 270 |
| `LEGACY_FROZEN` | 625 |
| `CROSS_LANE_SHARED` | 15 |
| `UNKNOWN_BLOCKED` | 4 |

The four `UNKNOWN_BLOCKED` paths are the two provenance screenshots and two opaque radial `.out` records already classified `UNKNOWN/BLOCKED` by R0. No content-based ownership was inferred for them.

## Migration readiness

| Readiness | Files |
|---|---:|
| `RETAIN_ROOT` | 38 |
| `IMMUTABLE_PATH` | 418 |
| `MOVE_READY` | 120 |
| `POINTER_MIGRATION_REQUIRED` | 388 |
| `IMPORT_MIGRATION_REQUIRED` | 49 |
| `MANIFEST_MIGRATION_REQUIRED` | 3 |
| `BLOCKED` | 98 |

These are dependency gates, not move authority. R1C executes none of them.

## Navigation and recommendation

The [research index](../research/README.md) and four lane READMEs point to existing paths. Claim labels are reproduced from `LIVE.md`, `HANDOFF.md`, `CANON.md`, and the accepted final status ledger without re-adjudication.

The [ranked future-migration recommendation](../research/_registry/FIRST_ACTIVE_FAMILY_MIGRATION_RECOMMENDATION.md) selects the two-file GR→UDT selector-audit pair as the smallest bounded active family. It records the exact file set, five current inbound substitutions, post-move relative-path qualifications, absence of import/test/data/manifest changes, and rollback/verification gates. The migration is not executed.

## Verification

- 1,114 unique frozen paths, ownership rows, and readiness rows: pass.
- Four lane inventories exactly reproduce primary and secondary relationships: pass.
- 54 generated Markdown links: pass.
- 306 current-frontier reference rows and 101 unique targets: pass.
- Six frozen manifests and complete frozen package states: pass.
- Full tests: 69 passed, 1 known hygiene-header failure, 1 xfailed—the established baseline.
- Original dirty checkout: 54 status/lstat rows unchanged; content remains `NOT_READ`.
- Catch-proofs for missing/duplicate rows, invalid owner/readiness, broken link, startup-order mutation, unauthorized edit, and manifest mutation: pass.

Machine result: [`VERIFY_RESULT.json`](../research/_registry/VERIFY_RESULT.json).

R1C stops here before R1D or any content migration.
