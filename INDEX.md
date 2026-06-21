# INDEX — Repo Map

Navigable map of udt_mass_codex. Created 2026-06-10. Layout note: the repo
is deliberately FLAT — ~474 `native_*.py` scripts plus 13 markdown docs in
one directory. See "Conventions" at the bottom before judging the layout.

Reading order (2026-06-21): CLAUDE.md "How we work" + ANTI-HANG -> **HANDOFF.md TOP** (the live
2026-06-21 FOUNDATIONAL-ASSUMPTIONS-AUDIT frontier) -> **FOUNDATIONAL_ASSUMPTIONS_LEDGER.md** (F0-F8,
the live work) -> **POST_POSTULATE_PROGRAM.md** (the corrected program) -> **SOLVER_COMPLETENESS_MAP.md**
(the live solver instrument) -> STATE.md TOP -> this file -> the records.
LIVE WORK (2026-06-21): FOUNDATIONAL-ASSUMPTIONS AUDIT (FOUNDATIONAL_ASSUMPTIONS_LEDGER.md, F0-F8, tasks
#23-31). Several recipes the program rests on were carried SILENTLY (deepest = the gravity-side curvature
action assumed = GR through all of P1-P5d). The forward build (P5e fully-coupled time solve / quantization
Step B/C) is PAUSED pending the audit (it builds on the assumed curvature operator). KEY LINKAGE: the central
result (classical metric = CONTINUUM => must quantize) is conditional on this stack. CONTEXT (the prior arc,
2026-06-20): the everything-on solver is BUILT + the classical metric shown to be a continuum + quantization
Step A confirmed (intrinsic discreteness, escapes box-control; spin-1/2 stays a postulate). Build docs:
FOUNDATIONAL_ASSUMPTIONS_LEDGER.md, EVERYTHING_ON_SOLVER_*_MAP.md (incl. _P5e), p1_*/p2_*/p3_*/p4_*/p5*_*/
p5c_*/p5d_*/quant_stepA_*/offround_classical_* results + _VERIFIER docs. See HANDOFF TOP + memories
everything-on-solver-build + solver-audit-rework-welcome for the distilled state + the capability gap.
NOTE (reframe): the pre-postulate MICROPHYSICS records below are RETIRED/legacy — the microphysics space is
UNENTERED, not walled (NEGATIVES_REGISTRY wholesale-retirement banner + STATE TOP). Mine for TOOLING only, never verdicts.

---

## 1. Document layer (13 markdown files)

### Charter and frontier (read first, always)

- **CLAUDE.md** — Working charter: Charles's binding principles (1-7), the
  Self-Hardening repo discipline (append-never-edit, verifier-before-record,
  pre-registration), orientation pointers. Read FIRST, every session.
