"""Seven independent exposed controls; no parent implementation imports."""
import json
import math
import os
import platform
import resource
from fractions import Fraction as Q

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
rows = []

def record(name, passed, **values):
    rows.append(dict(name=name, passed=bool(passed), **values))

# All factors are positive, so squaring preserves the threshold comparison.
threshold_squared = Q(".9991") ** 2 / (
    Q(".85") * Q("1.000000006") ** 2 * Q(".00002") ** 2
)
record("P1_positive_squared_threshold", threshold_squared > Q(54180) ** 2,
       squared_exact=str(threshold_squared), illustrative_Z=math.sqrt(float(threshold_squared)))

ratios = [1/Q(".00002"), 1/(Q(".1")*Q(".00002")),
          1/(Q(".01")*Q(".00002")), Q(".005")/Q(".1"), Q(".01")/Q(".05")]
record("geometry_ratios", ratios == [Q(50000), Q(500000), Q(5000000), Q(".05"), Q(".2")],
       exact=[str(x) for x in ratios])

phase_average = (Q(1,2) + Q(3,2)) / 2
mean_log = (math.log(.5) + math.log(1.5))/2
gap = -mean_log
range_bound = math.log(3)**2/8
record("phase_to_log_mean_counterexample", phase_average == 1 and 0 < gap <= range_bound,
       phase_average_exact=str(phase_average), mean_log=mean_log,
       positive_bias=gap, range_only_bound=range_bound)

H, eta, q, delta = Q(".005"), Q(".0005"), Q(".000005"), Q(".1")
M = H*(1+eta)+q
bias = M*M*delta*delta/8
record("P3_long_control_bound", bias < Q(".0000000314"), M_exact=str(M),
       bias_exact=str(bias), bias_float=float(bias))

fractional = -math.expm1(-.003)
milliarcsec = 5e-8 * 180/math.pi * 3600 * 1000
record("frequency_and_angle_conversions", .0029955 < fractional < .0029956 and 10.313 < milliarcsec < 10.314,
       fractional_frequency_envelope=fractional, milliarcseconds=milliarcsec)

velocities = [Q(x) for x in ["3319.9", "10192.6", "7801.5", "8525.7", "7172.2", "679.3"]]
proxies = [1+v/Q("299792.458") for v in velocities]
record("comparison_only_optical_proxies", Q("1.0022") < min(proxies) < Q("1.0023") and Q("1.0339") < max(proxies) < Q("1.0341"),
       values=[float(x) for x in proxies], minimum=float(min(proxies)), maximum=float(max(proxies)),
       status="model/frame proxies; not direct total-Z observations")

ratios2 = [H*Q(200), H*Q("1.6"), H*delta, q/H]
record("FRI_control_dimensionless_ratios", ratios2 == [Q(1),Q(".008"),Q(".0005"),Q(".001")],
       exact=[str(x) for x in ratios2])

result = {"schema":"PIA1-independent-fidelity-controls-1", "python":platform.python_version(),
          "implementation":"independent standard-library formulas; no parent imports",
          "limits":{"RLIMIT_AS":resource.getrlimit(resource.RLIMIT_AS), "BLAS_threads":{k:os.environ.get(k) for k in ["OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS"]}, "timeout":None},
          "control_count":len(rows), "all_passed":all(r["passed"] for r in rows), "controls":rows}
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["all_passed"] else 1)
