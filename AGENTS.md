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

Before interpreting the frontier, read from disk in this exact order. **Bounded-startup rule:** do
not dump whole long files or recursively open every cited artifact during orientation. Read only the
marked/current sections below; expand to full reports, scripts, JSON, logs, or historical layers only
after the user's actual task makes them load-bearing.

1. `LIVE.md` — read only the range between `STARTUP_CURRENT_BEGIN` and `STARTUP_CURRENT_END`; its
   `CURRENT STATE` overrides every other status description. Do not read the remaining historical
   layers at startup.
2. `HANDOFF.md` — read only its `STARTUP_CURRENT_BEGIN` / `STARTUP_CURRENT_END` range.
3. `CURRENT_SCIENTIFIC_PREMISES.md`, then `CURRENT_SCIENTIFIC_PREMISES.tsv`. This is the current
   source-precedence index for high-risk foundational terms. It is not canon and cannot overrule
   `LIVE.md`; any disagreement between it, `LIVE.md`, and its cited source is a mandatory stop.
4. `udt_scientific_arc_recovery_checkpoint_2026-08-04/SCIENTIFIC_ARC_CHECKPOINT.md` — the current
   documentary scientific checkpoint. Then read its mass authority map, Gröbner reconstruction,
   bankable/open ledger and overview/route map. This is the shortest authoritative route through
   the stability/mass-emergence, spacetime, compute-time correction and founded-`phi` arcs.
5. `udt_reciprocal_path_composition_residual_audit_2026-08-04/AUDIT_REPORT.md` — the latest bounded
   derivation before the recovery checkpoint. Then read its `EXACT_DERIVATION.md`, candidate, implication and loop
   ledgers, source adjudication, review closure, four gates, and next step as needed. Read the
   universal-query, native-law type, section/descent, metric-natural selector, globalization and
   factorized-skeleton parents only when their architecture is load-bearing. The current audit
   closes founded reciprocal composition as exact but nonselecting kinematics: it is an identity on
   endpoint potentials and supplied additive cocycles, not a metric-native residual. Do not restart
   the route without a new source-backed depth or loop premise. The proposed global–local return-map
   decision audit is not automatically authorized; do not invent a return map or launch action,
   source, carrier, bootstrap, time-live, or GPU work.
6. `UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` — read only its top/current overlay (pre-P4 overlay;
   historical context only).
7. PRE-P4 (2026-07-28 morning, superseded as frontier — read only when load-bearing):
   `UDT_EXTERNAL_AI_REVIEW_BRIEF_2026-07-28.md` (zero-context review navigation for the PRE-P4
   state) and `udt_higher_isometry_plane_ownership_audit_2026-07-28/README.md` (the last pre-P4
   bounded result, still valid as banked evidence).
8. `udt_general_screen_complete_cell_atlas_2026-07-28/AUDIT_REPORT.md`, then its
   `STATUS_LEDGER.tsv`, `EXACT_DERIVATION.md`, `LAY_REPORT.md`, `COMPLETENESS_MAP.md`,
   `BLOCK_PRESERVATION_CONDITIONS.tsv`, and `NEXT_STEP.md`. This parent bounded result says the
   full invertible angular screen has area and two metric shears plus local coframe-gauge rotation;
   both shears survive at isotropy; and the twisted `S3` contact structure forbids an all-direction
   parallel pair/screen split within the chosen stationary off-shell family. The proposed
   nonstationary first-jet release is not authorized automatically. Read the parent complete-screen
   branch atlas and historical-method salvage only when their branch census or provenance becomes
   load-bearing; no old particle/QCD claim is restored.
9. `udt_metric_natural_joint_selector_nogo_2026-07-28/AUDIT_REPORT.md`, then its
   `STATUS_LEDGER.tsv`, `EXACT_DERIVATION.md`, `COMPLETENESS_MAP.md`, `LAY_REPORT.md`, and
   `NEXT_STEP.md`. This parent bounded result says full-frame additive scalar comparison and
   pointwise metric-only non-scalar selection are obstructed; the surviving type is reciprocal
   cocycle plus angular/coframe transport. Higher-jet/nonlocal/whole-solution routes remain open,
   so this is not a universal no-go. The proposed comparison-versus-realization ownership audit is
   not authorized automatically.
