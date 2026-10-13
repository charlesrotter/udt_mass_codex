"""Independent incidence quadrature for the ALP1 mathematical review."""
import json
import platform
import resource
import sys
import time

import mpmath as mp

mp.mp.dps = 45
start_cpu = time.process_time()
checks = []
rows = []


def require(name, condition, details):
    checks.append({"name": name, "passed": bool(condition), "details": details})


def dec(x):
    return mp.nstr(x, 38)


for k in map(mp.mpf, ["-1.5", "-1", "0", "1", "3"]):
    s = 2 * mp.sqrt(k + 2) / mp.pi

    def a(t):
        x = t / s
        return 1 + k*x*x + x**4

    def eta(t):
        return mp.quad(lambda z: 1/a(z), [0, t])

    boundary = mp.quad(lambda z: 1/a(z), [0, s, mp.inf])
    require("common_boundary_" + dec(k), abs(boundary-1) < mp.mpf("1e-35"), dec(boundary))
    # Hold the original separation fixed while varying emission proper time.
    tr = 2*s
    separation = eta(tr)
    derivatives = []
    for h in [mp.mpf("1e-7")*s, mp.mpf("5e-8")*s]:
        arrivals = []
        residuals = []
        for te in [-h, h]:
            def incidence(t):
                return eta(t)-eta(te)-separation
            arrival = mp.findroot(incidence, (tr-a(tr)*h*2, tr+a(tr)*h*2))
            arrivals.append(arrival)
            residuals.append(abs(incidence(arrival)))
        derivative = (arrivals[1]-arrivals[0])/(2*h)
        relerr = abs(derivative/a(tr)-1)
        require("arrival_derivative_" + dec(k) + "_" + dec(h), relerr < mp.mpf("1e-10"), dec(relerr))
        require("incidence_residual_" + dec(k) + "_" + dec(h), max(residuals) < mp.mpf("1e-35"), dec(max(residuals)))
        derivatives.append({"h":dec(h), "observed":dec(derivative), "claimed":dec(a(tr)), "relative_error":dec(relerr)})
    local = []
    target_quartic = 1+k*k/6
    for x in map(mp.mpf, ["1e-3", "5e-4"]):
        y = eta(s*x)/s
        logp = mp.log(a(s*x))
        q = (logp-k*y*y)/y**4
        local.append({"x":dec(x), "quartic_residual_coefficient":dec(q), "target":dec(target_quartic), "error":dec(abs(q-target_quartic)), "mean":dec(logp)})
    require("local_quartic_"+dec(k), abs(mp.mpf(local[-1]["quartic_residual_coefficient"])-target_quartic) < mp.mpf("2e-5"), local[-1])
    tail = []
    errors = []
    for x in map(mp.mpf, ["20", "40", "80"]):
        t = s*x
        delta = mp.quad(lambda z:1/a(z), [t, mp.inf])
        ratio = a(t)/(s/(3*delta))**(mp.mpf(4)/3)
        errors.append(abs(ratio-1))
        tail.append({"x":dec(x), "delta":dec(delta), "asymptotic_ratio":dec(ratio)})
    require("tail_limit_"+dec(k), errors[-1] < mp.mpf("0.01") and errors[2]<errors[1]<errors[0], tail)
    rows.append({"k":dec(k),"s":dec(s),"boundary_integral":dec(boundary),"separation":dec(separation),"derivatives":derivatives,"local":local,"tail":tail})

crossing = mp.quad(lambda t:1/(1-t*t+t**4), [0,1])
claimed = mp.pi/4 + mp.log(2+mp.sqrt(3))/(2*mp.sqrt(3))
require("corrected_crossing", abs(crossing-claimed) < mp.mpf("1e-35"), {"integrated":dec(crossing),"formula":dec(claimed)})
require("reject_wrong_half_integral", abs(crossing-mp.pi/4)>mp.mpf("0.3"), dec(crossing-mp.pi/4))
result={"status":"PASS" if all(c["passed"] for c in checks) else "FAIL", "method":"Independent high-precision original-incidence quadrature and nearby-emission root solves; not an interval enclosure", "python":sys.version, "platform":platform.platform(), "mpmath":mp.__version__, "decimal_precision":mp.mp.dps,"rows":rows,"checks":checks,"cpu_seconds":time.process_time()-start_cpu,"maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
print(json.dumps(result,indent=2))
sys.exit(0 if result["status"]=="PASS" else 1)
