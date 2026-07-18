# Research registry semantics

`ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv` are fixed-base R1C audit snapshots. Their
`current_path` field names the path that existed at the R1C fixed base; it is not rewritten after a
later authorized migration. The R1C recommendation and verification records are likewise historical
evidence and remain unchanged.

Use `CURRENT_ARTIFACT_PATHS.tsv` for current navigation. It maps every one of the 1,114 original
fixed-base root paths to exactly one current path. `ROOT_RETAINED` means the original and current
paths are identical. `MIGRATED_R1D` identifies the single byte-identical S8 canary move. The original
path remains an identity key and does not assert that the old path still exists.

The lane `ROOT_INVENTORY.tsv` files are navigation indexes, not new physics authorities. Only the S8
row of the macro inventory changed in R1D. Claim labels and frozen evidence remain governed by
[`LIVE.md`](../../LIVE.md), [`HANDOFF.md`](../../HANDOFF.md), and their cited evidence.
