# Repository reorganization Phase R1A audit report

- Date: 2026-07-18
- R0 base: `4c98e32d7b8af0dc3159706d18006d673566d721`
- R1A branch: `codex/reorg-r1a-2026-07-18`
- Migration commit: `3cd2a99e402bd69cf180ca15e4b1337635dd5837`
- Scope: startup correction, lane-first proposal, complete 63-file
  adjudication, and one conservative archive batch

## **CORRECTION LAYER — inbound-reference boundary repair**

> **This layer supersedes the reference counts in the preserved original R1A
> run below; it does not rewrite or replace the original preregistered tables.**

The correction was preregistered in commit `f5b4ee5` before any live pointer
mutation. A repaired filename-boundary matcher and an independent literal
`git grep -F` implementation agree occurrence-for-occurrence at R0 base
`4c98e32`: **815 occurrences across 92 sources, including 16 formally
frozen-source occurrences**. The original 801/87/12 tables remain unchanged as
historical evidence. Executable catch-proofs detect `file.md.` and `file.md)`
while rejecting `file.md.bak`.

The 14 recovered omissions have explicit dispositions: five non-frozen live
pointers received only the preregistered `archive/pre_2026-07-01/` prefix; one
`archive/pre_native_coupled/` reference intentionally names its co-located
archived verifier and remains unchanged; the other eight name targets retained
at root. The consolidated pointer plan therefore has 85 substitutions across
33 sources, compared with 80 across 32 sources in the historical first run.

Post-correction verification confirms that all 17 moved files remain eligible
and retain their Git blobs and SHA-256 payloads, all six frozen packages remain
byte-identical to R0, the original workstation still matches its 54-row
metadata-only inventory, zero stale non-frozen pointers remain, and tests stay
at the recorded 69 passed / 1 xfailed / 1 known hygiene failure baseline.

The correction evidence is indexed under
[`correction_2026-07-18/`](correction_2026-07-18/), including the preregistration,
omission ledger, corrected/consolidated tables, literal-Git comparison,
pointer-change hashes, corrected post-move census, and fail-closed final result.
R1B remains unauthorized.

## Outcome

R1A moved 17 pre-July-1 superseded Markdown records to
`archive/pre_2026-07-01/` with `git mv`. Every rename is `R100`; all 17
SHA-256 values and Git blob identities are unchanged. Eighty exact path tokens
were atomically updated across 32 non-frozen source files. Each modified
pointer source was mechanically proven equal to its pre-move bytes plus only
the preregistered old-to-new path substitutions.

No active file, Python module, opaque artifact, numerical data file, manifest,
frozen source, or unresolved-dynamic-path target was moved. Nothing was
deleted, canonized, or physics-edited.

## Startup and proposed topology

The root `README.md` now states the operational order correctly: synchronize
Git under `AGENTS.md`, then read `LIVE.md` → `HANDOFF.md` →
`stability_branch_follow_256_DECISION.md` → the exact active-lane evidence.
`AGENTS.md` supplies operational and method instructions but cannot overrule
the topmost current-state block in `LIVE.md`.

The R1A proposal supersedes the generic R0 layout with four research lanes:

- `research/foundations/`;
- `research/native_action/`;
- `research/particle_mass/`; and
- `research/macro/`.

Each lane owns its applicable `src/udt/`, `tools/`, `evidence/`, and `data/`
children. There is no global file-type bucket that can erase lane provenance.
Only `archive/pre_2026-07-01/` is created and populated in R1A; the research
lane tree remains a proposal for later audit.

## Historical first-run review-queue adjudication (preserved)

The frozen pre-move adjudication contains exactly 63 rows: all 26 R0
`ARCHIVE_CANDIDATE` paths and all 37 R0 `UNKNOWN/BLOCKED` paths. Its independent
scanner reproduced all 801 exact inbound occurrences across 87 sources,
including 12 occurrences from frozen sources.

Seventeen archive candidates passed every preregistered gate. The exact
old-to-new paths and hashes are in `MOVE_MAP.tsv`.

Nine archive candidates were retained individually:

