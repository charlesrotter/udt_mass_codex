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
**POST_POSTULATE_PROGRAM.md** (supersedes VISION); instrument = SOLVER_COMPLETENESS_MAP.md.
(Also in CLAUDE.md tripwires + memory [[solver-first-not-mechanism]].)

History note: all 2026-06-19-and-earlier frontier blocks (the field-equation/foundation turn, the algebraic
pivot, postulate A + the catalog reframe, #65) are SUPERSEDED by the 2026-06-20 EVERYTHING-ON SOLVER block
below + **POST_POSTULATE_PROGRAM.md**. The reframe that opened this arc: the VISION mistook a graveyard of
contaminated/classical-solver negatives for a map of the metric; microphysics is UNENTERED, not walled; the
pre-postulate negative corpus is RETIRED. Full detail in STATE.md TOP + git. This file holds the live frontier.

## *** 2026-06-22 — THE NATIVE-MATTER ARC + COMPLETE-SOLVER BUILD (read FIRST; supersedes the NIGHT/B1' blocks below) ***
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
Memory: [[full-dimensional-complete-solver]] (BOUND grid, never FREEZE a DOF), [[gravitating-soliton-stability-test]]
(constraint-respecting coupled re-solve, never off-constraint stiffness — the method that resolved the off-round null).

## *** 2026-06-21 NIGHT — COMPLETION PROGRAM UNDERWAY (read FIRST) ***
Charles's directive: FINISH every F-item (no hanging threads, even substantially-done ones), THEN audit solvers +
previous results top-to-bottom; goal = a CLEAN, PHYSICS-CORRECT SOLVER before the next level (quantize, etc.).
Discipline: [[infrastructure-first-not-exciting-stuff]] — check/double/triple-check; hunt imports/frozen/improper
assumptions; verifier-before-record on EVERY closure. Tracker = COMPLETION_PROGRAM.md; status-of-record =
FOUNDATIONAL_ASSUMPTIONS_LEDGER.md SCOREBOARD (top).
**PHASE A COMPLETE** (F1-F8 all closed/tied-off + verified; F6 framework DECIDED = HOLD quantization, finish the
solver first — emergence not a target, quantize only if needed after). **PHASE B in progress:** B0 audit-
completeness (verified — found 1 hidden gap), B1 P5c radial re-grade (verified — one-soft-object SURVIVES), B3
imports (verified — M12 scoped; M10/M11 SETTLED = S^2, and the triple-check CAUGHT + RETIRED a stale F0 flag,
UPGRADING F2). REMAINING Phase B: **B1' off-round build (NEXT, see below)**, B2 secondary P-gaps, B4 solver-infra
audit, B5 previous-results top-to-bottom re-grade, B6 wide-range numerics.

## *** B1' STATUS (2026-06-21 LATER): ROUND-LIMIT GATE DONE + VERIFIED; the 3-D OFF-ROUND RESIDUAL is the live NEXT ***
Charles ran "clean the gate first." DONE + blind-verified (b1prime_round_gate_derived_operator_results.md, verifier
a6b142162a3211abd, SUPPORTED-WITH-REVISIONS): the derived operator is reconstructed into a well-posed RADIAL solver
(phi an independent player); a smuggled kap8=0.05 was found+fixed (kap8=1 DERIVED); Gate A PASS, Gate B PASS (1/R^2
tower + one node-free negative Derrick mode), operator=action's-own-equation confirmed. **CORRECTION banked: NO
resolvable scalar hair** (conserved charge ~=0; static_soliton's "tiny hair q.|X|~0.5" was a grid-fit artifact ->
NEGATIVES_REGISTRY CONDITIONS-CHANGED; reinforces "teeth in dynamics"). The round limit validates the OPERATOR only.
**LIVE NEXT = B1'-step1: the genuine 3-D OFF-ROUND residual** (wire phi into the full3d a,b,c,d machinery; gate its
round limit coupled; then OBSERVE the off-round l>=2 angular sector = the phi-angular obstruction on the correct
operator). The small-warp check so far was a linearized l=2 proxy only. See COMPLETION_PROGRAM.md B1'.

