# R1H effective registry and scientific-family closure audit

Date: 2026-07-18

Branch: `codex/reorg-r1h-effective-registry-2026-07-18`

Base: `2058f69db3f5c3a4322c5a9404e7145a62eeef2d`

Preregistration commit: `b7074062f0f8c196c9695e28add68950b3d9a996`

Verdict: **VERIFIED for the preregistered repository-classification scope.**
This is not a physics adjudication or migration authorization.

## Post-correction migration-state layer

The migration-state correction was separately preregistered at `cf0005a` from the exact
pre-correction tip `b050d2eec5050cdcacc0edada67a438656cf3307`. Before mutation, the exact
predicate `review_status = R1G_ADJUDICATED` and
`path_migration_safety = BLOCKED_PROVENANCE_CORRECTION_REQUIRED` selected 101 identities; their
newline-terminated `original_path` projection hashes to
`78f9afef35b3d4b97f4fea5f1c30b0ab269f1d91becad75034f0aaff11334393`.

Those exact 101 rows now read `BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED`. No family review was
performed, no row was promoted to a movable state, and zero rows retain the stale provenance block.
The new independent `migration_review_status` axis has exact counts:

| Rows | Migration review status |
|---:|---|
| 101 | `FAMILY_REVIEW_REQUIRED` |
| 32 | `FAMILY_REVIEWED_BLOCKED` |
| 1 | `IMMUTABLE_PATH` |
| 980 | `INHERITED_UNREVIEWED` |

The pre-existing 32 family-blocked rows and one immutable row are field-identical to `b050d2e` apart
from receiving the new status field. Every old field of all 980 inherited rows is identical to
`b050d2e`. The 32-row scientific-family closure table remains byte-identical at SHA-256
`e9bba349597e0b583a97f80ee6cc72a5caba943cd1e6b8788703c5846937cdec`.

## Effective current registry

The generated authoritative overlay is
[`CURRENT_CLASSIFICATION.tsv`](../research/_registry/CURRENT_CLASSIFICATION.tsv),
with schema [`CURRENT_CLASSIFICATION_SCHEMA.json`](CURRENT_CLASSIFICATION_SCHEMA.json)
and deterministic generator
[`build_r1h_effective_registry.py`](build_r1h_effective_registry.py).

Coverage and provenance counts:

- stable identities: 1,114 rows, 1,114 unique original paths, 1,114 unique
  current paths;
- R1G source sets: 121 affected cascade rows and 32 B02/B03 rows;
- exact intersection: 19 rows;
- exact union: 134 rows;
- review status: 980 `INHERITED_UNREVIEWED`, 102 `R1G_ADJUDICATED`,
  32 `R1H_SCIENTIFIC_FAMILY_REVIEWED`;
- operator provenance: 980 `INHERITED_UNREVIEWED`, 131
  `NATIVE_2026-07-01`, two `MIXED`, one `OPEN`;
- lifecycle: 980 `INHERITED_UNREVIEWED`, 133 `HISTORICAL`, one `FROZEN`;
- reference-only readout disclosures retained: six rows.

Effective primary-owner counts are 23 `CONTROL_ROOT`, 141 `FOUNDATIONS`, 27
`NATIVE_ACTION`, 140 `PARTICLE_MASS`, 273 `MACRO`, 491 `LEGACY_FROZEN`, 15
`CROSS_LANE_SHARED`, and four `UNKNOWN_BLOCKED`. The 980 unaffected rows carry
their fixed owner explicitly as unreviewed inheritance; none is represented as
freshly adjudicated.

SHA-256:

- current classification:
  `05cc6b48d40b9041d1bd82584489fde6cb2a29f59b495b50c32ac30abe6bb8e3`;
- schema:
  `6c589a8c51862ebc64b6b36a59bc21d84d443d5988b858f09a9768b5d5e794af`.

## B02/B03 scientific-family closure

The individual 32-row audit is
[`B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv`](B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv),
governed by
[`SCIENTIFIC_FAMILY_MIGRATION_RULE.md`](SCIENTIFIC_FAMILY_MIGRATION_RULE.md).

All 18 B02 and 14 B03 scripts remain runtime-standalone: zero rows have a
repository-local import and zero rows perform runtime file I/O. That fact is
not sufficient for independent migration. Every script belongs to a coherent
introducing-commit/operator family containing an immutable result, generated
evidence, or native-field provenance companion.

