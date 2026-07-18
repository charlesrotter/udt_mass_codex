# Repository reorganization Phase R1B preregistration

- Date: 2026-07-18
- Base commit: `4b226472c8f7c22dfcdd2c328a109e92d1df5abd`
- Branch: `codex/reorg-r1b-2026-07-18`
- Cutoff: first commit date strictly before `2026-07-01`
- Question: which pre-cutoff tracked root Markdown records are explicitly
  superseded/import-era history and can move to `archive/pre_2026-07-01/`
  without changing active physics, executable behavior, evidence bytes, or a
  path required by an immutable source?

This document and its four input tables are committed before any candidate is
classified and before any candidate, live pointer, or evidence source is
mutated.

## Fixed base-derived universe

The complete adjudication universe is the 99 rows in
`PREREGISTERED_CANDIDATES.tsv` (SHA-256
`c00a8fcd2f612ddd5af23f8e7d13f97feb8a9d3915ec1f6a523a9098db09cf02`):
every tracked root path ending in `.md` at base `4b22647` whose rename-aware
oldest Git commit date is strictly before `2026-07-01`.

`BASE_ROOT_MARKDOWN.tsv` records all 440 base root Markdown paths so the 99-row
selection can be independently recomputed. Python, data, manifests, nested
R1A destinations, and post-cutoff-native Markdown are outside the universe by
construction. Generated R1B records do not exist in the fixed base tree and
must never feed candidate selection, eligibility, reference counts, or the
safety-stop totals.

The permanent-root registry contains 16 controls. The current-frontier
registry was extracted only from the top current span of `LIVE.md` and the
`HANDOFF.md` `CURRENT` block using the corrected R1A boundary matcher. It
contains 28 occurrences and four targets inside the 99-row universe. These
registries are exclusion/classification inputs, not archive outcomes.

## Classification contract

Every one of the 99 paths receives exactly one classification, using this
fail-closed precedence:

1. `PERMANENT_ROOT` — listed in `PERMANENT_ROOT_REGISTRY.tsv`; never moves.
2. `ACTIVE_CROSS_ERA` — a current LIVE/HANDOFF anchor, current lane/control
   dependency, or a pre-cutoff file whose post-cutoff content remains active;
   never moves in R1B.
3. `HARD_FROZEN` — formal frozen evidence or manifest-covered package content;
   neither bytes nor path move.
4. `HISTORICAL_SNAPSHOT` — a control/audit snapshot intentionally retained at
   its current path; it is excluded from live substitution counts.
5. `ARCHIVE_ELIGIBLE` — explicitly superseded/import-era historical material
   satisfying every move gate below.
6. `SOFT_EVIDENCE_PATH_ONLY` — evidence prose whose bytes are protected from
   prose editing but whose path tokens could be changed mechanically; retained
   unless it also has affirmative supersession evidence and passes every move
   gate.
7. `BLOCKED` — collision, runtime/dynamic/manifest/test role, unresolved source
   immutability, ambiguous supersession, or any other failed/uncertain gate.

The cutoff date alone is never affirmative supersession evidence. An
`ARCHIVE_ELIGIBLE` row must cite an exact base-tree statement marking the file
or its family superseded, archived, retired, pre-native/import-era, or
otherwise historical. A later replacement must be named where the base record
supplies one. Silence or a naming hunch fails closed.

## Inbound-source immutability registry

The entire tracked base repository is scanned, including nested archive
records, contracts, preregistrations, dispatches, tests, manifests, and every
reorganization snapshot. Each source containing a corrected-boundary reference
to any of the 99 candidates receives one registry class:

- `HARD_FROZEN_SOURCE`: six native-action package trees, their manifest-covered
  contents, and formally `FROZEN_EVIDENCE` sources. Never rewrite.
- `RUNTIME_OR_MANIFEST_IMMUTABLE`: Python, tests, executable/configuration
  paths, manifests, or sources with runtime/dynamic-path semantics. Never
  rewrite; a path requirement blocks the candidate.
- `HISTORICAL_SNAPSHOT_SOURCE`: `reorganization_r0/`, `reorganization_r1a/`,
  and this phase's generated audit records. Retain base-era path facts and
  exclude them from the operational census.
- `MUTABLE_NAVIGATION_SOURCE`: non-frozen control/navigation Markdown. Only an
  exact old-to-new path-token substitution is allowed.
- `SOFT_EVIDENCE_PATH_ONLY_SOURCE`: non-frozen research Markdown, including
  nested contracts, preregistrations, result records, and dispatches. Physics
  prose is immutable; only exact path-token substitution is allowed, with
  complete before/after hashes.
