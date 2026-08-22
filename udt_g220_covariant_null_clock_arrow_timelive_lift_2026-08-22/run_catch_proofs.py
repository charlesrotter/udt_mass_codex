#!/usr/bin/env python3
"""Injected algebraic and ownership mutation catches for the bounded G220 result."""

from __future__ import annotations

import csv
import copy
import json
from fractions import Fraction
from pathlib import Path


if not __debug__:
    raise RuntimeError("G220 evidence must run with Python assertions enabled; -O is forbidden")

HERE = Path(__file__).resolve().parent


def norm(dt: Fraction, dx: Fraction, n: Fraction, a: Fraction, beta: Fraction) -> Fraction:
    return -(n * (dt + beta * dx)) ** 2 + (a * dx) ** 2


def catches() -> dict[str, bool]:
    def catches_mutation(validator, correct, mutant) -> bool:
        return bool(validator(correct)) and not bool(validator(mutant))

    # Covariant endpoint contract.
    sigma_a_u, sigma_b_u = Fraction(6), Fraction(-4)

    def implicit_valid(candidate: Fraction) -> bool:
        return candidate > 0 and sigma_a_u + sigma_b_u * candidate == 0

    correct_implicit = -sigma_a_u / sigma_b_u
    wrong_implicit_sign = sigma_a_u / sigma_b_u

    span = Fraction(2, 3)
    k_a_u, k_b_u = Fraction(-9), Fraction(-6)
    correct_sigma_source = -span * k_a_u
    correct_sigma_target = span * k_b_u

    def tangent_orientation_valid(pair: tuple[Fraction, Fraction]) -> bool:
        source, target = pair
        return source == sigma_a_u and target == sigma_b_u and -source / target == k_a_u / k_b_u

    # Rescale both endpoints or, in the mutant, only the source endpoint.
    affine_scale = Fraction(7, 3)

    def affine_ratio_valid(candidate: Fraction) -> bool:
        return candidate == k_a_u / k_b_u

    correct_affine_ratio = (affine_scale * k_a_u) / (affine_scale * k_b_u)
    one_endpoint_affine_ratio = (affine_scale * k_a_u) / k_b_u

    def frequency_valid(candidate: Fraction) -> bool:
        return candidate == correct_implicit

    correct_frequency = k_a_u / k_b_u
    inverted_frequency = k_b_u / k_a_u

    # Time-live triangular endpoint contract.
    n_a, n_b = Fraction(2), Fraction(3)
    a_a, a_b = Fraction(5), Fraction(6)
    beta_a, beta_b = Fraction(1, 2), Fraction(1, 3)
    cp_a, cp_b = a_a - n_a * beta_a, a_b - n_b * beta_b
    cm_a = a_a + n_a * beta_a

    def right_speed_valid(candidate: Fraction) -> bool:
        return candidate > 0 and norm(Fraction(1), candidate, n_a, a_a, beta_a) == 0

    correct_right_speed = n_a / cp_a
    cminus_right_speed = n_a / cm_a
    beta_dropped_speed = n_a / a_a

    correct_dt_b_dt_a = n_a * cp_b / (cp_a * n_b)

    def incidence_jet_valid(candidate: Fraction) -> bool:
        return candidate > 0 and -n_a / cp_a + n_b * candidate / cp_b == 0

    inverted_dt_b_dt_a = 1 / correct_dt_b_dt_a
    correct_r = n_b * correct_dt_b_dt_a / n_a
    target_dt_dy = correct_dt_b_dt_a / n_a
    target_norm = norm(target_dt_dy, Fraction(0), n_b, a_b, beta_b)

    def proper_slope_valid(candidate: Fraction) -> bool:
        return candidate == cp_b / cp_a and -(candidate**2) == target_norm

    lapse_retained_r = (n_b / n_a) * (cp_b / cp_a)

    def completed_clock_valid(candidate: Fraction) -> bool:
        return candidate > 0 and candidate**2 == -target_norm

    # Static, conformal time-live, and moving-flat controls as callable endpoint laws.
    def proper_ratio(n_source: Fraction, n_target: Fraction, dt_target_dt_source: Fraction) -> Fraction:
        return n_target * dt_target_dt_source / n_source

    static_n_a, static_n_b = Fraction(2), Fraction(3, 2)
    static_expected = proper_ratio(static_n_a, static_n_b, Fraction(1))

    def static_valid(candidate: Fraction) -> bool:
        return candidate == static_expected == static_n_b / static_n_a

    conformal_n_a, conformal_n_b = Fraction(2), Fraction(5)
    conformal_expected = proper_ratio(conformal_n_a, conformal_n_b, Fraction(1))

    def conformal_valid(candidate: Fraction) -> bool:
        return candidate == conformal_expected == conformal_n_b / conformal_n_a

    exp_eta = Fraction(2)
    gamma = (exp_eta + 1 / exp_eta) / 2
    sinh_eta = (exp_eta - 1 / exp_eta) / 2
    emission, separation = Fraction(1, 3), Fraction(5, 3)
    reception = exp_eta * (emission + separation)
    delta_t = gamma * reception - emission
    delta_x = separation + sinh_eta * reception
    world_source = delta_t
    world_target = -gamma * delta_t + sinh_eta * delta_x

    def moving_flat_valid(candidate: Fraction) -> bool:
        return (
            (-delta_t**2 + delta_x**2) / 2 == 0
            and world_source + world_target * candidate == 0
            and candidate == exp_eta
        )

    # Later B->A return at different endpoint data, so Cplus-return and outgoing inverse are distinct
    # mutants rather than aliases.
    return_n_source, return_n_target = Fraction(4), Fraction(5)
    cm_source, cm_target = Fraction(9), Fraction(11)
    cp_source_later, cp_target_later = Fraction(7), Fraction(8)
    return_correct = cm_target / cm_source
    return_coordinate_slope = return_n_source * cm_target / (cm_source * return_n_target)

    def return_valid(candidate: Fraction) -> bool:
        coordinate = return_n_source * candidate / return_n_target
        return (
            candidate > 0
            and -return_n_source / cm_source + return_n_target * coordinate / cm_target == 0
            and coordinate == return_coordinate_slope
        )

    outgoing_inverse = cp_a / cp_b
    cplus_later_return = cp_target_later / cp_source_later

    # Typed semantic contract drawn from the registered premise ledger, then explicitly mutated.
    with HERE.joinpath("PREMISE_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        ledger = {row["item"]: row for row in csv.DictReader(handle, delimiter="\t")}
    ownership = {
        "null_status": ledger["null_branch"]["status"],
        "universal_protocol": False,
        "history_selected": False,
        "g176_status": ledger["completed_reciprocity"]["status"],
    }

    def ownership_valid(candidate: dict[str, object]) -> bool:
        return candidate == {
            "null_status": "CHOSE_QUERY_CONTROL",
            "universal_protocol": False,
            "history_selected": False,
            "g176_status": "WORKING_FOUNDATIONAL_CLARIFICATION",
        }

    universal_null = copy.deepcopy(ownership)
    universal_null["universal_protocol"] = True

    caught = {
        "implicit_endpoint_sign_reversal": catches_mutation(
            implicit_valid, correct_implicit, wrong_implicit_sign
        ),
        "world_function_tangent_orientation_swap": catches_mutation(
            tangent_orientation_valid,
            (correct_sigma_source, correct_sigma_target),
            (-correct_sigma_source, -correct_sigma_target),
        ),
        "affine_scale_applied_at_one_endpoint": catches_mutation(
            affine_ratio_valid, correct_affine_ratio, one_endpoint_affine_ratio
        ),
        "frequency_ratio_inverted": catches_mutation(
            frequency_valid, correct_frequency, inverted_frequency
        ),
        "right_null_uses_Cminus": catches_mutation(
            right_speed_valid, correct_right_speed, cminus_right_speed
        ),
        "shift_beta_dropped": catches_mutation(
            right_speed_valid, correct_right_speed, beta_dropped_speed
        ),
        "incidence_first_jet_inverted": catches_mutation(
            incidence_jet_valid, correct_dt_b_dt_a, inverted_dt_b_dt_a
        ),
        "coordinate_lapse_retained_in_proper_slope": catches_mutation(
            proper_slope_valid, correct_r, lapse_retained_r
        ),
        "completed_target_clock_replaced_by_lapse": catches_mutation(
            completed_clock_valid, correct_r, n_b
        ),
        "static_depth_sign_flipped": catches_mutation(
            static_valid, static_expected, 1 / static_expected
        ),
        "conformal_endpoint_order_reversed": catches_mutation(
            conformal_valid, conformal_expected, 1 / conformal_expected
        ),
        "moving_flat_rapidity_sign_flipped": catches_mutation(
            moving_flat_valid, exp_eta, 1 / exp_eta
        ),
        "future_return_called_outgoing_inverse": catches_mutation(
            return_valid, return_correct, outgoing_inverse
        ),
        "future_return_uses_Cplus": catches_mutation(
            return_valid, return_correct, cplus_later_return
        ),
        "null_promoted_to_universal_protocol": catches_mutation(
            ownership_valid, ownership, universal_null
        ),
    }
    assert all(caught.values()), [key for key, value in caught.items() if not value]
    return caught


if __name__ == "__main__":
    result = catches()
    print(json.dumps({"caught": result, "count": len(result)}, indent=2, sort_keys=True))
