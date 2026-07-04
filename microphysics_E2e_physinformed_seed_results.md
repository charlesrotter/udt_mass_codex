# E2e — physics-informed seed: BUILT + certified-attempt FAILED (provisional; verifier owed)

**Date:** 2026-07-04. **Status: PROVISIONAL (verifier owed). BOTH approved paths RAN: lean 1 (physics-informed seed)
did NOT certify; lean 2 (scoped-caveated sweep) returned a NULL (no candidate). The genuine
option-3 decision (grind the solver further vs pivot to the ω≠0 reframe) is now owed to Charles.** Physics byte-identical (residual_comp
untouched; new code in `e2e_physinformed_seed.py` / `e2e_mms_combinedcell_certification.py` /
`e2e_physinformed_sweep.py`). Data-blind. Data: `e2e_mms_combinedcell_certification.json`.

## What was built
A PHYSICS-INFORMED seed generator from the DERIVED core (canon C-2026-07-03-3): even mirror fold
at finite depth, core pinned by the migrated criticality E_ang(core)=2 given (ξ,κ,N), interior from
a short outward EL integration — replacing E2d's flat continuity-flats. Derived core radii:
ρ_c=0.1826 (W1 plateau, N=1 ξ=0.5 κ=0.1); ρ_c=1.033 (W6 wall, N=2 ξ=0.05 κ=1.0).

## Certification result — the physics-informed seed does NOT certify the combined-cell field axis
On the MMS (synthetic known-root) combined-cell field axis, ALL cases read **reached = False**
(PHYS and FLAT seeds; direct and arclen; δ=0.1, 0.3; W1 plateau + W6 wall). The physics-informed
seed is MARGINALLY better than flat (smaller seed_dist — 0.10 vs 0.82 on W1; slightly larger fold
s_max) but insufficient. Runaway false-floors correctly rejected by the REACH criterion (e.g. W6
FLAT direct max|F|=1.4e-8 but dist=360, r_p-ratio=0.34 → rejected as the soft-dilation runaway).

## THE KEY FINDING (new — the reason the fix didn't work; input to the option-3 ponder)
**The combined-cell obstruction is EXTREME LOCAL STIFFNESS, not seed distance.** The
physics-informed seed at field-distance **0.1** already carries residual seedF ≈ 17, and the
Newton/arclength homotopy **folds almost immediately** (s_max ≈ 9e-4 on W1 δ=0.1; ≤2e-4 elsewhere)
then escapes along the soft-dilation direction. Starting *closer* does not help because the
residual surface near these combined-cell configurations is near-vertical (the e^{−2φ}~1e4–1e6
depth stiffness). This is consistent across E2c→E2d→E2e: three rounds of solver hardening (Ruiz
equilibration, dogleg trust region, continuation, now physics-informed seeding) have each improved
OTHER axes but not tamed the combined-cell field axis. Per solver-first this remains a tool/
conditioning limitation — but a CHARACTERIZED, PERSISTENT one, now with a mechanism (immediate
homotopy fold from extreme local stiffness), which is legitimate input to Charles's option-3
question (is this telling us something structural about static concentric embedded cells / does it
motivate the ω≠0 reframe?).

## The decision owed to Charles (before more compute)
- **Lean 1 (physics-informed seed) FAILED to certify** — the combined-cell axis is stiffness-locked.
- **Lean 2 (scoped-caveated sweep) is READY but now LOW-VALUE:** the tool cannot reliably reach
  combined-cell roots, so a null would be weak ("not found from these seeds") and a positive
  unlikely+suspect. It is Charles-authorized as the fallback; the new stiffness finding lowers its
  expected value.
