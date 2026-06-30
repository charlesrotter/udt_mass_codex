# LIVE — the only guaranteed-current file (READ ME FIRST)

Everything here is true RIGHT NOW. `HANDOFF.md` / `STATE.md` are detailed history; **if they
disagree with this file, THIS file wins.** No stale next-steps live here.
**Read order:** LIVE.md → CLAUDE.md "How we work" + the discipline skills → (for detail)
HANDOFF.md TOP → INDEX.md (repo map).

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/`), **completeness-map**.
- **DRIVER TRIGGERS (CLAUDE.md, always-loaded) + harness HOOKS** (`.claude/hooks/corral_trigger.py`,
  fires on Task/Bash/git-commit) now make the corral fire WITHOUT being challenged — pause+honesty, never
  merit; the allowed-lane clause (category-A technique always GREEN) is non-droppable. Memory freshness:
  every DATED memory carries a CURRENT/SUPERSEDED/HISTORICAL tag (read CURRENT only). Local-LLM cross-check
  to come — wiring = `export_for_local_llm.py` (refuses untagged DATED). Record = `cognitive_corral_triggers_results.md`.
  **PENDING — FIRST ACTION next fresh session (catch-proof §4, Charles will verify):** confirm the `## DRIVER
  TRIGGERS` section AUTO-LOADS — before touching any file, recite the 6 triggers / the allowed-lane clause from
  context; if present unprompted, §4 passes. (Could not self-certify the building session: the section was added
  AFTER that session's CLAUDE.md auto-load.) **DRY-RUN (2026-06-27, empty-instance agent ae0d35a4): a fresh
  SUBAGENT did NOT see the section in its auto-loaded CLAUDE.md (it had How-we-work + Orientation but not the
  Discipline-skills/DRIVER-TRIGGERS block) — a YELLOW FLAG, not a verdict (subagent context may differ from a
  top-level session). BUT the harness HOOKS fired regardless, so enforcement is LIVE either way. → The HOOKS
  (Part B) are the load-bearing mechanism; if the top-level fresh session ALSO lacks the auto-load, rely on the
  hooks and/or relocate `## DRIVER TRIGGERS` earlier in CLAUDE.md (right after "How we work").**
  **HOW YOU'LL KNOW IF THE HOOKS FAIL:** a `SessionStart` hook now prints **`✓ CORRAL GUARDRAILS ACTIVE`**
  at the TOP of every session (+ the startup self-check prompt). Its PRESENCE = hooks loaded (Part B live);
  its ABSENCE at session start = hooks did NOT load — the loud failure signal. (Per-tool-call DRIVER TRIGGER
  reminders are the other visible signal.) First live confirmation = the banner appearing next session.
- **DATA-BLIND:** never load the six lepton wall numbers during a derivation (contract 26fc757). We
  predict RATIOS.
- **ANTI-HANG:** coupled solves are SLOW — bound the grid (Nr<=16/24), ONE clean process, never
  background-poll a solve.

