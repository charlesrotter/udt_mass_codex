# COMPLETION PROGRAM — finish every thread before the next level

**Directive (Charles 2026-06-21):** finish ALL F-items (even the substantially-done ones — no hanging
threads), THEN audit the solvers + previous results top-to-bottom. Goal (next few days): a CLEAN,
PHYSICS-CORRECT SOLVER for doing work later. Finish everything before moving to the next level.
Discipline: [[infrastructure-first-not-exciting-stuff]] — check/double/triple-check; verifier-before-record
on every closure; hunt imports / frozen items / improper assumptions. Status-of-record = the SCOREBOARD in
FOUNDATIONAL_ASSUMPTIONS_LEDGER.md. This doc = the actionable checklist.

## PHASE A — finish F1–F8 (close every residual to a clean state)

- [x] **F1 — gravity curvature action.** CLOSED (F1F3_closure_results.md, verified CLEAN). DERIVED (vacuum!=GR). FINISH: confirm the derivation is airtight;
  formally close the superseded gravity-side residuals (N4 C1-uniqueness scope, N6 asymptotic-flatness-vs-
  no-infinity tension, N8 local-Lorentz-at-extremes); document the FREE X dial (kinetic/curvature ratio) as
  the one principle-unfixed parameter, with the no-ghost+Cassini window. Deliverable: F1 closure record.
- [x] **F2 — matter action L2+L4.** CLOSED (F2_closure_results.md, verified CLEAN). RESOLVED = minimal-but-not-unique. FINISH: document the {X^2,L6} admissible
  extras as a bounded value-open ambiguity (mass-only, not EOS); CHECK the load-bearing full-SO(3) target
  assumption (if reduced, V re-enters). Deliverable: F2 closure record.
- [x] **F3 — a(phi) coupling.** CLOSED (folded into F1F3_closure_results.md, verified CLEAN). DERIVED a=e^{+phi} (entangled w/ F1). FINISH: tie off with F1; confirm the
  physical-coupling re-grade is airtight; close "a=-1 silently used in P1-P5d" (the P1-P5 re-audit covers the
  downstream). Deliverable: folded into F1+F3 closure.
- [ ] **F4 — finite-cell / seal / boundary.** Seal-as-QUANTIZER question CLOSED (verified). FINISH the STRUCTURE:
  is the container DERIVED or POSITED — A1 (no spatial infinity), D2 (I×S^2 doubling vs S^2×S^1 Chern competitor),
  D3 (inner-core r=0 removal), and WHICH involution (t->-t vs P×T); resolve the time-surface/radial-crease fork
  held DERIVED-conditional. Deliverable: F4 structure closure (derived-vs-posited, each tagged).
- [x] **F5 — critical-universe frame.** CLOSED (F5_critical_universe_closure_results.md, verified CLEAN) = ADMITTED WORKING FRAME with a derived self-consistency mechanism (c²=2GM/R); pinning dimensional-only; does NOT bear on must-quantize. PARTIAL (bootstrap = critical universe w/ a why, c^2=2GM/R). FINISH:
  is "matter at ONE critical amount" DERIVABLE or an admitted FRAME? is the pinning derivable or dimensional-
  only? Deliverable: F5 closure (derived vs admitted-frame, explicit).