- **Option 3 (the persistent stiffness/fold is INFORMATIVE):** three solver rounds localizing the
  same combined-cell wall, with a mechanism, is a genuine input to whether static concentric A0
  cells are the right frame — i.e. the ω≠0 reframe (Charles's founding φ-angular hunch), which is
  HIS call.
CHOSE: MMS synthetic roots (may not sit near a PHYSICAL cell's derived core — a caveat on reading
the certification as verdict on physical cells); grids Nr12/Nθ8; window cells W1/W6; REACH criterion
(provenance-not-merit). Verifier owed: confirm reached=False is not a harness artifact; confirm the
immediate-fold/stiffness reading; confirm residual_comp untouched.

## Lean 2 (scoped-caveated sweep) RAN — NULL (data: `e2e_physinformed_sweep.json`)
Bracket A1 m=3 Z=8, window cells W1/W4/W6/C1 × {plateau, wall} × amp 0.8, BOTH seed families
(phys-blend + flat), physics-informed multi-start + continuation on lm_hardened. **candidates: [] —
NO converged cell** (every run status:no; conv target max|F|≤1e-8). Coverage COMPLETE (8/8
cell×slice), NOT throughput-limited. The homotopy folds EARLY everywhere (s_reached 0.0003–0.21) —
the same combined-cell stiffness wall. **Read STRICTLY per trap #1: "NOT FOUND from these seeds +
continuation," NEVER "does not exist"** — the tool is uncertified on the combined-cell axis, so this
null is WEAK (tool-couldn't-reach, not a nonexistence proof).
Sub-observation (honest): the PHYSICS-INFORMED seeds keep the free boundaries BOUNDED
(r_p_end ~O(100–2800)) while FLAT seeds run away catastrophically (r_p_end ~O(1e5–1e7)) — the
derived-core seed genuinely controls the soft-dilation runaway; it just cannot converge THROUGH the
depth-stiffness fold. So the physics-informed seed is a real (if insufficient) improvement.

## COMPLETE E2e PICTURE + the option-3 decision (owed to Charles)
Three verified solver rounds — E2c (Ruiz+dogleg, fixed the translation-gauge defeater), E2d
(continuation, certified boundary+u axes), E2e (physics-informed seed, controls runaway) — have
each improved the tool and each localized the SAME COMBINED-CELL WALL: extreme e^{−2φ} depth
stiffness that folds every homotopy path near s=0. Existence of static concentric A0 embedded
cells is therefore NOT decided (tool-limited, null-with-coverage), and solver-first has been
substantially exercised. This is the informed input to CHARLES'S OPTION 3: is the persistent,
now-mechanism-characterized wall telling us static concentric A0 is the wrong frame — motivating
the ω≠0 reframe (his founding φ-angular hunch, the pre-named escape)? Or one more solver idea
(e.g. a stiffness-homotopy that ramps e^{−2φ} depth from shallow→physical)? HIS CALL.

---

## VERIFIER RECORD (blind adversarial pass — agent a0205204484a1d48c, 2026-07-04): SAFE TO BANK (tool-limited null-with-coverage)

All 6 attacks PASS, independently reproduced. (1) PHYSICS UNTOUCHED — `git diff HEAD cell_solver_composite.py`
EMPTY (byte-identical to the E2c-verified HEAD c68d65d; residual_comp/lm_hardened unmodified; all E2e code
in e2e_* files, no monkeypatch). (2) NULL IS REAL — re-ran W1/plateau + W6/plateau: status:no genuine
(maxF 5+ orders from the 1e-8 target, not a near-miss, not a discarded root); the one sub-1e-8 point in the
corpus (cert W6_wall δ0.1 flat, 1.36e-9) correctly REJECTED as a dilation runaway false-floor (dist=360).
No mislabeled convergence. (3) STIFFNESS reading EXACT — W1/plateau δ0.1: MMS root max|F(v*)|=0; phys seed
at field-dist 0.100 carries seedF=16.913 (matches) and folds at s_max=8.76e-4 (matches) ⇒ depth-stiffness,
not distance; derived_rho_c reproduced to 10 digits. (4) PHYS-CONTROLS-RUNAWAY confirmed (phys r_p bounded
O(100–2000); flat runaway to 5.5e7). (5) TRAP-#1/OPTION-3 framing HONEST (null scoped tool-limited-not-
nonexistence; solver-first honored; MMS-synthetic-root caveat flagged; option-3 = Charles's call). (6)
HYGIENE — pytest 32/1xfail; data-blind. **VERDICT: safe to bank; existence UNDECIDED (tool-limited); the
option-3 decision (3a depth-stiffness homotopy vs 3b ω≠0 reframe) is Charles's.**
