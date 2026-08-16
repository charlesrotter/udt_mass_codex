#!/usr/bin/env python3
"""Implementation-independent numerical verification for G115.

This route integrates the null graph and affine geodesic from the metric components and numerical
metric derivatives. It does not import the production script or its generated JSON.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent

# FREE verification witness. These numbers test algebra; they are not physics inputs.
N0 = 0.17
NT = -0.11
ELL0 = -0.08
ELLT = 0.07
B0 = 0.23
BT = -0.19
BTT = 0.13
Q0 = -0.12
QT = 0.09
WX = 0.14
WY = -0.21

COEFF_RTOL = 1.0e-3
NULL_ATOL = 3.0e-10
SYMPLECTIC_ATOL = 2.0e-12


def fields(t: float, r: float) -> tuple[float, float, float]:
    n = N0 + NT * t
    ell = ELL0 + ELLT * t
    b = B0 + BT * t + 0.5 * BTT * t * t
    return 1.0 + n * r * r, 1.0 + ell * r * r, b * r


def metric(t: float, r: float) -> np.ndarray:
    lapse, radial, shift = fields(t, r)
    return np.array(
        [
            [-lapse * lapse + radial * radial * shift * shift, radial * radial * shift],
            [radial * radial * shift, radial * radial],
        ],
        dtype=float,
    )


def metric_derivative(t: float, r: float, axis: int) -> np.ndarray:
    # Numerical derivatives deliberately avoid the production Christoffel expressions.
    h = 2.0e-6
    if axis == 0:
        return (metric(t + h, r) - metric(t - h, r)) / (2.0 * h)
    return (metric(t, r + h) - metric(t, r - h)) / (2.0 * h)


def christoffel(t: float, r: float) -> np.ndarray:
    g = metric(t, r)
    gi = np.linalg.inv(g)
    dg = np.stack((metric_derivative(t, r, 0), metric_derivative(t, r, 1)))
    out = np.zeros((2, 2, 2), dtype=float)
    for a in range(2):
        for m in range(2):
            for n in range(2):
                for d in range(2):
                    out[a, m, n] += 0.5 * gi[a, d] * (
                        dg[m, d, n] + dg[n, d, m] - dg[d, m, n]
                    )
    return out


def rk4_step(fun, x: float, y: np.ndarray, h: float) -> np.ndarray:
    k1 = fun(x, y)
    k2 = fun(x + 0.5 * h, y + 0.5 * h * k1)
    k3 = fun(x + 0.5 * h, y + 0.5 * h * k2)
    k4 = fun(x + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def null_slope(t: float, r: float) -> float:
    lapse, radial, shift = fields(t, r)
    return radial / (lapse - radial * shift)


def integrate_null_graph(t0: float, r_end: float, steps: int = 1200) -> float:
    h = r_end / steps
    t = float(t0)
    r = 0.0
    for _ in range(steps):
        def f(rr: float, yy: np.ndarray) -> np.ndarray:
            return np.array([null_slope(float(yy[0]), rr)])

        t = float(rk4_step(f, r, np.array([t]), h)[0])
        r += h
    return t


def geodesic_rhs(_lam: float, y: np.ndarray) -> np.ndarray:
    t, r, kt, kr = (float(v) for v in y)
    gamma = christoffel(t, r)
    k = np.array([kt, kr])
    acc = np.zeros(2)
    for a in range(2):
        acc[a] = -sum(gamma[a, m, n] * k[m] * k[n] for m in range(2) for n in range(2))
    return np.array([kt, kr, acc[0], acc[1]])


def integrate_geodesic(lam_end: float, step: float = 1.0e-5) -> np.ndarray:
    steps = int(round(lam_end / step))
    h = lam_end / steps
    y = np.array([0.0, 0.0, 1.0, 1.0])
    x = 0.0
    for _ in range(steps):
        y = rk4_step(geodesic_rhs, x, y, h)
        x += h
    return y


def measured_log_frequency(t: float, r: float, kt: float) -> float:
    lapse, _radial, _shift = fields(t, r)
    omega_euler = lapse * kt
    q = Q0 + QT * t
    v = q * r
    return math.log(omega_euler) + 0.5 * math.log((1.0 - v) / (1.0 + v))


def fit_coefficients(x: np.ndarray, y: np.ndarray, powers: tuple[int, ...]) -> np.ndarray:
    design = np.column_stack([x**p for p in powers])
    return np.linalg.lstsq(design, y, rcond=None)[0]


def intersection_dimension(a: np.ndarray, b: np.ndarray, tol: float = 1.0e-10) -> int:
    ra = np.linalg.matrix_rank(a, tol)
    rb = np.linalg.matrix_rank(b, tol)
    rab = np.linalg.matrix_rank(np.column_stack((a, b)), tol)
    return int(ra + rb - rab)


def main() -> None:
    radii = np.array([0.006, 0.009, 0.012, 0.015, 0.018, 0.021])
    dtau = 2.0e-6
    t_path = []
    phi = []
    logfreq = []
    null_residuals = []

    for r in radii:
        t0 = integrate_null_graph(0.0, float(r))
        tp = integrate_null_graph(dtau, float(r))
        tm = integrate_null_graph(-dtau, float(r))
        t_tau = (tp - tm) / (2.0 * dtau)
        tr = null_slope(t0, float(r))
        g = metric(t0, float(r))
        h00 = g[0, 0] * t_tau * t_tau + r * r * (WX * WX + WY * WY)
        h01 = t_tau * (g[0, 0] * tr + g[0, 1])
        h11 = g[0, 0] * tr * tr + 2.0 * g[0, 1] * tr + g[1, 1]
        t_path.append(t0)
        phi.append(0.5 * (math.log(-h01) - math.log(-h00)))
        null_residuals.append(abs(h11))

    lambdas = radii.copy()
    geo = np.vstack([integrate_geodesic(float(x)) for x in lambdas])
    for t, r, kt, _kr in geo:
        logfreq.append(measured_log_frequency(t, r, kt))

    t_coeff = fit_coefficients(radii, np.asarray(t_path) - radii, (2, 3, 4, 5))
    phi_coeff = fit_coefficients(radii, np.asarray(phi), (2, 3, 4))[0]
    rlam_coeff = fit_coefficients(lambdas, geo[:, 1] - lambdas, (3, 4, 5))[0]
    kr_coeff = fit_coefficients(geo[:, 1], geo[:, 3] - 1.0, (2, 3, 4))[0]
    freq_coeff = fit_coefficients(geo[:, 1], np.asarray(logfreq), (1, 2, 3))

    optical_a = 2.0 * ELL0 + 2.0 * N0 + BT
    expected = {
        "T_R2": B0 / 2.0,
        "T_R3": (B0 * B0 + ELL0 - N0 + BT) / 3.0,
        "phi_R2": 0.5
        * (ELL0 - N0 + B0 * B0 - BT / 2.0 + WX * WX + WY * WY),
        "R_lambda3": -optical_a / 6.0,
        "KR_R2": -optical_a / 2.0,
        "logfreq_R1": B0 - Q0,
        "logfreq_R2": B0 * B0 / 2.0 - N0 + BT / 2.0 - QT,
    }
    observed = {
        "T_R2": float(t_coeff[0]),
        "T_R3": float(t_coeff[1]),
        "phi_R2": float(phi_coeff),
        "R_lambda3": float(rlam_coeff),
        "KR_R2": float(kr_coeff),
        "logfreq_R1": float(freq_coeff[0]),
        "logfreq_R2": float(freq_coeff[1]),
    }
    relative = {
        key: abs(observed[key] - expected[key]) / max(1.0e-12, abs(expected[key]))
        for key in expected
    }

    # Exact finite-dimensional rank controls, implemented from subspace column ranks.
    eye = np.eye(2)
    vertical = np.vstack((np.zeros((2, 2)), eye))
    qobs = 1.7
    observer = np.vstack((eye, qobs * eye))
    graph_equal = np.vstack((eye, qobs * eye))
    graph_one = np.vstack((eye, np.diag([qobs, -0.4])))
    graph_none = np.vstack((eye, np.diag([0.2, -0.4])))
    rotation = np.array([[0.6, -0.8], [0.8, 0.6]])
    lift = np.block([[rotation, np.zeros((2, 2))], [np.zeros((2, 2)), rotation]])
    ranks = {
        "point_noncaustic": intersection_dimension(observer, vertical),
        "point_vertical_caustic": intersection_dimension(vertical, vertical),
        "graph_rank_2": intersection_dimension(observer, graph_equal),
        "graph_rank_1": intersection_dimension(observer, graph_one),
        "graph_rank_0": intersection_dimension(observer, graph_none),
        "rotation_invariance": intersection_dimension(lift @ observer, lift @ graph_one),
    }

    # Exact oscillator caustic confirms that a singular position block need not lose phase.
    phase_caustic = -np.eye(4)
    omega = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]])
    symplectic_defect = float(np.max(np.abs(phase_caustic.T @ omega @ phase_caustic - omega)))

    checks = {
        "coefficient_convergence": bool(max(relative.values()) < COEFF_RTOL),
        "null_pullback": bool(max(null_residuals) < NULL_ATOL),
        "rank_controls": ranks
        == {
            "point_noncaustic": 0,
            "point_vertical_caustic": 2,
            "graph_rank_2": 2,
            "graph_rank_1": 1,
            "graph_rank_0": 0,
            "rotation_invariance": 1,
        },
        "caustic_phase_symplectic": bool(symplectic_defect < SYMPLECTIC_ATOL),
        "caustic_phase_invertible": bool(
            abs(np.linalg.det(phase_caustic) - 1.0) < SYMPLECTIC_ATOL
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "method": "RK4 metric geodesic plus separate null-graph integration and matrix-rank controls",
        "witness": {
            "n": N0,
            "n_T": NT,
            "ell": ELL0,
            "ell_T": ELLT,
            "b": B0,
            "b_T": BT,
            "b_TT": BTT,
            "q": Q0,
            "q_T": QT,
            "w": [WX, WY],
        },
        "expected_coefficients": expected,
        "observed_coefficients": observed,
        "relative_errors": relative,
        "max_relative_error": max(relative.values()),
        "max_null_pullback_residual": max(null_residuals),
        "intersection_ranks": ranks,
        "caustic_symplectic_defect": symplectic_defect,
        "checks": checks,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
