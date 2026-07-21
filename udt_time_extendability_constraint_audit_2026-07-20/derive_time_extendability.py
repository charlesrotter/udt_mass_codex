#!/usr/bin/env python3
"""Exact kinematic time-extendability algebra for the complete UDT reciprocal lifts."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def block_diagonal(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    output = sp.zeros(left.rows + right.rows)
    output[: left.rows, : left.cols] = left
    output[left.rows :, left.cols :] = right
    return output


def full_metric(base: sp.Matrix, cross: sp.Matrix, angular: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(angular))


def pair_invariant(metric: sp.Matrix, generator: sp.Matrix) -> sp.Expr:
    return sp.factor(sp.trace(metric.inv() * generator.T * metric * generator))


def linear_system_ranks(equation_matrices: list[sp.Matrix], variables: tuple[sp.Symbol, ...]):
    equations = []
    for matrix in equation_matrices:
        equations.extend(list(matrix))
    coefficients, rhs = sp.linear_eq_to_matrix(equations, variables)
    return coefficients.rank(), coefficients.row_join(rhs).rank(), len(variables) - coefficients.rank()


def positive_affine_on_unit_interval(expression: sp.Expr, parameter: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), parameter)
    return polynomial.degree() <= 1 and bool(expression.subs(parameter, 0) > 0) and bool(
        expression.subs(parameter, 1) > 0
    )


def main() -> None:
    checks: dict[str, str] = {}
    s = sp.symbols("s", real=True)
    k, dk, sigma = sp.symbols("k dk sigma", real=True)
    epsilon = sp.Rational(1, 10)

    H = sp.Matrix([[1, -k], [-k, 1]])
    H_k = H.diff(k)
    F = sp.Matrix([[0, 1], [1, 0]])
    L2 = sp.diag(-1, 1)
    L4 = sp.diag(-1, 1, 0, 0)

    lifts = {
        "PLUS_IDENTITY": {
            "A": sp.eye(2),
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
            "orientation": -1,
            "metric_seal_connection_dimension": 3,
            "positive_factors": [k + 1, 25 * k - 24, k - 1, 50 * k - 49],
        },
        "MINUS_IDENTITY": {
            "A": -sp.eye(2),
            "C": sp.Matrix([[epsilon, epsilon], [-epsilon, -epsilon]]),
            "orientation": -1,
            "metric_seal_connection_dimension": 3,
            "positive_factors": [k - 1, 25 * k + 24, k + 1, 50 * k + 49],
        },
        "AXIS_REFLECTION": {
            "A": sp.diag(1, -1),
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, -epsilon]]),
            "orientation": 1,
            "metric_seal_connection_dimension": 2,
            "positive_factors": [k - 1, k + 1, 50 * k - 49, 50 * k + 49],
        },
        "HOPF_EXCHANGE_LOCAL": {
            "A": F,
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
            "orientation": 1,
            "metric_seal_connection_dimension": 2,
            "positive_factors": [k + 1, 25 * k - 24, k - 1, 50 * k - 49],
        },
    }

    expected_determinants = {
        "PLUS_IDENTITY": -(k + 1) * (25 * k - 24) / 25,
        "MINUS_IDENTITY": -(k - 1) * (25 * k + 24) / 25,
        "AXIS_REFLECTION": -(50 * k - 49) * (50 * k + 49) / 2500,
        "HOPF_EXCHANGE_LOCAL": -(k + 1) * (25 * k - 24) / 25,
    }
    expected_schur = {
        "PLUS_IDENTITY": (
            (50 * k - 49) / (50 * (k - 1)),
            (25 * k - 24) / (25 * (k - 1)),
        ),
        "MINUS_IDENTITY": (
            (50 * k + 49) / (50 * (k + 1)),
            (25 * k + 24) / (25 * (k + 1)),
        ),
        "AXIS_REFLECTION": (
            (50 * k - 49) / (50 * (k - 1)),
            (50 * k - 49) * (50 * k + 49) / (2500 * (k - 1) * (k + 1)),
        ),
        "HOPF_EXCHANGE_LOCAL": (
            (50 * k - 49) / (50 * (k - 1)),
            (25 * k - 24) / (25 * (k - 1)),
        ),
    }

    trajectories = {
        "LOWER_HISTORY": 2 + s / 10,
        "UPPER_HISTORY": 3 + s / 10,
    }
    gamma_symbols = sp.symbols("gamma0:16")
    gamma = sp.Matrix(4, 4, gamma_symbols)
    history_results: dict[str, dict[str, object]] = {}
    lift_results: dict[str, dict[str, object]] = {}
    connection_results: dict[str, dict[str, object]] = {}

    for name, data in lifts.items():
        angular = data["A"]
        cross = data["C"]
        seal = block_diagonal(F, angular)
        metric = full_metric(H, cross, sp.eye(2))
        metric_k = metric.diff(k)

        require_zero(f"{name}_seal_involution", seal**2 - sp.eye(4), checks)
        require_zero(f"{name}_metric_isometry", seal.T * metric * seal - metric, checks)
        require_zero(f"{name}_reciprocal_inversion", seal * L4 * seal + L4, checks)
        require(f"{name}_nonzero_cross", cross != sp.zeros(2), checks)
        require(f"{name}_orientation", seal.det() == data["orientation"], checks)
        require_zero(
            f"{name}_differentiated_isometry_generic",
            seal.T * metric_k * seal - metric_k,
            checks,
        )

        determinant = sp.factor(metric.det())
        schur = sp.simplify(sp.eye(2) - cross.T * H.inv() * cross)
        require_zero(f"{name}_determinant_formula", determinant - expected_determinants[name], checks)
        require_zero(f"{name}_schur00_formula", schur[0, 0] - expected_schur[name][0], checks)
        require_zero(f"{name}_schurdet_formula", schur.det() - expected_schur[name][1], checks)

        # The metric-compatible connection Gamma=G^-1 dot(G)/2 is exact for any
        # symmetric metric path. Because dot(G) has the same seal parity, it also
        # parallel-transports the seal, but not the reciprocal generator when dk!=0.
        metric_dot_generic = dk * metric_k
        gamma_metric_seal = sp.simplify(sp.Rational(1, 2) * metric.inv() * metric_dot_generic)
        require_zero(
            f"{name}_metric_connection_compatibility",
            gamma_metric_seal.T * metric + metric * gamma_metric_seal - metric_dot_generic,
            checks,
        )
        require_zero(
            f"{name}_seal_connection_compatibility",
            gamma_metric_seal * seal - seal * gamma_metric_seal,
            checks,
        )
        require(
            f"{name}_metric_seal_connection_not_reciprocal_parallel",
            sp.simplify(gamma_metric_seal * L4 - L4 * gamma_metric_seal) != sp.zeros(4),
            checks,
        )

        sample_metric = metric.subs(k, 2)
        sample_dot = metric_k.subs(k, 2)
        metric_rank, metric_augmented, metric_dimension = linear_system_ranks(
            [gamma.T * sample_metric + sample_metric * gamma - sample_dot], gamma_symbols
        )
        seal_rank, seal_augmented, seal_dimension = linear_system_ranks(
            [
                gamma.T * sample_metric + sample_metric * gamma - sample_dot,
                gamma * seal - seal * gamma,
            ],
            gamma_symbols,
        )
        full_rank, full_augmented, _ = linear_system_ranks(
            [
                gamma.T * sample_metric + sample_metric * gamma - sample_dot,
                gamma * seal - seal * gamma,
                gamma * L4 - L4 * gamma,
            ],
            gamma_symbols,
        )
        static_full_rank, static_full_augmented, static_full_dimension = linear_system_ranks(
            [
                gamma.T * sample_metric + sample_metric * gamma,
                gamma * seal - seal * gamma,
                gamma * L4 - L4 * gamma,
            ],
            gamma_symbols,
        )
        require(
            f"{name}_metric_connection_system_consistent",
            metric_rank == metric_augmented == 10 and metric_dimension == 6,
            checks,
        )
        require(
            f"{name}_metric_seal_system_consistent",
            seal_rank == seal_augmented
            and seal_dimension == data["metric_seal_connection_dimension"],
            checks,
        )
        require(
            f"{name}_varying_mu_full_parallel_system_inconsistent",
            full_rank == 16 and full_augmented == 17,
            checks,
        )
        require(
            f"{name}_constant_mu_full_parallel_system_consistent",
            static_full_rank == static_full_augmented == 16 and static_full_dimension == 0,
            checks,
        )

        invariant = pair_invariant(metric, L4)
        for history_name, k_history in trajectories.items():
            history_metric = metric.subs(k, k_history)
            history_dot = sp.diff(history_metric, s)
            history_mu = sp.expand(k_history**2)

            require(f"{name}_{history_name}_k_gt_one", k_history.subs(s, 0) > 1, checks)
            require(
                f"{name}_{history_name}_nonconstant_mu",
                sp.diff(history_mu, s) != 0,
                checks,
            )
            require_zero(
                f"{name}_{history_name}_pointwise_isometry",
                seal.T * history_metric * seal - history_metric,
                checks,
            )
            require_zero(
                f"{name}_{history_name}_differentiated_isometry",
                seal.T * history_dot * seal - history_dot,
                checks,
            )
            require_zero(
                f"{name}_{history_name}_reciprocal_inversion",
                seal * L4 * seal + L4,
                checks,
            )

            for index, factor in enumerate(data["positive_factors"]):
                require(
                    f"{name}_{history_name}_positive_factor_{index + 1}",
                    positive_affine_on_unit_interval(factor.subs(k, k_history), s),
                    checks,
                )

            # Dividing the derivative of a determinant-normalized metric by its
            # positive normalization factor gives this exact trace-free tangent.
            trace_rate = sp.simplify(sp.trace(history_metric.inv() * history_dot))
            volume_fixed_tangent = sp.simplify(history_dot - trace_rate * history_metric / 4)
            require_zero(
                f"{name}_{history_name}_fixed_volume_trace",
                sp.trace(history_metric.inv() * volume_fixed_tangent),
                checks,
            )
            require_zero(
                f"{name}_{history_name}_fixed_volume_seal_parity",
                seal.T * volume_fixed_tangent * seal - volume_fixed_tangent,
                checks,
            )

            history_invariant = sp.factor(invariant.subs(k, k_history))
            require(
                f"{name}_{history_name}_pair_invariant_changes",
                sp.simplify(sp.diff(history_invariant, s)) != 0,
                checks,
            )
            history_id = f"{name}_{history_name}"
            history_results[history_id] = {
                "lift": name,
                "history": history_name,
                "k_initial": str(k_history.subs(s, 0)),
                "k_final": str(k_history.subs(s, 1)),
                "mu_initial": str(history_mu.subs(s, 0)),
                "mu_final": str(history_mu.subs(s, 1)),
                "determinant": str(sp.factor(determinant.subs(k, k_history))),
                "pair_invariant": str(history_invariant),
                "cross": "u=v=1/10 nonzero",
                "signature_certificate": "base_one_plus_one; positive_transverse_Schur_on_0_to_1",
                "fixed_volume_status": "EXACT_POSITIVE_CSN_NORMALIZATION_AVAILABLE",
            }

        lift_results[name] = {
            "orientation": int(data["orientation"]),
            "pointwise_nonconstant_histories": 2,
            "metric_connection_dimension": metric_dimension,
            "metric_seal_connection_dimension": seal_dimension,
            "metric_seal_allows_dot_mu": True,
            "full_reciprocal_parallelism_allows_dot_mu": False,
            "status": "KINEMATICALLY_TIME_EXTENDABLE_MU_VALUE_OPEN",
        }
        connection_results[name] = {
            "metric_only": f"CONSISTENT_DIMENSION_{metric_dimension}_AT_EXACT_SAMPLE",
            "metric_plus_seal": f"CONSISTENT_DIMENSION_{seal_dimension}_AT_EXACT_SAMPLE",
            "metric_plus_seal_plus_reciprocity_varying_mu": "INCONSISTENT_RANK_16_AUGMENTED_17",
            "metric_plus_seal_plus_reciprocity_constant_mu": "CONSISTENT_UNIQUE_ZERO_AT_STATIC_SAMPLE",
        }

    require("eight_nonconstant_histories_constructed", len(history_results) == 8, checks)
    require(
        "both_orientation_classes_have_nonconstant_histories",
        {
            (lift_results[row["lift"]]["orientation"], row["history"])
            for row in history_results.values()
        }
        == {(-1, "LOWER_HISTORY"), (-1, "UPPER_HISTORY"), (1, "LOWER_HISTORY"), (1, "UPPER_HISTORY")},
        checks,
    )

    # General analytic obstruction under the extra full-parallelism premise.
    alpha, beta, d11, d12, d21, d22 = sp.symbols("alpha beta d11 d12 d21 d22", real=True)
    gamma_commuting_L = block_diagonal(sp.diag(alpha, beta), sp.Matrix([[d11, d12], [d21, d22]]))
    require_zero(
        "L_commutant_has_no_base_angular_mix",
        gamma_commuting_L * L4 - L4 * gamma_commuting_L,
        checks,
    )
    require(
        "seal_commutation_forces_equal_base_diagonal",
        (gamma_commuting_L * block_diagonal(F, sp.eye(2))
         - block_diagonal(F, sp.eye(2)) * gamma_commuting_L)[0, 1]
        == alpha - beta,
        checks,
    )
    gamma_base = alpha * sp.eye(2)
    scaled_base_dot = 2 * sigma * H + dk * H_k
    compatibility_base = sp.simplify(gamma_base.T * H + H * gamma_base - scaled_base_dot)
    require_zero(
        "full_parallel_diagonal_equation_sets_alpha_sigma",
        compatibility_base[0, 0].subs(alpha, sigma),
        checks,
    )
    require_zero(
        "full_parallel_offdiagonal_residual_is_dk",
        compatibility_base[0, 1].subs(alpha, sigma) - dk,
        checks,
    )
    require(
        "full_reciprocal_parallelism_forces_dot_k_zero_not_k_value",
        not compatibility_base.subs({alpha: sigma, dk: 0}).has(k),
        checks,
    )
    require_zero(
        "common_scale_connection_preserves_metric",
        (sigma * sp.eye(4)).T * sp.eye(4) + sp.eye(4) * (sigma * sp.eye(4)) - 2 * sigma * sp.eye(4),
        checks,
    )
    require_zero(
        "common_scale_connection_preserves_seal_and_generator",
        sigma * sp.eye(4) * L4 - L4 * sigma * sp.eye(4),
        checks,
    )

    # Nonconstant frame conjugation separates component motion from invariant deformation.
    nilpotent = sp.zeros(4)
    nilpotent[0, 2] = sp.Rational(1, 7)
    moving_frame = sp.eye(4) + s * nilpotent
    moving_frame_inverse = sp.eye(4) - s * nilpotent
    require_zero("moving_frame_inverse_exact", moving_frame * moving_frame_inverse - sp.eye(4), checks)
    require("moving_frame_unit_determinant", moving_frame.det() == 1, checks)

    plus = lifts["PLUS_IDENTITY"]
    plus_seal = block_diagonal(F, plus["A"])
    plus_metric = full_metric(H, plus["C"], sp.eye(2))
    lower_k = trajectories["LOWER_HISTORY"]
    base_path_metric = plus_metric.subs(k, lower_k)
    base_path_dot = sp.diff(base_path_metric, s)
    base_gamma = sp.simplify(sp.Rational(1, 2) * base_path_metric.inv() * base_path_dot)
    moving_metric = sp.simplify(moving_frame_inverse.T * base_path_metric * moving_frame_inverse)
    moving_seal = sp.simplify(moving_frame * plus_seal * moving_frame_inverse)
    moving_generator = sp.simplify(moving_frame * L4 * moving_frame_inverse)
    frame_rate = sp.simplify(sp.diff(moving_frame, s) * moving_frame_inverse)
    moving_gamma = sp.simplify(-frame_rate + moving_frame * base_gamma * moving_frame_inverse)
    require_zero(
        "moving_frame_metric_compatibility",
        sp.diff(moving_metric, s) - moving_gamma.T * moving_metric - moving_metric * moving_gamma,
        checks,
    )
    require_zero(
        "moving_frame_seal_compatibility",
        sp.diff(moving_seal, s) + moving_gamma * moving_seal - moving_seal * moving_gamma,
        checks,
    )
    moving_generator_covariant_derivative = sp.simplify(
        sp.diff(moving_generator, s) + moving_gamma * moving_generator - moving_generator * moving_gamma
    )
    require(
        "moving_frame_does_not_hide_true_mu_deformation",
        moving_generator_covariant_derivative != sp.zeros(4),
        checks,
    )

    constant_path_metric = plus_metric.subs(k, 2)
    constant_moving_metric = sp.simplify(moving_frame_inverse.T * constant_path_metric * moving_frame_inverse)
    constant_moving_seal = sp.simplify(moving_frame * plus_seal * moving_frame_inverse)
    constant_moving_generator = sp.simplify(moving_frame * L4 * moving_frame_inverse)
    pure_frame_gamma = -frame_rate
    require_zero(
        "pure_frame_metric_compatibility",
        sp.diff(constant_moving_metric, s)
        - pure_frame_gamma.T * constant_moving_metric
        - constant_moving_metric * pure_frame_gamma,
        checks,
    )
    require_zero(
        "pure_frame_seal_compatibility",
        sp.diff(constant_moving_seal, s)
        + pure_frame_gamma * constant_moving_seal
        - constant_moving_seal * pure_frame_gamma,
        checks,
    )
    require_zero(
        "pure_frame_reciprocal_compatibility",
        sp.diff(constant_moving_generator, s)
        + pure_frame_gamma * constant_moving_generator
        - constant_moving_generator * pure_frame_gamma,
        checks,
    )

    output = {
        "schema": "udt-kinematic-time-extendability-derivation-1.0",
        "maximum_conclusion": "UDT_KINEMATIC_TIME_EXTENDABILITY_STATUS_CHARACTERIZED",
        "check_count": len(checks),
        "checks": dict(sorted(checks.items())),
        "outcomes": [
            "POINTWISE_TIME_PRESERVATION_ALLOWS_INEQUIVALENT_MU_HISTORIES",
            "ALL_REGISTERED_FROZEN_LIFTS_HAVE_KINEMATIC_TIME_EXTENSIONS",
            "METRIC_SEAL_COMPATIBILITY_ALLOWS_DOT_MU",
            "FULL_RECIPROCAL_PARALLELISM_ONLY_CONSERVES_MU",
            "FULL_RECIPROCAL_PARALLELISM_DOES_NOT_SELECT_MU_VALUE",
            "CSN_FIXED_VOLUME_GAUGE_DOES_NOT_SELECT_MU",
            "MOVING_FRAME_CONNECTION_SEPARATES_FRAME_MOTION_FROM_MU_DEFORMATION",
            "PHYSICAL_TRANSPORT_LAW_REMAINS_OPEN",
            "KINEMATIC_TIME_EXTENDABILITY_REMAINS_UNDERDETERMINED",
        ],
        "lift_results": lift_results,
        "histories": history_results,
        "connection_census": connection_results,
        "transport_hierarchy": {
            "pointwise": "arbitrary smooth mu(s)>1 in all four registered lift classes",
            "metric_only": "compatible connections exist; no mu selector",
            "metric_plus_seal": "compatible connections exist with dot(mu)!=0; no mu selector",
            "metric_plus_seal_plus_reciprocal_generator": "forces dot(mu)=0 while leaving every constant mu>1",
            "current_UDT_authority": "does not select the last transport premise or a physical evolution law",
        },
        "moving_frame": {
            "frame": "S(s)=I+s N with N_0_2=1/7 and N^2=0",
            "connection": "Gamma=-dot(S)S^-1+S Gamma_base S^-1",
            "pure_frame_constant_mu": "metric seal and reciprocal generator all parallel",
            "varying_mu": "metric and seal parallel; reciprocal covariant derivative nonzero",
        },
        "scope": {
            "complete": "registered constant real isotropic lift classes and complete parity-compatible constant cross patterns",
            "not_a_dynamical_solve": True,
            "not_covered": [
                "field-dependent global bundles and arbitrary anisotropic angular metrics",
                "selected physical connection or evolution parameter",
                "action field equation or boundary functional",
                "time-live carrier soliton or matter stability",
                "topology source mass scale Xmax value and canonization",
            ],
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
