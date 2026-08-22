#!/usr/bin/env python3
"""Dependency-free exact rational derivation witnesses for G215."""

from fractions import Fraction as F
import json


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def tr(a):
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def diag(a, b):
    return ((a, F(0)), (F(0), b))


def cong(h, p):
    return mm(mm(tr(p), h), p)


def pair_metric(T, L, beta):
    return ((-T * T, -T * T * beta), (-T * T * beta, L * L - T * T * beta * beta))


def normalize(h, m):
    return cong(h, diag(F(1), F(1) / m))


def terminal_k(h):
    """K=exp(4 Phi) on a regular Lorentz pair metric."""
    return -det(h) / (h[0][0] * h[0][0])


def completed_terminal_k_from_raw(h):
    """Use m^2=-det(h); no square-root approximation is needed."""
    m2 = -det(h)
    det_completed = det(h) / m2
    return -det_completed / (h[0][0] * h[0][0])


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


T = F(3, 5)
L = F(7, 4)
beta = F(-2, 3)
h = pair_metric(T, L, beta)
m = T * L
hs = normalize(h, m)

check("generic_pair_determinant", det(h) == -(T * L) ** 2)
check("generic_clock_recovery", -h[0][0] == T * T)
check("generic_ruler_recovery", h[1][1] - h[0][1] ** 2 / h[0][0] == L * L)
check("g176_density", m * m == -det(h))
check("completed_determinant", det(hs) == -1)
check("completed_clock_unchanged", hs[0][0] == -T * T)
check("completed_terminal_k", terminal_k(hs) == 1 / T**4)
check("completed_phi_proxy", T**4 * terminal_k(hs) == 1)

# G214 overlap refinement: ruler/shear recharting is scalar-neutral, while
# a clock rescaling is exactly the remaining calibration carry.
p_clock_fixed = ((F(1), F(4, 9)), (F(0), F(7, 3)))
h_clock_fixed = cong(h, p_clock_fixed)
check("clock_fixed_rechart_preserves_completed_scalar", completed_terminal_k_from_raw(h_clock_fixed) == 1 / T**4)
p_clock_scaled = ((F(5, 4), F(-2, 7)), (F(0), F(9, 5)))
h_clock_scaled = cong(h, p_clock_scaled)
check("general_rechart_scales_clock_factor", -h_clock_scaled[0][0] == (F(5, 4) * T) ** 2)
check("general_rechart_completed_scalar_clock_weight", completed_terminal_k_from_raw(h_clock_scaled) == 1 / ((F(5, 4) * T) ** 4))

# Same clock, different ruler scale and shift.
h_a = pair_metric(T, F(5, 6), F(1, 5))
h_b = pair_metric(T, F(11, 7), F(-3, 4))
m_a = T * F(5, 6)
m_b = T * F(11, 7)
hs_a = normalize(h_a, m_a)
hs_b = normalize(h_b, m_b)
check("shared_clock_scalar_equal", terminal_k(hs_a) == terminal_k(hs_b) == 1 / T**4)
check("raw_pair_scalar_can_differ", terminal_k(h_a) != terminal_k(h_b))
check("ruler_density_can_differ", m_a != m_b)
check("completed_shift_can_differ", hs_a[0][1] != hs_b[0][1])
check("scalar_equality_not_metric_equality", hs_a != hs_b)

# Exact G171 angular witness, now evaluated after G176 completion.
h171_a = ((F(-1), F(-1, 2)), (F(-1, 2), F(3, 4)))
h171_b = ((F(-1), F(-1, 2)), (F(-1, 2), F(211, 100)))
check("g171_raw_scalar_mismatch_retained_as_control", terminal_k(h171_a) == 1 and terminal_k(h171_b) == F(59, 25))
check("g171_shared_clock_factor", -h171_a[0][0] == -h171_b[0][0] == 1)
check("g171_second_ruler_square", -det(h171_b) == F(59, 25))
check("g171_completed_scalar_match", completed_terminal_k_from_raw(h171_a) == completed_terminal_k_from_raw(h171_b) == 1)
check("g171_completed_determinants", det(h171_a) / (-det(h171_a)) == det(h171_b) / (-det(h171_b)) == -1)

# Primary static common-clock specialization: exp(phi)=2, hence T=1/2 and exp(4 Phi)=16.
T_static = F(1, 2)
h_static_radial = pair_metric(T_static, F(2), F(0))
h_static_angular = pair_metric(T_static, F(17, 5), F(3, 7))
check("primary_static_phi_recovery", completed_terminal_k_from_raw(h_static_radial) == 16)
check("primary_static_angular_scalar_independence", completed_terminal_k_from_raw(h_static_angular) == 16)

# Network laws use q_X=exp(-2 varphi_X)=T_X^2.
t_a, t_b, t_c, t_d = F(2, 3), F(5, 4), F(7, 6), F(9, 5)
q_ab = t_b**2 / t_a**2
q_bc = t_c**2 / t_b**2
q_cd = t_d**2 / t_c**2
q_da = t_a**2 / t_d**2
check("same_edge_reversal", q_ab * (1 / q_ab) == 1)
check("triangle_clock_potential_closure", q_ab * q_bc * (t_a**2 / t_c**2) == 1)
check("arbitrary_cycle_clock_potential_closure", q_ab * q_bc * q_cd * q_da == 1)

# Same label but independently rescaled B clock on BC: exact scalar defect survives.
scale = F(3, 2)
q_bc_recalibrated = t_c**2 / ((scale * t_b) ** 2)
check("independent_clock_recalibration_defect", q_ab * q_bc_recalibrated * (t_a**2 / t_c**2) == 1 / scale**2)

# Full pair metrics still do not form a native product.
product = mm(hs_a, hs_b)
check("pair_metric_product_not_symmetric", product != tr(product))

print(json.dumps({
    "audit": "G215",
    "status": "PASS",
    "exact_checks": len(checks),
    "check_names": checks,
    "g171_raw_k": [str(terminal_k(h171_a)), str(terminal_k(h171_b))],
    "g171_completed_k": [str(completed_terminal_k_from_raw(h171_a)), str(completed_terminal_k_from_raw(h171_b))],
    "recalibrated_cycle_product": str(q_ab * q_bc_recalibrated * (t_a**2 / t_c**2)),
    "landing": "COMPLETED_SCALAR_DESCENDS_TO_SHARED_CLOCK__G171_REGRADED__FULL_PAIR_CARRY_REMAINS_STRONGER",
}, sort_keys=True))