- `UNKNOWN_BLOCKING_SOURCE`: any source not proven to fit the above. It blocks
  relocation.

Every occurrence records target, source, line, column, source class, frozen
status, operational/forensic scope, and reference role. A hard-frozen source
blocks a move only when leaving it unchanged would require the target's present
root path. A reference inside a jointly moved family may remain unchanged only
when it resolves to a co-located destination after the move; this is recorded
explicitly and tested.

## Corrected matcher and independent comparison

The production scan imports the corrected R1A matcher at
`reorganization_r1a/correction_2026-07-18/reference_boundary.py`, frozen here
at SHA-256
`1a20d563c1aae476d56ade647262626acacd0838ea9adee918c446ec7679cb8d`.
Its catch-proofs require `file.md.` and `file.md)` to match and `file.md.bak`
not to match.

A separate implementation must run literal `git grep -F` target-by-target at
base `4b22647`, apply an independently coded boundary predicate, and agree on
every `(target, source, line, column)` key. Shared-code agreement is not
accepted as independence.

## Separate dependency censuses

Two counts and edge tables are always reported separately:

1. **Full forensic census:** all base tracked sources, including every
   `reorganization_r*/` record and historical audit table.
2. **Operational census:** the same scan with all sources under
   `reorganization_r0/`, `reorganization_r1a/`, and `reorganization_r1b/`
   excluded. It still includes ordinary `archive/` sources, contracts,
   preregistrations, code, tests, and manifests.

Generated R1B records may appear only in a post-move forensic audit; they may
not alter the frozen base counts, candidate outcomes, planned substitutions,
or safety stop.

## Archive-eligibility and mutation gates

A file may move only when every statement is mechanically or textually
supported:

1. it is `ARCHIVE_ELIGIBLE` with affirmative superseded/import-era evidence;
2. it has no runtime, Python import, test, manifest, startup-control, or
   unresolved dynamic/glob path role, inbound or outbound;
3. no unchanged hard-frozen source requires the root path;
4. every mutable-navigation or soft-evidence pointer admits a literal exact
   path-only substitution;
5. every unchanged internal reference still resolves correctly at the
   co-located destination;
6. `archive/pre_2026-07-01/<basename>` is absent from the base and worktree;
7. no Python, data, manifest, active post-July physics, or hard-frozen evidence
   is included in the move set.

If eligible, use `git mv`. Each move must be `R100` and preserve its Git blob,
size, and SHA-256 exactly. Outside generated R1B records, mutations are limited
to the moved Markdown paths and preregistered exact path substitutions in
non-frozen Markdown. Each edited source must equal its base bytes plus only the
enumerated substitutions and must carry before/after hashes. No physics prose
may change.

## Safety stop

After all 99 rows and all base references are frozen, but before any move or
pointer rewrite:

- if more than 40 files classify `ARCHIVE_ELIGIBLE`; or
- if more than 400 operational live pointer occurrences require substitution,

stop after adjudication, produce the complete family map and verification
return, commit/push those additions only, and perform no repository mutation.
The thresholds count exact files and exact occurrence rows, not families or
source documents.

## Verification and maximum conclusion

Before banking a mutation (if the safety stop remains green), independent
verification must establish:

1. exact 99-row candidate coverage with no generated-record influence;
2. corrected scanner/literal-Git exact agreement over the full base tree;
3. a complete, mutually exclusive source-immutability registry and separate
   forensic/operational counts;
4. every eligible row passes every gate and both safety totals are within
   bounds;
5. every move is `R100` with identical blob, size, and SHA-256;
6. every source edit is an enumerated exact substitution and no hard-frozen,
   runtime, manifest, Python, test, or physics prose changes;
7. zero stale non-frozen operational pointers after the move;
8. all six frozen package manifest hashes and complete package-state digests
   match base/R0;
9. `python3 -m pytest tests/` remains 69 passed, 1 xfailed, and the one known
   hygiene-header failure;
10. the original dirty workstation still exactly matches its 54-row
    status/`lstat` metadata inventory without reading its contents; and
11. the final diff contains no deletion, code/data move, active-lane migration,
    native-action continuation, GPU work, canonization, or R1C work.

Maximum conclusion: a bounded set of explicitly historical pre-cutoff Markdown
records was relocated without changing its bytes, the active research record,
runtime behavior, or frozen evidence. R1B makes no physics claim and grants no
authority for active-lane migration.