10. `udt_joint_selector_provenance_audit_2026-07-28/AUDIT_REPORT.md` only when its fixed-tree census,
   three-gap decomposition, or stationary hybrid is load-bearing. Then read
   `udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md` only when its parent
   three-gap decomposition or complete nonultrastatic counterfamily becomes load-bearing. Read P03
   only when its frozen scoped result is load-bearing and apply the July 28 correction layer. Read
   P02/P01 only when their exact local-atlas or transport scope is required.
11. `udt_bootstrap_clock_angular_closure_audit_2026-07-24/AUDIT_REPORT.md`, then its
   `STATUS_LEDGER.tsv`, `BOOTSTRAP_ROUTE_LEDGER.tsv`, `EQUATION_FAMILY_GATE_MATRIX.tsv`,
   `COMPLETION_BOOTSTRAP_ATLAS.tsv`, `EXACT_DERIVATION.md`, `LAY_REPORT.md`, and
   `NEXT_STEP.md` only when its parent evidence is load-bearing. A simple screen tidal spectrum plus
   `det(T+a^2 I)=0` selects a conditional intrinsic clock-matched line, while parallelism, global
   descent, path-cocycle completion, and the native matter response remain separate open gates.
12. `udt_intrinsic_clock_transverse_solder_audit_2026-07-24/AUDIT_REPORT.md` only when the parent
   pointwise generator, screen-line, or path-cocycle premises become load-bearing.
13. The observer longitudinal/transverse cocycle, relational-depth, clock-operator,
   complete-metric separation, and `X_max` packages named by the frontier only when their exact
   path, bilocal, local-neutrality, or global-diameter premises become load-bearing.
14. `udt_scientific_consolidation_checkpoint_2026-07-23/SCIENTIFIC_CHECKPOINT.md`, then its
   `CURRENT_STATUS_LEDGER.tsv`, `METRIC_TO_FRONTIER_MAP.tsv`, and `REGRESSION_GUARD_LEDGER.tsv`
   only when a prior complete-metric, bootstrap, or regression-guard claim is load-bearing. This
   is a prior evidence-linked routing layer, not authority over its cited evidence.
15. `udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md`, then its
   `CLAIM_DEPENDENCY_LEDGER.tsv` and `OPEN_JOIN_LEDGER.tsv`, then
   `REFERENCE_CORRECTION_LAYER.md`, `REVIEW_AGREEMENT_DISAGREEMENT.tsv`, and `PONDER_READOUT.md`.
   The frozen reference plus append-only cold-review layer is a prior dependency spine, not
   authority over its cited evidence.
16. `angular_toric_closure_selector_2026-07-19/LAY_DECISION_TREE.md`, then
   `angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv` when the conditional global Hopf
   theorem is relevant.
17. `null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md` only when the exact reciprocal
   Hopf-orbit witness or its provenance becomes load-bearing, then
   `native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md` for the preceding carrier/topology
   classification only when that layer is relevant.
18. The exact scripts plus JSON/NPZ/log outputs load-bearing for the current return or task; none are
   part of generic startup orientation.
19. `stability_branch_follow_256_DECISION.md` when particle operator/stability history is relevant; it
   is durable lane evidence, not the global frontier.
20. `CLAUDE.md` sections `How we work`, `DRIVER TRIGGERS`, and repo discipline only; do not dump the
   whole charter at startup.
21. Only the specific full protocol under `.claude/skills/*/SKILL.md` triggered by the actual task;
   do not preload every skill.
22. The top/current summary in `INDEX.md` and `MEMORY.md`'s `TOP — CURRENT POINTER` for pointers only;
    neither can overrule `LIVE.md`.

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

