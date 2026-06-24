# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
>
> **CURRENT ACTIVITY (2026-06-23 late): the BRANCH-P PUSH.** Integrity arc P1-P5 DONE. Then found the
> native-S² "scale-free defect" verdict silently used Branch G (gauges the φ-angular potential AWAY);
> testing the untried **Branch P** (keeps it = a scale-breaker = the hunch). Step A DONE (`branch_operator.py`,
> explicit G/P switch, blind-verified, committed 9cd80ef), Step B DONE (`branchGP_native_s2_coupled_OBSERVE.py`,
> coupled residual w/ native S² radial twist live), Step C THROUGHPUT-LIMITED/INCONCLUSIVE (G floors to the
> 1/r² defect; P stiffer, didn't floor — only signal = U pulls φ ~5× deeper; record =
> `branch_p_coupled_observe_partial_results.md`). **NEXT = build the JFNK/preconditioned coupled solver**
> (prior: `p5a_prime_jfnk_fast.py`) → floor Branch-P → the seal-independence gate. Full detail = LIVE.md.

## *** STANDING BINDING DISCIPLINE — read every resume (Charles 2026-06-19) ***
**MISMATCH -> SOLVER, NOT MECHANISM.** If a result is far from observation, the FIRST hunt is the
SOLVER and our application of it — NEVER a mechanism. In order:
1. What did we leave OUT of the solver? (a term, a coupling, a sector, a boundary)
2. Is it a NUMERIC problem? (convergence, box-control, conditioning, a bug, grid)
3. Did we FREEZE or forget to turn on a degree of freedom?
4. Have we actually EXPLORED THE SOLUTION SPACE with everything on, or only a corner?
Plus the many WAYS to examine the same solve (different bases, grids, seeds, continuation, gauge
tests, independent re-derivation). **Reaching for a mechanism to close a gap is FORBIDDEN** until the
solver is demonstrably complete and the solution space genuinely explored. A mismatch indicts the
solver's COMPLETENESS first, the metric last, and a mechanism never (the import reflex). This is
Principle 1 applied to our own numerics. And: **the microphysics space is UNENTERED, not walled** —
the pre-postulate negative corpus is RETIRED (mine for TOOLING only). Forward frame =
**COMPLETION_PROGRAM.md** "THE COMPLETE 4-D SOLVER BUILD PROGRAM" (the live tracker; POST_POSTULATE_PROGRAM.md
/ SOLVER_COMPLETENESS_MAP.md were the 2026-06-20 frame, now subsumed). (Also in CLAUDE.md tripwires + memory
[[solver-first-not-mechanism]].) BOUND the grid, never FREEZE a DOF ([[full-dimensional-complete-solver]]);
test gravitating-soliton stability by a constraint-respecting COUPLED re-solve, never off-constraint stiffness
([[gravitating-soliton-stability-test]]). All pre-2026-06-22 frontier blocks are in HANDOFF_ARCHIVE.md + git.

