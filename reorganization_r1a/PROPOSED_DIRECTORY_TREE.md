# Proposed research-lane-first directory tree

Status: R1A proposal. Only the first verified batch under
`archive/pre_2026-07-01/` is authorized in this phase. No active research,
Python, data, manifest, or frozen-evidence relocation is authorized.

```text
/
|-- README.md
|-- AGENTS.md
|-- LIVE.md
|-- HANDOFF.md
|-- stability_branch_follow_256_DECISION.md
|-- INDEX.md
|-- CLAUDE.md
|-- CANON.md
|-- MEMORY.md
|-- FOUNDATIONAL_ASSUMPTIONS_LEDGER.md
|-- NEGATIVES_REGISTRY.md
|-- PROBLEM_STATEMENT.md
|-- PROVENANCE.md
|-- pytest.ini
|-- research/
|   |-- foundations/
|   |   |-- evidence/
|   |   `-- tools/
|   |-- native_action/
|   |   |-- evidence/
|   |   |   |-- frozen/
|   |   |   `-- manifests/
|   |   |-- tools/
|   |   `-- data/
|   |-- particle_mass/
|   |   |-- src/
|   |   |   `-- udt/
|   |   |-- tools/
|   |   |-- evidence/
|   |   `-- data/
|   `-- macro/
|       |-- src/
|       |   `-- udt/
|       |-- tools/
|       |-- evidence/
|       `-- data/
|-- archive/
|   |-- pre_2026-07-01/
|   `-- <existing historical families>/
|-- tests/
|-- reorganization_r0/
`-- reorganization_r1a/
```

## Lane boundary rule

`src/udt/`, `tools/`, `evidence/`, and `data/` are lane-owned children, not
global catch-all buckets. A later phase must decide the owning research lane
before relocating an implementation or artifact. Cross-lane utilities remain
at their current path until an explicit shared-interface contract exists.

- `research/foundations/` owns metric, postulate, selector, and derivation
  provenance—not live numerical outputs from another lane.
- `research/native_action/` owns the native-action derivation and adjudication
  chain. Its frozen packages would remain atomic under any later authorized
  relocation.
- `research/particle_mass/` owns the corrected-carrier stability, mass,
  boundary-virial, and basin program with its lane-specific code and evidence.
- `research/macro/` owns the simple-metric / WR-L program and its lane-specific
  code and evidence.
- `archive/pre_2026-07-01/` receives only pre-cutoff historical records that
  pass the R1A no-runtime, no-manifest, no-frozen-reference, no-unresolved-path
  predicate. Archive means retained history, never deletion.

## Root control surface

The R0 permanent root controls remain at root. The orientation chain is now
explicitly `LIVE.md` → `HANDOFF.md` →
`stability_branch_follow_256_DECISION.md` → relevant evidence after Git
synchronization. `AGENTS.md` controls operation and method but cannot override
the current frontier stated by `LIVE.md`.

## Later-phase gates

R1B must be separately authorized. Before any active-lane relocation it must
resolve ownership, imports, runtime file paths, tests, manifests, dynamic
paths, and all startup pointers as one atomic migration. No lane may borrow an
artifact merely because a generic file-type directory exists.
