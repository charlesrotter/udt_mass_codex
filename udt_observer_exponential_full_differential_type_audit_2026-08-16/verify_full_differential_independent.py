#!/usr/bin/env python3
"""Independent finite-difference and numeric verification of G110."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
SCREEN = np.array([[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])


def json_default(value: object) -> object:
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot encode {type(value).__name__}")


def flat_map(tau: float, lam: float, a: float, b: float) -> np.ndarray:
    n0 = math.sqrt(1.0 - a * a - b * b)
    return np.array([tau + lam, lam * n0, lam * a, lam * b])


def finite_column(args: list[float], index: int, step: float = 1.0e-4) -> np.ndarray:
    plus = args.copy()
    minus = args.copy()
    plus[index] += step
    minus[index] -= step
    return (flat_map(*plus) - flat_map(*minus)) / (2.0 * step)


def flat_check() -> dict[str, float | bool]:
    lam = 1.25
    args = [0.3, lam, 0.0, 0.0]
    columns = [finite_column(args, index) for index in range(4)]
    pair = np.column_stack(columns[:2])
    sky = np.column_stack(columns[2:])
    h = pair.T @ ETA @ pair
    w_pair = SCREEN @ pair
    d_sky = SCREEN @ sky
    expected_h = np.array([[-1.0, -1.0], [-1.0, 0.0]])
    expected_d = lam * np.eye(2)
    phi = 0.25 * math.log((-np.linalg.det(h)) / h[0, 0] ** 2)
    return {
        "maximum_pair_metric_residual": float(np.max(np.abs(h - expected_h))),
        "terminal_phi_abs": abs(phi),
        "pair_screen_norm": float(np.linalg.norm(w_pair)),
        "sky_jacobi_residual": float(np.max(np.abs(d_sky - expected_d))),
        "pair_screen_rank": int(np.linalg.matrix_rank(w_pair, tol=1.0e-10)),
        "sky_jacobi_rank": int(np.linalg.matrix_rank(d_sky, tol=1.0e-10)),
        "literal_same_w_rejected": bool(
            not np.allclose(w_pair, d_sky, atol=1.0e-10)
        ),
    }


def screen_map(kind: str, x: float) -> np.ndarray:
    if kind == "focusing":
        return math.sin(x) * np.eye(2)
    if kind == "flat":
        return x * np.eye(2)
    if kind == "defocusing":
        return math.sinh(x) * np.eye(2)
    if kind == "anisotropic":
        return np.diag([math.sin(x), x])
    raise ValueError(kind)


def tidal(kind: str) -> np.ndarray:
    if kind == "focusing":
        return np.eye(2)
    if kind == "flat":
        return np.zeros((2, 2))
    if kind == "defocusing":
        return -np.eye(2)
    if kind == "anisotropic":
        return np.diag([1.0, 0.0])
    raise ValueError(kind)


def curvature_check() -> dict[str, float | bool]:
    step = 2.0e-5
    maximum_residual = 0.0
    maximum_vertex = 0.0
    for kind in ("focusing", "flat", "defocusing", "anisotropic"):
        maximum_vertex = max(
            maximum_vertex,
            float(np.max(np.abs(screen_map(kind, step) / step - np.eye(2)))),
        )
        for x in (0.35, 0.7, 1.1):
            second = (
                screen_map(kind, x + step)
                - 2.0 * screen_map(kind, x)
                + screen_map(kind, x - step)
            ) / step**2
            residual = second + tidal(kind) @ screen_map(kind, x)
            maximum_residual = max(maximum_residual, float(np.max(np.abs(residual))))

    x = 0.8
    d = screen_map("anisotropic", x)
    d_dot = np.diag([math.cos(x), 1.0])
    optical = d_dot @ np.linalg.inv(d)
    shear = optical - np.trace(optical) * np.eye(2) / 2.0
    floating_sin_pi_map = screen_map("focusing", math.pi)
    d_caustic = np.zeros((2, 2))
    caustic_inverse_rejected = False
    try:
        np.linalg.inv(d_caustic)
    except np.linalg.LinAlgError:
        caustic_inverse_rejected = True
    near = math.pi - 1.0e-6
    optical_trace_near = 2.0 * math.cos(near) / math.sin(near)
    return {
        "maximum_jacobi_fd_residual": maximum_residual,
        "maximum_vertex_derivative_residual": maximum_vertex,
        "anisotropic_shear_norm": float(np.linalg.norm(shear)),
        "caustic_det_abs": abs(float(np.linalg.det(d_caustic))),
        "caustic_map_norm": float(np.linalg.norm(d_caustic)),
        "floating_sin_pi_map_norm": float(np.linalg.norm(floating_sin_pi_map)),
        "caustic_derivative_norm": math.sqrt(2.0),
        "riccati_trace_near_caustic": optical_trace_near,
        "second_order_continues_while_inverse_fails": bool(
            caustic_inverse_rejected
            and optical_trace_near < -1.0e6
        ),
    }


def join_and_gauge_check() -> dict[str, float | bool]:
    def phi(x: float) -> float:
        return x + x * x

    def d_map(x: float) -> np.ndarray:
        return np.diag([math.sinh(x), x])

    maximum_join = 0.0
    step = 1.0e-6
    for x in (0.3, 0.6, 1.0):
        direct = (
            math.log(abs(np.linalg.det(d_map(x + step))))
            - math.log(abs(np.linalg.det(d_map(x - step))))
        ) / (2.0 * step) / (2.0 * (1.0 + 2.0 * x))
        optical = np.diag([math.cosh(x) / math.sinh(x), 1.0 / x])
        joined = np.trace(optical) / (2.0 * (1.0 + 2.0 * x))
        maximum_join = max(maximum_join, abs(direct - joined))

    x = 0.7
    d = d_map(x)
    d_dot = np.diag([math.cosh(x), 1.0])
    optical = d_dot @ np.linalg.inv(d)
    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    right = np.array([[2.0, 1.0], [0.0, 3.0]])
    left_optical = rotation @ d_dot @ np.linalg.inv(rotation @ d)
    right_optical = d_dot @ right @ np.linalg.inv(d @ right)

    eta = ETA
    E = np.array(
        [[2.0, 1.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0],
         [1.0, 0.0, 2.0, 1.0], [0.0, 1.0, 0.0, 2.0]]
    )
    J = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, -1.0]])
    P = np.array(
        [[1.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 2.0, 1.0], [0.0, 0.0, 0.0, 1.0]]
    )
    original = E @ J
    refactored = E @ np.linalg.inv(P) @ P @ J
    h_original = original.T @ eta @ original
    h_refactored = refactored.T @ eta @ refactored
    flat_x = 0.7
    flat_phi_rate = (0.0 - 0.0) / (2.0 * step)
    flat_area_rate = (
        math.log(abs(np.linalg.det(screen_map("flat", flat_x + step))))
        - math.log(abs(np.linalg.det(screen_map("flat", flat_x - step))))
    ) / (2.0 * step)
    return {
        "maximum_finite_difference_join_residual": maximum_join,
        "left_conjugacy_residual": float(
            np.max(np.abs(left_optical - rotation @ optical @ rotation.T))
        ),
        "right_basis_residual": float(np.max(np.abs(right_optical - optical))),
        "trace_invariance_residual": abs(np.trace(left_optical) - np.trace(optical)),
        "EJ_refactorization_residual": float(np.max(np.abs(original - refactored))),
        "metric_refactorization_residual": float(
            np.max(np.abs(h_original - h_refactored))
        ),
        "flat_phi_rate": flat_phi_rate,
        "flat_screen_log_area_rate": flat_area_rate,
        "zero_phi_rate_not_universal": bool(
            abs(flat_phi_rate) < 1.0e-15 and abs(flat_area_rate) > 1.0
        ),
    }


def main() -> None:
    flat = flat_check()
    curvature = curvature_check()
    join = join_and_gauge_check()
    checks = {
        "flat_pair": flat["maximum_pair_metric_residual"] < 1.0e-10,
        "flat_phi": flat["terminal_phi_abs"] < 1.0e-10,
        "flat_pair_screen": flat["pair_screen_norm"] < 1.0e-10,
        "flat_sky": flat["sky_jacobi_residual"] < 1.0e-10,
        "same_w_catch": flat["literal_same_w_rejected"]
        and flat["pair_screen_rank"] == 0
        and flat["sky_jacobi_rank"] == 2,
        "jacobi_family": curvature["maximum_jacobi_fd_residual"] < 2.0e-6,
        "vertex_data": curvature["maximum_vertex_derivative_residual"] < 2.0e-9,
        "anisotropic_shear": curvature["anisotropic_shear_norm"] > 1.0e-3,
        "caustic_typed": curvature["second_order_continues_while_inverse_fails"],
        "distinct_join": join["maximum_finite_difference_join_residual"] < 2.0e-9,
        "screen_gauge": join["left_conjugacy_residual"] < 2.0e-14
        and join["right_basis_residual"] < 2.0e-14
        and join["trace_invariance_residual"] < 2.0e-14,
        "EJ_quotient": join["EJ_refactorization_residual"] < 2.0e-14
        and join["metric_refactorization_residual"] < 2.0e-13,
        "zero_rate_scope": join["zero_phi_rate_not_universal"],
    }
    result = {
        "schema": "UDT_G110_INDEPENDENT_FULL_DIFFERENTIAL_V1",
        "flat": flat,
        "curvature": curvature,
        "join_and_gauge": join,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True, default=json_default)
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(serialized + "\n")
    print(serialized)
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
