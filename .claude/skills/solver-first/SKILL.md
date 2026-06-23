---
name: solver-first
description: Use when a solver result is far from observation, or BEFORE reaching for any new mechanism/coupling/term to explain a gap. The binding "mismatch -> SOLVER, not MECHANISM" four-question protocol (Charles 2026-06-19).
---

# Solver-first, not mechanism (binding)

When a result is far from observation, the FIRST hunt is the SOLVER and our application of it
— NEVER a mechanism. Reaching for a mechanism to close a gap is FORBIDDEN until the solver is
demonstrably complete AND the solution space is genuinely explored.

## The four questions (in order)
1. What did we leave OUT of the solver? (a term, a coupling, a sector, a boundary)
2. Is it a NUMERIC problem? (convergence, box-control, conditioning, a bug, grid)
3. Did we FREEZE or forget to turn on a degree of freedom?
4. Have we explored the solution space with EVERYTHING ON, or only a corner?

Plus the many WAYS to examine one solve: different bases, grids, seeds, continuation, gauge
tests, independent re-derivation.

## Why
A mismatch indicts the solver's COMPLETENESS first, the metric last, and a mechanism never
(the import reflex). This is Principle 1 applied to our own numerics. The microphysics space
is UNENTERED, not walled — the pre-postulate negative corpus is RETIRED (mine for tooling only).

## Instruments
- `SOLVER_COMPLETENESS_MAP.md` — see what's on/off/frozen/never-built before trusting a result
  (skill `completeness-map`).
- BOUND the grid, never FREEZE a DOF. Frozen-DOF slices are NOT verdicts ("one more thing").
- Test gravitating-soliton stability by a constraint-respecting COUPLED re-solve along the
  negative modes — never off-constraint stiffness (over-counts instabilities).

SCAR it heads off: the year-long catalog/mechanism hunt that read a graveyard of
contaminated/classical-solver negatives as a verdict on the metric.
