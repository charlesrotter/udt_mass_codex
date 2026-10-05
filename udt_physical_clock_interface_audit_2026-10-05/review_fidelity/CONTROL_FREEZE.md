# Exposed independent arithmetic-control freeze

Question: do PIA1's admitted-domain redshift threshold, geometry ratios, counter
bias, units and comparison-only conversions survive independent reconstruction?
This is an exposed argument check, not a blind confirmation or physical test.
Candidate and five primary sources have been read. No parent code or numerical
result has been read or imported. Formulae are independently transcribed from
the candidate and checked against the original FRI1 domain/records.

Run seven named controls, at most one initial execution plus bounded repairs
within the total 40-control cap. Every failure is retained. Controls use
standard-library exact Fraction arithmetic for rational inequalities, and
binary64 math for illustrative log/angle/proxy conversions. The latter are
not interval certification. No field grid, GPU, solve, data fit or sampling
certificate is involved. One CPU Python process; 2 GiB RLIMIT_AS; one BLAS thread;
no wall/CPU timeout. Stop if a load-bearing bound fails or scope expansion is
needed. Maximum conclusion: checked conditional algebra/conversions.

1. Square the positive P1 expression exactly and compare to 54180 squared.
2. Reconstruct all four geometric ratio limits with exact rational arithmetic.
3. Exhibit identical phase increments and unequal log means for frequencies
   1 and the equally weighted pair (1/2,3/2); compare the gap to log(3)^2/8.
4. Recompute P3's FRI1 long-control bound exactly and compare with 3.14e-8.
5. Independently convert epsilon=.003 to a sufficient fractional-frequency
   envelope and 5e-8 radians to milliarcseconds.
6. Independently compute the range of the six MCP XIII Table 1 optical-frame
   proxies using its tabulated central velocities. These are comparison
   proxies, not physical total Z or a fitted observation.
7. Check long/short duration, window and source-drift dimensionless ratios from
   the FRI1 fixed controls.

Execution command (cwd repository root):

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_physical_clock_interface_audit_2026-10-05/review_fidelity/independent_controls.py > udt_physical_clock_interface_audit_2026-10-05/review_fidelity/controls.stdout.json 2> udt_physical_clock_interface_audit_2026-10-05/review_fidelity/controls.stderr
