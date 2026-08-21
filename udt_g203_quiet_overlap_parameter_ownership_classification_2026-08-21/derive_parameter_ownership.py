#!/usr/bin/env python3
"""Exact symbolic G203 quiet-overlap descriptor classification."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "PRODUCTION_RESULT.json"


def main() -> None:
    s, u = sp.symbols("s u", real=True)
    a, r0, c1 = sp.symbols("a r0 c1", positive=True)
    b, c2, c3 = sp.symbols("b c2 c3", real=True)
    checks: dict[str, bool] = {}

    def check(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    orders = (3, 5, 7, 9, 11, 13)
    psi = c1 * u + c2 * u**2 + c3 * u**3

    for n in orders:
        phi = a * s**n
        prefix = f"n{n}"
        check(f"{prefix}_value_quiet", sp.simplify(phi.subs(s, 0)) == 0)
        check(f"{prefix}_first_jet_quiet", sp.simplify(sp.diff(phi, s).subs(s, 0)) == 0)
        check(f"{prefix}_second_jet_quiet", sp.simplify(sp.diff(phi, s, 2).subs(s, 0)) == 0)
        check(f"{prefix}_leading_jet", sp.simplify(sp.diff(phi, s, n).subs(s, 0) / math.factorial(n) - a) == 0)
        check(f"{prefix}_positive_derivative_factor", sp.simplify(sp.diff(phi, s) - n * a * s ** (n - 1)) == 0)
        check(f"{prefix}_sign_factor", sp.simplify(phi / s - a * s ** (n - 1)) == 0)
        check(f"{prefix}_odd", sp.simplify(phi.subs(s, -s) + phi) == 0)

        composed = sp.Poly(sp.expand(a * psi**n + b * psi ** (n + 1)), u)
        check(
            f"{prefix}_reparam_lower_coefficients_zero",
            all(composed.coeff_monomial(u**k) == 0 for k in range(n)),
        )
        check(
            f"{prefix}_reparam_leading_coefficient",
            sp.simplify(composed.coeff_monomial(u**n) - a * c1**n) == 0,
        )

    # A quiet analytic crossing need not be a globally odd function of the chosen history argument.
    nonodd = s**3 + b * s**4
    check("nonodd_value_quiet", nonodd.subs(s, 0) == 0)
    check("nonodd_first_jet_quiet", sp.diff(nonodd, s).subs(s, 0) == 0)
    check("nonodd_second_jet_quiet", sp.diff(nonodd, s, 2).subs(s, 0) == 0)
    check("nonodd_profile_not_odd", sp.simplify(nonodd.subs(s, -s) + nonodd) == 2 * b * s**4)
    check("nonodd_local_monotone_factor", sp.factor(sp.diff(nonodd, s)) == s**2 * (4 * b * s + 3))

    # Positive areal radius is rigid when the angular metric is retained in areal form.
    R = sp.symbols("R", positive=True)
    check(
        "areal_factorization",
        sp.simplify((R**2 - r0**2) - (R - r0) * (R + r0)) == 0,
    )
    check("areal_positive_root", sp.solve(R**2 - r0**2, R) == [r0])
    area0 = 4 * sp.pi * r0**2
    check("quiet_orbit_area_recovers_r0", sp.simplify(sp.sqrt(area0 / (4 * sp.pi)) - r0) == 0)

    # Reciprocal algebra holds for every profile value and does not reference n, r0, or a.
    x, y = sp.symbols("x y", real=True)
    D = lambda z: sp.diag(sp.exp(-z), sp.exp(z))
    check("reciprocal_composition", sp.simplify(D(x) * D(y) - D(x + y)) == sp.zeros(2))
    check("reciprocal_reversal", sp.simplify(D(-x) - D(x).inv()) == sp.zeros(2))
    check("reciprocal_determinant", sp.simplify(D(x).det() - 1) == 0)

    # Reversal changes the sign of the leading coefficient but preserves its magnitude and order.
    n = 7
    phi7 = a * s**n
    reverse_lead = sp.diff(-phi7, s, n).subs(s, 0) / math.factorial(n)
    check("reversal_flips_leading_sign", sp.simplify(reverse_lead + a) == 0)
    check("reversal_preserves_leading_magnitude", sp.simplify(reverse_lead**2 - a**2) == 0)

    # Dimensional exponent systems. Dimensions are ordered (L, M, T).
    xc, xg, xm, xr = sp.symbols("x_c x_g x_m x_r")
    no_extra = sp.solve(
        (sp.Eq(xc + 3 * xg, 1), sp.Eq(-xg, 0), sp.Eq(-xc - 2 * xg, 0)),
        (xc, xg),
        dict=True,
    )
    with_mass = sp.solve(
        (sp.Eq(xc + 3 * xg, 1), sp.Eq(-xg + xm, 0), sp.Eq(-xc - 2 * xg, 0)),
        (xc, xg, xm),
        dict=True,
    )
    with_density = sp.solve(
        (
            sp.Eq(xc + 3 * xg - 3 * xr, 1),
            sp.Eq(-xg + xr, 0),
            sp.Eq(-xc - 2 * xg, 0),
        ),
        (xc, xg, xr),
        dict=True,
    )
    check("ce_g_alone_no_length", no_extra == [])
    check("mass_candidate_exponents", with_mass == [{xc: -2, xg: 1, xm: 1}])
    check(
        "density_candidate_exponents",
        with_density == [{xc: 1, xg: -sp.Rational(1, 2), xr: -sp.Rational(1, 2)}],
    )

    result = {
        "all_pass": all(checks.values()),
        "assertions": len(checks),
        "checked_orders": list(orders),
        "landing": (
            "INVARIANT_AFTER_AREAL_AND_DEPTH_CALIBRATION__"
            "FOUNDING_DOES_NOT_SELECT_ORDER_LOCATION_OR_STEEPNESS__"
            "OBSERVATIONS_MAY_CALIBRATE_A_DECLARED_FAMILY"
        ),
        "classification": {
            "order": "INVARIANT_GERM_DESCRIPTOR__ODD_AT_LEAST_THREE__VALUE_UNSELECTED",
            "quiet_areal_radius": "GEOMETRIC_ON_SUPPLIED_HISTORY__VALUE_UNSELECTED",
            "leading_steepness": "DIMENSIONLESS_LOG_AREAL_JET__MAGNITUDE_UNSELECTED",
            "global_profile": "OPEN_INFINITE_DIMENSIONAL",
        },
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
