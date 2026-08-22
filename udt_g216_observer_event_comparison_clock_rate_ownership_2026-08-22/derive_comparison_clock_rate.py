#!/usr/bin/env python3
"""Dependency-free exact rational derivation witnesses for G216."""

from fractions import Fraction as F
import json


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def clock_norm_squared(proper_rate):
    """Return -g(u,u) for u=(d tau/dy) U and g(U,U)=-1."""
    return proper_rate * proper_rate


def endpoint_q(proper_rate):
    """q_X=exp(-2 Phi_X)=T_X^2."""
    return proper_rate * proper_rate


def edge_exp_delta(rate_source, rate_target):
    """exp(delta_AB) for delta_AB=Phi_B-Phi_A."""
    return rate_source / rate_target


def edge_q(rate_source, rate_target):
    """exp(-2 delta_AB)."""
    return endpoint_q(rate_target) / endpoint_q(rate_source)


def reparameterize_rate(proper_rate, dy_prime_by_dy):
    """d tau/dy' when y'=f(y) with positive derivative dy'/dy."""
    return proper_rate / dy_prime_by_dy


# Metric proper-time normalization.
rate = F(7, 5)
check("comparison_tangent_norm", clock_norm_squared(rate) == F(49, 25))
check("comparison_clock_factor", clock_norm_squared(rate) == rate**2)
check("unit_proper_time_clock_factor", clock_norm_squared(F(1)) == 1)
check("unit_proper_time_endpoint_q", endpoint_q(F(1)) == 1)
check("unit_proper_time_endpoint_exp_phi", 1 / F(1) == 1)

# One pair parameter y induces two endpoint proper-clock rates.
t_a = F(3, 4)
t_b = F(5, 7)
exp_delta_ab = edge_exp_delta(t_a, t_b)
q_ab = edge_q(t_a, t_b)
check("endpoint_relative_rate_ratio", exp_delta_ab == F(21, 20))
check("endpoint_relative_q", q_ab == F(400, 441))
check("edge_exp_and_q_consistent", exp_delta_ab**2 * q_ab == 1)
check("edge_reversal", exp_delta_ab * edge_exp_delta(t_b, t_a) == 1)
check("edge_q_reversal", q_ab * edge_q(t_b, t_a) == 1)

# Common pair reparameterization changes endpoint potentials but cancels from depth.
common_scale = F(11, 6)
t_a_prime = reparameterize_rate(t_a, common_scale)
t_b_prime = reparameterize_rate(t_b, common_scale)
check("common_reparameterization_changes_endpoint_rates", t_a_prime != t_a and t_b_prime != t_b)
check("common_reparameterization_preserves_exp_delta", edge_exp_delta(t_a_prime, t_b_prime) == exp_delta_ab)
check("common_reparameterization_preserves_q", edge_q(t_a_prime, t_b_prime) == q_ab)

# Independent endpoint parameters reproduce the exact G215 calibration defect.
a_scale = F(7, 3)
b_scale = F(9, 4)
t_a_independent = reparameterize_rate(t_a, a_scale)
t_b_independent = reparameterize_rate(t_b, b_scale)
check(
    "independent_reparameterization_exp_defect",
    edge_exp_delta(t_a_independent, t_b_independent) == exp_delta_ab * b_scale / a_scale,
)
check(
    "independent_reparameterization_q_defect",
    edge_q(t_a_independent, t_b_independent) == q_ab * (a_scale / b_scale) ** 2,
)

# The invariant edge datum is the first derivative of the proper-time event pairing.
lambda_ab = t_b / t_a
check("pairing_derivative", lambda_ab == F(20, 21))
check("depth_is_inverse_pairing_derivative", exp_delta_ab == 1 / lambda_ab)
check("inverse_pairing_derivative", (1 / lambda_ab) * lambda_ab == 1)
check("pairing_derivative_squared_is_edge_q", lambda_ab**2 == q_ab)
check("common_reparameterization_preserves_pairing_derivative", t_b_prime / t_a_prime == lambda_ab)
check("endpoint_k_ratio_is_fourth_depth_power", ((1 / t_b) ** 4) / ((1 / t_a) ** 4) == exp_delta_ab**4)

# Composition is the chain rule for composable event-pair germs.
t_c = F(8, 9)
lambda_bc = t_c / t_b
lambda_ac = t_c / t_a
check("pairing_derivative_chain_rule", lambda_ab * lambda_bc == lambda_ac)
check(
    "depth_composition",
    edge_exp_delta(t_a, t_b) * edge_exp_delta(t_b, t_c) == edge_exp_delta(t_a, t_c),
)
check("q_composition", edge_q(t_a, t_b) * edge_q(t_b, t_c) == edge_q(t_a, t_c))

# Primary static specialization.  Write a=exp(-phi); g_x0x0=-a^2.
a_static = F(2, 5)
g_x0x0 = -(a_static**2)
unit_tangent_x0_component = 1 / a_static
check("static_unit_tangent_normalization", g_x0x0 * unit_tangent_x0_component**2 == -1)
check("static_coordinate_tangent_clock_factor", -g_x0x0 == a_static**2)
check("static_coordinate_tangent_endpoint_q", endpoint_q(a_static) == a_static**2)
check("static_primary_phi_proxy", (1 / a_static) ** 4 == F(625, 16))
check("static_unit_tangent_does_not_recover_nonzero_phi", endpoint_q(F(1)) != endpoint_q(a_static))

# Two static endpoints recover exp(phi_B-phi_A) exactly.
a_static_a = F(1, 2)
a_static_b = F(1, 5)
check("static_endpoint_relative_phi", edge_exp_delta(a_static_a, a_static_b) == F(5, 2))
check(
    "static_endpoint_relative_endpoint_k_ratio",
    ((1 / a_static_b) ** 4) / ((1 / a_static_a) ** 4) == edge_exp_delta(a_static_a, a_static_b) ** 4,
)

# Same persistent observer at distinct events is not one endpoint vertex.
t_event_one = F(2, 3)
t_event_two = F(4, 5)
check("same_observer_distinct_event_rates_can_differ", t_event_one != t_event_two)
check("event_label_needed_for_endpoint_potential", endpoint_q(t_event_one) != endpoint_q(t_event_two))

# A supplied pair map fixes the rates; no separate clock-scale coefficient remains.
check("pair_map_rate_fixes_clock_norm_a", clock_norm_squared(t_a) == t_a**2)
check("pair_map_rate_fixes_clock_norm_b", clock_norm_squared(t_b) == t_b**2)
check("both_unit_clocks_force_zero_relative_depth", edge_exp_delta(F(1), F(1)) == 1)

print(json.dumps({
    "audit": "G216",
    "status": "PASS",
    "exact_checks": len(checks),
    "check_names": checks,
    "unit_clock_q": str(endpoint_q(F(1))),
    "pairing_derivative": str(lambda_ab),
    "edge_exp_delta": str(exp_delta_ab),
    "common_reparameterized_edge_exp_delta": str(edge_exp_delta(t_a_prime, t_b_prime)),
    "independent_reparameterized_edge_exp_delta": str(edge_exp_delta(t_a_independent, t_b_independent)),
    "landing": "PAIR_GERM_PROPER_CLOCK_RATE_LAW__UNIT_CLOCK_TRIVIALIZATION__COMMON_REPARAMETERIZATION_CANCELLATION",
}, sort_keys=True))
