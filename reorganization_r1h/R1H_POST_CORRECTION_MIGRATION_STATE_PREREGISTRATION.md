# R1H post-correction migration-state fix preregistration

Date: 2026-07-18  
Branch: `codex/reorg-r1h-effective-registry-2026-07-18`  
Required parent: `b050d2eec5050cdcacc0edada67a438656cf3307`

## Frozen finding

Before this preregistration, `research/_registry/CURRENT_CLASSIFICATION.tsv` had SHA-256
`2de2a2795235f674218af54513b1f6ffd93711ef49d02f7e992a4f33a97e12ea`.
Applying the exact predicate

```text
review_status == R1G_ADJUDICATED
and path_migration_safety == BLOCKED_PROVENANCE_CORRECTION_REQUIRED
```

selects exactly 101 stable identities. The newline-terminated, lexicographically registry-ordered
`original_path` projection of that set has SHA-256
`78f9afef35b3d4b97f4fea5f1c30b0ab269f1d91becad75034f0aaff11334393`.

The pre-correction protected populations are:

- 32 `R1H_SCIENTIFIC_FAMILY_REVIEWED` rows at
  `BLOCKED_IMMUTABLE_FAMILY_COMPANION`;
- one `R1G_ADJUDICATED` row at `IMMUTABLE_PATH_RETAIN`;
- 980 `INHERITED_UNREVIEWED` rows.

## Authorized correction

The 101 selected rows will change only their `path_migration_safety` value to
`BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED`. No scientific-family review is performed and no row
may become movable.

A new `migration_review_status` column will distinguish provenance adjudication from migration
review, with these exact totals:

| Rows | Value |
|---:|---|
| 101 | `FAMILY_REVIEW_REQUIRED` |
| 32 | `FAMILY_REVIEWED_BLOCKED` |
| 1 | `IMMUTABLE_PATH` |
| 980 | `INHERITED_UNREVIEWED` |

All old fields of the 980 inherited rows must remain byte/field identical. All old fields of the 32
family-blocked rows and the one immutable row must remain unchanged. The 101 selected identities may
change only the stale migration-safety field plus receive the new field.

## Allowed tracked changes

- this preregistration;
- `reorganization_r1h/build_r1h_effective_registry.py`;
- `reorganization_r1h/CURRENT_CLASSIFICATION_SCHEMA.json`;
- `research/_registry/CURRENT_CLASSIFICATION.tsv`;
- `reorganization_r1h/R1H_AUDIT_REPORT.md`;
- `reorganization_r1h/verify_r1h_effective_registry.py`;
- `reorganization_r1h/VERIFY_RESULT.json`;
- `research/_registry/README.md`.

The fixed R1C snapshots, current-path mapping, R1G evidence, scientific-family definitions and
closure table, research artifacts, physics, frozen evidence, manifests, tests, and controls remain
immutable.

## Fail-closed gates

Verification must reject a surviving stale provenance-correction block, any set other than the
frozen 101 identities, promotion of any selected identity to a movable state, drift in the 32+1
protected rows, drift in any old field of the 980 inherited rows, or any unauthorized path change.
It must also replay the existing manifest/package, current-path, link/frontier, test-baseline, and
original dirty-checkout metadata gates.

This phase authorizes no integration, moves, scientific-family adjudication, physics work,
canonization, or GPU work.
