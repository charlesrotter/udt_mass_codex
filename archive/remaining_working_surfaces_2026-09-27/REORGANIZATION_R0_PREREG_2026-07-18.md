# Repository reorganization Phase R0 preregistration

Date: 2026-07-18
Base commit: `bfa0b9a9371fab0266315bc2bb6845b8a7446a18`
Branch: `codex/reorg-r0-2026-07-18`
Clean worktree: `/tmp/udt_mass_codex_r0_20260718`

## Authorized question and maximum conclusion

R0 asks only: what exists at the repository root at the fixed base snapshot,
what depends on it, what must remain at root, and what directory layout could be
audited in a later phase? R0 may add inventories, validators, navigation, and a
proposal. It may not delete, move, rename, rewrite history, alter physics,
change an existing tracked byte, touch the dirty workstation files, or execute
the proposed moves.

The maximum conclusion is a mechanically checked classification and a proposed
move plan. No file is approved to move merely because R0 calls it a candidate.

## Snapshot boundary

The root inventory covers every tracked path with no `/` in the tree of
`bfa0b9a`. R0 output files are necessarily outside that closed input census;
including the inventory in its own hash ledger would be self-referential. The
final audit must separately list every R0-added path and prove that the diff
from `bfa0b9a` contains additions only.

Each base root row must include:

- path;
- Git blob object ID;
- SHA-256 of the exact base blob;
- byte size;
- last commit hash, date, and subject at or before the base;
- inbound reference count and referencing paths;
- dependency/reference kinds; and
- exactly one R0 classification with a short basis.

## Classification rules frozen before the census

- `CONTROL`: startup, governance, canonical authority, repository configuration,
  dependency lock, or control-plane file whose location or role is operational.
- `ACTIVE`: part of a currently live lane, current solver/verification path, or
  current accepted research record named by the startup frontier.
- `FROZEN_EVIDENCE`: immutable return, manifest, transcript, evidence ledger, or
  historical record whose evidentiary path must be preserved byte-for-byte.
- `ARCHIVE_CANDIDATE`: apparently historical or superseded, with no current
  executable/startup requirement found. This is a proposal flag, never an R0
  action or deletion recommendation.
- `MOVE_CANDIDATE`: active or reusable material that appears suitable for a
  later directory move only after every recorded dependency is rewritten and
  audited.
- `UNKNOWN/BLOCKED`: evidence is insufficient, binary/opaque, or conflicting;
  later human adjudication is required before any move.

Precedence for automated classification is conservative:

1. explicitly required root/control files -> `CONTROL`;
2. paths inside the immutable evidence ledger or explicitly frozen records ->
   `FROZEN_EVIDENCE`;
3. current startup/frontier and live solver references -> `ACTIVE`;
4. clear historical/superseded markers with no live executable edge ->
   `ARCHIVE_CANDIDATE`;
5. cohesive reusable families with resolved dependencies -> `MOVE_CANDIDATE`;
6. everything else -> `UNKNOWN/BLOCKED`.

The required root-retention floor is:

```text
LIVE.md
HANDOFF.md
INDEX.md
AGENTS.md
CLAUDE.md
CANON.md
MEMORY.md
README.md
```

R0 may identify additional root-retention requirements but may not weaken this
floor.

## Dependency-map coverage

The dependency inventory must cover, at minimum:

1. Python imports, with internal targets resolved where static resolution is
   possible and external/unresolved imports labeled;
2. literal file-opening and path-construction calls, with dynamic expressions
   surfaced rather than guessed;
3. Markdown inline links and wiki links;
4. SHA-256 manifests and recognizable JSON artifact manifests;
5. tests, including their imports and literal repository paths; and
6. startup instructions/references in `AGENTS.md`, `LIVE.md`, `HANDOFF.md`,
   `INDEX.md`, `MEMORY.md`, and `CLAUDE.md`.

Every edge must carry source path, line when available, edge kind, raw target,
resolved target where possible, and resolution status. The map is a static
repository scan, not a proof that dynamic runtime path construction is
exhausted. Dynamic/ambiguous edges must remain visible as `DYNAMIC` or
`UNRESOLVED`.

## Dirty-workstation firewall

The original checkout `/home/udt-admin/udt_mass_codex` is out of mutation
scope. Its dirty and untracked inventory may use Git status plus filesystem
metadata (`lstat`) only. R0 must not open or hash those file contents, stage
them, move them, modify them, or create a file in that checkout. The inventory
will record path, Git status, tracked/untracked kind, filesystem object type,
and reported size; content hashes are deliberately `NOT_READ`.

## Frozen-evidence gates

All paths tracked at `bfa0b9a` must remain byte-identical. The final diff gate
is additions-only. The six current native-action package manifests are explicit
anchors:

| Package | Expected manifest SHA-256 |
|---|---|
| Stage-I A | `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19` |
| Stage-I B | `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92` |
| Stage-II A | `ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a` |
| Stage-II B | `30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45` |
| Arm C | `99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f` |
| Final adjudication | `57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33` |

Before and after R0, each internal manifest must pass and the complete base-tree
path-to-blob map must be identical.

## Verification and test gates

Before banking R0:

1. a fail-closed validator must recompute the base root path set and require
   exact one-row coverage with valid classifications;
2. it must verify blob OIDs, SHA-256 values, sizes, last-commit fields, and
   reference counts against independent recomputation;
3. it must require all six dependency categories and surface unresolved/dynamic
   counts rather than suppress them;
4. catch-proof fixtures must show that a missing root row, duplicate row, bad
   SHA-256, forbidden classification, missing dependency category, or modified
   base path is rejected;
5. the full existing `python3 -m pytest tests/` baseline must be recorded; the
   preregistered expected state is 69 passed, 1 xfailed, and the known
   hygiene-header documentation failure; and
6. the final Git diff from `bfa0b9a` must contain additions only.

Because this is a mechanical topology census rather than a physics verdict,
the independent layer is a separate fail-closed implementation and catch-proof
run. It verifies repository facts; classifications remain an auditable R0
proposal and `UNKNOWN/BLOCKED` is preferred over invented certainty.
