#!/usr/bin/env python3
"""Exact control: one supplied metric, two carried static clock references.

No physical query population or field equation is assumed. The positive profile
f=1+(r/ell)^2 is FREE-AND-EXPLORED control geometry; ell is a unit/reference
length, not a selected physical scale. All displayed radii use r/ell.
"""
from fractions import Fraction as F
import json
import platform


def enc(x):
    if isinstance(x, F):
        return str(x)
    raise TypeError(type(x).__name__)


checks = []


def check(name, statement):
    if not statement:
        raise AssertionError(name)
    checks.append(name)


def f(r):
    return 1 + r * r


r_b = F(2)
b = f(r_b)
metric_b = [-b, 1 / b, r_b * r_b, r_b * r_b]
records = []
for label, r_ref in [("A", F(1)), ("C", F(3))]:
    a = f(r_ref)
    q = b / a
    # y0=sqrt(a)*x0; y1=r/sqrt(a). The angular coordinates stay fixed.
    # These are squared Jacobian entries of dx/dy, so all arithmetic is rational.
    jacobian_squared = [1 / a, a, F(1), F(1)]
    transformed = [g * j for g, j in zip(metric_b, jacobian_squared)]
    expected = [-q, 1 / q, r_b * r_b, r_b * r_b]
    check(label + ":full_metric_pullback", transformed == expected)
    check(label + ":reciprocal_pair_determinant", transformed[0] * transformed[1] == -1)
    check(label + ":regular_clock_and_pair", transformed[0] < 0 and transformed[1] > 0)
    check(label + ":coordinate_null_tangent", transformed[0] + transformed[1] * q * q == 0)
    check(label + ":proper_null_ratio_squared", transformed[1] * q * q / -transformed[0] == 1)
    check(label + ":same_base_null_direction", a * q == b)
    check(label + ":angular_sector_retained", transformed[2:] == metric_b[2:])
    records.append({
        "reference": label,
        "reference_r_over_ell": r_ref,
        "reference_f": a,
        "terminal_r_over_ell": r_b,
        "terminal_f": b,
        "clock_ratio_squared_T2": q,
        "completed_pair_c_eff_over_c_E": q,
        "carried_metric_at_B_equator": transformed,
        "proper_null_speed_squared_over_c_E_squared": F(1),
        "base_coordinate_null_dr_over_dx0": a * q,
    })

q_ab, q_cb = (record["completed_pair_c_eff_over_c_E"] for record in records)
check("different_matched_reference_queries", q_ab != q_cb)
check("matched_composition", f(F(3)) / f(F(1)) * q_cb == q_ab)
check("matched_reversal", q_ab * (f(F(1)) / f(F(2))) == 1)
# If the proper-frame cone itself is changed to v/c_E=q, its original metric
# residual is q^2-1. These nonzero residuals concern that named substitution only.
bad_cone_residuals = [q_ab * q_ab - 1, q_cb * q_cb - 1]
check("direct_proper_cone_substitution_fails_A", bad_cone_residuals[0] != 0)
check("direct_proper_cone_substitution_fails_C", bad_cone_residuals[1] != 0)

result = {
    "status": "PASS_EXACT_CONTROL_ONLY",
    "python": platform.python_version(),
    "method": "dependency-free exact rational arithmetic",
    "scope": "two matched static reference queries on one supplied complete positive-f metric",
    "interpretation": "query dependence is demonstrated; physical population and field-law admission are not",
    "fixed_base_metric_at_B_equator": metric_b,
    "fixed_dimensionless_profile_jet_at_B_through_order_four": [b, 2*r_b, F(2), F(0), F(0)],
    "queries": records,
    "original_proper_metric_residual_after_named_bad_cone_substitution": bad_cone_residuals,
    "checks": checks,
    "check_count": len(checks),
}
print(json.dumps(result, indent=2, default=enc))
