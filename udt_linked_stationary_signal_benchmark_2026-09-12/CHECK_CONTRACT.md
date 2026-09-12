# LSB1 finite numerical and exact-check freeze

Frozen before parent scientific numerical outputs. No desired sign or success
is assumed. INITIAL_CANDIDATE.md is the mathematical candidate; these checks
cannot replace its argument or independently certify all its hypotheses.

FREE supplied examples: the Cartesian product a=(-1/500,0,1/500),
b=(-2/5,0,2/5), nine metrics on K=[3/2,10]. The elementary lower bound
f>=1-(1/500)100-(2/5)/(3/2)=8/15>1/2 certifies positivity over ALL K for
these examples without a grid. This is a chosen scale-free diagnostic set,
not a fit or a claim of typicality. L/c_E is left symbolic; report dimensionless
time tau*c_E/L. Clock calibration radii (2,4,8); signal endpoints (6,8),
angular separation 2 radians. The additional R_6,8 and chi clock leg are unused
readouts. No actual physical data or claimed observational uncertainty.

Branch search: turning radius p in [1.6,5.5], strictly below both endpoints.
The exact J_x form and b/p>=-1/4 give J_x>=1-(1/4)3=1/4 for every
0<=x<=1, so the positive simple-turn branch integrands are regular here.
Require a root sign bracket, root residual <=2e-10 and domain conditions.
Root selection is this bracket/one-periapse branch; no general uniqueness or
multiple-path claim. All nine examples and any failure remain in saved output.

Method: NumPy/SciPy FLOAT64, Brent root and transformed adaptive quadrature
from candidate (10); base epsabs=epsrel=2e-11, Brent xtol=2e-12,
rtol=2e-14, quadrature limit100. Repeat all nine at epsabs=epsrel=2e-12,
xtol=2e-13, rtol=2e-14. Require scaled output changes <=2e-9;
record actual quadrature error estimates, roots, R, delta, chi, angle, time
and flat contrasts. QUADPACK errors and tighter-repeat agreement are floating
point support, not rigorous interval certificates. Treat nonfinite results,
solver failure or IntegrationWarning as diagnostic failure, not class rejection.

Exact anchors: rational coefficient recovery for the nine examples, symbolic
determinant identity, chi=tanh(-log R) algebra expressed rationally via q,
turning transformation identities and local angle derivative. Confirm flat
root/duration/angle against the Euclidean chord formulas (scaled error <=2e-10).
Confirm a-independence of coordinate orbit at fixed b and the strict sampled
angle response in a. Analytic equation (11), not this grid, owns the general
strict derivative. Clock/pair reversal is a source-owned algebra regression.

Catch-proof three newly load-bearing guards by separate no-overwrite runs:
invert the clock ratio in calibration; drop the receiver lapse in the local
sky angle; drop the emitting-clock lapse in round-trip time. Each corresponding
guard must fail at exit1. Preserve every stdout/stderr, command, versions and
resource receipt. No source files are modified to inject defects.

Independent review rederives a load-bearing quantity with separate code/method
and examines the proof and unused-output contract. It need not replay unrelated
historical field solvers. It reports numerical limits and exposure separately
from source-first analytic agreement and final direct review.

Resources: existing capture utility, CPU single library thread, <=180 seconds
and <=2048 MiB per ordinary run. Parent full398 verifier completes BEFORE parent
numerical execution. Candidate and code hashes precede the outcome runs. No
scientific tuning after seeing outputs; any necessary repair preserves the
initial version and documents defect, reason, survivor and bounded correction.
