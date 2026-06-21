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

*** HEADLINE: the foundational audit's central worry — "a different recipe could make the classical metric do
MORE" — is ANSWERED. The different recipe (vacuum!=GR) was DERIVED, and it STILL box-controls. => the
classical-continuum **"MUST-QUANTIZE" conclusion SURVIVES the foundational audit** (robust on the R-scaling).
NAMED RESIDUALS (flagged, NOT banked): the finite-A harmonic-balance proxy; strong-coupling grid limit; the full
off-diagonal g_tr time-row PDE (the one remaining unbounded object). ***

**NEXT (gated on Charles): the forward path is UNBLOCKED** — quantization (Step B/C: the native Hamiltonian /
mass-as-cost on the quantized states) now sits on an AUDITED foundation (derived operator, physical matter,
redoubt closed). Open foundational items remain (F4 seal/F6 postulate-A boundary/F7 cosmic->particle bridge/F8;
the F2 {X^2,L6} mass-ambiguity is value-open). Consider: quantize (the original next step, now on firm ground),
OR close a named residual, OR the remaining F-items. MAP first; DATA-BLIND; anti-hang LOCKED.

## *** 2026-06-21 (EARLIER) — FOUNDATIONAL-ASSUMPTIONS AUDIT (Charles's zoom-out; now SUBSTANTIALLY RUN — see the EVENING block above) ***
Charles paused the forward build to audit the foundational assumptions the program rests on — several were
carried SILENTLY (the deepest: the gravity-side curvature action was assumed = GR's Einstein-Hilbert through
ALL of P1-P5d; "vacuum=GR" is built-in, not derived). THE KEY LINKAGE: the central result ("classical metric =
continuum => must quantize") is CONDITIONAL on this whole stack (Birkhoff is a curvature-action theorem, etc.) —
if a foundational recipe is genuinely different under UDT, the classical metric may do MORE, and we'd need less
quantization or none. So this audit is logically PRIOR to more solver/quantization work, and most items are
ANALYTIC (cheaper than the throughput-walled solver). Solver machinery is operator-agnostic/REUSABLE if a recipe
changes (modify-the-operator + re-run-the-physics, not a rebuild).
LEDGER = **FOUNDATIONAL_ASSUMPTIONS_LEDGER.md** (F0-F8, each a TASK to be discussed): F0 systematic audit (cheap,
completes the list); F1 curvature action (deepest; assumed GR; MAP target); F2 matter action L2+L4 (the twin —
derived or assembled?); F3 a(phi) coupling (a=-1 silently used everywhere); F4 finite-cell/seal/boundary
(posited); F5 critical-universe frame; F6 postulate-A boundary (admitted; spin-1/2 rides imported framework);
F7 scale bridge (open gap); F8 metric-form embedded choices. Proposed order: F0 -> F1+F2 (deepest twins, prior
to P5e) -> F3 -> rest as they bear. EACH GATED ON CHARLES (discuss before derive/build).
NEXT-AFTER-FOUNDATIONS (deferred, not abandoned): P5e (fully-coupled time solve, EVERYTHING_ON_SOLVER_P5e_MAP.md)
+ the quantization Step B/C (Hamiltonian/mass-as-cost on the quantized states) — both wait on the foundational
audit, because both build on the assumed curvature operator.

## *** 2026-06-20 — THE EVERYTHING-ON SOLVER IS BUILT; CLASSICAL METRIC = CONTINUUM; QUANTIZATION STEP A DONE [context for the audit above] ***
Read STATE.md TOP (the 2026-06-20 blocks) + memory [[everything-on-solver-build]] + POST_POSTULATE_PROGRAM.md.
THE BIG PICTURE (this arc's result): we built ONE clean everything-on solver (all DOF live, native S^2 matter,
a(phi), live time, scalable JFNK) and OBSERVED what the metric does. *** THE CLASSICAL METRIC GIVES A CONTINUUM,
period — there is NO classical discreteness. *** This DEMONSTRATES the postulate-A frame on the clean operator
("you were trying to get a quantum result classically" — now shown, not asserted). Discreteness REQUIRES
quantization. **NEXT (gated): QUANTIZE (postulate A).**

THE BUILD (each MAP-light -> branch -> blind-verify -> merge; the verifier caught something EVERY phase):
- P1 off-diagonals wired into the field equations (pole-stable hybrid Einstein, valid small-shear). P2 native
  S^2 Theta-free matter EL 3-D + coupled to the full off-diagonal metric. S^2-vs-S^3 SETTLED = S^2 (S^3 is an
  import; the cos-theta "texture" was a non-unit-embedding artifact). P3 a(phi) coupling = RULER weight
  exp(INT(a+1)dphi) (a=-1 baseline reproduces P2 bitwise; a!=-1 declared/unforced). P4 live time row
  (containment bitwise omega->0=static). P5 driver: JFNK rescued by RE-POSE to full-rank body DOF (the committed
  Jacobian was rank-deficient from the body-mask edge excision, NOT steep-core); light/no PC floors it.
- THE OBJECT (P5c, verified): the committed 3-D solver admits MULTIPLE charge-1 floored solutions, but the
  barrier test (NEB, Nr-trend closed) shows NO walls between them = ONE SOFT CONNECTED OBJECT, not a family.
  *** CHARLES'S FAMILY QUESTION ANSWERED: NO (same-charge multiplicity is one soft object; round = lowest-energy
  ground state; the ~5-7% mass scatter is the flat-valley width). *** M_MS(round)~0.29-0.31 bankable modulo
  grid drift (gated, not yet banked).
