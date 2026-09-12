# NCR1 numerical and check contract — before parent outcomes

CPU float64, SciPy DOP853, exact Bessel coefficients from G394; one library
thread, <=180seconds/2048MiB per capture. These are numerical controls, not
physical choices. The finite calculations support implementation, not the
infinite-time proof or an interval certificate. Initial candidate plus the
credited source-first addendum are the mathematical claim under review.
No new parent numerical outcome has been observed at this freeze.

Parent implementation integrates exact (ξ,η,log ω). The first two use the
metric-derived Hamiltonian/rapidity equations; the last uses the original
metric clock-transport contraction. Compare the integrated log ω against
the conserved-transverse-momentum reconstruction. Shared metric/special-
function code means this is consistency, not a separately implemented proof.
The fresh reviewer independently reconstructs original Christoffels and
full nonaffine geodesic transport; its checks have their own exposure record.

Finite grid: epsilon=(0,1/6,-1/6,1/2), μ=(-0.8,0,0.8),
ψ=(0,π/4,π/2), ξ_e=(0,0.7), reception=(2,8), t_e=1:
144 fixed cases, both signs, both transverse axes, mixtures and equator.
Use rtol2e-10, atol2e-12, max_stepπ/(8k); test log-frequency reconstruction
error<=2e-7, exact zero-amplitude clock error<=2e-7, invariant equatorial
control<=2e-7, and finite bound (6) with2e-7 slack in log form.

Long-reception illustrations: epsilon=(1/6,1/2), initial sign=(-1,1),
tilt from that axis=(0.4,0.04,0.0004) radians, ψ=π/4, ξ_e=0.7;
12 exact finite-tilt rays, sampled at t=(10,40,100,400,1600), with the same
tolerances/max_step. Record R, correct same-direction R0, contrast,
η/ξ, integrated/reconstructed frequency discrepancy, (6)'s bound, log
contrast/t and log contrast/log t. No fit, numerical assertion of the
asymptotic exponent, or inferred sharp angular threshold. Axial G415 values
at the same marks are explicitly labeled controls.

Convergence support: repeat the largest finite reconstruction discrepancy
and the specified long case epsilon1/2, negative sign, tilt0.04 at
rtol2e-11, atol2e-13, half max_step, independently comparing recorded
log ω and ξ to the original run with mixed scaled error<=2e-6.
If this fails preserve it and freeze a bounded diagnostic before repair;
do not relax the tolerance simply to pass. No finite solver convergence
claim beyond these repeats.

Actual hostile runs, each must exit1 with the named scientific check:
drop the b_ξ term from rapidity evolution (clock transport); freeze the
quadratic λ derivative response in rapidity evolution (clock transport);
substitute the axial background at nonzero tilt (zero-amplitude recovery).
Save full failed stdout/stderr and execution receipts. Baseline replay must
be byte-identical for scientific stdout; this is regression only. Source
hashes/guard pass counts are correspondence, not truth or independence.

The full current398 audit has a separate900second/2048MiB capture. At closure
authenticate its input correspondence and the unchanged registry; run only
the relevant existing navigation tests after any compact pointer edits.
Do not rerun the full audit merely to turn later prose into its earlier inputs.
