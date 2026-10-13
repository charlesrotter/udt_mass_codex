"""Independent finite quadrature audit; no candidate implementation imports."""
import json
import math
import platform
import resource
import sys
import time


def mean_simpson(fun, intervals):
    step = 2.0 / intervals
    odd = math.fsum(fun(-1.0 + step * i) for i in range(1, intervals, 2))
    even = math.fsum(fun(-1.0 + step * i) for i in range(2, intervals, 2))
    return step * (fun(-1.0) + fun(1.0) + 4.0 * odd + 2.0 * even) / 6.0


start = time.process_time()
print(json.dumps({"python": sys.version, "platform": platform.platform(),
                  "evidence": "independent double quadrature; analytic inputs exposed",
                  "intervals": [1024, 4096, 16384], "absolute_tolerance": 2e-10}), flush=True)
results = []
for rho in (0.25, 0.8, 1.5):
    a, b = math.cosh(rho), math.sinh(rho)
    expected = rho / math.tanh(rho) - 1.0
    grids = []
    for count in (1024, 4096, 16384):
        direct_receive = mean_simpson(lambda y: math.log(a - b * y), count)
        direct_emit = mean_simpson(lambda x: -math.log(a + b * x), count)
        carried = mean_simpson(lambda x: -math.log(a + b * x) / (a + b * x)**2, count)
        normalization = mean_simpson(lambda y: (a - b * y)**-2, count)
        jacobian_total = mean_simpson(lambda x: (a + b * x)**-2, count)
        wrong_jacobian_total = mean_simpson(lambda x: (a + b * x)**2, count)
        row = dict(intervals=count, receive=direct_receive, emit=direct_emit,
                   carried=carried, normalization=normalization,
                   jacobian_total=jacobian_total,
                   wrong_jacobian_total=wrong_jacobian_total)
        row["max_error"] = max(abs(direct_receive - expected),
                               abs(direct_emit + expected),
                               abs(carried - expected),
                               abs(normalization - 1.0), abs(jacobian_total - 1.0))
        grids.append(row)
        print(json.dumps(dict(rho=rho, expected_receive=expected, **row)), flush=True)
    assert grids[-1]["max_error"] < 2e-10, (rho, grids[-1])
    assert grids[-1]["receive"] > 0 and grids[-1]["emit"] < 0
    assert grids[-1]["carried"] > 0
    assert grids[-1]["wrong_jacobian_total"] - 1.0 > 0.01
    results.append(dict(rho=rho, maximum_fine_error=grids[-1]["max_error"]))

assert mean_simpson(lambda x: 0.0, 1024) == 0.0
assert mean_simpson(lambda x: 1.0, 1024) == 1.0
print(json.dumps({"status": "PASS", "results": results,
                  "false_pass_probes": "omitted measure reverses sign; inverse Jacobian fails normalization",
                  "cpu_seconds": time.process_time() - start,
                  "maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), flush=True)
