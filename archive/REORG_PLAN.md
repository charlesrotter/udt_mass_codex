> **[ARCHIVED 2026-06-27 — SUBSUMED by the static-solver completion; the live frontier is LIVE.md (detail: HANDOFF.md TOP). Kept for history.]**

# REORG_PLAN — repo curation (3-pass agent-verified, 2026-06-25)

**Decision (Charles): Option A** — keep load-bearing provenance at ROOT; archive only true sediment.
CANON.md needs NO edit (its provenance docs stay at root). Verified by analyze→verify→reconcile agent
passes ("double check" = agents checking agents). Execute in STAGED commits, verify between each.

## CODE reorg — VERIFIED (P1 import-graph + P2 adversarial). READY.
Move 19 reference/legacy .py OUT of root; NONE is import-critical (no canonical-chain/tests file imports
them). Each moved file needs a sys.path shim so it still finds root modules. **Co-location is load-bearing**:
all 14 prototype files must land together (they import each other + the 2 hubs branchGP/jfnk_branch_solver).
- `prototype/` (14): branchGP_native_s2_coupled_OBSERVE, jfnk_branch_solver, jfnk_floor_driver,
  jfnk_P_dilation_diagnostic, jfnk_equil_floor, equilibrated_lm_floor, probe_phi_terms, x_continuation,
  sharpen_localization, grid_refine_boundary_layer, grid_refine_warmstart, grid_refine_resume, seal_test,
  winding_native_diagnostics.
- `legacy/` (5): p1_validate, p2_residual_fullmetric, p2c_shear_observe, _verif_b_and_nth, _verif_hybrid_sweep.
- SHIM: prototype files already have `sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))` →
  change to `sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))`. The 5
  legacy files have NO sys.path line → add the `..` line near the top (before sibling imports).
- MUST STAY ROOT (canonical closure, 16): p1_residual_general_einstein, branch_operator,
  b1prime_3d_offround_residual, full3d_spectral, full3d_newton, whole_metric_3d_core, whole_metric_3d_matter,
  spectral_cheb, einstein_3d_eval, full3d_solver, solver_action, spectral_radial_soliton, spectral_sph,
  einstein_3d_weyl_gen, einstein_3d_general_eval, einstein_3d_general_gen. Plus migration_convergence_guard
  (seed script), free_s2_matter, and p2_matter_s2_fullmetric/p2_round_s2_solver (needed by the legacy-5).
- VERIFY after: `python3 -m pytest tests/ -q` (expect 23 pass/5 xfail) + `python3 -c "import
  p1_residual_general_einstein as P;print(hasattr(P,'residual_vector_p1'))"` + run one moved file
  (e.g. `python3 prototype/seal_test.py` bounded / or AST-parse all moved files).

## DOCS curation — VERIFIED (P1 classify + P2 + P3 reconcile). Keep ~110, archive ~160.
Option A KEEP set (everything else in `ls *.md` → `archive/`). **Do NOT archive any of these:**

