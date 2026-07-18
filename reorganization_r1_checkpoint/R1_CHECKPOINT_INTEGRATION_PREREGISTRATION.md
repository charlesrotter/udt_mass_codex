# R1 checkpoint integration preregistration

Date: 2026-07-18

Branch: `codex/reorg-r1-checkpoint-integration-2026-07-18`

Source tip: `b4e839c31583f1b220eabc390f235fb794578af9`

Required pre-integration `origin/grok`: `bfa0b9a9371fab0266315bc2bb6845b8a7446a18`

## Precondition

After a fresh `git fetch origin grok`, `origin/grok` must equal the required hash and must be an
ancestor of the source tip. The observed merge base must equal the required hash. Any advance or
divergence stops the integration before control-file mutation. The observed source contains 20
commits beyond the required `grok` hash.

## Bounded mutation

The final checkpoint may edit only these five existing operational controls:

- `LIVE.md`
- `HANDOFF.md`
- `INDEX.md`
- `README.md`
- `AGENTS.md`

It may add records only under `reorganization_r1_checkpoint/`. No equation, physics label,
scientific verdict, `CANON.md`, evidence, script, data, manifest, research artifact, fixed historical
inventory, or R0–R1D verification record may change.

The five edits are limited to recording that R0–R1D is complete; that fixed historical inventories
remain immutable; that current locations come from
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; that one active artifact moved byte-identically; and
that no further migration is authorized. Stale “reorganization not launched” wording in LIVE,
HANDOFF, and INDEX must be removed or explicitly superseded without changing their scientific status
language.

## Preregistered verification gates

Before banking the final integration commit:

1. the diff from the source tip contains only the five controls and checkpoint records;
2. all non-authorized source-tip paths, including every R0–R1D fixed record, remain unchanged;
3. `CURRENT_ARTIFACT_PATHS.tsv` still has 1,114 unique original paths and 1,114 unique current paths,
   with 1,113 `ROOT_RETAINED`, one `MIGRATED_R1D`, and every current path existing;
4. the S8 artifact remains at its R1D destination with Git blob
   `94b494cd326a27aacbbbedbd9aa91febb8acf471` and SHA-256
   `a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9`;
5. all Markdown links in the changed controls and current research/checkpoint navigation resolve;
6. all 306 frozen frontier rows and 101 unique targets resolve;
7. all six frozen package manifests replay, and their complete tracked path sets remain identical to
   the source tip;
8. the full CPU tests retain the known 69 passed, one known hygiene failure, one xfailed baseline;
9. the original checkout still has exactly the frozen 54-path status/lstat metadata inventory, with
   content never read;
10. catch-proofs reject an unauthorized file edit, stale reorganization wording, a missing current
    path, a broken link, a manifest mutation, and a dirty-metadata mismatch.

After the final integration branch is pushed, `grok` may advance only by a normal non-force
fast-forward push from its required pre-hash to the verified integration tip. Remote `grok` must then
equal that tip. Stop before R1E, another migration, physics work, or GPU work.

This checkpoint is one organization/control tile. It covers navigation truth and integration state;
it covers none of the ten physics/solver completeness criteria and makes no scientific claim.
