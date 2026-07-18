# Repository reorganization Phase R0 audit report

- Date: 2026-07-18
- Base: `bfa0b9a9371fab0266315bc2bb6845b8a7446a18`
- Branch: `codex/reorg-r0-2026-07-18`
- Scope: additions-only inventory and navigation proposal

## Outcome

R0 accounts for every tracked root file at the fixed base, maps static
dependencies, records the dirty workstation by metadata only, and proposes a
future directory layout. It executes no move, rename, deletion, physics edit,
history rewrite, or frozen-evidence mutation. Classification is a review queue,
not an authorization to reorganize any base path.

The base tree contains 3,335 tracked paths and 1,131 tracked root files. The
SHA-256 of its sorted path-to-Git-object map is
`21acc5aca8575dad3f381660bd99fe462f8cbbbdae470328b4f916c7b2f37eff`.

## Root census

| Classification | Files |
|---|---:|
| `CONTROL` | 18 |
| `ACTIVE` | 188 |
| `FROZEN_EVIDENCE` | 433 |
| `ARCHIVE_CANDIDATE` | 26 |
| `MOVE_CANDIDATE` | 429 |
| `UNKNOWN/BLOCKED` | 37 |
| **Total** | **1,131** |

`ROOT_FILE_INVENTORY.tsv` contains, for each row, the path, Git mode and blob
object ID, SHA-256, byte size, last commit/date/subject, exact inbound reference
count and sources, dependency kinds, classification, and classification basis.
The 37 opaque or insufficiently resolved files remain `UNKNOWN/BLOCKED`; the
scan does not invent roles for them.

## Dependency census

| Edge category | Edges |
|---|---:|
| Python imports | 6,582 |
| Literal/dynamic file paths | 1,404 |
| Markdown links | 315 |
| Manifests | 1,135 |
| Tests | 161 |
| Startup instructions | 399 |
| Exact root-name text references | 4,869 |
| **Total** | **14,865** |

The map retains 1,438 dynamic or unresolved edges for later audit rather than
guessing their runtime targets. Static imports do not prove runtime execution;
missing paths may be generated outputs; basename resolutions must be normalized
before relocation. `DEPENDENCY_MAP.tsv` is the complete edge table and
`DEPENDENCY_SUMMARY.md` provides the status matrix and representative audit
queue.

## Root retention

R0 proposes 15 permanent root paths: the user-required navigation floor plus
repository configuration, core ledgers, provenance, problem statement, and
test configuration. Four governance files stay at root pending an explicit
control-path migration. The static scan also pins 141 root files until their
startup/frontier references are migrated and 46 root Python files until their
imports are migrated. Overlap is collapsed in the 206-row `ROOT_RETENTION.tsv`.

The permanent root set includes `LIVE.md`, `HANDOFF.md`, `INDEX.md`, `AGENTS.md`,
`CLAUDE.md`, `CANON.md`, `MEMORY.md`, and the new `README.md`. The proposed tree
does not weaken that floor.

## Dirty-workstation firewall

The original checkout was not used as the R0 worktree. Its pre-existing status
contains 54 paths: 3 tracked modifications and 51 untracked paths. The separate
inventory was built only from `git status` and filesystem `lstat` metadata.
Every content-hash field says `NOT_READ`; no dirty or untracked content was
opened, hashed, modified, moved, staged, or copied into R0.

## Frozen evidence

The six preregistered native-action package manifest hashes match their expected
values, and all six internal manifests pass:

| Package | Manifest SHA-256 | Internal check |
|---|---|---|
| Stage-I A | `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19` | PASS |
| Stage-I B | `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92` | PASS |
| Stage-II A | `ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a` | PASS |
| Stage-II B | `30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45` | PASS |
| Arm C | `99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f` | PASS |
| Final adjudication | `57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33` | PASS |

Because the final Git gate requires an additions-only diff from the base, every
pre-existing tracked file—including all frozen packages and historical
records—remains byte-identical.

## Existing test baseline

The exact command `python3 -m pytest tests/` collected 71 tests:

- 69 passed;
- 1 xfailed as already marked; and
- 1 failed:
  `tests/test_hygiene_header.py::test_covered_results_have_hygiene_header`.

The failure is the preregistered, existing documentation hygiene-header gap;
R0 does not modify the affected records. Full output is preserved in
`TEST_BASELINE.txt`, with a machine-readable summary in `TEST_BASELINE.json`.

## Verification gates

`verify_r0_inventory.py` independently recomputes and checks the base root set,
Git object IDs, SHA-256 values, sizes, last-commit fields, exact root references,
dependency-category coverage, dirty metadata firewall, frozen manifests,
additions-only diff, and test baseline. Its catch-proof suite confirms rejection
of a missing row, duplicate row, bad SHA-256, invalid classification, missing
dependency category, and modified base path.

This is independent mechanical verification of repository facts, not an
independent scientific judgment. Semantic classifications remain proposals;
uncertainty is retained explicitly in `UNKNOWN/BLOCKED` and in the dynamic edge
queue.

## Audit stop

The next phase, if separately authorized, should adjudicate candidate families
and their unresolved edges before proposing an atomic migration plan. R0 stops
here: no proposed tree operation has been executed.
