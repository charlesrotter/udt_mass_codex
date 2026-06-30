# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
>
> **CURRENT ACTIVITY (2026-06-30 EOD — see LIVE.md "CURRENT STATE" block, authoritative): THE BIG DISCOVERY —
> X=−2e5 (dilaton kinetic/curvature ratio) is a Cassini-FORCED FIT mis-tagged `# FREE`; 2 audits (incl. blind)
> confirm it's the LONE observation-fit kluge on the live path → PIVOTED to EXPLORE X (object is X-stable). The
> whole conditioning saga is RESOLVED in understanding (none indicted the metric). Built the GALERKIN BC-recombined
> basis + seal-BC reconciliation → the determined solve now DESCENDS 6 orders (conditioning FIXED). REFRAMED after an
> external audit (NEUTRAL framing per the anti-imposition gate — NO merit judgment): there are TWO under-converged
> BASINS — Branch A (LM/crawl, alive dilaton, ~2e-3) vs Branch B (cold-galerkin, ~1.5e-5 but dead-dilaton/extreme-warp,
> physical-band); NEITHER is "the physical object". NEXT (next session, context-limited) = a **BASIN AUDIT**: continue
> BOTH under identical fair globalization + a per-run manifest, **CLASSIFY don't select**, reject only vs a
> PRE-REGISTERED geometric criterion. Do NOT do "LM-to-close → galerkin-polish" alone (biases Branch A by construction).
> Then re-grade across X + blind-verify; the e^{2φ}-weight (couples to Branch B's dead dilaton) + φ-seal-parity soft
> DERIVED-headlines; then DYNAMIC. Records: `EXTERNAL_AUDIT_2026-06-30.md`, PROVENANCE_AUDIT_2026-06-30.md, D1_FIX_DESIGN.md.**
> --- The full 2026-06-29→30 arc (D1 determinacy fix → re-solve stall → X-kluge discovery → galerkin) lives in
> LIVE.md's frontier (CURRENT + HISTORICAL blocks). Pre-2026-06-30 HANDOFF detail archived to `HANDOFF_ARCHIVE.md`.

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

**The static solver is CODE-COMPLETE** (the p1 MIGRATION + integrity-upgrades arc are DONE — archived; details in
`HANDOFF_ARCHIVE.md`): purity harness `pytest tests/` = **32 passed / 1 xfailed** (the 1 = the G/P-fork + charge-1-core
HABIT-pin gate), `solver_action.py`, the discipline skills, cross-model verify. The DERIVED operator (e^{2φ} weight,
a(φ)=e^{φ}) + native-S² matter are wired into the live `p1_residual`. (M2's X-kinetic value −2e5 is the one later
caught as the **Cassini KLUGE** — see LIVE.md CURRENT STATE + `PROVENANCE_AUDIT_2026-06-30.md`.)

**The native-matter arc foundation** (2026-06-22, blind-verified; records = `matter_object_identity_native_vs_import`,
`complete_solver_stage1_general_einstein`, `native_s2_object_`/`twist_freed_`/`offround_twist_shear_results`): the
round/static soliton was an IMPORTED S³ Skyrme baryon; **UDT's NATIVE matter = the S²/π₂ winding (n=x/r) = a
scale-free global-monopole DEFECT in every STATIC config** — and its discreteness is the integer TOPOLOGICAL CHARGE
(Q=1, exact, native), NOT a localized lump (the "lump" search was FRAME CREEP — Charles's 2026-06-25 catch; the
winding-native ruler in `prototype/winding_native_diagnostics.py`). The gravity operator is DERIVED (vacuum≠GR,
weight e^{2φ}, a(φ)=e^{φ}) and is wired into the live `p1_residual` (branchGP, which prototyped it, is now a reference
in `prototype/`). The STANDING φ-angular hunch's untested home is the TIME-LIVE / non-stationary sector (DYNAMIC),
gated behind flooring the determined static solve on the right branch (see LIVE.md NEXT ACTION).

**Read order for a new instance:** (0) **LIVE.md "CURRENT STATE" block** (THE only-guaranteed-current file). (1) CLAUDE.md
"How we work" + ANTI-HANG + the `.claude/skills/` discipline skills; frontier memory [[d1-fix-and-matter-fork-resolved]]
(the X-kluge/galerkin state) + [[apply-purist-logic-proactively]], [[solution-space-not-imposition]],
[[charles-workflow-preferences]], native-matter-defect-import-discovery, solver-first-not-mechanism. (2) THIS FILE +
`PROVENANCE_AUDIT_2026-06-30.md` + `D1_FIX_DESIGN.md` + the named results docs. (3) CANON.md (C-2026-06-14-1;
C-2026-06-18-1 — both SURVIVE); NEGATIVES_REGISTRY; FOUNDATIONAL_ASSUMPTIONS_LEDGER.
**HANDOFF_ARCHIVE.md + STATE.md + git + `archive/` = the deep historical record** (all pre-2026-06-30 frontier blocks).

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
