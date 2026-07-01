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

## ============ FRONTIER (2026-07-01 — RETURN TO SOLVER, native frame DERIVED) — READ THIS FIRST ============
**⇒ WHERE WE ARE NOW (read this line first): the whole native frame is DERIVED + CAS + blind-verified; we have RETURNED TO
BUILDING THE SOLVER on it. Pre-registration FROZEN (`discreteness_preregistration.md`). The next work is the 2-D free-field
`f(r,θ)` finite-mirror eigenproblem — but do NOT auto-start coding: FIRST run the startup self-check, then MAP the slice +
premise ledger, then PRESENT the plan to Charles and get his go (see the "IMMEDIATE NEXT ACTION" block further down for the
exact gate). The field-equation results below are the DERIVED FOUNDATION (now complete + verified), not the pending frontier.**

**CURRENT STATE — Phase 1 (the derived foundation, 2026-07-01, all CAS + BLIND-verified):** The chain (basins → e^{2φ}-weight
audit → frame audit) drove all the way to the FOUNDATION and Charles DERIVED the native UDT field equations (in-session).
Full record: **`native_field_equations_constrained_two_player_results.md`** (+ the 4 companion docs). Key results:
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
  **P is a genuine BULK equation** — now UNCONDITIONAL (see native-action result below).
- Regime map: G = bulk where χ free (continuum exterior, scale-free); P = cell INTERIOR where χ pinned & 𝒦≠0 (φ-angular
  coupling); the seal/cell-wall = where χ gets pinned = the matching layer. Matches finite-cell canon; ADDED N2/N3 to the hunch.

