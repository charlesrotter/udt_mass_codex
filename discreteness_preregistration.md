# PRE-REGISTRATION — "Discreteness emerged?" acceptance contract (Charles, 2026-07-01)

**FROZEN BEFORE THE SOLVER RUNS.** This is the falsification contract for the return-to-solver phase, committed
before any constrained-two-player solve, so criteria cannot be retrofitted. Author: Charles (verbatim below).
Frozen model = the DERIVED native frame: constrained-two-player metric, interior Branch P + exterior Branch G +
seal junctions JC1/JC2 (`native_field_equations_constrained_two_player_results.md`, `gp_switch_criterion_results.md`,
`native_geometric_action_results.md`, `seal_matching_junction_results.md`). `Z_φ` held FIXED across any scan (the
one open constant; one global choice at most).

## THE BINDING RULE
> **Do not solve for "the electron." Solve for the solution space.**
> Then ask: Are there isolated stable cells? What are their fluxes, sizes, and ratios?
> Only AFTER that do we compare with known particles.

## STAGED GOALS (modest first — do NOT jump to spectrum)
1. **FIRST:** does the derived P-interior / G-exterior / seal-matching system have ANY stable isolated finite-cell
   solutions AT ALL? (Prove the geometry produces CELLS.)
2. **THEN:** do the cells form a DISCRETE FAMILY? (Isolated values, gaps.)
3. **THEN (blind, after):** compare ratios/properties to known particles.

## "DISCRETENESS EMERGED" — the criteria (Charles, verbatim)
"discreteness emerged" means the solver finds stable finite-cell solutions only at certain isolated values, without
us putting those values in by hand. It does NOT mean we tune boundary conditions, stiffness constants, grid choices,
or seal rules until a particle-like number appears. Count discreteness as real only if MOST of these happen:

1. **Isolated solutions, not a continuum.** When the solver scans allowed cell sizes / seal fluxes / central
   conditions, stable solutions appear at separated points or bands, with gaps between them. If every nearby value
   also works, that is not discreteness.
2. **Same solutions from different seeds.** Starting from very different initial guesses lands on the same cell
   families. If the result depends heavily on the starting guess, it may be numerical steering.
3. **Stability without imposed targets.** The cell holds together under the derived equations without us forcing a
   mass, radius, charge, or particle identity. Label afterward, not before.
4. **Grid and method independence.** The same solution family survives changes in resolution, radial basis, solver
   method, and tolerances. If the "spectrum" moves around with the numerical machinery, it is not geometry.
5. **No hidden fitting knobs.** Any remaining free parameter, especially Z_φ, is held fixed across the scan. No
   retuning per solution. One global choice at most, then observe the whole space.
6. **Quantized public charge / flux.** Since exterior mass/charge appears to be seal flux, real discreteness shows
   up as only certain stable seal-flux values q being allowed.
7. **Branch consistency.** Interior P, exterior G, and seal matching all satisfied together. A candidate cell that
   only works by violating the derived matching rules is not a UDT solution.
8. **Perturbation survival.** Slightly disturb the solution → it returns to the same cell or moves toward another
   allowed cell. If it drifts continuously, the discreteness is not real.
9. **Blind classification.** The solver outputs UNLABELED solution families first. Only after the scan is complete
   do we compare ratios/properties to electron/proton/etc. Prevents sculpting the answer.

**Short definition:** discreteness has emerged if the derived UDT equations admit stable, isolated finite-cell
solutions with quantized seal fluxes, found repeatedly from neutral scans, robust to numerical changes, and only
compared to particles after the fact.

## Status
Committed as a pre-registration contract on 2026-07-01, before the constrained-two-player solver is built/run.
Next: MAP the solver (recipe + how each criterion is instrumented), bring to Charles, then build (gated).
