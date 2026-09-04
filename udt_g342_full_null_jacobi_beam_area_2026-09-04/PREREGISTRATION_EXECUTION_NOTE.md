# G342 preregistration execution note

Date: 2026-09-04

The first post-preregistration production run passed every geometric, fixed-affine, positivity,
expansion, shear, longitudinal-limit, and Jacobi-equation check, but failed three of 80 finite
transverse-axis approximation checks. The largest finite-axis difference was
`2.3418956002921627e-08` at `lambda/T_e=1e5`, against a code threshold of `2e-8`. The actual
Jacobi-equation residual was `8.339259594284873e-16`. The implementation-distinct direct-metric
curvature and RK Jacobi replay passed all 2,080 assertions, with maximum curvature error
`8.139322549283179e-15` and map error `4.0420728509142683e-11`.

This is a chart-boundary approximation miss, not a changed scientific outcome. The exact
transverse-limit formulas were preregistered as required output. Before accepting production, move
the finite check from `lambda/T_e=1e5` to `1e6`, where the analytic finite-parameter error is
`O(lambda^-2)`, and require the original preregistered raw tolerance `5e-9`. No formula, sample,
alternative, sign criterion, or scientific landing is changed. Preserve this initial miss in the
banked evidence.