**SPINE (orientation + live infra + canon + main records + maps/programs/specs):** LIVE, CLAUDE, HANDOFF,
HANDOFF_ARCHIVE, STATE, INDEX, MIGRATION, CANON, NEGATIVES_REGISTRY, PROVENANCE, AUDIT, COMPLETION_PROGRAM,
FOUNDATIONAL_ASSUMPTIONS_LEDGER, SOLVER_COMPLETENESS_MAP, POST_POSTULATE_PROGRAM, CROSS_MODEL_VERIFY,
SOLVER_INTEGRITY_UPGRADES_SPEC, REORG_PLAN, QUANTIZATION_MAP, MATTER_SECTOR_MAP_new_foundation,
F4_seal_boundary_MAP, STEP2_timelive_matter_MAP, P1_PURITY_HARNESS_MAP, dimension_ladder_null_audit,
lepton_ladder_falsification_contract; the INTEGRITY-ARC p-docs (p1_purity_harness, p1_offdiag_wiring,
p1_VERIFIER, p2_operator_from_action, p2_matter_fullmetric, p2_VERIFIER, p3_discipline_skills,
p3_aphi_coupling, p3_aphi_FIX, p3_VERIFIER, p4_cross_model_verify, p4_time_live, p4_VERIFIER,
p5_live_state_shrink, p5_solver_survey); main records negative_phi_native_geometry,
particle_spectrum_native_geometry, mass_emergence_canonical_geometry.
  NOTE: udt_canonical_geometry + legacy_hadron_survivor_filter are the legacy CORPUS — Charles may still
  ARCHIVE these (they're explicitly "legacy, mine for structure"); they're SPINE only because CLAUDE/INDEX
  point at them, so move them WITH a CLAUDE.md+INDEX.md pointer update if archiving.

**PROVENANCE-KEEP — CANON-cited (9, HARD — CANON breaks if archived):** angular_lagrangian_results,
angular_lagrangian_verifier_results, native_stabilizer_results, native_stabilizer_verifier_results,
relativistic_metric_rederivation_results, ns_scan_results, ns_scan_verifier_results, solution_space_map,
macro_sector_fork_resolution, external_input_notes.

**PROVENANCE-KEEP — STANDING-negative provenance (NOT retired by the 2026-06-19 banner):** phase1_geon_results
(#62), phase2a_rotation_results (#63), phase2b_ensemble_results (#64), P5e_proper_results (live banner),
branchP_solver_floor_xcontinuation_results (#66), weld_interface_mode_results (#3), exterior_cavity_results
(#3), open_domain_discreteness_results (#6), p_domain_closure_attempt_results (#7/#9), lepton_ladder_test_results
(#10), tier_d_round2_results (#10), tier_d_round3_results (#10), sector_weight_spectral_probe_results (#11),
weld_status_results (#13), weld_two_sided_results (#4), weld_discriminator_results (#14),
sourced_second_jet_results (#15/16), n_derivation_results (#17), angular_completeness_results (#20),
pde_p1_results (#21), nonstationary_opener_results (#22), measure_fork_results (#18/19), w_stiffness_results,
w2_uncovering_results, w3_results, w4_results, w5_results, w6_results, w7_results, w8_results, w_alg_results,
w_whole_results.

**PROVENANCE-KEEP — derived-operator foundation arc (CLAUDE orientation + memory-cited):**
native_dilation_weight_derivation, scale_symmetry_bootstrap_analysis, matter_regrade_derived_operator,
F2_matter_action_forcedness, STEP2_timelive_matter, seal_junction_condition, F1F3_closure, F2_closure,
F8_metric_choices, P1P5_reaudit_vs_derived_operator, F0_SYSTEMATIC_AUDIT, udt_field_equations_derivation,
udt_gravity_sector_rederivation, F5_critical_universe_closure, F6_postulate_A_ledger, F7_scale_bridge_native;
NEGATIVES-live #65 (coupled_timelive_solve + _CONTRACT + _VERIFIER, timelive_nonround_native_solve + _VERIFIER),
#object-identity (matter_object_identity_native_vs_import, static_soliton_rerun_derived_operator,
b1prime_round_gate_derived_operator).

**ARCHIVE = the rest (~160):** the 6 legacy-corpus (udt_validated_results, udt_active_results, UDT_REBUILD +
the 3 SPINE-flagged-optional above); the EVERYTHING-ON build (p5a_*, p5b_*, p5c_*, p5d_*, P5e_* except
P5e_proper, EVERYTHING_ON_*, quant_stepA_*, offround_classical_*); the pre-2026-06-18 RETIRED catalog/
oscillator/dpf/dyn/crux/su3/monodromy/tier(non-provenance)/full3d_catalog/RECON/phase(non-62-64)/a-function
threads; superseded MAPs/CONTRACTs/VERIFIERs whose results are dead. **EXECUTION RULE: archive = all root .md
MINUS the KEEP set above. Run a FINAL keep-list-assembly + a 4th verify pass (confirm no keep doc moved, no
CANON/STANDING provenance link broken) BEFORE the git mv.**

POINTER-UPDATES (the only edits the docs move needs; CANON.md needs NONE under Option A): INDEX.md
document-layer rewrite (it's stale anyway — says "13 markdown files"); STATE.md + NEGATIVES_REGISTRY.md add a
one-line "retired/superseded provenance under archive/" banner (do NOT hand-fix ~110 inline STATE links);
HANDOFF.md repath its one HANDOFF_ARCHIVE link IF HANDOFF_ARCHIVE is archived (it's SPINE here → no edit).

STAGED COMMITS: (code) 1=mkdir+git mv prototype/+legacy/ + shims + verify. (docs, next session) 2=mkdir
archive/ + move legacy-corpus + everything-on build; 3=pre-06-18 retired threads; 4=superseded MAPs/06-20+
builds; 5=pointer updates (INDEX rewrite, STATE/NEGATIVES banners). Verify (pytest + grep no-broken-keep-ref)
between each.
