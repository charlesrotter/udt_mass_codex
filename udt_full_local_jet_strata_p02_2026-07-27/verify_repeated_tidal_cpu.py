#!/usr/bin/env python3
"""Independent NumPy finite-difference check of P02-B repeated tides."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


OFFSETS = np.array([-2.0, -1.0, 1.0, 2.0])
WEIGHTS = np.array([1.0, -8.0, 8.0, -1.0]) / 12.0


def amplitudes(q: np.ndarray, dq: np.ndarray, ddq: np.ndarray, x: np.ndarray) -> np.ndarray:
    return q + dq @ x + 0.5 * np.einsum("aij,i,j->a", ddq, x, x)


def coframe_from_amplitudes(a: np.ndarray) -> np.ndarray:
    phi, sigma, alpha, k, s10, s11, s20, s21 = a
    r = math.exp(0.5 * sigma - alpha)
    qang = math.exp(0.5 * sigma + alpha)
    return np.array(
        [
            [math.exp(-phi), 0.0, 0.0, 0.0],
            [0.0, math.exp(phi), 0.0, 0.0],
            [r * (s10 + k * s20), r * (s11 + k * s21), r, k * r],
            [qang * s20, qang * s21, 0.0, qang],
        ],
        dtype=np.float64,
    )


def metric_from_amplitudes(a: np.ndarray) -> np.ndarray:
    coframe = coframe_from_amplitudes(a)
    return coframe.T @ np.diag((-1.0, 1.0, 1.0, 1.0)) @ coframe


def first(function, axis: int, h: float) -> np.ndarray:
    result = None
    for offset, weight in zip(OFFSETS, WEIGHTS):
        x = np.zeros(4)
        x[axis] = offset * h
        value = function(x)
        result = weight * value if result is None else result + weight * value
    return result / h


def second(function, axis: int, h: float) -> np.ndarray:
    values = []
    for offset in (-2.0, -1.0, 0.0, 1.0, 2.0):
        x = np.zeros(4)
        x[axis] = offset * h
        values.append(function(x))
    return (-values[4] + 16 * values[3] - 30 * values[2] + 16 * values[1] - values[0]) / (12 * h * h)


def mixed(function, axis1: int, axis2: int, h: float) -> np.ndarray:
    result = None
    for offset1, weight1 in zip(OFFSETS, WEIGHTS):
        for offset2, weight2 in zip(OFFSETS, WEIGHTS):
            x = np.zeros(4)
            x[axis1] = offset1 * h
            x[axis2] = offset2 * h
            value = function(x)
            result = weight1 * weight2 * value if result is None else result + weight1 * weight2 * value
    return result / (h * h)


def geometry_fd(q: np.ndarray, dq: np.ndarray, ddq: np.ndarray, h: float) -> tuple[float, np.ndarray, np.ndarray]:
    function = lambda x: metric_from_amplitudes(amplitudes(q, dq, ddq, x))
    origin = np.zeros(4)
    g = function(origin)
    ginv = np.linalg.inv(g)
    dg = np.stack([first(function, axis, h) for axis in range(4)])
    ddg = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for axis in range(4):
        ddg[axis, axis] = second(function, axis, h)
    for axis1 in range(4):
        for axis2 in range(axis1 + 1, 4):
            ddg[axis1, axis2] = mixed(function, axis1, axis2, h)
            ddg[axis2, axis1] = ddg[axis1, axis2]
    dginv = np.stack([-ginv @ dg[axis] @ ginv for axis in range(4)])
    bterm = np.zeros((4, 4, 4), dtype=np.float64)
    dbterm = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for s in range(4):
        for m in range(4):
            for n in range(4):
                bterm[s, m, n] = dg[m, s, n] + dg[n, s, m] - dg[s, m, n]
                for axis in range(4):
                    dbterm[axis, s, m, n] = (
                        ddg[axis, m, s, n] + ddg[axis, n, s, m] - ddg[axis, s, m, n]
                    )
    gamma = 0.5 * np.einsum("rs,smn->rmn", ginv, bterm)
    dgamma = 0.5 * (
        np.einsum("krs,smn->krmn", dginv, bterm)
        + np.einsum("rs,ksmn->krmn", ginv, dbterm)
    )
    rup = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for r in range(4):
        for s in range(4):
            for m in range(4):
                for n in range(4):
                    product = sum(
                        gamma[r, m, ell] * gamma[ell, n, s]
                        - gamma[r, n, ell] * gamma[ell, m, s]
                        for ell in range(4)
                    )
                    rup[r, s, m, n] = dgamma[m, r, n, s] - dgamma[n, r, m, s] + product
    ricci = sum((rup[r, :, r, :] for r in range(4)), np.zeros((4, 4)))
    scalar = float(np.einsum("mn,mn", ginv, ricci))
    rdown = np.einsum("ar,rsmn->asmn", g, rup)
    dual = np.linalg.inv(coframe_from_amplitudes(q))
    rframe = np.einsum("ma,nb,pc,qd,mnpq->abcd", dual, dual, dual, dual, rdown)
    tidal = np.array(
        (
            rframe[2, 0, 2, 0],
            0.5 * (rframe[2, 0, 3, 0] + rframe[3, 0, 2, 0]),
            rframe[3, 0, 3, 0],
        )
    )
    return scalar, g, tidal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("anchor", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--step", type=float, default=2e-4)
    args = parser.parse_args()
    anchor = json.loads(args.anchor.read_text())
    q = np.asarray(anchor["q"], dtype=np.float64)
    dq = np.asarray(anchor["dq"], dtype=np.float64)
    ddq = np.asarray(anchor["ddq"], dtype=np.float64)
    metric_reference = np.asarray(anchor["metric"], dtype=np.float64)
    scalar_reference = np.asarray(anchor["scalar"], dtype=np.float64)
    norm_reference = np.asarray(anchor["dphi_norm"], dtype=np.float64)
    tidal_reference = np.asarray(anchor["tidal_components"], dtype=np.float64)
    metric_error, scalar_error, norm_error, tidal_error = [], [], [], []
    for index in range(len(q)):
        scalar, g, tidal = geometry_fd(q[index], dq[index], ddq[index], args.step)
        ginv = np.linalg.inv(g)
        norm = float(dq[index, 0] @ ginv @ dq[index, 0])
        metric_error.append(float(np.max(np.abs(g - metric_reference[index]))))
        scalar_error.append(abs(scalar - scalar_reference[index]) / (1 + abs(scalar_reference[index])))
        norm_error.append(abs(norm - norm_reference[index]) / (1 + abs(norm_reference[index])))
        tidal_error.append(float(np.max(np.abs(tidal - tidal_reference[index]) / (1 + np.abs(tidal_reference[index])))))
    maxima = {
        "metric_absolute": max(metric_error),
        "scalar_scaled": max(scalar_error),
        "dphi_norm_scaled": max(norm_error),
        "tidal_components_scaled": max(tidal_error),
    }
    tolerances = {
        "metric_absolute": 5e-12,
        "scalar_scaled": 2e-4,
        "dphi_norm_scaled": 2e-8,
        "tidal_components_scaled": 2e-4,
    }
    checks = {name: bool(maxima[name] <= tolerance) for name, tolerance in tolerances.items()}
    result = {
        "schema": "udt-p02b-independent-repeated-tidal-cpu-anchor-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "production_module_imported": False,
        "method": "NUMPY_DIRECT_LOCAL_TAYLOR_METRIC_PLUS_FOURTH_ORDER_4D_FINITE_DIFFERENCE_RIEMANN",
        "anchor_sha256": hashlib.sha256(args.anchor.read_bytes()).hexdigest(),
        "anchors": len(q),
        "finite_difference_step": args.step,
        "maxima": maxima,
        "tolerances": tolerances,
        "checks": checks,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "device": "CPU",
            "dtype": "float64",
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
