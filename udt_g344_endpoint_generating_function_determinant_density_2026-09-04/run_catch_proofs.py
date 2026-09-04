#!/usr/bin/env python3
"""Hostile mutation catch proofs for the bounded G344 evidence contract."""

from __future__ import annotations

import json
import math
import os

import derive_endpoint_generator as production


TOL = 5.0e-9


def close(left, right, tolerance=TOL):
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def blocks_close(left, right, tolerance=TOL):
    return production.block_error(left, right) <= tolerance


def representative():
    t_reference = 1.7
    t0, t1, t2 = 0.83, 2.1, 4.4
    rho, nu = 0.37, 1.3
    return (
        production.blocks(t1, t0, rho, nu, t_reference),
        production.blocks(t2, t1, rho, nu, t_reference),
        production.blocks(t2, t0, rho, nu, t_reference),
        (t_reference, t0, t1, t2, rho, nu),
    )


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    block10, block21, block20, parameters = representative()
    t_reference, t0, t1, _, rho, nu = parameters
    x0 = [0.4, -0.7]
    x1 = [1.1, 0.2]
    x2 = [-0.3, 0.9]
    correct_target, correct_source, correct_negative_mixed = production.generator_coefficients(block10)
    correct_p1, correct_p0 = production.generator_momenta(block10, x1, x0)
    catches = {}

    r0 = production.rotate(0.31, False)
    r1 = production.rotate(-0.72, False)
    oblique = production.change_screen_bases(block10, r1, r0)
    correct_oblique_mixed = production.generator_coefficients(oblique)[2]
    wrong_cross_transpose = production.inverse_two(oblique[1])
    catches["wrong_cross_hessian_transpose"] = (
        production.matrix_error(wrong_cross_transpose, correct_oblique_mixed) > 1.0e-5
    )

    wrong_source_sign = [-value for value in correct_p0]
    catches["wrong_source_momentum_sign"] = production.vector_error(wrong_source_sign, correct_p0) > 1.0e-3

    b_inverse = production.inverse_two(block10[1])
    swapped_target = production.multiply(block10[0], b_inverse)
    swapped_source = production.multiply(b_inverse, block10[3])
    catches["swapped_A_D_hessians"] = max(
        production.matrix_error(swapped_target, correct_target),
        production.matrix_error(swapped_source, correct_source),
    ) > 1.0e-5

    missing_inverse = production.transpose(block10[1])
    catches["missing_B_inverse"] = production.matrix_error(missing_inverse, correct_negative_mixed) > 1.0e-4

    reflected = production.change_screen_bases(
        block10, production.rotate(0.2, True), production.rotate(-0.4, False)
    )
    reflected_oriented = production.determinant_two(production.generator_coefficients(reflected)[2])
    catches["dropped_density_absolute_value"] = reflected_oriented < 0.0 and production.density(reflected) > 0.0

    affine_scale = 2.4
    scaled = production.blocks(t1, t0, rho, affine_scale * nu, t_reference)
    catches["false_affine_invariance"] = not close(production.density(scaled), production.density(block10))

    independent_units = production.affine_endpoint_transform(block10, 1.9, 0.7)
    independent_four = production.assemble_four(independent_units)
    canonical_test = production.multiply(
        production.multiply(production.transpose(independent_four), production.J_FOUR),
        independent_four,
    )
    catches["independent_endpoint_units_called_canonical"] = (
        production.matrix_error(canonical_test, production.J_FOUR) > 1.0e-3
    )

    wrong_order = production.compose_blocks(block10, block21)
    catches["wrong_composition_order"] = not blocks_close(wrong_order, block20, 1.0e-7)

    _, stationary_hessian = production.stationary_middle(block21, block10, x2, x0)
    wrong_density_glue = production.density(block21) * production.density(block10)
    correct_density_glue = wrong_density_glue / abs(production.determinant_two(stationary_hessian))
    catches["omitted_stationary_hessian"] = (
        not close(wrong_density_glue, production.density(block20), 1.0e-7)
        and close(correct_density_glue, production.density(block20))
    )

    hidden_reference = production.blocks(t1, t0, rho, nu, 1.0)
    catches["hidden_unit_reference_scale"] = not blocks_close(hidden_reference, block10, 1.0e-7)

    longitudinal = production.blocks(t1, t0, 1.0, nu, t_reference)
    lost_principal = tuple([list(row) for row in block] for block in longitudinal)
    lost_principal[1][1][1] = 0.0
    catches["lost_longitudinal_screen_direction"] = (
        production.determinant_two(longitudinal[1]) != 0.0
        and production.determinant_two(lost_principal[1]) == 0.0
    )

    mixed_screen = tuple([list(row) for row in block] for block in block10)
    mixed_screen[1][0][1] = 0.125
    catches["injected_screen_mixing"] = production.matrix_error(mixed_screen[1], block10[1]) > 1.0e-3

    full_labels = ((0, 0, 0), (1, -1, 0), (-2, 3, 1), (4, 0, -5))
    deleted_labels = full_labels[:-1]
    catches["deleted_compact_path_label"] = deleted_labels != full_labels

    forbidden = ("LUMINOSITY", "DISTANCE", "PROBABILITY", "SCALE_SELECTED")
    promoted_landing = production.LANDING + "__LUMINOSITY_DISTANCE_PROBABILITY_SCALE_SELECTED"
    catches["forbidden_physical_promotion"] = any(token in promoted_landing for token in forbidden)

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
