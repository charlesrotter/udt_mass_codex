# Exposed independent ODE check freeze

Source-first work is complete and retained. I have now read INITIAL_CANDIDATE,
CANDIDATE_FREEZE, the initial parent checker and initial/diagnostic capture JSON;
the parent disclosed its drift-denominator defect. No successful candidate output
or other reviewer verdict has yet been read. This check is exposed, not blind.

Independently integrate one candidate incidence in affine ray parameter and
receiver proper time with SciPy DOP853; root-solve their three shared endpoint
coordinates. Input m=1,Lambda=0,a=10,R0=50,E=1,phi0=-0.2,t_e=0. Unknown ray
affine length, receiver proper time and b start at (55,65,2.4), chosen as simple
geometric estimates, not saved-result values. Use float64, rtol=atol=1e-12,
root xtol=1e-10. Actual residual and conserved-norm checks <=1e-9; eventual saved
60-digit row discrepancies <=2e-9 in R,b,tau_o,Z and sky components. These are
finite numerical agreements, not interval error certification. No tuning or fit.

The ODE equations are reconstructed from the independent source-first equations;
no parent implementation import. One new physical case, bringing this reviewer's
total to five cases. The review's arithmetic levels are the prior 50-digit anchor
and this float64 check. CPU, one BLAS thread, 2GiB address limit; no timeout/GPU,
grid or large output. Save stdout/stderr and JSON. Stop and retain diagnostic on
failure. A later successful output may be used solely for the declared comparison.
