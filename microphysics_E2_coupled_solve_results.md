# E2 COUPLED-SOLVE RESULTS — existence UNDECIDED; a first-class SOLVER-COMPLETENESS finding

**Date:** 2026-07-04. **Contract:** `microphysics_E2_battle_plan.md` (approved verbatim by
Charles). **Chain:** E2a solver (commit 17678d6) → four bracket sweeps
(`microphysics_E2b_{A1Z8,A1Z1,A3Z8,A3Z1}_results.md`, agents a4bd10c6ff038f738 /
a15639064dca75346 / aa2e5c0d9f3ec0fa0 / a536290aca4909115) → **blind adversarial verifier
a98ce79ecc245b189 over the WHOLE chain** (scripts `microphysics_E2_bv_*.py`, committed with
this doc). Data-blind throughout (verified). pytest 32/1xfail.

## THE VERDICT (the verifier's, adopted)

**The pre-drafted frame-level negative ("no static concentric embedded L2+L4 cell in the real
ambient") is NOT BANKED — the verifier BROKE it at the pre-committed failure ladder's step (2):**

- **Manufactured-solution gauntlet (the decisive instrument):** on a synthetic composite state
  with a GUARANTEED exact root at production grid/stiffness, the production float64 monolithic
  LM converges only from perturbations ≲1e-3–1e-4; from seed-class distances (O(0.3–1.5) in u)
  it stalls at floors 5.4e-4–1e-2 with outward boundary drift — **exactly the sweeps' failure
  signature, produced while an exact solution IS present.** Even the 1e-8 certification floor
  sits at the float64 achievability edge of this architecture.
- Therefore **0/256 phase-1 (0/338 all-instruments) is a true observation about the OPTIMIZER'S
  REACH, and existence of composite solutions in the swept window is UNDECIDED.** Solver-first,
  applied by the instrument itself: the gap demonstrated today is numeric.

## What DID survive verification (banked, blind-verified)

1. **The sweep data and landscape characterization (all recomputed independently):** 0/256;
   dilation-orbit exponents −1.3087 (A1Z8, node-uniform), −0.988±0.066 (A1Z1), −1.001±0.012
   (A3Z8), non-self-similar decelerating (A3Z1); H_cell O(1) on every end state = every falling
   Φ a false floor (the honest-gate logic HOLDS); shell-width preservation; **seed-height
   preservation SETTLED over station-tuning** (bracket 4's discriminating arithmetic exact:
   dev(seed) ≤ 3.2e-5 vs dev(station) ≈ +1.5e-4 uniform); the parking family = exactly the E1
   wall-admissible N=2 κ≈1 cells wherever they exist (the correlate that survived all four).
2. **The C1c adjudication (CORRECTED):** the universal θ-sawtooth holdout is NOT a C1c-vs-f-PDE
   functional incompatibility and NOT a discretization pathology — the u-subsystem at frozen
   geometry converges to 2e-14 under three discretizations. It is the coupled LM's stagnation
   residue of a **C2-vs-f-sector tension** (closing the f-sector drops E_ang(seal) to 0.55 vs
   the required 2.0 on runaway states; ≈2.03 on the parking family). May NOT be cited as
   nonexistence evidence.
3. **E2a instruments:** 25/25 harness reproduced fresh; pure-universe recovery a*≤5.1e-9 all
   brackets; the r_s softness = a 99.9%-pure r_sU slide direction (attack 2 HOLDS) — and it is
   THE SAME soft dilation/slide family the composite LM stagnates along: E2a's flagged softness
   and E2b's failure mode are one phenomenon.
4. **Bracket-2 REGRADE (formal, verifier's sentence, applied to that doc):** wall end states
   were seed-height-preserved, not station-tuned; U(ρ_p)≈2 was the 0.95·r_s seed sitting on the
   U≈2 shoulder; the solver-tuned row is C2.
5. **Count correction:** phase-1 = 256 (62+62+62+70), not 264; all-instruments = 338.

## Premise set of what WAS decided (explicit, per the verifier's attack 6)

The characterizations above are scoped to: round + static + diagonal + areal (CHOSE ×4);
CONCENTRIC (CHOSE); **Branch-P both media with the seal a P|P CONTINUITY interface (CHOSE, E1
ledger #9 — Charles's two-regime catch names exactly this row; the G|P weight-jump alternative
is UNTESTED; the purity harness's standing xfail names the "silent G/P fork")**; source-free
Class-A seal (CHOSE); free outer fold (CHOSE); a* HELD / Δφ floats (THEORY: E1 #5); L2+L4
carrier only (THEORY); ξN<2, κ∈(0,1], N∈{1,2}; rigid+bulge seeds amps ≤1.5 at
r_p0∈{100, 0.95·r_s}; the four E0 brackets; grids Nr≤16/Nθ≤12/Na≤256, kmap 2.5, guards ≤25·r_s;
**float64 monolithic LM with demonstrated ~1e-3 convergence radius; 1e-8 certification floor at
the float64 achievability edge** (the two NEW premises this pass added — without them any
negative over-claims). NOT swept: N≥3, ξ>1.9, κ>1, anchor='exact' (unwired), off-center, ω≠0,
and seeds within the LM's convergence radius of any putative solution (structurally
unreachable).

## THE OWED NEXT STEP (pre-committed by the plan's own ladder + binding solver-first)

**E2c — OPTIMIZER HARDENING**, not a reframe, not a mechanism: globalization / deflation /
extended-precision / explicit soft-direction (dilation-slide) handling, certified by the SAME
manufactured-solution gauntlet from seed-class distances BEFORE re-sweeping. The ω≠0 escape
ladder remains Charles's reframe decision and NOTHING here forces it yet. Charles's two-regime
frame-catch (the P|P seal CHOSE) remains live and is UNAFFECTED in either direction: the
same-regime null was never decided. NOTE OF HONESTY owed to the record: the driver's earlier
lay reading "the runaway corroborates the smaller-universe-cell picture" is WITHDRAWN as
evidence — the MMS test shows the same outward drift occurs when an exact solution exists;
the runaway characterizes the OPTIMIZER's soft-valley behavior, not (yet) the physics.

## Verifier corrections applied

Bracket-2 regrade appended to `microphysics_E2b_A1Z1_results.md`; the 256 count corrected here;
the C1c wording corrected here (per-bracket docs retain their raw contemporaneous text; THIS doc
+ the verifier record are authoritative on both points); premise set enumerated above; this
deliverable itself was owed (plan's outcome-table doc) — the per-bracket tables live in the four
bracket docs, linked, rather than duplicated.
