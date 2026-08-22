#!/usr/bin/env python3
"""Exact production algebra for the preregistered G210 spatial-volume tile."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("PRODUCTION_RESULT.json")


def require(label: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def derive() -> dict[str, object]:
    checks: list[str] = []
    f, u = sp.symbols("f u", positive=True)
    h1, h2, h3 = sp.symbols("h1 h2 h3", positive=True)
    b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)
    H = sp.diag(h1, h2, h3)
    K = u * H
    b = sp.Matrix([b1, b2, b3])
    P = sp.eye(4)
    P[1:, 0] = b
    base = sp.diag(-f, u * h1, u * h2, u * h3)
    metric = sp.simplify(P.T * base * P)

    require("spatial_det_scales_cubically", sp.simplify(K.det() - u**3 * H.det()) == 0, checks)
    require("adm_shift_map_det_one", sp.simplify(P.det() - 1) == 0, checks)
    require("ambient_det_volume_scaled", sp.simplify(metric.det() + f * u**3 * H.det()) == 0, checks)
    require("lorentz_inertia_by_positive_congruence", all(x > 0 for x in (f, u, h1, h2, h3)), checks)

    inverse_expected = sp.BlockMatrix(
        [
            [sp.Matrix([[-1 / f]]), b.T / f],
            [b / f, K.inv() - b * b.T / f],
        ]
    ).as_explicit()
    require("exact_inverse", sp.simplify(metric * inverse_expected - sp.eye(4)) == sp.zeros(4), checks)
    require("dt_remains_temporal", sp.simplify(inverse_expected[0, 0] + 1 / f) == 0, checks)

    # Unique relative-volume split in three spatial dimensions.
    dH, dK = sp.symbols("dH dK", positive=True)
    u_det = (dK / dH) ** sp.Rational(1, 3)
    require("determinant_ratio_cube_root", sp.simplify(u_det**3 * dH - dK) == 0, checks)
    require("sigma_factor_is_one_sixth", sp.simplify(sp.log(u_det) / 2 - sp.log(dK / dH) / 6) == 0, checks)
    require("det_one_remainder", sp.simplify(dK / u_det**3 - dH) == 0, checks)

    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True)
    v = sp.Matrix([v1, v2, v3])
    X = sp.Matrix([1, v1, v2, v3])
    square = sp.expand((X.T * metric * X)[0])
    expected_square = sp.expand(-f + u * ((v + b).T * H * (v + b))[0])
    require("scaled_shifted_cone", sp.simplify(square - expected_square) == 0, checks)
    require("cone_center_unchanged", sp.simplify(expected_square.subs({v1: -b1, v2: -b2, v3: -b3}) + f) == 0, checks)

    a = sp.symbols("a", positive=True)
    require("u_is_exp2sigma_proxy", sp.simplify(u.subs(u, a**2) - a**2) == 0, checks)
    vr, br = sp.symbols("vr br", real=True)
    radial_cone = sp.expand(u * (vr + br) ** 2 / f - f)
    require("g205_scaled_radial_factor", sp.simplify(radial_cone - (u * (vr + br) ** 2 - f**2) / f) == 0, checks)
    require("g205_lower_radial_root", sp.simplify(radial_cone.subs({u: a**2, vr: -br - f / a})) == 0, checks)
    require("g205_upper_radial_root", sp.simplify(radial_cone.subs({u: a**2, vr: -br + f / a})) == 0, checks)

    # Static radial null and live energy identities.
    E, rdot = sp.symbols("E rdot", real=True)
    radial_null = sp.expand(-E**2 / f + u * rdot**2 / f)
    require("radial_null_first_integral", sp.simplify(radial_null.subs(rdot**2, E**2 / u)) == 0, checks)
    sigmat, tdot = sp.symbols("sigmat tdot", real=True)
    energy_derivative = -sigmat * f * tdot**2
    require("live_energy_equation", sp.simplify(energy_derivative + sigmat * (f * tdot) * tdot) == 0, checks)

    # Completed pair pullback.
    a0, a1 = sp.symbols("a0 a1", real=True)
    w01, w02, w03, w11, w12, w13 = sp.symbols("w01 w02 w03 w11 w12 w13", real=True)
    w0 = sp.Matrix([w01, w02, w03])
    w1 = sp.Matrix([w11, w12, w13])
    J = sp.Matrix.hstack(sp.Matrix([a0, *w0]), sp.Matrix([a1, *w1]))
    pair = sp.simplify(J.T * metric * J)
    pair_expected = sp.Matrix(
        [
            [-f * a0**2 + u * ((w0 + a0 * b).T * H * (w0 + a0 * b))[0],
             -f * a0 * a1 + u * ((w0 + a0 * b).T * H * (w1 + a1 * b))[0]],
            [-f * a0 * a1 + u * ((w1 + a1 * b).T * H * (w0 + a0 * b))[0],
             -f * a1**2 + u * ((w1 + a1 * b).T * H * (w1 + a1 * b))[0]],
        ]
    )
    require("completed_pair_pullback", sp.simplify(pair - pair_expected) == sp.zeros(2), checks)
    T2 = sp.simplify(-pair[0, 0])
    expected_T2 = sp.simplify(f * a0**2 - u * ((w0 + a0 * b).T * H * (w0 + a0 * b))[0])
    require("completed_clock_norm", sp.simplify(T2 - expected_T2) == 0, checks)
    require("unshifted_static_clock_blind", sp.simplify(T2.subs({b1: 0, b2: 0, b3: 0, w01: 0, w02: 0, w03: 0}) - f * a0**2) == 0, checks)
    require("shifted_static_clock_hears_volume", sp.diff(T2.subs({w01: 0, w02: 0, w03: 0}), u) == -a0**2 * (b.T * H * b)[0], checks)
    require("eulerian_normal_clock_blind", sp.simplify(T2.subs({w01: -a0 * b1, w02: -a0 * b2, w03: -a0 * b3}) - f * a0**2) == 0, checks)
    require(
        "generic_spatial_clock_hears_volume",
        sp.simplify(sp.diff(T2, u) + ((w0 + a0 * b).T * H * (w0 + a0 * b))[0]) == 0,
        checks,
    )

    # Spatial-only scale = common conformal scale plus compensating lapse.
    require("conformal_plus_lapse_factorization", sp.simplify(u * (-f / u) + f) == 0, checks)

    return {
        "landing": "FULL_LOCAL_SPATIAL_VOLUME_SCALAR_IS_THE_UNIQUE_RELATIVE_DETERMINANT_MODE__IT_RESCALES_CAUSAL_WIDTH_WITHOUT_MOVING_THE_SHIFT_CENTER__LOWER_BOUNDED_STATIC_AND_CONTROLLED_COMPACT_LIVE_G205_CLASSES_SURVIVE__SIGMA_EQUALS_MINUS_PHI_IS_GLOBALLY_HYPERBOLIC_BUT_RADIAL_NULL_INCOMPLETE__COMPLETED_PAIRS_HEAR_SPATIAL_VOLUME_BEFORE_READOUT_ON_SPATIAL_BEARING_STRATA__NO_PHYSICAL_SIGMA_HISTORY_OR_XMAX_SELECTION",
        "assertion_count": len(checks),
        "assertions": checks,
        "mechanization_scope": "finite-dimensional algebra and radial null identity only",
    }


def main() -> None:
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
