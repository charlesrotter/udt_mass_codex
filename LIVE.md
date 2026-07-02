# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order:** LIVE.md FRONTIER → CLAUDE.md "How we work" + the discipline skills → (for detail) HANDOFF.md TOP
+ the five native-frame result docs + `discreteness_preregistration.md` → INDEX.md (repo map).

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/`), **completeness-map**.
- **DRIVER TRIGGERS (CLAUDE.md, always-loaded) + harness HOOKS** (`.claude/hooks/corral_trigger.py`, fires on
  Task/Bash/git-commit) make the corral fire WITHOUT being challenged — pause+honesty, never merit; the allowed-lane
  clause (category-A technique always GREEN) is non-droppable. **CONFIRMED LIVE (2026-07-01 startup): the
  `✓ CORRAL GUARDRAILS ACTIVE` banner appears + the 6 triggers auto-load** (self-check passed). Memory freshness: the
  TOP entry in MEMORY.md is the CURRENT frontier; older FRONTIER-labeled entries are tagged "SUPERSEDED as frontier"
  (durable lesson only); the rest are durable principle-memories. Read the TOP entry + this LIVE file for the live plan.
- **DATA-BLIND:** never load the six lepton wall numbers during a derivation (contract 26fc757). We
  predict RATIOS.
- **ANTI-HANG:** coupled solves are SLOW — bound the grid (Nr<=16/24), ONE clean process, never
  background-poll a solve.

## ============ CURRENT STATE (2026-07-02 EOD) — READ THIS FIRST ============
**⇒ WHERE WE ARE NOW: the ROUND-STATIC frame is EXHAUSTED (3 blind-verified layers, no cell) → RULING (Charles/claude.ai): this
is RISK 1 (round-static walls off discreteness), NOT a fourth object. NEXT = the STATIONARY (ω≠0) reduction — do it in a FRESH
session, MAP/counting FIRST (no auto-coding).**

THE ARC THIS SESSION (all CAS + BLIND-verified; each committed + pushed):
1. **CLOSED cell (H=0), N=1,2,3: NO cell** — geometry runs away / no finite stationary point (`cell_solver_f2d_first_build_results.md`,
   `cell_solver_f2d_N2_results.md`). Two-tier stability filter built+corrected (energy Hessian, not action). `verify_f2d_reduction.py` 11/11.
2. **EMBEDDED closure `H_cell(seal)=H_ambient` DERIVED+blind-verified** (`embedded_cell_closure_H_amb_results.md`; Weierstrass–Erdmann
   corner condition; ambient Misner–Sharp density sets cell size = the scale pin). **Embedded run: embedding RESCUES FINITENESS**
   (closes the runaway) but a Class-A mirror core is gradient-free/q≈0 → can't momentum-match a gradient-carrying ambient (`cell_solver_f2d_embedded_run_results.md`).
3. **CLASS-B charged core** (claude.ai rulings, `embedded_run_gate_rulings.md` + `embedded_classB_mini_MAP.md`, all blind-verified):
   **q CLOSES the flux match** (q≈Zq_A = canon charge=seal-flux) **but NO band** — a verified TWO-BRANCH MATTER wall: ρ'_amb>0 needs
   I_r>0 (airtight `π_ρ'=Zρφ'²−ξρI_r+κN²I_4θ/ρ³`) which does NOT emerge (V7: radial structure never free; verifier couldn't make I_r
   persist); ρ'_amb≤0 → R4 opens but R5 (skin E_ang matter match) blocks (`cell_solver_f2d_classB_run_results.md`).

**THE RULING (Charles/claude.ai 2026-07-02 — pre-committed tripwire fired: 3rd object failed → REFRAME, not 4th object):**
- The obstruction walked cleanly GEOMETRY→FLUX→MATTER-STRUCTURE and localized as **"nothing in the round-STATIC frame FORCES
  radial matter structure."** V7 is a STATIC theorem. That is RISK 1 knocking. The proposed 4th object (a matter-BC'd/unwound
  core) is **REJECTED**: f(r_c,θ)=0 breaks the degree/pole BC f(r,π)=π → axis term N²sin²f/sinθ diverges (infinite energy); the
  pole-respecting repair h(θ)≠θ is an arbitrary infinite-dim function = an X-kluge. Do NOT spec it.
- **NEXT = the STATIONARY internal-rotation reduction: extend the winding phase Nψ → Nψ + ωt.** From the metric g^tt=−e^{2φ}
  weights the ω² term with e^{2φ} → **positional time dilation couples DIRECTLY to internal frequency** = the φ-angular coupling
  the static frame structurally LACKS, and exactly the shape of the missing forcing (= Charles's founding φ-angular hunch). Evades
  V7 (static assumption); native Derrick-evasion; **mass ~ ω would be geometric.** Tagged DIRECTION, not result.
- **FIRST DELIVERABLE (fresh session): the ω≠0 mini-MAP — recompute the ROUND reduction with the time-live phase, FULL nonlinear
  e^{2φ} factor, COUNTING FIRST** (as every mini-MAP this session: state determinacy before running; gate with claude.ai; CAS+blind
  the reduction before banking). Connects to memory [[frontier-time-live-native-matter]] / [[everything-on-solver-build]] (the prior
  time-live arc) and [[project-ownership-and-hunch]] (φ-angular discreteness).
  **START FROM:** the STATIC round reduction to extend is in `round_matter_reduction_results.md` (the S² winding matter reduction:
  `ρ''_m=(e^{2φ}/4)(ξρI_r−κN²I_4θ/ρ³)`, moments I_r/I_4θ, the f(r,θ) EOM) + `cell_solver_round.py` (the 1-D φ,ρ solver header EOMs);
  the ω≠0 task is to redo that reduction with n's phase Nψ→Nψ+ωt so g^tt=−e^{2φ} weights the new ω² term. **"V7"** (cited throughout
  as "radial structure is never energetically free / rigid is a strict min") = the second-variation result in
  `f2d_virial_step0_results.md` (V7), blind-verified — the static theorem the ω≠0 frame is meant to EVADE.

**METHOD THAT WORKED THIS SESSION (keep it):** mini-MAP with counting done HONESTLY before any run → claude.ai gate ruling → CAS +
BLIND-verify the derivations → build/run bounded (anti-hang) → BLIND-verify the run (attack the load-bearing claim hardest) →
commit PROVISIONAL/scoped, NEVER a frame verdict. Every ruling/derivation/run this session was blind-verified before banking.
See memory [[treat-handoff-docs-as-binding-spec]] + [[decide-with-charles-not-forge-ahead]] (two corrections Charles made early).

### ↓↓↓ HISTORICAL — ARCHIVED 2026-07-02
- The **2026-07-01 native-frame FOUNDATION** (EH-empty; native bulk action `(r²φ')'=0`; matter φ-blind;
  constrained-two-player; G/P regimes; G↔P switch criterion; native geometric action + off-round K²-exclusion;
  Z_φ fork; seal JC1/JC2 + seal-parity Class A/B) **and the now-EXECUTED round-static "IMMEDIATE NEXT ACTION"**
  (build the f(r,θ) finite-mirror eigenproblem) moved to `archive/LIVE_native_frame_round_static_2026-07-01.md`.
  The native frame is STILL VALID (canonical record = the five result docs named in the CURRENT STATE block);
  it is no longer the frontier because the round-static build it pointed to RAN and exhausted (→ Risk 1 → ω≠0).
  **RISK 1 is now CONFIRMED as the wall**; RISK 2 (Z_φ fork, `e^φKφ'` mixing) is still open, gates ratios later.
- The **2026-06-29→30 basin / D1 / galerkin / X-kluge arc** → `archive/LIVE_basin_D1_galerkin_arc_2026-06-30.md`.

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