- **POST_POSTULATE_PROGRAM.md** (2026-06-19 LATE, DRAFT) — THE CORRECTED FORWARD PLAN,
  supersedes VISION_POST_POSTULATE.md. The reframe: the microphysics space is UNENTERED
  (the legacy negatives are facts about contaminated/classical TOOLS, not the metric;
  retired wholesale). Program = solve the whole CLEAN metric with EVERYTHING ON + the
  postulates as STRUCTURE, OBSERVE, quantize; solver-first on any mismatch, never a
  mechanism hunt. Read after CLAUDE.md "How we work". (Awaiting Charles's sign-off.)
- **SOLVER_COMPLETENESS_MAP.md** — the LIVE INSTRUMENT: every DOF/term/coupling/boundary,
  marked on/off/frozen/never-built, postulates as incorporated structure, with the
  tool-provenance (cleanest building blocks) wired in. Gates trust in any result.
- **VISION_POST_POSTULATE.md** (2026-06-19) — [SUPERSEDED by POST_POSTULATE_PROGRAM.md].
  The compiled recon + post-postulate-A vision (two-halves status, catalog-as-distinct-
  objects hypothesis, ordered path). RETAINED as history; its microphysics framing
  ("walled half", the catalog spine) is the frozen misinterpretation the reframe corrects.
  Its COSMOLOGY half (§I) is unaffected and still the strong, metric-pure layer.
- **STATE.md** — Frontier snapshot: one-paragraph program status, the five
  open gates, banked negatives, near-misses, active priority queue.
  Updated at every session close. Read SECOND.

### Microphysics research records (RETIRED/legacy as of 2026-06-19 — mine for TOOLING only, never verdicts; the microphysics space is UNENTERED)

- **negative_phi_native_geometry.md** (31k lines, sections 0-434) — The
  pre-spectrum research record: native negative-phi geometry rebuilt from
  the metric alone (no Form-T, no Dirac, no SM imports). Pattern: one
  numbered section = one result = one immutable script ("Implemented in
  `<script>.py`"). Contains the q=1/3, eta=1/18, and N=3 derivations and
  the full phi0-boundary/DtN/transfer campaign. Read via section headers
  (`grep '^## '`), not linearly.
- **particle_spectrum_native_geometry.md** (sections 1-43) — The spectrum
  stage, started after pre-spectrum closure: H1 operator alphabet
  End(H1)=1+3+5, commutator two-form selector, W(P)=Tr(P)/12, taxonomy
  skeleton, radial-coupling gates. Same section=script pattern. Read after
  (or instead of) the pre-spectrum record when working spectrum questions.

### 2026-06-10 audit cycle (working audits, not canonical)

- **dimension_ladder_null_audit.md** — Prices the evidential weight of the
  exact-rational identity ledger (`null_test_dimension_ladder.py`): only
  two independent locks survive, ~1/37 chance level; small-rational
  coverage 16-23%. Read before banking any new exact identity.
- **sector_weight_spectral_probe_results.md** — Direct test of the parked
  sector-dependent q(P) eigenvalue mechanism
  (`native_sector_weight_spectral_probe.py`): DEAD, 59/60 misses.
- **p_domain_closure_attempt_results.md** — P_domain closure attempt and
  honest failure (`native_source_share_boundary_identity_audit.py`):
  value-pinning route failed adversarial verification; P_domain stays open
  on three premises.
- **lepton_ladder_falsification_contract.md** — PRE-REGISTRATION (frozen
  model, candidate lists, tolerances, look-elsewhere) committed BEFORE the
  lepton test ran. Template for all future falsification tests.
- **lepton_ladder_test_results.md** — Outcome of the frozen test
  (`native_lepton_ladder_frozen_test.py`): muon +2.3%, tau -48% bare;
  ladder under falsification pressure; required corrections fall between
  eta-ladder rungs.

### Audit / prosecution layer

- **mass_emergence_canonical_geometry.md** — The hard audit record and
  binding Self-Hardening Protocol; graded the legacy mass sector (verdict:
  no unfittable prediction survived). Re-read before editing anything;
  rebuild work is graded AGAINST its verdicts.
- **UDT_REBUILD.md** — Clean canonical statement of rebuilt UDT geometry
  (sessions 6-8); replaces the old corpus; not Charles-canonized. Its
  companion docs (UDT_REBUILD_History.md, HANDOFF_SESSION.md) are NOT in
  this repo.

### Legacy (superseded — mine for structure only, never re-import)

- **legacy_hadron_survivor_filter.md** — The filtering strategy for mining
  legacy hadron material without re-importing the Dirac Form-T scaffold.
  Read this BEFORE opening the legacy corpus.
- **udt_canonical_geometry.md** (6.8k lines) — The old corpus; suspect
  labels, retraction banners. Access only through the survivor filter.

---

## 2. Script layer (~474 scripts, flat, immutable once committed)

Families by filename pattern (counts approximate; many scripts straddle
two themes — the doc section that cites a script is its true home).
"Load-bearing" = the scripts the markdown records hang core results on.

### Collar / q-flow & source law (~37: `*collar*`, `*q_flow*`, `*source*`)
Derivation of q=1/3 as the collar-flow fixed point and the source law
s(q)=q/3. Load-bearing: `native_minimal_q_flow_candidate.py`,
`native_derived_q_flow.py`, `native_q_flow_source_running.py`,
`native_h1_source_law_constructibility.py`,
`native_collar_h1_action_accept_reject_gate.py`,
`native_collar_h1_action_candidate_scan.py`,
`native_h1_transport_vs_collar_source.py`,
`native_curvature_share_action_no_go.py`,
`native_source_share_boundary_identity_audit.py`.

### Boundary / phi0 functional & momentum (~91: `*phi0*`, `*boundary*`, `*momentum*`, `*edge*`)
The phi0 interface campaign: boundary momentum, exact local boundary
forms, GHY/Brown-York/Robin candidates, functional requirements.
Load-bearing: `native_boundary_momentum_h1_projection.py`,
`native_phi0_boundary_functional_requirements.py`,
`native_exact_local_boundary_form.py`,
`native_exact_scale_normalized_boundary_momentum.py`,
`native_phi0_boundary_candidate_scorecard.py`,
`native_boundary_functional_q_correction.py`,
`native_phi0_boundary_layer_requirements.py`.

### H1 operator algebra & two-form selector (~61: `*h1*`, `*twoform*`, `*commutator*`, `*selector*`, `*taxonomy*`, `*channel*`, `*trace*`)
The spectrum-stage core: End(H1)=1+3+5, commutator selector, N=3 lock,
particle-taxonomy skeleton. Load-bearing:
`native_h1_operator_algebra.py`, `native_twoform_selector_n3_lock.py`,
`native_endh1_commutator_twoform.py`,
`native_commutator_isotropy_c1_weight.py`,
`native_prespectrum_dimension_ladder.py`,
`native_particle_taxonomy_skeleton.py`,
`native_twoform_functional_selector_audit.py`,
`native_h1_area_form_projector_bridge.py`, `native_n3_pq_bridge_gate.py`.

### Angular sector & monopole (~21: `*angular*`, `*monopole*`)
Angular admissibility, invariants, RG/staging, the angular bridge to eta.
Load-bearing: `native_monopole_angular.py`,
`native_angular_admissibility.py`, `native_angular_invariants.py`,
`native_angular_diophantine_survivor_audit.py`,
`native_angular_invariant_bridge_phi_spaces.py`.

### Eta / epsilon & C1 variational (~25: `*eta*`, `*c1*`, `*variation*`, `*activation*`)
eta=1/18 candidates, derivation/generalization, C1 variational options.
Load-bearing: `native_eta_candidate_audit.py`,
`native_eta_derivation_attempt.py`, `native_eta_generalization.py`,
`native_scalar_projection_eta.py`, `native_eta_epsilon_route.py`,
`native_eta_gamma_chain_current.py`,
`native_exact_c1_variational_options.py`.

### Transfer / gamma ladder & typed depth (~57: `*transfer*`, `*gamma*`, `*typed*`, `*depth*`, `*ladder*`, `*epsilon*`, `*branch*`)
The mass-ladder machinery: gamma = 3·exp(-1/36), transfer-matrix models,
typed branch graphs, Tier C/D ladder. Load-bearing:
`native_mass_ladder_candidate.py`, `native_universal_gamma_audit.py`,
`native_transfer_matrix_model.py`, `native_typed_branch_graph_current.py`,
`native_typed_graph_mass_diagnostic.py`,
`native_tier_c_symbolic_ladder.py`,
`native_tier_c_to_d_coefficient_requirements.py`,
`native_upgraded_transfer_conditional_theorem.py`.

### Hessian / DtN / Calderon (~16: `*hessian*`, `*dtn*`, `*calderon*`, `*schur*`)
GR-corpus boundary machinery under positional dilation. Load-bearing:
`native_dtn_calderon_phi0_audit.py`,
`native_warped_dtn_identity_preservation.py`,
`native_warped_dtn_hessian_spectrum.py`,
`native_warped_collar_operator_obstruction.py`,
`native_positional_dilation_calderon_refactor.py`,
`native_boundary_hessian_constructibility_audit.py`.

### Spectra & solvers (~17: `*spectrum*`, `*eigen*`, `*mode*`, `*kernel*`, `*solver*`)
Numerical spectra; home of the box-control negative. Load-bearing:
`native_scalar_spectrum.py`, `native_cell_spectrum.py`,
`native_sector_weight_spectral_probe.py`,
`native_h1_edge_kernel_eigenvalue_audit.py`.

### Orchestra & sector interaction (~14: `*orchestra*`, `*sector*`, `*interaction*`)
The ensemble structure (principle 5): interaction matrix, ablation,
locality. Load-bearing: `native_orchestra_interaction_matrix.py`,
`native_orchestra_ablation.py`, `native_orchestra_graph_current.py`,
`native_orchestra_residual_separation.py`.

### Metric atlas / GR-corpus mining (~11: `*metric*`, `*gr_*`, `*atlas*`)
What the metric is already doing; fan-out scans for uncovered functions.
Load-bearing: `native_metric_fanout_atlas.py`,
`native_metric_already_doing_inventory.py`,
`native_gr_metric_corpus_second_look.py`.

### Postulate ledgers & status / decision records (~28: `*postulate*`, `*ledger*`, `*status*`, `*decision*`, `*gate*`)
Machine-readable snapshots of what is assumed vs derived. Load-bearing:
`native_minimal_postulate_budget.py`,
`native_two_postulate_working_model.py`,
`native_active_lane_postulate_ledger_after_tier_c.py`,
`native_final_prespectrum_postulate_status.py`,
`native_spectrum_path_decision.py`.

### Audits & no-gos (~43 named `*audit*`/`*no_go*` outside the families above; ~105 total carry "audit")
Adversarial checks and closure proofs of dead routes; every banked
negative has one. Examples: `native_bare_measure_coefficient_no_go.py`,
`native_anchor_alternative_audit.py`,
`native_boundary_constraint_origin_audit.py`.

### Null tests & falsification (~6: `null_test_*`, `*lepton*`, `*falsification*`, `*frozen_test*`, `*probe*`)
The repo's discipline weapons. Load-bearing:
`null_test_dimension_ladder.py`, `native_lepton_ladder_frozen_test.py`,
`native_lepton_ratio_falsification_contract.py`,
`native_lepton_ratio_diagnostic_lane.py`,
`native_sector_weight_spectral_probe.py`.

### Misc exact identities (~47: endpoint, topology, constraint counting, curvature share)
E.g. `native_endpoint_self_similarity.py`, `native_flux_topology.py`,
`native_one_third_equivalence_triangle.py`,
`native_p_domain_dirichlet_principle.py`.

---

## 3. Load-bearing results: result -> script(s) -> doc section

| Result | Script(s) | Doc section |
|---|---|---|
| q=1/3 as collar-flow fixed point | `native_minimal_q_flow_candidate.py`, `native_derived_q_flow.py` | negative_phi §141, §143 |
| q-flow robustness under source running | `native_q_flow_source_running.py` | negative_phi §150 |
| eta=1/18 candidate, audit, generalization | `native_eta_candidate_audit.py`, `native_eta_derivation_attempt.py`, `native_eta_generalization.py`, `native_scalar_projection_eta.py` | negative_phi §37-39, §111 |
| N=3 native from the H1 area form | `native_h1_area_form_projector_bridge.py`, `native_eta_epsilon_route.py` | negative_phi §415, §40 |
| N=3 lock of the two-form match | `native_twoform_selector_n3_lock.py` | spectrum §7 |
| End(H1)=1+3+5 operator alphabet | `native_h1_operator_algebra.py` | spectrum §1 |
| Commutator two-form; W(P)=Tr(P)/12 | `native_endh1_commutator_twoform.py`, `native_commutator_isotropy_c1_weight.py` | spectrum §9-10 |
| Dimension-ladder evidential weight: 2 locks, ~1/37 | `native_prespectrum_dimension_ladder.py`, `null_test_dimension_ladder.py` | spectrum §6; dimension_ladder_null_audit.md |
| Box-control NEGATIVE (no native discreteness) | `native_scalar_spectrum.py`, `native_cell_spectrum.py` | negative_phi §8, §20; STATE banked negatives |
| Sector-dependent q(P) eigenvalue route DEAD | `native_sector_weight_spectral_probe.py` | sector_weight_spectral_probe_results.md (context spectrum §23-26) |
| P_domain still open; value-pinning failed verifier | `native_source_share_boundary_identity_audit.py` | p_domain_closure_attempt_results.md; negative_phi §393, §432 |
| Bulk scalar action for s(q)=q/3: no-go | `native_curvature_share_action_no_go.py` | p_domain_closure_attempt_results.md |
| B(F,Q,H1) derivative-sensitive boundary target | `native_derivative_joint_term_audit.py`, `native_h1_source_law_constructibility.py` | negative_phi §396-397 (verdict 382) |
| Frozen lepton test: muon +2.3%, tau -48% | `native_lepton_ladder_frozen_test.py` | lepton_ladder_test_results.md (pre-reg: lepton_ladder_falsification_contract.md) |
| Tier-D coefficient targets C_M1, C_E1, ratio | `native_lepton_ratio_diagnostic_lane.py`, `native_tier_c_to_d_coefficient_requirements.py` | lepton contract §"Known-limitation"; negative_phi §316 |
| gamma = 3·exp(-1/36) ladder + universality audit | `native_mass_ladder_candidate.py`, `native_universal_gamma_audit.py` | negative_phi §52, §56 |
| Typed branch graph and mass diagnostic | `native_typed_branch_graph_current.py`, `native_typed_graph_mass_diagnostic.py` | negative_phi §136-137 |
| Warped DtN preserves ell=1 identity triplet; transfer fork | `native_warped_dtn_identity_preservation.py`, `native_dtn_calderon_phi0_audit.py` | negative_phi §251-252, §239 |
| Boundary momentum H1 projection (eta/2 carrier) | `native_boundary_momentum_h1_projection.py`, `native_exact_scale_normalized_boundary_momentum.py` | negative_phi §160, §171 |
| Final pre-spectrum postulate status | `native_final_prespectrum_postulate_status.py` | negative_phi §434 |

---

## 4. Conventions (why the repo looks like this)

- **Flat layout is deliberate.** Docs cite scripts by bare filename
  ("Implemented in `native_x.py`"); no subdirectories, so citations never
  break.
- **Committed scripts are immutable; research-record docs are
  append-never-edit.** New work = NEW files, always (CLAUDE.md, "Repo
  discipline").
- **One section = one script.** Each numbered section in the research
  records names exactly one script whose output reproduces every number
  in that section. To find a result's code: grep the doc for the section,
  read its "Implemented in" line.
- **Verifier-before-record and pre-registration** are binding: results
  get a blind adversarial verifier pass before commit; falsification
  tests are pre-registered (see lepton_ladder_falsification_contract.md).
- Section numbers and "verdict" numbers in negative_phi differ (verdicts
  count results, sections count headers); audit docs cite both.
- Commit per result; push to github.com/charlesrotter/udt_mass_codex.
