# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
> **MODEL HANDOVER 2026-07-04: the successor driver's orientation = `PURSUIT_CHARTER_2026-07-04.md`
> (read after LIVE TOPMOST — treasure list, FORK 3 route-fork program R1–R4, the eleven known traps).**

## SESSION RECORD 2026-07-04 (Opus — route fork R1/R2 → S²-regrade → E2c/E2d/E2e optimizer arc; PENDING = Charles's option-3 decision)

First session after Fable's model handover (the charter was written at that handover). Charles directed
step-by-step; every result was committed + blind-verified before the next began. Arc, in order:
1. **R1 — route-fork native derivation** (commit **40294ef**; verifier **a31db58f300da6011** 8/8 + 3
   sharpenings). **VERDICT = FREE-ON-A-SHEET:** the forcing rule pins WEIGHTS, never coefficients; the
   fork is the TWO-PARAMETER SHEET (Z_φ, μ) — Route A = the μ=0 edge (Z free), Route B = the single point
   (8,2) conditional on 2 unforced CHOSEs (single-curvature-origin + c_L=1). **The ONE observable = s = 2μ/Z**
   (vacuum-deformation exponent; A:0, B:½; clocks in μ≠0 vacuum slaved to areal radius, e^{−2φ} ∝ ρ^{2s};
   observability EXACT). The mixing term IS a kinetic-level φ-angular coupling (areal growth drags depth —
   the founding hunch, in the action). `r1_route_fork_native_derivation.md`.
2. **R2 — s-dependence pre-registration + the FRAME FORK** (commit **3515f62**; verifier **a82dd36ef191768dd**,
   26/26, corrected 2 over-reaches; reframe BLESSED by Charles). BANKED: s=2μ/Z = the ONE gauge-invariant
   vacuum observable; **J(s) light-deflection = the frame-ROBUST confrontation lever** (J(0)=π, J(½)=4, O(s)
   impact-parameter-independent; a bound s_max<½ kills Route B but not small-μ = NOT binary). The rotation-law
   v²=s = PREMISE-CONDITIONAL (lives under g, killed only by the observationally-DEAD ĝ branch — NOT an
   artifact). **ĝ-as-physical = REDUCTIO** (zero gravitational redshift vs GPS + zero orbits). ⇒ THE FRAME
   FORK (which metric matter couples to; is matter-in-motion a worldline). `r2_prereg_s_dependence.md`.
3. **S²-defect CONDITIONS-CHANGED re-grade** (commit **e3ec6b0**; verifier **aa3af5a01f70aa096**) —
   triggered after Charles caught the driver leaning on the pre-field-equations S²-defect discovery
   (2026-06-22, predates the native field equations 2026-07-01) without re-grading. Verdicts: A(S³=imported
   provenance) + B(native S²/π₂ carrier) + D-negative(S13c: no R1-invariant worldline law) = CLEAN-CURRENT;
   C-"scale-free" SUPERSEDED (L4 size √(κ/ξ)); C-stability + D-positive(matter-in-motion IS a field w/
   dynamics) = STILL-OPEN, awaits the emergence program. The R2 frame fork stays OPEN; the point-particle-
   worldline branch is UNDERCUT (leans matter-in-MOTION toward a field/defect-SOLUTION) but NO positive
   verdict + does NOT select g vs ĝ. `regrade_S2_defect_2026-07-04.md` + NEGATIVES_REGISTRY entry. Discipline
   reinforced: charter trap #11 + memory [[dont-lean-on-conditions-changed-until-regraded]].
4. **E2c — optimizer hardening** (commit **c68d65d**; builder a366c26d, verifier **ab6305ce222eee961**;
   **NO PHYSICS MOVED** — git diff insertions-only, residual byte-identical). The E2 0/256-undecided cause
   was a near-EXACT TRANSLATION GAUGE of the boundary pair (ambient r-autonomy, cos=−1.000000); FIXED via
   Ruiz two-sided equilibration (cond 5.7e11→1.9e7) + Powell dogleg trust region; certified converging from
   boundary offsets ≥30 to ~5e-9 on 2 MMS (incl. a bulged one). Hardened driver = `lm_hardened` in
   `cell_solver_composite.py`. `microphysics_E2c_optimizer_hardening_results.md`.