## *** (the original B1' setup, still the spec for step1) THE OFF-ROUND BUILD (B1') — set up FRESH (Charles 2026-06-21) ***
**WHAT:** port the DERIVED operator into the full3d 3-D OFF-ROUND solver and run the OFF-ROUND / NON-SPHERICAL /
ANGULAR sector — the ONE consolidated solver-completeness gap (= F8 non-spherical residual = the off-round l>=2
discreteness gate [B0 gap#4] = P5c angular basins). **It is the only remaining PHYSICS piece for a 100%-complete
solver, AND where the phi-angular hunch lives** (the derived operator's DERIVED angular-curvature obstruction —
R1 cannot wash out the phi-free 2/r^2 angular block — has never been SOLVED off-round on the correct operator).
**THE OPERATOR (set):** S = INT sqrt(-g)[ e^{2phi}R + X e^{2phi}(dphi)^2 + e^{2phi}L_m ], two-player (phi & metric
independent), X=-2e5 (healthy window), charge-1 native hedgehog (degree-1, NOT the m>=2 import). L_m = native
S^2 L2+L4 (S^2 now DEMANDS-verified, M10).
**REUSE (don't rebuild):** the OLD full3d 3-D off-round solver (full3d_newton / the p5c_basins angular DOF:
a1,b1,c1,d1,F1 · P2(cos theta) warps) + the derived-operator radial solver (static_soliton_rerun's residual). The
job = swap the operator (the EXACT general Einstein + e^{2phi} weight + a=e^{phi} matter) into the 3-D solver; the
P1 hybrid is SUPERSEDED (P5e_proper built the exact operator in 3.3s — use exact, not the small-shear hybrid).
**GATES:** omega->0 / round-limit MUST recover the STEP2/P5e_proper round box-control; small-warp MUST recover the
off-round linear spectrum; box-control gate (cell-scan + wall-relocation + intrinsic-lock) on ANY claimed level.
**EXPECTATION (anti-false-convergence):** LIKELY box-control (the old off-round was box-controlled on EH; the
derived static is GR+tiny-hair) — BUT this is the one place the derived angular obstruction could finally bite;
OBSERVE-not-target, DATA-BLIND. **ANTI-HANG LOCKED:** bounded (Nr<=16/24), SINGLE process, dense-LM flooring,
NEVER background-poll; #60-class — if it walls, that's NUMERICS not physics (Charles: wall = better numerics;
spectral/multidomain/KEH-SCF/pseudo-arclength/JFNK+spectral-PC) and feeds B6. MAP-light first, then bounded build,
then blind-verify. Docs: COMPLETION_PROGRAM.md (B1'), p5c_basins_results.md (the 3-D solver to port),
native_dilation_weight_derivation (the operator + the angular obstruction).

The EVENING block below is the substantive arc that got us here.

## *** 2026-06-21 EVENING — LIVE FRONTIER: DERIVED OPERATOR + MATTER NOW PHYSICAL (read FIRST) ***
The foundational audit below RAN and moved the program a long way in one session. The arc (all blind-verified,
committed; see FOUNDATIONAL_ASSUMPTIONS_LEDGER.md TOP blocks + the named docs):
1. **F0 systematic audit DONE** (F0_SYSTEMATIC_AUDIT_results.md): F1/F2/F3/F6/F7 are the right gaps; F1+F3 are
   ENTANGLED (the absorbability that let us use a=-1 presupposes the EH left side); 3 solver-side soft spots
   under "must-quantize"; mu^2=pi/3 was a LEGACY data-fit (not live); the m-catalog rode an IMPORTED Skyrme BC.
2. **F1+F3 — the universal weight DERIVED** (native_dilation_weight_derivation_results.md): extending R1
   ("no privileged depth") to the ACTION = invariance under a global depth-shift phi->phi+const FORCES the
   weight **e^{+2phi}** (kinetic + gradient-curvature) and rest-mass **a(phi)=e^{+phi}** (NOT -1; the no-anomaly
   terrestrial value). **FREEZE BROKEN: vacuum != GR** (box f survives) -> the classical-continuum "must-quantize"
   headline is REOPENED. Cassini SURVIVABLE (healthy window X large negative). THE OBSTRUCTION: the depth-rule
   canNOT wash out the transverse/ANGULAR curvature (and, same root=reciprocity, the TIME-live kinetic sector) =
   **the phi-angular hunch from first principles**. Two branches characterized (branch_G/P docs): BOTH static
   SCALE-FREE.
3. **SCALE SYMMETRY (Charles's bootstrap question)** (scale_symmetry_bootstrap_analysis_results.md): "no
   privileged depth" IS a scale (dilatation) symmetry -> **box-control omega~1/R is the symmetry's FINGERPRINT,
   not a solver artifact** (VACUUM-scoped; MATTER breaks it). Charles's bootstrap = the canonized CRITICAL
   UNIVERSE with a "why" (closure c^2=2GM/R). [IMPORTED-Hubble number RETRACTED; anchor = A = phi_seal=7.004 via
   1+z=e^phi.] HEADLINE SPLIT: overall absolute scale looks classical-cosmological (one anchor); only the DISCRETE
   SPECTRUM OF RATIOS is left for quantization or the nonlinear coupled solve.
4. **Charles's strategic steer:** build a CONSISTENT THEORY OF MATTER first (anchor=A, VALUE-OPEN), serving the
   COMPLETE-SOLVER goal — NOT spectrum/catalog matching; "pure geometry all the way down" is PARKED. KEY: MATTER
   IS THE SCALE-SYMMETRY BREAKER (vacuum is scale-free). [[matter-theory-before-pure-geometry]].
5. **MATTER on the derived operator** (matter_regrade_derived_operator_results.md, F2_matter_action_forcedness_results.md):
   matter coupling is now **PHYSICAL** — the derived operator is NOT divergence-free, so the old "matter
   absorbable -> UDT=GR on the matter side" tautology is OVERTURNED; the teeth come from the OPERATOR (vacuum!=GR),
   NOT from a=+1-vs-(-1). New exterior = scalar-tensor {m,q} hair, B=1/A breaks with live hair, still a continuum.
   **F2 = MINIMAL-BUT-NOT-UNIQUE:** core {L2,L4} native+necessary; admissible extras {X^2 (moves masses not EOS),
   L6}; bulk potential V FORBIDDEN under full SO(3) (corrects the corpus); scale symmetry NEUTRAL on term-selection.

**SEQUENCE DONE (Charles's 1->3->2, all blind-verified, committed):**
- [1] consolidation (done). [3] BOUNDED STATIC RE-RUN (static_soliton_rerun_derived_operator_results.md): the
  static charge-1 soliton on the new operator = **GR + a TINY 1/r hair** (q~1/|X|); B=1/A break is dominantly the
  OPERATOR-INDEPENDENT matter-kinetic one; the new operator's static effect is small => **the teeth are in DYNAMICS.**
- [2] TIME-LIVE COUPLED MATTER SOLVE (STEP2_timelive_matter_results.md): **BOX-CONTROL** — on the DERIVED operator
  (vacuum!=GR, physical matter coupling, charge-1, live time) the classical metric gives **NO intrinsic
  discreteness**: positive tower w^2~1/R^2 (intercept statistically ZERO; R=64 push = clean 1/R^2, no plateau);
  the one negative mode = the Derrick/breathing soft direction (not a level); ACTION-ROBUST (persists at kap=0 /
  across the L4-vs-X^2 ambiguity). Reproduces the old #65 verdict ON THE CORRECTED FOUNDATION.

**P5e PROPER DONE (the heaviest residual, now RUN; blind-verified — P5e_proper_results.md):** the genuinely
fully-coupled solve — FULL off-diagonal time row g_tr=H LIVE (dynamically sourced; 0 statically = a gauge mode),
FREE-omega self-consistent eigenvalue, time-spectral (Nt=3 = DC+fundamental), finite-amplitude — CONVERGED
(bounded, |F|~1e-4, cells R in [8,12]); it genuinely REMOVED STEP-2's three reductions. VERDICT REPRODUCED:
softens/box-controls, NO intrinsic discreteness (omega softens with amplitude = anharmonic not locking; box
intercept b<=0, sign robust on independent recompute). CALIBRATION (verifier): the box gate rests on a 2-3 point
window — the SIGN is robust but a 2-point fit is not statistically airtight; the WIDE-RANGE (R=4..64) gate + Nt>=5
+ strong coupling + A2 true-Einstein are the remaining **NUMERICS, NOT physics** (Charles: "wall = better
numerics"; concrete upgrade plan recorded: spectral collocation / multidomain / KEH-SCF / pseudo-arclength /
JFNK+spectral PC).

*** HEADLINE: the foundational audit's central worry — "a different recipe could make the classical metric do
MORE" — is ANSWERED. The DERIVED vacuum!=GR operator STILL box-controls, NOW on the full coupled machinery
(P5e-proper, reductions removed). => the classical-continuum **"MUST-QUANTIZE" conclusion SURVIVES the
foundational audit** (strongly supported; the wide-range statistically-airtight version is a numerical-methods
task, not a physics gap). ***

**F4 DONE + CLOSED (the load-bearing caveat — RESOLVED, verified; seal_junction_condition_results.md).** Derived
the never-before-computed sigma-ODD/time-on seal junction (the sector every box-control solve had frozen) for
BOTH involutions on record: sigma1 (t->-t) = a NODE IN TIME (sin(omega*0)=0 for every omega -> selects NO omega
-> continuous); sigma2 (P×T) = a trivial HARMONIC ladder omega_n~n/R (wrong 1:2:3 pattern, slides with the
unpinned cell). Neither is a non-harmonic fixed-radius quantizer; verifier strengthened it (even a PINNED cell
gives only a trivial ladder). => **"must-quantize" is now UNCONDITIONAL w.r.t. the seal BC for the observed
spectrum** — the one open item that could have changed the result was checked and closed in FAVOR of the central
conclusion. (F4's STRUCTURE — A1 no-infinity, D2 doubling, D3 core removal, which-involution — stays posited, but
none rescues a classical spectrum.)

**NEXT (gated on Charles): the central conclusion is now robust on both the gravity-action axis (P5e-proper) and
the seal axis (F4).** Options: **quantize (F6** — the original forward step, now on doubly-audited ground); the
wide-range NUMERICS upgrade (statistically airtight box gate); or the remaining framing-only F-items (F5/F7 the
cosmic->particle bridge + imported-Hubble native redo / F8; M12 native sector-distinctness; M10/M11). Per the
scoreboard these are additive/framing, NOT result-changing. MAP first; DATA-BLIND; anti-hang LOCKED.

## *** (ARCHIVED) earlier resume blocks moved out ***
The 2026-06-21 EARLIER foundational-audit framing + the 2026-06-20 everything-on-solver / Quant-Step-A block were
moved to HANDOFF_ARCHIVE.md (superseded by the EVENING block above + COMPLETION_PROGRAM.md). Git has full history.

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
   [The 2026-06-21 NIGHT/EVENING blocks below this read-order are HISTORICAL: B1' "off-round build" became the
   native-matter arc; F0-F8 audit COMPLETE; the must-quantize verdict is now SCOPED to the imported object, native
   matter is unsolved beyond static (time-live = the live frontier).]

(The pre-2026-06-20 frontier blocks — the 2026-06-19 AFTERNOON #65 block, the 2026-06-19 MORNING postulate-A
block, the prior-arc condensation, and the old VISION-based goal/read-order/next-step — were moved to
HANDOFF_ARCHIVE.md on 2026-06-20. Full verbatim 2026-06-19 detail also in STATE.md TOP + git. This file holds
the LIVE frontier only.)

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
