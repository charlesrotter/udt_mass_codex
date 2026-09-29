# LKT1 exact-check plan

Pre-computation plan after algebraic exploration. CPU-only Python/SymPy,
60s/512MiB per run, one numerical thread, existing run_capture utility.
Exact residual zero or exact nonzero controls; no floating-point tolerance,
parameter fit, native model selection or numerical certification claim.

1. Preserve BOTH bilinear forms through the reciprocal-to-boost basis change.
   Catch silently identifying D with a physical eta-isometry.
2. Independently compute Christoffel symbols from the full triangular metric
   and convert to the coframe connection, comparing both components and all
   matrix entries with the proposed Cartan expression. Keep shift derivatives.
3. Compute curvature directly from Christoffel derivatives on a mixed t,x
   reciprocal metric, comparing its scalar with the connection curvature.
4. Check null contraction and the dynamic depth identity on both orientations,
   with nonzero time and spatial derivatives. Check static/time-only limits.
5. Independently differentiate a supplied null arrival map for T=1,L=1+t;
   verify ordinary proper clocks, Z=2 and nonzero comparison depth despite
   zero local-record depth. This is a supplied flat control, not native UDT.
6. Check Lorentz-generator commutators and a noncollinear direction-carrying
   frequency composition with exact rational boost matrices. Demonstrate that
   a deliberately omitted intermediate direction gives a different answer.

Wrong-form/sign/density/shift/direction controls are illustrative sensitivities,
not producer-mutation or exhaustive coverage. Mathematical arguments, domains,
source fidelity and reviews own theorem scope. Preserve failures/code revisions.
