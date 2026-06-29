# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
>
> **CURRENT ACTIVITY (2026-06-29): D1 determinacy fix — IMPLEMENTED + blind-verified (null-dim 0); the RE-SOLVE
> STALLED (full-rank but cond≈1e11 + BC-stiffness) so the RE-GRADE is BLOCKED on conditioning machinery. NEXT =
> the 3-move conditioning phase (warm-start+fixed-X / parity-Galerkin basis+equilibration / re-examine the stiff
> core Robin BC), then re-grade. See `LIVE.md` FRONTIER (authoritative) + `D1_FIX_DESIGN.md` (DERIVED BC TABLE +
> RE-SOLVE ATTEMPT 1). Git push RESTORED + synced.** This session: kap8 caveats #2 (winding survived) + #3 (off-diagonals excluded)
> CLOSED; native reframe (kap8 object = core-concentrated S² winding DEFECT, NOT a horizon); broad-sweep solver
> AUDIT → FIX-FIRST list, top item **D1 = static solve is UNDERDETERMINED** (1776 eqns / 4224 unknowns,
> null-dim 2448; quantitative results SOFT, qualitative SURVIVE); GR-numerics research → proven determined-posing
> recipe; the **|n|=1 / amplitude FORK RESOLVED** (matter = rigid unit field, native; the magnitude version is a
> gated Higgs-type import; amplitude ≠ φ); D1 fix designed + the BCs DERIVED from the seal mirror-fold parity +
> core regularity + topology (off-diagonal split: e_rt,e_rp Dirichlet / e_tp Neumann; φ(seal)=0; matter seal-pin
> dropped). **⚠ GIT PUSH DOWN (auth) — local commits `5fe1a44`,`898fbd4` ahead of origin `715c8e4`; re-auth + push.**
> (Prior 2026-06-27 line, now historical:) static solver CODE-COMPLETE + kap8 characterized (PARTIAL).** Across 2026-06-25→27 the WHOLE static-solver
> arc landed (anti-imposition GATE + import-traceability clean `solver_pack.py` + audit + **off-diagonal sector
> COMPLETED** (the kap8 GUARD-RED was a FROZEN DOF, not a horizon — Charles's "solver-dev not physics" catch) +
> **SH-exact grid fix** `spectral_sph_exact.py` + **NATIVE-S² matter WIRED** (operator takes `dn`; S³ RETIRED;
> free 3-component carrier; matter CORE FREE, no Θ pin) + provenance re-pointed). `pytest tests/` = **32 pass /
> 1 xfail** (the 1 = branch G/P exploration gate).
>
> **kap8 characterization RAN (~40.9 h, both branches) — PARTIAL/CAVEATED; record `kap8_characterization_complete_solver_results.md`.**
> Both branches FLOOR at Nr=8,10 with a MILD warp-trend (G 1.02→1.18 ×1.16; P 2.53→2.87 ×1.13) vs the old ×2.12.
> The blind verifier REJECTED the "divergence CURED / it was the frozen DOF, not a horizon" headline — NOT banked.
> **Follow-up #2 DONE (`check_winding_survival.py`): the winding SURVIVED** — Nr=8/Branch-G solved field has
> degree Q≈1 on every shell + real matter (ρ 0.10→0.18), so the converged solution is a GENUINE non-trivial S²
> matter object, NOT unwound vacuum; the warp is MATTER-sourced (resolves verifier caveat C). STILL OPEN: **B —
> firm convergence (Nr=12, both branches, ~days)**; **D — isolate the cause (off-diagonals-OFF control on native
> S², ~16 h)** since off-diag-completion AND S³→S² both changed at once. Horizon hypothesis now LESS likely but
> formally open. `test_no_habit_pins` NOT flipped.
>
> **Guardrails hardened (COGNITIVE_CORRAL_TRIGGERS_SETUP.md, Option A):** CLAUDE.md `## DRIVER TRIGGERS` (6
> output-bound triggers + non-droppable allowed-lane clause) + harness HOOKS (`.claude/hooks/corral_trigger.py`,
> fire on Task/Agent/Bash — LIVE-confirmed) + memory FRESHNESS tags (read CURRENT only) + LLM export gate
> (`export_for_local_llm.py`, refuses untagged DATED) — wiring point for the local LLM (not yet installed).
> Blind-verified CLEAN-WITH-GAPS, gaps fixed (record `cognitive_corral_triggers_results.md`). Pending: confirm
> the DRIVER TRIGGERS section auto-loads in a FRESH session.
>
> **NEXT (gated on Charles + compute): the open solver follow-ups** — D (off-diag-OFF control, ~16 h) and/or B
> (Nr=12, ~days), neither started (correctly: firm guardrails before long solves). **THEN dynamic** (time-live /
> non-stationary native S² — the φ-angular hunch's home). Still owed before/with dynamic: check whether the
> GRAVITY sector also needs the SH-exact d/dθ (verify, don't assume). Op: run solves MYSELF, bounded, single
> process, background-notify, NO nohup, NO `| grep` (block-buffers → no live progress). archive/MIGRATION.md M4/M5/M6 = SUBSUMED.
>
> --- (HISTORICAL prior-session plan, all DONE — kept for provenance) ---
> **NEXT SESSION — DO NOT AUTO-BEGIN; DISCUSS WITH CHARLES FIRST (Charles 2026-06-25).** Open issues to discuss
> before any building/solving. **TOP CONCERN, OUTRANKS the kap8 analysis + the current trajectory: FIX THE SOLVER
> TRAJECTORY — its ONLY imports should be NUMERIC METHODS** (numpy/torch/scipy calculation primitives), nothing
> else, so every number is traceable to the action + numeric methods (no physics/mechanism smuggled via an import
> = calculation traceability). Needs a FULL AUDIT of the solver's imports (numeric method, or smuggled physics
> object?) and feeds the gate design (the solution-space gate has more to discuss too — incl. this solver audit).
> Charles is MORE concerned with this import-purity trajectory than with the kap8 analysis. **CRITICAL ORDER —
> you CANNOT gate an already-corrupted solver:** a gate PRESERVES a baseline, so gating the current (corrupted)
> solver would FREEZE the corruption and stamp it "clean" (false confidence). So: (i) AUDIT the solver (imports:
> numeric vs smuggled physics; BCs/ansatz/acceptance: imposed vs theory) → (ii) CLEAN to a numeric-only,
> imposition-free baseline → (iii) ONLY THEN build the gate to preserve it. Building the gate first (the (2)-first
> plan) was BACKWARDS. DISCUSS the audit + clean-up with Charles FIRST; the (1)/(2) plan below is SUBORDINATE.
> **GOAL after cleaning = EXPLORE the metric's solution space (OBSERVE what it does, let structure EMERGE) — NOT
> "then go do physics / get a result." The kap8 question is pursued ONLY as EXPLORATION (characterize, don't
> target), gated on Charles. Any "then physics"-style result-hunting framing is the drift — strike it.**
>
> **(prior plan, pending discussion) three Charles items — ORDER: do item (2) FIRST.**
> Item (2) — the anti-imposition GATE — comes BEFORE the item-(1) kap8 physics, not because it's "important"
> but because **the kap8 analysis IS the first live test of the gate** ("characterize the solution, don't
> demand smoothness"). Doing the physics without the gate in place just risks drifting again (the recurring
> failure). Infrastructure before exciting stuff ([[infrastructure-first-not-exciting-stuff]]). So: build the
> gate (2), THEN run the kap8 analysis (1) under it.
> 1. **Reconcile the kap8 alternatives by ANALYSIS, not numerics:** instead of grinding grids to tell "real
>    singularity vs under-resolved core vs bad-kap8," ANALYZE what the metric DOES at strong coupling using
>    the GR corpus (Principle 4). The self-gravitating global monopole is solved in GR: as the effective
>    deficit → 1 (critical), the core INFLATES into a de Sitter/horizon (supermassive global monopole,
>    Liebling/Maison). Likely: the kap8=1 warp-divergence is a REAL strong-field feature (a forming horizon),
>    not a bug. CAVEAT: transform under the DERIVED operator (e^{2φ} weight + X-kinetic change the critical
>    condition) — native re-derivation, NOT an import.
> 2. **HARDEN "explore the solution space, don't impose" into a GATE — TOP PRIORITY** (Charles 2026-06-25;
>    full detail in memory [[solution-space-not-imposition]]). A RECURRING DRIFT (multiple times in ~2 weeks):
>    we slide from EXPLORING the metric's solution space to IMPOSING the expected physics. Purity gates catch
>    *imports*; NOTHING catches *impositions*. A memory/tripwire is RECALL-class and ALREADY FAILED to stop the
>    drift — so it must become a GATE like the purity harness (binding + machine-run, NOT remembered). BUILD it
>    (parallel to how the purity gate was built: skill + harness + CLAUDE pointer):
>    (a) a BINDING TRIPWIRE in CLAUDE.md (always-loaded): before any solve/result, tag every BC / matter-sector /
>        coupling / acceptance-criterion as explored-free, pinned-by-THEORY (cite it), or pinned-by-HABIT
>        (= drift flag); and ask "does the diagnostic CHARACTERIZE the solution or FILTER it (demand a shape /
>        smoothness / the expected answer)?".
>    (b) a discipline skill `.claude/skills/solution-space-not-imposition` (the 4-point audit: ansatz/BC ledger;
>        acceptance-criterion audit; question audit vs the SM-template list lump/mass/particle/spectrum;
>        solution-space completeness — classify the solutions, don't just find the one you sought).
>    (c) a MACHINE component so it's ENFORCED not remembered — e.g. a required PREMISE-LEDGER section every
>        results doc must carry (a pin with no theory citation FAILS the check), and/or a lint in `tests/`; wire
>        the acceptance-criterion audit into verifier-before-record + a `completeness-map` criterion.
>    SALVAGE of the current solver = MINOR-to-MODERATE, periphery-not-core (the CORE residual = EL of the action
>    is faithful): reframe the GUARD from filter→CHARACTERIZER (minor); FREE the matter sector (the Θ(core)=π /
>    charge-1 pin → scan it) (moderate); the lump-questions are HABIT (method, not code). Do this BEFORE/ALONGSIDE
>    item 1 — the kap8 analysis IS the first live test of "characterize the solution, don't demand smoothness."
> 3. **Organize the repo — DONE 2026-06-25** (code split `prototype/`+`legacy/`; docs 274→111 live + 164→`archive/`;
>    3-pass agent-verified; INDEX refreshed — see archive/REORG_PLAN.md). REMAINING (minor): a future pass could archive
>    dead `native_*.py` (~1000 still flat in root) with the same import-safety check.
>
> RUN SOLVES YOURSELF via background-notify, NO nohup (it detaches from the tracker); guards are SLOW (hours).

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

## Foundation (what the p1 MIGRATION builds on) + read order

**The integrity-upgrades arc (P1-P5) is DONE** (records `p1..p5_*_results.md`; summary in LIVE.md): the purity
harness (`pytest tests/` = 23 pass / 5 documented-gap xfails), `solver_action.py`, the discipline skills, cross-model
verify, LIVE.md. **The 5 xfails = the MIGRATION acceptance tests** — the p1 migration (archive/MIGRATION.md) is flipping them
as it wires the DERIVED operator + native S² into the live `p1_residual`. M1 (derived op+φ) / M2 (X-kinetic→−2e5) /
M3 (Branch-P U) all GREEN to machine precision; M4a (kap8→1) RED = the open frontier (the e^{2φ} weight + Branch G/P
fork the arc flagged are now resolved-in-the-operator and clean; only the kap8 strong-matter divergence remains).

**The native-matter arc foundation** (2026-06-22, blind-verified; records = `matter_object_identity_native_vs_import`,
`complete_solver_stage1_general_einstein`, `native_s2_object_`/`twist_freed_`/`offround_twist_shear_results`): the
round/static soliton was an IMPORTED S³ Skyrme baryon; **UDT's NATIVE matter = the S²/π₂ winding (n=x/r) = a
scale-free global-monopole DEFECT in every STATIC config** — and its discreteness is the integer TOPOLOGICAL CHARGE
(Q=1, exact, native), NOT a localized lump (the "lump" search was FRAME CREEP — Charles's 2026-06-25 catch; the
winding-native ruler in `prototype/winding_native_diagnostics.py`). The gravity operator is DERIVED (vacuum≠GR,
weight e^{2φ}, a(φ)=e^{φ}); the migration is wiring it into `p1_residual` (branchGP, which prototyped it, is now a
reference in `prototype/`). The STANDING φ-angular hunch's untested home is the TIME-LIVE / non-stationary sector,
gated behind the kap8 question (M4b).

**Read order for a new instance:** (0) **LIVE.md** (THE only-guaranteed-current file; archive/MIGRATION.md is now `archive/`). (1) CLAUDE.md
"How we work" + ANTI-HANG + the `.claude/skills/` discipline skills; memories [[solver-migration-p1]],
[[branchP-solver-continuation-x-premise]], [[charles-workflow-preferences]] (double-check=agent passes),
native-matter-defect-import-discovery, solver-first-not-mechanism. (2) THIS FILE + archive/REORG_PLAN.md + the named results
docs. (3) CANON.md (C-2026-06-14-1; C-2026-06-18-1 — both SURVIVE); NEGATIVES_REGISTRY; FOUNDATIONAL_ASSUMPTIONS_LEDGER.
**HANDOFF_ARCHIVE.md + STATE.md + git + `archive/` = the deep historical record** (all pre-migration frontier blocks).

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
