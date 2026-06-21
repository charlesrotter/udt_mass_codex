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

## *** 2026-06-21 NIGHT — COMPLETION PROGRAM UNDERWAY (read FIRST) ***
Charles's directive: FINISH every F-item (no hanging threads, even substantially-done ones), THEN audit solvers +
previous results top-to-bottom; goal = a CLEAN, PHYSICS-CORRECT SOLVER before the next level (quantize, etc.).
Discipline: [[infrastructure-first-not-exciting-stuff]] — check/double/triple-check; hunt imports/frozen/improper
assumptions; verifier-before-record on EVERY closure. Tracker = COMPLETION_PROGRAM.md; status-of-record =
FOUNDATIONAL_ASSUMPTIONS_LEDGER.md SCOREBOARD (top).
DONE: F0 audit; F1,F2,F3 (derived operator), F4 (seal-as-quantizer closed), F8 (metric choices) — all verified.
P1-P5 re-audited vs the derived operator (mostly survives; **P5c family-landscape = the loud un-re-graded gap**).
REMAINING — Phase A: F5 (critical-universe), F6 (postulate-A boundary ledger), F7 (scale bridge + Hubble native
redo). Phase B: verify-audit-completeness, P5c re-grade, secondary P-gaps, imports (M12/M10/M11), SOLVER-INFRA
audit, PREVIOUS-RESULTS top-to-bottom re-grade, wide-range numerics. The EVENING block below is the substantive
arc that got us here.

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

## Read order for a new instance (2026-06-20)
1. CLAUDE.md "How we work" (binding method) + ANTI-HANG rule + memories: solver-first-not-mechanism (read
   FIRST), everything-on-solver-build (the live frontier), how-we-work-method, cleaner-is-not-clean-no-shortcuts,
   audit-solving-infrastructure.
2. THIS FILE TOP (the 2026-06-20 live frontier) -> **POST_POSTULATE_PROGRAM.md** (the corrected program) ->
   SOLVER_COMPLETENESS_MAP.md (the live instrument) -> STATE.md TOP -> INDEX.md.
3. CANON.md (C-2026-06-18-1 + C-2026-06-14-1, both SURVIVE); NEGATIVES_REGISTRY (the pre-postulate corpus is
   RETIRED — wholesale-retirement banner; mine for TOOLING only).
4. The everything-on build docs as needed (EVERYTHING_ON_SOLVER_BUILD_MAP + sub-MAPs; p1_*/p2_*/p3_*/p4_*/
   p5*_*/p5c_*/p5d_*/offround_classical_* results + _VERIFIER). HANDOFF_ARCHIVE.md for the superseded
   2026-06-18/19 frontier blocks (field-equation turn, postulate A, the catalog reframe, #65) + earlier history.

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
