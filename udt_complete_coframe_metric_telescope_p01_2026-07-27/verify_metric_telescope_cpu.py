#!/usr/bin/env python3
"""Independent NumPy/finite-difference verifier for the P01 GPU anchor.

This file intentionally does not import the production PyTorch evaluator.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


FIRST_OFFSETS = np.array([-2.0, -1.0, 1.0, 2.0])
FIRST_WEIGHTS = np.array([1.0, -8.0, 8.0, -1.0]) / 12.0


def basis(t: float, x: float) -> np.ndarray:
    return np.array(
        [
            1.0,
            x,
            (3.0 * x * x - 1.0) / 2.0,
            math.sin(math.pi * x),
            math.sin(math.pi * t),
            math.cos(math.pi * t),
            math.sin(math.pi * t) * math.cos(math.pi * x),
            math.cos(2.0 * math.pi * t) * math.sin(math.pi * x),
        ],
        dtype=np.float64,
    )


def amplitudes(coefficients: np.ndarray, shell: float, t: float, x: float) -> np.ndarray:
    return shell / math.sqrt(8.0) * coefficients @ basis(t, x)


def coframe(coefficients: np.ndarray, shell: float, t: float, x: float) -> tuple[np.ndarray, np.ndarray]:
    q = amplitudes(coefficients, shell, t, x)
    phi, sigma, alpha, k, s10, s11, s20, s21 = q
    clock = math.exp(-phi)
    ruler = math.exp(phi)
    r = math.exp(0.5 * sigma - alpha)
    qang = math.exp(0.5 * sigma + alpha)
    E = np.array(
        [
            [clock, 0.0, 0.0, 0.0],
            [0.0, ruler, 0.0, 0.0],
            [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
            [qang * s20, qang * s21, 0.0, qang],
        ],
        dtype=np.float64,
    )
    return E, q


def metric(coefficients: np.ndarray, shell: float, t: float, x: float) -> np.ndarray:
    E, _ = coframe(coefficients, shell, t, x)
    return E.T @ np.diag([-1.0, 1.0, 1.0, 1.0]) @ E


def first_derivative(function, t: float, x: float, axis: int, h: float) -> np.ndarray:
    result = None
    for offset, weight in zip(FIRST_OFFSETS, FIRST_WEIGHTS):
        value = function(t + (offset * h if axis == 0 else 0.0), x + (offset * h if axis == 1 else 0.0))
        result = weight * value if result is None else result + weight * value
    return result / h


def second_derivative(function, t: float, x: float, axis: int, h: float) -> np.ndarray:
    values = [
        function(t + (-2 * h if axis == 0 else 0.0), x + (-2 * h if axis == 1 else 0.0)),
        function(t + (-h if axis == 0 else 0.0), x + (-h if axis == 1 else 0.0)),
        function(t, x),
        function(t + (h if axis == 0 else 0.0), x + (h if axis == 1 else 0.0)),
        function(t + (2 * h if axis == 0 else 0.0), x + (2 * h if axis == 1 else 0.0)),
    ]
    return (-values[4] + 16 * values[3] - 30 * values[2] + 16 * values[1] - values[0]) / (12 * h * h)


def mixed_derivative(function, t: float, x: float, h: float) -> np.ndarray:
    result = None
    for ot, wt in zip(FIRST_OFFSETS, FIRST_WEIGHTS):
        for ox, wx in zip(FIRST_OFFSETS, FIRST_WEIGHTS):
            value = function(t + ot * h, x + ox * h)
            result = wt * wx * value if result is None else result + wt * wx * value
    return result / (h * h)


def scalar_curvature_fd(coefficients: np.ndarray, shell: float, t: float, x: float, h: float) -> tuple[float, np.ndarray, np.ndarray]:
    function = lambda tt, xx: metric(coefficients, shell, tt, xx)
    g = function(t, x)
    ginv = np.linalg.inv(g)
    dg = np.zeros((4, 4, 4), dtype=np.float64)
    ddg = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for axis in range(2):
        dg[axis] = first_derivative(function, t, x, axis, h)
        ddg[axis, axis] = second_derivative(function, t, x, axis, h)
    ddg[0, 1] = mixed_derivative(function, t, x, h)
    ddg[1, 0] = ddg[0, 1]
    dginv = np.zeros((4, 4, 4), dtype=np.float64)
    for axis in range(4):
        dginv[axis] = -ginv @ dg[axis] @ ginv
    B = np.zeros((4, 4, 4), dtype=np.float64)
    dB = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for s in range(4):
        for m in range(4):
            for n in range(4):
                B[s, m, n] = dg[m, s, n] + dg[n, s, m] - dg[s, m, n]
                for axis in range(4):
                    dB[axis, s, m, n] = ddg[axis, m, s, n] + ddg[axis, n, s, m] - ddg[axis, s, m, n]
    gamma = 0.5 * np.einsum("rs,smn->rmn", ginv, B)
    dgamma = 0.5 * (np.einsum("krs,smn->krmn", dginv, B) + np.einsum("rs,ksmn->krmn", ginv, dB))
    rup = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for r in range(4):
        for s in range(4):
            for m in range(4):
                for n in range(4):
                    product = 0.0
                    for ell in range(4):
                        product += gamma[r, m, ell] * gamma[ell, n, s] - gamma[r, n, ell] * gamma[ell, m, s]
                    rup[r, s, m, n] = dgamma[m, r, n, s] - dgamma[n, r, m, s] + product
    ricci = np.zeros((4, 4), dtype=np.float64)
    for r in range(4):
        ricci += rup[r, :, r, :]
    return float(np.einsum("mn,mn", ginv, ricci)), g, ginv


def phi_gradient_fd(coefficients: np.ndarray, shell: float, t: float, x: float, h: float) -> np.ndarray:
    function = lambda tt, xx: np.asarray(amplitudes(coefficients, shell, tt, xx)[0])
    result = np.zeros(4, dtype=np.float64)
    result[0] = first_derivative(function, t, x, 0, h)
    result[1] = first_derivative(function, t, x, 1, h)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("anchor", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--step", type=float, default=2.0e-4)
    args = parser.parse_args()
    payload = json.loads(args.anchor.read_text())
    coefficients = np.asarray(payload["coefficients"], dtype=np.float64)
    points = np.asarray(payload["points"], dtype=np.float64)
    reference_metric = np.asarray(payload["metric"], dtype=np.float64)
    reference_scalar = np.asarray(payload["scalar"], dtype=np.float64)
    reference_dphi = np.asarray(payload["dphi_norm"], dtype=np.float64)
    metric_errors, scalar_scaled_errors, dphi_scaled_errors = [], [], []
    cpu_scalar = np.empty_like(reference_scalar)
    for config_index, coefficient in enumerate(coefficients):
        for point_index, (t, x) in enumerate(points):
            scalar, g, ginv = scalar_curvature_fd(coefficient, payload["shell"], float(t), float(x), args.step)
            gradient = phi_gradient_fd(coefficient, payload["shell"], float(t), float(x), args.step)
            dphi_norm = float(gradient @ ginv @ gradient)
            cpu_scalar[config_index, point_index] = scalar
            metric_errors.append(float(np.max(np.abs(g - reference_metric[config_index, point_index]))))
            scalar_scaled_errors.append(abs(scalar - reference_scalar[config_index, point_index]) / (1.0 + abs(reference_scalar[config_index, point_index])))
            dphi_scaled_errors.append(abs(dphi_norm - reference_dphi[config_index, point_index]) / (1.0 + abs(reference_dphi[config_index, point_index])))
    maxima = {
        "metric_absolute": max(metric_errors),
        "scalar_scaled": max(scalar_scaled_errors),
        "dphi_norm_scaled": max(dphi_scaled_errors),
    }
    tolerances = {"metric_absolute": 5.0e-13, "scalar_scaled": 5.0e-5, "dphi_norm_scaled": 2.0e-9}
    checks = {name: bool(maxima[name] <= tolerance) for name, tolerance in tolerances.items()}
    result = {
        "schema": "udt-p01-independent-cpu-anchor-verification-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "NUMPY_DIRECT_COFRAME_PLUS_FOURTH_ORDER_FINITE_DIFFERENCES",
        "production_module_imported": False,
        "anchor_sha256": hashlib.sha256(args.anchor.read_bytes()).hexdigest(),
        "configurations": len(coefficients),
        "points_per_configuration": len(points),
        "finite_difference_step": args.step,
        "maxima": maxima,
        "tolerances_preregistered_in_verifier": tolerances,
        "checks": checks,
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "device": "CPU", "dtype": "float64"},
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
