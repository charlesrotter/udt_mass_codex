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

## *** 2026-06-20 LIVE FRONTIER — THE EVERYTHING-ON SOLVER IS BUILT; CLASSICAL METRIC = CONTINUUM; NEXT = QUANTIZE (read FIRST) ***
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

## *** 2026-06-19 AFTERNOON FRONTIER [SUPERSEDED by the 2026-06-20 block above] — STEP 1 (FULL COUPLED TIME-LIVE SOLVE) = SCOPED NEGATIVE (#65); PIVOT TAKEN => CATALOG = DISTINCT SECTORS ***
Read STATE.md TOP (the 2026-06-19 AFTERNOON block) + NEGATIVES_REGISTRY #65. Distilled:
- VISION Step 1 was taken in FULL ("Build the full coupled solve", Charles-gated = the one shot against the
  tripwire). MAP-first CAUGHT that a reduced/structural version had already run overnight (time-live REVIVES
  the dead static operator into a real standing-wave problem — phi-angular hunch gets its carrier, a durable
  win — but gives {l(l+1) charge-barrier floor + box continuum}, no new tower). The ONE omitted ingredient =
  the fully-coupled NONLINEAR back-reaction. Charles authorized the shot at it.
- **#65 SCOPED NEGATIVE (pre-registered + blind-verified):** native S^2/pi_2 carrier Theta-FREE (r=0 node BC,
  NO Skyrme import; M_MS=0.281 clean), live time, fully-coupled finite-amplitude back-reaction. The
  back-reaction is ACTIVE + genuinely nonlinear but SOFTENS the ladder toward a TACHYON (omega^2->0), opens NO
  new bound level; lowest level stays ~1/R^2 box-controlled. Gate B PASS (grid-converged => real verdict, not
  a stall). => #44 (one carrier = one particle) confirmed EVEN WITH the back-reaction; tripwire residual CLOSED.