5. **E2d — continuation+multistart driver** (commit **92af4e2**; builder adfcf1eea, verifier
   **a5e1960b6f90b4686**; physics untouched to EXACT zero). `e2d_continuation_driver.py` certifies boundary
   ≥30 + the deviation-field (u) axis ~0.3; combined-cell field axis UNCERTIFIED along Newton/fp homotopy =
   COMPONENT SEPARATION (verifier-SCOPED to those homotopy families, NOT absolute — grid homotopy bridges
   some ⇒ a connecting path EXISTS). Real sweep GATED OUT (honest STOP). `microphysics_E2d_resweep_A1Z8_results.md`.
6. **E2e — physics-informed seed** (commit **ba31693**; verifier **a0205204484a1d48c**; physics
   byte-identical to HEAD). The DERIVED-core seed (even fold + E_ang(core)=2, canon C-2026-07-03-3) CONTROLS
   the boundary runaway (phys r_p bounded O(100–2000) vs flat O(1e7)) but does NOT crack the combined-cell
   wall. Certification FAILED + scoped A1Z8 sweep = NULL (candidates:[], 8/8 coverage, both seed families).
   **KEY FINDING: the combined-cell wall = EXTREME DEPTH-STIFFNESS** (residual 16.9 at field-distance 0.1,
   homotopy folds at s~9e-4) — NOT seed distance. ⇒ EXISTENCE of static concentric A0 embedded cells UNDECIDED
   (tool-limited; trap-#1 scoped: "not found from these seeds," NEVER "does not exist"). Three verified solver
   rounds (E2c/E2d/E2e) localize the SAME depth-stiffness wall. `microphysics_E2e_physinformed_seed_results.md`.

**PENDING = Charles's option-3 decision (presented 2026-07-04, AWAITING his call — THE next action):**
**3a** = one more mechanism-matched solver idea (a DEPTH-STIFFNESS HOMOTOPY ramping core depth
shallow→physical, untried, directly targets the diagnosed wall; cheap) · **3b** = pivot to the **ω≠0
REFRAME** (Charles's founding φ-angular hunch; static concentric A0 may be the wrong frame; the pre-named
escape) · **checkpoint** = bank the day, pick fresh. Driver lean: 3a once, 3b strongly queued if it fails —
but the frame call is HIS. **Standing owed (unchanged):** J(s)-vs-data (frame-robust, proceeds ANYTIME);
Charles's R1 flag (adopt single-curvature-origin premise? driver lean = decline); photon/EM-native re-grade
(#47-pos/#50); R3 = Route-B universe cell; D4 = ω≠0; the other 5 D2 forks (charter §4); Bin-2 registry
re-grades at point of use. **Durable win:** s=2μ/Z + J(s) light-deflection stand frame-independent.

## SESSION RECORD 2026-07-03 → 07-04 (rulings → Stage-D → microphysics re-entry → D1/D2; Fable's closing session)

Every result blind-verified before banking; the verifier broke one of our own headlines (E2) and
strengthened two others (N=3, T-G1) — the discipline's best session. Chain, with commits:
1. **Charles's four stability rulings** → canon C-2026-07-03-1 (E=−∫L flat-limit, scope-tagged) +
   C-2026-07-03-2 (fundamentals stable minimum-class; the universe = the N=0 ground state of its own
   ladder; F5 note) (5f99eec).
2. **Stage-D prediction test PASSED:** contract hash-frozen (34d1b6b) → blind sweep → the quantization
   closure called the never-refined aliased window **13/13 rungs N=23–35, labels rung-for-rung, worst
   dev −0.139%, incl. an untested γ<0.4 regime**; verifier 7/7, zero false passes (de090cd;
   `cascade_stageD_results.md`). The ladder is PREDICTION-GRADE.
3. **Microphysics re-entry** (mini-MAP w/ Charles's 2 guardrails, eeca93c): E0 real-ambient tables
   (H≡0 along the interior REAL-AND-FORCED, 8dfe483) → E1 composite closure derived natively
   (**criticality MIGRATES: E_ang(core)=2 at the particle core; counting SQUARE — the old
   over-determination WAS the model ambient**; canon C-2026-07-03-3: core = even fold at FINITE depth,
   φ→−∞ retired; 2df6087) → E2 battle plan approved verbatim → E2a solver (17678d6) → **E2b 4-bracket
   sweep 0/256 → THE VERIFIER BROKE THE NEGATIVE:** MMS gauntlet shows the LM's convergence radius
   ~1e-3 vs seed distances O(0.3–1.5) ⇒ **existence UNDECIDED; first-class solver-completeness
   finding** (01b663f; `microphysics_E2_coupled_solve_results.md`). Registry #75 = rigid-N=1
   closes-nowhere (the one clean kill).
4. **Charles's frame-catches mid-arc** (banked in memory + the ponder): two ASYMMETRIC regimes
   (emergence one-sided; angular sector the invariant link); "we're modeling a smaller universe cell";
   black-holes-at-φ=0 → self-revised to DEFERRED post-emergence after the marginality/formed-horizon
   push-back. His walk-back commissioned D1.
5. **The armchair ponder** (`ponder_emergence_directions_2026-07-04.md`, 4a5f657): directions D1–D5.
6. **D1 provenance audit** (800aa5c, verifier 8/8): **N=3 + the 1+3+5 algebra + structural-i = TRUE
   NATIVE CARGO (strengthened)**; q=1/3 + η=1/18 = IMPORT-DEPENDENT → targets; QCD/QED precision layer
   = pre-classifier scaffolding CONFIRMED; photon/EM re-grade OWED; a candidate→"derived" PROMOTION
   ERROR found and corrected in 3 banked locations.
7. **D2 two-regime MAP approved → D2a/b/c banked** (9f94d8b, verifier 64/64 own algebra): interior
   ALL-P (A1/A2 dead there; thin strong-P shell = 99% of q); **T-G1** (no G-vacuum self-closure,
   route-robust) + **T-G2 (the mass-emergence MECHANISM is P-ONLY — Charles's one-sidedness at theorem
   level)**; Route-B mixing term DISCHARGED (corrected Route-B EOMs banked; fold values +
   E_ang(core)=2 ROUTE-B-ROBUST verified; **flat FAILS Route-B G**); **Route-A G|P architecture closes
   NOWHERE (Z>0) — escapes = Route B / Class-B seals / twisted folds = three of Charles's SIX pending forks (full list: charter section 4). THE ROUTE FORK
   IS NOW PHYSICS and the pivot.**
8. **Organizing pass for the model handover** (this entry): PURSUIT_CHARTER_2026-07-04.md written;
   LIVE restructured (old layers → `archive/LIVE_stability_stageD_microphysics_arc_2026-07-03_04.md`);
   memory frontier cleaned. **Charles's directive: forks next, EMPHASIS FORK 3 (the route fork).**

## SESSION RECORD 2026-07-02 → 07-03 (universe cell → ladder → derived laws → stability; LIVE.md TOPMOST block = the frontier)

The reordered plan ("solve the universe cell first") executed and OVERSHOT: the cell was derived, closed, and
handed back a derived spectrum. Full chain, every step blind-verified (14+ verifier agents; 4 refutations
caught — one driver, one claude.ai, one leading-order launch, one ±1 convention — all corrections banked):
1. **Universe cell:** vacuum IMPOSSIBLE + center-free + two-mirror RIGIDITY (`universe_cell_vacuum_impossibility_results.md`);
   fork ruled → FLUX-SEALED cell; fold JCs + σ-admissibility + **E_m(core)=2 critical closure (F5 as a
   theorem)** (`universe_cell_fold_jc_sigma_results.md`); T2 knob-free identities + q-window
   (`universe_cell_T2_identities_results.md`); canon **C-2026-07-02-1** (anchor = Δφ, fold-pinned zero).
2. **T3 solve:** THE CELL CLOSES; closures = a COMPLETE consecutive-integer ladder N=0..22, FAMILY-UNIVERSAL
   (6 families, both Z), parity grain, TWIN ladder w/ inverted parity (`universe_cell_T3_closure_results.md`,
   `cascade_stageA/B/C_results.md`); ρ_s sheds the matter with N (0.44% spread at N=8).
3. **The laws DERIVED (never fitted):** Theorems A/B exact; O(ε) structure (amplifier CORRECTED to
   e^{Δφ/2}=√1101); **Lemma D: a_seal ≈ √Z/[(N+1)π+θ₀] — family data cancels EXACTLY; q ∝ √|s̃₁| = the one
   mechanism behind both Stage-C findings** (`ladder_lemmaD_sealing_amplitude_results.md`); θ₀ at 2nd order
   (bottom-launch dominant) AND **the accumulation law = the quantization closure** — the fit guard's
   "unclassified" resolved as an IMPLICIT law (`ladder_theta0_accumulation_results.md`).
4. **Ponders (closed 07-03):** corpus → "TOWERS REFUSED, CLOSURES ALLOWED" + re-grade-at-point-of-use
   (`negatives_premise_sweep_2026-07-03.md` + registry amendment); twin = BROKEN INVERSION u→−u; TWIN
   FUNDAMENTAL EXISTS (cap-displaced); **INNER-SEAL CHARGE CAP = exact bound** (`twin_ladder_involution_results.md`).
5. **Stability filter (COMPLETE through the ponder-presentation):** operator derived+verified (raw index
   INFINITE; theorem-pinned v₀=0 counting; `stability_operator_results.md`); full table + blind spot-pass
   (fundamentals uniquely n_pos(V̂)=0; excited saturate (2,N+1); twin fundamental (2,1);
   `stability_stage2_results.md` w/ correction note); soft mode IDENTIFIED + BLIND-VERIFIED = a FOLD-PAIR
   breathing mode, genuine converged negative (`ladder_softmode_results.md`; B00 λ*=−6.33e-7; SZ1 sign-solid
   mag-unconverged); ORIENTATION chain complete AIM-BLIND (`ladder_energy_orientation_results.md`): identities
   banked (lapse cancels exactly; E_can=−∫L; ∫L=2∫(2−E_m); H≡0 = r-flow NOT t-energy trap), the SIGN = an
   adjudicated CALL (MS anchor refuted-as-forcing; flat-limit anchor favors the banked E=−∫L). **THE PONDER
   WAS PRESENTED 2026-07-03 EOD; FOUR RULINGS PENDING (enumerated in archive/LIVE_stability_stageD_microphysics_arc_2026-07-03_04.md (formerly LIVE TOPMOST) — re-present on resume).**
**Method notes that must survive:** verifier-before-record caught something material at EVERY stage; the
freeze-before-data pattern (fit forms, diagnostics, predictions) paid out three times; agent process rules —
chunk CAS (one timeout), pre-declare shot budgets (one overage), graduated-floor zero counts, exact-projection
deflation before reading soft modes; blind passes get avoid-lists AND withheld values where possible.


> **Earlier frontiers:** see `HANDOFF_ARCHIVE.md` (2026-07-02-morning block archived 2026-07-03) — the
> sections below (STANDING BINDING DISCIPLINE / Foundation / STANDING RISKS / REUSABLE MACHINERY /
> Must-not-lose) are DURABLE, not frontier. NB Risk 1 (round-static walls) is now RESOLVED-IN-CONTEXT by
> the ladder arc (static discreteness exists via closures, not towers); Risk 2 (Z_phi fork) remains open,
> now with derived observational handles (window ceiling, a_seal, q all scale with Z).

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
the pre-postulate negative corpus is RETIRED (mine for TOOLING only). BOUND the grid, never FREEZE a
DOF ([[full-dimensional-complete-solver]]); test gravitating-soliton stability by a constraint-respecting
COUPLED re-solve, never off-constraint stiffness ([[gravitating-soliton-stability-test]]). (Also in
CLAUDE.md tripwires + the `.claude/skills/` discipline skills + memory [[solver-first-not-mechanism]].)

## Foundation (the DERIVED native frame the solver now builds on) + read order

**The native UDT frame is DERIVED + verified (2026-07-01) — this is the foundation the new solver stands on** (five docs:
`native_field_equations_constrained_two_player_results.md`, `gp_switch_criterion_results.md`,
`native_geometric_action_results.md`, `seal_matching_junction_results.md`, `round_matter_reduction_results.md`; each
CAS + blind-verified). Metric = constrained-two-player `ds²=-e^{-2φ}c²dt²+e^{2φ}dr²+h_AB dx^A dx^B`; native geometric
action `∫c√h[(Z_φ/2)φ'² + R^{(2)} + W_χ𝒦]`, `W_χ=e^{2φ}(G)/1(P)`; matter is **φ-BLIND** (sources geometry via
`n→h_AB→𝒦→φ`, not `e^{2φ}T`). One open constant `Z_φ` (held fixed; free vs `=8`-with-forced-mixing fork → consilience).

**The OLD static solver is the WRONG FRAME (retained only for the tests).** The p1 MIGRATION solver (`p1_residual`,
`branch_operator`, `full3d_*`, …) realizes the φ-OUTSIDE-the-metric two-player scalar-tensor frame that Phase 1 showed
is a CHOSE extension, NOT canonical UDT. Its `e^{2φ}L_m`/`e^{2φ}T` matter weight is the NON-native artifact that
manufactured the "basin A" runaway; the X=−2e5 was the Cassini KLUGE. `pytest tests/` = **32 passed / 1 xfailed** still
imports these modules, so they STAY until the new solver + test rewrite land (then retire to `legacy/`). Do NOT tune them.

**Durable native-matter facts (SURVIVE, and the new solver uses them):** UDT's native matter = the **S²/π₂ winding**
(`n=x/r`), a scale-free defect; its charge is the **integer TOPOLOGICAL degree N** (native quantization — the "lump"
search was frame-creep, Charles's 2026-06-25 catch). In the new round solver: rigid `f=θ` collapses (I_r=0); the
minimally-free `f(r,θ)` test RAN (arc archived; the universe-cell/ladder line superseded it — see LIVE.md). The φ-angular hunch now appears NATIVELY (Branch-P `𝒦`-source;
the route-B kinetic-completion mixing term; the seal source that charges a matter cell).

**Read order for a new instance:** (0) **LIVE.md FRONTIER block** (THE only-guaranteed-current file). (1) CLAUDE.md
"How we work" + ANTI-HANG + the `.claude/skills/` discipline skills; frontier memory **[[universe-cell-rigidity-frontier]]** (foundation one back: [[native-field-equations-frontier]])
+ the principle memories ([[apply-purist-logic-proactively]], [[solution-space-not-imposition]],
[[charles-workflow-preferences]], native-matter-defect-import-discovery, solver-first-not-mechanism). (2) THIS FILE +
the five native-frame result docs + `discreteness_preregistration.md` + `round_matter_reduction_results.md` +
`cell_solver_round.py`. (3) CANON.md (C-2026-06-14-1; C-2026-06-18-1 — both SURVIVE); NEGATIVES_REGISTRY;
FOUNDATIONAL_ASSUMPTIONS_LEDGER. **HANDOFF_ARCHIVE.md + STATE.md + git + `archive/` = the deep historical record.**

## STANDING RISKS — the two flagged open items in the derived frame (Charles 2026-07-01, do NOT lose)
Both are correctly TAGGED (unlike the X-kluge, which was mislabeled `# FREE` and so contaminated silently). A tagged
open choice is manageable; the danger is only if we forget it's open. They come due at DIFFERENT stages — convenient
for keeping them honest.

**RISK 1 — the CONSTRAINED-METRIC FORM (the CHOSE) may WALL OFF the structure we're hunting.** Derived + solid: the
exp clock law `g_tt=-e^{-2φ}` + the reciprocal tie `g_tt g_rr=-c²`. CHOSEN (not forced): static, diagonal, and the
"φ purely longitudinal + h_AB independent transverse" split. The serious danger: if discreteness actually needs a
metric structure our ansatz excludes — OFF-ROUND angular shape, a NON-STATIC/time-live piece, or φ mixing DIRECTLY
into the angular sector at the METRIC level (not just via the matter/𝒦 coupling) — we could scan the round-static
space forever, see only a continuum, and WRONGLY conclude "UDT has no discreteness." **A "round static → continuum"
result must be read STRICTLY as "this SLICE is a continuum," NEVER as the theory's verdict** (whole-before-slice;
frozen-DOF≠verdict). Load-bearing: ALL our derivations are SCOPED to this form — so if it's incomplete they're
PARTIAL, not wrong; the staged plan (round → off-round → time-live) exists to un-freeze these one at a time. This is
the bigger risk to WHETHER we find discreteness at all.

**RISK 2 — the OPEN CONSTANT Z_φ.** (a) **It could become the new X-kluge**: if a quantitative result rides on Z_φ,
the pull to "tune Z_φ until the ratios match" is the exact failure mode we just escaped — the pre-reg fence (held
fixed, ONE global choice, no per-solution retuning, decided BEFORE checking the match, blind-verified) must actually
hold. (b) **The fork is STRUCTURAL, not just a number**: Route B (`Z_φ=8`) FORCES an extra action term `e^φKφ'` (a
longitudinal-transverse = φ-angular coupling); Route A omits it. So "open constant" is really "**is there an extra
coupling term?**" — build in Route A and we may be missing a native channel (possibly THE φ-angular channel). (c)
**Scoped:** Z_φ (overall kinetic normalization) mostly rescales SIZES → it does NOT gate the first question ("are
there isolated cells?"); it DOES gate the QUANTITATIVE program (mass ratios) later. This is the bigger risk to
getting the numbers right and NOT fooling ourselves.

**Shared deep risk = INCOMPLETENESS** (a missing DOF for Risk 1; a missing term for Risk 2). Neither will announce
itself — this is exactly where "keep auditing and digging until it's correct" earns its keep: is this scoped or
general? chose or derived? whole or slice?

## REUSABLE MACHINERY (the old solver = a PARTS BIN, not a foundation) — Charles 2026-07-01
The old 3-D solver was the WRONG frame, but it has TWO layers: the **physics recipe** layer is DEAD (wrong frame),
the **numerical machinery** layer is Category-A ("how we solve", frame-agnostic) and is a REUSABLE parts bin. Raid it
DELIBERATELY, one audited part at a time, as the difficulty climbs — do NOT build on it wholesale.

**REUSABLE (Category-A numerics — mine the METHOD, in `legacy/` + the kept root closure):**
- `glm` step = Levenberg-Marquardt in a conditioned basis + Nielsen damping + line-search (in
  `p1_residual_general_einstein.py::newton_solve_p1`) — a general robust nonlinear solver for when the 2-D/off-round
  problem gets stiff.
- galerkin BC-recombined basis (`galerkin_basis.py`) — bake BCs into the basis for conditioning (the mirror-seal cell
  has its own tricky BCs).
- spectral methods — **`spectral_sph_exact.py` (SH-EXACT angular d/dθ) is the most directly relevant**: the naive
  GL-μ grid mis-differentiated the winding `sinθ` non-convergently; the new `f(r,θ)` winding field is EXACTLY that
  structure. Also `spectral_cheb.py` (Chebyshev radial). GPU batching (torch float64) for large scans.
- the junction/DtN/Israel formalism (already used for the seal JC1/JC2), and the grid/method-convergence harness
  (a pre-reg acceptance criterion).
- **Operational know-how (frame-independent, do NOT relearn the hard way):** the GL-μ-grid-mis-differentiates-winding
  gotcha; the V100/cu121 batched-Cholesky-with-broadcast-factor corruption at batch ≳150 (use explicit inverse +
  matmul); the ANTI-HANG rules (bound the grid, ONE process, never background-poll a solve).

**DEAD (wrong-frame PHYSICS — do NOT reuse the ASSEMBLY):** `p1_residual_general_einstein.py` (the 11-field residual),
`branch_operator.py` / `b1prime_3d_offround_residual.py` (the e^{2φ}-weighted derived operator), the X-continuation,
`solver_action.py` GR-baseline. These build the φ-OUTSIDE-the-metric frame.

**CAVEATS:** (1) the old modules INTERTWINE physics + numerics — you cannot just `import full3d_spectral` (it builds the
wrong metric; the matter EL bakes in e^{2φ}); pull the METHOD, never the assembly, or you re-import the flaw
(Category-A not B; the "audit-solving-infrastructure" discipline applies). (2) The near-term problem is MUCH simpler
(1-D ODE now, 2-D PDE next — scipy-handled; `cell_solver_round.py` is ~60 lines), so for a while a FRESH small tool is
CLEANER than untangling a 3-D module. (3) The parts bin being full is a real head start; assembling from it wholesale
would drag the wrong frame back in.

## Must-not-lose (durable facts)
- DATA-BLIND wall numbers (NEVER load during a derivation): the six lepton wall numbers, contract
  26fc757. We predict RATIOS.
- CANON C-2026-06-14-1 (B=1/A sourced by the angular sector; EOS-softened interior) — SURVIVES.
  CANON C-2026-06-18-1 (metric form derived from relativity) — the new foundation.
- Durable GEOMETRY: the seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass =
  the cell's public charge (Q=2 p_F); N=3 from the area form (D1-corrected 2026-07-04: N=3 + the 1+3+5 algebra + structural-i = NATIVE cargo; q=1/3 and eta=1/18 = IMPORT-DEPENDENT -> targets; d1_angular_constants_native_rederivation.md); 7.004 = ln(1+z_CMB)
  via 1+z=e^phi.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
