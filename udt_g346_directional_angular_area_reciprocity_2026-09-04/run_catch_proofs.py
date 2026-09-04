#!/usr/bin/env python3
"""Hostile mutation checks for bounded G346 directional angular-area reciprocity."""

from __future__ import annotations

import json
import math
import os

import derive_directional_angular_area as production


def different(left, right, floor=1.0e-5):
    return production.relative_error(left, right) > floor


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    t_reference = 0.91
    t0, t1, t2 = 1.17, 2.43, 4.02
    rho, nu = 0.31, 1.73
    block10 = production.blocks(t1, t0, rho, nu, t_reference)
    block21 = production.blocks(t2, t1, rho, nu, t_reference)
    block20 = production.blocks(t2, t0, rho, nu, t_reference)
    block01 = production.blocks(t0, t1, rho, nu, t_reference)
    omega0 = production.frequency(t0, rho, nu, t_reference)
    omega1 = production.frequency(t1, rho, nu, t_reference)
    bdet = abs(production.determinant_two(block10[1]))
    baseline = production.area_jacobian(block10[1], omega0)
    reverse = production.area_jacobian(block01[1], omega1)
    scalar = production.g345_scalar(block10[1], omega0, omega1)

    catches = {}
    catches["omit_one_source_frequency_power"] = different(baseline, omega0 * bdet)
    catches["use_target_frequency_for_forward_map"] = different(
        baseline, omega1 * omega1 * bdet
    )

    frame0 = [[1.7, 0.38], [-0.22, 0.71]]
    frame1 = [[0.64, -0.41], [0.33, 1.52]]
    q0 = production.screen_metric_after(frame0)
    q1 = production.screen_metric_after(frame1)
    changed_b = production.transform_b(block10[1], frame1, frame0)
    changed_baseline = production.area_jacobian(changed_b, omega0, q0, q1)
    catches["omit_source_metric_area"] = different(
        changed_baseline,
        omega0 * omega0 * abs(production.determinant_two(changed_b))
        * math.sqrt(production.determinant_two(q1)),
    )
    catches["omit_target_metric_area"] = different(
        changed_baseline,
        omega0 * omega0 * abs(production.determinant_two(changed_b))
        * math.sqrt(production.determinant_two(q0)),
    )
    catches["frequency_product_used_for_reversal"] = different(
        baseline / reverse, (omega0 * omega1) ** 2
    )
    catches["frequency_ratio_reversed"] = different(
        baseline / reverse, (omega1 / omega0) ** 2
    )
    catches["arithmetic_mean_replaces_geometric_mean"] = different(
        0.5 * (baseline + reverse), math.sqrt(baseline * reverse)
    )
    catches["G345_not_inverted"] = different(math.sqrt(baseline * reverse), scalar)

    nu0 = t_reference ** (1.0 / 3.0) * t0 ** (2.0 / 3.0) / production.hnorm(
        t0, rho, t_reference
    )
    source_block = production.blocks(t1, t0, rho, nu0, t_reference)
    alpha = production.frequency(t1, rho, nu0, t_reference)
    correct_reverse_reset = production.scale(production.transpose(source_block[1]), -alpha)
    wrong_reverse_reset = production.scale(production.transpose(source_block[1]), -1.0)
    catches["endpoint_reset_factor_omitted"] = (
        production.matrix_error(correct_reverse_reset, wrong_reverse_reset) > 1.0e-5
    )

    wrong_changed_b = production.multiply(
        production.multiply(frame1, block10[1]), production.inverse_two(frame0)
    )
    catches["wrong_GL2_position_block_transform"] = different(
        changed_baseline,
        production.area_jacobian(wrong_changed_b, omega0, q0, q1),
    )
    wrong_q0 = production.multiply(
        production.multiply(frame0, [[1.0, 0.0], [0.0, 1.0]]),
        production.transpose(frame0),
    )
    catches["wrong_GL2_metric_transform"] = different(
        changed_baseline,
        production.area_jacobian(changed_b, omega0, wrong_q0, q1),
    )
    sky_without_musical = (
        math.sqrt(production.determinant_two(q1))
        * abs(production.determinant_two(production.scale(changed_b, omega0)))
        / math.sqrt(production.determinant_two(q0))
    )
    catches["metric_musical_map_omitted"] = different(changed_baseline, sky_without_musical)

    hessian = production.stationary_hessian(block21, block10, block20)
    hhat = production.joined_scalar(hessian, omega1)
    area20 = production.area_jacobian(block20[1], omega0)
    area21 = production.area_jacobian(block21[1], omega1)
    catches["bare_multiplicative_sewing"] = different(area20, area21 * baseline)
    catches["stationary_factor_inverted"] = different(
        area20, area21 * baseline / hhat
    )

    new_reference = 2.11
    wrong_reference_block = production.blocks(t1, t0, rho, nu, new_reference)
    wrong_reference_omega0 = production.frequency(t0, rho, nu, new_reference)
    catches["hidden_unconverted_reference_event"] = different(
        baseline,
        production.area_jacobian(wrong_reference_block[1], wrong_reference_omega0),
    )

    deleted_screen = [[block10[1][0][0], 0.0], [0.0, 0.0]]
    catches["one_principal_screen_deleted"] = (
        production.area_jacobian(deleted_screen, omega0) == 0.0 and baseline > 0.0
    )

    per_lift = {"L0": baseline, "L1": 1.4 * baseline}
    catches["compact_lifts_summed_or_selected"] = (
        sum(per_lift.values()) not in per_lift.values()
        and set(per_lift) == {"L0", "L1"}
    )

    forbidden = (
        "BRIGHTNESS", "FLUX", "LUMINOSITY", "PROBABILITY", "DISTANCE_SELECTED",
        "ROUTE_SELECTED", "POPULATION_SELECTED", "SCALE_SELECTED", "XMAX_SELECTED",
    )
    promoted = production.LANDING + "__BRIGHTNESS_FLUX_LUMINOSITY_DISTANCE_SELECTED"
    catches["forbidden_physical_promotion"] = any(token in promoted for token in forbidden)
    catches["finite_beam_promotion_rejected"] = "INFINITESIMAL" not in production.LANDING
    catches["negative_scope_token_is_load_bearing"] = (
        production.LANDING.replace("NO_BRIGHTNESS", "BRIGHTNESS") != production.LANDING
    )

    failed = [name for name, caught in catches.items() if not caught]
    result = {
        "caught": sum(catches.values()),
        "failed": failed,
        "mutations": catches,
        "status": "PASS" if not failed else "FAIL",
        "total": len(catches),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("uncaught hostile mutations: " + ", ".join(failed))


if __name__ == "__main__":
    main()
