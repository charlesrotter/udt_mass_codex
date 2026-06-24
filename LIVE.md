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
- **DATA-BLIND:** never load the six lepton wall numbers during a derivation (contract 26fc757). We
  predict RATIOS.
- **ANTI-HANG:** coupled solves are SLOW — bound the grid (Nr<=16/24), ONE clean process, never
  background-poll a solve.

## CURRENT ACTIVITY (2026-06-23): solver-integrity-upgrades arc — COMPLETE
A Charles-requested detour to harden the solver's integrity MACHINERY before resuming the physics
build (spec = `SOLVER_INTEGRITY_UPGRADES_SPEC.md`). SPINE: the harness REFERENCES derivations, it
never RE-ASSERTS their values. All committed + blind-verified:
- **P1** — purity harness `tests/test_solver_integrity.py` (liveness, provenance lint, limit/de-Sitter
  normalization, native-object guard). `pytest tests/` = **16 passed / 5 documented-gap xfails**.
- **P2** — `solver_action.py` (single source-of-truth GR-baseline action + provenance registry) +
  `tests/test_operator_from_action.py` (operator == EL of the action).
- **P3** — 4 auto-loading discipline skills + CLAUDE.md pointer (tripwires stay inline).
- **P4** — `CROSS_MODEL_VERIFY.md` (cross-tier blind verify for load-bearing calls).
- **P5** — this file.
Records: `p1..p5_*_results.md`. **The 5 documented-gap xfails + the P2 baseline = the MIGRATION
acceptance tests** (kap8=1, a=e^φ, native S², core_mode free, ξ/κ tags). Migration must ALSO resolve:
the curvature **Branch G/P fork** (= the φ-angular tension) and the **e^{2φ} matter weight**
(PARTIALLY-TRACED — a flagged CHOSE, NOT derived for field matter; P4).

## BRANCH-P PUSH — DONE/RESOLVED (2026-06-24): solver fixed, no static localization, X-premise caught
The Branch-P push (does native matter localize / select a scale on the untried φ-angular branch?) is
RESOLVED for STATICS. Record = `branchP_solver_floor_xcontinuation_results.md` (blind-verified
PASS-WITH-FIXES; NEGATIVES_REGISTRY #66). Steps A+B (committed 9cd80ef): `branch_operator.py` (derived
G/P-switch operator) + `branchGP_native_s2_coupled_OBSERVE.py` (static coupled residual, 6 LIVE fields
incl. native S² twist `gtw`). What the floor push found:
- **The solver is FIXED via CONTINUATION-IN-X** (`x_continuation.py`): warm-start up a geometric X-ladder
  floors X=−2e5 to Φ=0.18 where every cold-started solver sticks (cold −2e5: Φ=2720). The wall was the
  singularly-stiff φ-equation (`2X·div≈2U'(φ)`, X=−2e5 huge → φ forced ~flat; EL_φ≈X·curvature-error).
- **Solver-integrity catches:** the "P stall at Φ=8.67" was a stochastic unseeded-Jacobi-PC artifact (P
  floors ~like G); the interior-Einstein "obstruction" (cond~1e10) was a SCALING artifact — Ruiz
  equilibration drove Einstein residual→0, moving it to EL_φ (NOT under-resolution, NOT a missing term).
- **PREMISE CAUGHT:** X=−2e5 is a CHOSEN placeholder (`FREE`, Cassini-bounded half-line; branch_operator.py:85)
  that throttles φ ∝1/|X| — so "scale-free" was X-conditioned. But unthrottling φ (continuation) does NOT
  reveal a hidden body: the extra structure is BC BOUNDARY-LAYERS (φ=−0.40 core/+0.44 seal, ~0.01 body),
  NOT an interior core. **Static Branch P = scale-free defect, no interior localization** (scoped: Nr=10
  coarse, static-only, deep-regime X OPEN).
- **→ NEXT (Charles's pick at the next ponder):** statics on BOTH branches now say scale-free defect with
  the solver trustworthy → the φ-angular discreteness hunch's one UNTESTED instrument is the **TIME-LIVE /
  non-stationary native S²** (PHYSICS FRONTIER below). Optional firming: Nr=16/24 grid-refine to resolve
  the boundary layers and close the coarse-grid caveat. The "migration" (wire the derived operator into
  the LIVE p1_residual + flip the 5 P1 xfails) remains a SEPARATE gated step.
- **OPERATIONAL (relearned, 2026-06-24):** run solves MYSELF, bounded, single process; `run_in_background`
  WITHOUT `nohup` (nohup detaches from the harness tracker → false "complete"); agents HANG on solves —
  build-only, never delegate a solve.

## PHYSICS FRONTIER (parked, unchanged): TIME-LIVE NATIVE S²
Live foundational state (2026-06-22 native-matter arc, all blind-verified):
- UDT's **native matter = the S²/π₂ winding (n=x/r) = a scale-free global-monopole DEFECT**, NOT a
  localized particle, in EVERY STATIC config played. The round/static soliton was an IMPORTED S³
  Skyrme baryon (its body held by the imported winding BC).
- The gravity operator is **DERIVED** (vacuum ≠ GR; weight e^{2φ}, a(φ)=e^{φ}) but is **NOT yet wired
  into the live solver** (the live operator runs the a=−1 GR-baseline — that wiring IS the migration).
- **LIVE FRONTIER = the TIME-LIVE / non-stationary native S²** object — the standing φ-angular
  discreteness hunch's home and the one major UNTESTED instrument. Every native solve so far is STATIC.
- **Two MAP-first decisions before building** (make-visible, get Charles's sign-off; detail in HANDOFF
  TOP): (i) finish the remaining STATIC native instruments first vs jump straight to time-live;
  (ii) THE DISCRETENESS GATE (Charles 2026-06-23): OBSERVE for emergence first; if discreteness does
  NOT emerge after sufficient development, IMPORT it under Postulate A (the accepted ħ/spin/statistics
  quantum postulate; UDT = quantized dilation-geometry). Emergence is the goal, Postulate A the fallback.
- **OPEN (found 2026-06-23, P4-style check): the curvature Branch G/P fork is already BEHIND us SILENTLY.**
  The native-S² static solves ran the DERIVED operator on **Branch G** (gauges the angular obstruction
  AWAY; scale-free by construction) — never named/flagged. **Branch P** (keeps the φ-angular curvature
  as a physical potential + the scale-breaker e^{2φ}−1) was NEVER tried on the native object. So the
  "scale-free defect" headline is BRANCH-G-CONDITIONED — possibly an artifact of the silent choice, and
  Branch P is where the φ-angular hunch lives. Make the branch an EXPLICIT switch; try Branch P
  (static, then time-live) before banking "featureless defect." (p1_residual GR-baseline solver is a
  SEPARATE line from this derived-Branch-G native-S² solver.)

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
