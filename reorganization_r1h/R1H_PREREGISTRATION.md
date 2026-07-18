# R1H effective registry and scientific-family closure preregistration

Date: 2026-07-18

Branch: `codex/reorg-r1h-effective-registry-2026-07-18`

Fixed base: `2058f69db3f5c3a4322c5a9404e7145a62eeef2d`

Question type: repository-evidence-led classification audit. This is not a
physics derivation, content migration, or artifact edit.

## Frozen scope

The stable identity universe is exactly the 1,114 unique `original_path` rows
in `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`, resolved to their unique
current paths. The R1G override universe is exactly the set union of
`reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv` and
`reorganization_r1g/B02_B03_ADJUDICATION.tsv`: expected 121 and 32 rows with a
19-row intersection and therefore a 134-row union. These expected counts are
gates, not values to be forced if the source sets disagree.

The 32 B02/B03 candidates are frozen by the R1G adjudication table. Each will
be reviewed exactly once for runtime/import closure, result/evidence
companions, introducing-commit family, conceptual/operator family,
frozen/manifest-bound companions, current control/frontier companions, and
the consequence of moving it without those companions.

## Frozen inputs

| Path | SHA-256 |
|---|---|
| `research/_registry/ROOT_OWNERSHIP.tsv` | `4e8a4e82d4698f24dea7510932a919773267dfad3ad4033999e195044a056edc` |
| `research/_registry/MIGRATION_READINESS.tsv` | `4fbdb4e71aae4caf18df9142e7ab822bb5b348b3b364b72e97707679bd244062` |
| `research/_registry/CURRENT_ARTIFACT_PATHS.tsv` | `9c1f7c9a9f11dbf31706268d5dbd3c2ffd4247e3f981a603d86e2095925e729c` |
| `research/_registry/CURRENT_FRONTIER_TARGETS.tsv` | `5ad9408676d788063165d5b41d6e4002d81f157c2b2a22a5dd23714740d2ec61` |
| `reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv` | `d44c2b8b55c3e16350dec8ce55349426e57cce4d1035859e29898c9fa0736c9d` |
| `reorganization_r1g/B02_B03_ADJUDICATION.tsv` | `cbae13c1d79f3d16a2c6542dfe003559fd3abadffb1d56e8490fdecc3070de11` |
| `reorganization_r1g/READOUT_PROVENANCE_CORRECTION_AUDIT.tsv` | `16f2237db4a3188e9668fa3f57cac265e473f9bbaddabf9f767a4fef5281252c` |
| `reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv` | `c9089c1885f2f618c12567885f1e3d416abeeaa026cd6c442cf7ae64ae70f82c` |

`research/_registry/ROOT_OWNERSHIP.tsv`,
`research/_registry/MIGRATION_READINESS.tsv`, and every tracked path under
`reorganization_r0/` through `reorganization_r1g/` are immutable historical
records for this phase. Their complete path/blob state must equal the fixed
base at final verification.

## Effective-registry contract

`research/_registry/CURRENT_CLASSIFICATION.tsv` will be generated
deterministically and contain exactly one row for every stable identity, with
these columns:

1. `original_path`;
2. `current_path`;
3. `fixed_snapshot_owner`;
4. `fixed_snapshot_evidence`;
5. `effective_primary_owner`;
6. `operator_provenance`;
7. `imported_action_or_coupling`;
8. `comparison_readout`;
9. `role`;
10. `scientific_lifecycle`;
11. `path_migration_safety`;
12. `scientific_family`;
13. `adjudication_source`;
14. `review_status`.

All 134 R1G-overridden identities must take their provenance axes and family
classification from R1G, with any R1H change limited to the separately audited
B02/B03 migration-safety conclusion. Every other row must carry
`review_status=INHERITED_UNREVIEWED`; no inherited row may be represented as
R1G- or R1H-adjudicated.

## Scientific-family migration rule under test

Absence of a runtime import is necessary but not sufficient for independent
move safety. A candidate is independently move-safe only if its complete
scientific family has no result/evidence, provenance, immutable, manifest,
control, frontier, or conceptual/operator companion whose required present
path would be stranded by moving the candidate alone. If a complete atomic
family can be named but contains an immutable or unauthorized companion, the
candidate is blocked; the family is recorded, not split. No replacement batch
may be invented in this phase.

Permitted per-candidate conclusions are:

- `INDEPENDENT_MOVE_SAFE`;
- `ATOMIC_FAMILY_MOVE_ONLY`;
- `BLOCKED_IMMUTABLE_FAMILY_COMPANION`;
- `BLOCKED_CONTROL_OR_FRONTIER_COMPANION`;
- `BLOCKED_INCOMPLETE_OR_OPEN_CLOSURE`.

## Fail-closed falsification contract

The independent verifier must reject:

1. fallback to `PRE_NATIVE` for any R1G-overridden identity;
2. a missing or duplicate override;
3. loss of a reference-only readout disclosure;
4. a standalone-safe ruling that strands an immutable scientific-family
   companion;
5. treating `INHERITED_UNREVIEWED` as adjudicated;
6. any union/intersection other than 134/19;
7. missing or duplicate stable identities or current paths;
8. mutation of a fixed snapshot or R0–R1G record;
9. a stale/missing current path, broken current link/frontier target, frozen
   package mutation, test-baseline drift, or original dirty-checkout metadata
   drift.

All catch-proofs must be exercised by corrupted in-memory fixtures and must go
red for the registered reason.

## Maximum conclusion and authority boundary

Maximum conclusion: an authoritative current classification overlay plus
scoped B02/B03 scientific-family closure rulings. If closure is incomplete or
immutable companions would be split, B02/B03 are withdrawn as executable
batches. This phase authorizes no artifact move, copy, rename, deletion,
research-content edit, fixed-snapshot rewrite, LIVE/HANDOFF/INDEX update,
physics change, canonization, GPU work, integration, or migration.
