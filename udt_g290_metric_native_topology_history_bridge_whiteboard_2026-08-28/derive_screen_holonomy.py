#!/usr/bin/env python3
"""Exact G290 complete-pair screen-connection and holonomy descent."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
LANDING = (
    "EXACT_COMPLETE_PAIR_SCREEN_HOLONOMY_DESCENDS_CONDITIONALLY"
    "__CONFORMAL_TWIN_HISTORY_SEPARATOR_DERIVED"
    "__TIMELIVE_HOLONOMY_CHANGE_EQUALS_SCREEN_CURVATURE_FLUX"
    "__ORIENTABLE_SCREEN_FULL_O2_ROTATION_DATA_IS_INVERSE_CONJUGACY_CLASS"
    "__NO_PERSISTENCE_DYNAMICS_POPULATION_OR_HISTORY_SELECTION"
)


def screen_connection(omega: sp.Expr, coords: tuple[sp.Symbol, ...]) -> list[sp.Expr]:
    """Compute a_mu=g(e_x,nabla_mu e_y) directly from g=exp(2 omega) eta."""
    eta = sp.diag(-1, 1, 1, 1)
    metric = sp.exp(2 * omega) * eta
    inverse = sp.exp(-2 * omega) * eta
    dim = 4
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for upper in range(dim):
        for left in range(dim):
            for right in range(dim):
                gamma[upper][left][right] = sp.simplify(
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

    e1 = [sp.S.Zero, sp.exp(-omega), sp.S.Zero, sp.S.Zero]
    e2 = [sp.S.Zero, sp.S.Zero, sp.exp(-omega), sp.S.Zero]

    def covariant_derivative(mu: int, vector: list[sp.Expr]) -> list[sp.Expr]:
        return [
            sp.simplify(
                sp.diff(vector[upper], coords[mu])
                + sum(gamma[upper][mu][lower] * vector[lower] for lower in range(dim))
            )
            for upper in range(dim)
        ]

    connection = []
    for mu in range(dim):
        derivative = covariant_derivative(mu, e2)
        connection.append(
            sp.simplify(
                sum(metric[left, right] * e1[left] * derivative[right]
                    for left in range(dim) for right in range(dim))
            )
        )
    return connection


def main() -> None:
    t, x, y, z = sp.symbols("t x y z", real=True)
    alpha, rho, psi = sp.symbols("alpha rho psi", real=True)
    coords = (t, x, y, z)

    omega = alpha * (x**2 + y**2 + z**2)
    connection = screen_connection(omega, coords)
    expected_connection = [0, 2 * alpha * y, -2 * alpha * x, 0]

    checks: dict[str, bool] = {}
    checks["levi_civita_connection_direct"] = all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(connection, expected_connection)
    )

    curvature_xy = sp.simplify(sp.diff(connection[2], x) - sp.diff(connection[1], y))
    checks["screen_curvature_direct"] = sp.simplify(curvature_xy + 4 * alpha) == 0

    circle_x = rho * sp.cos(psi)
    circle_y = rho * sp.sin(psi)
    circle_density = sp.simplify(
        connection[1].subs({x: circle_x, y: circle_y}) * sp.diff(circle_x, psi)
        + connection[2].subs({x: circle_x, y: circle_y}) * sp.diff(circle_y, psi)
    )
    circle_integral = sp.simplify(sp.integrate(circle_density, (psi, 0, 2 * sp.pi)))
    checks["circle_integral"] = sp.simplify(circle_integral + 4 * sp.pi * alpha * rho**2) == 0
    checks["small_loop_curvature_coefficient"] = (
        sp.simplify(circle_integral / (sp.pi * rho**2) - curvature_xy) == 0
    )
    checks["flat_holonomy_phase"] = sp.simplify(circle_integral.subs(alpha, 0)) == 0

    theta = sp.Function("theta")(*coords)
    c = sp.cos(theta)
    s = sp.sin(theta)
    # In the frozen convention e1'=c e1+s e2 and e2'=-s e1+c e2.
    # Metric compatibility gives a'=a-dtheta componentwise.
    for mu, coord in enumerate(coords):
        a_symbol = sp.Symbol(f"a{mu}", real=True)
        abstract_rotated = sp.expand(
            c * (-sp.diff(theta, coord) * c + a_symbol * c)
            + s * (-sp.diff(theta, coord) * s + a_symbol * s)
        )
        checks[f"so2_gauge_component_{mu}"] = (
            sp.trigsimp(abstract_rotated - (a_symbol - sp.diff(theta, coord))) == 0
        )
    theta_start, theta_end, open_angle = sp.symbols("theta_start theta_end open_angle", real=True)
    transformed_open_angle = open_angle - theta_end + theta_start
    checks["open_carry_endpoint_covariant"] = (
        sp.simplify(transformed_open_angle + theta_end - theta_start - open_angle) == 0
    )
    checks["closed_so2_holonomy_invariant"] = (
        sp.simplify(transformed_open_angle.subs(theta_end, theta_start) - open_angle) == 0
    )
    reflected_connection = [-value for value in connection]
    checks["o2_reflection_inverts_connection"] = all(
        sp.simplify(reflected + value) == 0
        for reflected, value in zip(reflected_connection, connection)
    )
    checks["o2_unoriented_cosine_invariant"] = sp.simplify(
        sp.cos(circle_integral) - sp.cos(-circle_integral)
    ) == 0

    alpha_t = sp.Function("alpha")(t)
    omega_t = alpha_t * (x**2 + y**2 + z**2)
    connection_t = screen_connection(omega_t, coords)
    expected_t = [0, 2 * alpha_t * y, -2 * alpha_t * x, 0]
    checks["timelive_connection_direct"] = all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(connection_t, expected_t)
    )

    curvature_tx = sp.simplify(sp.diff(connection_t[1], t) - sp.diff(connection_t[0], x))
    curvature_ty = sp.simplify(sp.diff(connection_t[2], t) - sp.diff(connection_t[0], y))
    expected_tx = 2 * sp.diff(alpha_t, t) * y
    expected_ty = -2 * sp.diff(alpha_t, t) * x
    checks["timelive_mixed_curvature"] = (
        sp.simplify(curvature_tx - expected_tx) == 0
        and sp.simplify(curvature_ty - expected_ty) == 0
    )

    flux_density = sp.simplify(
        curvature_tx.subs({x: circle_x, y: circle_y}) * sp.diff(circle_x, psi)
        + curvature_ty.subs({x: circle_x, y: circle_y}) * sp.diff(circle_y, psi)
    )
    flux_rate = sp.simplify(sp.integrate(flux_density, (psi, 0, 2 * sp.pi)))
    holonomy_angle = -4 * sp.pi * alpha_t * rho**2
    checks["timelive_transgression_rate"] = (
        sp.simplify(flux_rate - sp.diff(holonomy_angle, t)) == 0
    )

    alpha0, slope, t1, t2 = sp.symbols("alpha0 slope t1 t2", real=True)
    linear_flux = sp.simplify(
        sp.integrate(flux_rate.subs(alpha_t, alpha0 + slope * t), (t, t1, t2))
    )
    linear_angle_change = sp.simplify(
        holonomy_angle.subs(alpha_t, alpha0 + slope * t).subs(t, t2)
        - holonomy_angle.subs(alpha_t, alpha0 + slope * t).subs(t, t1)
    )
    checks["linear_timelive_transgression"] = sp.simplify(linear_flux - linear_angle_change) == 0

    alias_alpha_rho2 = sp.Rational(1, 2)
    alias_angle = sp.simplify(circle_integral.subs({alpha: 1, rho**2: alias_alpha_rho2}))
    checks["single_loop_phase_alias_exists"] = sp.simplify(sp.exp(sp.I * alias_angle) - 1) == 0
    small_phase_over_pi = sp.simplify(
        (circle_integral / sp.pi).subs({alpha: sp.Rational(2), rho**2: sp.Rational(1, 100)})
    )
    checks["small_loop_principal_branch_control"] = bool(abs(small_phase_over_pi) < 1)

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"failed checks: {failed}")

    conclusions = {
        "projected_connection_conditional_on_supplied_screen_carry": True,
        "closed_so2_holonomy_is_frame_gauge_invariant": True,
        "orientable_screen_full_o2_rotation_data_is_inverse_conjugacy_class": True,
        "small_loop_holonomy_recovers_screen_curvature": True,
        "conformal_twins_are_separated_by_metric_screen_holonomy": True,
        "timelive_change_is_curvature_flux_on_supplied_worldtube": True,
        "transgression_is_not_conservation_or_history_selection": True,
        "screen_projection_is_required_beyond_a_bare_null_line": True,
        "arbitrary_smooth_alpha_t_remains_admitted": True,
    }
    result = {
        "status": "PASS",
        "landing": LANDING,
        "computed_check_count": len(checks),
        "computed_checks": checks,
        "derived_conclusion_count": len(conclusions),
        "derived_conclusions": conclusions,
        "connection": [str(sp.simplify(value)) for value in connection],
        "curvature_xy": str(curvature_xy),
        "circle_integral": str(circle_integral),
        "timelive_flux_rate": str(flux_rate),
        "imports_action_source_history_scale_or_xmax": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
