# WINT — The Interacting-Whole Solve: PRE-REGISTRATION

Date: 2026-06-13. Driver: Claude (Opus 4.8), INTERACTING-WHOLE agent.
Frame: CRITICAL_UNIVERSE_FRAME.md (governing). Declaration: METRIC-LED
("what structures does the two-way interacting metric+matter produce?").
This file is committed BEFORE any wint_*.py runs. Append-only.

## Charles's instruction (verbatim register, not re-framed)

"Compute the solution space of the WHOLE metric and analyse what
structures form." "The geometry more likely forces the TYPES of lumps."
It is NOT the metric on a FIXED matter background — it is "how the metric
and matter INTERACT" (two-way, self-consistent). Solve and LOOK; impose
nothing.

## The forbidden moves (the driver kept making these; this push does NOT)

1. NO determinacy/counting (no conditions-vs-parameters, no "does it pin
   one universe"). 2. NO imposed discreteness mechanism (no integer
   tiling, no mode spectrum, no quantize, no eigenvalue ladder).
3. NO frozen background (no frozen-f, no fixed/scanned matter shape;
   metric and matter ITERATE to mutual self-consistency). 4. NO added
   terms (no W_wave, no stiffness, no D_cell, no kappa, no beta — the
   bare metric the theory has). 5. NO slaving the angular sector (both
   radial-phi AND angular live).

## The system (exact; nothing added) — stated before running

The metric IS primary and GENERATES the dilation field f = e^{-2phi}
(critical-universe frame). The matter-energy content the metric carries
is the Misner-Sharp mass, read off the metric itself:
    m(r) = (c^2 r / 2G) (1 - e^{-2 phi})            (MS/dilation tie)
The dilation field's OWN stress-energy is what curves the metric — the
two-way tie is self-referential through f = e^{-2phi}: phi sets the
metric, the metric's propagation operator carries the e^{-2phi} weight,
and the MS mass it generates is the matter the metric holds. The metric's
own field equation (the C1 dilation action L_C1 = (c/2) e^{-2phi}
g^{ab} phi_a phi_b sqrt(-g), c=2, taken EXACTLY, no kappa/beta) is, in
the full (r,theta) geometry with BOTH sectors live:
    Box_g phi = (1/sqrt(-g)) d_a( sqrt(-g) g^{ab} e^{-2phi}? ) ...
the derived static equation (w_whole step 1, exact, nothing added) on
the spherical sector is
    Box phi = (1/r^2) d_r( r^2 e^{-2phi} phi' ) = 0,
and with the angular sector LIVE (theta-dependence retained, not slaved)
the WHOLE static field equation is the 2D dilation Laplacian
    (1/r^2) d_r( r^2 e^{-2phi} phi_r )
      + (1/(r^2 sin th)) d_th( sin th e^{-2phi} phi_th ) = 0.
This is the metric's own geometry, unreduced, both sectors co-equal.
The "two-way" loop: solve this nonlinear PDE for phi (the e^{-2phi}
weight is phi-dependent -> the operator depends on its own solution),
ITERATING the weight to self-consistency (Picard/Newton on the full
e^{-2phi} coefficient), reading off the MS mass at convergence. The
matter (MS mass distribution) and the metric (phi) are mutually
determined — neither frozen.

## What "a structure / a type" IS (operational, pre-stated)

A STRUCTURE = a converged self-consistent solution phi(r,theta) of the
2D interacting field equation that PERSISTS (the Picard/Newton iterate
converges to a fixed point to tol, residual of the full nonlinear PDE
< 1e-8, and the solution is regular on its domain). A TYPE = a class of
such solutions distinguished by an invariant character (shape; angular
content; the MS-mass profile; the internal geometry/curvature class;
whether it is round or shaped). Two converged solutions are the SAME
type if one maps to the other under the metric's own continuous
symmetry (global rescaling r->lambda r, the Axis-1 scale freedom);
DIFFERENT types if no such map exists.

## Domain / scope (pre-stated, honest)

The FULL domain to the seal (f->0) collapses computationally (known
fact, w_whole/W-series). The interacting solve is done on the INTERIOR /
trust-window region where the two-way iterate is well-posed and
converges; the scope of every reported structure is recorded. This is
the genuine two-way problem W5/W8 only did on trust windows with ADDED
terms — here with NO added terms, iterated to self-consistency.

## Possible outcomes (pre-registered; whichever is honest gets reported)

(O1) ONE type: a single class of converged self-consistent lump, the
     rest being rescalings of it (a smooth one-parameter family of one
     type). (O2) A FAMILY: a continuum of one type parameterized by a
     genuine free datum (e.g. partition energy E), no internal
     distinction. (O3) SEVERAL DISTINCT TYPES: two or more classes not
     related by the metric's symmetry, distinguished by angular content
     / shape / MS-mass character. (O4) NOTHING STABLE: no converged
     persistent self-consistent solution on the trust window.

## Procedure

- wint_system.py: encode the system, verify the field equation is the
  metric's own (cross-check against w6_arm1_lib geom engine and the
  w_whole spherical reduction); assert-laden; exact spherical reduction
  recovered. SPHERICAL exploration: solve+iterate the radial interacting
  equation across genuine free data (total MS energy / boundary depth),
  characterize the converged solutions (THE radial structures).
- wint_angular.py: turn the angular sector ON (2D PDE, theta-live, NOT
  slaved); solve+iterate to self-consistency on the trust window across
  free data AND angular content; characterize what converges. Does the
  angular sector produce DISTINCT types (shaped vs round) or only
  dress the radial family?
- wint_classify.py: characterize the converged set — types, invariants
  (shape, angular q/N if any emerges natively, MS mass, curvature
  class). Mass RATIOS data-blind FIRST; wall note only after.
- Convergence evidence MANDATORY for anything reported as a structure
  (residual decay, grid/iterate refinement, cross-method). Logs
  /tmp/wint_*.log. Checkpoint. HYPOTHESIS-GRADE on all results.
- A blind verifier attacks: (i) is the encoded equation REALLY the
  metric's own (no smuggled term)? (ii) is the iterate genuinely
  two-way (weight updated, not frozen)? (iii) are the "types" real or
  rescaling/discretization artifacts? (iv) convergence honest?

## Banked constraints carried (premise-scoped, do not re-derive)

- Axis-1 absolute size is scale-free (theorem, registry #32): types are
  characterized by RATIOS/shape, not kilograms.
- The spherical bare static field equation gives a CONTINUUM (one per E)
  (registry #33). This push asks the question registry #33 did NOT: with
  the ANGULAR sector LIVE and matter interacting two-way, what TYPES of
  lumps form? (Not "does it discretize" — "what structures are there".)
- Data-blind wall numbers (only after blind characterization):
  C_M1=0.977679087638, C_E1=1.93121474779, ratio=1.97530536575.
