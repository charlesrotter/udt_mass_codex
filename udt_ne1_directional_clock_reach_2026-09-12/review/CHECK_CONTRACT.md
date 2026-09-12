# Reviewer finite check contract

Source-first written before new numerical outcomes, 2026-09-12. The analytic
candidate is SOURCE_FIRST_RECONSTRUCTION.md. Full NE1 metric, t_e=1, common
sky and unit initial frequency. Controls are free-and-explored illustrative
values, not selected physics or typicality. CPU float64, one library thread,
one scientific child process in this context, <=180seconds and2048MiB through
the unchanged capture_existing.py wrapper. No GPU or production grid.

One independent implementation will construct the original diagonal metric,
its first derivative arrays and Christoffels, then integrate all spatial
coordinate slopes plus log(k^t) using t as parameter. A second implementation
uses reduced rapidity (A), only for nonaxial q>0. Both retain both transverse
axes and exact P/lambda. They share source formulas/SciPy, but the geodesic
connection and reduced equations are independently assembled. This is not
independent reproof of the admitted metric or a different-library check.

Eight fixed cases (epsilon, xi_e, normalized sky, t_o):
(0, .2, [.8,.6,0],20),
(.4,.2,[.8,.6,0],80),
(-.4,.7,[-.8,0,.6],80),
(.4,1.1,[.6,.48,.64],120),
(1.2,.3,[-.6,.48,-.64],30),
(.4,0,[0,1,0],80),
(.4,2pi/3,[0,1/sqrt(2),1/sqrt(2)],80),
(.4,.2,[sqrt(1-.01^2),.01,0],80).
End-point and129 evenly spaced intermediate outputs. DOP853 baseline
rtol=2e-10, atol=2e-12, max_step=.2. Reduced comparison rtol=2e-11,
atol=2e-13, max_step=.1. Finite verification thresholds: maximum scaled
frequency/xi discrepancy <2e-7; original null constraint relative error
<2e-7; conserved transverse momenta absolute error <2e-7. Zero-amplitude
analytic frequency and two exactly invariant equatorial controls checked
to2e-7. Repeat the largest-discrepancy case with original-connection
rtol=2e-12, atol=2e-14, max_step=.1; require error <2e-8 and less than
baseline error plus2e-10. No fine-to-coarse ratio claim when solver noise
dominates. Save all outcomes and failures; repair only after a labeled
diagnostic supplement.

Hostile variants: the independent connection integrator can suppress all
lambda-response derivatives/values or invert its frequency readout. Apply
the same baseline discrepancy assertions, require actual exit1 failures,
and save outputs. Failure names alone are not a guard. These controls do
not prove all possible errors detectable. Additional large-t finite examples
are optional only after a separate frozen supplement; no sampling proves
the analytic limits. Direct parent attack/replay follows explicit invitation.
