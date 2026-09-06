---
name: solver-first
description: Use when a solver result is far from observation, or BEFORE reaching for any new mechanism/coupling/term to explain a gap. The binding "mismatch -> SOLVER, not MECHANISM" four-question protocol (Charles 2026-06-19).
---

# Solver-first, not mechanism (binding)

When a result is far from observation, first audit the solver and its application before proposing a
new physical mechanism. This protects against repairing an implementation error with invented
physics, but it is a finite diagnostic protocol rather than an indefinite shield from adverse
evidence.

## The four questions (in order)
1. What did we leave OUT of the solver? (a term, a coupling, a sector, a boundary)
2. Is it a NUMERIC problem? (convergence, box-control, conditioning, a bug, grid)
3. Did we FREEZE or forget to turn on a degree of freedom?
4. Does the claim require broader solution-space coverage than the bounded calculation supplied?

Freeze a diagnostic plan before running it: relevant checks, resource budget, stop conditions, and
maximum conclusion. Use only the claim-relevant subset of bases, grids, seeds, continuation, gauge
tests, and independent re-derivation. When the plan ends, report one of: implementation defect,
bounded incompatibility, or remaining numerical ambiguity. Do not demand every imaginable solution.

## Why
A mismatch initially tests solver completeness before motivating new physics. A surviving mismatch
may be valid bounded adverse evidence. Do not protect a favored theory or a favored negative result,
and do not introduce an undeclared repair mechanism.

## Instruments
- `archive/SOLVER_COMPLETENESS_MAP.md` — historical coverage map; use it only for dated context,
  then record current coverage in the task's preregistration and current program
  (skill `completeness-map`).
- Bound the computation. Declared fixed-DOF slices can answer appropriately scoped questions; they
  are not whole-theory verdicts.
- For any declared constrained problem, test perturbations within its constraint surface; an
  off-constraint diagnostic cannot by itself certify stability or instability of the admitted class.

SCAR it heads off: the year-long catalog/mechanism hunt that read a graveyard of
contaminated/classical-solver negatives as a verdict on the metric.
