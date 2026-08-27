#!/usr/bin/env python3
"""Exact G282 neighboring-ray and primary-spherical discriminator."""

from __future__ import annotations

import json

import sympy as sp


def christoffel(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]) -> list:
    inverse = sp.simplify(metric.inv())
    n = len(coords)
    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for mu in range(n):
            for nu in range(n):
                gamma[rho][mu][nu] = sp.simplify(
                    sum(
                        inverse[rho, sigma]
                        * (
                            sp.diff(metric[sigma, nu], coords[mu])
                            + sp.diff(metric[sigma, mu], coords[nu])
                            - sp.diff(metric[mu, nu], coords[sigma])
                        )
                        / 2
                        for sigma in range(n)
                    )
                )
    return gamma


def riemann_down(
    metric: sp.Matrix,
    gamma: list,
    coords: tuple[sp.Symbol, ...],
    rho: int,
    sigma: int,
    mu: int,
    nu: int,
) -> sp.Expr:
    n = len(coords)
    upper = [
        sp.simplify(
            sp.diff(gamma[alpha][nu][sigma], coords[mu])
            - sp.diff(gamma[alpha][mu][sigma], coords[nu])
            + sum(
                gamma[alpha][mu][beta] * gamma[beta][nu][sigma]
                - gamma[alpha][nu][beta] * gamma[beta][mu][sigma]
                for beta in range(n)
            )
        )
        for alpha in range(n)
    ]
    return sp.simplify(sum(metric[rho, alpha] * upper[alpha] for alpha in range(n)))


def main() -> None:
    u, v, x, y = sp.symbols("u v x y", real=True)
    A = sp.symbols("A", positive=True)
    coords = (u, v, x, y)
    H = A * (x**2 - y**2)
    metric = sp.Matrix(
        [
            [H, -1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    flat = metric.subs(A, 0)
    on_ray = {x: 0, y: 0}
    gamma = christoffel(metric, coords)

    same_metric = sp.simplify(metric.subs(on_ray) - flat) == sp.zeros(4)
    same_first_jet = all(
        sp.simplify(sp.diff(metric[i, j], coordinate).subs(on_ray)) == 0
        for i in range(4)
        for j in range(4)
        for coordinate in coords
    )
    same_connection = all(
        sp.simplify(gamma[rho][mu][nu].subs(on_ray)) == 0
        for rho in range(4)
        for mu in range(4)
        for nu in range(4)
    )

    r_uxux = sp.simplify(riemann_down(metric, gamma, coords, 0, 2, 0, 2).subs(on_ray))
    r_uyuy = sp.simplify(riemann_down(metric, gamma, coords, 0, 3, 0, 3).subs(on_ray))
    r_xuxu = sp.simplify(riemann_down(metric, gamma, coords, 2, 0, 2, 0).subs(on_ray))
    r_yuyu = sp.simplify(riemann_down(metric, gamma, coords, 3, 0, 3, 0).subs(on_ray))

    q = sp.symbols("q", positive=True)
    dx = sp.sinh(q * u) / q
    dy = sp.sin(q * u) / q
    jacobi_x = sp.simplify(sp.diff(dx, u, 2) - q**2 * dx) == 0
    jacobi_y = sp.simplify(sp.diff(dy, u, 2) + q**2 * dy) == 0
    vertex_data = (
        sp.simplify(dx.subs(u, 0)) == 0
        and sp.simplify(dy.subs(u, 0)) == 0
        and sp.simplify(sp.diff(dx, u).subs(u, 0)) == 1
        and sp.simplify(sp.diff(dy, u).subs(u, 0)) == 1
    )
    determinant = sp.simplify(dx * dy)
    determinant_series = sp.series(determinant, u, 0, 9)
    flat_determinant = u**2
    first_difference = sp.expand(determinant_series.removeO() - flat_determinant)

    s = sp.symbols("s", positive=True)
    phi_a = s**2
    phi_b = s**2 + s**4
    s_a = sp.sqrt(2)
    s_b = sp.S.One
    primary_same_depth = (
        sp.simplify(phi_a.subs(s, s_a)) == 2
        and sp.simplify(phi_b.subs(s, s_b)) == 2
    )
    primary_different_area = sp.simplify(s_a - s_b) != 0

    checks = {
        "same_central_metric": same_metric,
        "same_central_metric_first_jet": same_first_jet,
        "same_central_connection_transport": same_connection,
        "transverse_curvature_nonzero_and_tracefree": (
            r_uxux != 0 and r_uyuy != 0 and sp.simplify(r_uxux + r_uyuy) == 0
        ),
        "riemann_pair_symmetry_control": (
            sp.simplify(r_uxux - r_xuxu) == 0 and sp.simplify(r_uyuy - r_yuyu) == 0
        ),
        "jacobi_equations_exact": jacobi_x and jacobi_y,
        "vertex_initial_data_exact": vertex_data,
        "jacobi_area_differs_from_flat": sp.simplify(determinant - flat_determinant) != 0,
        "first_area_difference_is_sixth_order": (
            sp.simplify(first_difference + q**4 * u**6 / 90) == 0
        ),
        "primary_same_depth": primary_same_depth,
        "primary_different_areal_position": primary_different_area,
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "curvature": {
                        "R_uxux": str(r_uxux),
                        "R_uyuy": str(r_uyuy),
                        "R_xuxu": str(r_xuxu),
                        "R_yuyu": str(r_yuyu),
                    },
                    "determinant_series": str(determinant_series),
                },
                indent=2,
                sort_keys=True,
                default=str,
            )
        )

    result = {
        "audit": "G282_COMPLETE_HISTORY_DEPTH_JACOBI_MINIMAL_LAW_TYPE",
        "status": "PASS",
        "landing": "NO_OWNED_JOINT_HISTORY_LAW__NEIGHBOR_RELATION_CURVATURE_CONSTRAINT_REQUIRED",
        "checks": checks,
        "full_metric_witness": {
            "metric": "ds2=-2 du dv+dx2+dy2+A(x2-y2)du2",
            "central_ray": "x=y=0",
            "R_uxux": str(r_uxux),
            "R_uyuy": str(r_uyuy),
            "jacobi_Dx": str(dx),
            "jacobi_Dy": str(dy),
            "jacobi_determinant": str(determinant),
            "jacobi_determinant_series": str(determinant_series),
        },
        "primary_witness": {
            "phi_A": "s**2",
            "phi_B": "s**2+s**4",
            "depth": 2,
            "s_A": "sqrt(2)",
            "s_B": "1",
        },
        "minimum_missing_information_types": [
            "nonidentity_complete_metric_two_jet_or_curvature_law",
            "equivalent_first_order_coframe_connection_curvature_system",
            "global_neighboring_relation_network_law_with_value_content",
        ],
        "not_uniquely_implied": [
            "second_order_metric_PDE",
            "Einstein_equation",
            "action",
            "source_model",
        ],
        "fitted_coefficients": 0,
        "observational_outcomes_used": 0,
        "field_equations_adopted": 0,
        "Xmax_used": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
