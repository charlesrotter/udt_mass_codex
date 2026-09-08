---
name: solution-space-not-imposition
description: Use before any solve/result and when building or editing solver code. Stops the recurring drift from EXPLORING the metric's solution space to IMPOSING the physics we expect. The purity gate catches imports; this catches impositions — and the gate itself is constrained to never become a new imposition.
---

# Solution-space, not imposition (binding)

**The recurring drift (Charles, multiple times in ~2 weeks):** we slide from *building a solver to
EXPLORE the metric's solution space and see what emerges* to *IMPOSING the answer we expect* onto what
we build. The purity gate (`pytest tests/`) catches *imports*; nothing automatic catches *impositions* —
so we cross the line (legitimate numeric/theory input vs imposed physics motivation) without noticing.

**The simple goal (Charles 2026-06-25):** perform PURE MATH and explore the solution space for WHAT
EMERGES, which LATER we consider as physics. A solver computes the currently admitted equations with
numeric tools only. An action is load-bearing only when the task's premise ledger admits it; physics
never enters silently through an import, BC, ansatz, or acceptance test.

## The governing principle — PROVENANCE & HONESTY, never MERIT

Any gate, guard, lint, or diagnostic we build to enforce this discipline may check only:
- **PROVENANCE** — where did this come from? (Is this import a numeric technique, or a smuggled physics
  object/count/BC/mechanism? Is this value derived from the action, or pinned by hand?) Objective,
  decidable, makes **no physics judgment**.
- **HONESTY** — is every pinned choice tagged and surfaced so we can see it and choose to free it?
  Documentation, not a verdict. Makes **no physics judgment**.

It may not judge **AESTHETIC OR INTERPRETIVE MERIT** — whether a solution has the desired shape, looks
like a particle, or matches an expected answer. It may and should check **MATHEMATICAL VALIDITY** for
the claimed class: original-equation residuals, constraints, object type, boundary treatment, error
control, and claimed convergence. Smoothness is required only when the stated solution class requires
it. These distinctions are reviewed by a human because a label alone cannot certify honest use.

## The 4-point audit (run before banking any solve/result)

1. **ANSATZ / BC LEDGER.** Tag every boundary condition, matter-sector choice, coupling, and fixed value:
   - `free-and-explored` — scanned, not pinned.
   - `pinned-by-THEORY` — fixed, WITH a citation to the derivation/action/canon. (No citation ⇒ not this.)
   - `pinned-by-HABIT` — fixed with no theory behind it = a **drift flag**. Justify (→ theory) or free it.
   A pin with no tag, or a habit-pin left unjustified, fails the honesty check.

2. **ACCEPTANCE-CRITERION AUDIT — validity, then characterization.** A certification test may reject a
   claimed numerical solution for invalid residuals, constraints, object type, boundaries, error
   control, or convergence. Preserve the run as diagnostic evidence. Do not discard a mathematically
   valid member merely because its appearance or interpretation is unwanted; characterize it.

3. **QUESTION AUDIT — observing, targeted, or answer-fitted?** A question about a phenomenon,
   symmetry sector, witness, or counterexample is legitimate. State the quantifier, restrictions, and
   retained degrees of freedom. Reject hidden answer-fitting, outcome filtering, or a template silently
   promoted to UDT physics; do not reject a bounded question merely because it is targeted.

4. **QUANTIFIER AND COVERAGE.** One valid witness establishes scoped existence; one valid
   counterexample refutes a universal claim. Uniqueness, typicality, nonexistence, and completeness
   need broader arguments. Report only the census required by the actual claim; a finite failed search
   is not nonexistence.

## What the machine enforces (and what it deliberately does not)

`pytest tests/` adds two PROVENANCE/HONESTY lints (`test_solution_space_gate.py`) — physics-blind, can
never grow into a merit check:
- **Numeric-only imports** — every import in the solver graph is a numeric technique (numpy/torch/scipy/
  benign stdlib) or a *registered* project module classified `numeric-method` / `action-EL-derived`. An
  unregistered project import or an unknown third-party import fails: it forces a provenance decision.
- **Premise tags** — pinned values/BCs/ansatz carry a provenance tag (extends the P1 constant-provenance
  lint). Surfacing, not forbidding.

The machine does not infer physical merit, intent, or a completeness theorem. It may enforce declared
provenance and numerical-certification contracts. Human review checks whether the contract answers the
stated quantifier without hidden fitting or generalization.

See [[solution-space-not-imposition]], [[how-we-work-method]], [[solver-first-not-mechanism]].
Companion gates: `no-shortcuts` (anti-import/anti-freeze + purity harness), `verifier-before-record`,
`completeness-map`, `solver-first`.
