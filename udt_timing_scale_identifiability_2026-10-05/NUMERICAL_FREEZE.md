# TSI1 parent numerical confirmation freeze

No parent confirmation outcomes seen. Discovery is algebraic and inherited
CPR/OJM experience; preliminary independent reviewers confirm smooth-tail and
cadence cautions. Freeze current initial candidate and check_timing_scale.py.

CPU mpmath35/60 digits and SymPy exact; existing capture gives2GiB/1BLAS/no
timeout. Conditional units m=1,a=10,H=sqrt(.0001/3); E=1,10; b_*=0,2,-3;
R=1000,100000,10000000, all combinations.18 incidences/precision. Each E1,
R100000 branch gets lambda7/3 homothetic solve,3/precision. Principal E1,
R100000 gets relativeR steps +/-1e-4,+/-5e-5,4 extra solves/precision.
Total50 finite cases plus9 exact groups and2 unit-conversion negative controls.
<=100 total including repair/reruns; only50 finite cases remain after first run.

Check original incidence residual <10^(-dps+8); directional norm same tolerance;
scale agreement <10^(-dps+10);35/60-digit output agreement <1e-22. Latest-R
K/H differs from1 by<.001 and error <.1 previous-R error +1e-15. Principal
angular rate/H differs from1 by<.001. Symmetric differences over integrated
receiver proper interval agree with analytic rates to1e-7; halving step reduces
error by factor<.4 plus1e-25. No claim these tolerances prove a continuum limit.
Exact controls: original EF metric frame norms and parallel transport, derivative
identity and anchor dimensions. Deliberate omission of c_E in seconds rejected.

Stop on a failure; retain stdout/stderr/code/candidate. Freeze a finite diagnosis
and at most a same-premise implementation repair within remaining cases. No
tolerance relaxation or fitted asymptotic coefficient. Initial results remain.