- TIME-LIVE (P5d, verified): the ROUND object is TIME-FROZEN by Birkhoff (d_t^2 inertia M=0) — no oscillator.
  The off-round channel HAS an oscillator (M!=0) but (off-round classical-discreteness gate, verified incl. a
  3-cell high-mode persistence test to Nr=24) it is BOX-CONTROLLED (omega~1/R, no intrinsic level binds). Matter
  DOES pin a size sqrt(kappa/xi) (the loophole was genuine) but it sets only high core modes, not the spectrum.
  Numerical + structural agree, on the CLEAN operator (not the distrusted #65 proxy).

THE CAPABILITY GAP (named, honest — what the solver does NOT do): it is a STATIC + small-vibration (linearized-
fluctuation) solver. It does NOT do the FULLY-COUPLED TIME version (off-round + time + back-reaction at full
strength, free-omega, self-consistent). What that costs (ranked): (1) genuinely NONLINEAR time-dependent bound
objects (breathers/geons) that linear analysis misses — the one place a classical surprise could still hide
(#65 + the structural argument say coupling softens/box-mode-geometric, but it's not theorem-grade); (2) ROTATING/
spinning stationary objects (angular momentum — relevant to spin/magnetic moment later); (3) genuine long-time
evolution/stability; (4) airtightness on the no-discreteness verdict; (5) POSSIBLY the quantization substrate IF
that route needs the off-round coupled modes (the forward risk — unknown until we quantize). We SKIPPED it on
cost/benefit (hardest #60-class solve; the discreteness answer is well-supported without it). Per the standing
discipline: if a mismatch with observation points at any of these, BUILD this solver — do not reach for a mechanism.

NEXT (gated on Charles): QUANTIZE (postulate A) the box-controlled classical continuum. Substrate it inherits:
the round object's surviving FIRST-ORDER G^t_r momentum/phase channel + K's flat directions. NATIVE LEAD: a
first-order/phase structure quantizes differently than an oscillator (Birkhoff forbids a round oscillator) —
possibly the i=area-form / Born thread [[udt-derives-sm-assumptions]]. MAP it first (the quantization approach
is a real open choice). Docs: EVERYTHING_ON_SOLVER_BUILD_MAP.md (+ _P2/_P5 MAPs), p1..p5* results + _VERIFIER docs,
offround_classical_discreteness_results.md.

*** OPERATIONAL DISCIPLINE — ANTI-HANG (binding; SIX+ agents hung this arc): solves are SLOW (jacrev/iteration-
bound, mins to ~1700s). ALWAYS run solves BOUNDED (Nr<=16/24, iter caps), SINGLE clean process, NEVER concurrent
(GPU contention), NEVER launch-a-solve-and-background-poll. Fixed-background eigenproblems are cheap (5-22s);
the dense-LM (jacrev+lstsq) is the flooring tool; recompute-on-saved-fields where possible. If a solve would
exceed budget, REDUCE and report "throughput-limited" — a bounded honest partial beats a hang. Stability tests:
NEVER blend toward a chosen endpoint (biased artifact) — use unbiased kicks + NEB + 3-cell persistence. ***

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
