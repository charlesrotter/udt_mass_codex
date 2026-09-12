# NTB1 discovery and numerical scope freeze

Before new numerical outcomes or reviewer findings. Parent knows G394/G415/G348
and NCR1 source results and standard Hamiltonian/variational mathematics.
No claimed blind rediscovery of those sources. No new external physics imported.

Explore a finite diagnostic grid: epsilon=0,1/2,1; source xi=0,0.7;
mu=-0.8,0,0.8; psi=0,pi/4,pi/2; endpoints t=2,8,20,40 on each ray.
Add exact-axis controls mu=+/-1 at epsilon=0,1/2, source xi=0.7.
Samples are numerical controls, not a typicality measure or a completeness proof.
CPU float64 SciPy DOP853, rtol=2e-10, atol=2e-12, max_step=0.2.
Save full states and variational matrices at declared endpoints. A sign change
is initially floating-point evidence only; any further selected bracket/refinement
will disclose discovery exposure and freeze its own check contract.

Use full reduced Hamiltonian h=sqrt(p_xi^2+N^2(p_y^2/b_y^2+p_z^2/b_z^2)),
its analytic Hessian, and the six-dimensional canonical first variation.
No small-angle or small-amplitude replacement metric. Infinitesimal beam maps
are exact derivatives, distinct from finite beams. Check null-screen orthogonality,
canonical symplecticity, source normalization, zero-amplitude quadrature and axial
G415 widths. These internal controls are not implementation independence.

Numerical acceptance controls: scaled screen orthogonality <=2e-7;
scaled symplectic residual <=2e-7; axial/zero-background relative discrepancy <=2e-6.
Scaled residuals accompany unscaled values; no residual proves infinite-time absence.
Freeze later finite-difference/reversal/observer/tighter-repeat selections explicitly.
All failures retained, no silently widened tolerances. Ordinary capture<=180s/2048MiB.
