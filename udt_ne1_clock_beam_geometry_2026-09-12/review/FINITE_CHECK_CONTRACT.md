# Direct-stage independent finite check freeze

2026-09-12, after INITIAL_CANDIDATE equations (1)–(14) exposure. Before any
new finite numerical execution. Source-first argument/checks remain sealed.

Independently implement the exact supplied metric first jet. Build all
Christoffels from diagonal-metric derivative arrays, integrate the complete
eight-dimensional position/tangent null-geodesic ODE at fixed central affine
endpoint, and perturb both source-sky directions. Compare its differential
with independently written candidate quadratures. This does not import any
parent script, curvature helper or previous package scientific implementation.
The SciPy Bessel/ODE library is shared technology, not a different-library
claim. The full perturbed nonlinear geodesic route is distinct from direct
integration of the proposed scalar Jacobi equations.

Six predetermined (epsilon, t_e, xi_e, sign, length) tuples:
(0,0.4,0.3,+1,0.6), (1/6,0.4,0.3,-1,0.6),
(-0.5,1.4,-0.7,+1,1.1), (1.2,1.4,0.2,-1,0.8),
(0.5,2,0.7,-1,2), (-1/6,3,-1.2,+1,0.9).
All coordinates in the supplied NE1 normalization; no new physical literal.

Use SciPy DOP853 rtol=2e-12, atol=2e-13, central affine quadrature epsabs=
epsrel=2e-12. Sky angle offsets {0.002,0.001,0.0005}; keep all errors.
Require finest differential mixed-scaled error <2e-6, coarsest-to-finest
error reduction >8 when coarsest error >1e-8, direct null residual <2e-9,
and central (t,xi) endpoint mixed-scaled error <2e-10. The convergence
criterion is conditional on resolved truncation, not fake precision.
Independently compute the clock slope from short proper-time integrals at
fixed endpoint worldlines with half-width 1e-5; error threshold 2e-9.
No tolerance/sample change after outcomes without retained diagnostic.

CPU only, <=180 s, 2048 MiB, one library thread via existing capture utility.
No claim of interval certification, arbitrary-amplitude numerical coverage,
infinite-time proof, finite physical beams or physical ray selection.
