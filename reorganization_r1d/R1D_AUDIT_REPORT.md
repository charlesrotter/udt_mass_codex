# R1D S8 byte-identical canary audit

Date: 2026-07-18

Base: `b3c50109df90658378d157c65fc723b1265c48c8`

Preregistration commit: `9f6bdb4`

## Outcome

R1D migrated exactly one artifact with `git mv`:

`simple_metric_S8_action_provenance_note.md`
→ `research/macro/simple_metric_S8_action_provenance_note.md`

Git reports `R100`. The destination is byte-identical to the source at the fixed base:

- Git blob: `94b494cd326a27aacbbbedbd9aa91febb8acf471`
- SHA-256: `a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9`
- old path: absent
- new path: present
- tracked paths with that blob: one, the destination
- duplicate copies: zero

The artifact's line-10 token `simple_metric_solution_space_ZOOM.md` remains byte-for-byte unchanged.
It is a repository-root informational token in a code span, not a Markdown link or runtime-relative
file open. No `../../` substitution was made.

## Fixed history and current navigation

All 150 existing R0/R1A/R1B/R1C and R1C-registry records frozen by R1D remain unchanged. The new
`CURRENT_ARTIFACT_PATHS.tsv` has exactly 1,114 data rows, 1,114 unique original paths, and 1,114
unique current paths:

- `ROOT_RETAINED`: 1,113
- `MIGRATED_R1D`: 1

Every mapped current path exists. The original-path column remains the fixed-base identity, while
the current-path column is navigation. `ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv` remain
fixed R1C snapshots. Only the S8 row changed in `research/macro/ROOT_INVENTORY.tsv`; it now points to
the destination. Historical old-path occurrences are explicitly classified in
`OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv`; the current-navigation stale-pointer count is zero.

## Verification

The independent fail-closed verifier records its full machine-readable return in
`VERIFY_RESULT.json`. It checks the R100 rename and exact artifact hashes, all 1,114 current-path
mappings, fixed-history bytes, current navigation, Markdown links, 306 current-frontier rows with
101 unique targets, the complete tracked state and SHA-256 manifest of all six frozen packages, and
the untouched original checkout's 54 metadata-only dirty paths. Catch-proofs reject a missing map
row, duplicate current path, artifact-hash mutation, fixed-history mutation, stale current pointer,
and the forbidden `../../` token substitution.

The CPU-only full test run remains at the known baseline: 69 passed, one known hygiene-header
failure, and one xfailed. No physics prose, claim label, frozen evidence, solver, data, manifest, or
unrelated research artifact changed.

## Scope boundary

This is one organization tile: current-path semantics plus one byte-identical canary. It does not
cover another migration, R1E, physics work, carrier assumptions, GPU work, canonization, deletion,
or broader repository reorganization. Work stops here after the final commit and push.
