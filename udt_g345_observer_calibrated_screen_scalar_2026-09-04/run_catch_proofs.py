#!/usr/bin/env python3
"""Hostile mutation catch proofs for the bounded G345 evidence contract."""

from __future__ import annotations

import json
import os

import derive_screen_scalar as production


def close(left, right, tolerance=1.0e-8):
    return production.relative_error(left, right) <= tolerance


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    t_reference = 1.7
    t0, t1, t2 = 0.81, 2.2, 4.9
    rho, nu = 0.37, 1.31
    map10 = production.blocks(t1, t0, rho, nu, t_reference)
    map21 = production.blocks(t2, t1, rho, nu, t_reference)
    map20 = production.blocks(t2, t0, rho, nu, t_reference)
    omega0 = production.frequency(t0, rho, nu, t_reference)
    omega1 = production.frequency(t1, rho, nu, t_reference)
    omega2 = production.frequency(t2, rho, nu, t_reference)
    correct = production.scalar_density(map10, omega0, omega1)
    delta = production.raw_density(map10)
    catches = {}

    catches["omitted_source_frequency"] = not close(delta / omega1, correct)
    catches["omitted_target_frequency"] = not close(delta / omega0, correct)
    catches["used_frequency_ratio_only"] = not close(delta / (omega1 / omega0), correct)
    catches["used_sqrt_frequency_product_at_determinant_level"] = not close(
        delta / (omega0 * omega1) ** 0.5, correct
    )
    catches["multiplied_endpoint_frequencies"] = not close(delta * omega0 * omega1, correct)

    frame0 = [[-1.8, -0.3], [0.0, 0.7]]
    frame1 = [[1.4, 0.2], [-0.25, 0.8]]
    q0 = production.screen_metric_after(frame0)
    q1 = production.screen_metric_after(frame1)
    moved = production.change_screen_coordinates(map10, frame1, frame0)
    moved_correct = production.scalar_density(moved, omega0, omega1, q0, q1)
    moved_delta = production.raw_density(moved)
    wrong_without_q0 = moved_delta / (
        omega0 * omega1 * production.determinant_two(q1) ** 0.5
    )
    wrong_without_q1 = moved_delta / (
        omega0 * omega1 * production.determinant_two(q0) ** 0.5
    )
    catches["omitted_source_metric_screen_area"] = not close(wrong_without_q0, moved_correct)
    catches["omitted_target_metric_screen_area"] = not close(wrong_without_q1, moved_correct)

    wrong_mixed_transform = production.multiply(
        production.multiply(frame1, production.mixed_hessian(map10)),
        production.transpose(frame0),
    )
    catches["wrong_general_frame_tensor_transform"] = (
        production.matrix_error(wrong_mixed_transform, production.mixed_hessian(moved)) > 1.0e-4
    )
    catches["dropped_absolute_orientation"] = (
        production.determinant_two(production.mixed_hessian(moved)) < 0.0
        and moved_correct > 0.0
    )

    hessian = production.stationary_hessian(map21, map10, map20)
    target = production.scalar_density(map20, omega0, omega2)
    naive = production.scalar_density(map21, omega1, omega2) * correct
    catches["naive_multiplicative_composition"] = not close(naive, target)
    wrong_join = abs(production.determinant_two(hessian))
    wrong_sewn = production.scalar_density(map21, omega1, omega2) * correct / wrong_join
    catches["omitted_middle_frequency_square"] = not close(wrong_sewn, target)

    nu0 = t_reference ** (1.0 / 3.0) * t0 ** (2.0 / 3.0) / production.hnorm(
        t0, rho, t_reference
    )
    nu1 = t_reference ** (1.0 / 3.0) * t1 ** (2.0 / 3.0) / production.hnorm(
        t1, rho, t_reference
    )
    segment10_reset0 = production.blocks(t1, t0, rho, nu0, t_reference)
    segment21_reset1 = production.blocks(t2, t1, rho, nu1, t_reference)
    direct20_reset0 = production.blocks(t2, t0, rho, nu0, t_reference)
    ill_typed = production.compose_blocks(segment21_reset1, segment10_reset0)
    catches["mixed_independent_segment_gauges"] = (
        production.block_error(ill_typed, direct20_reset0) > 1.0e-4
    )

    hidden_reference = production.blocks(t1, t0, rho, nu, 1.0)
    catches["hidden_unit_reference_event"] = (
        production.block_error(hidden_reference, map10) > 1.0e-4
    )

    wrong_exponents = delta / (omega0 ** 0.5 * omega1 ** 1.5)
    reversed_wrong = delta / (omega1 ** 0.5 * omega0 ** 1.5)
    catches["asymmetric_frequency_exponents"] = not close(wrong_exponents, reversed_wrong)

    full_labels = ((0, 0, 0), (1, -1, 0), (-2, 3, 1), (4, 0, -5))
    catches["summed_or_selected_compact_lifts"] = full_labels[0:1] != full_labels

    forbidden = (
        "LIGHT_LAW", "FLUX", "LUMINOSITY", "PROBABILITY", "DISTANCE",
        "ROUTE_SELECTED", "POPULATION_SELECTED", "SCALE_SELECTED", "XMAX_SELECTED",
    )
    promoted = production.LANDING + "__LIGHT_LAW_FLUX_LUMINOSITY_DISTANCE_SCALE_SELECTED"
    catches["forbidden_physical_promotion"] = any(token in promoted for token in forbidden)

    wrong_landing = production.LANDING.replace("NO_LIGHT", "LIGHT")
    catches["negative_scope_token_removed"] = wrong_landing != production.LANDING

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
