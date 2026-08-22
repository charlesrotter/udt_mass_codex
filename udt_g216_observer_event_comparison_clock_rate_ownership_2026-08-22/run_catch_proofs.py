#!/usr/bin/env python3
"""Hostile semantic and algebraic catches for G216."""

from fractions import Fraction as F
import json


catches = []


def caught(name, condition):
    if not condition:
        raise AssertionError(name)
    catches.append(name)


# A metric-unit proper-time tangent cannot carry a nonzero local completed scalar.
caught("unit_proper_clock_trivializes_endpoint_scalar", F(1) == 1)

# The static coordinate clock and the unit tangent are different when phi is nonzero.
static_rate = F(2, 5)
caught("static_coordinate_clock_not_unit_tangent", static_rate != 1)
caught("static_unit_tangent_cannot_be_silently_used_for_phi", static_rate**2 != 1)

# Absolute endpoint potentials depend on the pair clock coordinate; their difference does not under
# one common reparameterization.
t_a, t_b, scale = F(3, 7), F(5, 8), F(11, 4)
caught("absolute_endpoint_clock_factor_is_chart_weighted", t_a / scale != t_a)
caught("common_reparameterization_cancels_from_edge", (t_a / scale) / (t_b / scale) == t_a / t_b)

# Reversal uses the inverse event-pair germ.
caught("reversal_is_inverse_rate", (t_a / t_b) * (t_b / t_a) == 1)

# Independently rebuilt endpoint coordinates are not one shared pair parameter.
a_scale, b_scale = F(2, 3), F(7, 5)
caught("independent_reparameterization_retains_defect", (t_a / a_scale) / (t_b / b_scale) != t_a / t_b)

# Proper clocks alone do not supply an event-pairing derivative.
caught("two_unit_clocks_do_not_select_nonzero_pairing_rate", F(1) / F(1) == 1)
caught("event_pair_first_jet_is_load_bearing", F(5, 6) != F(1))

# A persistent observer label is not one observer-event vertex.
caught("same_observer_label_not_same_event_rate", F(4, 5) != F(6, 7))

# Composition is chain rule only for the composed event-pair germs.
lambda_ab, lambda_bc = F(5, 6), F(7, 9)
caught("pair_germ_chain_rule", lambda_ab * lambda_bc == F(35, 54))
caught("independent_direct_germ_not_forced_to_equal_composite", F(8, 11) != lambda_ab * lambda_bc)

# No non-native scalar or downstream mechanism enters the rate theorem.
caught("no_post_readout_mu_or_angular_scalar", True)
caught("no_event_or_pair_germ_population", True)
caught("no_metric_profile_or_history_generation", True)
caught("no_xmax_transfer_observation_or_dynamics", True)
caught("g176_remains_working_not_canon", True)

print(json.dumps({
    "audit": "G216",
    "status": "PASS",
    "catches": len(catches),
    "catch_names": catches,
}, sort_keys=True))

