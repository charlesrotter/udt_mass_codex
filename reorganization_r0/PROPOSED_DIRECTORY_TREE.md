# Proposed post-R0 directory tree

Status: **proposal only; no move, rename, deletion, or copy has been executed**.

This is a smallest-useful navigation target for later, separately authorized
phases. Names describe functions rather than asserting new scientific status.

```text
/
|-- README.md
|-- AGENTS.md
|-- LIVE.md
|-- HANDOFF.md
|-- INDEX.md
|-- CLAUDE.md
|-- CANON.md
|-- MEMORY.md
|-- FOUNDATIONAL_ASSUMPTIONS_LEDGER.md
|-- NEGATIVES_REGISTRY.md
|-- PROBLEM_STATEMENT.md
|-- PROVENANCE.md
|-- pytest.ini
|-- governance/
|   |-- controls/
|   `-- templates/
|-- docs/
|   |-- active/
|   |-- maps/
|   |-- dispatches/
|   |-- results/
|   `-- archive/
|-- src/
|   `-- udt/
|       |-- geometry/
|       |-- operators/
|       |-- solvers/
|       `-- validation/
|-- tools/
|   |-- audit/
|   |-- migration/
|   `-- verification/
|-- evidence/
|   |-- frozen/
|   |-- manifests/
|   `-- numerical/
|-- data/
|-- tests/
`-- reorganization_r0/
```

## Root-retention rule

The permanent root control surface proposed by R0 is:

- `.gitattributes`, `.gitignore`, and `pytest.ini`;
- `README.md`, `AGENTS.md`, `LIVE.md`, `HANDOFF.md`, `INDEX.md`, `CLAUDE.md`,
  `CANON.md`, and `MEMORY.md`; and
- `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md`, `NEGATIVES_REGISTRY.md`,
  `PROBLEM_STATEMENT.md`, and `PROVENANCE.md`.

Four more governance files remain at root unless and until a later audited
control-path migration is approved. Another 187 base files are conditionally
root-pinned: 141 by startup/frontier references and 46 by resolved Python or
test imports. The exact rows and release gates are in `ROOT_RETENTION.tsv`.
These conditional pins are migration constraints, not claims that every file
must remain at root forever.

## Proposed routing

| R0 material | Later target | Constraint before any action |
|---|---|---|
| Current governance helpers | `governance/` | Rewrite startup/control references and rerun tests. |
| Active narratives, maps, dispatches, results | `docs/` subtrees | Adjudicate semantic family and rewrite every pointer. |
| Reusable Python modules | `src/udt/` | Establish packages, migrate imports, and preserve the test baseline. |
| Standalone verifiers and audit utilities | `tools/` | Separate library imports from executable entry points. |
| Frozen packages and manifests | `evidence/frozen/` | Only an atomic, manifest-preserving relocation with before/after package hashes and provenance updates; never file-by-file normalization. |
| Numerical artifacts and inputs | `evidence/numerical/` or `data/` | Resolve producer/consumer paths and opaque-file status first. |
| Clearly historical documents | `docs/archive/` | Human audit must confirm no current startup, import, manifest, or evidentiary requirement. Archive never means delete. |

## Phase gates before a later move proposal

1. Resolve or explicitly waive the relevant rows in the 1,438-edge static
   unresolved/dynamic queue.
2. Convert basename-only and ambiguous manifest references to canonical paths.
3. Define package/import compatibility for each Python family before relocating
   any module.
4. Rewrite all startup and Markdown pointers in the same atomic change as a
   document move.
5. Preserve frozen package bytes and verify every internal manifest before and
   after any authorized relocation.
6. Run the independent R0 verifier and the complete existing test suite, with
   no regression from the recorded baseline.

`MOVE_CANDIDATE` and `ARCHIVE_CANDIDATE` are audit classifications, not move
authorization. `UNKNOWN/BLOCKED` requires human adjudication before any later
phase may act on the path.
