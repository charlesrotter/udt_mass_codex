# Repository reorganization Phase R1A preregistration

- Date: 2026-07-18
- Base commit: `4c98e32d7b8af0dc3159706d18006d673566d721`
- Branch: `codex/reorg-r1a-2026-07-18`
- Question: which of the 26 R0 `ARCHIVE_CANDIDATE` files can be relocated
  without changing evidence, runtime behavior, or frozen history, and what
  blocks each of the other 26 candidates and 37 `UNKNOWN/BLOCKED` files?

## Authorized scope and maximum conclusion

R1A may correct the root `README.md` startup order, supersede the generic R0
layout with a research-lane-first proposal, inventory and adjudicate all 63 R0
review-queue files, and execute one conservative archive batch with `git mv`.
It may update exact non-frozen live pointers to moved files in the same commit.

R1A may not delete, edit physics, move active files or Python modules, move
opaque data, alter frozen evidence or manifests, rewrite history, canonize, or
begin R1B. A candidate classification is not itself move authority.

## Fixed input set

The adjudication set is exactly the 26 `ARCHIVE_CANDIDATE` and 37
`UNKNOWN/BLOCKED` root paths in
`reorganization_r0/ROOT_FILE_INVENTORY.tsv`. Every path gets one disposition
row, and every inbound reference gets one reference row stating its source,
edge type, resolution status, whether the source is frozen, and whether a
pointer rewrite is required.

## Frozen source and pointer rules

A reference source is `FROZEN` when it is classified `FROZEN_EVIDENCE` in the
R0 root inventory, lies inside one of the six native-action frozen packages,
or is covered by one of their internal manifests. A frozen source is never
rewritten.

The R0 census and audit artifacts are historical snapshots. They retain their
base-era paths and are labeled `HISTORICAL_SNAPSHOT`, not live pointers. Other
references are classified as live pointer, descriptive mention, runtime edge,
manifest edge, or startup/test edge. Every exact non-frozen live pointer to a
moved path must be rewritten atomically with the move; descriptive prose is
rewritten only when it functions as navigation.

## Archive eligibility predicate

A path is eligible for the first batch only if every condition is true:

1. R0 classified it `ARCHIVE_CANDIDATE`; no `UNKNOWN/BLOCKED` path is eligible.
2. It is a text research record whose historical subject predates 2026-07-01;
   it is not Python, a manifest, opaque data, an image, a model, or executable.
3. It has no inbound or outbound `PYTHON_IMPORT`, runtime `FILE_PATH`, `TEST`,
   `STARTUP`, or `MANIFEST` dependency.
4. It has no inbound reference from a frozen source.
5. It is not an exact or glob match for any unresolved `DYNAMIC`,
   `DYNAMIC_OR_GLOB`, `AMBIGUOUS_BASENAME`, or `MISSING_OR_GENERATED` edge.
6. Every remaining inbound live pointer is in a non-frozen text source and can
   be rewritten as an exact old-to-new path substitution.
7. Its destination is exactly `archive/pre_2026-07-01/<old-root-path>` and does
   not collide with an existing path.

Any uncertainty fails closed to `RETAIN` with a concrete blocker. The complete
eligible set is fixed by the first run of the adjudicator; it will not be
expanded after moves or tests are seen.

## Mutation and hash contract

- Create the archive directory without deleting or normalizing content.
- Use `git mv` for each eligible path.
- Record old path, new path, Git blob ID, pre-move SHA-256, post-move SHA-256,
  and rewritten pointer sources.
- Require identical blob IDs and SHA-256 values across every move.
- Restrict edits outside new R1A records to `README.md`, the eligible pointer
  sources, and path-only substitutions. No frozen or manifest source may be
  edited.
- Preserve the original dirty checkout using Git status plus `lstat` metadata
  only; never open, hash, stage, move, or modify its dirty/untracked content.

## Verification gates

Before banking R1A:

1. exactly 63 disposition rows and exact candidate-set coverage;
2. complete independently recomputed inbound-reference coverage, with every
   source carrying a frozen/non-frozen decision;
3. no moved path violates any eligibility condition;
4. every moved blob and SHA-256 is identical before/after;
5. every non-frozen live pointer is rewritten and no frozen source changed;
6. all six frozen package manifests and complete package-state checks pass;
7. the post-move dependency census exposes all unresolved/dynamic edges and no
   resolved dependency remains pointed at an old moved path;
8. `python3 -m pytest tests/` is no worse than the R0 baseline of 69 passed,
   1 xfailed, and the one known hygiene-header failure; and
9. the diff from `4c98e32` contains only authorized additions, `git mv` pairs,
   the README correction, and exact non-frozen pointer substitutions.

The verifier is mechanical and adversarial: it must reject missing/duplicate
adjudication rows, an omitted inbound reference, a moved ineligible path, a
hash mismatch, a frozen-source edit, an old live pointer, or a new test
regression. R1A reports topology only; it makes no physics verdict.
