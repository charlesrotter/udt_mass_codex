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

## Axis 2 RESOLVED (2026-06-13): GENERAL-MEMBER COMPACTNESS IS A CONTINUUM

Driver: GENERAL-MEMBER COMPACTNESS agent (Opus 4.8). Scripts (new, per
discipline): w_whole_gm_derive.py (2/2), w_whole_gm_scan.py (6/6),
w_whole_gm_hostile.py (8/8). Logs /tmp/w_whole_gm_*.log. Blind
adversarial verifier ab72b577c0c705d75 (independent machinery):
CONFIRMED. Declaration: METRIC-LED. Registry #33.

### The whole-profile ODE + closure count (step 1, exact)
The metric's own static scalar field equation IS the whole-profile ODE:
    Box phi = (1/r^2) d/dr( r^2 e^{-2 phi} phi' ) = 0
    <=>  r^2 phi'' + 2 r phi' - 2 r^2 phi'^2 = 0   (2nd order).
Full derived closure (nothing added): center regularity phi'(0)=0
(mirror-fold parity, cell owns its center); Misner-Sharp/dilation tie
m(r)=(c^2 r/2G)(1-e^{-2phi}) (defines X at the boundary); outer
Dirichlet phi(r*)=phi_*=-1/2 ln(1-X); outer Neumann phi'(r*)=0 (CR-87
pair, no third). OVER-DETERMINATION = +1 (2nd-order ODE; inner
regularity launches a 1-param family; outer end imposes TWO conditions).

### The decisive structure (step 2) and the verdict
The metric's geometric tie collapses general members to TWO whole-
profile classes (w_alg PART E, derived not added): rho=1 (f~1/r) gives
the autonomous Liouville member; rho!=1 gives the scale-invariant
Emden-Fowler member v_mm=Lambda m^{-2} e^{-2v}, which autonomizes in
tau=ln m to w'' - w' = Lambda e^{-2w} (the rescaling, Axis 1, divided
out). The OFF/vacuum single-exponential source e^{-2v} is MONOTONE: at
a Neumann node v_m=0, v_m'=+Lambda e^{-2v}>0 always, so v_m never
returns to 0 -> NO second Neumann node -> Neumann-Neumann closure EMPTY.
A closed two-node cell REQUIRES the ON two-exponential restoring source
v_mm=Phi(e^{-2v}-e^{v}) (first integral (1/2)v_m^2+(Phi/2)e^{-2v}+
Phi e^{v}=E; well U_min=3Phi/2 at v=0). EVERY bounded orbit (E>U_min)
has TWO turning points automatically -> the inner+outer Neumann
conditions impose NOTHING; the only residual condition (Dirichlet
depth) is a continuous bijection depth<->E. Therefore:

  *** A CONTINUUM of admissible compactness X closes -- ONE per E. The
      +1 over-determination is absorbed by the depth<->E relation, NOT
      by discretizing. The dimensionless compactness is NOT pinned by
      the (c,G) single-cell whole-profile closure alone. ***

### Hostile-continuum attempt + convergence (step 3) -- the continuum SURVIVES
Cell width L(E) and boundary depth v_max(E) are smooth, strictly
monotone over 59 energies spanning the whole well (desingularized
split-panel quadrature); small-amplitude endpoint L->pi/sqrt(3Phi)
confirmed analytically. CONVERGENCE: L(E=3,Phi=1)=1.67427938129 stable
to <1e-15 under quadrature-degree doubling AND reproduced to 9 digits
by an independent RK4 IVP (cross-method; no three-term extrapolation).
Free-function audit: E is the conserved partition energy (coordinate-
invariant amplitude), NOT the global rescaling (already divided out) and
NOT a parameterization freedom (m0=center fixed by parity). The
continuum is PHYSICAL.

### Reconciliation of the flat-member single Gelfand-Bratu root
The #32 "discrete" reading (s tanh s=1) was DIRICHLET-DIRICHLET at an
EXTERNALLY-FROZEN cell length M. In the whole closure the cell length IS
the compactness (free unknown); freeing M turns the isolated fold into a
continuous (M,s) curve (verified). The single root was a frozen-length
artifact, consilient with the general-member continuum.

### Verdict for the frame (honest, against the program-confirming hope)
Bootstrap (a) is NOT delivered by single-cell closure on EITHER axis:
absolute size scale-free (#32 Axis 1), compactness a continuum (#33).
The frame as currently closed RELATES X to the partition energy E but
does not pin it. #32's proposed discreteness mechanism (over-determined
single-cell nonlinear eigenvalue) is REFUTED as the source of
discreteness. 7.004=ln(1+z_CMB) stays an OBSERVATIONAL anchor (X free).
NO data-blind wall-ratio comparison is made (the discrete X set the
contract required does not exist at this closure level). Discreteness,
if real, must come from (i) an INTEGER CELL-TILING condition (the
partition picture: N identical critical cells tiling a closed universe
of fixed total extent T -> L=T/N discrete, integer N the label; needs T
fixed by an un-derived closure) or (ii) hbar entering the partition.
Neither is in the (c,G) classical single-cell closure.

### What a blind verifier should attack first (next pass)
The single load-bearing physical step is "the closed cell is the ON
two-exponential member, not the OFF vacuum" -- attack whether the
metric's own field content actually selects the ON (restoring) source
for the WHOLE closed universe (here taken from w_alg PART E, premise:
the ON-branch statics). Then attack the TILING redirect: is there a
derived closure fixing the total universe tau-extent T (which would
re-discretize X via integer cell count)? That is the sharp next object.
