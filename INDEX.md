# INDEX — Repo Map (2026-07-10 lean)

**⚠ BRANCH: `grok` (2026-07-10)** — `main` is stale for this arc; `git checkout grok`.
**Frontier authority:** `LIVE.md` (wins on conflict).  
**➤ LIVE PARTICLE-MASS ARC (2026-07-17, separate lane — arc COMPLETE through F; awaiting Charles):**
Read LIVE.md CURRENT STATE topmost layer. Result docs: `noNull_phaseG_mass_results.md` (conditional mass
readout, virial-gap finding) + `noNull_boundary_virial_results.md` (BOX-STRESS LEAD) +
`noNull_virial_identity_derivation.md` (V1 identity, CAS 4/4) + `noNull_hess_refine_256_log.txt` /
`noNull_hess_h2fit_log.txt` (spectrum certification) + `noNull_schur_inertia_ALL.json` (full-H inertia seal).
Solvers/tools: `noNull_energy.py` (corrected operator + **exact HVP** `hvp_exact`/`_chunked`) /
`noNull_precond.py` / `noNull_resolve.py` (relax/NK/hess, N-tagged outputs) / `noNull_hess_refine.py`
(soft-lock ortho-LOBPCG) / `noNull_schur_inertia.py` + `noNull_schur_verify.py` (inertia seal) /
`noNull_phaseG_mass.py` + `verify_noNull_phaseG_mass.py` (G) / `noNull_boundary_virial.py` +
`verify_noNull_boundary_virial.py` + `verify_virial_identity_cas.py` (boundary-virial).
Dispatches: `UDT_H3_CORRECTED_G_THEN_F_SEQUENCING_DISPATCH.md` (F prereg = §9; F LOCKED) +
`UDT_H3_BOUNDARY_VIRIAL_CLOSURE_BEFORE_F_DISPATCH.md` (done) +
`UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md` (DRAFT awaiting Charles §0/§1 review).
F (basin): `noNull_behavioral_F.py` + `verify_noNull_behavioral_F.py` + `noNull_behavioral_F_results.md` +
`noNull_F_{dirs,gate,control_*,ladder_N128,fine_*}​.json` + `F_endpoints/` (hashed) + `F_evidence/`.
Audit patch: `noNull_boxscout_build.py` (+_start_rebuilt npz manifested).
Evidence: `phaseG_evidence_2026-07-16/`, `boundary_virial_evidence_2026-07-16/`, `boundary_audit_patch_2026-07-16/`,
`verifier_evidence_2026-07-14/`, `artifact_manifest.json` (SHA-256 of all npz).  
**Frame:** simple metric + **WR-L / C-2026-07-09-1** (\(A=1-r/X\)).  
**NEXT (MACRO lane only — 2026-07-10, may be stale; the PARTICLE lane's next = LIVE.md topmost = WAIT on Charles):** Thread B time-live eigenmode about drained f2d; residual L time-live appearance still live.  
**Quarantine:** free \(D_A\) → `grok/quarantine_free_DA/` (not live theory verdicts).

---

## Reading order

1. **`LIVE.md`** FRONTIER  
2. **`MEMORY.md`** TOP (disk)  
3. **`HANDOFF.md`** CURRENT block  
4. **`CLAUDE.md`** principles + how-we-work + DRIVER TRIGGERS  
5. **`CANON.md`** / **`NEGATIVES_REGISTRY.md`** as needed  
6. This INDEX → specific result docs  

---

## Live simple-metric spine (root)

| Role | Files |
|------|--------|
| Foundation | `SIMPLE_METRIC_MACRO.md`, `simple_metric_FE_rederive.py` |
| Frame / method | `UDT_ELEGANT_FRAME.md`, `UDT_METHOD_MUSIC.md`, `UDT_DOTTED_LINE.md`, `UDT_ELEGANCE_UNCOVER.md` |
| L form (canon+audit) | `CANON.md` **C-2026-07-09-1/1a**, WR-L results, external audit |
| Center no-go / atlas | `simple_metric_WR_L_center_nogo_atlas_results.md` |
| Center invariants (2nd pass) | `simple_metric_WR_L_center_invariants_second_pass_results.md` |
| Re-center ⊥ center (3rd) | `simple_metric_WR_L_center_recenter_exclusion_results.md` |
| EOS power window / dS | `simple_metric_EOS_power_window_dS_results.md` |
| Charles rulings (A)+dS heuristic | `simple_metric_Charles_rulings_center_dS_2026-07-09.md` |
| Center/dS verify pass | `simple_metric_center_dS_external_verify_pass_results.md` |
| dS any-α closed | `simple_metric_dS_native_any_alpha_closed_results.md` |
| α restoring probe | `simple_metric_alpha_restoring_probe_results.md` |
| Thread B cell charter | `threadB_coupled_cell_flatness_Lselector_CHARTER.md` |
| Thread B workstation one-pager | `threadB_WORKSTATION_DISPATCH.md` |
| Thread B f2d drain MAP | `threadB_f2d_drain_solver_first_MAP.md` |
| Thread B non-round+topo audit | `threadB_f2d_nonround_topological_audit_results.md` |
| Thread B mirror-vs-wall dispatch | `threadB_WORKSTATION_DISPATCH_mirror_vs_wall.md` |
| Thread B mirror-vs-wall results | `threadB_f2d_mirror_vs_wall_results.md` |
| Time-live linear no-go + finite-amp | `threadB_timelive_linear_nogo_and_finite_amp_MAP.md` |
| Matter carrier provenance | `matter_carrier_provenance_audit_results.md` |
| Hopfion mass / ambient-φ MAP | `hopfion_mass_background_coupling_MAP.md` |
| Hopfion G/P exterior NEXT charter | `hopfion_GP_exterior_NEXT_CHARTER.md` |
| Hopfion G/P exterior probe results | `hopfion_GP_exterior_probe_results.md` |
| Fixed-Q isorotation MAP / Phase 0–1b | `hopfion_fixedQ_isorotation_MAP.md`, phase0/1/1b results |
| Phase 2 metric backreaction dispatch | `hopfion_WORKSTATION_DISPATCH_phase2_metric.md` |
| Phase 2 metric backreaction results | `hopfion_phase2_metric_backreaction_results.md` |
| G/P switch hopfion dispatch | `hopfion_WORKSTATION_DISPATCH_GP_switch.md` |
| G/P switch apply MAP/results | `hopfion_GP_switch_apply_MAP.md`, `hopfion_GP_switch_apply_results.md` |
| H4·N4rev CF2 box-control | `H4_N4rev_sign_certification_results.md` |
| H/L / optics | `simple_metric_HL_unification_results.md`, `simple_metric_L_native_optical_derive_results.md` |
| Kaleidoscope | `simple_metric_kaleidoscope_MAP.md`, `simple_metric_kaleidoscope_MINE_results.md` |
| BAO / time-live | `simple_metric_bao_*`, `simple_metric_timelive_*` |
| Time-live appearance MAP | `simple_metric_timelive_residual_appearance_MAP.md` |
| Time-live AP exact derive | `simple_metric_timelive_AP_exact_derive_results.md` |
| SNe / cascade history | `simple_metric_pantheon_*`, `simple_metric_mass_xmax_cascade.md`, … |
| Orientation | `LIVE.md`, `MEMORY.md`, `HANDOFF.md`, this INDEX |
| Discipline | `CLAUDE.md`, `.claude/skills/`, `tests/` |

---

## Durable ledgers (never archive)

- **`CANON.md`** — Charles-canonized statements (append-only)  
- **`NEGATIVES_REGISTRY.md`** — premise-scoped negatives  
- **`CLAUDE.md`** — working charter  

---

## Repo layout (short)

- **root** — live simple-metric docs/scripts + orientation + still-imported solver modules (pytest)  
- **`grok/quarantine_free_DA/`** — free-\(D_A\) / mixed scoreboards (quarantined)  
- **`archive/`** — sediment + **archived startup layers** (this trim):  
  - `LIVE_historical_frontier_through_2026-07-08.md`  
  - `INDEX_pre_simple_metric_WR_L_2026-07-09.md`  
  - per-arc `LIVE_*.md`  
- **`HANDOFF_ARCHIVE.md`** — superseded HANDOFF session blocks  
- **`legacy/`**, **`prototype/`** — retired / reference code  

**Pre-native coupled era:** `pre_native_era_census.md`; docs in `archive/pre_native_coupled/`.

---

## Full pre-lean INDEX

The long 2026-07-01 cell/solver/hopfion map (sections 1–4 + arc lists) is preserved at:

**`archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md`**

Do not treat it as the live frontier map.