- Residual scope cost (flagged, non-blocking, = #65 reopener): the live mode was the ROUND radial breather;
  spatial l>=2 non-roundness reduced to round; the joint nonlinear+l>=2 corner argued-empty via the proxy's
  LINEARIZED drift finding, not a direct solve (would need a full 3-D live-time solver).
- **THE PIVOT (Charles, "do 1"):** retire the "catalog = one carrier's spectrum/tower" template. Catalog
  frontier = what DISTINGUISHES DISTINCT objects + sets their DEPTHS — distinct charge/winding SECTORS + the
  free non-stationary/off-diagonal/ensemble DOF (VISION spine §III). Mass-as-cost = the exponential home.
  Docs: coupled_timelive_solve_CONTRACT.md, coupled_timelive_solve_results.md, coupled_timelive_VERIFIER.md.

## *** 2026-06-19 MORNING FRONTIER — POSTULATE A ACCEPTED; BOX-TRAP BROKEN; TOWER FRAMING INDICTED => CATALOG REFRAME ***
Read STATE.md TOP (the 2026-06-19 MORNING block) + memory postulate-A-accepted. Distilled:
- *** POSTULATE A ACCEPTED (Charles) ***: UDT = QUANTIZED DILATION-GEOMETRY. Geometry NATIVE; quantization
  (postulate A = hbar/spin-1/2/statistics ONLY; i=area-form STAYS NATIVE; no SM import) gives discreteness.
  UDT does NOT derive QM from geometry — "unify cosmology+microphysics is good enough"; door OPEN for later.
- DURABLE WINS: (1) postulate A BROKE the box-control trap — FIRST intrinsic (non-box) discrete level on the
  program; spin-1/2 = native area-form. (2) mass-as-COST (B1 Misner-Sharp, not hbar*omega) is EXPONENTIAL +
  SCALE-FREE + BOX-FREE + INTRINSIC in FORM — the native home for the hierarchy. (cost sees e^{phi}
  undifferentiated; frequency saw its log-derivative => power-law. The split is the key insight.)
- THE WALL: every "tower of ONE carrier" route (radial overtones / depth-rungs / nonlinear breather U(D)) gives
  ~1 stable level then a tachyon at D*; more rungs reintroduce box-control. No multi-rung exponential ladder
  from one carrier. The depth-selector NON-CLOSURE is blind-verified.
- *** REFRAME (confirms #44) ***: one charge-1 cell = EXACTLY ONE particle, NOT a tower. The
  generations-as-a-TOWER framing is INDICTED. Generations = a CATALOG of distinct stable objects
  (particle-catalog-frame), masses exponential in their DEPTH DIFFERENCES (mass-as-cost).
- **NEXT (Charles's frame, gated):** "what DISTINGUISHES the distinct stable objects + sets their DEPTHS" (the
  catalog), NOT "what tower". Residual flagged-not-drilled (tripwire): the fully-coupled nonlinear well.
  Docs: quantized_carrier_structure_results.md, mass_as_cost_ladder_results.md, depth_selector_breather_results.md.

## Prior arc (condensed — full detail in STATE.md TOP + VISION_POST_POSTULATE.md + HANDOFF_ARCHIVE.md)
The field-equation question (2026-06-18) was chased to ground: it is **GR-FORM** (f(phi)R departs but is
Cassini-dead; the running-rate source weight absorbs back to GR); the UDT-vs-GR departure relocated to the
MATTER coupling a(phi), UNFORCED at the principle level (the native curvature-sector action is still UNBUILT =
the deepest open Principle-7 item). That triggered the ALGEBRAIC PIVOT (B1 charge-native + mass-as-cost
exponential; B2 phi-angular non-closure), the time-live solve, then POSTULATE A (above). CANON C-2026-06-18-1
(metric from relativity) + C-2026-06-14-1 (B=1/A sourced) + the bare-vacuum no-go's #62/#63/#64 all SURVIVE.

## THE GOAL (current, post-postulate-A — see VISION_POST_POSTULATE.md §II)
UDT = QUANTIZED DILATION-GEOMETRY: provide the NATIVE geometry (the dilation metric, the area-form charge
N=3/q=1/3, the standing-wave carrier, the depth/scale) and POSTULATE {hbar / spin-1/2 / statistics; i=area-form
stays native}; QUANTIZATION supplies the discreteness. Goal = **unify cosmology + microphysics** by matching
OBSERVATIONS, via the CATALOG of distinct native objects (mass = dilation cost). NO imports / frozen values /
box-control; let structure EMERGE; gated DERIVE (no masses vs the wall numbers until Charles says ready).

## Read order for a new instance (2026-06-19)
1. CLAUDE.md "How we work" (binding method) + memories: session-handoff-pointer (read FIRST),
   postulate-A-accepted, frontier-time-live-native-matter, particle-catalog-frame, how-we-work-method,
   cleaner-is-not-clean-no-shortcuts, algebraic-objects-can-be-imports, audit-solving-infrastructure.
2. **VISION_POST_POSTULATE.md** — the FORWARD PLAN (recon + post-postulate-A vision; the spine + ordered path).
3. STATE.md TOP (the 2026-06-19 MORNING + OVERNIGHT blocks).
4. THIS FILE; CANON.md (C-2026-06-18-1 + C-2026-06-14-1, both SURVIVE); NEGATIVES_REGISTRY (#61-#64).
5. The recon docs (RECON_A/B/C/D) + this session's docs (B1_*, B2_*, quantized_carrier_*, mass_as_cost_*,
   depth_selector_*, gravity_sector_*, udt_a_*) only as needed; HANDOFF_ARCHIVE.md for pre-2026-06-18 history.

**NEXT STEP (gated on Charles, = VISION step 1):** the native pi_2, Theta-FREE, time-live non-round CATALOG
solve — does UDT's OWN area-form charge (no imported Skyrme BC, #61) give a catalog of DISTINCT STABLE TYPES?
HIGH risk/leverage (home of the live import + the #58/#60 off-round solver-limit). Anti-import + anti-box-
control + anti-frozen-matter discipline LOCKED. Then: quantize per object -> depth-selector {D_n} -> gated
pre-registered mass-as-cost vs wall numbers -> two-anchor scale bridge.

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
