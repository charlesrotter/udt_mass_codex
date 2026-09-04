#!/usr/bin/env python3
"""Implementation-distinct metric/curvature and RK verification for G342."""

from __future__ import annotations

import json
import math
import os
import random


TOL = 5.0e-9


def close(left: float, right: float, tol: float = TOL) -> bool:
    return abs(left - right) <= tol * max(1.0, abs(left), abs(right))


def zeros(*shape: int):
    if len(shape) == 1:
        return [0.0 for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def metric_jets(t: float, cx: float, cp: float):
    g = zeros(4, 4)
    dg = zeros(4, 4, 4)
    ddg = zeros(4, 4, 4, 4)
    g[0][0] = -1.0
    g[1][1] = cx * cx * t ** (-2.0 / 3.0)
    g[2][2] = cp * cp * t ** (4.0 / 3.0)
    g[3][3] = g[2][2]
    for index, power in ((1, -2.0 / 3.0), (2, 4.0 / 3.0), (3, 4.0 / 3.0)):
        dg[0][index][index] = power * g[index][index] / t
        ddg[0][0][index][index] = power * (power - 1.0) * g[index][index] / (t * t)
    inverse = zeros(4, 4)
    for index in range(4):
        inverse[index][index] = 1.0 / g[index][index]
    dinverse = zeros(4, 4, 4)
    for derivative in range(4):
        for a in range(4):
            for d in range(4):
                dinverse[derivative][a][d] = -sum(
                    inverse[a][m] * dg[derivative][m][n] * inverse[n][d]
                    for m in range(4) for n in range(4)
                )
    return g, inverse, dinverse, dg, ddg


def curvature(t: float, cx: float, cp: float):
    g, inverse, dinverse, dg, ddg = metric_jets(t, cx, cp)
    gamma = zeros(4, 4, 4)
    dgamma = zeros(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                gamma[a][b][c] = 0.5 * sum(
                    inverse[a][d] * (
                        dg[b][d][c] + dg[c][d][b] - dg[d][b][c]
                    ) for d in range(4)
                )
                for derivative in range(4):
                    dgamma[derivative][a][b][c] = 0.5 * sum(
                        dinverse[derivative][a][d] * (
                            dg[b][d][c] + dg[c][d][b] - dg[d][b][c]
                        )
                        + inverse[a][d] * (
                            ddg[derivative][b][d][c]
                            + ddg[derivative][c][d][b]
                            - ddg[derivative][d][b][c]
                        )
                        for d in range(4)
                    )
    riemann = zeros(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    riemann[a][b][c][d] = (
                        dgamma[c][a][d][b] - dgamma[d][a][c][b]
                        + sum(
                            gamma[a][c][e] * gamma[e][d][b]
                            - gamma[a][d][e] * gamma[e][c][b]
                            for e in range(4)
                        )
                    )
    return g, riemann


def inner(g, left, right) -> float:
    return sum(g[a][b] * left[a] * right[b] for a in range(4) for b in range(4))


def tidal_from_metric(
    t: float, te: float, lam_physical: float, cx: float, cp: float
) -> tuple[float, float, float, float]:
    g, riemann = curvature(t, cx, cp)
    root = math.sqrt(t * t + lam_physical * lam_physical)
    c = t / root
    s = lam_physical / root
    a = cx * t ** (-1.0 / 3.0)
    b = cp * t ** (2.0 / 3.0)
    alpha = (
        (t / te) ** (-2.0 / 3.0) * root
        / math.sqrt(te * te + lam_physical * lam_physical)
    )
    ray = (alpha, alpha * c / a, alpha * s / b, 0.0)
    screens = ((0.0, -s / a, c / b, 0.0), (0.0, 0.0, 0.0, 1.0 / b))

    def entry(left, right):
        return sum(
            g[mu][aa] * left[mu] * riemann[aa][bb][cc][dd]
            * ray[bb] * right[cc] * ray[dd]
            for mu in range(4) for aa in range(4) for bb in range(4)
            for cc in range(4) for dd in range(4)
        )

    return tuple(entry(left, right) for left in screens for right in screens)


def simpson(function, low: float, high: float, panels: int = 1600) -> float:
    if panels % 2:
        panels += 1
    step = (high - low) / panels
    total = function(low) + function(high)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * function(low + index * step)
    return total * step / 3.0


def reference_map(ratio: float, lam: float) -> tuple[float, float]:
    ibar = simpson(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        1.0, ratio,
    )
    kbar = simpson(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        1.0, ratio,
    )
    return (
        (1.0 + lam * lam) * math.sqrt(ratio * ratio + lam * lam)
        * ratio ** (-1.0 / 3.0) * ibar,
        math.sqrt(1.0 + lam * lam) * ratio ** (2.0 / 3.0) * kbar,
    )


def alpha(ratio: float, lam: float) -> float:
    return (
        ratio ** (-2.0 / 3.0) * math.sqrt(ratio * ratio + lam * lam)
        / math.sqrt(1.0 + lam * lam)
    )


def direct_q(ratio: float, lam: float) -> float:
    return 2.0 * lam * lam / (
        3.0 * (1.0 + lam * lam) * ratio ** (10.0 / 3.0)
    )


def rk_map(ratio: float, lam: float) -> tuple[float, float, float, float]:
    panels = max(500, int(420 * (ratio - 1.0)))
    step = (ratio - 1.0) / panels
    state = [0.0, 1.0, 0.0, 1.0]  # D_parallel, P_parallel, D_az, P_az

    def rhs(at: float, values: list[float]) -> list[float]:
        al = alpha(at, lam)
        q = direct_q(at, lam)
        return [values[1] / al, q * values[0] / al,
                values[3] / al, -q * values[2] / al]

    at = 1.0
    for _ in range(panels):
        k1 = rhs(at, state)
        k2_state = [state[i] + 0.5 * step * k1[i] for i in range(4)]
        k2 = rhs(at + 0.5 * step, k2_state)
        k3_state = [state[i] + 0.5 * step * k2[i] for i in range(4)]
        k3 = rhs(at + 0.5 * step, k3_state)
        k4_state = [state[i] + step * k3[i] for i in range(4)]
        k4 = rhs(at + step, k4_state)
        state = [
            state[i] + step * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
            for i in range(4)
        ]
        at += step
    return tuple(state)


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    rng = random.Random(342991)
    checks: dict[str, bool] = {}
    maxima = {"curvature_error": 0.0, "rk_map_relative_error": 0.0}

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    for index in range(160):
        te = 10.0 ** rng.uniform(-1.2, 1.2)
        ratio = 1.0 + 10.0 ** rng.uniform(-1.7, 1.0)
        t = te * ratio
        lam = 10.0 ** rng.uniform(-2.5, 2.5)
        lam_physical = te * lam
        cx = 10.0 ** rng.uniform(-0.7, 0.7)
        cp = 10.0 ** rng.uniform(-0.7, 0.7)
        matrix = tidal_from_metric(t, te, lam_physical, cx, cp)
        expected = 2.0 * lam_physical * lam_physical * te ** (4.0 / 3.0) / (
            3.0 * (te * te + lam_physical * lam_physical) * t ** (10.0 / 3.0)
        )
        error = max(
            abs(matrix[0] + expected), abs(matrix[3] - expected),
            abs(matrix[1]), abs(matrix[2]),
        ) / max(1.0, abs(expected))
        maxima["curvature_error"] = max(maxima["curvature_error"], error)
        record(f"metric_tidal_parallel_{index}", close(matrix[0], -expected, 2e-11))
        record(f"metric_tidal_azimuth_{index}", close(matrix[3], expected, 2e-11))
        record(f"metric_tidal_diagonal_{index}", abs(matrix[1]) < 2e-11 and abs(matrix[2]) < 2e-11)
        record(f"metric_tidal_tracefree_{index}", close(matrix[0] + matrix[3], 0.0, 2e-11))

    for index in range(360):
        ratio = 1.0 + 10.0 ** rng.uniform(-1.6, 0.9)
        lam = 10.0 ** rng.uniform(-2.0, 2.0)
        numeric = rk_map(ratio, lam)
        reference = reference_map(ratio, lam)
        error = max(
            abs(numeric[0] - reference[0]), abs(numeric[2] - reference[1])
        ) / max(1.0, abs(reference[0]), abs(reference[1]))
        maxima["rk_map_relative_error"] = max(maxima["rk_map_relative_error"], error)
        record(f"rk_position_map_{index}", error < 8.0e-8)
        record(f"rk_positive_map_{index}", numeric[0] > 0.0 and numeric[2] > 0.0)
        record(f"rk_positive_rates_{index}", numeric[1] > 0.0 and numeric[3] > 0.0)
        record(f"rk_shear_order_{index}", numeric[1] / numeric[0] > numeric[3] / numeric[2])

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": "INDEPENDENT_DIRECT_METRIC_CURVATURE_AND_RK_JACOBI_VERIFICATION",
        "maxima": maxima,
        "method": "generic coordinate metric two-jet curvature plus independent Simpson/RK4",
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:12]))


if __name__ == "__main__":
    main()
