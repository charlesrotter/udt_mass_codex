#!/usr/bin/env python3
"""Independent finite-ray verification of the G128 Jacobi endpoints.

This implementation does not import the production module, its symbolic
connection, its curvature, or its Jacobi equation.  It constructs the metric
and first derivatives directly, propagates central and neighboring nonlinear
geodesics, parallel-transports the screen, and reconstructs the endpoint
Jacobi map by a five-point angular finite difference.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
LAM_END = 0.8
STEP = 1.5e-4
CASES = (
    ("H0_flat", 0.0),
    ("H0_flat", math.pi / 4),
    ("H1_static_reciprocal", 0.0),
    ("H1_static_reciprocal", math.pi / 4),
    ("H2_timelive_reciprocal", 0.0),
    ("H2_timelive_reciprocal", math.pi / 4),
    ("H3_timelive_full_spherical_base", 0.0),
    ("H3_timelive_full_spherical_base", math.pi / 4),
)


def fields(history: str, t: float, r: float):
    """Return kappa, phi, beta and their T/R derivatives."""
    if history == "H0_flat":
        return (0.0,) * 9

    q = (1.0 + 0.4 * math.sin(t)) / 4.0
    qt = 0.1 * math.cos(t)
    denom = 1.0 + q * r * r
    phi = 0.5 * math.log(denom)
    phi_t = 0.5 * qt * r * r / denom
    phi_r = q * r / denom

    if history == "H1_static_reciprocal":
        phi = 0.5 * math.log(1.0 + r * r / 4.0)
        phi_t = 0.0
        phi_r = r / (4.0 + r * r)
        return 0.0, phi, 0.0, 0.0, 0.0, phi_t, phi_r, 0.0, 0.0
    if history == "H2_timelive_reciprocal":
        return 0.0, phi, 0.0, 0.0, 0.0, phi_t, phi_r, 0.0, 0.0
    if history != "H3_timelive_full_spherical_base":
        raise KeyError(history)

    kap = r * r * math.cos(t / 2.0) / (20.0 * (1.0 + r * r))
    kap_t = -r * r * math.sin(t / 2.0) / (40.0 * (1.0 + r * r))
    kap_r = r * math.cos(t / 2.0) / (10.0 * (1.0 + r * r) ** 2)
    common = 1.0 + math.sin(t / 2.0)
    beta = r * math.exp(-r * r) * common / 12.0
    beta_t = r * math.exp(-r * r) * math.cos(t / 2.0) / 24.0
    beta_r = math.exp(-r * r) * (1.0 - 2.0 * r * r) * common / 12.0
    return kap, phi, beta, kap_t, kap_r, phi_t, phi_r, beta_t, beta_r


def metric_and_derivatives(history: str, x: np.ndarray):
    t, r, theta, _psi = x
    kap, phi, beta, kt, kr, pt, pr, bt, br = fields(history, t, r)
    n = math.exp(kap - phi)
    ell = math.exp(kap + phi)
    g = np.zeros((4, 4))
    g[0, 0] = -n * n + ell * ell * beta * beta
    g[0, 1] = g[1, 0] = ell * ell * beta
    g[1, 1] = ell * ell
    g[2, 2] = r * r
    g[3, 3] = r * r * math.sin(theta) ** 2

    dg = np.zeros((4, 4, 4))
    for mu, nd, ld, bd in (
        (0, n * (kt - pt), ell * (kt + pt), bt),
        (1, n * (kr - pr), ell * (kr + pr), br),
    ):
        dg[mu, 0, 0] = -2.0 * n * nd + 2.0 * ell * ld * beta**2 + 2.0 * ell**2 * beta * bd
        dg[mu, 0, 1] = dg[mu, 1, 0] = 2.0 * ell * ld * beta + ell**2 * bd
        dg[mu, 1, 1] = 2.0 * ell * ld
    dg[1, 2, 2] = 2.0 * r
    dg[1, 3, 3] = 2.0 * r * math.sin(theta) ** 2
    dg[2, 3, 3] = 2.0 * r * r * math.sin(theta) * math.cos(theta)
    return g, dg


def connection(history: str, x: np.ndarray):
    g, dg = metric_and_derivatives(history, x)
    gi = np.linalg.inv(g)
    gamma = np.zeros((4, 4, 4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                gamma[a, b, c] = 0.5 * sum(
                    gi[a, d] * (dg[b, d, c] + dg[c, d, b] - dg[d, b, c])
                    for d in range(4)
                )
    return gamma


def initial_frame(history: str, alpha: float):
    x = np.array([0.0, 0.4, math.pi / 2.0, 0.0])
    kap, phi, beta, *_ = fields(history, x[0], x[1])
    n = math.exp(kap - phi)
    ell = math.exp(kap + phi)
    e0 = np.array([1.0 / n, -beta / n, 0.0, 0.0])
    e1 = np.array([0.0, 1.0 / ell, 0.0, 0.0])
    e2 = np.array([0.0, 0.0, 1.0 / x[1], 0.0])
    e3 = np.array([0.0, 0.0, 0.0, 1.0 / x[1]])
    v = math.cos(alpha) * e1 + math.sin(alpha) * e2
    s1 = -math.sin(alpha) * e1 + math.cos(alpha) * e2
    return x, e0, v, s1, e3


def rhs(history: str, with_screen: bool):
    def evaluate(_lam, y):
        x, k = y[:4], y[4:8]
        gamma = connection(history, x)
        pieces = [k, -np.einsum("abc,b,c->a", gamma, k, k)]
        if with_screen:
            screen = y[8:16].reshape(2, 4)
            pieces.append(-np.einsum("abc,b,Ac->Aa", gamma, k, screen).ravel())
        return np.concatenate(pieces)

    return evaluate


def integrate(history: str, alpha: float, axis=None, delta=0.0, with_screen=False):
    x, e0, v, s1, s2 = initial_frame(history, alpha)
    direction = v if axis is None else math.cos(delta) * v + math.sin(delta) * (s1, s2)[axis]
    values = [x, e0 + direction]
    if with_screen:
        values.append(np.vstack((s1, s2)).ravel())
    sol = solve_ivp(
        rhs(history, with_screen),
        (0.0, LAM_END),
        np.concatenate(values),
        method="DOP853",
        rtol=5e-12,
        atol=5e-14,
        max_step=0.004,
    )
    if not sol.success:
        raise RuntimeError(f"independent ray failed: {history} {alpha} {axis} {delta}")
    return sol.y[:, -1]


def reconstructed_endpoint(history: str, alpha: float):
    central = integrate(history, alpha, with_screen=True)
    endpoint = central[:4]
    screens = central[8:16].reshape(2, 4)
    g, _ = metric_and_derivatives(history, endpoint)
    dmap = np.zeros((2, 2))
    for axis in range(2):
        points = {
            m: integrate(history, alpha, axis=axis, delta=m * STEP)[:4]
            for m in (-2, -1, 1, 2)
        }
        jac = (-points[2] + 8.0 * points[1] - 8.0 * points[-1] + points[-2]) / (12.0 * STEP)
        dmap[:, axis] = screens @ g @ jac
    null = abs(central[4:8] @ g @ central[4:8])
    orth = np.max(np.abs(screens @ g @ screens.T - np.eye(2)))
    ray_orth = np.max(np.abs(screens @ g @ central[4:8]))
    return dmap, central[:8], float(max(null, orth, ray_orth))


def main():
    banked = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    samples = np.load(HERE / "FINITE_PATH_SAMPLES.npz")
    cases = []
    max_dmap = 0.0
    max_phase = 0.0
    max_geometry_drift = 0.0
    for history, alpha in CASES:
        key = f"{history}__alpha_{alpha:.12f}"
        dmap, phase, drift = reconstructed_endpoint(history, alpha)
        reference = np.asarray(banked["branches"][key]["D_endpoint"], dtype=float)
        production_phase = samples[f"{key}__state"][:8, -1]
        dmap_error = float(np.max(np.abs(dmap - reference)))
        phase_error = float(np.max(np.abs(phase - production_phase)))
        max_dmap = max(max_dmap, dmap_error)
        max_phase = max(max_phase, phase_error)
        max_geometry_drift = max(max_geometry_drift, drift)
        cases.append(
            {
                "history": history,
                "alpha": alpha,
                "independent_D_endpoint": dmap.tolist(),
                "production_D_endpoint": reference.tolist(),
                "D_max_abs_error": dmap_error,
                "phase_max_abs_error": phase_error,
                "null_screen_drift": drift,
            }
        )

    flat = [c for c in cases if c["history"] == "H0_flat"]
    radial = [c for c in cases if c["alpha"] == 0.0]
    tilted = [c for c in cases if c["history"] != "H0_flat" and c["alpha"] != 0.0]
    checks = {
        "all_eight_cases_replayed": len(cases) == 8,
        "independent_D_agreement": max_dmap < 2e-7,
        "independent_phase_agreement": max_phase < 2e-9,
        "independent_null_screen_geometry": max_geometry_drift < 2e-9,
        "flat_endpoint_is_lambda_identity": all(
            np.max(np.abs(np.asarray(c["independent_D_endpoint"]) - 0.8 * np.eye(2))) < 2e-8
            for c in flat
        ),
        "radial_endpoint_isotropic": all(
            abs(np.linalg.svd(np.asarray(c["independent_D_endpoint"]), compute_uv=False)[0]
                - np.linalg.svd(np.asarray(c["independent_D_endpoint"]), compute_uv=False)[1]) < 2e-8
            for c in radial
        ),
        "all_nonflat_tilted_endpoints_anisotropic": all(
            abs(np.linalg.svd(np.asarray(c["independent_D_endpoint"]), compute_uv=False)[0]
                - np.linalg.svd(np.asarray(c["independent_D_endpoint"]), compute_uv=False)[1]) > 1e-7
            for c in tilted
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "method": "independent direct metric-derivative connection plus five-point nonlinear neighboring rays",
        "checks": checks,
        "maxima": {
            "D_max_abs_error": max_dmap,
            "phase_max_abs_error": max_phase,
            "null_screen_drift": max_geometry_drift,
        },
        "cases": cases,
        "maximum_conclusion": "independent verification of eight declared G128 controls only",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({k: result[k] for k in ("status", "checks", "maxima")}, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
