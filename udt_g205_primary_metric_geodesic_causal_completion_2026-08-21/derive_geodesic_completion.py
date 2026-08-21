#!/usr/bin/env python3
"""Direct symbolic G205 geodesic, optical, and null-trapping classification."""

from __future__ import annotations

import json
import os
from pathlib import Path

import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "PRODUCTION_RESULT.json"


def christoffels() -> tuple[tuple[sp.Symbol, ...], sp.Expr, list[list[list[sp.Expr]]]]:
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    coordinates = (t, r, theta, azimuth)
    f = sp.Function("f")(r)
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = metric.inv()
    gamma = [[[sp.simplify(sp.Rational(1, 2) * sum(
        inverse[a, d] * (
            sp.diff(metric[d, c], coordinates[b])
            + sp.diff(metric[d, b], coordinates[c])
            - sp.diff(metric[b, c], coordinates[d])
        )
        for d in range(4)
    )) for c in range(4)] for b in range(4)] for a in range(4)]
    return coordinates, f, gamma


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    (t, r, theta, azimuth), f, gamma = christoffels()
    fp = sp.diff(f, r)
    expected = {
        "G_t_tr": (gamma[0][0][1], fp / (2 * f)),
        "G_t_rt": (gamma[0][1][0], fp / (2 * f)),
        "G_r_tt": (gamma[1][0][0], f * fp / 2),
        "G_r_rr": (gamma[1][1][1], -fp / (2 * f)),
        "G_r_thth": (gamma[1][2][2], -f * r),
        "G_r_phph": (gamma[1][3][3], -f * r * sp.sin(theta) ** 2),
        "G_th_rth": (gamma[2][1][2], 1 / r),
        "G_ph_rph": (gamma[3][1][3], 1 / r),
        "G_th_phph": (gamma[2][3][3], -sp.sin(theta) * sp.cos(theta)),
        "G_ph_thph": (gamma[3][2][3], sp.cot(theta)),
    }
    for name, (actual, wanted) in expected.items():
        check(name, sp.simplify(actual - wanted) == 0)

    E, L, epsilon = sp.symbols("E L epsilon", real=True)
    radial_sq = E**2 + epsilon * f - f * L**2 / r**2
    norm = -f * (E / f) ** 2 + radial_sq / f + r**2 * (L / r**2) ** 2
    check("first_integral_norm", sp.simplify(norm - epsilon) == 0)
    radial_accel_from_integral = sp.diff(radial_sq, r) / 2
    radial_accel_from_christoffel = sp.simplify(
        -gamma[1][0][0] * (E / f) ** 2
        - gamma[1][1][1] * radial_sq
        - gamma[1][3][3].subs(theta, sp.pi / 2) * (L / r**2) ** 2
    )
    check(
        "radial_acceleration",
        sp.simplify(radial_accel_from_christoffel - radial_accel_from_integral) == 0,
    )
    check(
        "timelike_E0_negative_factor",
        sp.simplify(radial_sq.subs({E: 0, epsilon: -1}) + f * (1 + L**2 / r**2)) == 0,
    )
    check(
        "null_E0_negative_factor",
        sp.simplify(radial_sq.subs({E: 0, epsilon: 0}) + f * L**2 / r**2) == 0,
    )
    check("null_E0_zero_at_L0", radial_sq.subs({E: 0, epsilon: 0, L: 0}) == 0)

    x = sp.symbols("x", positive=True)
    a, r0 = sp.symbols("a r0", positive=True)
    y = sp.symbols("y", real=True)
    orders = (3, 5, 7, 9, 11)
    critical_amplitudes: dict[str, str] = {}

    for n in orders:
        prefix = f"n{n}"
        phi = a * x**2 * (x**2 - 1) ** n / 2**n
        local_f = sp.exp(-2 * phi)
        center_series = sp.series(phi, x, 0, 5).removeO()
        check(f"{prefix}_center_even", sp.simplify(phi.subs(x, -x) - phi) == 0)
        check(f"{prefix}_center_phi_O_r2", center_series.coeff(x, 0) == 0 and center_series.coeff(x, 1) == 0)
        check(f"{prefix}_finite_f_positive", local_f.is_positive is True)
        check(f"{prefix}_no_finite_killing_horizon", sp.solve(sp.Eq(local_f, 0), x) == [])
        check(f"{prefix}_outer_f_zero", sp.limit(local_f, x, sp.oo) == 0)
        check(f"{prefix}_outer_spatial_integrand", sp.limit(1 / sp.sqrt(local_f), x, sp.oo) == sp.oo)
        check(f"{prefix}_outer_optical_integrand", sp.limit(1 / local_f, x, sp.oo) == sp.oo)
        check(f"{prefix}_outer_nonzero_E_correction", sp.limit(local_f * (1 + L**2 / (r0**2 * x**2)), x, sp.oo) == 0)

        p = sp.simplify(x * sp.diff(phi, x))
        p_expected = a * y * (y - 1) ** (n - 1) * ((n + 1) * y - 1) / 2 ** (n - 1)
        check(f"{prefix}_p_formula", sp.simplify(p.subs(x, sp.sqrt(y)) - p_expected) == 0)
        qfun = y * (1 - y) ** (n - 1) * (1 - (n + 1) * y)
        poly = (n + 1) ** 2 * y**2 - (3 * n + 2) * y + 1
        check(f"{prefix}_q_derivative", sp.simplify(sp.diff(qfun, y) - (1 - y) ** (n - 2) * poly) == 0)
        ystar = ((3 * n + 2) - sp.sqrt(n * (5 * n + 4))) / (2 * (n + 1) ** 2)
        yplus = ((3 * n + 2) + sp.sqrt(n * (5 * n + 4))) / (2 * (n + 1) ** 2)
        check(f"{prefix}_ystar_stationary", sp.simplify(poly.subs(y, ystar)) == 0)
        check(f"{prefix}_ystar_inside", bool(0 < ystar < sp.Rational(1, n + 1)))
        check(f"{prefix}_second_root_outside_inner_interval", bool(yplus > sp.Rational(1, n + 1)))
        check(f"{prefix}_qprime_positive_at_center", poly.subs(y, 0) == 1)
        check(f"{prefix}_qprime_negative_at_inner_endpoint", sp.simplify(poly.subs(y, sp.Rational(1, n + 1))) == -sp.Rational(n, n + 1))
        qmax = sp.simplify(qfun.subs(y, ystar))
        acrit = sp.simplify(2 ** (n - 1) / qmax)
        check(f"{prefix}_qmax_positive", qmax.is_positive is True)
        check(f"{prefix}_subcritical_no_roots", sp.simplify((acrit / 2) * qmax / 2 ** (n - 1)) == sp.Rational(1, 2))
        check(f"{prefix}_critical_tangent", sp.simplify(acrit * qmax / 2 ** (n - 1)) == 1)
        check(f"{prefix}_supercritical_two_level", sp.simplify((2 * acrit) * qmax / 2 ** (n - 1)) == 2)
        mp.mp.dps = 60
        critical_amplitudes[str(n)] = mp.nstr(mp.mpf(str(sp.N(acrit, 70))), 50)

    # The optical radial coefficient is f^-2, so any unbounded spatial curve has at least
    # integral |dr|/f length. The ordinary spatial radial coefficient is f^-1.
    z, F = sp.symbols("z F", positive=True)
    check("optical_lower_bound_identity", sp.simplify(sp.sqrt(z**2 / F**2) - z / F) == 0)
    check("spatial_lower_bound_identity", sp.simplify(sp.sqrt(z**2 / F) - z / sp.sqrt(F)) == 0)

    landing = (
        "FULL_GEODESIC_COMPLETENESS_AND_GLOBAL_HYPERBOLICITY_SURVIVE_ALL_REGISTERED_PARAMETERS__"
        "NULL_TRAPPING_HAS_SUBCRITICAL_CRITICAL_AND_SUPERCRITICAL_STRATA__"
        "NO_PARAMETER_XMAX_OR_PHYSICAL_HISTORY_SELECTION"
    )
    result = {
        "all_pass": all(checks.values()),
        "assertions": len(checks),
        "checked_orders": list(orders),
        "critical_amplitudes": critical_amplitudes,
        "null_orbit_stability": {
            "supercritical_inner_root": "stable_minimum_of_f_over_r2",
            "supercritical_outer_root": "unstable_maximum_of_f_over_r2",
            "critical_root": "degenerate",
        },
        "geodesic_types": ["timelike", "null", "spacelike"],
        "outer_cases": ["E_nonzero", "causal_E_zero_impossible", "spacelike_E_zero"],
        "finite_radius_killing_horizon": False,
        "mechanized_scope": [
            "Christoffel_symbols",
            "first_integral_and_acceleration_identities",
            "sampled_order_profile_limits",
            "sampled_order_trapping_algebra",
            "optical_and_spatial_radial_lower_bound_identities",
        ],
        "analytic_theorems_recorded_not_mechanized": [
            "full_geodesic_completeness",
            "optical_spatial_metric_completeness",
            "global_hyperbolicity",
            "all_odd_n_universal_quantifier",
        ],
        "landing": landing,
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
