"""ORS2 reviewer checks: source-summary arithmetic and independent exact witnesses.

No candidate import, observation fit, empirical residual or raw data read.
Rank proof uses the complete-graph Laplacian rather than candidate elimination.
"""
import json
import math
import platform
import sys
from fractions import Fraction as F

n = 5
edges = [(i, j) for j in range(n) for i in range(j)]
rows = [tuple((k == j) - (k == i) for k in range(n)) for i, j in edges]
laplacian = [[sum(row[i] * row[j] for row in rows)
              for j in range(n)] for i in range(n)]
assert laplacian == [[n * (i == j) - 1 for j in range(n)] for i in range(n)]
ones = [1] * n
assert [sum(a*b for a, b in zip(row, ones)) for row in laplacian] == [0]*n
for k in range(1, n):
    difference = [int(i == k) - int(i == 0) for i in range(n)]
    assert [sum(a*b for a, b in zip(row, difference))
            for row in laplacian] == [n*v for v in difference]
# Four independent zero-sum directions have positive eigenvalue5, one null.

nodes = [F(i, 4) for i in range(5)]
def invisible_change(x):
    return math.prod(x-z for z in nodes)
assert all(invisible_change(z) == 0 for z in nodes)
between = invisible_change(F(1, 8))
assert between != 0

# A fixed metric and fixed identified segment under physical homothety:
# ratios stay, proper lengths and proper-acceleration magnitudes change.
scale = F(3, 2)
length = F(1, 100)
acceleration = F(9803, 1000)
scaled_length = scale * length
scaled_acceleration = acceleration / scale
assert scaled_acceleration * scaled_length == acceleration * length
assert scaled_length != length and scaled_acceleration != acceleration

c = 299792458
g = 9.803
H = 0.01
u = math.hypot(0.7, 2.5)
u_ref = math.hypot(u, 0.1)
s = g * H / c**2
out = {
    "evidence_type": "independent method checks; no empirical fit",
    "python": sys.version,
    "platform": platform.platform(),
    "laplacian_exact": laplacian,
    "rank_by_laplacian_eigenspaces": 4,
    "cycle_dimension": len(edges) - 4,
    "unobserved_between_node_change_at_1_over_8": str(between),
    "homothety_witness": {
        "scale": str(scale), "length": str(length),
        "scaled_length": str(scaled_length),
        "acceleration": str(acceleration),
        "scaled_acceleration": str(scaled_acceleration),
        "dimensionless_ratio_invariant_but_dimensional_controls_change": True
    },
    "source_summary_arithmetic": {
        "expected_gradient_magnitude_1e19_per_cm": s / 1e-19,
        "quadrature_stat_sys": u,
        "including_reference_bound_fraction": u_ref / 10.9,
        "reported_total_fraction": 2.6 / 10.9,
        "equivalent_potential_u_m2_s2": c*c*2.6e-19,
        "equivalent_height_u_mm": c*c*2.6e-19/g*1000,
        "exponential_remainder_bound": math.exp(abs(s))*s*s/2,
        "B_full_error_threshold_s_minus2": 2*c*c*2.6e-19/H**2
    },
    "omissions": ["no observed clock-gradient arithmetic", "no covariance certification",
                  "no atomic calibration replay", "no registry/source theorem rerun"]
}
print(json.dumps(out, indent=2))
