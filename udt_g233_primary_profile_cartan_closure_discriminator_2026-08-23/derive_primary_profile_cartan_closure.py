#!/usr/bin/env python3
"""Exact G233 production derivation from the full primary spherical metric.

This is a local, metric-led discriminator.  It does not select a profile or
perform a jet-dimension census.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("exact_results.json")


def full_metric_scalar():
    t, s, theta, azimuth = sp.symbols("t s theta azimuth", real=True)
    r0, c_e = sp.symbols("r0 c_E", positive=True)
    f = sp.Function("f")(s)
    r = r0 * sp.exp(s)
    coords = (t, s, theta, azimuth)
    g = sp.diag(-c_e**2 * f, r**2 / f, r**2, r**2 * sp.sin(theta) ** 2)
    gi = sp.simplify(g.inv())
    dim = 4

    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for upper in range(dim):
        for left in range(dim):
            for right in range(dim):
                value = sp.S.Zero
                for q in range(dim):
                    value += gi[upper, q] * (
                        sp.diff(g[q, right], coords[left])
                        + sp.diff(g[q, left], coords[right])
                        - sp.diff(g[left, right], coords[q])
                    )
                gamma[upper][left][right] = sp.simplify(value / 2)

    ricci = [[sp.S.Zero for _ in range(dim)] for _ in range(dim)]
    for left in range(dim):
        for right in range(dim):
            value = sp.S.Zero
            for k in range(dim):
                value += sp.diff(gamma[k][left][right], coords[k])
                value -= sp.diff(gamma[k][left][k], coords[right])
                for ell in range(dim):
                    value += gamma[k][left][right] * gamma[ell][k][ell]
                    value -= gamma[ell][left][k] * gamma[k][right][ell]
            ricci[left][right] = sp.simplify(value)

    scalar = sp.simplify(sum(gi[i, j] * ricci[i][j] for i in range(dim) for j in range(dim)))
    expected = sp.exp(-2 * s) / r0**2 * (
        -sp.diff(f, s, 2) - 3 * sp.diff(f, s) + 2 * (1 - f)
    )
    return {
        "coords": coords,
        "r0": r0,
        "c_e": c_e,
        "f": f,
        "g": g,
        "gamma": gamma,
        "ricci": ricci,
        "scalar": scalar,
        "expected": expected,
        "scalar_check": sp.simplify(scalar - expected),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    direct = full_metric_scalar()
    _, s, theta, _ = direct["coords"]
    r0 = direct["r0"]
    c_e = direct["c_e"]
    b, c = sp.symbols("b c", real=True)
    phi = s**3 + c * s**4 + b * s**5
    f_profile = sp.exp(-2 * phi)

    scalar = sp.simplify(direct["expected"].subs(direct["f"], f_profile).doit())
    radial_speed = sp.exp(-phi - s) / r0

    def radial_derivative(expr):
        return sp.simplify(radial_speed * sp.diff(expr, s))

    radial_values = []
    value = scalar
    for _ in range(4):
        radial_values.append(sp.simplify(value.subs(s, 0)))
        value = radial_derivative(value)

    expected_radial = [
        sp.S.Zero,
        12 / r0**3,
        24 * (2 * c - 1) / r0**4,
        12 * (20 * b - 24 * c + 1) / r0**5,
    ]

    # The radial unit field is geodesic, so repeated radial derivatives of a
    # scalar equal the all-radial components of its covariant derivatives.
    accel = []
    for mu in range(4):
        component = direct["gamma"][mu][1][1] * radial_speed**2
        if mu == 1:
            component += radial_speed * sp.diff(radial_speed, s)
        component = component.subs(direct["f"], f_profile).doit()
        accel.append(sp.simplify(component))

    r = r0 * sp.exp(s)
    g_profile = sp.diag(
        -c_e**2 * f_profile,
        r**2 / f_profile,
        r**2,
        r**2 * sp.sin(theta) ** 2,
    )
    g0 = g_profile.subs(b, 0)
    g1 = g_profile.subs(b, 1)
    common_point = {s: 0, theta: sp.pi / 2}
    jet_differences = {}
    for order in range(6):
        entries = []
        for i in range(4):
            for j in range(4):
                delta = sp.diff(g1[i, j] - g0[i, j], s, order).subs(common_point)
                entries.append(sp.simplify(delta))
        jet_differences[str(order)] = entries

    # General finite-order principal-symbol control.  If the curvature state
    # is prolonged through nabla^N R, b*s^(N+3) first appears in the next
    # all-radial derivative of scalar curvature.
    arbitrary_order_checks = {}
    for order in range(7):
        phi_n = s**3 + b * s ** (order + 3)
        f_n = sp.exp(-2 * phi_n)
        scalar_n = sp.simplify(direct["expected"].subs(direct["f"], f_n).doit())
        speed_n = sp.exp(-phi_n - s) / r0
        next_value = scalar_n
        for _ in range(order + 1):
            next_value = sp.simplify(speed_n * sp.diff(next_value, s))
        b_coefficient = sp.simplify(sp.diff(next_value.subs(s, 0), b))
        expected_coefficient = 2 * sp.factorial(order + 3) / r0 ** (order + 3)
        arbitrary_order_checks[str(order)] = {
            "coefficient": str(b_coefficient),
            "expected": str(expected_coefficient),
            "pass": sp.simplify(b_coefficient - expected_coefficient) == 0,
        }

    # Fixed-n G204 conditional finite-state closure control.
    x, amplitude, scale = sp.symbols("x amplitude scale", real=True, positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    phi_g204 = amplitude * x**2 * (x**2 - 1) ** n / 2**n
    f_g204 = sp.exp(-2 * phi_g204)
    f_r = sp.diff(f_g204, x) / scale
    f_rr = sp.diff(f_g204, x, 2) / scale**2
    scalar_g204 = sp.simplify(
        -f_rr - 4 * f_r / (scale * x) + 2 * (1 - f_g204) / (scale**2 * x**2)
    )
    x_flow = sp.exp(-phi_g204) / scale
    scalar_flow = sp.simplify(x_flow * sp.diff(scalar_g204, x))
    allowed_symbols = {x, amplitude, scale, n}

    checks = {
        "full_metric_scalar_matches_primary_formula": direct["scalar_check"] == 0,
        "metric_jets_zero_through_order_four": all(
            entry == 0 for order in range(5) for entry in jet_differences[str(order)]
        ),
        "metric_fifth_jet_differs": any(entry != 0 for entry in jet_differences["5"]),
        "radial_unit_field_is_geodesic": all(component == 0 for component in accel),
        "g231_scalar_contractions_match": all(
            sp.simplify(radial_values[k] - expected_radial[k]) == 0 for k in range(3)
        ),
        "next_scalar_contraction_matches": sp.simplify(radial_values[3] - expected_radial[3]) == 0,
        "next_scalar_contraction_depends_on_b": sp.simplify(sp.diff(radial_values[3], b) - 240 / r0**5) == 0,
        "arbitrary_finite_orders_match_principal_coefficient": all(
            item["pass"] for item in arbitrary_order_checks.values()
        ),
        "g204_state_flow_is_finite": x_flow.free_symbols <= allowed_symbols,
        "g204_scalar_is_state_function": scalar_g204.free_symbols <= allowed_symbols,
        "g204_scalar_flow_is_state_function": scalar_flow.free_symbols <= allowed_symbols,
    }

    result = {
        "landing": (
            "FIXED_MEMBER_CARTAN_DESCENT_IS_EVALUATIVE"
            "__FINITE_G204_CLOSURE_IS_FAMILY_CONDITIONAL"
            "__UNRESTRICTED_PRIMARY_PROFILE_HAS_NO_UNIVERSAL_FINITE_JET_AUTONOMOUS_CLOSURE"
            "__VALUED_PAIR_NETWORK_ENCODES_BUT_DOES_NOT_GENERATE_PROFILE"
        ),
        "scope": "local primary static-spherical regular orbit; finite-order natural autonomous laws",
        "full_metric_scalar": str(direct["scalar"]),
        "scalar_profile": str(scalar),
        "radial_values_orders_0_to_3": [str(item) for item in radial_values],
        "next_difference_b1_minus_b0": str(sp.simplify(radial_values[3].subs(b, 1) - radial_values[3].subs(b, 0))),
        "metric_jet_nonzero_counts": {
            order: sum(entry != 0 for entry in entries) for order, entries in jet_differences.items()
        },
        "arbitrary_order_checks": arbitrary_order_checks,
        "g204": {
            "phi": str(phi_g204),
            "state": ["x", "amplitude", "scale", "n"],
            "x_flow": str(x_flow),
            "parameter_flows": {"amplitude": "0", "scale": "0", "n": "0"},
            "scalar_free_symbols": sorted(str(symbol) for symbol in scalar_g204.free_symbols),
            "scalar_flow_free_symbols": sorted(str(symbol) for symbol in scalar_flow.free_symbols),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