## ============ FRONTIER (2026-06-29 PM) — READ THIS FIRST (only DURABLE CANON follows) ============
**One-line state:** D1 determinacy FIXED+blind-verified (null-dim 0). The **core-BC FORM artifact is now FIXED+
symbolically-verified too** — P1-(1) RAN: the core had copied the SEAL's metric-component Neumann `∂_r g_θθ=0`,
which at the finite cutoff forces the spurious stiff Robin `c'(rc)=−1/rc=−10` (the attempt-1 stall). DERIVED
correct form = gentle bare-warp Neumann `c'(rc)=0` (rigid hedgehog `T^θ_θ=(e^{−2c}−e^{−2d})/2r²` → angular block
NOT singularly sourced, vanishes at c=d; global-monopole/BV structure). Implemented (rows 222/223/229 core slots),
pytest 32/1xfail, determinacy preserved. **RE-SOLVE ATTEMPT 2** (warm-start from old field, FIXED X=−2e5):
**UNBLOCKED but not floored** — Phi 6.3e10 → 9.6e-2 over 60 MONOTONE steps at the PRODUCTION X (attempt-1
death-spiraled at the easy X≈−1), then a slow ~4%/step LINEAR tail = the residual cond≈1e11 (Chebyshev ENDPOINT
AMPLIFICATION, smax≈7e6 — a SEPARATE source the BC fix doesn't touch) is now rate-limiting. So: the BC-form
artifact is CONFIRMED+removed (the binding stall), but **"floors with just the BC fix" was OVER-OPTIMISTIC — the
parity/Galerkin basis + Ruiz equilibration (Category-A conditioning) is genuinely needed to floor + re-grade.**
RE-GRADE is PROVISIONAL only (Phi not floored; qualitative survives — Q=0.990/|n|=1/gentle-φ/lapse 3.2 no-horizon;
quantitative NOT banked). `determined=True` stays NON-default until it floors; old path intact.
**CONDITIONING: equilibration RULED OUT (structural, not scaling).** Tried Ruiz row+col (cond→3e5 but row-reweight
corrupts the ‖F‖² objective → drives true residual UP to 7e3, garbage) and column-only (objective-safe but cond~1e9,
genuine near-null smin~6e-9). The ill-conditioning is **structural Chebyshev endpoint differentiation amplification**
(d_r ~O(N²) at rc,ri) — rescaling can't fix it. **DECISION (Charles 2026-06-29): build the principled discretization
fix.** Phase 1 = targeted corpus research RUNNING (which well-conditioned spectral method for our finite-shell
singular-core coupled mixed-BC system: integration/quasi-inverse (ultraspherical/Olver–Townsend) vs Galerkin
recombination vs parity — parity's r^l is flagged for SMOOTH origins, ours is singular). Phase 2 = build + revalidate
conditioning + re-solve + re-grade. OPERATIONAL: next solve UNBUFFERED (python3 -u, NO grep pipe — it hid progress 2.5h).
Records: `D1_FIX_DESIGN.md` (P1-(1) + CONDITIONING INVESTIGATION). Matter-model fork RESOLVED (rigid unit / amplitude=gated import).
**SOFT-MODE CHARACTERIZED (2026-06-29, Charles "derive don't assert"):** the 2 near-null directions (smin~1e-4, NOT
the 6e-9 garbage-point value) are DERIVED SYMMETRIES — mode#1 = the matter SO(3) ROTATION (79% overlap w/ ω_z×n,
77% matter, invariants unmoved), mode#2 = a metric DIFFEOMORPHISM gauge mode (off-diag, invariants unmoved). **No
imposition needed** — they're the action's own rotation+coordinate invariance, benign, LM-damping-handled; smin is
NOT a flooring obstruction. So the ONLY remaining obstruction = smax~7e6 (Chebyshev endpoint amplification), a pure
Category-A numerical fix. **NEXT (in progress): mapped/declustered radial grid (KTE-type) to reduce smax → re-solve
+ floor.** (`d1_softmode_characterize.py`; blind-verify the symmetry finding owed before banking.)

**GIT: push went down mid-session (auth) then RESTORED 2026-06-29 — fully synced (origin/main == HEAD). No
unpushed commits.** (If push fails again it's auth: `gh auth login`.)

### NEXT-SESSION PRIORITIES (P1–P4; recommendation, not a menu)
- **P1 — make the determined posing FLOOR, then RE-GRADE. [moves (1)+(2) DONE 2026-06-29 PM]** Done: (1) the
  core-BC FORM check FOUND+FIXED the −10 artifact (warp-Neumann c'(rc)=0; symbolically verified); (2) the
  warm-start fixed-X re-solve UNBLOCKED the solve (Phi 6.3e10→9.6e-2 monotone at production X). **REMAINING = the
  FORK (decision for Charles):** the solve does NOT floor — a slow linear tail = residual cond≈1e11 (Chebyshev
  ENDPOINT amplification, smax≈7e6, a separate source). So **(3) the conditioning build IS genuinely needed:**
  Ruiz equilibration first (cheap row/col scaling, can drop cond orders) → parity/Galerkin basis-recombination
  (bakes regularity into the basis, kills endpoint amplification) if equilibration alone is insufficient; possibly
  examine the φ-core pin (d_rφ=0 may want a log). **(4) then RE-GRADE** ρ_max/warp/charge/caveat-#3 + blind-verify.
  Per fix-all-flaws this is a static RED gate to clear before time-live, AND the same conditioning the time-live
  solver needs — so building it now serves both. **The deliberate decision LIVE flagged: build it now vs fold into
  the time-live solver build.**
- **P2 (parallel, when the 2nd adversarial model lands) — CROSS-MODEL verify** this session's load-bearing,
  same-tier-only results: the matter-model fork (rigid unit / amplitude=gated-import / amplitude≠φ), the D1
  determinacy, the derived BC table.
- **P3 (after D1 solves) — the rest of the fix-first list:** A2/D5 (tag e^{2φ} weight + ξ=κ provenance), G3
  (stability notion on the 11-field object), §3-iii consolidation (one canonical solver — good dedicated workflow),
  cheap bugs C5/D4. Clearing these = "no red gates."
- **P4 — DYNAMIC (time-live native S²)** — the actual physics frontier + the φ-angular hunch's home; gated behind P3.
- **Calibration:** D1 is INFRASTRUCTURE (necessary per fix-all-flaws-before-dynamic, not the physics). If P1-move-1
  shows the stiffness was a BC-form artifact → cheap win; if it genuinely needs the parity/Galerkin build → a
  deliberate decision, and a fair moment to ask whether to do that conditioning work now vs fold it into the
  time-live solver build (which needs robust conditioning anyway). **Recommended first move: P1-(1), the cheap core-BC-form check.**

### This session's arc (all committed; all blind-verified unless noted)
1. **kap8 caveat #2 CLOSED** (`92e363a`): native-S² winding SURVIVED (degree Q≈1, real matter) — verifier `a63753fff`.
2. **kap8 caveat #3 CLOSED** (`d3d81be`): off-diagonals EXCLUDED as the warp-tamer (Nr=8 same-grid +0.7%) — `ae5a16bb`.
3. **NATIVE REFRAME** (`772e6f5`): the kap8 object is a **core-concentrated degree-1 S² winding DEFECT in a gentle
   dilation well — NOT a forming horizon** (the GR "compact/near-horizon" reading was a misapplied ruler) — `a9efe4b`.
4. **Spectral check** (`1750f24`): the SMOOTH sector (φ/lapse/interior) is RESOLVED at Nr=8 → Nr=12 LOW-value; the
   "fat tails" are a benign BC step + the inherent rc-regulated singular core — `a73caf9`.
5. **BROAD-SWEEP SOLVER AUDIT** (`0086672`, 21-agent workflow, `SOLVER_AUDIT_2026-06-29.md`): physics core
   TRUSTWORTHY (no smuggled GR/mechanism), FIX-FIRST a bounded list before time-live. Top finding = D1.
6. **D1 CONFIRMED** (`ad5df06`): the static solve is UNDERDETERMINED — residual = 1776 eqns / 4224 unknowns at
   Nr=8 (body mask `[3:Nr-3]` imposes the PDE on only 2 of 8 radial layers; most fields singly-BC'd), Jacobian
   full ROW rank 1776 → 2448-dim null space; 58% of DOF set by seed/min-norm, not the metric — `a5e07d7`.
   Localization: 85% of the slack in excised core/seal layers; qualitative/topological claims (winding degree,
   not-a-horizon, gentle-φ) SURVIVE; the QUANTITATIVE core-dominated numbers (ρ_max, warp magnitudes, charge
   profile) are SOFT → must re-grade on a determined solve.
7. **GR-NUMERICS RESEARCH** (`a0f381a`, `GR_NUMERICS_RESEARCH_2026-06-29.md`, deep-research, 25 claims verified):
   proven posing — impose the PDE at every interior node + sufficient endpoint BCs → determined square system;
   origin regularity via parity (r^l), not excision.
8. **|n|=1 / amplitude FORK RESOLVED** (`2151ccd`, `715c8e4`; `winding_amplitude_gauge_derivation_results.md`,
   `matter_amplitude_native_MAP_2026-06-29.md`; verifiers `a803da6`/`a12f170`/`ac20415`): the matter field is the
   verified RIGID UNIT field (amplitude is an exact gauge null mode; e^{2φ} gives it no dynamics; unit-ness is an
   un-derived POSIT but the alternative — a linear-σ amplitude field — needs an imported Mexican-hat V(A) =
   Category-B, and the amplitude is NOT φ). So UDT-as-derived gives the rigid intrinsically-singular core WITHOUT
   import. The native exploration (Charles's anti-myopia push) VINDICATED the rigid path by derivation, not default.
9. **D1 FIX DESIGNED + BCs DERIVED + VERIFIED** (`5fe1a44`, `898fbd4`; `D1_FIX_DESIGN.md`; verifiers
   `a71a586`/`aecae70`/`aeb0ab5`): see the IMPLEMENTATION SPEC immediately below.

### D1 IMPLEMENTATION SPEC — ✅ DONE (implemented `bdcc705`; determinacy blind-verified). This is the RECORD of what was built, NOT a pending action. (The pending action is the conditioning/re-solve phase in the one-line state above.) Spec also in `D1_FIX_DESIGN.md` "DERIVED BC TABLE".
Re-pose `p1_residual_general_einstein.py::residual_vector_p1` as a DETERMINED square system:
- **Interior:** impose the 11 coupled rows at ALL non-endpoint radial layers `[1:Nr-1]` (replace the `body=[3:Nr-3]`
  excision in `full3d_spectral.py:129-130` usage — do NOT re-excise, that IS D1).
- **Endpoint closures (DERIVED, verified — from the seal mirror-fold parity + core r^l regularity + topology):**
  - a: seal a=0 (gauge), core ∂_r a=0. b: seal Neumann ∂_r(g_rr)=0, core b=−p (depth dial, **honor p — fixes D4 bug**).
  - c,d: BOTH ends **Neumann on the METRIC COMPONENT** (∂_r g_θθ=0, ∂_r g_ψψ=0 — NOT the bare warp; Robin in warp vars).
  - **e_rt, e_rp: Dirichlet =0 at BOTH ends** (one radial index → reflection-odd). **e_tp: Neumann at both ends**
    (tangential-tangential → even). [This CORRECTS the old blanket choice — get the off-diagonal split right.]
  - φ: seal **φ=0** (mirror-odd = domain definition, derived default — Charles confirmed-pending but proceed), core ∂_r φ=0.
  - matter n1,n2,n3: 2× tangential Neumann (∂_r n̂_⊥=0) + |n|=1 algebraic at every node; **DROP the seal direction
    value-pin** (degree topologically conserved under |n|=1 — the pin was redundant/over-imposing).
- **Count:** interior 6×48×11 + endpoints 2×48×11 = **4224 == cols** at Nr=8 (Dirichlet↔Neumann = 1-for-1 row swap).
- **DETERMINACY CHECK (the milestone):** rebuild the Jacobian (the `d1_determinacy_check.py` pattern) → expect
  **rank==4224, null-dim 0** (vs current null-dim 2448). THIS is the pass/fail gate for the fix.
- **RISK (flagged, must handle):** dropping the excision re-exposes Chebyshev endpoint conditioning on the steep
  warps — use the research's parity/Galerkin basis + pole-stable hybrid; **re-validate conditioning** (flat-space
  error-growth test), do NOT re-excise. **Owed + now load-bearing:** SH-exact d/dθ in the GRAVITY sector
  (`full3d_grid_shexact.py` exists, not wired) — the off-diagonal rows are now active everywhere.
- **THEN:** bounded re-solve (SLOW, hours — run MYSELF, single process, background-notify, NO nohup) → **RE-GRADE**
  the soft quantities (ρ_max, warp magnitudes, charge E(<r), caveat #3 warp-comparison) vs the old min-norm values;
  qualitative claims expected to survive, quantitative numbers may move. Blind-verify; cross-model when 2nd model lands.
- **Residues for Charles (only non-derived choices):** φ(seal)=0 canon-confirm (derived default holds); rc finite-core
  model = justified CHOSE. Everything else in the BC table is DERIVED + blind-verified.

### Other fix-first items still open (after D1, before time-live) — from `SOLVER_AUDIT_2026-06-29.md`
A2/D5 (tag the e^{2φ} weight + xi=kap provenance), G3 (stability notion on the 11-field object), §3-iii consolidation
(retire proliferated solvers to one canonical), cheap bugs (C5 NameError, D4 seed). Then DYNAMIC (time-live native S²).
**LEGACY ARCHIVING / CONSOLIDATION = the §3-iii task, DELIBERATELY NOT done end-of-session 2026-06-29:** the
subsumed-tracker docs (FOUNDATIONAL_ASSUMPTIONS_LEDGER, SOLVER_INTEGRITY_UPGRADES_SPEC, COGNITIVE_CORRAL_TRIGGERS_SETUP,
etc.) are each referenced 10+ places (incl. live `solver_action.py`, `CLAUDE.md`, the corral hook, INDEX.md) — moving
them requires updating every reference + the transitive-closure check the audit scoped. Do it as a DEDICATED careful
task (good workflow candidate), NOT a rushed cleanup. (Untracked scratch .log files are harmless gitignored clutter.)

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
