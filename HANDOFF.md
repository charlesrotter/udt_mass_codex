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
> dropped). Determinacy blind-verified; re-solve stalled on conditioning. (Full session arc + next moves: `LIVE.md` FRONTIER.)

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
