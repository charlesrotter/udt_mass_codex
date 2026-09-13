# One independent exact geometry anchor

Frozen before implementing/running this check. Question: on an explicit smooth
full metric in geodesic normal coordinates, does the exact density-separation
Hessian equal minus one third of Ricci computed directly from Christoffel
derivatives, with mixed and off-diagonal components retained? This is a
mathematical check of the chosen definition, not physical premise verification.

Metric-led local diagnostic arena: g_ab(x)=eta_ab+sum_r c_r (F_r x)_a(F_r x)_b,
where each F_r is an explicit antisymmetric rational matrix. The Gauss identity
g_ab(x)x^b=eta_ab x^b holds, so RF1's retained argument makes x genuine normal
coordinates. Lorentz regularity holds near zero. This is a freely explored
supplied witness, not a physical solution ansatz, admitted native history,
finite search/classification or completeness claim. F_r, c_r and reporting
frame are free-and-explored diagnostics, not physical constants. No new fields.

Use Python standard-library Fraction exact arithmetic. Compute the full 4 by 4
determinant polynomial along v=q w by summing all 24 permutations, extracting
the quadratic log-density coefficient without using the author's h2(Ric)
substitution. Reconstruct the symmetric Hessian by polarization. Independently
compute Christoffel first derivatives directly from explicit metric second
derivatives, then contract the curvature definition for Ricci at the origin.
Compare all 16 components for one mixed fixture and one flat normalization.
Retain at least one nonzero quartic determinant coefficient to show the density
contains higher separation data; do not infer that Ricci-flat finite-volume
distortion is proved by this fixture. No solver, symbolic library or author code.

CPU only, no GPU, one scientific process; parent yielded exclusive slot. Limit
120 seconds and 2048 MiB address space, small JSON/stdout files in FE1/reviews.
No grid, relaxation, fit, tolerances or floating arithmetic. Stop on any exact
mismatch, exception, timeout or resource limit; preserve failures without repair
until diagnostic review. Max claim is one independent exact witness check plus
its finite algebraic mechanism, not original-science reproof or a physical law.
