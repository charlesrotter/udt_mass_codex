# UDT Mass Codex — Codex Working Instructions

Charles canonizes. Nothing enters `CANON.md` without his explicit sign-off.
This repository is an evidence ledger, not a place to turn a promising lead into a stronger claim.

## Mandatory startup

Work on branch `grok`. Do not trust a hash, branch count, or status quoted in a prompt or handoff.
At the start of every fresh session run, in order:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

If a pull is blocked by local work, preserve and inspect that work. Never reset, overwrite, clean, or
stash user changes merely to make the pull succeed. If an untracked file collides with an identical
upstream file, prove that it is byte-identical and preserve a backup before moving it aside.

Known workstation caveat: `udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/` may appear
as 83 protected untracked paths. It is local curvature/holonomy atlas work product, not current
authority and not pushed to `grok`. Do not stage, modify, delete, mine, or cite it without an
explicit later dispatch. A clean clone may not contain it.

Before interpreting the frontier, read from disk in this exact order. **Bounded-startup rule:**
do not dump whole long files or recursively open cited evidence during orientation.

1. `LIVE.md` — read only `STARTUP_CURRENT_BEGIN` through `STARTUP_CURRENT_END`; it overrides every
   other status description.
2. `HANDOFF.md` — read only its matching current block.
3. `CURRENT_RESEARCH_PROGRAM.md` — the active dependency spine and bounded next question.
4. `CURRENT_SCIENTIFIC_PREMISES.md`, then `CURRENT_SCIENTIFIC_PREMISES.tsv` — the source-precedence
   registry for high-risk terms. Any disagreement with LIVE or a cited source is a mandatory stop.
