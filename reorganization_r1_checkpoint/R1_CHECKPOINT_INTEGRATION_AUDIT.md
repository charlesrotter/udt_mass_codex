# R1 checkpoint integration audit

Date: 2026-07-18

Source tip: `b4e839c31583f1b220eabc390f235fb794578af9`

Pre-integration `origin/grok`: `bfa0b9a9371fab0266315bc2bb6845b8a7446a18`

## Outcome

The R0–R1D reorganization checkpoint is integrated on the checkpoint branch. The operational
controls now state that fixed historical inventories remain immutable, current locations come from
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`, R1D migrated exactly one active artifact
byte-identically, and no further migration is authorized.

Exactly five existing control files changed:

- `AGENTS.md`
- `HANDOFF.md`
- `INDEX.md`
- `LIVE.md`
- `README.md`

The old “repository reorganization not launched” state is explicitly superseded in `LIVE.md`; the
corresponding HANDOFF and INDEX stop language now blocks *further migration* rather than denying the
completed checkpoint. The existing scientific labels, equations, verdicts, and authority ordering
are unchanged. `AGENTS.md` continues to defer to `LIVE.md`.

## Verification

The external fail-closed return is recorded in `VERIFY_RESULT.json`:

- source/ancestry gate: `origin/grok` was freshly fetched at the exact required hash and was the
  source tip's ancestor and merge base;
- scope gate: only the five controls above changed; all other additions are checkpoint records;
- fixed history: 150 frozen R0–R1D records match their preregistered SHA-256 values;
- current navigation: 1,114 unique original paths map to 1,114 unique existing current paths, with
  1,113 `ROOT_RETAINED` and one `MIGRATED_R1D`;
- S8 canary: Git blob `94b494cd326a27aacbbbedbd9aa91febb8acf471`, SHA-256
  `a3fae1798f64c4bdc3a79692a618281c407d162309073a02dc72d89eb9c554f9`;
- navigation: 62 Markdown links and all 306 frontier rows / 101 unique targets resolve;
- frozen evidence: all six SHA-256 manifests replay and all 133 tracked package paths are
  byte-identical to the source tip;
- tests: 69 passed, one known hygiene-header failure, one xfailed;
- original checkout: exactly 54 dirty paths match frozen status/lstat metadata; content remained
  `NOT_READ`.

Catch-proofs reject an unauthorized control edit, stale reorganization wording, a missing current
path, a broken link, a mutated manifest, and dirty-metadata drift.

## Scope boundary

This is one operational integration tile and covers none of the physics/solver completeness map.
No R1E, batch migration, physics work, GPU work, canonization, deletion, history rewrite, or further
artifact movement is authorized. After a clean final verification, the branch may be pushed and
`grok` may be advanced only by a normal non-force fast-forward push; then work stops.
