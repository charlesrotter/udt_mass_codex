# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
>
> **CURRENT ACTIVITY (2026-07-01 — see LIVE.md "FRONTIER" block, authoritative). TWO PHASES this session:**
>
> **PHASE 1 — the whole native frame DERIVED (the big arc).** The 2026-06-30 basin work (HISTORICAL note below)
> chased the X=−2e5 kluge → the e^{2φ} matter-weight → and found the whole live "two-player scalar-tensor" frame
> (φ OUTSIDE the metric) was a CHOSE extension, NOT canonical UDT. So Charles DERIVED UDT's field equations natively
> (in-session); the driver CAS-verified AND blind-adversarially verified every step. Results (each its own doc):
> **EH is EMPTY on the canonical family** (√-g R = boundary term → "vacuum=GR" was the Principle-7 scar, not a result);
> native frame = **CONSTRAINED-TWO-PLAYER** (φ = longitudinal dilation INSIDE g; h_AB = independent transverse
> 2-geometry) → **the old solver was the WRONG frame**; **matter is φ-BLIND** → the whole basin/X/e^{2φ} saga was a
> NON-native artifact, EXPLAINED + retired; **G/P switch criterion** (pinned aspect ratio χ); **native geometric
> action** (angular-mismatch, 𝒦 genuinely bulk, EH the empty red herring); **off-round uniqueness** (𝒦=K_ABK^AB−K²
> forced, independent K² excluded, only the Z_φ fork left); **seal junctions** (JC1: external charge = seal FLUX;
> JC2: e^{2φ} weight-jump; seal parity = two classes). Docs: `native_field_equations_constrained_two_player_results.md`,
> `gp_switch_criterion_results.md`, `native_geometric_action_results.md`, `seal_matching_junction_results.md`.
>
> **PHASE 2 — RETURN TO THE SOLVER** (Charles: "more derivation risks substituting for letting the geometry speak").
> Pre-registration FROZEN before solving (`discreteness_preregistration.md`): binding rule = **"solve the SPACE, not
> the electron"**; a UDT cell is a **finite MIRRORED domain** (not a lump in flat space — the infinity test is a
> control only); Class A first = closed topological cell modes (smooth mirror seal φ'=ρ'=0, q=0, isolated cell sizes
> per integer winding N); Class B later = charged pinned seal (q≠0); **N (sector) ≠ q (flux)**; 9 acceptance criteria;
> no per-solution retuning. **Repo CONSOLIDATED** (1086 one-off .py → `legacy/root_oneoffs_2026-07-01/`; root 1113→27
> .py; pytest 32/1xfail). **First solver built** (`cell_solver_round.py`): the derived frame makes the round cell a
> CHEAP 1-D system — TWO fields φ(r),ρ(r) (ρ dynamical; areal ρ=r is the neutral sub-case). Vacuum mirror cell is
> TRIVIAL → needs MATTER. **Round S² winding matter reduced + CAS-verified** (`round_matter_reduction_results.md`):
> ρ-source `ρ''_m=(e^{2φ}/4)(ξρI_r − κN²I_4θ/ρ³)`; **RIGID hedgehog (f=θ, I_r=0) → the cell COLLAPSES** (real, verified,
> not a sign bug — rigid kills the outward ξρI_r channel).
>
> **IMMEDIATE NEXT (build, next session) = the MINIMALLY-FREE axisymmetric field f(r,θ)** (n=(sin f cosNψ, sin f sinNψ,
> cos f); rigid=f=θ): a 2-D finite-mirror eigenproblem coupling f(r,θ) to φ(r),ρ(r) on a finite mirrored radial domain
> (pole BCs f(r,0)=0,f(r,π)=π; mirror seal BCs). Matter EOM in `round_matter_reduction_results.md`. Do NOT insert I_r
> by hand — let the BVP decide if f develops radial structure I_r>0 that balances the inward pull to a stable size
> (balance ρ⁴~κN²I_4θ/(ξI_r)). Look for ISOLATED cell lengths (φ,ρ,f close), UNLABELED, fixed Z_φ/ξ/κ/N. Still collapses
> → scoped negative (go freer/off-round); isolated modes → the FIRST real discreteness signal. One open constant = Z_φ
> (held fixed; free vs =8-with-forced-mixing fork → consilience later).**
> --- HISTORICAL (2026-06-29→30, SUPERSEDED by Phase 1): D1 determinacy fix → galerkin conditioning → basin audit →
> X-kluge. That arc was the trail that led to Phase 1's discovery that the live FRAME itself was un-derived; it lives
> in LIVE.md's HISTORICAL blocks. Pre-2026-06-30 HANDOFF detail in `HANDOFF_ARCHIVE.md`.

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
minimally-free `f(r,θ)` is the next test (see LIVE.md). The φ-angular hunch now appears NATIVELY (Branch-P `𝒦`-source;
the route-B kinetic-completion mixing term; the seal source that charges a matter cell).

**Read order for a new instance:** (0) **LIVE.md FRONTIER block** (THE only-guaranteed-current file). (1) CLAUDE.md
"How we work" + ANTI-HANG + the `.claude/skills/` discipline skills; frontier memory **[[native-field-equations-frontier]]**
+ the principle memories ([[apply-purist-logic-proactively]], [[solution-space-not-imposition]],
[[charles-workflow-preferences]], native-matter-defect-import-discovery, solver-first-not-mechanism). (2) THIS FILE +
the five native-frame result docs + `discreteness_preregistration.md` + `round_matter_reduction_results.md` +
`cell_solver_round.py`. (3) CANON.md (C-2026-06-14-1; C-2026-06-18-1 — both SURVIVE); NEGATIVES_REGISTRY;
FOUNDATIONAL_ASSUMPTIONS_LEDGER. **HANDOFF_ARCHIVE.md + STATE.md + git + `archive/` = the deep historical record.**

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
