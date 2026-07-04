# ARCHIVED LIVE layered detail — the 2026-07-04 Opus route-fork + E2c/d/e optimizer arc

> Split out of `LIVE.md` on 2026-07-04 to keep the CURRENT STATE block clean (the top block leads
> with Charles's pending option-3 decision). This is the verbatim layered "LIVE NEXT" detail as it
> stood at the bank of E2e. Canonical records = the results docs (`r1_*`, `r2_*`, `regrade_S2_*`,
> `microphysics_E2c/d/e_*`). If this disagrees with LIVE.md's CURRENT STATE block, LIVE.md wins.

**LIVE NEXT (as of the E2e bank, 2026-07-04):**

**(1) FORK 3 UPDATE — R1 DONE, BANKED blind-verified (40294ef): verdict = FREE-ON-A-SHEET**
(the fork = the (Z_φ,μ) sheet; Route A = μ=0 edge, Route B = the point (8,2) on 2 CHOSEs; the ONE
observable = s = 2μ/Z, the vacuum-deformation exponent — observability EXACT; the mixing term = a
kinetic-level φ-angular coupling). **R2 (reframed): BOUND s against the macro constraints —
pre-register the s-dependence of each observable FIRST (data-blind), then confront** (charter §3).

**R2 DONE + BANKED, blind-verified** (`r2_prereg_s_dependence.md`, commit 3515f62; reframe BLESSED by
Charles; verifier a82dd36ef191768dd 26/26, corrected 2 over-reaches). BANKED: s=2μ/Z = the ONE
gauge-invariant vacuum observable; J(s) light-deflection = the frame-ROBUST confrontation lever
(J(0)=π, J(½)=4, O(s) impact-parameter-independent; a bound s_max<½ kills Route B but not small-μ =
NOT binary); ∝s structural levers (realizability caveats). The rotation-law v²=s = PREMISE-CONDITIONAL
(lives under g, killed only by the observationally-DEAD ĝ branch — NOT an artifact, NOT banked).
⇒ THE FRAME FORK (which metric matter couples to; is matter-in-motion a worldline). ĝ-as-physical REFUTED
(reductio: zero redshift vs GPS + zero orbits).

**S²-DEFECT RE-GRADE — RESOLVED-AS-FAR-AS-DERIVATION-ALLOWS (2026-07-04, after Charles caught a
stale-rung lean): the S²-defect discovery was RE-GRADED under the native foundation**
(`regrade_S2_defect_2026-07-04.md`, commit e3ec6b0, verifier aa3af5a01f70aa096; registry updated). Outcome: the
point-particle-WORLDLINE branch is UNDERCUT clean-current (S13c: no R1-invariant worldline law) ⇒ leans
matter-in-MOTION toward a field/defect-SOLUTION description — but NO positive verdict, and it does NOT
select g vs ĝ. The decisive positive content (does the native S² winding form a stable object; how it MOVES
as a field) is STILL-OPEN, and lives INSIDE THE EMERGENCE PROGRAM (E2c existence → D4 native moving-field
solve) — NOT a macro frame-pick. So the frame fork is NOT a standalone Charles-ruling; it folds back into
the emergence program. What stands frame-independent: s=2μ/Z + J(s) light-deflection as the measurable
lever.

**E2c OPTIMIZER HARDENING DONE + BANKED, blind-verified** (2026-07-04, commit c68d65d;
`microphysics_E2c_optimizer_hardening_results.md`; builder a366c26d, verifier ab6305ce222eee961 —
NO PHYSICS MOVED: git diff insertions-only, residual byte-identical, root-preservation re-derived).
The 0/256-undecided cause was a near-EXACT TRANSLATION GAUGE of the boundary pair (ambient r-autonomy;
cos=−1.000000) — FIXED via Ruiz two-sided equilibration (cond 5.7e11→1.9e7) + Powell dogleg trust region;
CERTIFIED converging from boundary offsets ≥30 (3× spec) to ~5e-9 on 2 MMS (incl. a bulged one). Residual
FIELD-AXIS wall = intrinsic local-NLLS minima (multiple globalizations all stall short) ⇒ the re-sweep
needs MULTI-START + CONTINUATION, and non-convergence reads "not found from these seeds," NEVER
"does not exist" (charter trap #1). Hardened driver = `lm_hardened` in `cell_solver_composite.py`.

**E2d DONE + BANKED, blind-verified** (2026-07-04, commit 92af4e2; `microphysics_E2d_resweep_A1Z8_results.md`;
builder adfcf1eea, verifier a5e1960b6f90b4686 — physics untouched to EXACT zero). The continuation+multistart
driver (`e2d_continuation_driver.py`, wraps byte-identical lm_hardened) certifies boundary offsets ≥30 +
the deviation-field (u) axis to ~0.3 (NEW), but the COMBINED-CELL field axis (the flat core φ_c/ρ_c of a real
seed) is UNCERTIFIED along Newton/fp homotopy = COMPONENT SEPARATION — verifier-SCOPED to those homotopy
families, NOT absolute: GRID HOMOTOPY bridges some of the same distances ⇒ a CONNECTING PATH EXISTS. The real
sweep was GATED OUT (honest STOP — don't sweep an uncertified tool; defensible but the verifier judged it
mildly over-cautious: a scoped sweep reading nulls as "not found from these seeds" would also be legitimate).

**E2e DONE + BANKED, blind-verified** (2026-07-04, commit ba31693; `microphysics_E2e_physinformed_seed_results.md`;
verifier a0205204484a1d48c — physics byte-identical to HEAD). The PHYSICS-INFORMED SEED (derived even-fold core
+ E_ang(core)=2, canon C-2026-07-03-3) CONTROLS the boundary runaway (phys r_p bounded O(100–2000) vs flat's
runaway O(1e7)) but does NOT crack the combined-cell wall. Certification FAILED + scoped A1Z8 sweep = NULL
(candidates:[], 8/8 coverage, both seed families). KEY: the wall is EXTREME DEPTH-STIFFNESS — residual 16.9 at
field-distance 0.1, homotopy folds at s~9e-4 — NOT seed distance; starting closer doesn't help. ⇒ EXISTENCE
of static concentric A0 embedded cells UNDECIDED (tool-limited, trap-#1 scoped: "not found from these seeds,"
NEVER "does not exist"). Three verified solver rounds (E2c gauge-fix / E2d continuation / E2e phys-seed) each
localize the SAME depth-stiffness wall.

**⇒ THE OPTION-3 DECISION IS CHARLES'S (presented 2026-07-04, awaiting his call): 3a = one more mechanism-
matched solver idea (a DEPTH-STIFFNESS HOMOTOPY ramping core depth shallow→physical, untried, directly targets
the diagnosed wall) vs 3b = pivot to the ω≠0 REFRAME (his founding φ-angular hunch, the pre-named escape —
static concentric A0 may be the wrong frame) vs checkpoint/pause. Driver lean: 3a once (cheap, mechanism-
matched), 3b strongly queued if it fails — but the frame call is his.**
