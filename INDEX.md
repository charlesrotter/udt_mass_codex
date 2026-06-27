# INDEX — Repo Map (refreshed 2026-06-27 after the static-solver completion)

Navigable map of `udt_mass_codex`. **Structure (post-curation):**
- **root** — the LIVE spine: ~111 markdown (orientation + canon/negatives + audit/verifier + active-arc
  records + load-bearing provenance) and the canonical solver `.py` (+ ~510 `native_*.py` tooling
  scripts, still flat, that back the kept research records).
- **`prototype/`** (14 `.py`) — the branchGP/JFNK reference drivers from the 2026-06-23/24 Branch-P arc.
  Reference only; superseded by the p1 migration. (Each carries a `sys.path '..'` shim to still run.)
- **`legacy/`** (5 `.py`) — old P1/P2 validators + verifiers (`p1_validate`, `p2_*`, `_verif_*`).
- **`archive/`** (~169 `.md`) — sediment: the pre-2026-06-18 catalog/oscillator/sf_scan/weld/w-thread era,
  the legacy corpus (udt_validated/active, udt_canonical via the survivor filter), the superseded
  everything-on/derived-operator build MAPs+VERIFIERs, and (2026-06-27) the 5 SUBSUMED status/program
  trackers `COMPLETION_PROGRAM.md`, `SOLVER_COMPLETENESS_MAP.md`, `POST_POSTULATE_PROGRAM.md`,
  `MIGRATION.md`, `REORG_PLAN.md` (each carries an ARCHIVED header). RETIRED — mine for history/tooling
  only, never verdicts. Recoverable via git or `archive/<name>`. (CANON/NEGATIVES load-bearing provenance
  was kept at root, NOT archived — verified by a 3-pass agent check, see `archive/REORG_PLAN.md`.)

**Reading order (every session):** `LIVE.md` (only-guaranteed-current) → `CLAUDE.md` "How we work" + the
discipline skills → `HANDOFF.md` TOP (current activity) → `CANON.md` / `NEGATIVES_REGISTRY.md`
→ this INDEX → the specific records. The file-immutability rule is **REPEALED** (Charles 2026-06-24): use git
as git — edit in place, roll back via history.

