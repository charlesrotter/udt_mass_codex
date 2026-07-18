# R1A pre-move candidate adjudication

Snapshot: `d8c712942c7b7dc3941c90609d9b0b4dd881dc7c`. This is the frozen first adjudicator run.

Every one of the 26 R0 archive candidates and 37 R0 unknown/blocked paths is
listed below. `INBOUND_REFERENCES.tsv` records every exact occurrence and
states whether its source is frozen. `POINTER_REWRITE_PLAN.tsv` is the complete
non-frozen live-pointer rewrite set for the first batch.

## Outcome

- First safe batch: 17 files.
- Retained in R1A: 46 files.
- Exact inbound occurrences: 801 across 87 sources.
- Frozen-source occurrences: 12.
- Required pointer substitutions: 80 occurrences in 68 source/target groups.

## All 26 archive candidates

| Path | First commit | Inbound occurrences | Frozen sources | Disposition | Individual ruling |
|---|---|---:|---|---|---|
| `D1_FIX_DESIGN.md` | `2026-06-29` | 39 | seal_matching_junction_results.md | `RETAIN_R1A` | Retain > **MOVED 2026-07-06 → `archive/pre_native_coupled/D1_FIX_DESIGN.md` (pre-native-era census).**; FROZEN_INBOUND:seal_matching_junction_results.md |
| `EXTERNAL_AUDIT_2026-06-30.md` | `2026-06-30` | 15 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/EXTERNAL_AUDIT_2026-06-30.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `F1F3_closure_results.md` | `2026-06-21` | 22 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (F1 + F3 CLOSURE RECORD — tying off the gravity-action + a(phi)-coupling foundation); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `P1P5_reaudit_vs_derived_operator_results.md` | `2026-06-21` | 23 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (P1–P5 RE-AUDIT vs the Newly-Derived Operator — did the recent work affect any P-result?); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `P5e_proper_results.md` | `2026-06-21` | 34 | F8_metric_choices_results.md | `RETAIN_R1A` | Retain P5e PROPER — the genuinely fully-coupled, multi-harmonic, free-omega, finite-amplitude, FULL off-diagonal time-row time-live solve on UDT's DERIVED operator — BOUNDED OBSERVE; FROZEN_INBOUND:F8_metric_choices_results.md |
| `PROVENANCE_AUDIT_2026-06-30.md` | `2026-06-30` | 27 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/PROVENANCE_AUDIT_2026-06-30.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `SOLVER_AUDIT_2026-06-29.md` | `2026-06-29` | 41 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/SOLVER_AUDIT_2026-06-29.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `STEP2_timelive_matter_results.md` | `2026-06-21` | 34 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (STEP 2 — TIME-LIVE COUPLED NATIVE-MATTER SOLVE on UDT's DERIVED operator — BOUNDED OBSERVE); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `b1prime_round_gate_derived_operator_results.md` | `2026-06-21` | 19 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (B1' — Round-Limit Gate on the Derived Operator (RADIAL reconstruction + blind verification)); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `branch_operator_contamination_ledger.md` | `2026-07-06` | 53 | - | `RETAIN_R1A` | Retain branch_operator.py — SCOPED CONTAMINATION LEDGER (ERA-WIDE re-grade); FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-06 |
| `coupled_timelive_VERIFIER.md` | `2026-06-19` | 15 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/coupled_timelive_VERIFIER.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `coupled_timelive_solve_CONTRACT.md` | `2026-06-19` | 38 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/coupled_timelive_solve_CONTRACT.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `coupled_timelive_solve_results.md` | `2026-06-19` | 34 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/coupled_timelive_solve_results.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `lepton_ladder_test_results.md` | `2026-06-10` | 20 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (Lepton Ladder Test Results); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `macro_native_matter_after_vacuum_MAP.md` | `2026-07-09` | 6 | - | `RETAIN_R1A` | Retain MAP — Native matter *after* Path B vacuum (what to ask next); FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-09 |
| `matter_object_identity_native_vs_import_results.md` | `2026-06-21` | 25 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (Matter Object Identity — the Round-Gate Soliton is an IMPORTED S³ Baryon; UDT's Native Matter is S² (and Unsolved on the Derived Operator)); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `matter_regrade_derived_operator_results.md` | `2026-06-21` | 66 | F2_closure_results.md;p4_cross_model_verify_results.md | `RETAIN_R1A` | Retain Re-grading UDT's Matter Sector on the Newly-Derived Gravitational Operator — Analytic OBSERVE; FROZEN_INBOUND:F2_closure_results.md,p4_cross_model_verify_results.md |
| `nonstationary_opener_results.md` | `2026-06-11` | 47 | ns_scan_results.md;w_stiffness_results.md | `RETAIN_R1A` | Retain The Nonstationary Opener (N1 + N2) — Results: THE FORK ADJUDICATED; FROZEN_INBOUND:ns_scan_results.md,w_stiffness_results.md |
| `p1_VERIFIER.md` | `2026-06-19` | 18 | p2_matter_fullmetric_results.md | `RETAIN_R1A` | Retain > **MOVED 2026-07-06 → `archive/pre_native_coupled/p1_VERIFIER.md` (pre-native-era census).**; FROZEN_INBOUND:p2_matter_fullmetric_results.md |
| `p1_offdiag_wiring_results.md` | `2026-06-19` | 14 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (P1 -- Off-diagonal wiring to the general Einstein: results); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `scale_symmetry_bootstrap_analysis_results.md` | `2026-06-21` | 37 | F2_matter_action_forcedness_results.md;F5_critical_universe_closure_results.md;F7_scale_bridge_native_results.md | `RETAIN_R1A` | Retain Scale (Dilatation) Symmetry & the Global-Bootstrap Hypothesis — Analytic OBSERVE; FROZEN_INBOUND:F2_matter_action_forcedness_results.md,F5_critical_universe_closure_results.md,F7_scale_bridge_native_results.md |
| `static_soliton_rerun_derived_operator_results.md` | `2026-06-21` | 46 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (Static Charge-1 Soliton, Re-Solved on the Newly-Derived Gravitational Operator — BOUNDED OBSERVE); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `timelive_nonround_VERIFIER.md` | `2026-06-19` | 10 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/timelive_nonround_VERIFIER.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `timelive_nonround_native_solve_results.md` | `2026-06-19` | 36 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (> **MOVED 2026-07-06 → `archive/pre_native_coupled/timelive_nonround_native_solve_results.md` (pre-native-era census).**); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `weld_discriminator_results.md` | `2026-06-10` | 4 | - | `MOVE_BATCH_1` | Pre-cutoff superseded text record (Weld Discriminator Results); no runtime, manifest, frozen-source, or unresolved-path dependency; non-frozen pointers are atomically rewritable. |
| `weld_status_results.md` | `2026-06-10` | 19 | weld_interface_mode_results.md | `RETAIN_R1A` | Retain Weld Status Results; FROZEN_INBOUND:weld_interface_mode_results.md |

## All 37 unknown/blocked paths

No unknown/blocked path is moved in R1A. Opaque artifacts are not
deserialized and numerical outputs are not reinterpreted as archival merely
because they have no exact inbound reference.

| Path | Artifact role | Inbound occurrences | Disposition | Individual ruling |
|---|---|---:|---|---|
| `A_pre_reconciliation_floored_glm.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-01 |
| `B_floored_glm.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-01 |
| `cascade_stageC_primary_table.json` | `CASCADE_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain CASCADE_NUMERICAL_JSON; R0_UNKNOWN:CASCADE_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-02 |
| `cascade_stageC_twomethod.json` | `CASCADE_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain CASCADE_NUMERICAL_JSON; R0_UNKNOWN:CASCADE_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-02 |
| `energy_min_m2_18_out.json` | `NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain NUMERICAL_JSON; R0_UNKNOWN:NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `hopfion_GP_switch_apply_out.json` | `NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain NUMERICAL_JSON; R0_UNKNOWN:NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-10 |
| `noNull_hess_256_bs8_run_log.txt` | `NUMERICAL_LOG` | 3 | `RETAIN_R1A` | Retain NUMERICAL_LOG; R0_UNKNOWN:NUMERICAL_LOG; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-13 |
| `noNull_hess_bw2_N128_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-14 |
| `noNull_hess_bw2_N192_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-14 |
| `noNull_hess_refine_192_log.txt` | `NUMERICAL_LOG` | 3 | `RETAIN_R1A` | Retain NUMERICAL_LOG; R0_UNKNOWN:NUMERICAL_LOG; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-14; UNRESOLVED_PATH_TOUCH:LIVE.md:107 |
| `noNull_nk_converged_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-12 |
| `noNull_relax_lbfgs_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-12 |
| `noNull_relax_lbfgs_traj.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-12 |
| `noNull_resolve_U1deflated_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-12 |
| `noNull_resolve_undeflated_out.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-12 |
| `noNull_schur_inertia_N128.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-16 |
| `noNull_schur_inertia_N192.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-16 |
| `noNull_schur_inertia_N256.json` | `PARTICLE_MASS_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PARTICLE_MASS_NUMERICAL_JSON; R0_UNKNOWN:PARTICLE_MASS_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-16 |
| `origin_prompts_screenshot_2025-08-12.png` | `PROVENANCE_IMAGE` | 4 | `RETAIN_R1A` | Retain PROVENANCE_IMAGE; R0_UNKNOWN:PROVENANCE_IMAGE; NOT_MARKDOWN_TEXT_RECORD |
| `phase3b_descend_m2_out.json` | `NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain NUMERICAL_JSON; R0_UNKNOWN:NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `phase3b_descend_m3_out.json` | `NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain NUMERICAL_JSON; R0_UNKNOWN:NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `provenance_origin_prompts_2025-08-12.png` | `PROVENANCE_IMAGE` | 4 | `RETAIN_R1A` | Retain PROVENANCE_IMAGE; R0_UNKNOWN:PROVENANCE_IMAGE; NOT_MARKDOWN_TEXT_RECORD |
| `radial_Bfree_depth.out` | `RUNTIME_OUTPUT` | 7 | `RETAIN_R1A` | Retain RUNTIME_OUTPUT; R0_UNKNOWN:RUNTIME_OUTPUT; NOT_MARKDOWN_TEXT_RECORD; PROHIBITED_DEPENDENCY:FILE_PATH:legacy/root_oneoffs_2026-07-01/radial_Bfree_depth.py |
| `radial_Bfree_diag.out` | `RUNTIME_OUTPUT` | 7 | `RETAIN_R1A` | Retain RUNTIME_OUTPUT; R0_UNKNOWN:RUNTIME_OUTPUT; NOT_MARKDOWN_TEXT_RECORD; PROHIBITED_DEPENDENCY:FILE_PATH:legacy/root_oneoffs_2026-07-01/radial_Bfree_diag.py |
| `simple_metric_kaleidoscope_K1_out.json` | `MACRO_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain MACRO_NUMERICAL_JSON; R0_UNKNOWN:MACRO_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-09 |
| `simple_metric_kaleidoscope_K2b_out.json` | `MACRO_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain MACRO_NUMERICAL_JSON; R0_UNKNOWN:MACRO_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD; FIRST_COMMIT_NOT_PRE_CUTOFF:2026-07-09 |
| `u_plat_m1_18x8x8.json` | `PLATEAU_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PLATEAU_NUMERICAL_JSON; R0_UNKNOWN:PLATEAU_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `u_plat_m1_18x8x8.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `u_plat_m2_18x8x8.json` | `PLATEAU_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PLATEAU_NUMERICAL_JSON; R0_UNKNOWN:PLATEAU_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `u_plat_m3_18x8x8.json` | `PLATEAU_NUMERICAL_JSON` | 1 | `RETAIN_R1A` | Retain PLATEAU_NUMERICAL_JSON; R0_UNKNOWN:PLATEAU_NUMERICAL_JSON; NOT_MARKDOWN_TEXT_RECORD |
| `u_plat_m3_18x8x8.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X10.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X100.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X1000.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X3.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X30.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |
| `xexplore_field_X300.pt` | `OPAQUE_TORCH_ARTIFACT` | 1 | `RETAIN_R1A` | Retain OPAQUE_TORCH_ARTIFACT; R0_UNKNOWN:OPAQUE_TORCH_ARTIFACT; NOT_MARKDOWN_TEXT_RECORD |

## Interpretation boundary

A `MOVE_BATCH_1` ruling means only that the path satisfies the
preregistered topology predicate. It does not alter or endorse the record's
physics. A `RETAIN_R1A` ruling is a conservative location decision, not a
claim that the file is active or canonical.
