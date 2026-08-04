# RAM-aware exploration program

## Scientific success criteria

A phase succeeds when it does one or more of the following within its preregistered scope:

- covers a stated configuration family;
- derives a new identity or incompatibility from the metric;
- reduces an open degree of freedom without importing a physical premise;
- supplies a constructive witness or certified obstruction;
- identifies the exact additional datum or law required for the next phase.

Wall time, RAM use and solver completion are operational observations only. A stopped computation is
not a negative physics result. A fast computation is not evidence of physical relevance.

## Phase A — factorized whole-spacetime skeleton

**Mode:** CPU, symbolic, sparse, no solve.

1. Define the complete object graph described in `SPACETIME_MODEL_OBJECTIVES.md`.
2. For each symbol, record type, dimension, chart behavior, gauge action, provenance and whether it is
   free, identity-constrained, law-constrained or open.
3. Express the coframe and connection in blocks/exterior forms. Do not expand determinants,
   curvature components or polynomial ideals globally.
4. Separate four lists: definitions, identities, conditional equations and absent equations.
5. Demonstrate reduction to the already audited stationary/general-screen and reciprocal-pair
   branches.

**Stop condition:** a one-to-one accounting of all complete-coframe slots and every missing equation
slot. No selection claim is permitted.

## Phase B — branch and transition completion

**Mode:** exact special anchors plus sparse numerical continuation.

1. Choose complete branch representatives from the existing atlas without privileging a desired
   physical outcome.
2. Compute local Jacobian ranks, transition compatibility and degeneration surfaces in factorized
   form.
3. Continue one coherent family at a time with checkpoints and branch-event detection.
4. Preserve all branches, including singular, disconnected and non-particle-like outcomes.

**Stop condition:** branch coverage or a documented coverage boundary. Do not demand a single branch.

## Phase C — native-law search on the correct domain

**Mode:** premise audit first; bounded symbolic tests second.

1. Ask whether the complete metric supplies a covariant response, constraint or global-local
   operation on the Phase-A object graph.
2. Test covariance, locality/nonlocality, variation domain, boundary integrability and closure without
   presupposing an action.
3. Only if a response one-form is actually obtained, test whether it is variational and whether an
   action can be reconstructed.
4. Keep EH, Bach and carrier actions as conditional comparison lanes.

**Stop condition:** either a derived bounded response operation or an exact statement of the smallest
additional premise needed. “The CAS did not finish” is never a stop conclusion.

## Phase D — time-live system

**Entry gate:** Phase C must identify evolved variables, native equations, constraints and boundary
posture.

1. Derive CPU algebraic and ODE anchors first.
2. Check constraints, characteristic structure, conserved identities and raw residuals.
3. Use GPU continuation only after the equations and falsification contract are frozen.
4. Save checkpoints and raw fields; use one GPU process; preregister memory and stop thresholds.

**Stop condition:** coverage and numerical certification, not a desired waveform or lump.

## Phase E — global readout and bootstrap

**Entry gate:** native global observables and a return operation must be type-correct.

1. Define the observer-pair path/domain functional before evaluating `Xmax`.
2. Define native mass/energy/global curvature variables before bracketing density.
3. Scan broad ranges without fitting a desired answer; record branch births, mergers, singularities
   and admissible windows.
4. Compare completed survivors with SNe, BAO or CMB only as observational readouts.

## Phase F — conditional and emergent matter

1. Propagate each completed background branch into every relevant conditional matter family.
2. Keep the `S^2`/`L2+L4` Hopfion lane explicitly premise-stamped.
3. Test whether any Layer-3 law derives a carrier, source or persistence condition.
4. Do not promote geometry-only mass-bearing witnesses into stable matter.

## Representation and resource rules

- Prefer coframes, exterior forms, block matrices, sparse graphs and invariant subspaces.
- Factor before expanding; eliminate only the variable needed for a registered decision.
- Use local rank tests and exact special points before Gröbner bases.
- When exact elimination is unavoidable, use modular probes only as probes, estimate basis growth,
  checkpoint if supported, and preregister a hard memory ceiling.
- A memory ceiling protects the workstation. Reaching it returns `INCOMPLETE-COMPUTATION`, not a
  scientific class.
- Prefer independently coded residual checks to a second run of the same expansion.
- Defer C08 reverse containment until it becomes load-bearing for a branch decision; it currently is
  not.

## Recommended next dispatch

Preregister and execute Phase A only: the factorized whole-spacetime skeleton and identity/law
separation audit. It should be a small CPU/symbolic task and should stop before selecting or solving a
native dynamical law.
