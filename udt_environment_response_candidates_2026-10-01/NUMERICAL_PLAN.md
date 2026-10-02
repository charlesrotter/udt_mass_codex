# ERC1 fixed short-check plan

This plan fixes equations/cases/tolerances before numerical outcomes. Parent
already derived INITIAL_DERIVATION and knew standard f(R) results; this is
mathematical exploration followed by a frozen diagnostic, not blind observation.
No data fitting or cosmological dataset enters. Scientific code is frozen before
execution; repairs preserve original code/outputs and cannot change physics or
tolerances merely to pass. Use existing TPS1 capture,2GiB/no time cutoff, CPU only.

## Exact and weak controls

Symbolic checks: modulation identity; full trace-free B form; scalar trace;
original FLRW00/spatial components and constraint propagation; local cubic Taylor
coefficients; full static linearized exterior tensor equations with both potentials.
Check alpha=0 separately and retain F=0 caveats; no division there.

Weak example: alpha=1 in chosen length units, mu=1/5,A=1/10, r in[1,4],
epsilon in{1/16,1/32,1/64,1/128}. The scalar radial branch is decaying, an explicit
boundary choice, not a native physical rule. Actual supplied weak-metric clock
ratios use r_e=1,r_o=2; immediate stationary echo must invert. Bound the log-clock
Taylor remainder from the exact lapse expression and verify O(epsilon²).
No physical matter source or relation of mu/A to mass is assigned.

## Evolving cases

Use alpha=1 (positive-alpha unit representative), a(0)=1,eta(0)=0, t in[0,6].
Given Lambda,R0,P0, choose H0 from C=0. Unless specified otherwise, use the
nonnegative root of3F H²+6alpha P H-(alpha R²/2+Lambda)=0. Eight cases:

| id | Lambda | R0 | P0 | H branch |
|---|---:|---:|---:|---|
| flat | 0 | 0 | 0 | 0 |
| constant_positive | 1/100 | 1/25 | 0 | nonnegative |
| positive_curvature | 0 | 1/10 | 0 | nonnegative |
| negative_curvature | 0 | -1/10 | 0 | nonnegative |
| positive_offset | 1/100 | 7/50 | 0 | nonnegative |
| negative_offset | 1/100 | -3/50 | 0 | nonnegative |
| contracting | 0 | 1/10 | 0 | negative |
| flat_event | 0 | 0 | 3/100 | 0 |

The alpha<0 growing homogeneous linear curvature mode is checked analytically,
not a finite negative-alpha survey. Both signs of initial R and a contracting
control are retained; positive redshift is not an admission/pass gate.

Short actual-workload smoke: flat_event at the middle tolerance through t=1,
one clock distance L=1/4, and readable saved states/metrics/receipts. Check
original equations with the same residual machinery, initial constraint,
null/clock outputs, manual stop/domain events, output shape and refinement path.
This is a seconds/minutes ODE job, not production or restartable multi-hour work.
If smoke passes, run the fixed eight cases at three solve_ivp DOP853 settings:
(rtol,atol,max_step)=(1e-9,1e-11,.1),(1e-11,1e-13,.05),(1e-13,1e-15,.025).
No adaptive case hunting; save every case/setting including domain stops.

Domain stops (engineering controls, not physical boundaries): a<=1/4,F<=1/4,
or |H|,|R|,|P|>=2. An early stop is recorded and excludes claims beyond it; it
does not reject the candidate or prove a singularity. A numerical failure or
memory/resource growth triggers a finite implementation/equation/scope diagnosis.

## Original-equation and clock checks

Save float64 t,H,R,P,a,eta at uniform grids with32,64,128 subdivisions of each
declared time interval, plus solver/query metadata. The tight solve owns the
three-grid residual check. Use nine-point centered finite differences on saved H
through derivative order3, reconstruct R=6(H'+2H²), R',R'', and evaluate the
original E_B+Lambda g00/spatial components and a'-aH. Do not substitute the
evolution RHS to certify these residuals. Trim four boundary samples per grid.
Report absolute and normalized errors separately. Finest-grid normalized original
tensor, geometric-R and metric-clock errors must be <=1e-7; refinement must reduce
the error by at least factor2 from coarse to fine OR both be <=1e-9 fixed floating-
accuracy floor. Constraint normalized error on saved states must be <=1e-9.
This is qualified floating evidence, not interval certification or global stability.

For L in{1/4,1,2}, solve eta(t_b)=L and eta(t_a)=2L on the saved finite branch.
Absent arrivals are marked NOT_REACHED_WITHIN_WINDOW, never extrapolated.
Record p=a(t_b),q=a(t_a)/a(t_b),pq=a(t_a). Compare the three solve settings;
matched existing arrivals/ratios must agree within1e-7 absolute+relative tolerance.
Direct first/immediate-return clock definitions follow the regular null protocol;
they are not an assumed redshift curve. Exact flat and constant-positive controls
provide analytic anchors. For the flat_event case also evaluate decreasing L
{1/8,1/16,1/32} against the derived leading cubic coefficients; errors and limited
small-distance scope must be reported, not hidden by a generic pass count.

Independent review/recomputation: a separate implementation or reconstructed
saved-data calculation must examine load-bearing quantities; shared RHS regression
does not count as independent field-equation verification. Saved-artifact checks
must disclose exposure. No new guard suite is planned; these are finite scientific
diagnostics whose failures remain evidence. Maximum claims are in WORK_ORDER.