| Scientific family | Rows | Ruling |
|---|---:|---|
| `SF01_THETA0_ACCUMULATION` | 9 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF02_TWIN_LADDER_INVOLUTION` | 2 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF03_STABILITY_OPERATOR` | 5 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF04_ENERGY_ORIENTATION_READOUT` | 2 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF05_LEMMA_D_SEALING_AMPLITUDE` | 1 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF06_PHI_ALPHA_COUPLING` | 2 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF07_STAGE_D_FORECAST` | 1 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF08_HOMOGENEOUS_UNIVERSE_NEGATIVE` | 2 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF09_REDSHIFT_OPTICS_N2` | 1 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |
| `SF10_UNIVERSE_CELL_FOLD_JC_SIGMA` | 7 | `BLOCKED_IMMUTABLE_FAMILY_COMPANION` |

No candidate is independently move-safe. B02 and B03 are withdrawn as
execution batches. R1H does not promote the recorded atomic families to
replacement batches and does not claim that whole-family migration is safe.

Closure-table SHA-256:
`e9bba349597e0b583a97f80ee6cc72a5caba943cd1e6b8788703c5846937cdec`.

## Independent verification

The independent implementation
[`verify_r1h_effective_registry.py`](verify_r1h_effective_registry.py) produced
[`VERIFY_RESULT.json`](VERIFY_RESULT.json). It does not import the generator.
It independently rejoined the source tables, recomputed set arithmetic and
Git commit families, re-parsed candidate imports/file I/O, validated immutable
companions, and compared the checked-in outputs with a fresh deterministic
generator replay.

All 19 exercised catch-proofs passed. The original 13 remain passing:

1. pre-native fallback rejected;
2. missing override rejected;
3. duplicate override rejected;
4. reference-only readout disclosure loss rejected;
5. standalone movement stranding an immutable companion rejected;
6. inherited-unreviewed inflation rejected;
7. incorrect 134-row union or 19-row overlap rejected;
8. unauthorized edit rejected;
9. frozen-record mutation rejected;
10. duplicate current path rejected;
11. manifest mutation rejected;
12. broken link rejected;
13. original dirty-checkout metadata drift rejected.

The six post-correction proofs also passed:

14. a surviving stale provenance-correction state rejected;
15. an incorrect replacement set rejected;
16. promotion of a family-review-required row rejected;
17. drift in a family-reviewed blocked row rejected;
18. drift in the immutable row rejected;
19. drift in an old inherited-row field rejected.

Repository gates:

- deterministic generator replay: PASS;
- current paths: 1,109 `ROOT_RETAINED`, one `MIGRATED_R1D`, four
  `MIGRATED_R1F`; all 1,114 resolve uniquely;
- six frozen manifests: PASS; all 133 package paths byte-identical to base;
- frontier: 306 rows / 101 unique targets, all present;
- tests: 69 passed, one known hygiene-header failure, one xfailed; baseline
  match PASS;
- original dirty checkout: 54 status/lstat rows match; contents `NOT_READ`;
- fixed `ROOT_OWNERSHIP.tsv`, `MIGRATION_READINESS.tsv`, and all R0–R1G
  evidence/planning paths: unchanged.

## Evidence gates and remaining scope

1. Preregistered: yes, before candidate-content inspection.
2. Full space or bounded scope: complete for all 32 B02/B03 candidates and all
   1,114 stable registry identities; no claim about broader family migration.
3. Independently verified: yes, by a separate fail-closed implementation with
   exercised corrupt fixtures.
4. Premises audited: runtime, commit-family, result/evidence, operator,
   frozen/manifest, control/frontier, current-path, and historical-snapshot
   premises are explicit.

The 980 inherited rows remain unreviewed. The 101 corrected rows still require scientific-family
migration review. This audit is one bounded repository organization tile, not completion of
migration or scientific-family review.

## Authority boundary

No research artifact moved, copied, renamed, deleted, or content-edited. No
fixed snapshot, R0–R1G record, LIVE/HANDOFF/INDEX file, physics claim,
`CANON.md`, manifest, data, or evidence package changed. Stop before
integration, registry navigation updates outside the authorized README,
replacement batch planning, migration, physics, canonization, or GPU work.