- [x] **F6 — postulate-A boundary.** BOUNDARY CLOSED (F6_postulate_A_ledger_results.md, verified FAITHFUL): clean POSTULATED {hbar, spin-1/2, statistics} / FREE-with-imported-framework {the discreteness math} / NATIVE {i=area-form, omega_H1=symplectic-form identification, cell-independence, N=3/q=1/3} ledger. REMAINING for Charles: SIGN OFF the framework question (quantize-now vs geometric-emergence) + the k=2j-vs-N=3 open. (We have not quantized — that's Step B/C, gated.) OPEN (admitted). FINISH the clean ledger: what is truly POSTULATED
  {hbar, spin-1/2, statistics} vs FREE-with-the-imported-metaplectic-framework vs NATIVE (i=area-form,
  cell-independence); is quantization the right framework vs later geometric emergence (the door-open clause)?
  This is an ADMISSION/decision item, not a derivation — make the boundary crisp + Charles-signed. Deliverable:
  F6 postulated-vs-free-vs-native ledger.
- [x] **F7 — scale bridge / ~10^40 autonomy gap.** CLOSED-TO-CLEAN-STATE (F7_scale_bridge_native_results.md, verified CLEAN): imported-Hubble REMOVED (M/R=c²/2G native; absolute size = unpinned dilatation modulus, H0 order-correct as OUTPUT, number pinning-deferred to the coupled solve); cosmic->particle half = the IRREDUCIBLE known-open gap, stated cleanly (M doesn't bridge; depth ~115x short; particle size must come from the cell's own cavity/angular structure). OPEN (known-hard). FINISH to a clean state: do the
  imported-Hubble NATIVE redo (anchor A=7.004, H0/rho_crit as DERIVED outputs); then either close the cosmic->
  particle bridge or formally characterize it as the IRREDUCIBLE open gap (what's needed, why it's hard).
  Deliverable: native cosmic-scale redo + bridge status record.
- [x] **F8 — embedded metric-form choices.** CLOSED (F8_metric_choices_results.md, verified CLEAN; one named residual = non-spherical on the derived operator, value/solve-open). PARTIAL. FINISH: characterize each embedded choice (static /
  spherical / diagonal / areal-r / P8 slot-id) as DERIVED-from-the-principle vs CHOSEN (free solution-space DOF),
  explicitly. Deliverable: F8 choice-provenance record.

## PHASE B — audit solvers + previous results, top to bottom

- [x] **B0 — verify the P1-P5 re-audit's COMPLETENESS** (verified, agent a488bcabf7fcde972) — FOUND ONE hidden
  gap: the off-round l>=2 discreteness gate was mis-labeled REESTABLISHED (only the ROUND object was re-run on the
  derived op) -> re-classified UNCHECKED-GAP #4. Three named gaps + imports list otherwise complete. Triple-check worked.
- [x] **B1 — re-grade P5c (family/landscape)** on the derived operator (P5c_regrade_derived_operator_results.md,
  verified): RADIAL sector = "one soft object, NO durable family" SURVIVES + sharpens (single basin, field-level
  ~1e-10, no walls). Honest scope: the ANGULAR/non-axisymmetric basins are NOT in the radial chart -> that part
  folds into the consolidated off-round gap below.
- [~] **B1' — *** THE CONSOLIDATED SOLVER-COMPLETENESS GAP *** : port the DERIVED operator into the full3d 3-D
  OFF-ROUND solver and run the off-round/non-spherical/angular sector.** This single gap = {F8 non-spherical
  residual} = {off-round discreteness gate, B0 gap#4} = {P5c angular basins}. It is where the phi-angular hunch
  lives (the derived-operator angular obstruction). A BUILD (not a bounded re-grade). The key remaining piece for
  a 100%-complete solver. Anti-hang LOCKED.
    - [x] **B1'-step0 ROUND-LIMIT GATE — DONE + blind-verified** (b1prime_round_gate_derived_operator_results.md,
      verifier a6b142162a3211abd, SUPPORTED-WITH-REVISIONS). Reconstructed the derived operator into a well-posed
      RADIAL solver, phi an independent player; found+fixed a smuggled kap8=0.05 (kap8=1 is DERIVED). Gate A PASS
      (localized charge-1, B=1/A matter-kinetic break ~0.07), Gate B PASS (1/R^2 tower + one node-free negative
      Derrick mode), operator=action's-equation confirmed. CORRECTION banked: NO resolvable scalar hair (conserved
      charge ~=0; static_soliton's "tiny hair 0.5" was a grid-fit artifact -> NEGATIVES_REGISTRY CONDITIONS-CHANGED).
      Reinforces "teeth in dynamics." Round limit validates the OPERATOR only.
    - [x] **B1'-step1 3-D OFF-ROUND RESIDUAL BUILT + proven correct** (Schwarzschild->0, flat->1e-14, box-f->6e-16;
      reduces to radial operator). `b1prime_3d_offround_residual.py`. Angular fork RESOLVED NUMERICAL (E^th_th~2.9
      was unpinned a'' grid-sawtooth; E^th_th is conservation-DEPENDENT, proven symbolically -> round IS a valid
      off-round solution).
    - [x] **B1'-step2/3 off-round OBSERVE (SCOPED) -> box-control**, BUT each was a SLICE (step2 phi-pinned; step3
      diagonal coupled with off-diagonal SHEAR + matter-ansatz + time FROZEN). NOT verdicts (frozen DOFs).
    - [ ] **B1'-COMPLETE -> SUPERSEDED INTO THE COMPLETE 4-D SOLVER BUILD (Charles 2026-06-21):** the off-round
      slices exposed that NO solve is simultaneously full-spatial-3D AND time-dependent — must-quantize rests on
      complementary slices. Charles: build the COMPLETE 4-D solver, MAXIMAL PURITY (fix all audit shortcuts + FREE
      the areal chart). See **THE COMPLETE 4-D SOLVER BUILD PROGRAM** block below.

