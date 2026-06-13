# Whole-Metric Pinning — First Calculation of the Critical-Universe Frame

Date: 2026-06-13. Driver: Claude (Opus 4.8). Frame:
CRITICAL_UNIVERSE_FRAME.md. Declaration: W9 / the whole-metric solve.
Agent a5a4c7c001ca41275 (determinacy analysis, no shortcuts; scripts
in rescued_workspaces/w_whole_2026-06-13/: w_whole_pinning.py 10/10,
w_whole_modulus_hunt.py 3/3). Independent verifier PENDING (the
compactness claim below is HYPOTHESIS-GRADE until the general-member
calculation + blind pass).

## The question split into two axes (the key structural result)

"Does closing the whole metric PIN the critical configuration?" splits
cleanly:
- ABSOLUTE-SIZE axis: how big the universe is in meters/kilograms.
- COMPACTNESS / PARTITION axis: the dimensionless ratio
  X = 2GM/(c^2 r*), and the dimensionless structure (hence the wall
  RATIOS).

## Axis 1 — ABSOLUTE SIZE: SCALE-FREE (a family). THEOREM-GRADE.

Applying the global rescaling r -> lambda r, M -> lambda M,
t -> lambda t (c, G fixed; phi dimensionless) to EVERY closure +
regularity condition (center regularity, the Misner-Sharp/dilation
tie, the same-minus mirror-fold seal, the boundary closure incl. the
corrected Dirichlet+Neumann pair, finite action, the scalar EOM) —
all dimensionless closure quantities are rescale-INVARIANT; the only
covariant object is the overall scale lambda, which is UNFIXED. No
closure condition carries a length or mass standard. So with only c
and G, the absolute size is a PROVABLY FREE one-parameter family. The
absolute scale of the universe is one OBSERVATIONAL input — as in
every physical theory. (Charles's dimensional intuition confirmed:
the kilograms are not the fixed thing; the structure is.) The deep-well
horizon condition c^2 = 2GM/r* is itself scale-free — it RELATES M and
r*, fixing neither.

## Axis 2 — COMPACTNESS / PARTITION: plausibly PINNED to a DISCRETE
## set. HYPOTHESIS-GRADE (the bootstrap lives here).

The dimensionless compactness X is NOT fixed by rescaling — it is set
by the whole-profile closure, which is OVER-DETERMINED: outer
Dirichlet AND Neumann at r*, plus inner regularity, on the nonlinear
profile equation. An over-determined nonlinear BVP is a NONLINEAR
EIGENVALUE problem, which generically admits a DISCRETE set of
solutions, not a curve. On the one exactly-solvable member (f ~ 1/r,
w_alg), the closure is EXACTLY the Gelfand-Bratu fold s*tanh(s) = 1 —
a SINGLE ISOLATED ROOT (s* = 1.1997). So the dimensionless structure
(and hence the wall RATIOS) is plausibly pinned to a discrete set even
while absolute size stays free. This is the same Gelfand-Bratu
structure w_alg found inside a cell, now appearing as the WHOLE-
universe closure condition — a consilience. NOT the mode-spectrum/
box-control shortcut: it is the nonlinear closure of the whole static
profile being over-determined, like a fold, not a linear ringing mode.

CAVEAT (the soft spot, agent-flagged): the discrete-compactness claim
is FLAT-MEMBER-ONLY; w_alg flags f ~ 1/r as the unique exactly-
solvable scaling, so the single-root could be a member artifact. The
GENERAL-MEMBER eigenvalue count (is the closure a discrete set, or a
curve leaving X free?) is NUMERICAL and UNRUN — it is the precise next
calculation and the actual determines-vs-relates resolution.

## The 7.004 boundary value: FREE, not forced (at the size level)

phi* = -(1/2) ln(1 - X) is fixed entirely by the compactness X; no
closure condition fixes X to a number at the absolute-scale level. So
7.004 = ln(1+z_CMB) is currently an OBSERVATIONAL anchor, not a
closure prediction — UNLESS the Axis-2 discrete-compactness closure
forces X to specific values (then z_CMB would be predicted). That is
the same open calculation as Axis 2.

## Verdict and what it means for the frame

Charles's literal "one absolute universe" (a fixed number of kilograms)
is NOT delivered by c-and-G closure — absolute size is observational
(grading (ii) on that axis). But the bootstrap (a) is NOT refuted: it
MIGRATES to the compactness/partition axis and is alive there, as a
nonlinear-eigenvalue closure that plausibly discretizes the
dimensionless structure (the wall ratios). The physics is in the
dimensionless partition, pinned discretely by the whole closure;
the absolute scale is one observation. This is exactly the "structure
not the kilograms" reading, now with a mechanism for the discreteness
(over-determined whole-profile closure = nonlinear eigenvalue) that is
NOT a mode spectrum and NOT an added term.

## Next calculation (the actual answer)

THE GENERAL-MEMBER COMPACTNESS EIGENVALUE COUNT: on general (non-flat)
profiles, is the over-determined whole-profile closure a DISCRETE set
of compactness values (bootstrap (a) on the partition axis -> wall
ratios forced) or a CURVE leaving X free (relates only)? Numerical,
verifier-grade. This is what actually answers "does it pin." See
registry #32.
