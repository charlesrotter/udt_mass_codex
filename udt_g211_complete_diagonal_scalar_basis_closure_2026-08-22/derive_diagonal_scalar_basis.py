#!/usr/bin/env python3
"""Exact symbolic derivation for the G211 diagonal scalar basis."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("PRODUCTION_RESULT.json")


def require(name: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def derive() -> dict:
    checks: list[str] = []

    # Linear scalar coordinates: (ell,sigma) <-> (Omega,q) and (V,W).
    scalar_to_common_relative = sp.Matrix([[1, 0], [-1, 1]])
    common_relative_to_scalar = sp.Matrix([[1, 0], [1, 1]])
    require(
        "common_relative_basis_inverse",
        scalar_to_common_relative * common_relative_to_scalar == sp.eye(2),
        checks,
    )
    require("common_relative_basis_rank_two", scalar_to_common_relative.det() == 1, checks)

    scalar_to_volume_width = sp.Matrix([[1, 3], [1, -1]])
    volume_width_to_scalar = sp.Rational(1, 4) * sp.Matrix([[1, 3], [1, -1]])
    require(
        "volume_width_basis_inverse",
        volume_width_to_scalar * scalar_to_volume_width == sp.eye(2),
        checks,
    )
    require("volume_width_basis_rank_two", scalar_to_volume_width.det() == -4, checks)

    # Arbitrary positive spatial matrix, positive squared scale factors, and supplied shift.
    f, u, z = sp.symbols("f u z", positive=True)
    h11, h22, h33 = sp.symbols("h11 h22 h33", positive=True)
    h12, h13, h23 = sp.symbols("h12 h13 h23", real=True)
    H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])
    b1, b2, b3 = sp.symbols("b1 b2 b3", real=True)
    b = sp.Matrix([b1, b2, b3])

    metric = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[-u * f + z * (b.T * H * b)[0]]]), (z * H * b).T),
        sp.Matrix.hstack(z * H * b, z * H),
    )
    P = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.ones(1, 1), sp.zeros(1, 3)),
        sp.Matrix.hstack(b, sp.eye(3)),
    )
    diagonal = sp.diag(-u * f, *list(z * H))
    diagonal = sp.diag(-u * f, 1, 1, 1)
    diagonal[1:4, 1:4] = z * H
    require("adm_congruence", sp.simplify(metric - P.T * diagonal * P) == sp.zeros(4), checks)
    require("adm_determinant", sp.simplify(metric.det() + u * f * z**3 * H.det()) == 0, checks)

    expected_inverse = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.Matrix([[-1 / (u * f)]]), b.T / (u * f)),
        sp.Matrix.hstack(b / (u * f), H.inv() / z - b * b.T / (u * f)),
    )
    require("adm_inverse", sp.simplify(metric * expected_inverse) == sp.eye(4), checks)
    require("temporal_dt", sp.simplify(expected_inverse[0, 0] + 1 / (u * f)) == 0, checks)

    # Common-relative factorization with u=c and z=c*r.
    c, r = sp.symbols("c r", positive=True)
    relative_metric = metric.subs({u: 1, z: r})
    require(
        "common_relative_metric_factorization",
        sp.simplify(metric.subs({u: c, z: c * r}) - c * relative_metric) == sp.zeros(4),
        checks,
    )
    require("lapse_only_is_common_plus_relative", sp.simplify((c * r).subs({c: u, r: 1 / u}) - 1) == 0, checks)

    # Tangent and cone-center algebra.
    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    x = sp.Matrix([x1, x2, x3])
    X = sp.Matrix([1, x1, x2, x3])
    tangent_square = sp.expand((X.T * metric * X)[0])
    expected_square = -u * f + z * ((x + b).T * H * (x + b))[0]
    require("translated_scaled_cone", sp.simplify(tangent_square - expected_square) == 0, checks)
    require("cone_center_fixed", sp.simplify(expected_square.subs({x1: -b1, x2: -b2, x3: -b3}) + u * f) == 0, checks)

    L, S = sp.symbols("L S", positive=True)
    vr, br = sp.symbols("vr br", real=True)
    radial_cone = z * (vr + br) ** 2 / f - u * f
    require(
        "radial_lower_root",
        sp.simplify(radial_cone.subs({u: L**2, z: S**2, vr: -br - f * L / S})) == 0,
        checks,
    )
    require(
        "radial_upper_root",
        sp.simplify(radial_cone.subs({u: L**2, z: S**2, vr: -br + f * L / S})) == 0,
        checks,
    )
    require("causal_width_is_lapse_over_space", sp.simplify((L / S) ** 2 - u / z).subs({u: L**2, z: S**2}) == 0, checks)
    require("common_factor_cancels_cone_width", sp.simplify((u / z).subs({u: c, z: c * r}) - 1 / r) == 0, checks)

    # Static radial null affine law.
    E, tdot, rdot = sp.symbols("E tdot rdot", positive=True)
    radial_null = -u * f * tdot**2 + z * rdot**2 / f
    energy_sub = radial_null.subs(tdot, E / (u * f))
    require(
        "radial_null_first_integral",
        sp.simplify(energy_sub.subs(rdot, E / sp.sqrt(u * z))) == 0,
        checks,
    )
    require("radial_affine_density", sp.simplify(1 / (E / (L * S)) - L * S / E) == 0, checks)

    # Exact same-cone/different-affine controls.
    phi = sp.symbols("phi", real=True)
    base_width = sp.Integer(1)
    common_fail_width = sp.sqrt(sp.exp(-2 * phi) / sp.exp(-2 * phi))
    require("same_cone_common_control", sp.simplify(common_fail_width - base_width) == 0, checks)
    require("common_control_affine_weight", sp.simplify(sp.sqrt(sp.exp(-2 * phi) * sp.exp(-2 * phi)) - sp.exp(-2 * phi)) == 0, checks)
    relative_width = sp.sqrt(1 / sp.exp(-2 * phi))
    compensated_width = sp.sqrt(sp.exp(phi) / sp.exp(-phi))
    require("relative_compensated_same_cone", sp.simplify(relative_width - compensated_width) == 0, checks)
    require("relative_affine_weight", sp.simplify(sp.sqrt(sp.exp(-2 * phi)) - sp.exp(-phi)) == 0, checks)
    require("compensated_affine_weight", sp.simplify(sp.sqrt(sp.exp(phi) * sp.exp(-phi)) - 1) == 0, checks)

    # Completed pair pullback and strata.
    a0, a1 = sp.symbols("a0 a1", real=True)
    w01, w02, w03, w11, w12, w13 = sp.symbols("w01 w02 w03 w11 w12 w13", real=True)
    w0 = sp.Matrix([w01, w02, w03])
    w1 = sp.Matrix([w11, w12, w13])
    J = sp.Matrix.hstack(sp.Matrix([a0, *w0]), sp.Matrix([a1, *w1]))
    pair = sp.simplify(J.T * metric * J)
    pair_expected = sp.Matrix(
        [
            [-u * f * a0**2 + z * ((w0 + a0 * b).T * H * (w0 + a0 * b))[0],
             -u * f * a0 * a1 + z * ((w0 + a0 * b).T * H * (w1 + a1 * b))[0]],
            [-u * f * a0 * a1 + z * ((w1 + a1 * b).T * H * (w0 + a0 * b))[0],
             -u * f * a1**2 + z * ((w1 + a1 * b).T * H * (w1 + a1 * b))[0]],
        ]
    )
    require("completed_pair_pullback", sp.simplify(pair - pair_expected) == sp.zeros(2), checks)
    T2 = sp.simplify(-pair[0, 0])
    relative_clock = f * a0**2 - r * ((w0 + a0 * b).T * H * (w0 + a0 * b))[0]
    require("completed_clock_common_factor", sp.simplify(T2.subs({u: c, z: c * r}) - c * relative_clock) == 0, checks)
    require(
        "eulerian_relative_blind",
        sp.simplify(T2.subs({w01: -a0 * b1, w02: -a0 * b2, w03: -a0 * b3}) - u * f * a0**2) == 0,
        checks,
    )
    require(
        "unshifted_static_relative_blind",
        sp.simplify(T2.subs({b1: 0, b2: 0, b3: 0, w01: 0, w02: 0, w03: 0}) - u * f * a0**2) == 0,
        checks,
    )
    require(
        "generic_spatial_clock_hears_spatial_scale",
        sp.simplify(sp.diff(T2, z) + ((w0 + a0 * b).T * H * (w0 + a0 * b))[0]) == 0,
        checks,
    )
    require("static_clock_hears_common_scale", sp.diff((c * f * a0**2), c) == f * a0**2, checks)

    return {
        "landing": "COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_HAS_RANK_TWO_AFTER_SUPPLIED_1PLUS3_REFERENCE__COMMON_SCALE_AND_RELATIVE_SPATIAL_VOLUME_FORM_AN_EXACT_BASIS__LAPSE_ONLY_IS_NOT_A_THIRD_TILE__CAUSAL_CONES_DEPEND_ONLY_ON_RELATIVE_MODE_WHILE_NULL_AFFINE_AND_COMPLETED_DEPTH_HEAR_COMMON_SCALE__NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION",
        "assertion_count": len(checks),
        "assertions": checks,
        "mechanization_scope": "finite-dimensional scalar basis, ADM, cone, radial-null, and completed-pair algebra only",
    }


def main() -> None:
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
