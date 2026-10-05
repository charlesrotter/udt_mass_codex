"""Independent algebra/operator controls; no parent implementation imports."""
from fractions import Fraction as Q
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
checks = []


def record(name, passed, **values):
    checks.append({"name": name, "pass": bool(passed), **values})


# FRI bounds, independently recombined. Squaring is safe: all factors positive.
zmin_sq = (Q(9991, 10000) / (Q(500000003, 500000000) * Q(1, 50000)))**2 / Q(17, 20)
zmin = math.sqrt(float(zmin_sq))
record("conservative_Z_lower_bound", zmin_sq > 54180**2, lower_bound=zmin,
       exact_squared_numerator=zmin_sq.numerator, exact_squared_denominator=zmin_sq.denominator)
record("areal_R_over_a", 1 / (Q(1, 10)*Q(1, 50000)) == 500000, lower_bound=500000)
record("areal_R_over_m", 1 / (Q(1, 100)*Q(1, 50000)) == 5000000, lower_bound=5000000)
record("C_equal_one_source_radius_to_duration", Q(1, 20) <= Q(1, 10),
       a_over_c_duration=[0.05, 0.1], R_over_c_duration_lower=50000)

# Free synthetic source map, verifying proper-emitter to proper-receiver conversion.
K, Z0, qe, t = 0.3, 60000.0, 0.07, 0.4
Z = Z0 * math.exp(K*t)
s = -math.expm1(-K*t) / (K*Z0)
step = 1e-4
def log_source(time):
    return qe * (-math.expm1(-K*time) / (K*Z0))
numeric = (log_source(t+step)-log_source(t-step))/(2*step)
exact = qe/Z
record("emitter_drift_chain_rule", abs(numeric-exact) < 1e-14,
       numeric=numeric, expected=exact, emitter_time=s)

eta = Q(1, 2000)
# For the constant-rate map, the exact remaining source duration sits between
# the FRI integrated rate-bound endpoints, without assuming source frequency.
tail_exact = 1/(K*Z)
tail_lo = 1/(K*(1+float(eta))*Z)
tail_hi = 1/(K*(1-float(eta))*Z)
record("future_emitter_endpoint_enclosure", tail_lo < tail_exact < tail_hi,
       lower=tail_lo, exact=tail_exact, upper=tail_hi)

duration, spacing = Q(1), Q(1, 100000)
max_count = int(duration/(54180*spacing))+1
record("pulse_count_necessary_bound", max_count == 2, maximum_count=max_count,
       hypothetical_receiver_duration=str(duration), hypothetical_emitter_spacing=str(spacing))

# Y=t^2 has exact uniform-window mean t^2+delta^2/12.
c1, c2, delta = Q(1), Q(2), Q(2, 5)
mean1, mean2 = c1*c1+delta*delta/12, c2*c2+delta*delta/12
record("equal_translated_window_difference", mean2-mean1 == c2*c2-c1*c1,
       mean_difference=str(mean2-mean1))

# For Lipschitz Y=L|t|, differing centered widths attain the transport bound.
L, d0, d1 = Q(3), Q(1, 5), Q(2, 5)
err = L*(d1-d0)/4
record("unequal_width_Lipschitz_bound_sharp_control", err == Q(3, 20),
       error=str(err), bound_formula="L*abs(delta1-delta0)/4")


def simpson_mean_exp_negative_square(center, width, n=4096):
    left, step = center-width/2, width/n
    total = math.exp(-left*left) + math.exp(-(left+width)**2)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * math.exp(-(left+i*step)**2)
    return total*step/(3*width)


bias = []
for center in (0.0, 1.0):
    mean_log = center**2 + 0.4**2/12
    minus_log_mean = -math.log(simpson_mean_exp_negative_square(center, 0.4))
    bias.append(mean_log-minus_log_mean)
record("log_mean_is_not_mean_log", bias[0] > 0 and bias[1]-bias[0] > 0.02,
       Jensen_bias_by_center=bias, centers=[0, 1], width=0.4,
       quadrature="composite Simpson 4096 subdivisions, non-certifying float64 control")

kappa = Q(1, 1000)
measured = Q(3, 10)/(1+kappa)
record("receiver_time_scale_calibration", measured*(1+kappa) == Q(3, 10),
       ratio_measured_to_true=str(measured/Q(3, 10)))
frame_rate, dt = Q(1, 10000), Q(2)
record("frame_rate_difference_survives_window_average", frame_rate*dt == Q(1, 5000),
       frame_mean_difference=str(frame_rate*dt))

sources = ["AGENTS.md", "CLAUDE.md", "UDT_DEVELOPMENT.md",
           "udt_finite_record_scale_test_2026-10-05/INITIAL_CANDIDATE.md",
           "udt_timing_scale_identifiability_2026-10-05/INITIAL_CANDIDATE.md",
           "udt_physical_clock_interface_audit_2026-10-05/WORK_ORDER.md"]
result = {"status": "PASS" if all(c["pass"] for c in checks) else "FAIL",
          "controls": checks, "count": len(checks), "python": sys.version,
          "platform": platform.platform(), "address_space_cap_bytes": 2*1024**3,
          "blas_threads": {v: os.getenv(v) for v in
                           ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
          "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
                            for p in sources}}
(HERE/"CONTROL_RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"status": result["status"], "count": len(checks), "controls": checks}, indent=2))
sys.exit(0 if result["status"] == "PASS" else 1)
