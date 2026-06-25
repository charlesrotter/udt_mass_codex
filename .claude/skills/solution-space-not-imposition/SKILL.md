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
EMERGES, which LATER we consider as physics. The solver computes the action's Euler–Lagrange residual
with numeric tools only; physics lives in the action, never in an import, a BC, or an acceptance test.

## The governing principle — PROVENANCE & HONESTY, never MERIT

Any gate, guard, lint, or diagnostic we build to enforce this discipline may check only:
- **PROVENANCE** — where did this come from? (Is this import a numeric technique, or a smuggled physics
  object/count/BC/mechanism? Is this value derived from the action, or pinned by hand?) Objective,
  decidable, makes **no physics judgment**.
- **HONESTY** — is every pinned choice tagged and surfaced so we can see it and choose to free it?
  Documentation, not a verdict. Makes **no physics judgment**.

It may **NEVER** check **MERIT** — is this solution the "right" shape, smooth, a lump, convergent, the
expected answer? The moment a check judges merit, it becomes a blocker that imposes physics, and that
judgment (written by a possibly-drifting AI) accumulates into inappropriate blockers — the very failure
we are fighting. **Merit is judged LATER, with Charles.** A proposed check that would throw a class of
solutions away on physics grounds is itself an imposition and is forbidden. This limit is enforced by
hand (Charles / verifier) when reviewing any new check — deliberately NOT by a machine meta-test, because
a label is satisfiable by a drifting author while a binding principle is not.

## The 4-point audit (run before banking any solve/result)

1. **ANSATZ / BC LEDGER.** Tag every boundary condition, matter-sector choice, coupling, and fixed value:
   - `free-and-explored` — scanned, not pinned.
   - `pinned-by-THEORY` — fixed, WITH a citation to the derivation/action/canon. (No citation ⇒ not this.)
   - `pinned-by-HABIT` — fixed with no theory behind it = a **drift flag**. Justify (→ theory) or free it.
   A pin with no tag, or a habit-pin left unjustified, fails the honesty check.

2. **ACCEPTANCE-CRITERION AUDIT — characterize, don't filter.** Does the guard/diagnostic *FILTER* the
   space (demand a shape, smoothness, convergence, a lump, the expected answer — and call everything else
   "failure")? If so it is an imposition. Reframe it to *CHARACTERIZE*: report what the math did
   (floored / diverged / horizon / box-controlled / multi-branch) and let the solution stand. A real
   horizon is a result, not a failure. Never let an acceptance test discard a solution.

3. **QUESTION AUDIT — observing or targeting?** State the question and check it against the SM-template
   list: **lump / mass / particle / spectrum**. If the question is "is there a localized particle/mass?"
   you are targeting an imported template, not observing what the metric does. (Caught twice: lump→charge;
   "are we imposing?") Reframe to "what solutions exist here, and how do they classify?"

4. **SOLUTION-SPACE COMPLETENESS.** Did we CLASSIFY the solutions present in the regime, or just find the
   one we went looking for? Finding the sought solution is not exploring the space. Report the census.

## What the machine enforces (and what it deliberately does not)

`pytest tests/` adds two PROVENANCE/HONESTY lints (`test_solution_space_gate.py`) — physics-blind, can
never grow into a merit check:
- **Numeric-only imports** — every import in the solver graph is a numeric technique (numpy/torch/scipy/
  benign stdlib) or a *registered* project module classified `numeric-method` / `action-EL-derived`. An
  unregistered project import or an unknown third-party import fails: it forces a provenance decision.
- **Premise tags** — pinned values/BCs/ansatz carry a provenance tag (extends the P1 constant-provenance
  lint). Surfacing, not forbidding.

The machine does **NOT** judge filter-vs-characterizer, observe-vs-target, or completeness — those are
points 2–4 above, applied by a human in `verifier-before-record`, because a machine judging them would be
judging merit. The gate's only job is to make impositions *visible and traceable*; deciding they are
acceptable is human, and happens LATER.

See [[solution-space-not-imposition]], [[how-we-work-method]], [[solver-first-not-mechanism]].
Companion gates: `no-shortcuts` (anti-import/anti-freeze + purity harness), `verifier-before-record`,
`completeness-map`, `solver-first`.
