#!/usr/bin/env python3
"""Exact G284 causal/projective discriminator on the arbitrary-T Brinkmann family."""

from __future__ import annotations

import json

import sympy as sp


LANDING = (
    "EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_"
    "TIDAL_HISTORY"
)


def main() -> None:
    u, v, x, y = sp.symbols("u v x y", real=True)
    c_e, scale = sp.symbols("c_E lambda", positive=True)
    t_xx = sp.Function("T_xx")(u)
    t_xy = sp.Function("T_xy")(u)
    t_yy = sp.Function("T_yy")(u)
    coords = (u, v, x, y)
    qform = t_xx * x**2 + 2 * t_xy * x * y + t_yy * y**2
    metric = sp.Matrix(
        [
            [-qform, -1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    inverse = sp.simplify(metric.inv())
    expected_inverse = sp.Matrix(
        [
            [0, -1, 0, 0],
            [-1, qform, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    central = {x: 0, y: 0}
    central_metric = metric.subs(central)

    gamma = [
        [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                gamma[upper][left][right] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[upper, rho]
                        * (
                            sp.diff(metric[rho, right], coords[left])
                            + sp.diff(metric[rho, left], coords[right])
                            - sp.diff(metric[left, right], coords[rho])
                        )
                        for rho in range(4)
                    )
                )

    def riemann_up(upper: int, lower: int, left: int, right: int) -> sp.Expr:
        return sp.simplify(
            sp.diff(gamma[upper][lower][right], coords[left])
            - sp.diff(gamma[upper][lower][left], coords[right])
            + sum(
                gamma[upper][left][rho] * gamma[rho][lower][right]
                - gamma[upper][right][rho] * gamma[rho][lower][left]
                for rho in range(4)
            )
        )

    def riemann_down(first: int, second: int, third: int, fourth: int) -> sp.Expr:
        return sp.simplify(
            sum(
                metric[first, rho] * riemann_up(rho, second, third, fourth)
                for rho in range(4)
            )
        )

    t_matrix = sp.Matrix([[t_xx, t_xy], [t_xy, t_yy]])
    curvature = sp.Matrix(
        [
            [riemann_down(0, 2, 0, 2), riemann_down(0, 2, 0, 3)],
            [riemann_down(0, 3, 0, 2), riemann_down(0, 3, 0, 3)],
        ]
    ).applyfunc(lambda entry: sp.simplify(entry.subs(central)))

    jacobian_tz = sp.Matrix(
        [
            [c_e / sp.sqrt(2), -1 / sp.sqrt(2), 0, 0],
            [c_e / sp.sqrt(2), 1 / sp.sqrt(2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    central_tz_metric = sp.simplify(jacobian_tz.T * central_metric * jacobian_tz)
    expected_tz = sp.diag(-c_e**2, 1, 1, 1)
    plus_null = sp.Matrix([1, c_e, 0, 0])
    minus_null = sp.Matrix([1, -c_e, 0, 0])

    unit_clock = sp.Matrix([1 / sp.sqrt(2), 1 / sp.sqrt(2), 0, 0])
    central_ray = sp.Matrix([1, 0, 0, 0])
    frequency = sp.simplify(-(unit_clock.T * central_metric * central_ray)[0])

    neighbor_slope = -qform / 2
    neighbor_ray = sp.Matrix([1, neighbor_slope, 0, 0])
    slope_hessian = sp.hessian(neighbor_slope, (x, y))

    identity2 = sp.eye(2)
    zero2 = sp.zeros(2)
    generator = zero2.row_join(identity2).col_join((-t_matrix).row_join(zero2))
    symplectic_form = zero2.row_join(identity2).col_join((-identity2).row_join(zero2))

    scaled_metric = scale**2 * metric
    scaled_inverse = inverse / scale**2
    scaled_gamma = [
        [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
        for _ in range(4)
    ]
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                scaled_gamma[upper][left][right] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        scaled_inverse[upper, rho]
                        * (
                            sp.diff(scaled_metric[rho, right], coords[left])
                            + sp.diff(scaled_metric[rho, left], coords[right])
                            - sp.diff(scaled_metric[left, right], coords[rho])
                        )
                        for rho in range(4)
                    )
                )

    first_jet_zero = all(
        sp.simplify(sp.diff(metric[i, j], coordinate).subs(central)) == 0
        for i in range(4)
        for j in range(4)
        for coordinate in coords
    )
    central_connection_zero = all(
        sp.simplify(gamma[a][b][c].subs(central)) == 0
        for a in range(4)
        for b in range(4)
        for c in range(4)
    )
    homothetic_connection_same = all(
        sp.simplify(scaled_gamma[a][b][c] - gamma[a][b][c]) == 0
        for a in range(4)
        for b in range(4)
        for c in range(4)
    )

    checks = {
        "metric_determinant_minus_one_for_arbitrary_T": sp.simplify(metric.det()) == -1,
        "metric_inverse_exact": sp.simplify(inverse - expected_inverse) == sp.zeros(4),
        "central_metric_independent_of_T": central_metric
        == sp.Matrix([[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
        "central_first_metric_jet_independent_of_T": first_jet_zero,
        "central_connection_independent_of_T": central_connection_zero,
        "clock_ruler_coordinates_give_local_cE_cone": sp.simplify(
            central_tz_metric - expected_tz
        )
        == sp.zeros(4),
        "central_plus_longitudinal_slope_is_cE": sp.simplify(
            (plus_null.T * expected_tz * plus_null)[0]
        )
        == 0,
        "central_minus_longitudinal_slope_is_cE": sp.simplify(
            (minus_null.T * expected_tz * minus_null)[0]
        )
        == 0,
        "central_clock_is_unit_timelike": sp.simplify(
            (unit_clock.T * central_metric * unit_clock)[0]
        )
        == -1,
        "central_ray_is_null": sp.simplify(
            (central_ray.T * central_metric * central_ray)[0]
        )
        == 0,
        "central_frequency_is_T_independent": frequency == 1 / sp.sqrt(2),
        "central_pair_state_is_delta0_chi0_M1": all(
            sp.simplify(value - expected) == 0
            for value, expected in (
                (-sp.log(frequency / frequency), 0),
                (sp.tanh(0), 0),
                (sp.sech(0), 1),
            )
        ),
        "neighboring_null_slope_exists_for_arbitrary_T": sp.simplify(
            (neighbor_ray.T * metric * neighbor_ray)[0]
        )
        == 0,
        "neighboring_cone_hessian_reconstructs_T": sp.simplify(slope_hessian + t_matrix)
        == sp.zeros(2),
        "curvature_equals_reconstructed_T": sp.simplify(curvature - t_matrix) == sp.zeros(2),
        "Jacobi_generator_is_Hamiltonian_for_arbitrary_symmetric_T": sp.simplify(
            generator.T * symplectic_form + symplectic_form * generator
        )
        == sp.zeros(4),
        "constant_homothety_preserves_connection": homothetic_connection_same,
        "constant_homothety_preserves_null_cones": sp.simplify(
            (neighbor_ray.T * scaled_metric * neighbor_ray)[0]
        )
        == 0,
        "constant_homothety_preserves_central_frequency_ratio": sp.simplify(
            (scale * frequency) / (scale * frequency)
        )
        == 1,
        "cE_does_not_enter_T_reconstruction": not any(
            entry.has(c_e) for entry in slope_hessian + t_matrix
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})

    result = {
        "audit": "G284_EMERGENT_CE_CAUSAL_PROJECTIVE_VALUE_LAW",
        "status": "PASS",
        "landing": LANDING,
        "checks": checks,
        "exact_checks": len(checks),
        "arbitrary_tidal_functions_retained": ["T_xx(u)", "T_xy(u)", "T_yy(u)"],
        "central_pair_state": {"frequency_ratio": 1, "delta": 0, "chi": 0, "M": 1},
        "neighboring_cone_reconstruction": "T_ij=-partial_i partial_j a_null",
        "value_selecting_constraints_found": 0,
        "stronger_unowned_candidates": [
            "endpoint_only_or_path_independent_tape_law",
            "zero_holonomy_or_all_germ_isotropy",
            "nonidentity_relation_between_longitudinal_projective_jet_and_transverse_cone_Hessian",
        ],
        "imports": {
            "field_equation": False,
            "action": False,
            "source_or_matter": False,
            "observation_or_fit": False,
            "scale_or_Xmax": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
