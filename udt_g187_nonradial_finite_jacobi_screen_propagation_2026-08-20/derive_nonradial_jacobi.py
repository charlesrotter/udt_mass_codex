#!/usr/bin/env python3
"""Exact symbolic derivation for the bounded G187 nonradial Jacobi query."""

from __future__ import annotations

import json

import sympy as sp


LANDING = (
    "FINITE_NONRADIAL_JACOBI_MAP_DERIVED_CONDITIONALLY"
    "__G186_LOCAL_SCREEN_SEEDS_TWO_METRIC_FIXED_MODES"
    "__NONRADIAL_SHEAR_EMERGES_WITHOUT_EXTRA_COEFFICIENT"
)


def zero_vector(vector: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in vector)


def main() -> None:
    t, r, theta, varphi = sp.symbols("t r theta varphi", real=True)
    coordinates = [t, r, theta, varphi]
    f = sp.Function("f")(r)
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    inverse_metric = sp.simplify(metric.inv())
    dimension = 4

    christoffel = [
        [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                christoffel[a][b][c] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse_metric[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        for d in range(dimension)
                    )
                )

    riemann = [
        [
            [
                [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    riemann[a][b][c][d] = sp.simplify(
                        sp.diff(christoffel[a][d][b], coordinates[c])
                        - sp.diff(christoffel[a][c][b], coordinates[d])
                        + sum(
                            christoffel[a][c][e] * christoffel[e][d][b]
                            - christoffel[a][d][e] * christoffel[e][c][b]
                            for e in range(dimension)
                        )
                    )

    energy, angular_momentum, radial_rate = sp.symbols("E L q", real=True)
    ray = sp.Matrix([energy / f, radial_rate, 0, angular_momentum / r**2])
    null_rule = {radial_rate**2: energy**2 - f * angular_momentum**2 / r**2}
    radial_acceleration = (
        angular_momentum**2 * (2 * f - r * sp.diff(f, r)) / (2 * r**3)
    )

    out_of_plane = sp.Matrix([0, 0, 1 / r, 0])
    in_plane = sp.Matrix(
        [
            0,
            -f * angular_momentum / (energy * r),
            0,
            radial_rate / (energy * r),
        ]
    )

    def reduce(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.simplify(expression.subs(theta, sp.pi / 2)).subs(null_rule)
        )

    def inner(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
        return reduce((left.T * metric * right)[0])

    def along(vector: sp.Matrix) -> sp.Matrix:
        entries = []
        for a in range(dimension):
            direct = (
                sp.diff(vector[a], r) * radial_rate
                + sp.diff(vector[a], radial_rate) * radial_acceleration
            )
            connection = sum(
                christoffel[a][b][c] * ray[b] * vector[c]
                for b in range(dimension)
                for c in range(dimension)
            )
            entries.append(reduce(direct + connection))
        return sp.Matrix(entries)

    ray_acceleration = along(ray)
    out_transport = along(out_of_plane)
    in_transport = along(in_plane)
    null_gauge_coefficient = -angular_momentum * sp.diff(f, r) / (2 * energy * r)

    def tidal(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
        value = sp.S.Zero
        for mu in range(dimension):
            for a in range(dimension):
                for b in range(dimension):
                    for c in range(dimension):
                        for d in range(dimension):
                            value += (
                                metric[mu, a]
                                * left[mu]
                                * riemann[a][b][c][d]
                                * ray[b]
                                * right[c]
                                * ray[d]
                            )
        return reduce(value)

    tidal_out = tidal(out_of_plane, out_of_plane)
    tidal_in = tidal(in_plane, in_plane)
    tidal_cross = tidal(out_of_plane, in_plane)
    expected_out = (
        angular_momentum**2
        * (r * sp.diff(f, r) - 2 * f + 2)
        / (2 * r**4)
    )
    expected_in = (
        angular_momentum**2
        * (r * sp.diff(f, r, 2) - sp.diff(f, r))
        / (2 * r**3)
    )

    # G186 projector for the same observer/ray plane.
    root_f = sp.sqrt(f)
    observer = sp.Matrix([1 / root_f, 0, 0, 0])
    spatial_direction = sp.Matrix(
        [
            0,
            radial_rate * root_f / energy,
            0,
            root_f * angular_momentum / (energy * r**2),
        ]
    )
    pair = sp.Matrix.hstack(observer, spatial_direction)
    pair_metric = sp.simplify(pair.T * metric * pair).subs(theta, sp.pi / 2)
    projector = sp.simplify(
        sp.eye(4) - pair * pair_metric.inv() * pair.T * metric
    ).subs(theta, sp.pi / 2)

    # Exact out-of-plane Killing mode D_perp=r sin(Delta varphi)/sin(alpha_o).
    sine_delta = sp.symbols("S_delta", real=True)
    second_r_sine = (radial_acceleration - angular_momentum**2 / r**3) * sine_delta
    killing_mode_residual = reduce(second_r_sine + expected_out * r * sine_delta)

    sine_alpha, cosine_alpha, radius_o, f_o = sp.symbols(
        "s_a c_a r_o f_o", positive=True, real=True
    )
    energy_o = sp.sqrt(f_o)
    angular_momentum_o = radius_o * sine_alpha
    radial_rate_o = sp.sqrt(f_o) * cosine_alpha
    out_initial_slope = sp.simplify(
        angular_momentum_o / (radius_o * sine_alpha)
    )
    delta_k_r = -sp.sqrt(f_o) * sine_alpha
    delta_k_varphi = cosine_alpha / radius_o
    in_initial_slope = sp.simplify(
        (-angular_momentum_o / (energy_o * radius_o)) * delta_k_r
        + (radial_rate_o * radius_o / energy_o) * delta_k_varphi
    ).subs(sine_alpha**2 + cosine_alpha**2, 1)

    mass = sp.symbols("M", real=True)
    schwarzschild = 1 - 2 * mass / r
    flat_controls = {
        "in": sp.simplify(expected_in.subs(f, 1).doit()) == 0,
        "out": sp.simplify(expected_out.subs(f, 1).doit()) == 0,
    }
    schwarzschild_controls = {
        "in": sp.simplify(expected_in.subs(f, schwarzschild).doit()),
        "out": sp.simplify(expected_out.subs(f, schwarzschild).doit()),
    }

    checks = {
        "affine_geodesic": zero_vector(ray_acceleration),
        "g186_projector_annihilates_pair": zero_vector(projector * pair),
        "g186_projector_contains_in_plane_screen": zero_vector(
            sp.simplify(projector * in_plane - in_plane).subs(null_rule)
        ),
        "g186_projector_contains_out_of_plane_screen": zero_vector(
            sp.simplify(projector * out_of_plane - out_of_plane).subs(null_rule)
        ),
        "g186_projector_trace_two": reduce(sp.trace(projector) - 2) == 0,
        "in_plane_screen_is_unit": inner(in_plane, in_plane) == 1,
        "in_plane_screen_orthogonal_to_ray": inner(in_plane, ray) == 0,
        "in_plane_screen_parallel_modulo_null": zero_vector(
            sp.simplify(in_transport - null_gauge_coefficient * ray)
        ),
        "null_ray": inner(ray, ray) == 0,
        "out_of_plane_killing_mode": killing_mode_residual == 0,
        "out_of_plane_screen_is_parallel": zero_vector(out_transport),
        "out_of_plane_screen_is_unit": inner(out_of_plane, out_of_plane) == 1,
        "out_of_plane_screen_orthogonal_to_ray": inner(out_of_plane, ray) == 0,
        "tidal_cross_zero": tidal_cross == 0,
        "tidal_in_formula": sp.simplify(tidal_in - expected_in) == 0,
        "tidal_out_formula": sp.simplify(tidal_out - expected_out) == 0,
        "vertex_in_slope": sp.simplify(
            in_initial_slope.subs(cosine_alpha**2, 1 - sine_alpha**2) - 1
        ) == 0,
        "vertex_out_slope": out_initial_slope == 1,
        "flat_tidal_zero": all(flat_controls.values()),
        "schwarzschild_trace_zero": sp.simplify(
            schwarzschild_controls["in"] + schwarzschild_controls["out"]
        ) == 0,
    }

    phi_prime, phi_second = sp.symbols("phi_prime phi_second", real=True)
    phi_form_out = sp.factor(
        expected_out.subs(
            {
                sp.diff(f, r): -2 * f * phi_prime,
            }
        )
    )
    phi_form_in = sp.factor(
        expected_in.subs(
            {
                sp.diff(f, r, 2): 4 * f * phi_prime**2 - 2 * f * phi_second,
                sp.diff(f, r): -2 * f * phi_prime,
            }
        )
    )

    result = {
        "audit": "G187_PRODUCTION",
        "checks": checks,
        "finite_map": (
            "D=diag(D_parallel,D_perp) in the propagated orbital/reflection screen; "
            "D_parallel solves D''+T_parallel D=0 with D(0)=0,D'(0)=1; "
            "D_perp=r sin(varphi-varphi_o)/sin(alpha_o)"
        ),
        "first_integrals": {
            "angular": "L=r^2 varphi_dot",
            "energy": "E=f t_dot",
            "radial": "r_dot^2=E^2-f L^2/r^2",
        },
        "landing": LANDING,
        "screen_tidal": {
            "cross": str(tidal_cross),
            "parallel": str(expected_in),
            "parallel_phi_form": str(phi_form_in),
            "perpendicular": str(expected_out),
            "perpendicular_phi_form": str(phi_form_out),
            "trace": str(sp.factor(expected_in + expected_out)),
        },
        "status": "PASS" if all(checks.values()) else "FAIL",
        "controls": {
            "flat": flat_controls,
            "schwarzschild_parallel": str(schwarzschild_controls["in"]),
            "schwarzschild_perpendicular": str(schwarzschild_controls["out"]),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
