#!/usr/bin/env python3
"""Implementation-distinct direct-metric verification of G340."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


LANDING = (
    "METRIC_NULL_GEOMETRY_CLOSES_A_PATH_LABELLED_FINITE_NORMAL_PAIR_FAMILY"
    "__NO_PHENOMENOLOGICAL_LIGHT_MODEL_REQUIRED"
    "__SLICE_DISTANCE_NULL_EXCHANGE_RADAR_AND_PROJECTIVE_READOUT_ARE_RELATED_NOT_IDENTICAL"
    "__COMPACT_WINDINGS_REMAIN_DISTINCT_BRANCHES"
    "__NO_PHYSICAL_PROTOCOL_POPULATION_SCALE_OR_XMAX_SELECTED"
)
TOL = 2.0e-10

# Eight-point Gauss--Legendre rule, independent of the production Simpson route.
GL_X = (
    -0.9602898564975363,
    -0.7966664774136267,
    -0.5255324099163290,
    -0.1834346424956498,
    0.1834346424956498,
    0.5255324099163290,
    0.7966664774136267,
    0.9602898564975363,
)
GL_W = (
    0.1012285362903763,
    0.2223810344533745,
    0.3137066458778873,
    0.3626837833783620,
    0.3626837833783620,
    0.3137066458778873,
    0.2223810344533745,
    0.1012285362903763,
)


def metric(t: float, cx: float, cp: float) -> tuple[float, float, float, float]:
    return (-1.0, cx * cx * t ** (-2.0 / 3.0), cp * cp * t ** (4.0 / 3.0), cp * cp * t ** (4.0 / 3.0))


def inverse_metric(t: float, cx: float, cp: float) -> tuple[float, float, float, float]:
    g = metric(t, cx, cp)
    return tuple(1.0 / value for value in g)


def future_null_tangent(
    t: float, covector: tuple[float, float, float], cx: float, cp: float
) -> tuple[float, float, float, float]:
    inv = inverse_metric(t, cx, cp)
    spatial_sq = sum(inv[i + 1] * covector[i] * covector[i] for i in range(3))
    kt = math.sqrt(spatial_sq)
    return (kt, inv[1] * covector[0], inv[2] * covector[1], inv[3] * covector[2])


def coordinate_velocity(
    t: float, covector: tuple[float, float, float], cx: float, cp: float
) -> tuple[float, float, float]:
    k = future_null_tangent(t, covector, cx, cp)
    return (k[1] / k[0], k[2] / k[0], k[3] / k[0])


def gauss_integral(f, a: float, b: float, panels: int = 24) -> float:
    width = (b - a) / panels
    total = 0.0
    for panel in range(panels):
        left = a + panel * width
        right = left + width
        mid = 0.5 * (left + right)
        half = 0.5 * width
        total += half * sum(w * f(mid + half * x) for x, w in zip(GL_X, GL_W))
    return total


def displacement(
    te: float,
    tr: float,
    covector: tuple[float, float, float],
    cx: float,
    cp: float,
    component: int,
) -> float:
    return gauss_integral(lambda t: coordinate_velocity(t, covector, cx, cp)[component], te, tr)


def solve_arrival(
    axis: int, te: float, q: float, cx: float, cp: float
) -> float:
    covector = ((1.0, 0.0, 0.0) if axis == 0 else (0.0, 1.0, 0.0))
    low = te
    high = te * 1.2 + 0.1
    while abs(displacement(te, high, covector, cx, cp, axis)) < q:
        high = 2.0 * high + 0.1
    for _ in range(70):
        mid = 0.5 * (low + high)
        if abs(displacement(te, mid, covector, cx, cp, axis)) < q:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def solve_emission(
    axis: int, tb: float, q: float, cx: float, cp: float
) -> float:
    covector = ((1.0, 0.0, 0.0) if axis == 0 else (0.0, 1.0, 0.0))
    low = max(1.0e-10, tb * 1.0e-8)
    high = tb
    if abs(displacement(low, tb, covector, cx, cp, axis)) < q:
        raise ValueError("requested past route reaches the T=0 boundary")
    for _ in range(70):
        mid = 0.5 * (low + high)
        if abs(displacement(mid, tb, covector, cx, cp, axis)) > q:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def main() -> None:
    checks: dict[str, bool] = {}

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(340991)
    principal_cases = 0
    for axis in (0, 1):
        for _ in range(180):
            cx = rng.uniform(0.45, 2.4)
            cp = rng.uniform(0.45, 2.4)
            te = rng.uniform(0.3, 3.0)
            q = rng.uniform(0.01, 1.2)
            tr = solve_arrival(axis, te, q, cx, cp)
            expected = (
                (te ** (4.0 / 3.0) + 4.0 * cx * q / 3.0) ** (3.0 / 4.0)
                if axis == 0
                else (te ** (1.0 / 3.0) + cp * q / 3.0) ** 3
            )
            record(f"direct_arrival_{principal_cases}", close(tr, expected, 3.0e-11))
            covector = ((rng.uniform(0.2, 3.0), 0.0, 0.0) if axis == 0 else (0.0, rng.uniform(0.2, 3.0), 0.0))
            ke = future_null_tangent(te, covector, cx, cp)
            kr = future_null_tangent(tr, covector, cx, cp)
            ratio = ke[0] / kr[0]
            expected_ratio = ((te / tr) ** (1.0 / 3.0) if axis == 0 else (tr / te) ** (2.0 / 3.0))
            record(f"direct_frequency_{principal_cases}", close(ratio, expected_ratio))
            delta = -math.log(ratio)
            record(f"direct_projective_{principal_cases}", close(math.tanh(delta), (1.0 - ratio * ratio) / (1.0 + ratio * ratio)))
            g = metric(te, cx, cp)
            record(f"direct_null_{principal_cases}", abs(sum(g[i] * ke[i] * ke[i] for i in range(4))) <= TOL * max(1.0, ke[0] ** 2))
            principal_cases += 1

    radar_cases = 0
    for axis in (0, 1):
        for _ in range(90):
            cx = rng.uniform(0.6, 1.9)
            cp = rng.uniform(0.6, 1.9)
            tb = rng.uniform(0.8, 3.2)
            max_q = (0.35 * 3.0 * tb ** (4.0 / 3.0) / (4.0 * cx) if axis == 0 else 0.35 * 3.0 * tb ** (1.0 / 3.0) / cp)
            q = rng.uniform(0.02, max_q)
            tm = solve_emission(axis, tb, q, cx, cp)
            tp = solve_arrival(axis, tb, q, cx, cp)
            record(f"direct_radar_order_{radar_cases}", 0.0 < tm < tb < tp)
            if axis == 0:
                lhs = tb ** (4.0 / 3.0)
                rhs = 0.5 * (tm ** (4.0 / 3.0) + tp ** (4.0 / 3.0))
                derivative_terms = (tb / tm) ** (1.0 / 3.0) + (tb / tp) ** (1.0 / 3.0)
            else:
                lhs = tb ** (1.0 / 3.0)
                rhs = 0.5 * (tm ** (1.0 / 3.0) + tp ** (1.0 / 3.0))
                derivative_terms = (tm / tb) ** (2.0 / 3.0) + (tp / tb) ** (2.0 / 3.0)
            record(f"direct_radar_power_midpoint_{radar_cases}", close(lhs, rhs, 4.0e-11))
            eps = tb * 2.0e-6
            tm_lo = solve_emission(axis, tb - eps, q, cx, cp)
            tp_lo = solve_arrival(axis, tb - eps, q, cx, cp)
            tm_hi = solve_emission(axis, tb + eps, q, cx, cp)
            tp_hi = solve_arrival(axis, tb + eps, q, cx, cp)
            d_mid = ((tm_hi + tp_hi) - (tm_lo + tp_lo)) / (4.0 * eps)
            record(f"direct_radar_rate_{radar_cases}", close(1.0 / d_mid, 2.0 / derivative_terms, 3.0e-9))
            radar_cases += 1

    general_cases = 0
    for _ in range(1000):
        t = rng.uniform(0.2, 4.0)
        cx = rng.uniform(0.3, 3.0)
        cp = rng.uniform(0.3, 3.0)
        p = tuple(rng.uniform(-3.0, 3.0) for _ in range(3))
        if sum(value * value for value in p) < 0.02:
            p = (p[0] + 0.5, p[1], p[2])
        k = future_null_tangent(t, p, cx, cp)
        g = metric(t, cx, cp)
        residual = sum(g[i] * k[i] * k[i] for i in range(4))
        record(f"general_direct_null_{general_cases}", abs(residual) <= TOL * max(1.0, k[0] ** 2))
        record(f"future_orientation_{general_cases}", k[0] > 0.0)
        recovered_p = tuple(g[i + 1] * k[i + 1] for i in range(3))
        record(f"spatial_covector_reconstruction_{general_cases}", all(close(a, b) for a, b in zip(p, recovered_p)))
        factor = rng.uniform(0.1, 5.0)
        v1 = coordinate_velocity(t, p, cx, cp)
        v2 = coordinate_velocity(t, tuple(factor * value for value in p), cx, cp)
        record(f"affine_scale_independence_{general_cases}", all(close(a, b) for a, b in zip(v1, v2)))
        general_cases += 1

    winding_cases = 0
    for axis in (0, 1):
        for delta in (0.09, 0.31, 0.5):
            branches = [(n, abs(delta + n)) for n in range(-5, 6)]
            arrivals = [(n, solve_arrival(axis, 1.0, q, 1.1, 0.9)) for n, q in branches]
            minimum_q = min(q for _, q in branches)
            minimum_t = min(t for _, t in arrivals)
            record(f"direct_winding_order_{winding_cases}", all((close(t, minimum_t, 5.0e-11)) == close(q, minimum_q) for (_, q), (_, t) in zip(branches, arrivals)))
            if delta == 0.5:
                record(f"direct_cut_tie_{winding_cases}", sum(close(q, minimum_q) for _, q in branches) == 2)
            winding_cases += 1

    all_passed = all(checks.values())
    result = {
        "all_passed": all_passed,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "grade": "IMPLEMENTATION_DISTINCT_DIRECT_METRIC_VERIFICATION",
        "landing": LANDING,
        "method": "direct four-metric Hamiltonian reconstruction plus Gauss-Legendre quadrature and bisection; no production import or result read",
        "random_seed": 340991,
        "coverage": {
            "principal_cases": principal_cases,
            "radar_cases": radar_cases,
            "general_metric_cases": general_cases,
            "winding_cases": winding_cases,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
