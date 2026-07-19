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

Use `CURRENT_CLASSIFICATION.tsv` as the authoritative current classification overlay. It joins all
1,114 stable identities to current paths without rewriting the fixed R1C snapshots. Its exact R1G
override union is 134 rows (121 affected cascade rows plus 32 B02/B03 rows with 19 overlapping);
the other 980 rows are explicitly `INHERITED_UNREVIEWED`, not newly adjudicated. R1H adds
scientific-family closure only for the 32 B02/B03 candidates. All 32 are
`BLOCKED_IMMUTABLE_FAMILY_COMPANION`, so B02 and B03 are withdrawn as execution batches. This branch
authorizes no migration or fixed-snapshot rewrite.

`migration_review_status` is a separate axis from provenance `review_status`. The post-correction
registry has 101 `FAMILY_REVIEW_REQUIRED` rows at
`BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED`, 32 `FAMILY_REVIEWED_BLOCKED` rows, one
`IMMUTABLE_PATH` row, and 980 `INHERITED_UNREVIEWED` rows. The 101 rows have incorporated the R1G
provenance correction but have not received scientific-family migration review; none is move-ready.
No row retains the obsolete `BLOCKED_PROVENANCE_CORRECTION_REQUIRED` state.

The lane `ROOT_INVENTORY.tsv` files are navigation indexes, not new physics authorities. The S8 row
changed in R1D and the four verifier rows changed in R1F.

The R1G provenance audit and readout correction are complete. The prefix-based pre-native
classification was false: the affected cascade set is 121 `NATIVE_2026-07-01` and zero `MIXED`;
B02/B03 contain 29 `NATIVE_2026-07-01`, two `MIXED`, and one `OPEN`. GR/Einstein/Misner–Sharp
reference-only readouts do not demote native operator provenance. `phi_source_derivation.py` and
`homog_alpha_test.py` remain `MIXED` because alpha enters the action/EOM. The old B02/B03
`archive/pre_2026-07-01/` destinations are withdrawn. For affected paths,
[`reorganization_r1g/`](../../reorganization_r1g/R1G_READOUT_PROVENANCE_CORRECTION_REPORT.md) supersedes the
corresponding classifications in `ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv` until a
separately authorized correction is applied. No B02/B03 or further migration is authorized.
Claim labels and frozen evidence remain governed by [`LIVE.md`](../../LIVE.md),
[`HANDOFF.md`](../../HANDOFF.md), and their cited evidence.
