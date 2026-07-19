#!/usr/bin/env python3
"""Exact CPU algebra for the angular-toric closure selector audit."""

from __future__ import annotations

import argparse
import json
import math
import platform

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


VERDICT = (
    "S3_AND_FREE_HOPF_ACTION_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES; "
    "RECIPROCITY_CSN_FINITE_CELL_AND_BOOTSTRAP_DO_NOT_SELECT_THOSE_PREMISES; "
    "FIRST_MISSING_GATE_TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY; "
    "CONDITIONAL_SECOND_GATE_FINITE_CELL_CAP_COMPLETION_OPEN"
)


def simplify(expr):
    if isinstance(expr, sp.MatrixBase):
        return expr.applyfunc(lambda item: sp.trigsimp(sp.simplify(item)))
    return sp.trigsimp(sp.simplify(expr))


def require_zero(name: str, expr) -> str:
    value = simplify(expr)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    if not good:
        raise AssertionError(f"{name}: expected zero, got {value}")
    return "PASS"


def text(expr) -> str:
    return str(simplify(expr))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    eta, phi = sp.symbols("eta phi", real=True)
    scale_f, scale_g = sp.symbols("F G", positive=True)

    # Genericity: every positive diagonal orbit block has reciprocal determinant-one form.
    orbit = sp.diag(scale_f**2, scale_g**2)
    normalized_orbit = sp.simplify(orbit / (scale_f * scale_g))
    generic_reciprocal_check = require_zero(
        "generic_reciprocal_orbit",
        normalized_orbit - sp.diag(scale_f / scale_g, scale_g / scale_f),
    )
    phi_from_ratio = sp.log(scale_g / scale_f) / 2
    ratio_realization_check = require_zero(
        "ratio_realizes_phi",
        normalized_orbit - sp.diag(sp.exp(-2 * phi_from_ratio), sp.exp(2 * phi_from_ratio)),
    )

    # Integral collapse-cycle lattice.  Columns are primitive cycles at the two endpoints.
    cycle_examples = {
        "p0_same_cycle": sp.Matrix([[1, 1], [1, 1]]),
        "p1_axis_exchange": sp.Matrix([[1, 0], [0, 1]]),
        "p3_mirror_exchange": sp.Matrix([[2, 1], [1, 2]]),
        "p5_mirror_exchange": sp.Matrix([[3, 2], [2, 3]]),
    }
    determinant_classes = {name: abs(int(matrix.det())) for name, matrix in cycle_examples.items()}
    if determinant_classes != {
        "p0_same_cycle": 0,
        "p1_axis_exchange": 1,
        "p3_mirror_exchange": 3,
        "p5_mirror_exchange": 5,
    }:
        raise AssertionError(determinant_classes)
    primitivity = {
        name: [math.gcd(abs(int(column[0])), abs(int(column[1]))) for column in matrix.columnspace()]
        for name, matrix in cycle_examples.items()
    }
    if any(value != 1 for values in primitivity.values() for value in values):
        raise AssertionError(primitivity)
    smith_classes = {}
    for name, matrix in cycle_examples.items():
        smith = smith_normal_form(matrix, domain=ZZ)
        smith_classes[name] = [abs(int(smith[index, index])) for index in range(2)]
    if smith_classes != {
        "p0_same_cycle": [1, 0],
        "p1_axis_exchange": [1, 1],
        "p3_mirror_exchange": [1, 3],
        "p5_mirror_exchange": [1, 5],
    }:
        raise AssertionError(smith_classes)
    additional_mirror_cycles = {
        "p7": ((4, 3), (3, 4)),
        "p8": ((3, 1), (1, 3)),
        "p9": ((5, 4), (4, 5)),
        "p15": ((4, 1), (1, 4)),
    }
    additional_mirror_determinants = {
        name: abs(left[0] * right[1] - left[1] * right[0])
        for name, (left, right) in additional_mirror_cycles.items()
    }
    if additional_mirror_determinants != {"p7": 7, "p8": 8, "p9": 9, "p15": 15}:
        raise AssertionError(additional_mirror_determinants)
    additional_mirror_primitivity = {
        name: [math.gcd(abs(x), abs(y)) for x, y in (left, right)]
        for name, (left, right) in additional_mirror_cycles.items()
    }
    if any(value != 1 for values in additional_mirror_primitivity.values() for value in values):
        raise AssertionError(additional_mirror_primitivity)
    additional_mirror_smith = {}
    for name, (left, right) in additional_mirror_cycles.items():
        matrix = sp.Matrix([[left[0], right[0]], [left[1], right[1]]])
        smith = smith_normal_form(matrix, domain=ZZ)
        additional_mirror_smith[name] = [abs(int(smith[index, index])) for index in range(2)]
    if additional_mirror_smith != {
        "p7": [1, 7], "p8": [1, 8], "p9": [1, 9], "p15": [1, 15],
    }:
        raise AssertionError(additional_mirror_smith)
    axis_cap_determinant_check = require_zero(
        "opposing_axis_caps_det_one",
        sp.det(sp.Matrix([[1, 0], [0, 1]])) - 1,
    )

    # Round witness and a non-round mirror-symmetric S3 family with the same orbit block.
    c, s = sp.cos(eta), sp.sin(eta)
    epsilon = sp.Rational(1, 3)
    radial_h = 1 + epsilon * sp.sin(2 * eta) ** 2
    round_metric = sp.diag(1, c**2, s**2)
    nonround_metric = sp.diag(radial_h**2, c**2, s**2)
    round_orbit = round_metric[1:3, 1:3]
    nonround_orbit = nonround_metric[1:3, 1:3]
    round_normalized_orbit = sp.simplify(round_orbit / (c * s))
    nonround_normalized_orbit = sp.simplify(nonround_orbit / (c * s))
    same_orbit_check = require_zero(
        "round_nonround_same_normalized_orbit",
        round_normalized_orbit - nonround_normalized_orbit,
    )
    mirror_radial_check = require_zero(
        "nonround_mirror_symmetry",
        radial_h.subs(eta, sp.pi / 2 - eta) - radial_h,
    )
    reciprocal_eta = sp.atan(sp.exp(2 * phi))
    reciprocal_orbit_check = require_zero(
        "hopf_orbit_reciprocal_depth",
        round_normalized_orbit.subs(eta, reciprocal_eta)
        - sp.diag(sp.exp(-2 * phi), sp.exp(2 * phi)),
    )

    # Smooth primitive cap slopes in proper radial distance for both metrics.
    cap_data = {
        "H_at_left": sp.simplify(radial_h.subs(eta, 0)),
        "H_prime_left": sp.simplify(sp.diff(radial_h, eta).subs(eta, 0)),
        "collapse_slope_left": sp.simplify(sp.diff(s, eta).subs(eta, 0) / radial_h.subs(eta, 0)),
        "spectator_slope_left": sp.simplify(sp.diff(c, eta).subs(eta, 0) / radial_h.subs(eta, 0)),
        "H_at_right": sp.simplify(radial_h.subs(eta, sp.pi / 2)),
        "H_prime_right": sp.simplify(sp.diff(radial_h, eta).subs(eta, sp.pi / 2)),
        "collapse_slope_right": sp.simplify(-sp.diff(c, eta).subs(eta, sp.pi / 2) / radial_h.subs(eta, sp.pi / 2)),
        "spectator_slope_right": sp.simplify(sp.diff(s, eta).subs(eta, sp.pi / 2) / radial_h.subs(eta, sp.pi / 2)),
    }
    if cap_data != {
        "H_at_left": 1,
        "H_prime_left": 0,
        "collapse_slope_left": 1,
        "spectator_slope_left": 0,
        "H_at_right": 1,
        "H_prime_right": 0,
        "collapse_slope_right": 1,
        "spectator_slope_right": 0,
    }:
        raise AssertionError(cap_data)
    left_cap_all_order_parity_check = require_zero(
        "left_cap_all_order_parity",
        sp.Matrix([
            radial_h.subs(eta, -eta) - radial_h,
            c.subs(eta, -eta) - c,
            s.subs(eta, -eta) + s,
        ]),
    )
    cap_x = sp.symbols("cap_x", real=True)
    right_h = sp.trigsimp(radial_h.subs(eta, sp.pi / 2 - cap_x))
    right_collapse = sp.trigsimp(c.subs(eta, sp.pi / 2 - cap_x))
    right_spectator = sp.trigsimp(s.subs(eta, sp.pi / 2 - cap_x))
    right_cap_all_order_parity_check = require_zero(
        "right_cap_all_order_parity",
        sp.Matrix([
            right_h.subs(cap_x, -cap_x) - right_h,
            right_collapse.subs(cap_x, -cap_x) + right_collapse,
            right_spectator.subs(cap_x, -cap_x) - right_spectator,
        ]),
    )

    # CSN cannot remove the changed full-metric radial/orbit ratio.
    round_radial_orbit_ratio = sp.simplify(round_metric[0, 0] / (c * s))
    nonround_radial_orbit_ratio = sp.simplify(nonround_metric[0, 0] / (c * s))
    ratio_difference_midpoint = sp.simplify(
        (nonround_radial_orbit_ratio - round_radial_orbit_ratio).subs(eta, sp.pi / 4)
    )
    if ratio_difference_midpoint != sp.Rational(14, 9):
        raise AssertionError(ratio_difference_midpoint)
    angular_conformal_factor = sp.simplify(nonround_metric[1, 1] / round_metric[1, 1])
    radial_conformal_factor = sp.simplify(nonround_metric[0, 0] / round_metric[0, 0])
    nonconformal_check = require_zero(
        "nonround_not_full_conformal_at_midpoint",
        (radial_conformal_factor - angular_conformal_factor).subs(eta, sp.pi / 4)
        - sp.Rational(7, 9),
    )

    # Weighted circle actions: endpoint stabilizers have orders |m| and |n|.
    effective_weights = [
        (m, n) for m in range(-5, 6) for n in range(-5, 6)
        if (m, n) != (0, 0) and math.gcd(abs(m), abs(n)) == 1
    ]

    def endpoint_stabilizer_order(weight: int) -> int | str:
        return "U1" if weight == 0 else abs(weight)

    stabilizer_orders = {
        (m, n): (endpoint_stabilizer_order(m), endpoint_stabilizer_order(n))
        for m, n in effective_weights
    }
    free_weights = sorted(
        pair for pair, orders in stabilizer_orders.items() if orders == (1, 1)
    )
    if free_weights != [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        raise AssertionError(free_weights)
    exceptional_examples = {
        str(pair).replace(" ", ""): list(stabilizer_orders[pair])
        for pair in [(1, 2), (2, 1), (2, 3)]
    }
    if exceptional_examples != {"(1,2)": [1, 2], "(2,1)": [2, 1], "(2,3)": [2, 3]}:
        raise AssertionError(exceptional_examples)

    # Derive common-scale-independent connections and unit classes for all free sign choices.
    omega2 = sp.symbols("Omega2", positive=True)
    f, g = c**2, s**2
    connection_data = {}
    for m, n in free_weights:
        denominator = sp.simplify(m**2 * omega2 * f + n**2 * omega2 * g)
        coefficients = sp.Matrix([
            sp.simplify(m * omega2 * f / denominator),
            sp.simplify(n * omega2 * g / denominator),
        ])
        common_scale_check = require_zero(
            f"common_scale_cancellation_{m}_{n}",
            coefficients - sp.Matrix([m * f, n * g]),
        )
        density = sp.simplify(coefficients[1] * sp.diff(coefficients[0], eta)
                              - coefficients[0] * sp.diff(coefficients[1], eta))
        integral = sp.simplify(sp.integrate(density, (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2)
        charge = sp.simplify(-integral / (4 * sp.pi**2))
        if charge != m * n:
            raise AssertionError((m, n, integral, charge))
        connection_data[f"({m},{n})"] = {
            "coefficients": [text(item) for item in coefficients],
            "integral_A_wedge_dA": text(integral),
            "registered_charge": text(charge),
            "common_scale_check": common_scale_check,
        }

    # A compact no-cap torus countermodel: s-circle x T2 with odd periodic phi=sin(s).
    sigma = sp.symbols("sigma", real=True)
    phi_periodic = sp.sin(sigma)
    torus3_metric = sp.diag(1, sp.exp(-2 * phi_periodic), sp.exp(2 * phi_periodic))
    swap = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    reflected = torus3_metric.subs(sigma, -sigma)
    torus_mirror_check = require_zero(
        "finite_no_cap_mirror_isometry",
        swap.T * reflected * swap - torus3_metric,
    )
    torus_determinant_check = require_zero(
        "finite_no_cap_positive_determinant",
        sp.det(torus3_metric) - 1,
    )
    seal_parity_check = require_zero(
        "finite_no_cap_phi_odd_and_zero_at_seal",
        sp.Matrix([
            phi_periodic.subs(sigma, -sigma) + phi_periodic,
            phi_periodic.subs(sigma, 0),
        ]),
    )
    finite_interval_endpoint_coefficients = [
        text(sp.exp(-2 * phi_periodic).subs(sigma, value))
        for value in (-sp.pi / 2, sp.pi / 2)
    ] + [
        text(sp.exp(2 * phi_periodic).subs(sigma, value))
        for value in (-sp.pi / 2, sp.pi / 2)
    ]
    if any(value == "0" for value in finite_interval_endpoint_coefficients):
        raise AssertionError(finite_interval_endpoint_coefficients)

    # Positive CSN holds on the principal region; the round orbit factor tends to zero at both caps.
    round_common_phi = 1 / (2 * sp.cosh(2 * phi))
    csn_endpoint_limits = [
        sp.limit(round_common_phi, phi, -sp.oo),
        sp.limit(round_common_phi, phi, sp.oo),
    ]
    if csn_endpoint_limits != [0, 0] or round_common_phi.subs(phi, 0) <= 0:
        raise AssertionError(csn_endpoint_limits)

    checks = {
        "generic_positive_orbit_block_has_reciprocal_normal_form": generic_reciprocal_check,
        "ratio_defines_reciprocal_depth": ratio_realization_check,
        "collapse_cycle_determinant_examples": "PASS",
        "collapse_cycles_are_primitive": "PASS",
        "smith_lattice_quotient_classes": "PASS",
        "additional_mirror_determinant_examples": "PASS",
        "additional_mirror_cycles_are_primitive": "PASS",
        "additional_mirror_smith_classes": "PASS",
        "opposing_axis_caps_have_determinant_one": axis_cap_determinant_check,
        "round_and_nonround_share_normalized_orbit_block": same_orbit_check,
        "nonround_witness_has_exchange_mirror": mirror_radial_check,
        "hopf_orbit_is_reciprocal_in_phi": reciprocal_orbit_check,
        "round_and_nonround_cap_regularity": "PASS",
        "left_cap_all_order_analytic_parity": left_cap_all_order_parity_check,
        "right_cap_all_order_analytic_parity": right_cap_all_order_parity_check,
        "nonround_csn_invariant_ratio_differs": "PASS",
        "nonround_full_metric_not_conformal_to_round": nonconformal_check,
        "free_weight_classification": "PASS",
        "weighted_action_stabilizer_examples": "PASS",
        "free_weight_connections_and_charges": "PASS",
        "finite_no_cap_torus_mirror_isometry": torus_mirror_check,
        "finite_no_cap_torus_positive_determinant": torus_determinant_check,
        "finite_no_cap_phi_seal_parity": seal_parity_check,
        "finite_interval_orbit_coefficients_do_not_collapse": "PASS",
        "positive_csn_common_factor_vanishes_at_caps": "PASS",
    }
    if set(checks.values()) != {"PASS"}:
        raise AssertionError(checks)

    result = {
        "status": "PASS",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "generic_normalized_orbit": text(normalized_orbit),
            "reciprocal_depth_from_orbit_ratio": text(phi_from_ratio),
            "collapse_determinant_classes": determinant_classes,
            "collapse_smith_classes": smith_classes,
            "additional_mirror_determinants": additional_mirror_determinants,
            "additional_mirror_primitivity": additional_mirror_primitivity,
            "additional_mirror_smith_classes": additional_mirror_smith,
            "mirror_examples_are_primitive": primitivity,
            "round_metric": text(round_metric),
            "nonround_metric": text(nonround_metric),
            "nonround_radial_factor": text(radial_h),
            "cap_regularity": {key: text(value) for key, value in cap_data.items()},
            "left_cap_parity": {"H": "even", "collapse": "odd", "spectator": "even"},
            "right_cap_parity": {"H": "even", "collapse": "odd", "spectator": "even"},
            "radial_orbit_ratio_difference_at_midpoint": text(ratio_difference_midpoint),
            "free_effective_weights": [list(pair) for pair in free_weights],
            "exceptional_stabilizer_orders": exceptional_examples,
            "zero_weight_stabilizer_orders": {
                "(0,1)": list(stabilizer_orders[(0, 1)]),
                "(1,0)": list(stabilizer_orders[(1, 0)]),
            },
            "free_weight_connection_data": connection_data,
            "finite_no_cap_metric": text(torus3_metric),
            "finite_no_cap_phi": text(phi_periodic),
            "finite_interval_endpoint_orbit_coefficients": finite_interval_endpoint_coefficients,
            "round_common_scale_cap_limits": [text(value) for value in csn_endpoint_limits],
        },
        "classification": {
            "global_diagonal_two_eigencaps": "S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES",
            "exchange_mirror_without_eigencap_rule": "TOPOLOGY_UNDERDETERMINED",
            "general_toric_completion": "P0_P1_LENS_P_GREATER_1_INCOMPLETE_AND_NONCOMPACT_FAMILIES_REMAIN",
            "round_completion": "NOT_UNIQUE_EVEN_WITHIN_SMOOTH_MIRROR_S3_CLASS",
            "free_smooth_circle_quotient": "WEIGHTS_ABS_M_EQUALS_ABS_N_EQUALS_1_UNIQUE_CONDITIONAL",
            "registered_udt_selection": "SPATIAL_TORUS_SLOT_CAP_AND_QUOTIENT_NOT_SELECTED",
            "first_missing_gate": "TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY",
            "conditional_second_gate": "FINITE_CELL_CAP_COMPLETION",
        },
        "maximum_verdict": VERDICT,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"DERIVATION PASS {len(checks)}/{len(checks)}")
    print(VERDICT)


if __name__ == "__main__":
    main()
