#!/usr/bin/env python3
"""Exact off-diagonal orbit-metric witness for the G119 covariant theorem."""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    t, x, theta, varphi, lam = sp.symbols("t x theta varphi lambda", real=True)
    velocity = sp.Rational(1, 3)
    coordinates = (t, x, theta, varphi)
    scale = 1 + t
    old_radius = x + velocity * t
    areal = scale * old_radius

    # Flat-FLRW a(t)=1+t after the nontrivial radial coordinate change r=x+v t.
    metric = sp.Matrix([
        [-1 + scale**2 * velocity**2, scale**2 * velocity, 0, 0],
        [scale**2 * velocity, scale**2, 0, 0],
        [0, 0, areal**2, 0],
        [0, 0, 0, areal**2 * sp.sin(theta) ** 2],
    ])
    inverse = sp.simplify(metric.inv())
    dimension = 4
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2) * sum(
                inverse[i, ell] * (
                    sp.diff(metric[ell, k], coordinates[j])
                    + sp.diff(metric[ell, j], coordinates[k])
                    - sp.diff(metric[j, k], coordinates[ell])
                )
                for ell in range(dimension)
            )
        )
        for k in range(dimension)] for j in range(dimension)] for i in range(dimension)]

    def riemann(rho: int, sigma: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(
            sp.diff(gamma[rho][nu][sigma], coordinates[mu])
            - sp.diff(gamma[rho][mu][sigma], coordinates[nu])
            + sum(
                gamma[rho][mu][ell] * gamma[ell][nu][sigma]
                - gamma[rho][nu][ell] * gamma[ell][mu][sigma]
                for ell in range(dimension)
            )
        )

    s = sp.sqrt(1 + 2 * lam)
    path = {
        t: s - 1,
        x: sp.log(s) - velocity * (s - 1),
        theta: sp.pi / 2,
    }
    position = (path[t], path[x])
    tangent = tuple(sp.simplify(sp.diff(value, lam)) for value in position)
    tangent4 = sp.Matrix([tangent[0], tangent[1], 0, 0])

    null_residual = sp.simplify((tangent4.T * metric.subs(path) * tangent4)[0])
    geodesic_residuals = []
    for a in range(2):
        connection_term = sum(
            gamma[a][b][c].subs(path) * tangent[b] * tangent[c]
            for b in range(2) for c in range(2)
        )
        geodesic_residuals.append(sp.simplify(sp.diff(tangent[a], lam) + connection_term))

    direct_tidal = sp.simplify(sum(
        riemann(2, a, 2, b).subs(path) * tangent[a] * tangent[b]
        for a in range(2) for b in range(2)
    ))
    areal_path = sp.simplify(areal.subs(path))
    jacobi_residual = sp.simplify(sp.diff(areal_path, lam, 2) + direct_tidal * areal_path)

    checks = {
        "orbit_cross_term_nonzero": sp.simplify(metric[0, 1]) != 0,
        "null_residual": str(null_residual),
        "time_geodesic_residual": str(geodesic_residuals[0]),
        "shifted_radial_geodesic_residual": str(geodesic_residuals[1]),
        "direct_tidal": str(direct_tidal),
        "areal_radius": str(areal_path),
        "jacobi_residual": str(jacobi_residual),
        "all_exact_residuals_zero": all(
            value == 0 for value in (null_residual, *geodesic_residuals, jacobi_residual)
        ),
    }
    result = {
        "status": "PASS" if checks["orbit_cross_term_nonzero"] and checks["all_exact_residuals_zero"] else "FAIL",
        "checks": checks,
        "scope": "exact off-diagonal coordinate witness; covariant arbitrary-h_ab theorem remains analytic",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
