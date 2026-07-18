# Phase R1B final audit report

## Scope and stop condition

R1B started from fixed base `4b226472c8f7c22dfcdd2c328a109e92d1df5abd` on `codex/reorg-r1a-2026-07-18`. Candidate selection, inbound evidence, and the safety gate were frozen before adjudication or mutation. Generated audit records did not affect the candidate set.

The fixed universe contains 99 tracked root Markdown files first committed before 2026-07-01. Individual rulings are preserved in [`adjudication/CANDIDATE_ADJUDICATION.tsv`](adjudication/CANDIDATE_ADJUDICATION.tsv):

- `ACTIVE_CROSS_ERA`: 17
- `ARCHIVE_ELIGIBLE`: 2
- `BLOCKED`: 8
- `HARD_FROZEN`: 58
- `HISTORICAL_SNAPSHOT`: 2
- `PERMANENT_ROOT`: 10
- `SOFT_EVIDENCE_PATH_ONLY`: 2

Only 2 files and 1 live substitution qualified, below the preregistered 40-file/400-substitution safety stop.

## Executed archive batch

| Old path | New path | Git result | SHA-256 |
|---|---|---|---|
| `STEP2_timelive_matter_MAP.md` | `archive/pre_2026-07-01/STEP2_timelive_matter_MAP.md` | `R100` | `44447c0269c1712f2afe47497c89c2b6e908ba15e1e28735463dd0254f1ab715` |
| `p4_VERIFIER.md` | `archive/pre_2026-07-01/p4_VERIFIER.md` | `R100` | `d79cf4a1f3ead7c0a8ee704179ca6191fab9fbd968374c44f4f907d4169985fb` |

The only pointer edit is the exact token substitution in `STATE.md`: `p4_VERIFIER.md` became `archive/pre_2026-07-01/p4_VERIFIER.md`. Before/after source hashes are in [`migration/POINTER_SUBSTITUTION_RESULT.tsv`](migration/POINTER_SUBSTITUTION_RESULT.tsv). The reference from `archive/pre_2026-07-01/STEP2_timelive_matter_results.md` to `STEP2_timelive_matter_MAP.md` was intentionally not rewritten because it remains a valid same-directory reference.

No physics prose was rewritten. No active file, Python module, data file, manifest, or frozen package was moved.

## Dependency censuses

The post-move full forensic census is pinned to migration commit `49814eb5e12928edb443fca73e69cab2af2e76dc`. It includes historical reorganization records. The operational census excludes sources under `reorganization_r0/`, `reorganization_r1a/`, and `reorganization_r1b/`.

| Census | Base edges | Post-move edges |
|---|---:|---:|
| Full forensic | 20,807 | 25,470 |
| Operational | 14,829 | 14,827 |

The 10,643 post-move edges excluded from the operational view are historical reorganization-record edges. The corrected filename matcher still detects `file.md.` and `file.md)`, rejects `file.md.bak`, and agrees with literal `git grep` for both moved basenames. There are zero stale non-frozen operational pointers.

## Preservation and tests

- All 99 adjudicated rows are accounted for: 98 candidate payloads are byte-identical, while `STATE.md` has the single audited exact path-only edit.
- Both moved blobs and SHA-256 values are identical before and after.
- All six frozen native-action package manifests replay successfully, and their complete tracked package states match the fixed base.
- The original dirty workstation checkout remains 54 paths with identical status, lstat size, and object type; content remains `NOT_READ`.
- The full suite remains at the known baseline: 69 passed, 1 known hygiene failure, and 1 xfailed.

R1B stops here before active-lane migration, R1C, native-action continuation, GPU work, canonization, or any repository reorganization beyond this bounded archive batch.
