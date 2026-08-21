#!/usr/bin/env python3
"""Exact symbolic G202 quiet-overlap and anchor classification."""

import json
import sympy as sp


def main() -> None:
    s = sp.symbols("s", real=True)
    phi_value, p_log, q_log = sp.symbols("phi P Q", real=True)
    a = sp.symbols("a", positive=True)

    amplitude_parallel = sp.exp(-2 * phi_value) * (2 * p_log**2 + 2 * p_log - q_log)
    amplitude_perp = 1 - sp.exp(-2 * phi_value) * (1 + p_log)
    assertions = []

    # Quiet zero-depth overlap iff the full logarithmic second jet vanishes.
    zero_depth = [sp.simplify(expr.subs(phi_value, 0))
                  for expr in (amplitude_parallel, amplitude_perp)]
    quiet_p = sp.solve(sp.Eq(zero_depth[1], 0), p_log)
    quiet_q = sp.solve(sp.Eq(zero_depth[0].subs(p_log, quiet_p[0]), 0), q_log)
    assertions.extend([quiet_p == [0], quiet_q == [0]])

    # Minimal nondegenerate analytic crossing control.
    cubic_phi = a * s**3
    cubic_p = sp.diff(cubic_phi, s)
    cubic_q = sp.diff(cubic_phi, s, 2)
    cubic_parallel = sp.simplify(amplitude_parallel.subs({
        phi_value: cubic_phi, p_log: cubic_p, q_log: cubic_q,
    }))
    cubic_perp = sp.simplify(amplitude_perp.subs({
        phi_value: cubic_phi, p_log: cubic_p,
    }))
    cubic_contrast = sp.cosh(2 * cubic_phi) - 1
    assertions.extend([
        cubic_phi.subs(s, 0) == 0,
        cubic_p.subs(s, 0) == 0,
        cubic_q.subs(s, 0) == 0,
        sp.simplify(cubic_p - 3 * a * s**2) == 0,
        sp.limit(cubic_phi, s, sp.oo) == sp.oo,
        sp.limit(cubic_phi, s, -sp.oo) == -sp.oo,
    ])
    cubic_series = {
        "parallel": sp.series(cubic_parallel, s, 0, 6).removeO(),
        "perpendicular": sp.series(cubic_perp, s, 0, 6).removeO(),
        "reciprocal_contrast": sp.series(cubic_contrast, s, 0, 8).removeO(),
    }
    assertions.extend([
        sp.expand(cubic_series["parallel"]).coeff(s, 1) == -6 * a,
        sp.expand(cubic_series["perpendicular"]).coeff(s, 2) == -3 * a,
        sp.expand(cubic_series["reciprocal_contrast"]).coeff(s, 6) == 2 * a**2,
    ])

    # Infinite monotone odd family: positive coefficients on s^3,s^5,s^7.
    b, c = sp.symbols("b c", nonnegative=True)
    odd_phi = a * s**3 + b * s**5 + c * s**7
    odd_p = sp.factor(sp.diff(odd_phi, s))
    odd_q = sp.diff(odd_phi, s, 2)
    assertions.extend([
        sp.simplify(odd_phi.subs(s, 0)) == 0,
        sp.simplify(odd_p.subs(s, 0)) == 0,
        sp.simplify(odd_q.subs(s, 0)) == 0,
        sp.simplify(odd_phi.subs(s, -s) + odd_phi) == 0,
        sp.simplify(odd_p - s**2 * (3 * a + 5 * b * s**2 + 7 * c * s**4)) == 0,
        sp.simplify(odd_phi - a * s**3 - s**5 * (b + c * s**2)) == 0,
    ])

    # Concrete finite-anchor counterfamily, preserving value and first two derivatives.
    epsilon = sp.symbols("epsilon", real=True)
    anchors = (-1, 0, 1)
    perturbation = sp.exp(-s**2) * (s + 1)**3 * s**3 * (s - 1)**3
    anchor_checks = []
    for anchor in anchors:
        for order in range(3):
            value = sp.simplify(sp.diff(perturbation, s, order).subs(s, anchor))
            anchor_checks.append(value)
            assertions.append(value == 0)
    perturbed_profile = cubic_phi + epsilon * perturbation
    assertions.extend([
        sp.limit(perturbation, s, sp.oo) == 0,
        sp.limit(perturbation, s, -sp.oo) == 0,
        sp.simplify(perturbed_profile - cubic_phi) != 0,
    ])

    # Dimensional exponent systems.  Columns are powers of c_E, G, and the added anchor.
    ae, bg, cm = sp.symbols("a_e b_G c_M")
    no_anchor = sp.solve([
        sp.Eq(ae + 3 * bg, 1), sp.Eq(-bg, 0), sp.Eq(-ae - 2 * bg, 0)
    ], (ae, bg), dict=True)
    mass_anchor = sp.solve([
        sp.Eq(ae + 3 * bg, 1), sp.Eq(-bg + cm, 0), sp.Eq(-ae - 2 * bg, 0)
    ], (ae, bg, cm), dict=True)
    drho = sp.symbols("d_rho")
    density_anchor = sp.solve([
        sp.Eq(ae + 3 * bg - 3 * drho, 1),
        sp.Eq(-bg + drho, 0),
        sp.Eq(-ae - 2 * bg, 0),
    ], (ae, bg, drho), dict=True)
    assertions.extend([
        no_anchor == [],
        mass_anchor == [{ae: -2, bg: 1, cm: 1}],
        density_anchor == [{ae: 1, bg: sp.Rational(-1, 2), drho: sp.Rational(-1, 2)}],
    ])

    payload = {
        "landing": (
            "QUIET_OVERLAP_FORCES_SECOND_ORDER_FLATNESS"
            "__TWO_SIDED_GROWTH_HAS_INFINITE_NATIVE_PROFILES"
            "__ANCHORS_CALIBRATE_BUT_DO_NOT_DERIVE_HISTORY"
        ),
        "all_pass": all(bool(item) for item in assertions),
        "assertions": len(assertions),
        "passed": sum(bool(item) for item in assertions),
        "log_radius_amplitudes": {
            "parallel": str(amplitude_parallel),
            "perpendicular": str(amplitude_perp),
        },
        "quiet_overlap_solution": {"P": str(quiet_p[0]), "Q": str(quiet_q[0])},
        "cubic_control": {
            "phi": str(cubic_phi),
            "P": str(cubic_p),
            "Q": str(cubic_q),
            "series": {key: str(value) for key, value in cubic_series.items()},
        },
        "infinite_odd_family_control": {"phi": str(odd_phi), "P": str(odd_p)},
        "finite_anchor_counterfamily": {
            "anchors": list(anchors),
            "orders_preserved": [0, 1, 2],
            "all_anchor_residuals": [str(value) for value in anchor_checks],
            "perturbation": str(perturbation),
        },
        "dimensional_length_solutions": {
            "cE_and_G_only": no_anchor,
            "with_mass": [{str(key): str(value) for key, value in row.items()}
                          for row in mass_anchor],
            "with_density": [{str(key): str(value) for key, value in row.items()}
                             for row in density_anchor],
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
