#!/usr/bin/env python3
"""Exact G119 direct-curvature and finite-dimensional screen checks."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def direct_warped_curvature_check() -> dict[str, object]:
    """Rebuild the relevant 4D curvature block from a generic diagonal orbit chart."""
    t, r, theta, varphi = sp.symbols("t r theta varphi", real=True)
    kt, kr = sp.symbols("k_t k_r", real=True)
    coordinates = (t, r, theta, varphi)
    A = sp.Function("A")(t, r)
    B = sp.Function("B")(t, r)
    R = sp.Function("R")(t, r)
    metric = sp.diag(-A**2, B**2, R**2, R**2 * sp.sin(theta) ** 2)
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

    # Convention: R^rho_{ sigma mu nu} Z^sigma X^mu Y^nu = (R(X,Y)Z)^rho.
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

    k = (kt, kr)
    acceleration = []
    for a in range(2):
        acceleration.append(sp.simplify(-sum(
            gamma[a][b][c] * k[b] * k[c]
            for b in range(2) for c in range(2)
        )))

    second_R = sp.simplify(
        sp.diff(R, t, 2) * kt**2
        + 2 * sp.diff(R, t, r) * kt * kr
        + sp.diff(R, r, 2) * kr**2
        + sp.diff(R, t) * acceleration[0]
        + sp.diff(R, r) * acceleration[1]
    )
    tidal = sp.simplify(sum(
        riemann(2, a, 2, b) * k[a] * k[b]
        for a in range(2) for b in range(2)
    ))
    residual = sp.simplify(tidal + second_R / R)
    return {
        "generic_mixed_curvature_identity": residual == 0,
        "generic_mixed_curvature_residual": str(residual),
    }


def finite_screen_checks() -> dict[str, object]:
    rho, rho_1, rho_2 = sp.symbols("rho rho_1 rho_2", real=True, nonzero=True)
    rotation = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                          [sp.Rational(4, 5), sp.Rational(3, 5)]])
    reflection = sp.diag(1, -1)
    eye = sp.eye(2)

    screen = rho * rotation
    tidal = -(rho_2 / rho) * eye
    jacobi_residual = sp.simplify(rho_2 * rotation + tidal * screen)
    optical = sp.simplify((rho_1 * rotation) * screen.inv())
    shear = sp.simplify((optical + optical.T) / 2 - sp.trace(optical) * eye / 2)
    twist = sp.simplify((optical - optical.T) / 2)

    reflected = reflection * screen
    caustic_lambda = sp.pi
    caustic_D = sp.sin(caustic_lambda) * eye
    caustic_Ddot = sp.cos(caustic_lambda) * eye

    return {
        "rotation_is_orthogonal": zero_matrix(rotation.T * rotation - eye),
        "rotation_determinant": str(sp.simplify(rotation.det())),
        "jacobi_residual_zero": zero_matrix(jacobi_residual),
        "optical_matrix": [[str(value) for value in optical.row(i)] for i in range(2)],
        "shear_zero": zero_matrix(shear),
        "twist_zero": zero_matrix(twist),
        "absolute_area_equals_rho_squared": sp.simplify(screen.det() - rho**2) == 0,
        "reflection_flips_signed_not_absolute_area": (
            sp.simplify(reflected.det() + rho**2) == 0
        ),
        "caustic_position_rank": caustic_D.rank(),
        "caustic_derivative_rank": caustic_Ddot.rank(),
        "caustic_phase_survives": caustic_D.rank() == 0 and caustic_Ddot.rank() == 2,
    }


def main() -> None:
    checks = {}
    checks.update(direct_warped_curvature_check())
    checks.update(finite_screen_checks())
    boolean_checks = [value for value in checks.values() if isinstance(value, bool)]
    result = {
        "status": "PASS" if boolean_checks and all(boolean_checks) else "FAIL",
        "checks": checks,
        "scope": (
            "generic diagonal orbit chart plus exact finite-dimensional basis/caustic controls; "
            "the semantic theorem also requires the declared smooth central spherical query"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
