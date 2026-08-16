#!/usr/bin/env python3
"""Exact checks for the bounded static-spherical chord and P1 center obstruction."""

import json

import sympy as sp


def main() -> None:
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    c_e, n, x_eff = sp.symbols("c_E n X_eff", positive=True)
    f = sp.Function("f")(r)
    f_pair = sp.symbols("f_pair", positive=True)

    # In y0=c_E*tau and y1=r, a radial null graph has dt/dr=1/(c_E*f).
    h00 = -f_pair
    h01 = sp.simplify(-f_pair * c_e**2 * (1 / c_e) * (1 / (c_e * f_pair)))
    h11 = sp.simplify(-f_pair * c_e**2 * (1 / (c_e * f_pair)) ** 2 + 1 / f_pair)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    det_h = sp.simplify(h.det())
    phi_pair = sp.simplify(sp.log((-det_h) / h00**2) / 4)

    # Derive the Ricci scalar directly from the four-dimensional metric rather than assuming it.
    coords = (t, r, theta, azimuth)
    metric = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = sp.simplify(metric.inv())
    dimension = 4
    gamma = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coords[b])
                            + sp.diff(metric[d, b], coords[c])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        for d in range(dimension)
                    )
                    / 2
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]
    ricci = sp.MutableDenseMatrix.zeros(dimension, dimension)
    for a in range(dimension):
        for b in range(dimension):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(gamma[c][a][b], coords[c])
                    - sp.diff(gamma[c][a][c], coords[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(dimension)
                    )
                    for c in range(dimension)
                )
            )
    ricci_scalar = sp.factor(
        sum(
            inverse[a, b] * ricci[a, b]
            for a in range(dimension)
            for b in range(dimension)
        )
    )
    expected_ricci = sp.factor(
        -sp.diff(f, r, 2) - 4 * sp.diff(f, r) / r + 2 * (1 - f) / r**2
    )

    p1_f = (1 - r / (n * x_eff)) ** n
    p1_phi = -sp.Rational(1, 2) * sp.log(p1_f)
    p1_ricci = sp.simplify(ricci_scalar.subs(f, p1_f).doit())
    angular_sectional = sp.simplify((1 - p1_f) / r**2)

    checks = {
        "pair_h00": sp.simplify(h[0, 0] + f_pair) == 0,
        "pair_h01": sp.simplify(h[0, 1] + 1) == 0,
        "pair_h11": sp.simplify(h[1, 1]) == 0,
        "pair_determinant": det_h == -1,
        "terminal_depth": sp.simplify(phi_pair + sp.log(f_pair) / 2) == 0,
        "direct_ricci_formula": sp.simplify(ricci_scalar - expected_ricci) == 0,
        "p1_phi_origin": sp.simplify(sp.limit(p1_phi, r, 0)) == 0,
        "p1_phi_prime_origin": sp.simplify(sp.limit(sp.diff(p1_phi, r), r, 0) - 1 / (2 * x_eff)) == 0,
        "p1_f_prime_origin": sp.simplify(sp.limit(sp.diff(p1_f, r), r, 0) + 1 / x_eff) == 0,
        "p1_scalar_curvature_residue": sp.simplify(sp.limit(r * p1_ricci, r, 0) - 6 / x_eff) == 0,
        "p1_angular_curvature_residue": sp.simplify(sp.limit(r * angular_sectional, r, 0) - 1 / x_eff) == 0,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "derived": {
            "h_parallel": [["-f", "-1"], ["-1", "0"]],
            "det_h": "-1",
            "phi_pair": "-(1/2) log(f)",
            "D_sky_on_central_spherical_subclass": "r I_2",
            "p1_f": "(1-r/(n X_eff))^n",
            "p1_phi_prime_at_origin": "1/(2 X_eff)",
            "p1_f_prime_at_origin": "-1/X_eff",
            "limit_r_times_Ricci_scalar": "6/X_eff",
            "limit_r_times_angular_sectional_curvature": "1/X_eff",
        },
        "scope": "static central spherical radial null subclass; P1 exact inward extrapolation",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
