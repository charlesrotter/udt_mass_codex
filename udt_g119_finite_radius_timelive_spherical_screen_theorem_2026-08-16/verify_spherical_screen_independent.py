#!/usr/bin/env python3
"""Independent explicit time-live and numerical G119 verification."""

from __future__ import annotations

import json

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def exact_timelive_control() -> dict[str, object]:
    lam = sp.symbols("lambda", nonnegative=True)
    s = sp.sqrt(1 + 2 * lam)
    scale = s
    time = s - 1
    radius_coordinate = sp.log(s)
    k_time = sp.diff(time, lam)
    k_radius = sp.diff(radius_coordinate, lam)

    null_residual = sp.simplify(-k_time**2 + scale**2 * k_radius**2)
    time_geodesic = sp.simplify(
        sp.diff(time, lam, 2) + scale * k_radius**2
    )
    radial_geodesic = sp.simplify(
        sp.diff(radius_coordinate, lam, 2)
        + 2 * k_time * k_radius / scale
    )

    areal_radius = sp.simplify(scale * radius_coordinate)
    # Direct coordinate curvature: R^theta_{r theta r}=(da/dt)^2=1 and
    # R^theta_{t theta t}=-a_ddot/a=0 for a(t)=1+t.
    direct_tidal = sp.simplify(k_radius**2)
    jacobi_residual = sp.simplify(
        sp.diff(areal_radius, lam, 2) + direct_tidal * areal_radius
    )

    return {
        "null_residual": str(null_residual),
        "time_geodesic_residual": str(time_geodesic),
        "radial_geodesic_residual": str(radial_geodesic),
        "direct_tidal": str(direct_tidal),
        "jacobi_residual": str(jacobi_residual),
        "vertex_position": str(sp.simplify(areal_radius.subs(lam, 0))),
        "vertex_derivative": str(sp.simplify(sp.diff(areal_radius, lam).subs(lam, 0))),
        "all_exact_residuals_zero": all(
            value == 0
            for value in (null_residual, time_geodesic, radial_geodesic, jacobi_residual)
        ),
    }


def numerical_jacobi_control() -> dict[str, object]:
    def rhs(lam: float, state: np.ndarray) -> np.ndarray:
        tidal = 1.0 / (1.0 + 2.0 * lam) ** 2
        return np.array([state[1], -tidal * state[0]], dtype=np.float64)

    grid = np.linspace(0.0, 12.0, 1201)
    solution = solve_ivp(
        rhs,
        (grid[0], grid[-1]),
        np.array([0.0, 1.0], dtype=np.float64),
        t_eval=grid,
        method="DOP853",
        rtol=1.0e-12,
        atol=1.0e-14,
    )
    s = np.sqrt(1.0 + 2.0 * grid)
    exact = s * np.log(s)
    maximum_error = float(np.max(np.abs(solution.y[0] - exact)))
    return {
        "solver_success": bool(solution.success),
        "grid_points": int(grid.size),
        "lambda_final": float(grid[-1]),
        "maximum_absolute_error": maximum_error,
        "tolerance": 2.0e-10,
        "within_tolerance": maximum_error < 2.0e-10,
    }


def main() -> None:
    exact = exact_timelive_control()
    numeric = numerical_jacobi_control()
    checks = {
        "exact_timelive_control": exact,
        "numerical_jacobi_control": numeric,
    }
    status = (
        exact["all_exact_residuals_zero"]
        and exact["vertex_position"] == "0"
        and exact["vertex_derivative"] == "1"
        and numeric["solver_success"]
        and numeric["within_tolerance"]
    )
    result = {
        "status": "PASS" if status else "FAIL",
        "checks": checks,
        "scope": "independent flat-FLRW a(t)=1+t time-live control; not a history-selection claim",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if status else 1)


if __name__ == "__main__":
    main()
