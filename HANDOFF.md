# HANDOFF — Resume Instructions and Perspective

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
