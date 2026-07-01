# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order:** LIVE.md CURRENT STATE → CLAUDE.md "How we work" + the discipline skills → (for detail)
HANDOFF.md TOP + EXTERNAL_AUDIT_2026-06-30.md → INDEX.md (repo map).

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/`), **completeness-map**.
- **DRIVER TRIGGERS (CLAUDE.md, always-loaded) + harness HOOKS** (`.claude/hooks/corral_trigger.py`,
  fires on Task/Bash/git-commit) now make the corral fire WITHOUT being challenged — pause+honesty, never
  merit; the allowed-lane clause (category-A technique always GREEN) is non-droppable. Memory freshness: the
  TOP entry in MEMORY.md is the CURRENT frontier; older FRONTIER-labeled entries are tagged "SUPERSEDED as
  frontier" (durable lesson only — do NOT treat their "NEXT/read-FIRST" as live); the rest are durable
  principle-memories (binding, not dated frontiers). Read the TOP entry + this LIVE file for the live plan. Local-LLM cross-check
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

## ============ FRONTIER (2026-07-01 — NATIVE FIELD EQUATIONS) — READ THIS FIRST ============
**CURRENT STATE (2026-07-01 late — supersedes the basin/weight arc below):** The chain (basins → e^{2φ}-weight audit →
frame audit) drove all the way to the FOUNDATION and Charles DERIVED the native UDT field-equation skeleton (in-session);
the driver CAS-verified every step; blind-adversarial verifier PENDING. Full record: **`native_field_equations_constrained_two_player_results.md`**.
Key results (all CAS-verified):
- **EH is EMPTY on the canonical UDT family:** `√-g·R` is a pure boundary term (`r²R=d/dr[…]`) → bare Einstein-Hilbert gives
  NO bulk equation for φ. "Vacuum=GR" was that emptiness showing through (the Principle-7 scar), never a result.
- **Native bulk action = the R1-shift-invariant kinetic**, whose density `√-g·e^{2φ}g^{rr}φ'² = c r²sinθ·φ'²` is φ-FREE
  (only φ') → probe=self-consistent → `(r²φ')'=0` → `φ=φ_∞-q/r` → `g_tt=-e^{-2φ_∞+2q/r}`, an **exponential lapse, NOT
  Schwarzschild.** The naive "one-player ⇒ GR-collapse" is FALSE.
- **Native matter is φ-BLIND** (channel-corrected → couples to the UNDILATED metric; `δS_m/δφ=0`). So the live `e^{2φ}·L_m`
  / `e^{2φ}T` was NON-native — **that is exactly what manufactured the "dilaton-runaway basin A."** The whole basin saga is
  now EXPLAINED + retired. Matter sources φ only INDIRECTLY, via geometry: **n → h_AB → 𝒦 → φ** (Branch P), not n→e^{2φ}T→φ.
- **Native frame = CONSTRAINED-TWO-PLAYER** (φ = longitudinal dilation INSIDE g; h_AB = independent transverse 2-geometry) —
  NOT the live scalar-tensor solver (φ outside g). **⇒ the live solver is the WRONG frame** (do NOT keep tuning it).
- **G/P are two REGIMES, not a global choice (Charles):** **Branch G** = strict depth-gauge → `(r²φ')'=0`, scale-free =
  CONTINUUM EXTERIOR. **Branch P** = angular scale physical (BREAKS R1) → `Z(r²φ')'=4e^{-2φ}` = the native φ-angular coupling
  = FINITE-CELL/microphysics. **Discriminator (CAS):** P has NO asymptotically-constant vacuum (`0=4e^{-2φ_∞}≠0`) ⇒ P is
  intrinsically finite-domain. Map: continuum-exterior→G, finite-cell→P, boundary between→a MATCHING problem.

**G↔P SWITCH CRITERION — DERIVED (2026-07-01; `gp_switch_criterion_results.md`; CAS + blind-verifier).** The switch is a
PINNED DIMENSIONLESS radial-to-angular invariant (Charles's sharpening — "fixed angular scale" alone is too broad):
- Only the transverse extrinsic term `𝒦=K_AB K^AB−K²` breaks the shift (kinetic/`R^{(2)}`/matter all invariant).
- Invariant moved = the cell ASPECT RATIO `χ = (∫e^φ dr)/√(A/4π)` → `χ→e^λχ` (proper-length ratio; coord-invariant).
- **N+S:** shift breaks → **Branch P** iff (N1) √A pinned AND (N2) radial interval [r_c,r_i] pinned AND (N3) `𝒦≠0`. Else G.
- Adversarial: fixed-angular-scale ALONE insufficient (need N2); topology alone insufficient (degree pins no length);
  **P is a genuine BULK equation** (∂𝒦/∂φ=−2𝒦≠0; `∫√h𝒦` not a total derivative) — SCOPED to 𝒦-as-standalone-action-piece.
- Regime map: G = bulk where χ free (continuum exterior, scale-free); P = cell INTERIOR where χ pinned & 𝒦≠0 (φ-angular
  coupling); the seal/cell-wall = where χ gets pinned = the matching layer. Matches finite-cell canon; ADDED N2/N3 to the hunch.

**IMMEDIATE NEXT ACTION (2026-07-01) = DERIVE WHAT THE NATIVE GEOMETRIC ACTION IS** — is `𝒦` a standalone invariant, or part
of a total-derivative curvature combination (like the EH boundary result)? This is the LAST item gating full bulk-P certainty
(Task-3 scope) AND bears on "is the minimal kinetic the whole bulk action." MAP first, no solver. THEN (later) the G↔P MATCHING
problem at the seal; a constrained-two-player SOLVER is gated behind those.
Premise flags (standing): constrained-metric FORM (φ purely longitudinal) CHOSE-not-forced; matter-φ-blind + shift rule ride
R1+P5 (CHOSE); Branch P breaks R1 in the angular sector.
**DO NOT (per Charles):** re-pose one-player in code, keep two-player as canonical, build any solver, or change the matter
weight — until the action question is settled. Op: any CAS/solve UNBUFFERED, single process, no grep pipe, no nohup.

### ↓↓↓ SUPERSEDED 2026-07-01 (basin/e^{2φ}-weight arc — HOW WE GOT HERE; the field-eq result above explains it) ↓↓↓
**Basin audit (classify-only) + glm stronger step + the e^{2φ}-weight audit** — the chain that led to the frame result above.
- **STALE-BRANCH-A CATCH:** `xexplore_field_X1.pt` was floored on the PRE-seal-reconciliation residual (commit 80d8e37) —
  reads **Phi=3.4e5 on CURRENT code**, not 2e-3. Renamed A_pre_reconciliation. (Projection-fairness pre-check caught it.)
- **STRONGER STEP:** `newton_solve_p1(step='glm')` = LM-in-galerkin + Nielsen + singular-metric guard. FLOORED Branch B to
  8.2e-12 where all prior crawled. pytest 32/1xfail. (`basin_audit.py`.) **Still valid + useful** for the eventual solver.
- **CLASSIFY (now EXPLAINED as an e^{2φ}-artifact):** B floors clean (dead dilaton φ≈0.02); A_pre_reconciliation ran its
  dilaton to φ≈3.3 (e^{2φ}≈735) and stalled — because the NON-native e^{2φ}T drove it. The field-eq derivation dissolves this.
- **e^{2φ}-weight audit (`a05295762e39e6260`):** the matter weight is a CHOSE posit (self-tagged / MIGRATION-DEFERRED) —
  now SUPERSEDED by the native result: channel-corrected matter is φ-blind (weight ≡ undilated-metric coupling).

### ↓↓↓ SUPERSEDED 2026-07-01 (the basin audit below RAN — see CURRENT STATE above; kept for the hygiene checklist) ↓↓↓
**PRE-TEST HYGIENE (cheap; do BEFORE the basin audit — external-audit items that could CONTAMINATE it):** (a) the
basin-audit DRIVER hard-codes NO hidden provenance — pass X/xi/kap/kap8/branch/p/wbc/determined/step/grid explicitly +
print the manifest (note: `residual_vector_p1`/`newton_solve_p1` STILL default X=-1/xi=1/kap=1/branch=G — a silent-
default risk at the higher entrypoint, unlike branch_operator which now requires explicit; the driver must not rely on
them) [DONE: basin_audit.py passes all provenance explicit + prints manifest]; (b) keep the framing neutral (this
block). **DEFER to before any PHYSICS claim (NOT blocking the basin audit):**
action-registry staleness (`solver_action.py` still GR-baseline / MIGRATION-DEFERRED while the live path uses the
derived e^{2φ} operator); premise-ledger upgrade (token-presence → call-path); add `determined=True` tests (liveness
tests still exercise determined=False/kap8=0.05); split GR-baseline regression from live-UDT-action consistency
(`test_operator_from_action.py` locks φ=0 = GR-baseline); make conditional solver modes (`galerkin`,`svd_ls`)
first-class in the gate's import graph; hooks are reminders not guards. (Full external audit = `EXTERNAL_AUDIT_2026-06-30.md`.)
**Key files:** `galerkin_basis.py`, `newton_solve_p1(step='galerkin'|'lm')`, `d1_gauge_check.py`,
`x_solution_space_explore.py`, `PROVENANCE_AUDIT_2026-06-30.md`, `D1_FIX_DESIGN.md`. Op: solves UNBUFFERED, single process.

### RESUME RUNBOOK (the concrete first moves — verified 2026-06-30; everything below is ON DISK + committed)
0. **Confirm guardrails** (catch-proof §4): see the `✓ CORRAL GUARDRAILS ACTIVE` banner + recite the 6 DRIVER TRIGGERS
   from context. `python3 -m pytest tests/` → expect **32 passed / 1 xfailed**.
1. **The two start-fields EXIST + committed** (don't regenerate — hours each): **Branch A** = `xexplore_field_X1.pt`
   (X=−1, Φ=2.09e-3, branch G, kap8=1, determined — LM/crawl, alive dilaton); **Branch B** = `galerkin_floored_X1.pt`
   (X=−1, Φ=1.57e-5, same provenance — cold-galerkin, dead dilaton/extreme warp). Diagnostics: reuse `d1_gauge_check.py`
   (observables Q/φ_max/warp/ρ_max/lapse + the physical/gauge residual split).
2. **PRE-REGISTER FIRST, with Charles (do NOT skip — pre-registration discipline):** define + COMMIT the geometric
   ACCEPTANCE/REJECTION criterion BEFORE any solve (e.g. what warp/compactness/dilaton-survival values would reject a
   basin), so classification can't be retrofitted. The criterion does NOT exist yet — it's a PONDER-with-Charles item.
3. **Pre-test hygiene:** write the basin-audit driver to pass ALL provenance EXPLICITLY (X, xi, kap, kap8, branch, p,
   wbc, determined, step, grid — `residual_vector_p1`/`newton_solve_p1` still SILENTLY default X=−1/xi=1/kap=1/branch=G;
   do not rely on them) and PRINT the manifest per run (run_id, seed_type, start_field, all provenance, Phi,
   physical/gauge residual split, Q, φ_max, warp_max, ρ_max, lapse_min, accepted_steps).
4. **Run the BASIN AUDIT (classify, don't select):** continue BOTH start-fields under IDENTICAL fair globalization
   (e.g. step='galerkin' with damped/line-searched physical-band reduction — same settings both), log the manifest +
   diagnostics, and CLASSIFY against the pre-registered criterion. Bounded grid, single process, UNBUFFERED, run MYSELF.
   (Cleanup the ~14 one-off `d1_*.py`/`kte_*`/`x_*` diagnostic scripts = the §3-iii consolidation, owed but not blocking.)

---
### ↓↓↓ HISTORICAL ARC (2026-06-29 → 30; superseded by the CURRENT STATE above — mine for detail, not the frontier) ↓↓↓
**One-line state (2026-06-29):** D1 determinacy FIXED+blind-verified (null-dim 0). The **core-BC FORM artifact is now FIXED+
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
**SOFT-MODE CHARACTERIZED (2026-06-29, Charles "derive don't assert"):** the 2 near-null directions (smin~1e-4) are
DERIVED SYMMETRIES — mode#1 = matter SO(3) ROTATION (79% overlap w/ ω_z×n), mode#2 = metric DIFFEOMORPHISM gauge.
No imposition needed (benign, LM-damping-handled); smin is NOT a flooring obstruction. (`d1_softmode_characterize.py`.)

**=== MAJOR PIVOT (2026-06-30): the conditioning wall is the X=-2e5 KLUGE, not numerics. ===** smax was NOT Chebyshev
endpoints (KTE falsified it: smax barely moved) — it is **smax ∝ |X|, carried entirely by the φ-EL row** (`d1_smax_source.py`).
And X=-2e5 is a **Cassini-FORCED FIT mis-tagged FREE** (magnitude = the PPN bound rounded up; nothing in the metric
selects it — Charles caught it). So we PIVOTED (Charles): stop forcing the floor at the imposed X; EXPLORE the
determined solution across FREE X. **TWO PROVENANCE AUDITS (direct + blind-adversarial, `PROVENANCE_AUDIT_2026-06-30.md`):
X is the LONE observation-fit kluge on the live path** (kap8=1 verified DERIVED; xi=kap=1 units; 2e-2 defaults dead;
no swarm). Two soft DERIVED-headlines flagged: **the e^{2φ} matter weight** (CHOSE, LIVE, O(5) at hadronic depth =
Principle-2 territory — Charles's eye owed) and **φ(seal)=0 parity** (two docs contradict). **X-SWEEP (PROVISIONAL,
unfloored): the kap8=1 object is X-STABLE across X=-1..-1000** (winding EXACTLY 1, dilaton alive φ≈0.8, no horizon,
flat warps) → NOT a Cassini artifact; recent results survive un-pinning X. **NON-FLOORING RESOLVED: it's solver GLOBALIZATION, not a posing flaw.**
The determined solve crawls (~0.3%/iter) even at well-conditioned X=-1, but `d1_lsfloor_test.py` proves **F is 99.9%
REDUCIBLE** (irreducible LS floor from the 4608-vs-4224 over-determination = only 2.67e-6) → a near-exact solution
EXISTS; the posing is CONSISTENT. The reducible residual lives in the SOFT (benign gauge/rotation) directions that
the uniform LM lam*I damping suppresses → crawl. **Whole conditioning saga resolves: determinacy FIXED, core-BC
FIXED, smax = the X=-2e5 KLUGE (pivoted to explore X), soft modes = benign symmetries, posing CONSISTENT,
non-flooring = solver globalization — none indicted the metric.** NEXT (building): **a better Newton step — SVD-
pseudoinverse + line-search** (regularize only genuinely-null dirs; take reducible dirs; scale by nonlinear-accepted
step) replacing uniform-damped LM → then the determined solve should FLOOR → trustworthy re-grade across X.
Also done 2026-06-30: removed the silent coupling-default TRAP in branch_operator (X/xi/kap now require explicit pass).
Equilibration/KTE/integration-preconditioner line = SUPERSEDED (the conditioning was the X kluge, now being explored).

**=== GALERKIN BASIS BUILT — CONDITIONING FIXED; cold run reaches a 2nd basin (2026-06-30 EOD) ===**
*(⚠️ The words "spurious / RIGHT branch / physical compact object" in THIS historical block are PRE-REFRAME MERIT
language — REPLACED by the neutral Branch A/B basin-audit framing in the CURRENT STATE block at the top of this file.
Read this block for the technical detail (the seal-BC reconciliation, the numbers), NOT for the framing of what to do.)*
Built `galerkin_basis.py` (BC-recombined radial basis) + `newton_solve_p1(step='galerkin')` (change-of-variables
du=B@da; residual physics unchanged; lm default byte-stable, pytest 32/1xfail). Conditioning FIXED: cond(J@B) drops
38x, stiff near-edge modes lifted. **Seal-BC reconciliation (commit 80d8e37):** the basis enforces the seal BC in
WARP form (c'(ri)=-1/ri etc.); the residual imposed the SPECTRAL d_r(g_thth) form — inconsistent at Nr=8 (projection
catapulted Phi 2e-3→7e7). FIXED by discretizing the residual seal rows (b,c,d,e_tp) in the matching warp-Robin form
(== d_r(g_*)=0 in continuum; Category-A; 1/ri,2/ri are DERIVED geometry, registered in test_solver_integrity).
**RESULT — honest:** the determined solve now DESCENDS 6 orders (round seed Phi 23.8→1.5e-5, where LM/equil/KTE/SVD all
crawled at 2e-3) — **conditioning machinery WORKS.** BUT (`d1_gauge_check.py`): the 1.5e-5 residual is **100% PHYSICAL
band (NOT gauge) → still UNDER-CONVERGED**, AND the observables moved SUSPICIOUSLY vs the old crawl-floor: **dilaton
φ_max 0.90→0.021 (nearly DEAD), max warp 2.57→10.1 (BLEW UP), ρ_max 0.0097→3e-8 (collapsed), lapse 0.55→0.31** (only
winding Q≈1 survived). => the **cold galerkin run wandered into a SPURIOUS extreme-warp/dead-dilaton branch** (big steps
from the far round seed overshoot), NOT the physical compact object. **The "floor" is the residual onto a suspicious
branch — the re-grade is NOT valid.** **NEXT (when resumed): gentler globalization / PHYSICAL warm-start — LM-to-close
then galerkin-POLISH near the physical solution — so it floors the RIGHT branch, not a cold run that overshoots.**
Conditioning saga otherwise fully resolved (determinacy, core-BC, X-kluge, soft modes, posing-consistency, edge-cond).

**GIT: push went down mid-session (auth) then RESTORED 2026-06-29 — fully synced (origin/main == HEAD). No
unpushed commits.** (If push fails again it's auth: `gh auth login`.)

### NEXT-SESSION PRIORITIES (SUPERSEDED 2026-06-30 — see "IMMEDIATE NEXT ACTION" at the top of the frontier)
*The P1–P4 below were the 2026-06-29 plan; P1 (floor the determined posing) is now the galerkin/warm-start work in
the CURRENT STATE block above. P2 (cross-model verify) + P3 (e^{2φ} weight, φ-seal, §3-iii consolidation) + P4
(DYNAMIC) still stand, after the warm-start floor + re-grade. Kept verbatim below for the detail.*
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