5. **ACTIVE ARC (2026-08-10): CMB PEAK OPTIMIZATION.** First read
   `udt_multiregime_pair_relation_admissibility_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_ordered_observer_query_projection_ownership_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_multichannel_observer_relation_assembly_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_stationary_local_one_form_selection_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_depth_holonomy_joint_invariant_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_pair_leaf_normal_holonomy_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_nonisometric_calibration_magnitude_owner_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_carried_intrinsic_middle_morphism_ownership_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_branch_nonisometric_calibration_transition_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_global_relation_family_branch_classification_2026-08-10/AUDIT_REPORT.md`, then
   `udt_three_observer_overlap_calibration_carry_audit_2026-08-10/AUDIT_REPORT.md`, then
   `udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md`, then
   `udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md`, then
   `udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md`, then
   `udt_reciprocal_calibration_state_solder_audit_2026-08-09/AUDIT_REPORT.md`, then
   `udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/AUDIT_REPORT.md`, then
   `udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md`, then
   `udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md`, then
   `udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md`, then
   `udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md`, then
   `udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md`, then
   `udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md`. The corrected 462-row atlas
   has three interleaved equatorial ladders, and the old same-index `OPEN-COMPATIBILITY-WINDOW` is
   WITHDRAWN. The ownership audit proves that those roots do not lift unchanged into the conditional
   complete spherical operator; axial `m` survives only in symmetry-preserving representatives,
   and no metric-only population projector is selected. The family-atlas MAP derives the general
   stationary screen-plus-shift operator and maps 18 families plus all 2,800 axis cells without
   selecting a screen. N01 is now complete and `VERIFIED-WITH-CAVEATS`: it derives the exact
   conditional fixed-`|m|`/parity matrix architecture and full radial matrix flux, not a physical
   screen or spectrum. N02 is complete and `VERIFIED-WITH-CAVEATS`: no banked P1 row is a regular
   complete spherical center-to-wall anchor; this does not invalidate P1's declared relational/SNe
   role. Mixed walls require a free extension family and D/N are not selected. N03 is now complete
   and `VERIFIED-WITH-CAVEATS`: the observer-pair law is not a centered local lapse; no mapped source
   supplies a complete global profile; a nonempty smooth C1 local jet space remains compatible with
   mu on; and the physical groupoid cocycle stays open. The subsequent reciprocal-flag audit derives
   the abstract reciprocal calibration seed and an exact conditional flag character. The solder
   audit derives the associated calibration line, conditionally constructs regular pair directions,
   proves canonical local metric transport has zero depth, and leaves the general physical state
   bilocal/global/branch/dynamical. The terminal pair-metric audit derives the unique reciprocal
   log imbalance only on a supplied regular A-calibrated pair metric. The completed pair-map atlas
   derives a local orthogonal exponential tube from the metric plus a full declared query and
   regular branch, but finds no universal pair map from bare endpoints. The founding ownership
   audit derives the character on supplied ordered depth and classifies the complete query as a
   conditional enrichment. The three-observer audit derives carry associativity only on matched
   enriched objects, separates direct-equals-composite as Cech descent/path independence, and
   leaves global relation-family ownership plus scalar reduction open. The complete-branch census
   retains path/holonomy, endpoint-clock, and stratified projector families. Its branch-transition
   follow-up finds that R17's exact semidirect formula is a lawful conditional assembly, not a
   branch-owned physical law; zero complete branch-owned non-isometric transitions survive. The
   middle-morphism follow-up derives the path-labelled `SO(2)` alignment bitorsor and exact balanced
   projector composition without selecting a screen phase. The scalar-descent follow-up proves
   that supplied reciprocal density/readout data descend through that bitorsor on all six regular
   strata, with exact balanced telescoping; isometric alignment generates zero calibration, so the
   physical non-isometric magnitude and its owner remain open. Its controlling source is
   `udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md`. The
   subsequent magnitude-owner census finds exactly two branch-conditional endpoint clock
   magnitudes, R17 and R18, but zero complete physical owners. The R17 selector follow-up then fixes
   the branch-internal vertical reciprocal metric class modulo `SO(2)` conditional on each supplied
   complete off-shell C01--C06 coframe. It does not select a physical cross-fibre arrow; R18 still
   lacks a ruler completion. The R17 foliation follow-up then derives the global `S2`-parametrized
   family of `R x S1` pair leaves, their complete twisted determinant-`-1` metric, and same-leaf
   `delta_K`; its 4D angular plane remains a nonintegrable normal bundle. It does not select a leaf,
   winding, cross-leaf comparison, normal carry, holonomy/reset, or physical complete arrow. The
   completed normal-holonomy follow-up then derives the projected leafwise normal connection and
   representative-free closed-loop data; `lambda=-1` flatness and `lambda=0` Hopf-basicness are
   distinct and select neither branch. Cross-leaf path choice and the complete physical arrow stay
   open. The completed path-labelled decomposition now derives the full projected connection in
   all four directions, all six curvature planes, and exact isometric transport after a path is
   supplied. No `lambda` is generically completely flat or base-descended. The later audits listed
   above complete the stationary sublocus and scalar-projection chain. G55 maps the 24 pinned branch
   identities into 11 mathematical apparatus patterns but derives no physical regime map; R04 is
   a member-dependent aggregate and must not inherit one member's panel. The current open decision
   is time-live/on-shell, global descent, bootstrap closure, or an explicit observer-query premise.
   No profile repair,
   inner cutoff, eigenvalue solve, or FD2 is authorized. Then read
   `udt_freedata_inventory_MAP_2026-08-09.md` as the parent FD1-FD4 menu and
   `udt_roadA_mode_quantization_MAP_2026-08-08.md` with the RA1/RA2 packages (the native resonator;
   RA2 = PARTIAL-WEAK). The x_max STRUCTURE (O1-O3) and SCALE (M1-M4) lanes are COMPLETE (verified
   leads; the fitted background R_w~2.2 Gpc, n~1.056); the BAO lane is BANKED + TABLED (M1-M3d done;
   resume-build = a broadband fair mock, in the M3d package). Lineage/foundation to build FORWARD
   from (LIVE's 2026-08-09 block §1-6 routes these): `udt_complete_pair_phi_orchestra_audit_2026-08-05/`
   (phi+orchestra), `udt_ceff_depth_orchestra_integration_2026-08-06.md` (c_eff reframe; the
   two-point ratio is the invariant), [[mu-on-is-the-default]] (mu turned on — the inertia ruling).
   The Global Cell Assembly lane is ARCHIVED-LEGACY (`archive/global_cell_assembly_2026-08-06_legacy/`)
   -- do not reach into the pre-orchestra corpus without an explicit re-grade. Also read
   `INFLIGHT_STATE.md` (the live resume ledger; currently: NOTHING in flight — clean stop).
6. `udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md` for current observer-pair,
   `phi`, angular-orchestra and physical-cocycle orientation; then exact evidence only to the depth
   required by the user's task.

7. When mass emergence, stability, branch response, or particle history is relevant, read
   `udt_scientific_arc_recovery_checkpoint_2026-08-04/MASS_BRANCH_AUTHORITY_MAP.tsv` first. It is the
   seven-entry plural-branch authority map. Then use its cited reconciliation evidence and
   `stability_branch_follow_256_DECISION.md` only to the depth required; neither is the global
   frontier.
8. `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and repo discipline only.
9. Only the specific protocol under `.claude/skills/*/SKILL.md` triggered by the actual task.
10. `INDEX.md` and `MEMORY.md` for compact pointers only; neither can overrule LIVE.

`UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` is a historical compatibility path, not a generic startup
read. Open it only when a task makes its dated evidence load-bearing. Its exact root path is retained
because historical verifiers depend on it.

**Compact semantic regression guard:** the founding character acts on **supplied ordered depth**;
pointwise `phi` is a presentation potential on the supplied factorization, not a claimed universal
physical scalar. On a supplied fixed calibrated pair metric, the terminal reciprocal log imbalance
is derived and angular/mixing data enter the pullback before readout; the pair map and calibration
owner are not derived, and the mixed-geometry physical `c_eff` remains conditional. The
complete-arrow strain and angular/mixing modulation result is derived structural evidence, and
exact physical signed reciprocal depth belongs in an owned typed observer/path cocycle; neither
selects the unique physical cocycle. `CHOSE_COMPARISON_CONFIGURATION` remains
comparison-only;
`CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` keeps strong local CSN inactive. The generic metric count is
a generic configuration-arena count. `X_max` is a `WORKING_FOUNDATIONAL_FRAME` for the
positional-dilation asymptote, not a material wall, preferred center, radial edge, or finite-cell
seal. The mass branch map is plural: F01/F02 are distinct conditional geometry-only candidates, F04
is carrier/action/box-conditional, and F03/F05/F06/F07 are nonfamily support classes. No candidate
reading is physical UDT mass. Authoritative fields and sources are in
`CURRENT_SCIENTIFIC_PREMISES.tsv`.

**Current spectral regression guard:** the corrected FD1 scalar atlas contains three interleaved
equatorial ladders. The old same-index `OPEN-COMPATIBILITY-WINDOW` is WITHDRAWN. The complete-angular
ownership audit is now the controlling correction: the full spherical lift changes the radial
operator and generically couples `(r,theta)`; fixed-`ell`, not equal FD1 index, owns a round `SO(3)`
multiplet; admitted screens may lack any axial `m`; symmetry projection is not population
weighting. Do not call an equal-index `m=-1,0,+1` bookkeeping triple a physical multiplet,
postselect the best standalone ladder, assume `m=0` dominance, promote the chosen C1 lift to native,
or promote the scalar `Box_g` atlas into native dynamics. FD2 remains gated.

The complete-angular family-atlas MAP is an architecture/regression gate only. A general angular
shift has an additional shift-divergence term absent from the special axial formula. Do not apply
the axial shortcut universally, treat a family disposition as physical merit, splice conditional
S3 controls into WR-L, or promote C1 to the native screen. The N01 C1 coupling atlas is conditional
wiring only: do not promote scalar `Box_g`, discard negative-`m` sign, call bounded matrix reach a
spectrum, or launch FD2/GPU work without a separate preregistered gate. N02 is an admissibility
gate only: do not invalidate P1's relational/SNe role, call `h=O(r^2)` sufficient for full
smoothness, select D/N physically, repair P1, insert an inner cutoff, or launch an eigensolve.
N03 is the controlling profile-role correction: retain the two-point `c_eff` ratio, the disclosed
reference-observer readout, phi+orchestra, mu on, the full N01 matrices, C01-C18 screen arena, and
the general shift-divergence term. Do not copy P1 directly into a smooth centered lapse, promote
local jets to a global solution, select `k0`, derive transport from cocycle regularity, or turn
`X_max` into a wall.

For the 1,114 fixed-base artifact identities, use
`research/_registry/CURRENT_ARTIFACT_PATHS.tsv`. Post-base additions such as the July 19 frontier and
audit packages are outside that fixed universe; use their direct tracked paths named by `LIVE.md`
rather than expecting registry rows. The R0–R1C ownership, readiness, census, preregistration, and
verification records are fixed historical snapshots and must not be rewritten to mimic current
paths. This is an operational navigation rule; like every instruction in this file, it cannot
overrule `LIVE.md`.

Then give Charles a short orientation report: actual HEAD and dirt, the current honest claim, its
premise stamps, the open gate, and the proposed bounded next action. Do not mutate files or launch a
long solve until that orientation is complete.

Scientific status belongs in `LIVE.md`, `CURRENT_RESEARCH_PROGRAM.md`, and the current premise
registry—not in this operational file. Historical startup/status prose is quarantined in
`archive/startup_orientation_history_2026-08-05/AGENTS.pre_cleanup.md`.

## Codex/Claude compatibility

`CLAUDE.md` and `.claude/skills/` contain binding project method even though their names are
Claude-specific. Read and apply them manually when their trigger applies. Codex must not assume that
`.claude/hooks/corral_trigger.py`, Claude project memory, background jobs, or Claude skill auto-loading
are active. The corresponding pauses are therefore manual and mandatory:

- before a solve: observing or targeting; whole frame or bounded slice; every physical choice tagged;
- before explaining a mismatch: solver completeness before any new mechanism;
- before a commit or verdict: preregistration, bounded scope, independent verification of the
  load-bearing premise, and premise audit;
- before words such as *proved*, *settled*, *stable*, *single basin*, *native*, or *derived*: state the
  exact regime and the remaining open scope.

Do not rely on conversational memory. Disk evidence wins.

## Binding UDT research rules

- Remain pure to UDT: **the metric is the theory**.
- The founding source derives the exact reciprocal character
  `D(delta)=diag(exp(-delta),exp(delta))` on **supplied ordered depth**. It does not derive the map
  from complete observer/event/path data to `delta`. Pointwise `phi` is a presentation potential on
  the supplied factorized architecture and may become physical only on a separately selected
  endpoint-exact branch. Never demote the character to a placeholder or promote pointwise `phi` to
  a universal physical scalar or extra native field.
- The complete A-to-B comparison has a derived frame-covariant strain object. Angular/screen/mixing
  structure can modulate one A-to-B relational depth inside the complete comparison, and exact
  reciprocal depth structurally belongs in a real observer/path groupoid 1-cocycle. The metric has
  not selected the unique physical cocycle. Never treat the older equal-pointwise-`phi` angular
  counterexample as refuting a complete relational `phi_AB`, and never promote strain, a spectral
  norm, or the conditional stationary screen-modulated family to the physical law.
- `X_max` is the `WORKING_FOUNDATIONAL_FRAME` for the frame-shared observer-pair
  positional-dilation asymptote. Its exact separation/depth law, approach profile, all-frame theorem,
  value, WR-L/global join, angular/bootstrap modulation, and boundary completion remain `OPEN`.
  Passing the asymptote is necessary but does not select tanh, fractional-linear, WR-L, or any other
  profile. Never turn the limit into a preferred center, material wall, finite-cell seal, or boundary
  term.
- Independently varying a scalar in an older atlas is `CHOSE_COMPARISON_CONFIGURATION`, not native
  field ownership. A generic `F4[6]` metric quotient is a **generic configuration-arena count**, not
  a UDT propagating-mode count or selected native field census.
- Strong local CSN is `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` and inactive unless Charles explicitly
  reauthorizes that counterfactual premise. Common-factor cancellation is algebra, not a local Weyl
  gauge theorem. Measured `c_E` and `G_obs` remain observational anchors in the calibrated
  physical-metric reading.
- Before banking any field census, action selector, scale argument, bootstrap claim, Maxwell-like
  claim, carrier result, `X_max` result, or mass/source/boundary claim, run
  `python3 verify_current_scientific_premises.py` and cite the controlling registry row.
- Trace every claimed result explicitly to the UDT metric and the stated matter carrier.
- Keep the macro WR-L lane separate from the particle-mass/carrier lane.
- Do not import Lambda-CDM, Standard Model physics, quantum mechanics, QED, GR field equations,
  fluids, Q-balls, boson stars, or textbook mechanisms as UDT derivations. They may be comparison or
  readout tools only, clearly labeled.
- The `S^2` carrier is a `POSIT`, not a derived necessity. A replacement or emergence remains open.
- The conditional conformal-Lorentzian null-direction fiber is a celestial topological/conformal
  `S^2`; it does not by itself derive the carrier's fixed round target, section, transport, action,
  or boundary completion.
- An EH metric-only action is `CONDITIONAL` through the stated minimality premise; it is not native UDT
  merely because it is mathematically familiar.
- No fitting, fudge factors, hard physical cutoffs, effective corrections, or invented couplings.
- Numerical controls and consistent discretizations are allowed only when they do not change the
  tested continuum functional.
- Use full nonlinear covariant operators. Do not linearize without a controlled error and an explicit
  scope stamp.
- Audit algebra, signs, boundary conditions, operator provenance, convergence, raw evidence, and code
  before accepting or abandoning an approach.
- Use the labels `DERIVED`, `CHOSE`, `WORKING`, `OPEN`, `CONDITIONAL`, `POSIT`, and `OBSERVED`
  precisely. A numerical result is `OBSERVED`, not automatically physics or canon.
- Raw residual/backward error remains the certification gate. A preconditioned residual may diagnose
  or accelerate, but never silently replace it.

## Method

Default order is `MAP -> OBSERVE -> PONDER -> DERIVE`. MAP and PONDER with Charles are brief and in lay
language. Derivation begins only after the frame, assumptions, and premise ledger are visible and
Charles gives the go.

For every proposed computation, state:

1. the whole question and the exact bounded regime being sampled;
2. whether the question is metric-led or template-led;
3. every physical value, boundary condition, sign, chart, source, carrier, and action premise as
   `free-and-explored`, `pinned-by-THEORY` with a citation, or `pinned-by-HABIT`;
4. what degrees of freedom, sectors, branches, boundaries, and limits are not covered;
5. a preregistered falsification/certification contract and maximum allowed conclusion.

Characterize the solution space; do not filter it to demand a particle, lump, spectrum, smooth shape,
or expected answer. A negative is always premise-scoped. If a premise changes, re-grade every negative
that depended on it.

When a result disagrees with expectation, check in order: omitted terms/sectors/boundaries, numerical
convergence or bugs, frozen degrees of freedom, and incomplete solution-space exploration. Do not add a
mechanism to repair a mismatch.

## Evidence and banking

- Pre-register tests, tolerances, candidates, classifications, and conclusion wording before seeing
  outcomes. Do not retune after inspection.
- Independently recompute the load-bearing quantity from saved artifacts. Hunt circular checks,
  shared-code false independence, vacuous assertions, loose tolerances, and incomplete sampling.
- For a load-bearing result, use a fresh adversarial context and an independent implementation; use a
  different method or model family where practical. A same-code comparison is a regression check, not
  independent evidence.
- Preserve raw stdout/stderr, compact machine-readable outputs, exact commands, versions, parameters,
  array shapes, and SHA-256 manifests for large artifacts.
- Commit one logical evidence change at a time and push `grok`. Edit the canonical live file rather
  than proliferating `v2` scripts; git is the rollback trail.
- Do not edit `LIVE.md` or `CANON.md` unless the current dispatch or Charles explicitly authorizes it.
  Never overwrite grid artifacts; use grid-tagged and branch-tagged filenames.
- Preserve unrelated dirty and untracked files. Never use destructive git or filesystem commands.

Before banking any verdict, explicitly report the four gates:

1. preregistered;
2. full space, or bounded scope justified;
3. independently verified on the load-bearing premise;
4. every premise audited.

If any gate is absent, bank a `LEAD`, `OPEN`, or `VERIFIED-WITH-CAVEATS`, not a settled result.

## Numerical operations

- Use one GPU process at a time. Confirm the selected process, device, dtype, grid, memory estimate,
  output names, timeout, checkpoint/restart behavior, and stop conditions before launch.
- Prefer saved-field recomputation to repeating a relaxation.
- Bound exploratory work. Long production work requires a written dispatch and preregistered gates.
- Check GPU results with independent CPU/symbolic anchors where feasible.
- For corrected-carrier work, use the audited no-null `L2+L4` functional and its exact-HVP path; old
  centered-derivative tools are provenance only unless a task explicitly audits them.
- A relaxation trajectory is not physical time evolution. A finite box is not the infinite-volume
  limit. Positive sampled Ritz values alone are not stability certification.

## Communication

Keep returns concise but retain decisive equations and raw gates. Lead with what was actually learned,
then state what remains open. Separate observation, inference, and canonization. Charles owns the final
physics verdict.