The bootstrap/stable-matter interpretation remains a working hypothesis. Founded reciprocal
comparison is an exact typed query law; ambient geometry lives on spacetime; pair-resolved response
lives over query space unless reduced by the metric. A formula `L(g,q)` must state whether `q` is
supplied, universal, existential, realized, branch-derived, stratified, or aggregated. An
all-queries residual can constrain an observer-independent metric solution without varying `q`.
The registered SNe relation is only a downstream compatibility anchor. No complete law home,
quantifier, action, response law, carrier, source, boundary, mass, bootstrap equation, time-live
solve, or physical branch is adopted.

The pre-P4
higher-isometry audit refutes universal unique reciprocal-plane ownership within its bounded
stationary descended `R x T2` family. It derives family-wide identity robustness of `span(K,V)`,
not uniqueness for a typical fixed metric. The full response-degeneracy atlas and regular cap
gluing remain open, and the toric `S3` control supplies two free primitive circle lines rather than
a selector. No fixed-profile classification or further science is authorized automatically.

The parent general-screen
atlas closes the bounded stationary `S3` angular configuration vocabulary: one area and two metric
shears plus local coframe-gauge rotation. Both shears survive at isotropy, and the inherited angular
twist couples to anisotropy. The exact contact/Frobenius obstruction rules out only an all-direction
parallel pair/screen split inside this chosen off-shell block-screen family. It does not select a
physical screen, dynamics, action, source, carrier, density/bootstrap law, boundary, or matter. The
proposed `E0(P)` first-jet release requires a new dispatch.

The parent exact partial
no-go says a continuous full-Lorentz additive scalar character is trivial, non-collinear comparison
forces angular transport, and pointwise full-isotropy metric data cannot select a non-scalar
reciprocal generator. A supplied observer line conditionally gives `lambda=+1`, a supplied ruler
line gives `lambda=-1`, and a supplied ordered pair leaves real `lambda` free. The surviving type is
reciprocal cocycle plus angular/coframe groupoid transport, not a selected physical law. Stationary
base-dependent depth and unclassified higher-jet/nonlocal/whole-solution routes prevent a universal
no-go. P03-B was not launched and is not authorized. Do not choose `lambda`, a reduction, profile,
completion, action, density sweep, matter/time-live solve, or GPU run from this result.

The prior observer-pair chain derives the abstract ordered reciprocal operator with founding-premise
stamps and narrows its global input to an observer-indexed bilocal depth type, conditional on an open
profile, signed lift, and chart-transition law. Dilation is an inter-frame comparison: every
observer has neutral self-depth and unchanged local physics. The three-observer theorem rejects only
a universal absolute-scalar-difference encoding; it does not reject pairwise dilation. Angular data
is required for non-collinear composition. Do not silently turn the surviving type, a projective
display, the balanced `O(1,1)` representation, coordinate-covector transport, or `sech` diagnostic
into a physical mutual-clock law, signal law, or selected `X_max`.

The prior complete-metric chain supplies the exact timelike boost/rotation `3+3`, full connection
mixing, spacelike/null/zero causal classification, and the 12-by-5 completion-family cross. It also
supplies `h0=|g^{-1}(dphi,dphi)|g` and `LC(h0)` as exact local CSN-invariant geometric candidates on
smooth nonnull-`dphi` branches. The `h_f` and stabilizer families leave physical connection
selection open, torsion-free split preservation is conditional on an umbilical screen, and the
construction does not cross null/zero strata. Kato transport remains geometric and not physical
time; the registered completion families are not solved universes; and no branch is selected. Do
not silently turn `h0`, its connection, the Cartan join, Kato transport, conditional Hopf theorem,
celestial fiber, completion family, or time-live proposal into authority to adopt a physical
connection, carrier, section, torus, cap, framing, boundary, action, mass law, run GPU work, or
claim bootstrap selection.

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
- Founded `phi` is the **derived additive logarithmic depth** of the reciprocal clock/ruler pair,
  acting as `diag(exp(-phi),exp(phi))`. Its physical observer/path assignment, profile, complete 4D
  extension, variation, dynamics, boundary, and global completion remain open; those open joins may
  not demote its identity to a placeholder or promote it to an extra native scalar.
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
