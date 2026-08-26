#!/usr/bin/env python3
"""Direct symbolic G271 primary-metric null-screen first-jet derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT__"
    "ONE_PRIMARY_METRIC_GRADIENT_GENERATES_DEPTH_AND_TRANSPORTED_SCREEN_CHANNELS__"
    "RADIAL_AND_QUIET_STRATA_EXACT__NO_FINITE_PATH_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)
MUTATIONS = (
    "flip_connection_sign",
    "drop_lapse_factor",
    "flip_screen_orientation",
    "omit_frequency",
    "force_w_zero",
    "wrong_depth_sign",
)


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(sp.trigsimp(expr)) == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--mutation", choices=MUTATIONS)
    args = parser.parse_args()

    t, r, theta, varphi = sp.symbols("t r theta varphi", real=True)
    coords = (t, r, theta, varphi)
    phi = sp.Function("phi")(r)
    p = sp.diff(phi, r)
    q = sp.exp(-phi)
    omega = sp.symbols("omega", positive=True)
    alpha = sp.symbols("alpha", real=True)
    lam = sp.symbols("lam", real=True)

    metric = sp.diag(-q**2, q**-2, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse[a, d]
                * (
                    sp.diff(metric[d, c], coords[b])
                    + sp.diff(metric[d, b], coords[c])
                    - sp.diff(metric[b, c], coords[d])
                )
                for d in range(4)
            )
        )
        for c in range(4)] for b in range(4)] for a in range(4)]

    def dot(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
        return sp.simplify((x.T * metric * y)[0])

    def nabla_along(x: sp.Matrix, y: sp.Matrix) -> sp.Matrix:
        values = []
        for a in range(4):
            directional = sum(x[b] * sp.diff(y[a], coords[b]) for b in range(4))
            connection = sum(
                x[b] * gamma[a][b][c] * y[c]
                for b in range(4)
                for c in range(4)
            )
            values.append(sp.simplify(directional + connection))
        return sp.Matrix(values)

    u = sp.Matrix([1 / q, 0, 0, 0])
    e_r = sp.Matrix([0, q, 0, 0])
    e_theta = sp.Matrix([0, 0, 1 / r, 0])
    e_varphi = sp.Matrix([0, 0, 0, 1 / (r * sp.sin(theta))])
    acceleration = sp.simplify(nabla_along(u, u))
    acceleration_expected = sp.Matrix([0, -q**2 * p, 0, 0])
    acceleration_hat = sp.simplify(dot(acceleration, e_r))

    x_symbols = sp.symbols("x0:4", real=True)
    x = sp.Matrix(x_symbols)
    congruence_left = sp.simplify(nabla_along(x, u))
    congruence_right = sp.simplify(-dot(x, u) * acceleration)

    equator = {theta: sp.pi / 2}
    e_phi_eq = sp.simplify(e_varphi.subs(equator))
    n = sp.simplify(sp.cos(alpha) * e_r + sp.sin(alpha) * e_phi_eq)
    screen = sp.simplify(-sp.sin(alpha) * e_r + sp.cos(alpha) * e_phi_eq)
    k = sp.simplify(omega * (u + n))

    implemented_acceleration_hat = acceleration_hat
    if args.mutation == "flip_connection_sign":
        implemented_acceleration_hat = -implemented_acceleration_hat
    elif args.mutation == "drop_lapse_factor":
        implemented_acceleration_hat = -p

    depth_jet = sp.simplify(k[1] * p)
    if args.mutation == "wrong_depth_sign":
        depth_jet = -depth_jet

    screen_jet = sp.simplify(-omega * implemented_acceleration_hat * sp.sin(alpha))
    if args.mutation == "flip_screen_orientation":
        screen_jet = -screen_jet
    elif args.mutation == "omit_frequency":
        screen_jet = sp.simplify(screen_jet / omega)
    elif args.mutation == "force_w_zero":
        screen_jet = sp.Integer(0)

    normalized_depth = sp.simplify(depth_jet / omega)
    normalized_screen = sp.simplify(screen_jet / omega)
    common_amplitude = sp.simplify(q * p)

    k_radial = sp.simplify(omega * (u + e_r))
    radial_theta_transport = sp.simplify(nabla_along(k_radial, e_theta).subs(equator))
    radial_phi_transport = sp.simplify(nabla_along(k_radial, e_varphi).subs(equator))
    equatorial_theta_transport = sp.simplify(nabla_along(k, e_theta).subs(equator))

    delta_first = sp.symbols("delta_first", real=True)
    w_first = sp.symbols("w_first", real=True)
    delta_series = delta_first * lam
    w_series = w_first * lam
    ratio_series = sp.exp(-delta_series)
    gamma_series = sp.cosh(delta_series) + ratio_series * w_series**2 / 2
    mutual_series = sp.series(1 / gamma_series, lam, 0, 3).removeO()
    sech_series = sp.series(sp.sech(delta_series), lam, 0, 3).removeO()

    checks: dict[str, bool] = {}
    checks["metric_inverse"] = all(
        zero(value)
        for value in sp.simplify(metric * inverse - sp.eye(4))
    )
    checks["clock_unit"] = zero(dot(u, u) + 1)
    checks["radial_frame_unit"] = zero(dot(e_r, e_r) - 1)
    checks["angular_frame_unit"] = zero(dot(e_phi_eq, e_phi_eq).subs(equator) - 1)
    checks["acceleration_direct"] = all(
        zero(value) for value in acceleration - acceleration_expected
    )
    checks["acceleration_orthonormal"] = zero(acceleration_hat + q * p)
    checks["static_congruence_identity"] = all(
        zero(value) for value in congruence_left - congruence_right
    )
    checks["null_direction_unit"] = zero(dot(n, n).subs(equator) - 1)
    checks["screen_unit"] = zero(dot(screen, screen).subs(equator) - 1)
    checks["screen_pair_orthogonal"] = zero(dot(screen, n).subs(equator))
    checks["null_tangent"] = zero(dot(k, k).subs(equator))
    checks["frequency_normalization"] = zero(-dot(k, u).subs(equator) - omega)
    checks["depth_jet_direct"] = zero(depth_jet - omega * q * p * sp.cos(alpha))
    checks["screen_jet_from_acceleration"] = zero(
        screen_jet + omega * acceleration_hat * sp.sin(alpha)
    )
    checks["screen_jet_expected"] = zero(
        screen_jet - omega * q * p * sp.sin(alpha)
    )
    checks["affine_normalized_depth"] = zero(
        normalized_depth - q * p * sp.cos(alpha)
    )
    checks["affine_normalized_screen"] = zero(
        normalized_screen - q * p * sp.sin(alpha)
    )
    checks["angular_pythagorean_split"] = zero(
        normalized_depth**2 + normalized_screen**2 - common_amplitude**2
    )
    checks["radial_screen_first_jet"] = zero(screen_jet.subs(alpha, 0))
    checks["tangential_depth_first_jet"] = zero(
        depth_jet.subs(alpha, sp.pi / 2)
    )
    checks["quiet_depth_first_jet"] = zero(depth_jet.subs(p, 0))
    checks["quiet_screen_first_jet"] = zero(screen_jet.subs(p, 0))
    checks["gradient_sign_reversal_depth"] = zero(
        depth_jet.xreplace({p: -p}) + depth_jet
    )
    checks["gradient_sign_reversal_screen"] = zero(
        screen_jet.xreplace({p: -p}) + screen_jet
    )
    checks["radial_theta_screen_parallel"] = all(
        zero(value) for value in radial_theta_transport
    )
    checks["radial_phi_screen_parallel"] = all(
        zero(value) for value in radial_phi_transport
    )
    checks["equatorial_out_of_plane_parallel"] = all(
        zero(value) for value in equatorial_theta_transport
    )
    checks["mutual_leading_term"] = zero(
        mutual_series - (1 - (delta_first**2 + w_first**2) * lam**2 / 2)
    )
    checks["sech_leading_term"] = zero(
        sech_series - (1 - delta_first**2 * lam**2 / 2)
    )
    checks["screen_gap_leading_term"] = zero(
        sech_series - mutual_series - w_first**2 * lam**2 / 2
    )

    failed = [name for name, passed in checks.items() if not passed]
    if args.mutation:
        print(json.dumps({
            "status": "MUTATION_CAUGHT" if failed else "MUTATION_SURVIVED",
            "mutation": args.mutation,
            "failed_checks": failed,
        }, indent=2, sort_keys=True))
        return

    assert not failed, failed

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": "C__NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT",
        "static_congruence": "nabla_X U=-g(X,U)*a",
        "acceleration": "a_hat_r=-exp(-phi)*phi_prime",
        "exact_screen_evolution": "dW_I/dlambda=omega*g(a,E_I) for parallel transported screen E_I",
        "normalized_depth_jet": "(1/omega)*d(delta)/dlambda=exp(-phi)*phi_prime*cos(alpha)",
        "normalized_screen_jet": "(1/omega)*d(W_s)/dlambda=exp(-phi)*phi_prime*sin(alpha)",
        "interlock": "depth_jet_normalized^2+screen_jet_normalized^2=exp(-2phi)*phi_prime^2",
        "leading_mutual_gap": "sech(delta)-M_PT=(1/2)*(dW_s/dlambda at A)^2*lambda^2+O(lambda^3)",
        "radial": "W=0 exactly on the regular static-radial stratum",
        "quiet": "phi_prime=0 makes both local first jets zero",
        "phi_sign": "value sign alone does not select either jet; exp(-phi) rescales and phi_prime sets orientation",
        "finite_path": "OPEN_REQUIRES_SUPPLIED_PROFILE_BRANCH_AND_TRANSPORT_INTEGRATION",
        "history_distance_xmax": "OPEN_NOT_SELECTED",
        "exact_checks": len(checks),
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
