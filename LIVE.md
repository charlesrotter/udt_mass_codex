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

## NEXT ACTION
Integrity arc done → **resume the physics frontier** (below): MAP the two decisions with Charles and
get sign-off BEFORE any build (do NOT auto-launch a solve). The "migration" (wiring the DERIVED
operator + native S² matter into the live solver, which flips the 5 P1 xfails green) is a SEPARATE
gated step, not the immediate next — reach for it only when a result points there.

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
  (ii) DEFINE THE DISCRETENESS GATE (what counts as "discreteness found" vs "still continuum/defect").

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
