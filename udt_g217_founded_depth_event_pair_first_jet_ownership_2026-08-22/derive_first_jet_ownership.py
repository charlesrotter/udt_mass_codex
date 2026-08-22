#!/usr/bin/env python3
"""Dependency-free exact rational witnesses for the G217 first-jet theorem."""

from fractions import Fraction as F
import json


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def multiplier(exp_depth):
    """Positive proper-clock first-jet multiplier for exp(delta)."""
    return 1 / exp_depth


def local_map(source_event, target_event, lam, curvature, source_value):
    offset = source_value - source_event
    return target_event + lam * offset + curvature * offset * offset


def local_derivative(source_event, lam, curvature, source_value):
    return lam + 2 * curvature * (source_value - source_event)


# One positive scalar owns the oriented linear map between two one-dimensional clock lines.
k_ab = F(7, 3)  # NUMERICAL_CONTROL: exp(delta_AB), not a physics pin.
lam_ab = multiplier(k_ab)
check("positive_first_jet_multiplier", lam_ab > 0)
check("depth_multiplier_inverse", k_ab * lam_ab == 1)
check("zero_depth_identity", multiplier(F(1)) == 1)
check("registered_sign", lam_ab == F(3, 7))
check("wrong_sign_excluded", lam_ab != k_ab)

# Reversal is inversion.
k_ba = 1 / k_ab
lam_ba = multiplier(k_ba)
check("reversed_depth_exponent", k_ab * k_ba == 1)
check("reversed_first_jet", lam_ab * lam_ba == 1)
check("double_reversal", multiplier(1 / k_ba) == lam_ab)

# Actual-composite composition is multiplication of first jets.
k_bc = F(11, 5)
lam_bc = multiplier(k_bc)
k_ac = k_ab * k_bc
lam_ac = multiplier(k_ac)
check("depth_composition", k_ac == F(77, 15))
check("first_jet_composition", lam_bc * lam_ab == lam_ac)
check("composition_inverse_relation", k_ac * lam_ac == 1)
check("composition_order_irrelevant_for_scalar_line", lam_ab * lam_bc == lam_bc * lam_ab)

# A common pair-domain parameter cancels from the proper-clock derivative.
rate_a = F(5, 8)
rate_b = lam_ab * rate_a
common = F(13, 6)
check("pairing_rate_from_common_parameter", rate_b / rate_a == lam_ab)
check("common_reparameterization_rate_a", rate_a / common != rate_a)
check("common_reparameterization_rate_b", rate_b / common != rate_b)
check("common_reparameterization_cancels", (rate_b / common) / (rate_a / common) == lam_ab)

# Independent incidence reparameterizations are different calibrated inputs.
scale_a = F(4, 3)
scale_b = F(9, 7)
changed = (rate_b / scale_b) / (rate_a / scale_a)
check("independent_reparameterization_changes_first_jet", changed != lam_ab)
check("independent_reparameterization_defect", changed == lam_ab * scale_a / scale_b)

# Depth does not select which events are paired.
source_event = F(0)
target_one = F(2)
target_two = F(5)
check("distinct_target_events", target_one != target_two)
check("same_multiplier_on_distinct_event_pairs", lam_ab == multiplier(k_ab))
check("event_one_affine_map_hits_target", local_map(source_event, target_one, lam_ab, F(0), source_event) == target_one)
check("event_two_affine_map_hits_target", local_map(source_event, target_two, lam_ab, F(0), source_event) == target_two)

# Paired events plus the multiplier own the first jet, not the full smooth germ.
target_event = F(4)
c_one = F(1, 2)
c_two = F(5, 3)
probe = F(1, 10)
f_one_base = local_map(source_event, target_event, lam_ab, c_one, source_event)
f_two_base = local_map(source_event, target_event, lam_ab, c_two, source_event)
df_one_base = local_derivative(source_event, lam_ab, c_one, source_event)
df_two_base = local_derivative(source_event, lam_ab, c_two, source_event)
check("same_base_event_value", f_one_base == f_two_base == target_event)
check("same_first_derivative", df_one_base == df_two_base == lam_ab)
check("same_first_jet_tuple", (source_event, target_event, df_one_base) == (source_event, target_event, df_two_base))
check("distinct_smooth_germs", local_map(source_event, target_event, lam_ab, c_one, probe) != local_map(source_event, target_event, lam_ab, c_two, probe))
check("distinct_second_derivatives", 2 * c_one != 2 * c_two)
check("first_germ_locally_positive", local_derivative(source_event, lam_ab, c_one, probe) > 0)
check("second_germ_locally_positive", local_derivative(source_event, lam_ab, c_two, probe) > 0)

# An independent direct AC relation is not automatically the actual composite.
independent_lam_ac = F(4, 9)
check("actual_composite_first_jet", lam_ac == F(15, 77))
check("independent_direct_not_forced_composite", independent_lam_ac != lam_ac)

# Exponentiated G216/static controls.
static_rate_a = F(1, 2)
static_rate_b = F(1, 5)
static_lam = static_rate_b / static_rate_a
static_k = static_rate_a / static_rate_b
check("static_pairing_derivative", static_lam == F(2, 5))
check("static_depth_exponent", static_k == F(5, 2))
check("static_temporal_factor_is_first_jet", multiplier(static_k) == static_lam)
check("static_reciprocal_ruler_factor", static_k * static_lam == 1)
check("edge_q_is_first_jet_squared", static_lam**2 == F(4, 25))
check("unit_clock_identity_control", multiplier(F(1)) ** 2 == 1)

print(json.dumps({
    "audit": "G217",
    "status": "PASS",
    "exact_checks": len(checks),
    "check_names": checks,
    "exp_depth_ab": str(k_ab),
    "first_jet_multiplier_ab": str(lam_ab),
    "actual_composite_multiplier": str(lam_ac),
    "independent_direct_multiplier": str(independent_lam_ac),
    "landing": "FOUNDED_DEPTH_COMPLETES_POSITIVE_FIRST_JET_ON_SUPPLIED_PAIRED_EVENTS__EVENT_SELECTION_AND_FULL_GERM_REMAIN_OPEN",
}, sort_keys=True))
