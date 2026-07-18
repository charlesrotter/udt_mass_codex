# R1F checkpoint integration preregistration

Date: 2026-07-18

Branch: `codex/reorg-r1f-checkpoint-integration-2026-07-18`

Source tip: `3bb88a6b6cfc223d308b8bae6e27d69b1a1b119f`

Required pre-integration `origin/grok`: `b59005dba9acaf6c575185876655bd6a5c792094`

## Precondition

After this preregistration is committed, a fresh `git fetch origin grok` must leave `origin/grok`
exactly at the required pre-integration hash. That hash must be an ancestor of the source tip and
the observed merge base must equal it. Any advance or divergence stops the integration before an
operational navigation file is changed.

## Bounded mutation

The integration may edit only these six existing navigation/control files:

- `LIVE.md`
- `HANDOFF.md`
- `INDEX.md`
- `README.md`
- `research/README.md`
- `research/_registry/README.md`

It may add audit and verification records only under `reorganization_r1f_checkpoint/`. It may not
alter scientific prose, equations, status labels, verdicts, `CANON.md`, evidence, scripts, data,
manifests, research artifacts, migration registries, or R0–R1F historical and planning records.

The six edits are limited to recording that R1E planning and R1F/B01 are complete; that B01 was
behaviorally verified; that five active artifacts have moved byte-identically (the R1D note and four
R1F verifiers); that current paths come from `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; that
migration provenance comes from `research/_registry/MIGRATION_LEDGER.tsv`; and that B02/B03 remain
proposals with no further migration authorized.

## Preregistered verification gates

Before banking the integration commit:

1. the diff from the source tip contains only the six controls and new checkpoint records;
2. every non-authorized source-tip path, including all R0–R1F fixed records, remains unchanged;
3. `CURRENT_ARTIFACT_PATHS.tsv` has exactly 1,109 `ROOT_RETAINED`, one `MIGRATED_R1D`, four
   `MIGRATED_R1F`, and 1,114 unique original/current paths, each with one existing current path;
4. all four R1F scripts retain their registered blobs and SHA-256 values and appear as R100 renames
   in migration commit `c4cf405bba49625a9352a022b60754e7249c27f9`;
5. all four post-move replay exit codes and raw stdout/stderr hashes exactly match the pre-move
   records;
6. `MIGRATION_LEDGER.tsv` has exactly four R1F rows naming migration commit `c4cf405...` and its
   real first parent `fa211047...`; the ledger must not exist in the named migration commit;
7. all Markdown links in current navigation/checkpoint records and all current frontier targets
   resolve;
8. all six frozen package manifests replay and their complete tracked package states match the
   source tip;
9. the full CPU tests retain the known baseline of 69 passed, one known hygiene failure, and one
   xfailed;
10. the original checkout retains the frozen 54-path status/lstat metadata inventory without its
    dirty file contents being read;
11. catch-proofs reject an unexpected `origin/grok`, an unauthorized edit, a current-map mismatch,
    a behavioral hash mismatch, a non-R100 move, an invalid ledger commit/parent, a broken link, a
    manifest mutation, and dirty-metadata drift.

After the verified integration branch is pushed, `grok` may advance only by a normal non-force
fast-forward push from the required pre-hash to the verified integration tip. Remote `grok` must
then equal that tip.

This is an organization/navigation checkpoint only. It authorizes no B02/B03 migration, physics
work, canonization, GPU work, or change to scientific content.