## *** 2026-06-23 — SOLVER-INTEGRITY-UPGRADES ARC (current activity; a Charles-requested detour BEFORE the time-live build) ***
Charles paused the physics frontier to harden the solver's integrity MACHINERY first (spec =
**SOLVER_INTEGRITY_UPGRADES_SPEC.md**, P1->P2->P3, then P4/P5). The PHYSICS frontier (time-live native S^2, below)
is UNCHANGED — only DEFERRED. SPINE of the arc: **the harness REFERENCES derivations, it never RE-ASSERTS their
results** (no derived VALUE hard-coded into a test; tags checked, values SOURCED) — keeps the integrity layer from
becoming a NEW import surface (Charles's embedding-risk catch).
- **P1 DONE + committed (4ef7add), blind-verified x2 (VERIFIED):** the PURITY HARNESS `tests/test_solver_integrity.py`
  (+ conftest, pytest.ini) — pytest, **9 pass / 5 documented-gap xfails, <1s, no Newton/jacrev**. Four checks each
  anchored to a banked bug: liveness (off-diagonals built-but-dead), provenance lint (smuggled kap8=0.05), limit
  recovery (flat/Schwarzschild vacuum + a de Sitter NORMALIZATION anchor for operator scale), native-object guard
  (S^3 Skyrme import). Guards the CURRENT live solver. **The 5 xfails ARE the migration TODO** (kap8=1 untagged,
  a=-1 not a(φ), 4-comp S^3 hedgehog not native S^2, core_mode='deg1' pins Θ(0)=π, ξ=κ=1.0 untagged) — each XPASSes
  when the live path is migrated (self-resolving tripwire). Catch-proof: 4 historical bugs + 2 verifier-found holes
  reintroduced -> matching test RED, repo restored byte-identical. Record = **p1_purity_harness_results.md**; MAP =
  P1_PURITY_HARNESS_MAP.md; verifiers a8d2dae18fdcecfc9, a1b23eea2004b7446.
- **P2 DONE + committed, blind-verified (VERIFIED-WITH-CAVEATS, caveats CLOSED).** Charles decision: build on the
  a=-1 GR-BASELINE; open physics DEFERRED TO MIGRATION. Deliverables: **solver_action.py** (THE single source-of-truth
  GR-baseline action `S=∫√−g[(1/2κ8)R + L2 + L4]` with a provenance-tagged ACTION_TERMS registry; the derived-theory
  + UNTRACED matter-weight terms recorded MIGRATION-DEFERRED, operator=None) + **tests/test_operator_from_action.py**
  (7 tests). PROVEN: matter STRESS == exact Hilbert variation (~1e-15); gravity = two independent analytic engines
  agree (no drift, 1.7e-13; truth anchored by P1 de Sitter/Schwarzschild). CONSISTENCY: matter FIELD-EOM matter_el_3d
  (strong) == -autograd(action) (weak), converging ~0.4% (codegen-bug-sensitive). REGRESSION-LOCK: residual assembles
  G-κ8T. Catch-proof: 4 injected bugs -> matching test RED. Record = **p2_operator_from_action_results.md**; verifier
  acc513a4bfdeef941. The DERIVED-action version is wired at MIGRATION — the step that picks the fork + settles the
  matter weight + swaps a(φ)=e^{φ} in, and flips the 5 P1 xfails green. **The P1 xfails + the P2 baseline = the
  migration's acceptance tests.** MIGRATION-OPEN PHYSICS (tripwired, do NOT silently resolve to make a test pass):
  (1) **e^{2φ}R is DERIVED only on the GRADIENT-sector curvature; the ANGULAR curvature REFUSES the weight** — the
  native_dilation derivation reaches a Branch G / Branch P FORK and never picks a side. Plain `e^{2φ}R` silently
  assumes Branch P. (This fork IS the phi-angular tension / Charles's standing hunch, surfacing in the foundational
  action.) (2) **the matter weight `e^{2φ}` in front of L_m is UNTRACED / pattern-matched** — it appears NOWHERE in
  F2/scale-symmetry/CANON; the corpus matter action has NO such factor; inserting it CHANGES the matter field
  equations = a candidate smuggled import IN THE SPEC. (3) **X is FREE/UNFORCED** (weight e^{2φ} derived, coefficient
  not; healthy window |X|>~1.7e5, large NEGATIVE) — must be tagged FREE not DERIVED. (4) **the live operator runs the
  a=-1 GR baseline, NOT the derived e^{2φ}/a(φ)=e^{φ} theory** — so "generated-from-derived-action == hand-coded
  operator" CANNOT hold without either scoping the action to the a=-1 limit or migrating the operator. Decision for
  Charles (lay): build P2 on the a=-1 baseline the operator ACTUALLY realizes (machinery now, derived version at
  migration) vs. treat the curvature fork + matter weight as gated PHYSICS to resolve first. L_m is MINIMAL-BUT-NOT-
  UNIQUE (F2: {L2,L4} core + optional {X²,L6}). Recon agent trail in this session; no codegen written yet.
- **P3 DONE + committed.** Factored the binding disciplines into 4 auto-loading skills (each <=1 screen) in
  `.claude/skills/`: **solver-first** (mismatch->SOLVER four-question protocol), **verifier-before-record** (clean
  blind-pass requirements), **no-shortcuts** (anti-import/anti-freeze checklist + `pytest tests/`), **completeness-map**
  (ten criteria + standing questions). CLAUDE.md POINTS to them but KEEPS the short tripwires INLINE (skills lazy-load
  their body; only the description is always-in-context — so the binding rules stay always-loaded; Charles-agreed
  design). Fresh session auto-discovers them (confirmed via claude-code-guide; takes effect next session since
  `.claude/` is new). Record = **p3_discipline_skills_results.md**.
- **P4-P5 remain:** P4 cross-model verify (ruling: fresh zero-context Claude; documented flag; log disagreement),
  P5 LIVE.md shrink. Then the integrity arc is complete and the physics frontier (time-live native S^2) resumes.

## *** 2026-06-22 — THE NATIVE-MATTER ARC + COMPLETE-SOLVER BUILD (read FIRST; supersedes the 2026-06-21 NIGHT/B1'/EVENING blocks, now in HANDOFF_ARCHIVE.md) ***
The Phase-B off-round work (B1') opened a foundational arc. Read order: this block -> COMPLETION_PROGRAM.md
(THE COMPLETE 4-D SOLVER BUILD PROGRAM) -> the named results docs -> FOUNDATIONAL_ASSUMPTIONS_LEDGER scoreboard.
All blind-verified + committed this session. THE ARC (each its own results doc):
1. **Round gate CLEANED + banked** (b1prime_round_gate_derived_operator_results.md): found+fixed a smuggled
   kap8=0.05 (kap8=1 DERIVED); CORRECTED the static_soliton "tiny hair" -> NO resolvable scalar hair (grid-fit
   artifact; registry CONDITIONS-CHANGED).
2. **STAGE 1 (the gating numerical problem) DONE + verified** (complete_solver_stage1_general_einstein_results.md):
   the general CORE.einstein is N-DIVERGENT on the steep core (nested spectral diff) -> built an ANALYTIC general
   Christoffel/Einstein engine (einstein_3d_general_*) that is shear+time-row capable, machine-exact, N-convergent.
   This UNBLOCKS the whole complete solver (every prior residual was secretly diagonal). d_t=0 caveat (Stage 5 regen).
3. **MATTER OBJECT IDENTITY re-derived + verified** (matter_object_identity_native_vs_import_results.md):
   *** the round-gate/static_soliton/STEP2/P5e soliton is an IMPORTED S^3 Skyrme baryon; its BODY is held by the
   imported winding BC. UDT's NATIVE matter is the S^2/pi_2 winding (CANON C-2026-06-14-1). *** The box-control/
   must-quantize line was on the IMPORTED object (registry SCOPED).
4. **NATIVE S^2 matter SOLVED on the derived operator (first ever)** — rigid (native_s2_object_..._results.md) +
   twist-freed (native_s2_twist_freed_...) + off-round twist x shear coupled (native_offround_twist_shear_results.md),
   all verified: **UDT's native matter is a scale-free global-monopole DEFECT, not a localized particle, in EVERY
   STATIC configuration played** (rigid, radial-twist=flat-Goldstone, and the decisive constraint-respecting coupled
   off-round twist x shear re-solve = mass RISES, 12 unbiased seeds all uphill -> defect STABLE). The matter strains
   toward an off-round body but gravity wins on-constraint. Core: structurally self-regulated by the derived phi-hair
   (q>0 DERIVED), ~1/|X|-weak. The localized particle/size/B!=1/A break were ALL the import.
*** THE LIVE FRONTIER = TIME-LIVE / NON-STATIONARY native S^2. *** Every native-matter solve so far is STATIC. The
project's STANDING HUNCH places discreteness at the closed-time/non-stationary sector (not the static metric) — and
that is now the one major UNTESTED instrument. The complete-solver build's remaining stages (S2 full 2-angle matter,
S3 free chart, S4 assemble, **S5 TIME-LIVE** [regen the engine with live d_t], S6 run) all converge here. NEXT =
build the time-live native S^2 object (the orchestra's time instrument). Anti-hang LOCKED (the analytic engine + the
bounded coupled-solve recipe are proven this session; the FD-Jacobian 9-field solve costs ~120-240s/grid — bound it).
**PRECISE ENTRY POINT (do FIRST, MAP-not-launch; two items are genuine Charles decisions):** (i) **sequencing** —
the static native S^2 is NOT exhausted (we played rigid, azimuthal-twist, and off-round twist x shear; the FULL
2-angle static field Theta_t(r,theta),Phi_t and the other shear channels = the rest of "S2" are NOT done). So the
first decision: finish the remaining STATIC native instruments (S2) first, or jump straight to TIME-LIVE (S5, the
hunch's home)? Present this to Charles. (ii) **the GATE is undefined** — what observation counts as "discreteness
found" vs "still a continuum/defect" for the time-live native object is NOT yet specified; MAP it (with premises,
in lay terms) and get Charles's sign-off BEFORE building. Both are the make-visible-and-ponder method, not a stall.
Memory: [[full-dimensional-complete-solver]] (BOUND grid, never FREEZE a DOF), [[gravitating-soliton-stability-test]]
(constraint-respecting coupled re-solve, never off-constraint stiffness — the method that resolved the off-round null).


## Read order for a new instance (2026-06-22 — current; supersedes the NIGHT read-order)
1. CLAUDE.md "How we work" (binding method) + ANTI-HANG rule + memories: **native-matter-defect-import-discovery**
   (read FIRST — the live foundational state), **full-dimensional-complete-solver** (BOUND grid, never FREEZE a DOF),
   **gravitating-soliton-stability-test** (constraint-respecting coupled re-solve, never off-constraint stiffness),
   solver-first-not-mechanism, audit-solving-infrastructure, algebraic-objects-can-be-imports.
2. THIS FILE TOP (the **2026-06-22 NATIVE-MATTER ARC** block) -> **COMPLETION_PROGRAM.md** "THE COMPLETE 4-D SOLVER
   BUILD PROGRAM" (the actionable stage list, S1 DONE) -> STATE.md TOP (2026-06-22 block) -> FOUNDATIONAL_ASSUMPTIONS_LEDGER.md
   SCOREBOARD (status-of-record).
3. The native-matter arc docs (the current foundation, all blind-verified + committed): **matter_object_identity_native_vs_import_results**
   (the import discovery), **complete_solver_stage1_general_einstein_results** (the gating engine — einstein_3d_general_*),
   native_s2_object_derived_operator_results, native_s2_twist_freed_derived_operator_results, native_offround_twist_shear_results.
   The PRIOR derived-operator arc (now SCOPED to the imported S^3 object): b1prime_round_gate_derived_operator_results,
   native_dilation_weight_derivation, static_soliton_rerun / STEP2_timelive_matter / P5e_proper.
4. CANON.md (C-2026-06-18-1 metric-from-relativity + C-2026-06-14-1 native S^2 carrier + B=1/A, both SURVIVE);
   NEGATIVES_REGISTRY (TOP: the 2026-06-22 object-identity SCOPING — the soliton corpus + must-quantize line are
   scoped to the imported S^3 object; native S^2 is the defect). HANDOFF_ARCHIVE.md for superseded earlier frontier blocks.
   [Historical context (B1' off-round build became the native-matter arc; F0-F8 audit COMPLETE; the must-quantize
   verdict is now SCOPED to the imported object, native matter is unsolved beyond static) is in HANDOFF_ARCHIVE.md
   — the 2026-06-21 NIGHT/B1'/EVENING blocks were moved there 2026-06-23. This file holds the LIVE frontier only.]

(All pre-2026-06-22 frontier blocks — the 2026-06-21 NIGHT/B1'/EVENING derived-operator arc, the 2026-06-20
everything-on-solver / Quant-Step-A, the 2026-06-19 #65 + postulate-A blocks, and earlier — are in
HANDOFF_ARCHIVE.md. Full verbatim detail also in STATE.md + git. This file holds the LIVE frontier only.)

## Must-not-lose (durable facts)
- DATA-BLIND wall numbers (NEVER load during a derivation): the six lepton wall numbers, contract
  26fc757. We predict RATIOS.
- CANON C-2026-06-14-1 (B=1/A sourced by the angular sector; EOS-softened interior) — SURVIVES.
  CANON C-2026-06-18-1 (metric form derived from relativity) — the new foundation.
- Durable GEOMETRY: the seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass =
  the cell's public charge (Q=2 p_F); q=1/3, N=3, eta=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB)
  via 1+z=e^phi.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
