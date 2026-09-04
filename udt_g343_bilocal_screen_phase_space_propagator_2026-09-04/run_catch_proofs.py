#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G343 evidence contract."""

from __future__ import annotations

import json
import math
import os
import sys

sys.dont_write_bytecode = True

from derive_bilocal_propagator import (  # noqa: E402
    J,
    identity,
    max_relative_error,
    multiply,
    propagator,
    scalar_transfer,
    tide_q,
    transpose,
    transverse_power_transfer,
)


LANDING = (
    "FULL_BILOCAL_PHASE_SPACE_PROPAGATOR_CLOSES__EXACT_COMPOSITION_SYMPLECTICITY"
    "__COMMON_AFFINE_INVERSE_AND_SOURCE_NORMALIZED_FREQUENCY_RECIPROCITY"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def validate(state: dict[str, object]) -> tuple[bool, str]:
    if state["reference_event_explicit"] is not True:
        return False, "hidden_unit_reference_scale"
    if len(set(state["affine_nus"])) != 1:
        return False, "intermediate_affine_renormalization"
    if max_relative_error(state["composition_candidate"], state["composition_expected"]) > 1e-11:
        return False, "wrong_composition_order"
    if max_relative_error(multiply(state["reverse_candidate"], state["forward"]), identity()) > 1e-11:
        return False, "reversal_without_inverse"
    if max(abs(state["b_reverse"][i] + state["b_forward"][i]) for i in range(2)) > 1e-11:
        return False, "wrong_bilocal_B_sign"
    if max(abs(state["ordered_blocks"][i] - state["expected_blocks"][i]) for i in range(2)) > 1e-11:
        return False, "swapped_A_D_blocks"
    if not state["tide_entries"][0] < 0.0 < state["tide_entries"][1]:
        return False, "curvature_sign_flip"
    if max(abs(value) for value in state["cross_screen_entries"]) > 1e-13:
        return False, "injected_screen_mixing"
    if max(abs(value - 1.0) for value in state["channel_wronskians"]) > 1e-11:
        return False, "broken_wronskian"
    if state["longitudinal_limit_error"] > 1e-11:
        return False, "lost_longitudinal_limit"
    if state["transverse_limit_error"] > 1e-11:
        return False, "lost_transverse_limit"
    if state["retained_path_labels"] != state["expected_path_labels"]:
        return False, "deleted_compact_path_label"
    if state["physical_promotion"] is not False:
        return False, "physical_readout_promotion"
    return True, "ok"


def baseline_state() -> dict[str, object]:
    t0, t1, t2 = 0.9, 1.7, 3.2
    rho, nu, t_reference = 0.37, 1.4, 0.8
    m10 = propagator(t1, t0, rho, nu, t_reference)
    m21 = propagator(t2, t1, rho, nu, t_reference)
    m20 = propagator(t2, t0, rho, nu, t_reference)
    m01 = propagator(t0, t1, rho, nu, t_reference)
    par = scalar_transfer(t1, t0, rho, nu, t_reference, "parallel")
    az = scalar_transfer(t1, t0, rho, nu, t_reference, "azimuth")

    affine_delta = (
        1.5 * t_reference ** (1.0 / 3.0)
        * (t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)) / nu
    )
    free = [
        [1.0, 0.0, affine_delta, 0.0],
        [0.0, 1.0, 0.0, affine_delta],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    longitudinal_error = max_relative_error(
        propagator(t1, t0, 1.0, nu, t_reference), free
    )

    trans = propagator(t1, t0, 0.0, nu, t_reference)
    transverse_constant = nu * t_reference ** (2.0 / 3.0)
    trans_par = transverse_power_transfer(
        t1, t0, transverse_constant, "parallel"
    )
    trans_az = transverse_power_transfer(
        t1, t0, transverse_constant, "azimuth"
    )
    trans_expected = [
        [trans_par[0][0], 0.0, trans_par[0][1], 0.0],
        [0.0, trans_az[0][0], 0.0, trans_az[0][1]],
        [trans_par[1][0], 0.0, trans_par[1][1], 0.0],
        [0.0, trans_az[1][0], 0.0, trans_az[1][1]],
    ]
    q = tide_q(t1, rho, nu, t_reference)
    labels = ((0, 0, 0), (1, 0, 0), (-1, 2, 0), (3, -1, 4))
    return {
        "reference_event_explicit": True,
        "affine_nus": (nu, nu, nu),
        "composition_candidate": m20,
        "composition_expected": multiply(m21, m10),
        "forward": m10,
        "reverse_candidate": m01,
        "b_forward": (m10[0][2], m10[1][3]),
        "b_reverse": (m01[0][2], m01[1][3]),
        "ordered_blocks": (m10[0][0], m10[2][2]),
        "expected_blocks": (m10[0][0], m10[2][2]),
        "tide_entries": (-q, q),
        "cross_screen_entries": (
            m10[0][1], m10[0][3], m10[1][0], m10[1][2],
            m10[2][1], m10[2][3], m10[3][0], m10[3][2],
        ),
        "channel_wronskians": (
            par[0][0] * par[1][1] - par[0][1] * par[1][0],
            az[0][0] * az[1][1] - az[0][1] * az[1][0],
        ),
        "longitudinal_limit_error": longitudinal_error,
        "transverse_limit_error": max_relative_error(trans, trans_expected),
        "retained_path_labels": labels,
        "expected_path_labels": labels,
        "physical_promotion": False,
        "symplectic_control": max_relative_error(multiply(multiply(transpose(m10), J), m10), J),
    }


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    baseline = baseline_state()
    ok, message = validate(baseline)
    if not ok or baseline["symplectic_control"] > 1e-11:
        raise AssertionError(f"baseline failed: {message}")

    wrong_order = multiply(
        propagator(1.7, 0.9, 0.37, 1.4, 0.8),
        propagator(3.2, 1.7, 0.37, 1.4, 0.8),
    )
    mutations = (
        ("hidden_unit_reference_scale", "reference_event_explicit", False),
        ("intermediate_affine_renormalization", "affine_nus", (1.4, 1.2, 1.4)),
        ("wrong_composition_order", "composition_candidate", wrong_order),
        ("reversal_without_inverse", "reverse_candidate", baseline["forward"]),
        ("wrong_bilocal_B_sign", "b_reverse", baseline["b_forward"]),
        ("swapped_A_D_blocks", "ordered_blocks", tuple(reversed(baseline["ordered_blocks"]))),
        ("curvature_sign_flip", "tide_entries", tuple(reversed(baseline["tide_entries"]))),
        ("injected_screen_mixing", "cross_screen_entries", (0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0)),
        ("broken_wronskian", "channel_wronskians", (1.0, 0.8)),
        ("lost_longitudinal_limit", "longitudinal_limit_error", 0.1),
        ("lost_transverse_limit", "transverse_limit_error", 0.1),
        ("deleted_compact_path_label", "retained_path_labels", baseline["retained_path_labels"][:-1]),
        ("physical_readout_promotion", "physical_promotion", True),
    )
    checks: dict[str, bool] = {}
    messages: dict[str, str] = {}
    for expected, key, value in mutations:
        mutant = dict(baseline)
        mutant[key] = value
        passed, failure = validate(mutant)
        checks[expected] = not passed and failure == expected
        messages[expected] = failure

    result = {
        "all_passed": all(checks.values()),
        "catches_passed": sum(checks.values()),
        "catches_total": len(checks),
        "checks": checks,
        "landing": LANDING,
        "messages": messages,
        "validator_shared_by_baseline_and_mutants": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
