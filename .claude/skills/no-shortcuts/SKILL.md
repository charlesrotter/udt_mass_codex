---
name: no-shortcuts
description: Use when building/editing solver code or before banking a result. The anti-shortcut / anti-import checklist + the machine-enforced purity harness (cleaner is not clean; the AI always wants shortcuts).
---

# No shortcuts — cleaner is not clean (binding)

The AI always wants shortcuts: freeze a DOF, fix a value, take the tractable slice, linearize,
import a BC/count. Cleanest machinery != completely clean. Audit AS you build; FLAG every
compromise out loud; never present a slice as the whole; vet your own headline.

## Run the machine guard
`python3 -m pytest tests/` — the purity harness:
- P1 (`test_solver_integrity.py`): liveness (no dead DOF), provenance lint (no untagged physics
  literal), limit recovery (flat/Schwarzschild vacuum + de Sitter NORMALIZATION), native-object
  guard (no S^3 Skyrme import).
- P2 (`test_operator_from_action.py`): the live operator == the EL of `solver_action.py`.
GREEN required. The `documented_gap` xfails are the migration TODO (an XPASS = a tripwire to flip
the guard), NOT failures. Catch-proof every NEW guard (reintroduce the bug -> RED).

## Anti-import / anti-freeze checklist
- Every physics constant carries a tag: `# DERIVED | POSTULATED | FREE | IMPORTED`. No bare
  physics literal in the operator. Values are SOURCED (solver_action.py), never re-asserted in a test.
- No mechanism/coupling/term posited because it would HELP — derive from the metric/action (P1).
- No SM entity/analog imported as a label until the metric demands it (P3).
- No linearization/approximation as a stated result or an input to another calc (P2;
  exp(-2*phi0) ~ 5 at hadronic depth — linearization invalid ~5x there).
- BOUND the grid; never FREEZE a DOF to pass a test. Frozen-DOF slices are NOT verdicts.
- "chose or derived?" on every value/BC/sign/chart BEFORE use. "observing or targeting?" before
  every agent launch — if targeting a desired answer, STOP and ponder.
- Algebraic objects can be imports (cohomology / transfer-ladder / N=3-q=1/3 dressed as native).
  Audit native-vs-import provenance before banking mass/spectrum on one.
- ANTI-HANG: coupled solves are SLOW — bound iters/grid (Nr<=16/24), ONE clean process, never
  concurrent, never launch-a-solve-and-poll a background task.
