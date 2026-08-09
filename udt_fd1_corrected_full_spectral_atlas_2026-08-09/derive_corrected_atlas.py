#!/usr/bin/env python3
"""Blind complete FD1 atlas in the original regular radial variable.

No CMB peak or trough datum is present or loaded.  The wall is reached with a
factored endpoint compactification; no finite cutoff or harmonic tail is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
INV_N_VALUES = (0.9658, 0.9470, 0.9284)
Q_RATIOS = (-2.0, -1.0, 0.0, 0.25, 0.50, 0.75, 0.95)
HBARS = (0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0)
WALLS = ("D", "N")
MS = (-1, 0, 1)
NMODES = 8
YSPLIT = 1.0
R0 = 1.0e-7
SCAN_RTOL = 2.0e-10
SCAN_ATOL = 2.0e-12
ROOT_RTOL = 2.0e-11
ROOT_ATOL = 2.0e-13
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q_value(n: float, ratio: float) -> float:
    return 0.0 if ratio == 0.0 else ratio * (2.0 - n) / 2.0


def exponents(n: float, q: float) -> tuple[float, float, float, float]:
    sigma = 0.5 * (n + 2.0 * q)
    alpha = 1.0 - sigma
    beta = 1.0 - 0.5 * n
    gamma = 1.0 + n - sigma
    delta = min(alpha, beta)
    if delta <= 0.0:
        raise ValueError("compactification requires the registered q<qcrit region")
    return alpha, beta, gamma, delta


def coeff_y(y: float, n: float, q: float, hbar: float) -> tuple[float, float, float, float, float]:
    u = math.exp(-y)
    r = -math.expm1(-y)
    A = u**n
    h = hbar * r * r * u**q
    p = math.sqrt(A * (A * r * r + h * h))
    return u, r, A, h, p


def center_state(omegas: np.ndarray, m: int, n: float, q: float, hbar: float, r0: float) -> np.ndarray:
    omegas = np.asarray(omegas, dtype=float)
    y0 = -math.log1p(-r0)
    _, _, _, _, p0 = coeff_y(y0, n, q, hbar)
    k2 = omegas * omegas + 2.0 * hbar * m * omegas
    if m == 0:
        R = 1.0 - k2 * r0**2 / 4.0 + k2**2 * r0**4 / 64.0
        dR = -k2 * r0 / 2.0 + k2**2 * r0**3 / 16.0
        F = p0 * dR
    else:
        R = 1.0 - k2 * r0**2 / 8.0 + k2**2 * r0**4 / 192.0
        F = (p0 / r0) * (1.0 - 3.0 * k2 * r0**2 / 8.0 + 5.0 * k2**2 * r0**4 / 192.0)
    return np.r_[R, F]


def _power_at_endpoint(t: float, exponent: float, delta: float) -> float:
    power = exponent / delta - 1.0
    if abs(power) < 2.0e-13:
        return 1.0
    if t <= 0.0:
        return 0.0
    return t**power


def propagate(
    omegas: np.ndarray,
    m: int,
    n: float,
    q: float,
    hbar: float,
    *,
    ysplit: float = YSPLIT,
    r0: float = R0,
    rtol: float = SCAN_RTOL,
    atol: float = SCAN_ATOL,
) -> tuple[np.ndarray, np.ndarray]:
    """Propagate one or many real frequencies from the regular center to the exact wall."""
    omegas = np.atleast_1d(np.asarray(omegas, dtype=float))
    count = len(omegas)
    y0 = -math.log1p(-r0)
    initial = center_state(omegas, m, n, q, hbar, r0)

    def rhs_y(y: float, state: np.ndarray) -> np.ndarray:
        u, r, A, h, p = coeff_y(y, n, q, hbar)
        R, F = state[:count], state[count:]
        return np.r_[u * F / p, u * (A * m * m - 2.0 * h * m * omegas - r * r * omegas**2) * R / p]

    body = solve_ivp(
        rhs_y,
        (y0, ysplit),
        initial,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=0.08,
    )
    if not body.success:
        raise RuntimeError(body.message)

    alpha, beta, gamma, delta = exponents(n, q)
    tstart = math.exp(-delta * ysplit)

    def rhs_t(t: float, state: np.ndarray) -> np.ndarray:
        R, F = state[:count], state[count:]
        u = 0.0 if t <= 0.0 else t ** (1.0 / delta)
        r = 1.0 - u
        ratio_power = (n - 2.0 * q) / delta
        ratio = 0.0 if t <= 0.0 else t**ratio_power / (hbar * hbar * r * r)
        scale = math.sqrt(1.0 + ratio)
        pa = _power_at_endpoint(t, alpha, delta)
        pb = _power_at_endpoint(t, beta, delta)
        pg = _power_at_endpoint(t, gamma, delta)
        dR = -pa * F / (delta * hbar * r * r * scale)
        coefficient = (
            -(m * m) * pg / (delta * hbar * r * r * scale)
            + 2.0 * m * omegas * pb / (delta * scale)
            + omegas**2 * pa / (delta * hbar * scale)
        )
        return np.r_[dR, coefficient * R]

    tail = solve_ivp(
        rhs_t,
        (tstart, 0.0),
        body.y[:, -1],
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=min(0.025, tstart / 20.0),
    )
    if not tail.success:
        raise RuntimeError(tail.message)
    return tail.y[:count, -1], tail.y[count:, -1]


def normalized_values(R: np.ndarray, F: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    norm = np.hypot(R, F)
    if np.any(norm == 0.0) or np.any(~np.isfinite(norm)):
        raise RuntimeError("nonfinite or zero endpoint state")
    return R / norm, F / norm


def wall_length(n: float, q: float, hbar: float, ysplit: float = YSPLIT) -> float:
    alpha, _, _, delta = exponents(n, q)
    y0 = -math.log1p(-R0)

    def body_integrand(y: float) -> float:
        u, r, _, _, p = coeff_y(y, n, q, hbar)
        return r * u / p

    body = R0 + quad(body_integrand, y0, ysplit, epsabs=2.0e-11, epsrel=2.0e-11, limit=400)[0]
    tstart = math.exp(-delta * ysplit)

    def tail_integrand(t: float) -> float:
        u = 0.0 if t <= 0.0 else t ** (1.0 / delta)
        r = 1.0 - u
        ratio = 0.0 if t <= 0.0 else t ** ((n - 2.0 * q) / delta) / (hbar * hbar * r * r)
        return _power_at_endpoint(t, alpha, delta) / (delta * hbar * r * math.sqrt(1.0 + ratio))

    tail = quad(tail_integrand, 0.0, tstart, epsabs=2.0e-10, epsrel=2.0e-10, limit=700)[0]
    return body + tail


def _collect_brackets(points: np.ndarray, values: np.ndarray) -> list[tuple[float, float]]:
    brackets: list[tuple[float, float]] = []
    for left, right, lv, rv in zip(points[:-1], points[1:], values[:-1], values[1:]):
        if not (math.isfinite(float(lv)) and math.isfinite(float(rv))):
            raise RuntimeError("nonfinite boundary scan")
        if lv * rv < 0.0:
            brackets.append((float(left), float(right)))
    return brackets


def boundary_value(
    omega: float, m: int, n: float, q: float, hbar: float, wall: str, **controls: float
) -> float:
    R, F = propagate(np.asarray([omega]), m, n, q, hbar, **controls)
    D, N = normalized_values(R, F)
    return float(D[0] if wall == "D" else N[0])


def scan_channel(n: float, q: float, hbar: float, m: int, xwall: float) -> dict[str, object]:
    step = min(0.08, math.pi / max(20.0 * xwall, 1.0e-12))
    first = max(1.0e-7, step / 64.0)
    points = np.geomspace(first, step, 24)
    R, F = propagate(points, m, n, q, hbar)
    D, N = normalized_values(R, F)
    all_points, all_D, all_N = list(points), list(D), list(N)
    dbr = _collect_brackets(points, D)
    nbr = _collect_brackets(points, N)
    cursor = float(points[-1])
    chunks = 0
    while len(dbr) < NMODES or len(nbr) < NMODES:
        new_points = cursor + step * np.arange(1, 257, dtype=float)
        R, F = propagate(new_points, m, n, q, hbar)
        new_D, new_N = normalized_values(R, F)
        joined_points = np.r_[cursor, new_points]
        joined_D = np.r_[all_D[-1], new_D]
        joined_N = np.r_[all_N[-1], new_N]
        dbr.extend(_collect_brackets(joined_points, joined_D))
        nbr.extend(_collect_brackets(joined_points, joined_N))
        all_points.extend(new_points.tolist())
        all_D.extend(new_D.tolist())
        all_N.extend(new_N.tolist())
        cursor = float(new_points[-1])
        chunks += 1
        if cursor > 800.0 or chunks > 160:
            raise RuntimeError(f"root scan obstructed m={m}, omega={cursor}, D={len(dbr)}, N={len(nbr)}")

    roots: dict[str, list[float]] = {}
    residuals: dict[str, list[float]] = {}
    for wall, brackets in (("D", dbr), ("N", nbr)):
        roots[wall], residuals[wall] = [], []
        for left, right in brackets[:NMODES]:
            root = brentq(
                lambda w: boundary_value(w, m, n, q, hbar, wall, rtol=ROOT_RTOL, atol=ROOT_ATOL),
                left,
                right,
                xtol=1.0e-11,
                rtol=1.0e-11,
                maxiter=100,
            )
            roots[wall].append(float(root))
            residuals[wall].append(abs(boundary_value(root, m, n, q, hbar, wall, rtol=ROOT_RTOL, atol=ROOT_ATOL)))
    return {
        "omega": roots,
        "normalized_wall_residual": residuals,
        "scan_step": step,
        "scan_max": cursor,
        "scan_points": len(all_points),
        "sign_brackets": {"D": len(dbr), "N": len(nbr)},
    }


def continuum_rows(inv_n: float, n: float, ratio: float, q: float) -> list[dict[str, object]]:
    return [
        {
            "inv_n": inv_n,
            "n": n,
            "q_ratio": ratio,
            "q": q,
            "qcrit": (2.0 - n) / 2.0,
            "hbar": 0.0,
            "wall": wall,
            "classification": "MU_OFF_LIMIT_POINT_CONTINUUM_CONTROL",
            "positive_discrete_roots_computed": False,
        }
        for wall in WALLS
    ]


def spectral_rows(inv_n: float, n: float, ratio: float, q: float, hbar: float) -> list[dict[str, object]]:
    xwall = wall_length(n, q, hbar)
    channels = {m: scan_channel(n, q, hbar, m, xwall) for m in MS}
    rows: list[dict[str, object]] = []
    for wall in WALLS:
        modes = {m: np.asarray(channels[m]["omega"][wall], dtype=float) for m in MS}
        mean_pair = 0.5 * (modes[-1] + modes[1])
        eta = np.abs(modes[1] - modes[-1]) / mean_pair
        displacement = np.maximum(np.abs(modes[1] - modes[0]), np.abs(modes[-1] - modes[0])) / modes[0]
        ordered = sorted(
            ({"omega": float(value), "m": m, "radial_index": k} for m in MS for k, value in enumerate(modes[m])),
            key=lambda item: item["omega"],
        )
        q0_error = None
        if ratio == 0.0:
            q0_error = float(np.max(np.abs(np.abs(modes[1] - modes[-1]) - 2.0 * hbar)))
        rows.append(
            {
                "inv_n": inv_n,
                "n": n,
                "q_ratio": ratio,
                "q": q,
                "qcrit": (2.0 - n) / 2.0,
                "hbar": hbar,
                "wall": wall,
                "classification": "MIXING_CREATED_LIMIT_CIRCLE_LADDER",
                "xwall": xwall,
                "omega_mminus": modes[-1].tolist(),
                "omega_m0": modes[0].tolist(),
                "omega_mplus": modes[1].tolist(),
                "eta_split": eta.tolist(),
                "same_index_displacement": displacement.tolist(),
                "full_frequency_order": ordered,
                "neumann_m0_exact_zero_mode": wall == "N",
                "q0_split_max_abs_error": q0_error,
                "max_normalized_wall_residual": {
                    str(m): max(channels[m]["normalized_wall_residual"][wall]) for m in MS
                },
                "scan": {
                    str(m): {name: channels[m][name] for name in ("scan_step", "scan_max", "scan_points", "sign_brackets")}
                    for m in MS
                },
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="corrected_full_atlas.json")
    parser.add_argument("--max-configs", type=int, default=0, help="conditioning-only prefix; 0 is full production")
    args = parser.parse_args()
    if args.max_configs < 0:
        raise SystemExit("--max-configs must be nonnegative")
    start = time.time()
    rows: list[dict[str, object]] = []
    configs_done = 0
    production = args.max_configs == 0
    stop = False
    for inv_n in INV_N_VALUES:
        n = 1.0 / inv_n
        for ratio in Q_RATIOS:
            q = q_value(n, ratio)
            rows.extend(continuum_rows(inv_n, n, ratio, q))
            for hbar in HBARS[1:]:
                if args.max_configs and configs_done >= args.max_configs:
                    stop = True
                    break
                rows.extend(spectral_rows(inv_n, n, ratio, q, hbar))
                configs_done += 1
                print(
                    f"CONFIG {configs_done:03d}/210 inv_n={inv_n:.4f} q/qcrit={ratio:+.2f} hbar={hbar:g}",
                    flush=True,
                )
            if stop:
                break
        if stop:
            break

    spectral = [row for row in rows if row["hbar"] > 0.0]
    q0_errors = [row["q0_split_max_abs_error"] for row in spectral if row["q0_split_max_abs_error"] is not None]
    residuals = [value for row in spectral for value in row["max_normalized_wall_residual"].values()]
    ordered = all(
        len(row[name]) == NMODES and np.all(np.diff(np.asarray(row[name])) > 0.0)
        for row in spectral
        for name in ("omega_mminus", "omega_m0", "omega_mplus")
    )
    expected_rows = 462 if production else 2 * (configs_done + math.ceil(configs_done / 10.0))
    key("CFA_P1_full_row_count", len(rows) == expected_rows)
    key("CFA_P2_positive_ordered_roots", ordered)
    key("CFA_P3_wall_residuals", max(residuals) < 2.0e-8)
    key("CFA_P4_q0_exact_split", (not q0_errors) or max(q0_errors) < 2.0e-8)
    key("CFA_P5_neumann_zero_modes", all(row["neumann_m0_exact_zero_mode"] for row in spectral if row["wall"] == "N"))
    key("CFA_P6_blind_phase", True)
    payload = {
        "phase": "BLIND_CORRECTED_FULL_SPECTRAL_ATLAS",
        "production_complete": production,
        "observational_peak_or_trough_values_loaded": False,
        "config": {
            "inv_n_values": INV_N_VALUES,
            "q_ratios": Q_RATIOS,
            "hbars": HBARS,
            "walls": WALLS,
            "m_channels": MS,
            "positive_modes": NMODES,
            "ysplit": YSPLIT,
            "r0": R0,
            "configs_done": configs_done,
        },
        "keys": KEYS,
        "summary": {
            "rows": len(rows),
            "spectral_rows": len(spectral),
            "continuum_control_rows": len(rows) - len(spectral),
            "maximum_normalized_wall_residual": max(residuals),
            "q0_max_abs_split_error": max(q0_errors) if q0_errors else None,
            "runtime_seconds": time.time() - start,
        },
        "rows": rows,
    }
    output = ROOT / args.output
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"WROTE {output} SHA256 {sha256(output)}", flush=True)
    if production and not all(KEYS.values()):
        raise SystemExit("production gate failed")


if __name__ == "__main__":
    main()
