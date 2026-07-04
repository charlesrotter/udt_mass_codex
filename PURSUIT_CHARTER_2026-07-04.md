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
- **R1 (armchair, FIRST): attempt the native derivation.** Does the positional-dilation
  principle force one route? The fork originated in the native-action derivation (the Z_φ fork;
  see native_dilation_weight_derivation_results + F1F3_closure_results + the
  constrained-two-player doc). Interrogate: is the mixing term FORCED by the same R1-preservation
  logic that forced everything else, or forbidden by it, or genuinely free? Watch: "it folds
  away" claims = the prime smuggle suspect (CLAUDE.md trigger #6). Outcome: FORCED-A / FORCED-B /
  FREE (then observation decides).
- **R2 (cheap, potentially decisive): the vacuum-deformation confrontation.** Route-B G has no
  flat solution — derive what its deformed vacuum (ρ=ar+b, φ=φ₀−½ln ρ) implies for the banked
  macro constraints (Cassini-class solar-system bounds — see the X=−2e5 Cassini history in
  memory/NEGATIVES; terrestrial clock constraints; the a(φ) both-extremes rule
  [[myopic-errors-dilation-exponent]]). If Route-B's vacuum violates a solid bound → Route B
  dies and fork 3 closes cheaply. If compatible → it becomes a PREDICTION (consilience roadmap).
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

- **E2c OPTIMIZER HARDENING (gates ALL sweeps of ANY frame):** globalization/deflation/
  extended-precision/explicit soft-direction (dilation-slide) handling. CERTIFICATION = the
  manufactured-solution (MMS) gauntlet from seed-class distances (O(0.3–1.5) in field norm) to
  max|F|≤1e-8 at production grids — the harness pattern is in microphysics_E2_bv_mms.py. No
  sweep result means anything until an optimizer passes this.
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
