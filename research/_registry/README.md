# Research registry semantics

`ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv` are fixed-base R1C audit snapshots. Their
`current_path` field names the path that existed at the R1C fixed base; it is not rewritten after a
later authorized migration. The R1C recommendation and verification records are likewise historical
evidence and remain unchanged.

Use `CURRENT_ARTIFACT_PATHS.tsv` for current navigation. It maps every one of the 1,114 original
fixed-base root paths to exactly one current path: 1,109 `ROOT_RETAINED`, one `MIGRATED_R1D`, and
four `MIGRATED_R1F`. The migrated rows identify the byte-identical S8 canary and behaviorally
verified R1F/B01 macro verifier quartet. The original path remains an identity key and does not
assert that the old path still exists. Use `MIGRATION_LEDGER.tsv` for the R1F migration commit,
rollback parent, blob, SHA-256, verification record, and rollback command.

The lane `ROOT_INVENTORY.tsv` files are navigation indexes, not new physics authorities. The S8 row
changed in R1D and the four verifier rows changed in R1F. R1E's B02/B03 entries remain proposals;
no further migration is authorized. Claim labels and frozen evidence remain governed by
[`LIVE.md`](../../LIVE.md), [`HANDOFF.md`](../../HANDOFF.md), and their cited evidence.
