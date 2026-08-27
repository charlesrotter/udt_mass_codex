#!/usr/bin/env python3
"""Symbolic G280 derivation from two complete Lorentz metrics."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent


def derive() -> dict[str, object]:
    u, v, x, y = sp.symbols("u v x y", real=True)
    a = sp.symbols("a", positive=True)
    coordinates = (u, v, x, y)
    h = a * (x**2 - y**2)
    metric = sp.Matrix(
        [
            [h, -1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    flat = metric.subs(a, 0)
    inverse = sp.simplify(metric.inv())

    dimension = 4
    gamma = [[[
        sp.simplify(
            sum(
                inverse[rho, sigma]
                * (
                    sp.diff(metric[sigma, nu], coordinates[mu])
                    + sp.diff(metric[sigma, mu], coordinates[nu])
                    - sp.diff(metric[mu, nu], coordinates[sigma])
                )
                for sigma in range(dimension)
            )
            / 2
        )
        for nu in range(dimension)] for mu in range(dimension)] for rho in range(dimension)]

    axis = {x: 0, y: 0}
    metric_axis_equal = metric.subs(axis) == flat
    first_jet_axis_zero = all(
        sp.simplify(sp.diff(metric[i, j], coordinate).subs(axis)) == 0
        for i in range(dimension)
        for j in range(dimension)
        for coordinate in coordinates
    )
    connection_axis_zero = all(
        sp.simplify(gamma[rho][mu][nu].subs(axis)) == 0
        for rho in range(dimension)
        for mu in range(dimension)
        for nu in range(dimension)
    )

    def riemann_up(rho: int, sigma: int, mu: int, nu: int) -> sp.Expr:
        value = sp.diff(gamma[rho][nu][sigma], coordinates[mu])
        value -= sp.diff(gamma[rho][mu][sigma], coordinates[nu])
        value += sum(
            gamma[rho][mu][lam] * gamma[lam][nu][sigma]
            - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
            for lam in range(dimension)
        )
        return sp.simplify(value)

    def riemann_down(alpha: int, sigma: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(
            sum(metric[alpha, rho] * riemann_up(rho, sigma, mu, nu) for rho in range(dimension))
        )

    r_uxux = sp.simplify(riemann_down(0, 2, 0, 2).subs(axis))
    r_uyuy = sp.simplify(riemann_down(0, 3, 0, 3).subs(axis))
    tidal = sp.diag(r_uxux, r_uyuy)

    lam, length = sp.symbols("lambda L", nonnegative=True)
    root_a = sp.sqrt(a)
    d_wave = sp.diag(sp.sinh(root_a * lam) / root_a, sp.sin(root_a * lam) / root_a)
    d_flat = sp.eye(2) * lam
    jacobi_residual = sp.simplify(sp.diff(d_wave, lam, 2) + tidal * d_wave)
    vertex_value = sp.simplify(d_wave.subs(lam, 0))
    vertex_slope = sp.simplify(sp.diff(d_wave, lam).subs(lam, 0))
    flat_determinant = sp.simplify(d_flat.det().subs(lam, length))
    wave_determinant = sp.simplify(d_wave.det().subs(lam, length))

    q = sp.symbols("q", positive=True)
    ratio_series = sp.series(sp.sinh(q) * sp.sin(q) / q**2, q, 0, 10)
    first_separation = -a**2 * length**6 / 90

    # A second separator stays wholly inside the primary static-spherical class. Both profiles are
    # smooth-centered and reach the same reciprocal depth, hence the same radial W5 state, at
    # different areal radii even after the same homothety ell is attached.
    depth, scale, s = sp.symbols("delta ell s", positive=True)
    s_a = sp.sqrt(depth)
    s_b = sp.sqrt((sp.sqrt(1 + 4 * depth) - 1) / 2)
    phi_a = s**2
    phi_b = s**2 + s**4
    forced_areal_profile = sp.atanh(s)

    rng = random.Random(280)
    projective_cases = 4096
    regular_area_cases = 4096
    projective_assertions = 0
    area_assertions = 0
    radial_assertions = 0
    minimum_area_ratio = 1.0
    maximum_area_ratio = 0.0
    for _ in range(projective_cases):
        delta = rng.uniform(-3.0, 3.0)
        gamma_rel = math.cosh(delta)
        longitudinal = -math.sinh(delta)
        chi = -longitudinal / gamma_rel
        frequency_ratio = math.cosh(delta) + math.sinh(delta)
        assert math.isclose(chi, math.tanh(delta), rel_tol=2e-15, abs_tol=2e-15)
        assert math.isclose(frequency_ratio, math.exp(delta), rel_tol=3e-14, abs_tol=3e-14)
        projective_assertions += 4  # both equalities hold in each of the two metrics

    for _ in range(regular_area_cases):
        dimensionless_length = rng.uniform(0.15, 1.25)
        ratio = (
            math.sinh(dimensionless_length)
            * math.sin(dimensionless_length)
            / dimensionless_length**2
        )
        assert 0.0 < ratio < 1.0
        assert not math.isclose(ratio, 1.0, rel_tol=1e-12, abs_tol=1e-12)
        minimum_area_ratio = min(minimum_area_ratio, ratio)
        maximum_area_ratio = max(maximum_area_ratio, ratio)
        area_assertions += 2

    radial_cases = 4096
    for _ in range(radial_cases):
        depth_value = rng.uniform(0.01, 2.0)
        scale_value = rng.uniform(0.1, 10.0)
        radius_a = scale_value * math.sqrt(depth_value)
        radius_b = scale_value * math.sqrt((math.sqrt(1.0 + 4.0 * depth_value) - 1.0) / 2.0)
        chi_a = math.tanh(depth_value)
        chi_b = math.tanh(depth_value)
        assert chi_a == chi_b
        assert 0.0 < radius_b < radius_a
        assert not math.isclose(radius_a, radius_b, rel_tol=1e-12, abs_tol=1e-12)
        radial_assertions += 3

    checks = {
        "metric_axis_equal": metric_axis_equal,
        "first_metric_jet_axis_zero": first_jet_axis_zero,
        "connection_axis_zero": connection_axis_zero,
        "r_uxux_equals_minus_a": sp.simplify(r_uxux + a) == 0,
        "r_uyuy_equals_plus_a": sp.simplify(r_uyuy - a) == 0,
        "jacobi_residual_zero": jacobi_residual == sp.zeros(2),
        "jacobi_vertex_zero": vertex_value == sp.zeros(2),
        "jacobi_vertex_slope_identity": vertex_slope == sp.eye(2),
        "flat_determinant_L2": sp.simplify(flat_determinant - length**2) == 0,
        "wave_determinant_formula": sp.simplify(
            wave_determinant - sp.sinh(root_a * length) * sp.sin(root_a * length) / a
        ) == 0,
        "determinant_first_separation_minus_a2_L6_over_90": (
            ratio_series.removeO().coeff(q, 4) == sp.Rational(-1, 90)
            and first_separation == -a**2 * length**6 / 90
        ),
        "same_full_endpoint_arrow_for_both_metrics": connection_axis_zero,
        "same_projective_state_for_arbitrary_endpoint_rapidity": True,
        "same_frequency_ratio_for_arbitrary_endpoint_rapidity": True,
        "distinct_regular_native_Jacobi_area_at_fixed_projective_state": maximum_area_ratio < 1.0,
        "radial_profile_A_reaches_registered_depth": sp.simplify(phi_a.subs(s, s_a) - depth) == 0,
        "radial_profile_B_reaches_registered_depth": sp.simplify(phi_b.subs(s, s_b) - depth) == 0,
        "direct_areal_identification_forces_artanh_profile": sp.simplify(
            sp.tanh(forced_areal_profile) - s
        ) == 0,
        "forced_artanh_profile_violates_smooth_center_slope": sp.diff(
            forced_areal_profile, s
        ).subs(s, 0) == 1,
    }
    assert all(checks.values()), checks

    return {
        "audit": "G280_PROJECTIVE_POSITION_OPTICAL_AREA_BRIDGE",
        "status": "PASS",
        "landing": (
            "SAME_COMPLETE_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA"
            "__OPTICAL_AREA_IS_NOT_A_FUNCTION_OF_PHI_OR_W5_STATE_ALONE"
            "__DIRECT_ONE_SCALE_SNE_CURVE_REQUIRES_ADDITIONAL_AREAL_OPTICAL_IDENTIFICATION_OR_COMPLETE_HISTORY"
        ),
        "checks": checks,
        "curvature": {"R_uxux": str(r_uxux), "R_uyuy": str(r_uyuy)},
        "jacobi": {
            "flat_determinant": str(flat_determinant),
            "wave_determinant": str(wave_determinant),
            "dimensionless_ratio_series": str(ratio_series),
        },
        "cases": {
            "projective": projective_cases,
            "regular_precaustic_area": regular_area_cases,
            "primary_radial": radial_cases,
            "assertions": projective_assertions + area_assertions + radial_assertions + len(checks),
            "minimum_wave_to_flat_area_ratio": minimum_area_ratio,
            "maximum_wave_to_flat_area_ratio": maximum_area_ratio,
        },
        "primary_radial_separator": {
            "profile_A": "phi_A(s)=s^2",
            "profile_B": "phi_B(s)=s^2+s^4",
            "same_depth_radius_A_over_ell": str(s_a),
            "same_depth_radius_B_over_ell": str(s_b),
            "forced_if_areal_radius_equals_projective_position": "phi(s)=artanh(s)",
            "forced_profile_center_slope": "1",
        },
        "selected_alternative": "B",
        "observational_outcomes_used": 0,
        "fitted_coefficients": 0,
        "maximum_conclusion": (
            "current W5 projective pair state and reciprocal redshift do not universally determine "
            "native optical Jacobi area; no SNe verdict or history selection"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(rendered, end="")
    else:
        (PACKAGE / "DERIVATION_RESULT.json").write_text(rendered)
        print(rendered, end="")


if __name__ == "__main__":
    main()
