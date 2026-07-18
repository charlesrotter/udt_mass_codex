# UDT repository

This root is the control and navigation surface for the UDT research record.
After synchronizing Git as directed by [`AGENTS.md`](AGENTS.md), orient in this
order: [`LIVE.md`](LIVE.md) → [`HANDOFF.md`](HANDOFF.md) →
[`stability_branch_follow_256_DECISION.md`](stability_branch_follow_256_DECISION.md)
→ the exact evidence named by those files for the active lane. `AGENTS.md`
supplies operational instructions and binding research discipline, but it
cannot overrule the topmost current-state block in `LIVE.md`.

[`INDEX.md`](INDEX.md) is the repository map; [`CANON.md`](CANON.md),
[`NEGATIVES_REGISTRY.md`](NEGATIVES_REGISTRY.md), and
[`PROVENANCE.md`](PROVENANCE.md) are the main status and evidence ledgers.

## Repository reorganization checkpoint R0–R1F

R1E batch planning and R1F/B01 are complete as an audited checkpoint. Fixed historical inventories,
preregistrations, planning records, and verification records remain immutable. Resolve current
artifact locations through
[`CURRENT_ARTIFACT_PATHS.tsv`](research/_registry/CURRENT_ARTIFACT_PATHS.tsv), not by rewriting those
snapshots; use [`MIGRATION_LEDGER.tsv`](research/_registry/MIGRATION_LEDGER.tsv) for migration
provenance. Five active artifacts moved byte-identically: the R1D S8 note and four behaviorally
verified R1F macro verifiers. B02/B03 remain proposals; no further migration is authorized.

## Repository reorganization R0

Phase R0 is an additions-only census and navigation proposal at base commit
`bfa0b9a`. It does not authorize or execute any move, rename, deletion, physics
change, or history rewrite. Start with the
[`R0 audit report`](reorganization_r0/R0_AUDIT_REPORT.md), then consult the
[`root inventory`](reorganization_r0/ROOT_FILE_INVENTORY.tsv),
[`dependency summary`](reorganization_r0/DEPENDENCY_SUMMARY.md), and
[`proposed directory tree`](reorganization_r0/PROPOSED_DIRECTORY_TREE.md).

Frozen evidence packages and their historical records are immutable. Any later
reorganization phase must preserve their bytes, manifests, and provenance.

## Research lane index

Phase R1C adds an ownership and navigation-only [research lane index](research/README.md). It does not move or copy research artifacts and does not create a new physics authority.

## Repository reorganization R1A

R1A supersedes the generic R0 tree proposal with a research-lane-first layout
and executes only the independently gated first pre-July-1 archive batch. See
the [`R1A audit index`](reorganization_r1a/README.md) and
[`lane-first proposal`](reorganization_r1a/PROPOSED_DIRECTORY_TREE.md).
