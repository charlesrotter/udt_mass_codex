# Fixed-base source-discovery rule

All discovery is evaluated from base `bd8649ae31aab31435fbe986427d7f4e84d58e6d`; worktree content
cannot enter.

## Seed discovery

Search tracked post-2026-07-01 Markdown, TSV, JSON, and Python paths for either:

1. a filename containing `finite_cell`, `completion`, `complete_branch`, `global_metric`,
   `nonultrastatic`, `coframe`, or `screen`; or
2. content containing a case-insensitive conjunction of one completion term (`finite cell`,
   `completion`, `complete`, `global regular`) and one geometry term (`metric`, `coframe`, `screen`,
   `branch`).

Include current reports/ledgers that claim exhaustive completion or branch coverage even if their
individual rows are incomplete.

## Transitive discovery

From each seed, extract repository-relative references with extensions `.md`, `.tsv`, `.json`,
`.py`, `.npz`, `.txt`, `.csv`, or `.log`. Follow a reference only when its surrounding line also
contains `branch`, `metric`, `coframe`, `screen`, `completion`, `path`, `holonomy`, `curvature`, or
`finite`. Resolve exact paths first and unique basenames second. Iterate to closure.

## Exclusions

- this atlas directory and later generated records;
- archive-only, rescued-workspace, and pre-July sources unless a current post-July seed explicitly
  names them as load-bearing evidence;
- unrelated particle results, cosmology fits, action/source work, and reorganization records;
- candidate files found only by a particle, mass, force, or Standard-Model label.

Every excluded seed receives a recorded reason. Discovery is provenance-only; it does not decide
scientific merit.

## Branch identity rule

Every exact identifier in a seed ledger is retained. Aliases may be consolidated only with an exact
same-source pointer, same defining metric/coframe formula, or explicit current-source equivalence.
Filename similarity is insufficient.
