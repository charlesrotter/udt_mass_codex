---
name: no-shortcuts
description: Use when building/editing solver code or before banking a result. The anti-shortcut / anti-import checklist + the machine-enforced purity harness (cleaner is not clean; the AI always wants shortcuts).
---

# No shortcuts — cleaner is not clean (binding)

Shortcuts become dangerous when they are hidden: an untagged fixed degree of freedom, imported
physical equation, undisclosed truncation, or conclusion wider than the calculation. Audit as you
build, state every restriction, and keep the headline inside the proved scope.

## Run the machine guard
Run the targeted tests while editing and the relevant current regression at closure. Do not use a
copied pass count or dated failure exemption. The historical solver harness includes:
- P1 (`test_solver_integrity.py`): liveness (no dead DOF), provenance lint (no untagged physics
  literal), limit recovery (flat/Schwarzschild vacuum + de Sitter NORMALIZATION), native-object
  guard (no S^3 Skyrme import).
- P2 (`test_operator_from_action.py`): the live operator == the EL of `solver_action.py`.
Required checks must pass in their declared scope. An intentional documented gap remains unverified,
not a universal exemption. Catch-proof every new guard by reintroducing the defect and observing the
corresponding failure.

## Anti-import / anti-freeze checklist
- Every physics constant carries a tag: `# DERIVED | POSTULATED | FREE | IMPORTED`. No bare
  physics literal in the operator. Values are SOURCED (solver_action.py), never re-asserted in a test.
- No mechanism/coupling/term posited because it would help and then mislabeled derived. Conditional
  counterfactual branches are allowed only when the work order authorizes and labels them.
- No SM entity/analog imported as a label until the metric demands it (P3).
- Controlled approximations state expansion parameter, validity domain, error/convergence support,
  and inherited downstream limits. Exact first variations and linear stability are legitimate
  scoped results, not global nonlinear claims. A convenient truncated equation may not silently
  replace the admitted one.
- Bound the computation. A fixed-DOF or symmetry slice is allowed when declared and sufficient for
  the stated quantifier; it is not a whole-theory verdict.
- "chose or derived?" on every value/BC/sign/chart BEFORE use. "observing or targeting?" before
  every agent launch. A targeted bounded question is legitimate; hidden answer-fitting or discarding
  unwanted valid outcomes is not.
- Algebraic objects can be imports (cohomology / transfer-ladder / N=3-q=1/3 dressed as native).
  Audit native-vs-import provenance before banking mass/spectrum on one.
- Resource safety: use the current work order and measured environment to state process count,
  grid/iteration/memory/time budgets, output, checkpointing, and stop conditions. Keep one GPU
  process at a time; do not inherit obsolete filename lists or universal grid caps.
