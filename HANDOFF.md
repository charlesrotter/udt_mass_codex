# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
>
> **CURRENT ACTIVITY (2026-06-25): the p1 MIGRATION — read `MIGRATION.md`.** The 2026-06-23 Branch-P/JFNK
> push (historical, below) led to: caught X=−2e5 as a chosen placeholder, built continuation-in-X, found the
> winding-native ruler (topological charge Q=1 = the real native discreteness; the "lump" question was frame
> creep — Charles's catch), diagnosed branchGP's matter-warp as branchGP-specific. Charles then REPEALED the
> file-immutability rule and decided to EXTEND the hardened `p1_residual_general_einstein.py` to the derived
> operator (not canonize the un-harnessed branchGP prototype), incrementally, with a solve-level convergence
> GUARD (`migration_convergence_guard.py`). **DONE: M1 (derived op+φ) / M2 (X→−2e5) / M3 (Branch-P U, deep
> φ=2.2) all GREEN; M4a (kap8 0.05→1.0 derived) = RED** — warp diverges with Nr (3.98→8.42). branchGP's
> divergence is LOCALIZED to the **kap8=1 strong-matter coupling** (NOT operator/X/U/S²-vs-S³).
>
> **NEXT SESSION — three Charles items (discussed 2026-06-25, HOLD until next session):**
> 1. **Reconcile the kap8 alternatives by ANALYSIS, not numerics:** instead of grinding grids to tell "real
>    singularity vs under-resolved core vs bad-kap8," ANALYZE what the metric DOES at strong coupling using
>    the GR corpus (Principle 4). The self-gravitating global monopole is solved in GR: as the effective
>    deficit → 1 (critical), the core INFLATES into a de Sitter/horizon (supermassive global monopole,
>    Liebling/Maison). Likely: the kap8=1 warp-divergence is a REAL strong-field feature (a forming horizon),
>    not a bug. CAVEAT: transform under the DERIVED operator (e^{2φ} weight + X-kinetic change the critical
>    condition) — native re-derivation, NOT an import.
> 2. **Are we exploring the metric's solution space, or imposing physics motivations?** The guard's "must
>    floor + N-converge" criterion silently expects smooth/localized solutions; if the metric forms a horizon,
>    the guard calls real physics a "failure" (same pattern as the lump-ruler + box-control demand). Lean: let
>    the metric show its full solution space (incl. horizons/singular branches); OBSERVE, don't "fix" the kap8
>    divergence into convergence if it's the metric being honest. (Ties to item 1.)
> 3. **Organize the repo:** legacy/stale → subfolders. `legacy/` (superseded research + reduced solvers),
>    `prototype/` (branchGP_* + the session's one-off drivers jfnk_*/equilibrated_*/x_continuation/sharpen_*/
>    grid_refine_*/seal_test/probe_phi_terms), lean working root (canonical p1+branch_operator+full3d+b1prime+
>    whole_metric, tests/, the guard, the live records). CAUTION: moving files changes import paths — one
>    careful reorg commit, verify harness+solver still run.
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

## Foundation (the parked physics the Branch-P push builds on) + read order

**The integrity-upgrades arc (P1-P5) is DONE** (records `p1..p5_*_results.md`; summary in LIVE.md). Built the
purity harness (`pytest tests/` = 23 pass / 5 documented-gap xfails), the single source-of-truth `solver_action.py`,
the discipline skills, cross-model verify (`CROSS_MODEL_VERIFY.md`), and LIVE.md. **The 5 xfails + the P2 baseline =
the MIGRATION acceptance tests** (wiring the DERIVED operator + native S² into the live `p1_residual`). Migration
must also resolve the two MIGRATION-OPEN-PHYSICS items the arc surfaced (tripwired, do NOT silently resolve to pass
a test): the curvature **Branch G/P fork** (= the φ-angular tension; native-S² silently used Branch G — the Branch-P
push is testing it) and the **e^{2φ} matter weight** (PARTIALLY-TRACED, a flagged CHOSE; P4 cross-model verified).

**The native-matter arc foundation** (2026-06-22, blind-verified; records = `matter_object_identity_native_vs_import`,
`complete_solver_stage1_general_einstein`, `native_s2_object_`/`twist_freed_`/`offround_twist_shear_results`): the
round/static soliton was an IMPORTED S³ Skyrme baryon; **UDT's NATIVE matter = the S²/π₂ winding (n=x/r) = a
scale-free global-monopole DEFECT, not a localized particle, in every STATIC config played — but ALL on Branch G**
(now made explicit; the Branch-P push tests whether keeping the φ-angular potential changes this). The gravity
operator is DERIVED (vacuum≠GR, weight e^{2φ}, a(φ)=e^{φ}) but NOT yet wired into the live solver. The STANDING
HUNCH places discreteness at the TIME-LIVE / non-stationary sector — the one major untested instrument; the Branch-P
static push is the prerequisite probe before time-live.

**Read order for a new instance:** (0) **LIVE.md** (the only-current file — frontier + next action). (1) CLAUDE.md
"How we work" + the ANTI-HANG rule + the `.claude/skills/` discipline skills; memories native-matter-defect-import-discovery,
full-dimensional-complete-solver, gravitating-soliton-stability-test, solver-first-not-mechanism. (2) THIS FILE +
the named results docs for detail. (3) CANON.md (C-2026-06-14-1 native S² carrier + B=1/A; C-2026-06-18-1 metric
from relativity — both SURVIVE); NEGATIVES_REGISTRY; COMPLETION_PROGRAM.md / FOUNDATIONAL_ASSUMPTIONS_LEDGER scoreboard.
**HANDOFF_ARCHIVE.md + STATE.md + git = the deep historical record** (all pre-2026-06-22 frontier blocks; the verbose
2026-06-23 integrity-arc + 2026-06-22 native-matter blocks were trimmed here 2026-06-23 LATE — their full detail is
in the results docs above).

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
