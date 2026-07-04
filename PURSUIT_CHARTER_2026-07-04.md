# PURSUIT CHARTER — written 2026-07-04 at the Fable→successor model handover

**What this is:** the load-bearing orientation document for the NEXT driver, written deliberately
explicit — assume nothing is obvious. Read order: LIVE.md TOPMOST → this charter → CLAUDE.md
"How we work" + DRIVER TRIGGERS + the `.claude/skills/` → HANDOFF.md TOP. Charles's standing
instruction at handover: organize first, then the forks, **with emphasis on FORK 3 (the route
fork)**.

## 1. Where the project stands (one paragraph, lay)

The universe cell is SOLVED: a finite sealed domain that closes only on an integer ladder
N=0..22, whose spectrum law was derived and then blind-predicted 13 unseen rungs to ~0.1%
(Stage-D — the project's strongest result type). The universe is the stable N=0 ground state of
its own ladder (canon). Microphysics re-entry began: particles are hypothesized as embedded
cells inside the real solved universe (never in model ambients — that era is over). The first
embedded sweep (E2) came back "nothing converges," but the blind verifier proved the OPTIMIZER
was too weak to decide existence (convergence radius ~1e-3 vs seed distances ~1) — so embedded-
particle existence is genuinely UNDECIDED, not refuted. Meanwhile the two-regime frame (Charles)
produced verified theorems: the mass-emergence MECHANISM (anchors, seal flux, quantization
closure) exists ONLY in Branch P; Branch G is provably emergence-dead. And the long-parked
Route-A/Route-B action ambiguity was discharged into PHYSICS: the two routes now differ
structurally and observably. That fork is the current pivot.

## 2. The treasure list (banked, blind-verified — do NOT re-litigate; cite these)

| Result | Doc |
|---|---|
| Integer ladder N=0..22 + derived laws (a_seal≈√Z/[(N+1)π+θ₀]; quantization closure) | cascade_stage{A,B,C}_results, ladder_* docs |
| Stage-D: 13/13 blind prediction of the aliased window | cascade_stageD_results.md (+prereg) |
| Stability: fundamentals minimum-class; universe = N=0 ground state | canon C-2026-07-03-1/-2 |
| Native field equations; G/P branch fork; switch criterion (χ-pinning) | native_field_equations_constrained_two_player_results, gp_switch_criterion_results |
| Criticality migration: embedded cell inherits E_ang(core)=2 (BRANCH-BLIND, ROUTE-B-ROBUST) | microphysics_E1_composite_closure_results (+canon-adjacent note), d2c |
| E2: existence UNDECIDED; solver-completeness finding (optimizer radius ~1e-3) | microphysics_E2_coupled_solve_results.md |
| D1: N=3 + the 1+3+5 algebra + structural-i = TRUE CARGO (native); q=1/3, η=1/18 = imports → now TARGETS | d1_angular_constants_native_rederivation.md |
| D2a: universe interior ALL-P; thin strong-P shell holds 99% of q (last ~0.04–0.14% of radius) | d2a_switch_criterion_interior.md |
| D2b: T-G1 (no G-vacuum self-closure, route-robust) + T-G2 (emergence mechanism P-ONLY) | d2b_no_structure_in_G.md |
| D2c: corrected Route-B EOMs; banked fold values + E_ang(core)=2 route-robust; Route-A G|P closes nowhere (Z>0); flat FAILS Route-B G | d2c_gp_composite_conditions.md |

## 3. FORK 3 — THE ROUTE FORK (the emphasized pursuit)

**What it is.** Two candidate forms of the native action have coexisted since June: Route A
(the form all live solvers implement, carrying Z=8 as a free value) and Route B (Z_φ=8 PLUS a
forced mixing term 2√h e^φKφ'). D2c derived the mixing term through everything: in round-static
it reduces to 4ρρ'φ' per steradian; the corrected Route-B EOMs are banked in
`d2c_gp_composite_conditions.md` §Part-1 (+ CAS `d2c_part1_mixing.py`); the exact identity
Route-B-kinetics = Route-A Z=8 in the shifted field φ̃ = φ + ½ln ρ, minus a ρ'² term.

**Why it is now the pivot (three independent arrows):**
1. **Structural discriminator:** the regime-crossing (G|P) particle architecture closes NOWHERE
   under Route A (derived sign obstruction) but is OPEN under Route B (φ̃-monotonicity replaces
   φ-monotonicity; φ_p ≤ ½ln(ρ_sU/ρ_p) can be positive). Necessary-not-sufficient.
2. **Macro lever:** flat space FAILS Route-B's Branch G exactly; Route B's flat-analog is
   ρ=ar+b, φ=φ₀−½ln ρ — Route B DEFORMS THE VACUUM. This is confrontable with observation.
3. **Twisted-fold interplay:** the G-exclusive fold family φ→2a−φ (every a) interacts with the
   route choice (see d2b E2/E3).

**What is SAFE either way (verified):** all banked fold pins, E_ang(core)=2, the criticality
migration. **What is ROUTE-A-CONDITIONED:** the interior profiles and ladder NUMERICS (the
integers/laws were derived at Route-A structure, Z as stated), the E2 landscape, the D2c
sign obstruction.

**THE RECOMMENDED DECISION PROGRAM (in order; MAP first at each step; lay-present to Charles):**
- **R1 — DONE, BANKED, BLIND-VERIFIED (2026-07-04, commit 40294ef;
  `r1_route_fork_native_derivation.md`, verifier a31db58f300da6011 8/8): VERDICT = FREE-ON-A-SHEET.**
  The forcing rule pins WEIGHTS, never coefficients; the mixing term is weight-0 (admitted) with
  no orphan weight to compensate (not required). The fork is really the TWO-PARAMETER SHEET
  (Z_φ, μ): Route A = the μ=0 edge (Z free), Route B = the single point (8,2), conditional on
  two unforced CHOSEs (single-curvature-origin + c_L=1). **The ONE observable = s = 2μ/Z, the
  vacuum-deformation exponent** (A: s=0; B: s=1/2; clocks in μ≠0 vacuum are slaved to areal
  radius, e^{−2φ} ∝ ρ^{2s}; observability EXACT — no redefinition hides it). The mixing term IS
  a kinetic-level φ-angular coupling (areal growth drags depth — the founding hunch at the
  action level). Fold pins are family-robust across the whole sheet (R3 well-posed everywhere).
  CHARLES'S TWO STANDING FLAGS from R1: (i) adopt "kinetic must descend from one curvature
  object"? (would force B modulo c_L); (ii) bless the R2 reframe below.
- **R2 (cheap, potentially decisive — REFRAMED by R1's verdict): BOUND s = 2μ/Z, not a binary
  A/B test.** The general-(Z,μ) deformed vacuum is ρ=ar+b, φ=φ₀−s·lnρ (clock rate ∝ ρ^{2s}).
  Derive what the banked macro constraints (Cassini-class solar-system bounds — see the X=−2e5
  Cassini history; terrestrial clock constraints; the a(φ) both-extremes rule
  [[myopic-errors-dilation-exponent]]) imply as a BOUND on s. s bounded ≈0 ⇒ Route A wins and
  fork 3 closes; s bounded away from 0 impossible but a finite window ⇒ the sheet survives as
  a measured parameter (a PREDICTION lever for the consilience roadmap). Extra R1-derived
  levers: the φ'-jump at G|P seals; flux-without-twist Φ=2μln(ρ₂/ρ₁)/I in odd+odd G-domains.
  DATA-BLIND discipline: derive the s-dependence of each observable FIRST, frozen, before any
  observational number is loaded (pre-register the confrontation).
- **R3 (bounded solve, only after R1/R2): the Route-B universe cell.** Re-run the T3 closure
  under the corrected Route-B EOMs (the solver change is small — the φ-EOM gains (4ρρ'φ')'
  terms... use the banked corrected forms, do NOT re-derive ad hoc). Questions: does the cell
  still close? Is there still an integer ladder? Do the rungs move? (The fold values can't —
  verified — but interiors can.) A ladder that survives BOTH routes = magnificent robustness;
  a ladder that dies under B while B wins R1/R2 = a crisis to bring to Charles immediately.
- **R4 (gated on R1–R3): the Route-B G|P particle architecture** — the E1-analog condition set
  partially exists (d2c Part 2's Route-B rows); complete it, then it queues behind the
  optimizer gate like everything else.

## 4. The other forks (Charles's, pending — do not resolve silently)

F1 twisted folds admissible? (rescues architecture A1 only; canon-as-worded blocks) · F2 does
the φ-flat inert massed G-cell "count" as structure (T-G1 headline wording) · F4 compactly-
supported carrier (definitional) · F5 Class A/B for the particle seal (standing June gate;
Class-B = a named escape of the D2c obstruction) · F6 the G-core (G-inside) architecture
(underived; awaits interest). Also owed: the **photon/EM-native re-grade** (#47-pos/#50 on the
native field equations — absent from the CARRY table; cheap; a good warm-up task).

## 5. The other paths (valid regardless of fork 3)

- **E2c OPTIMIZER HARDENING — DONE, BANKED, blind-verified (2026-07-04, commit c68d65d;
  `microphysics_E2c_optimizer_hardening_results.md`; no physics moved — git diff insertions-only).**
  The 0/256-undecided cause = a near-exact TRANSLATION GAUGE of the boundary pair (ambient r-autonomy,
  cos=−1.000000); FIXED via Ruiz two-sided equilibration (cond 5.7e11→1.9e7) + Powell dogleg trust
  region; certified converging from boundary offsets ≥30 to ~5e-9 on 2 MMS (incl. bulged). Hardened
  driver = `lm_hardened` in `cell_solver_composite.py` (lm_qr + pure-universe left byte-identical).
  Residual FIELD-AXIS wall = intrinsic local-NLLS minima ⇒ the re-sweep needs MULTI-START +
  CONTINUATION; non-convergence reads "not found from these seeds," NEVER "does not exist" (trap #1).
- **E2d = THE GATED RE-SWEEP (the owed next step):** build a continuation/homotopy driver (coarse→fine
  grid or stiffness homotopy) on `lm_hardened`, multi-start; re-run the E2 embedded-particle sweep. THIS
  is what makes existence decidable. Still concentric round-static Branch-P (A0), or the surviving frame.
- **D4 ω≠0 stationary internal rotation** (Nψ→Nψ+ωt): Charles's founding φ-angular hunch; the
  e^{2φ}-weighted frequency is the derived one-sided coupling; enter via a MAP, after the route
  fork is settled enough to know which action to rotate in.

## 6. KNOWN TRAPS (hard-won; each cost real work — the next driver inherits them free)

1. **Optimizer reach ≠ physics.** 0/256 sweeps meant NOTHING until MMS-tested. Never bank a
   nonexistence claim without proving the instrument could have found existence.
2. **H_cell is the honest gate:** falling residual with H_cell=O(1) is a FALSE FLOOR, always.
3. **Graduated floors** (≥2 decades) for all zero-counting; loose floors undercount high-N.
4. **Bracket ambiguity** near accumulations: one bracket can hold many roots.
5. **Anti-hang:** bounded grids (Nr≤16/24), capped iters, ONE process, never background-poll a
   solve, never blend-toward-an-endpoint and call it dynamics.
6. **GPU:** torch float64 works (ignore NVML warning); batched solve_triangular with broadcast
   Cholesky corrupts at batch~150+ — explicit inverse + matmul + per-batch CPU asserts.
7. **The promotion trap:** "candidate" labels drift into "derived" (it happened; D1 caught it).
   Every constant: chose-or-derived, out loud, with the deriving script actually deriving it.
8. **Charles's intuition = compass, not evidence.** It has repeatedly pointed within arm's
   reach of load-bearing assumptions (the P|P seal, the two regimes) AND repeatedly needed the
   record to file it sharp (φ→−∞, horizons-at-zero, "mirrored"). Aim verifiers hardest at
   whatever would CONFIRM his standing picture. Ponder with him in LAY language, always.
9. **Every result: verifier-before-record.** The blind adversarial pass has caught something
   material in essentially every arc — including breaking our own headline negatives (E2) and
   strengthening our own positives (D2b). Budget for it; it is not optional overhead.
10. **Decide with Charles:** forks are HIS. Present, recommend, stop. Canon is his signature.

11. **Don't lean on CONDITIONS-CHANGED / pre-native-field-equations work until it is re-graded.**
    (Charles 2026-07-04, after the driver cited the 2026-06-22 S²-defect discovery to help resolve
    the R2 frame fork.) The native field equations (2026-07-01) are THE foundation; any banked result
    older than that, or flagged CONDITIONS-CHANGED in NEGATIVES_REGISTRY, has NO supporting or blocking
    authority until re-graded at point of use. Check date + registry status BEFORE citing a result as
    support; clean-current support must stand on its own. Re-grade owed ⇒ run it before leaning.
