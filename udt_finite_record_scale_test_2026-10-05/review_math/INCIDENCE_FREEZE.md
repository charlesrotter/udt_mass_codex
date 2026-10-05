# Independent incidence check freeze

Source-first reviewer implementation; no parent code imported or opened.
Dimensionless supplied shape mu=.005, A=.05, E=1, principal B_*=0,
initial y0=1e-5. Two free-and-explored homothetic histories have H=.005 and
.0025 with m=mu/H, a=A/H and R0=1/(H*y0). Evaluate receiver proper length
times centered on 0, 1.6, 200 and each center plus/minus .05. Negative first
window times are admitted on the same late branch (y remains <1/50000).

Use the exact E=1 radial solution in y and direct mpmath quadrature of the
original principal incidence equation. Solve at 70 and 90 decimal digits,
36 incidence cases total including precision replay; no optimization or sweep.
Root residual tolerance 1e-55 at both precisions; 70/90-digit readout discrepancy
<1e-45 for B, logZ, theta and K/H. Readout checks include original null-direction
unit norm, source/ray/receiver domains and b derivative along actual incidence.
Preserve all results and failures. Stop on nonconvergence or resource excess.

Synthetic errors are epsilon_log=.003, epsilon_angle=5e-8; window width=.1.
Check that the midpoint of the two center predictions is within those errors
of both true equal-width window means using certified point-to-window bounds.
Log slope bound H(1+eta), eta=.0005, uses zero source drift (which belongs to
the allowed |drift|<=5e-6 class). Angular bound |dtheta/dell|<=3e-5*H follows
from the same dimensionless constants and y<=2e-5; check the conservative
algebra explicitly. A short-record witness need cover only t=0 and t=1.6.
The t=200 pair is a contrasting separated-record diagnostic, not a universal
uniqueness assertion or a different fitted record class.

CPU only, 2GiB virtual memory, one BLAS thread, no wall/CPU timeout, capture.py;
small JSON output, no grid. Maximum claim: original incidence numerical support
and a synthetic compatible finite-record witness conditional on declared
protocol. This neither supplies a physical clock source nor selects the metric.
