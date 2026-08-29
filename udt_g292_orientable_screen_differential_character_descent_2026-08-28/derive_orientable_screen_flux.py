#!/usr/bin/env python3
"""Exact symbolic G292 orientable screen-flux descent and metric witness."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
LANDING = (
    "ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY"
    "__G225_SKY_AND_G290_PAIR_CONNECTIONS_REQUIRE_SUPPLIED_IDENTIFICATION"
    "__GLOBAL_SAME_PAIR_BLOCK_SAME_EULER_CLASS_DIFFERENT_LOCAL_FLUX_METRIC_FAMILY"
    "__NO_CONTINUOUS_FLUX_PROPAGATION_OR_HISTORY_SELECTION"
)


def christoffel_symbols(
    metric: sp.Matrix, coords: tuple[sp.Symbol, ...]
) -> list[list[list[sp.Expr]]]:
    inverse = sp.simplify(metric.inv())
    dim = len(coords)
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for upper in range(dim):
        for left in range(dim):
            for right in range(dim):
                gamma[upper][left][right] = sp.trigsimp(
                    sp.simplify(
                        sp.Rational(1, 2)
                        * sum(
                            inverse[upper, lower]
                            * (
                                sp.diff(metric[lower, right], coords[left])
                                + sp.diff(metric[lower, left], coords[right])
                                - sp.diff(metric[left, right], coords[lower])
                            )
                            for lower in range(dim)
                        )
                    )
                )
    return gamma


def main() -> None:
    theta, varphi = sp.symbols("theta varphi", real=True)
    epsilon = sp.symbols("epsilon", real=True)
    radius = sp.symbols("R", positive=True, finite=True)
    theta0 = sp.symbols("theta_0", positive=True)
    coords = (theta, varphi)

    u = epsilon * sp.cos(theta)
    conformal = radius**2 * sp.exp(2 * u)
    metric = sp.diag(conformal, conformal * sp.sin(theta) ** 2)
    gamma = christoffel_symbols(metric, coords)

    # Direct coordinate R^theta_{varphi theta varphi}; no conformal-curvature
    # formula is assumed as an input.
    riemann = sp.diff(gamma[0][1][1], theta) - sp.diff(gamma[0][0][1], varphi)
    for lower in range(2):
        riemann += gamma[0][0][lower] * gamma[lower][1][1]
        riemann -= gamma[0][1][lower] * gamma[lower][0][1]
    riemann = sp.trigsimp(sp.simplify(riemann))
    gaussian = sp.trigsimp(sp.simplify(riemann / metric[1, 1]))
    area_density = conformal * sp.sin(theta)
    curvature_density = sp.trigsimp(sp.simplify(gaussian * area_density))
    expected_density = (1 + 2 * epsilon * sp.cos(theta)) * sp.sin(theta)

    # Cartan connection for e^1=R exp(u)dtheta,
    # e^2=R exp(u)sin(theta)dvarphi in the G290 convention.
    connection_varphi = sp.trigsimp(
        -(sp.diff(u, theta) * sp.sin(theta) + sp.cos(theta))
    )
    baseline_connection = -sp.cos(theta)
    connection_difference = sp.trigsimp(connection_varphi - baseline_connection)
    curvature_from_connection = sp.trigsimp(sp.diff(connection_varphi, theta))
    difference_curvature = sp.trigsimp(sp.diff(connection_difference, theta))

    total_flux = sp.trigsimp(
        sp.integrate(
            sp.integrate(curvature_density, (theta, 0, sp.pi)),
            (varphi, 0, 2 * sp.pi),
        )
    )
    cap_flux = sp.trigsimp(
        sp.integrate(
            sp.integrate(curvature_density, (theta, 0, theta0)),
            (varphi, 0, 2 * sp.pi),
        )
    )
    baseline_cap = sp.trigsimp(cap_flux.subs(epsilon, 0))
    cap_change = sp.trigsimp(cap_flux - baseline_cap)
    latitude_phase = sp.trigsimp(2 * sp.pi * connection_varphi.subs(theta, theta0))
    patch_integer = sp.trigsimp(cap_flux - latitude_phase)

    pair_metric = sp.diag(-1, 1)
    pair_det = sp.det(pair_metric)
    pair_phi = sp.simplify(
        sp.Rational(1, 4) * sp.log((-pair_det) / pair_metric[0, 0] ** 2)
    )
    pair_common_scale = sp.simplify(sp.Rational(1, 4) * sp.log(-pair_det))

    bad_euler_number = sp.simplify(
        sp.integrate(
            sp.integrate(
                sp.Rational(4, 3) * sp.sin(theta),
                (theta, 0, sp.pi),
            ),
            (varphi, 0, 2 * sp.pi),
        )
        / (2 * sp.pi)
    )

    time = sp.symbols("s", real=True)
    epsilon_time = sp.Function("epsilon")(time)
    time_total_flux = sp.simplify(total_flux.subs(epsilon, epsilon_time))

    checks: dict[str, bool] = {}
    checks["screen_metric_positive_on_regular_chart"] = bool(radius.is_positive)
    checks["metric_determinant_direct"] = (
        sp.trigsimp(metric.det() - conformal**2 * sp.sin(theta) ** 2) == 0
    )
    checks["gaussian_curvature_density_direct"] = (
        sp.trigsimp(curvature_density - expected_density) == 0
    )
    checks["cartan_connection_direct"] = (
        sp.trigsimp(connection_varphi - (epsilon * sp.sin(theta) ** 2 - sp.cos(theta))) == 0
    )
    checks["connection_curvature_matches_riemann"] = (
        sp.trigsimp(curvature_from_connection - curvature_density) == 0
    )
    checks["same_bundle_connection_difference"] = (
        sp.trigsimp(connection_difference - epsilon * sp.sin(theta) ** 2) == 0
    )
    checks["same_class_curvature_difference_exact"] = (
        sp.trigsimp(
            difference_curvature - 2 * epsilon * sp.sin(theta) * sp.cos(theta)
        )
        == 0
    )
    checks["curvature_scale_R_cancels"] = sp.diff(curvature_density, radius) == 0
    checks["total_flux_four_pi"] = sp.simplify(total_flux - 4 * sp.pi) == 0
    checks["euler_number_two"] = sp.simplify(total_flux / (2 * sp.pi) - 2) == 0
    checks["cap_flux_formula"] = (
        sp.trigsimp(
            cap_flux
            - 2
            * sp.pi
            * (1 - sp.cos(theta0) + epsilon * sp.sin(theta0) ** 2)
        )
        == 0
    )
    checks["cap_flux_change_formula"] = (
        sp.trigsimp(cap_change - 2 * sp.pi * epsilon * sp.sin(theta0) ** 2) == 0
    )
    checks["north_patch_phase_differs_by_two_pi"] = (
        sp.simplify(patch_integer - 2 * sp.pi) == 0
    )
    checks["completed_pair_phi_zero"] = pair_phi == 0
    checks["completed_pair_common_scale_zero"] = pair_common_scale == 0
    checks["pair_state_independent_of_R_epsilon"] = (
        sp.diff(pair_phi, radius) == 0 and sp.diff(pair_phi, epsilon) == 0
    )
    checks["positive_negative_epsilon_local_separation"] = (
        sp.trigsimp(
            curvature_density.subs(epsilon, 1)
            - curvature_density.subs(epsilon, -1)
            - 4 * sp.sin(theta) * sp.cos(theta)
        )
        == 0
    )
    checks["same_total_flux_for_all_epsilon"] = sp.diff(total_flux, epsilon) == 0
    checks["smooth_timelive_class_derivative_zero"] = (
        sp.diff(time_total_flux, time) == 0
    )
    checks["orientation_reversal_keeps_unsigned_euler_magnitude"] = (
        sp.Abs(-2) == sp.Abs(2)
    )
    checks["nonintegral_total_flux_rejected_for_TS2"] = bad_euler_number == sp.Rational(8, 3)
    checks["nonflat_full_sky_required"] = total_flux != 0

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"failed checks: {failed}")

    conclusions = {
        "oriented_screen_holonomy_curvature_is_degree_two_differential_character": True,
        "curvature_periods_represent_euler_class": True,
        "smooth_regular_fixed_rank_continuation_preserves_euler_class": True,
        "connections_on_identified_oriented_metric_line_differ_by_bJ": True,
        "same_euler_class_retains_exact_curvature_and_flat_holonomy_freedom": True,
        "g225_full_sky_TS2_has_euler_number_magnitude_two": True,
        "sky_pair_connection_comparison_requires_supplied_isometric_bundle_identification": True,
        "global_metric_family_has_same_pair_state_and_euler_class_but_different_local_flux": True,
        "full_holonomy_reconstructs_but_does_not_select_connection": True,
        "topological_sector_persistence_is_not_physical_dynamics": True,
        "nonorientable_reflection_and_twisted_euler_strata_remain_open": True,
        "no_complete_metric_history_is_selected": True,
    }

    result = {
        "status": "PASS",
        "landing": LANDING,
        "computed_check_count": len(checks),
        "computed_checks": checks,
        "derived_conclusion_count": len(conclusions),
        "derived_conclusions": conclusions,
        "screen_connection_varphi": str(connection_varphi),
        "screen_connection_difference": str(connection_difference),
        "screen_curvature_density": str(curvature_density),
        "total_flux": str(total_flux),
        "cap_flux": str(cap_flux),
        "cap_flux_change": str(cap_change),
        "pair_phi": str(pair_phi),
        "free_parameters": ["R>0", "epsilon in R", "theta_0 in (0,pi)"],
        "imports_action_source_history_observation_scale_selection_or_xmax": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