**CURRENT FRONTIER (2026-06-27, see LIVE.md):** the STATIC SOLVER is **CODE-COMPLETE** — derived operator +
the 3 spatial off-diagonals live + native-S² matter wired (free core, imported S³ hedgehog retired);
`pytest tests/` = 32 passed / 1 xfailed. The **kap8 characterization RAN (both branches, ~40.9 h)** but its
result is **PARTIAL/CAVEATED** (record = `kap8_characterization_complete_solver_results.md`): the strong-field
horizon hypothesis REMAINS OPEN (the "cured / frozen-DOF not horizon" headline was REJECTED by the blind
verifier on confounded 2-grid data). NEXT (gated on Charles): three follow-ups (firm convergence at Nr=12;
characterize the matter solution; isolate the off-diagonal effect), then DYNAMIC (time-live / non-stationary
native S² — the φ-angular hunch's home). The old "p1 MIGRATION / COMPLETION PROGRAM / F0-F8 scoreboard / B1'
off-round" frame is **SUPERSEDED** (trackers in `archive/`).

---

## 1. The live document spine (root)

**Orientation / charter:** `LIVE.md` (read first) · `CLAUDE.md` (binding charter: principles 1-7, how-we-work,
repo discipline) · `HANDOFF.md` (frontier + next-session items) · `HANDOFF_ARCHIVE.md` (frontier history) ·
`STATE.md` (snapshot — top-of-file frontier STALE, body is the running lab-log) · this INDEX.
(`archive/MIGRATION.md`, `archive/REORG_PLAN.md` = archived; the curation plan + the superseded p1-migration record.)

**Canon / negatives (load-bearing):** `CANON.md` (Charles-canonized statements, append-only; cites its
provenance docs which are all kept at root) · `NEGATIVES_REGISTRY.md` (premise-scoped banked negatives; the
2026-06-19 banner RETIRED the microphysics-discreteness corpus — those provenance docs are in `archive/`,
the STANDING negatives' provenance is kept at root).

**Purity gates / integrity arc (the discipline infrastructure — NEVER archive):** `SOLVER_INTEGRITY_UPGRADES_SPEC.md`,
`P1_PURITY_HARNESS_MAP.md`, and the integrity-arc records `p1_*`/`p2_*`/`p3_*`/`p4_*`/`p5_*_results.md` +
`p{1..4}_VERIFIER.md`. The machine harness is `tests/` (run `python3 -m pytest tests/`: 23 pass / 5
documented-gap xfails) + the discipline skills in `.claude/skills/` (solver-first, no-shortcuts,
verifier-before-record, completeness-map).

**Assumptions audits / programs:** `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (the F0-F8 scoreboard, status-of-record —
top-of-file FRONTIER STALE, body kept as record) · the live MAPs (`QUANTIZATION_MAP`,
`MATTER_SECTOR_MAP_new_foundation`, `F4_seal_boundary_MAP`, `STEP2_timelive_matter_MAP`). **ARCHIVED (2026-06-27,
SUBSUMED by the static-solver completion):** `archive/COMPLETION_PROGRAM.md` · `archive/SOLVER_COMPLETENESS_MAP.md`
· `archive/POST_POSTULATE_PROGRAM.md`.

**Verifier requirements:** `CROSS_MODEL_VERIFY.md` (cross-tier blind verify) · `PROVENANCE.md` · `AUDIT.md`.

**The DERIVED-operator foundation arc (current physics foundation, 2026-06-21):** `native_dilation_weight_derivation`,
`scale_symmetry_bootstrap_analysis`, `matter_regrade_derived_operator`, `F2_matter_action_forcedness`,
`seal_junction_condition`, `F1F3_closure`, `F2_closure`, `F8_metric_choices`, `P1P5_reaudit_vs_derived_operator`,
`F0_SYSTEMATIC_AUDIT`, `udt_field_equations_derivation`, `udt_gravity_sector_rederivation`,
`F5/F6/F7_*` closures (all `_results.md`).

**The static-solver-completion / Branch-P record:** `kap8_characterization_complete_solver_results.md` (2026-06-27;
both-branch kap8 floor + the OPEN strong-field-horizon question, PARTIAL/CAVEATED) · `cognitive_corral_triggers_results.md`
(the driver-trigger / corral-hook guardrail record) · `branchP_solver_floor_xcontinuation_results.md` (#66; the
continuation + winding-native ruler + the kap8 localization arc) + the standing time-live records
(`coupled_timelive_solve`, `timelive_nonround_native_solve` + their CONTRACT/VERIFIER).

**Main research records (kept — hold the load-bearing derivations):** `negative_phi_native_geometry.md` (31k
lines; the q=1/3, η=1/18, N=3 derivations — read via `grep '^## '`) · `particle_spectrum_native_geometry.md`
(End(H1)=1+3+5, N=3 lock, W(P)=Tr(P)/12) · `mass_emergence_canonical_geometry.md` (the audit/prosecution record).

**Standing-negative provenance (kept):** the weld/W-push/Tier-D/source/#62-64 docs (`phase1_geon`,
`phase2a_rotation`, `phase2b_ensemble`, `weld_*`, `w*_results`, `tier_d_*`, `open_domain_discreteness`,
`p_domain_closure_attempt`, `sector_weight_spectral_probe`, etc.) — the evidence behind NEGATIVES_REGISTRY
entries the wholesale banner did NOT retire.

---

## 2. The canonical solver (the live chain)

The CODE-COMPLETE static solver + its audited building blocks (all root; MUST stay — the import-critical closure):
- `p1_residual_general_einstein.py` — **the live static solver** (derived operator + φ; pack6 a,b,c,d,Th,φ;
  X-continuation; Branch G/P; the 3 spatial off-diagonals live; native-S² matter via `dn`).
  `migration_convergence_guard.py` — the solve-level N-convergence guard (reframed filter→CHARACTERIZER).
- `solver_pack.py` — the extracted numeric-method + action-EL pack (the import-traceability cleanup: the live
  solver graph is THIS + the action-EL modules only; `full3d_solver`/`spectral_radial_soliton` left the graph).
- `branch_operator.py` — the DERIVED scalar-tensor operator (e^{2φ} weight, Branch G/P; tagged source-of-truth
  for KAP8/XI_PROD/KAP_PROD), wrapping the audited `b1prime_3d_offround_residual.py` (`E_mixed`, `EL_phi_3d`).
- `free_s2_matter.py` — **native-S² matter, now LIVE** (`field_dn_components_exact`; free 3-component carrier,
  |n|=1 constraint, FREE core — winding from the seed's homotopy class `seed_round_native`; the imported S³
  hedgehog is RETIRED). `spectral_sph_exact.py` — the **SH-EXACT d/dtheta grid fix** (the GL-μ grid
  mis-differentiated winding sin θ non-convergently; unblocked the pure native matter).
- `check_winding_survival.py` — winding/|n| post-solve inspection (the parked follow-up: does the free core
  unwind to vacuum?).
- `full3d_spectral.py`, `full3d_newton.py`, `full3d_solver.py`, `whole_metric_3d_core.py`,
  `whole_metric_3d_matter.py`, `spectral_cheb.py`, `spectral_sph.py`,
  `einstein_3d_eval.py` (+ `einstein_3d_weyl_gen`, `einstein_3d_general_eval/_gen`), `solver_action.py`,
  `spectral_radial_soliton.py`.
- Harness: `tests/test_solver_integrity.py`, `tests/test_operator_from_action.py`,
  `tests/test_solution_space_gate.py` (the 2 physics-blind anti-imposition lints) (+ conftest).
  `pytest tests/` = **32 passed / 1 xfailed** (the 1 xfail = `test_no_habit_pins`, the Branch G/P fork —
  an EXPLORATION gate, not a code flaw).

**Guardrail hooks / cross-check tooling:** `.claude/hooks/corral_trigger.py` + `.claude/settings.json` (the
driver-trigger corral fires on Task/Bash/git-commit — pause+honesty, never merit) · `export_for_local_llm.py`
(local-LLM cross-check export; refuses untagged DATED memory). Record = `cognitive_corral_triggers_results.md`.

**Legacy tooling scripts (~510 `native_*.py`, of ~1078 root .py, still flat):** these back the kept research records
(negative_phi / particle_spectrum) — one doc section = one script ("Implemented in `native_x.py`"). They are
the microphysics-era tooling; mine for structure, not verdicts. (The .py layer was NOT curated — only the 19
prototype/legacy drivers moved; a future pass could archive dead `native_*.py` with the same import-safety check.)

---

## 3. Load-bearing results → script(s) → doc section (still valid; docs kept at root)

| Result | Script(s) | Doc section |
|---|---|---|
| q=1/3 as collar-flow fixed point | `native_minimal_q_flow_candidate.py`, `native_derived_q_flow.py` | negative_phi §141, §143 |
| η=1/18 candidate / audit / generalization | `native_eta_candidate_audit.py`, `native_eta_derivation_attempt.py`, `native_eta_generalization.py` | negative_phi §37-39, §111 |
| N=3 native from the H1 area form | `native_h1_area_form_projector_bridge.py`, `native_eta_epsilon_route.py` | negative_phi §415, §40 |
| N=3 lock of the two-form match | `native_twoform_selector_n3_lock.py` | particle_spectrum §7 |
| End(H1)=1+3+5 operator alphabet | `native_h1_operator_algebra.py` | particle_spectrum §1 |
| Commutator two-form; W(P)=Tr(P)/12 | `native_endh1_commutator_twoform.py`, `native_commutator_isotropy_c1_weight.py` | particle_spectrum §9-10 |
| Box-control NEGATIVE (no classical discreteness) | `native_scalar_spectrum.py`, `native_cell_spectrum.py` | negative_phi §8, §20 |
| γ = 3·exp(−1/36) ladder + universality audit | `native_mass_ladder_candidate.py`, `native_universal_gamma_audit.py` | negative_phi §52, §56 |
| Warped DtN preserves ℓ=1 identity triplet | `native_warped_dtn_identity_preservation.py`, `native_dtn_calderon_phi0_audit.py` | negative_phi §251-252, §239 |
| Final pre-spectrum postulate status | `native_final_prespectrum_postulate_status.py` | negative_phi §434 |

(These derivations are now SUPERSEDED-context for the live physics — the foundation moved to the derived
operator + the migration — but they remain the canon-provenance for q=1/3/η/N=3, hence kept.)

---

## 4. Conventions (current)

- **Use git as git** (immutability REPEALED 2026-06-24): edit files in place; commit per logical change for
  rollback; the audit trail is git history. When you improve a solver, EDIT it (and its harness) — don't
  spawn a new file (that caused the solver proliferation the curation cleaned up).
- **Verifier-before-record** (binding): every banked result gets a blind adversarial verifier pass (recorded
  with agent id + date) before commit. "Double check" = additional agent passes that CHECK prior agents'
  work (analyze→verify→reconcile), not just present-before-execute.
- **Pre-register before testing**; **negatives are premise-scoped** (NEGATIVES_REGISTRY); **calibrate, never
  dramatize**.
- **ANTI-HANG:** coupled solves are SLOW (minutes-to-hours) — bound the grid, ONE clean process, run solves
  yourself via background-notify (NO `nohup` — it detaches from the harness tracker), never background-poll.
- Commit per result; push to github.com/charlesrotter/udt_mass_codex.
