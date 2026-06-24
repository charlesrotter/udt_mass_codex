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

## NEXT ACTION — BUILD THE PROPER (JFNK) COUPLED SOLVER (Charles 2026-06-23)
The BRANCH-P PUSH is underway (testing whether native matter localizes / selects a scale on Branch P,
the untried branch that keeps the φ-angular potential — see PHYSICS FRONTIER below). Status:
- **Step A DONE** (committed 9cd80ef): `branch_operator.py` — the DERIVED gravity operator with an
  EXPLICIT G/P switch (blind-verified). Closed the silent-branch + uncommitted-operator gaps.
- **Step B DONE**: `branchGP_native_s2_coupled_OBSERVE.py` — the static coupled residual, 6 LIVE fields
  incl. the native S² radial twist `gtw` (the unfrozen rigid-slice DOF); G-control reproduces the defect.
- **Step C THROUGHPUT-LIMITED / INCONCLUSIVE** (record = `branch_p_coupled_observe_partial_results.md`):
  bounded GPU solves floored G (Phi~37, 1/r² defect) but NOT P (Phi~1.5e4 — P is STIFFER; the U potential
  pulls φ ~5× deeper = the scale-breaker ACTS, but rho/localization are seed-dominated, inconclusive).
  The wall is SOLVER THROUGHPUT (dense jacrev ~113s/iter + P stiffness = the known #60 conditioning wall).
- **JFNK SOLVER BUILT** (`jfnk_branch_solver.py`, record = `jfnk_solver_results.md`): matrix-free
  jvp/vjp + LSMR + Jacobi-PC + damping. Fixed a 1-D/4-D Krylov shape bug (flat-space fix; fidelity
  INTACT — confirmed: JFNK reaches a LOWER residual than dense-LM = same branch, more converged).
  **~15× faster** on Branch G (Phi 2.3e5→3.9 in 2 iters/120s vs dense-LM 37/340s). CAVEAT: **STALLS
  near Phi≈4 with pc='none'** (not tightly floored); Branch P not yet reached.
- **→ NOW: break the stall + FLOOR.** The Jacobi PC is ALREADY wired (`jfnk_solve(..., pc='jacobi')`,
  jfnk_branch_solver.py ~L210); the stall was a run with the DEFAULT `pc='none'`. So: SWITCH to
  `pc='jacobi'` + tune the inner-tol/line-search knobs (`eta0/eta_min/tol/lsmr_maxit`) so JFNK floors
  tightly; BUILD the block/spectral PC only if Jacobi isn't enough. THEN floor Branch P (the OBSERVE:
  localized body / selected scale vs the 1/r² defect?) → the SEAL-INDEPENDENCE gate (native scale vs
  imported seal). Run all solves MYSELF via background-notify, WRITE runs to a file not a grep-pipe
  (buffering loses output on kill); agents HANG on solves — build-only, NEVER delegate a solve.
The "migration" (wiring the derived operator into the LIVE p1_residual + flipping the 5 P1 xfails) is a
SEPARATE gated step, not the immediate next.

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