| Retained path | R1A blocker |
|---|---|
| `D1_FIX_DESIGN.md` | Frozen inbound source: `seal_matching_junction_results.md`. |
| `P5e_proper_results.md` | Frozen inbound source: `F8_metric_choices_results.md`. |
| `branch_operator_contamination_ledger.md` | First committed 2026-07-06; not a pre-July-1 record. |
| `macro_native_matter_after_vacuum_MAP.md` | First committed 2026-07-09; not a pre-July-1 record. |
| `matter_regrade_derived_operator_results.md` | Frozen inbound sources: `F2_closure_results.md`, `p4_cross_model_verify_results.md`. |
| `nonstationary_opener_results.md` | Frozen inbound sources: `ns_scan_results.md`, `w_stiffness_results.md`. |
| `p1_VERIFIER.md` | Frozen inbound source: `p2_matter_fullmetric_results.md`. |
| `scale_symmetry_bootstrap_analysis_results.md` | Frozen inbound sources: `F2_matter_action_forcedness_results.md`, `F5_critical_universe_closure_results.md`, `F7_scale_bridge_native_results.md`. |
| `weld_status_results.md` | Frozen inbound source: `weld_interface_mode_results.md`. |

All 37 unknown/blocked paths were retained. They include opaque Torch
artifacts, provenance images, numerical JSON, logs, and runtime outputs; lack
of an exact inbound reference was never treated as proof of archival safety.
Their individual roles, references, blockers, hashes, history, and rulings are
in `CANDIDATE_ADJUDICATION.tsv` and `PREMOVE_ADJUDICATION_REPORT.md`.

## Historical first-run pointer and hash gates (preserved)

- 17/17 move-map rows have identical before/after SHA-256 values.
- 17/17 Git renames are 100% identical.
- 80/80 planned non-frozen pointer occurrences were updated.
- 32/32 pointer sources contain only exact path substitutions.
- The post-move token census reports zero stale non-frozen pointers.
- R0 and R1A audit snapshots retain old paths as historical facts; moved
  records retain self/cohort basenames because their bytes are preserved.

## Rebuilt dependency census

At migration commit `3cd2a99`, the repository contains 3,374 tracked paths and
1,116 tracked root files. The rebuilt census contains 17,863 static edges:

| Category | Edges |
|---|---:|
| `FILE_PATH` | 1,450 |
| `MANIFEST` | 1,135 |
| `MARKDOWN_LINK` | 341 |
| `PYTHON_IMPORT` | 6,667 |
| `STARTUP` | 399 |
| `TEST` | 161 |
| `TEXT_REFERENCE` | 7,710 |

The increase from R0 is primarily the exhaustive R1A adjudication, pointer,
and migration ledgers referencing the reviewed paths. Dynamic, ambiguous, and
missing/generated edges remain visible in the post-move summary; they are not
silently resolved. The R0 review rulings remain the semantic authority for the
63-path queue—automatic post-move root classification is only a fresh static
heuristic, not a re-adjudication.

## Frozen evidence and dirty-workstation firewall

All six native-action package manifest hashes match R0. Complete tracked
package-state digests also match R0 byte-for-byte for Stage-I A/B, Stage-II
A/B, Arm C, and final adjudication. No frozen source appears in the changed
path set.

The original workstation remains outside the R1A worktree. Its same 54 dirty
or untracked paths were rechecked using Git status and `lstat` metadata only;
their content was not opened, hashed, staged, moved, or modified.

## Tests and verification status

The complete command `python3 -m pytest tests/` collected 71 tests:

- 69 passed;
- 1 xfailed; and
- the same single known hygiene-header documentation test failed.

The pre-move adjudication verifier passed six catch-proof corruptions. The
migration verifier passed move/hash/pointer catch-proofs and found zero stale
non-frozen pointers. The post-move census verifier independently recomputes the
root inventory, references, metadata, category coverage, frozen packages,
dirty firewall, and final additions-only audit seal.

## Four gates and stop

1. **Preregistered:** commit `d8c7129` froze the predicate before per-file
   outcomes.
2. **Bounded scope:** exactly 63 reviewed paths and the resulting 17-file first
   batch; no broader lane move.
3. **Independently verified:** pre-move, migration, package, pointer, census,
   and test checks all have recorded mechanical passes.
4. **Premises audited:** every candidate, inbound reference, frozen-source
   decision, unresolved-path touch, move hash, and pointer source is exposed.

R1A stops here before R1B. The lane tree beyond the first archive directory is
not executed.
