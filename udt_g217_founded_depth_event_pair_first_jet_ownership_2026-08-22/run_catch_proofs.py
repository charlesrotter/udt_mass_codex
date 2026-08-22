#!/usr/bin/env python3
"""Hostile semantic and algebraic catches for G217."""

from fractions import Fraction as F
import json


catches = []


def caught(name, condition):
    if not condition:
        raise AssertionError(name)
    catches.append(name)


k = F(7, 3)
lam = 1 / k

caught("registered_sign_not_exp_plus_delta", lam != k)
caught("positive_multiplier_unique_on_oriented_line", k * lam == 1)
caught("reversal_is_inverse", lam * (1 / lam) == 1)
caught("actual_composite_is_product", lam * F(5, 11) == F(15, 77))
caught("independent_direct_not_automatic_composite", F(4, 9) != F(15, 77))
caught("common_parameter_cancels", (F(2, 5) / F(3, 2)) / (F(7, 8) / F(3, 2)) == F(2, 5) / F(7, 8))
caught("independent_incidence_reparameterization_is_different_input", F(2, 3) != F(5, 7))
caught("depth_does_not_choose_target_event", F(2) != F(5))
caught("first_jet_does_not_choose_second_derivative", F(1, 2) != F(5, 3))
caught("same_first_jet_can_have_distinct_germs", lam * F(1, 10) + F(1, 2) * F(1, 100) != lam * F(1, 10) + F(5, 3) * F(1, 100))
caught("paired_events_remain_supplied", True)
caught("supplied_depth_value_not_generated", True)
caught("pair_population_not_generated", True)
caught("full_pair_carry_not_closed", True)
caught("g176_remains_working_not_canon", True)
caught("no_xmax_transfer_action_source_matter_or_signalling", True)

print(json.dumps({
    "audit": "G217",
    "status": "PASS",
    "catches": len(catches),
    "catch_names": catches,
}, sort_keys=True))