**NATIVE GEOMETRIC ACTION — DERIVED (given form) + CAS + blind-verified (2026-07-01; `native_geometric_action_results.md`).**
`S = ∫c√h[(Z/2)φ'² + R^{(2)} + W_χ(φ)𝒦]`, W_χ=e^{2φ}(G)/1(P) — the action-level G/P switch. It CLOSES the switch-criterion
gate: **𝒦 is genuinely BULK** in the √h-measure action (√h·𝒦=−2e^{-2φ}sinθ, no local antiderivative), while 4D-EH `√-g R` is a
total derivative (empty) — so P is UNCONDITIONALLY a bulk cell-interior equation; EH is the empty red herring (the P7 scar).
Round G-cancellation `R^{(2)}+e^{2φ}𝒦=0` (any φ); native action ≠ 3D-EH (`R^{(3)}=R^{(2)}+𝒦+4e^{-2φ}φ'/r`) ≠ 4D-EH.
**OFF-ROUND UNIQUENESS — DERIVED (2026-07-01; CAS + blind-verified).** The angular extrinsic term is UNIQUE: off-round
angular-flatness (`R^{(2)}=K²−K_ABK^AB` for flat ambient, verified on a paraboloid) forces `b=a,d=−a` → **`𝒦=K_ABK^AB−K²`;
an independent `K²` is EXCLUDED** (round-h couldn't test it — degenerate; off-round resolved it).
**REMAINING RESIDUAL = the Z_φ FORK** (no longer the K² ambiguity): the longitudinal kinetic normalization is NOT fixed by
angular flatness or R1 shift symmetry. **Route A** (sector-orthogonal, banked action): **Z_φ FREE**, no mixing. **Route B**
(kinetic = R1-weighted longitudinal-block curvature `R_L`): **Z_φ=8** but FORCES a mixed term `2e^φKφ'` (D=2). Real fork; the
math alone doesn't pick it — a candidate for CONSILIENCE selection (fitted-constant-free spectrum).

**G↔P MATCHING AT THE SEAL — DERIVED (2026-07-01; CAS + blind-verified; `seal_matching_junction_results.md`).** Two junction
conditions from `δ(S_P+S_seal+S_G)=0`:
- **JC1 (dilation-flux):** `[√h Z_φ φ']=0` continuous; round → `q=(r²φ')|_seal` — **the exterior public charge q IS the
  interior dilation flux through the seal** (native Q=Misner-Sharp mass=2p_F). **External charge is SEAL FLUX, not bulk matter:**
  `n → h_AB → 𝒦 → φ → Π_φ|_seal → q`.
- **JC2 (transverse momentum):** `π^{AB}=c√h W_χ e^{-φ}(K^{AB}−K h^{AB})` continuous → `(K^{AB}−Kh^{AB})_P = e^{2φ_s}(K^{AB}−Kh^{AB})_G`
  (source-free), or `[π^{AB}]=S^{AB}_seal` with a seal stress. The e^{2φ} weight-jump = the G/P interface signature.
- **Seal parity = TWO CLASSES (NOT an adjudication — Charles corrected a driver error):** Class A = smooth source-free
  mirror fold → even radial parity → Neumann φ'_n=0 → **q=0 closed cell**; Class B = pinned/charged seal → φ'_n≠0 → **q≠0,
  needs a seal source/constraint**. RETRACTED: "time-reversal ⇒ radial Neumann" (doesn't follow) and "Dirichlet ⇒ charged"
  (q is the normal-derivative flux, not the value — Dirichlet permits but doesn't force q≠0). The two-doc φ(seal) contradiction
  = these two seal CLASSES, not rival answers. Which cell (universe/matter) is which = OPEN physics/canon (Charles holds).

**PHASE SHIFT (Charles, 2026-07-01): DERIVATION DETOUR DONE → RETURN TO THE SOLVER.** More derivation now risks becoming a
substitute for letting the geometry speak. The native frame is derived + trustworthy (one open constant Z_φ). BUILD the
constrained-two-player solver ON THE DERIVED FRAME (interior P + exterior G + seal JC1/JC2) and let discreteness EMERGE.
**PRE-REGISTRATION COMMITTED (`discreteness_preregistration.md`) — the falsification contract, frozen before solving.** Binding
rule: **"Do not solve for the electron. Solve for the solution space."** Modest FIRST GOAL: does the derived system have ANY
stable isolated finite-cell solutions AT ALL? (prove the geometry produces CELLS) → THEN do they form a DISCRETE FAMILY? →
THEN (blind, after) compare to particles. Discreteness counts only if isolated/gapped, seed-independent, stability-without-
imposed-targets, grid/method-independent, Z_φ-fixed (no per-solution retuning), quantized seal-flux q, branch-consistent,
perturbation-surviving, blind-classified (9 criteria in the pre-reg doc).
**SOLVER PROGRESS (2026-07-01):** round cell reduces to a CHEAP 1-D system, TWO fields φ(r),ρ(r) (ρ dynamical; areal ρ=r is
the neutral sub-case, NOT free). Mirror-fold seal BC = φ'=ρ'=0 (drum → eigenvalue). VACUUM mirror cell is TRIVIAL (constant) →
needs MATTER. Round S² winding matter reduced + CAS-verified (`round_matter_reduction_results.md`, `cell_solver_round.py`):
`ρ''_m=(e^{2φ}/4)(ξρI_r − κN²I_4θ/ρ³)`. **RIGID hedgehog (f=θ, I_r=0) → the cell COLLAPSES (real, verified, not a sign bug)**;
the stabilizing +ξρI_r needs RADIAL matter structure I_r>0; balance ρ⁴~κN²I_4θ/(ξI_r).

**IMMEDIATE NEXT ACTION — do NOT auto-start coding/computing. FIRST, in order:** (a) run the startup self-check (the
`✓ CORRAL GUARDRAILS ACTIVE` banner → recite the 6 DRIVER TRIGGERS from context → `python3 -m pytest tests/` = 32 passed/1
xfailed); (b) do the **MAP (no compute)** — state the round-static `f(r,θ)` slice WHOLE + a PREMISE LEDGER tagging every free
choice (Z_φ, the core rule, the constrained-metric FORM, ξ/κ, N — all CHOSE/held-fixed) + name what this slice does NOT test
(off-round, non-static — see HANDOFF "STANDING RISKS"); (c) **PRESENT the build plan to Charles in lay terms and get his go**
(Session-workflow rule: "present the process plan before launching long pushes"). This is OBSERVE mode (sanctioned, not a gated
DERIVE) — but it still goes through MAP + plan-present first; do not skip to code. **THEN build:**
**the minimally-free axisymmetric field f(r,θ)** (n=(sin f cosNψ,sin f sinNψ,cos f); rigid=f=θ) — a 2-D finite-mirror eigenproblem
coupling f(r,θ) to φ(r),ρ(r) (matter EOM in `round_matter_reduction_results.md`). Don't insert I_r by hand; look for ISOLATED
cell lengths (φ,ρ,f close), unlabeled, fixed Z_φ/ξ/κ/N. Still collapses → scoped negative; isolated modes → first discreteness signal.
The Z_φ fork stays a held-fixed parameter (consilience later); it does not gate the "are there cells at all?" question.
Premise flags (standing): constrained-metric FORM (φ purely longitudinal) CHOSE-not-forced; angular term UNIQUE (K² excluded);
Z_φ/mixing = OPEN FORK; seal-class (universe/matter ↔ A/B) OPEN; matter-φ-blind + shift rule ride R1+P5 (CHOSE).
**STANDING RISKS (full analysis in HANDOFF.md "STANDING RISKS"): (1) the constrained-metric FORM may WALL OFF discreteness
(off-round/non-static/φ-angular metric mixing excluded) → a "round static → continuum" result is a SLICE result, NEVER the
theory's verdict; (2) Z_φ could become the new X-kluge fitting knob AND its fork is STRUCTURAL (Route B forces an extra
φ-angular `e^φKφ'` term) — Z_φ doesn't gate "are there cells?" but DOES gate the quantitative ratios later. Both TAGGED (not
hidden); the danger is only forgetting they're open.**
**DO NOT (per Charles):** re-pose one-player in code, keep two-player as canonical, build any solver, or change the matter
weight — until the action question is settled. Op: any CAS/solve UNBUFFERED, single process, no grep pipe, no nohup.

### ↓↓↓ HISTORICAL ARC — ARCHIVED 2026-07-01
The 2026-06-29→30 basin / D1-determinacy / galerkin / X-kluge detail (RESUME RUNBOOK, NEXT-SESSION PRIORITIES,
This-session's-arc, D1 IMPLEMENTATION SPEC) moved to `archive/LIVE_basin_D1_galerkin_arc_2026-06-30.md` — it was the
trail that led to Phase 1's discovery that the live frame was un-derived. Mine for detail; NOT the frontier.

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