## *** THE COMPLETE 4-D SOLVER BUILD PROGRAM (2026-06-21, Charles-directed; the live frontier) ***
GOAL: ONE solver with EVERY axis live at once — full spatial metric INCL off-diagonal shear (g_rth,g_rps,g_thps)
+ live time row (g_tr,g_tth,g_tps) + multi-harmonic finite-amplitude time + phi(t,r,th,ps) independent + matter
FULL angular freedom (no welded hedgehog) + FREE areal chart (sphere-size a DOF) + all harmonics; ONLY the grid
bounded, NO frozen DOF. The audit (3 parallel agents 2026-06-21) found the primitives CLEAN (core christoffel/
einstein general 4x4 to 2.7e-15; all 3 spatial axes full spectral; matter stress/lagrangian general) — the
shortcuts are in what's FED to them. Charles rulings: S^2 everywhere (per M10/M11); FREE the areal chart; add an
exp-clamp tripwire; replace 3-row edge excision with a real boundary.
- [x] **S1 (GATING) — DONE + blind-verified** (complete_solver_stage1_general_einstein_results.md; verifier
  afe291bf819a17d0a SUPPORTED-WITH-REVISIONS). Diagnosed: CORE.einstein noise is STRUCTURAL N-divergence (nested
  spectral differentiation, grows with N). FIX: analytic general Christoffel/Einstein codegen (einstein_3d_general_*),
  carries shear + time-row, machine-exact formula, ~1e-12..1e-14 vs diagonal-analytic, N-CONVERGENT. Edge-mask DROPPED
  (engine clean at edges). BANKED LIMITATION: d_t=0 stationary (Stage 5 regenerates with live ∂_t).
- **S2 — REFRAMED (2026-06-21, verified):** the free-matter build surfaced + a data-blind re-derivation/blind
  verifier CONFIRMED that the derived-operator soliton corpus ran the IMPORTED S^3/pi_3 Skyrme baryon (body
  BC-held); UDT's NATIVE matter is the S^2/pi_2 winding (n=x/r), UNSOLVED on the derived operator
  (matter_object_identity_native_vs_import_results.md). free_s2_matter.py built (machinery reusable) but its
  gate was vs n=x/r — fine, since n=x/r IS the native object. **S2 deliverable = SOLVE the native S^2/pi_2
  object (n=x/r, NO imported baryon BC) on the derived operator** — does it form a stable localized object
  (size from geometry/weight, NOT a matter lump), and what is its gate (box-control or structure)? This is the
  decisive open item + the genuine native matter stage. Reuse MAT.stress/lagrangian/field_metric + autograd-EL;
  codegen EL retired. THEN the round gate / box-control get re-derived on the NATIVE object.
- **S3:** free areal chart (r^2,sin^2 prefactors -> solved DOF) + gauge-fixing (radial + angular coord freedom).
- **S4:** assemble COMPLETE STATIC solver (shear+free-chart+free-phi+free-matter); validate round/diagonal limits
  recover banked gates; bounded run.
- **S5:** multi-harmonic finite-amplitude TIME on the FULL 3-D grid (NOT the single-cos QEP eigenvalue) + time
  off-diagonals live; validate P5e/STEP2 limits.
- **S6:** run the complete 4-D solver bounded, OBSERVE (the hunch test on a tool with nothing frozen).
Cleanups folded: S^2 everywhere, exp-clamp tripwire assert. Audit source: task#8 / the 3 ledgers (synthesize doc TBD).
MULTI-SESSION. Anti-hang LOCKED throughout (BOUND the grid, never FREEZE a DOF — [[full-dimensional-complete-solver]]).
- [ ] **B2 — secondary P-gaps:** P1 static spatial-shear on the EXACT operator; the P5a'/P5b solution-manifold.
- [x] **B3 — standing imports (verified):** M12 RESOLVED-as-SCOPED (charge-1 native used / catalog parked / import quarantined; no native ladder; M12_winding_bc_closure). M10/M11 RESOLVED (S^2 DEMANDED + blind-verified 2026-06-19; F0 flag was STALE/wrong, RETIRED; texture=artifact; UPGRADES F2; M10_M11_object_identity_closure).
- [ ] **B4 — SOLVER INFRASTRUCTURE audit** ([[audit-solving-infrastructure]]): engines/solvers/stress for hidden
  patches/imports/approximations/frozen-DOF; the pole-stable HYBRID (approx) now superseded by the exact operator
  — confirm nothing still rides the hybrid; B=1/A over-imposition; seal-injection; etc.
- [ ] **B5 — PREVIOUS RESULTS audit, top to bottom:** re-grade the banked corpus against the corrected foundation;
  NEGATIVES_REGISTRY re-grade pass; flag every result still scoped to the old operator.
- [ ] **B6 — wide-range NUMERICS upgrade:** make the box-control gate statistically airtight (spectral/multidomain/
  KEH-SCF/pseudo-arclength/JFNK+spectral-PC; Nt>=5; strong coupling; A2 true-Einstein), per the recorded plan.

## GOAL
A CLEAN, PHYSICS-CORRECT SOLVER (correct + complete; imports/frozen/approximations removed or explicitly scoped;
every prior result re-graded on the corrected foundation) — ready for later work. THEN the next level (quantize, etc.).

## LOG (append as items close; each verifier-passed before checking the box)
- (2026-06-21) Program opened. F1-F4 substantially done (scoreboard); finishing residuals + F5-F8 + Phase B.
