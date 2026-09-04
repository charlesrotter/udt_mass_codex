#!/usr/bin/env python3
"""Implementation-distinct numerical reconstruction of the G339 result."""

from __future__ import annotations

import json
import math
import os
import random
from pathlib import Path


LANDING = (
    "FINITE_TIME_PAIR_COMPONENTS_DEPEND_ON_SUPPLIED_CARRY"
    "__G338_LIE_CARRY_IS_THE_COMOVING_OBSERVER_SEPARATION_QUERY"
    "__PARALLEL_AND_FERMI_LOCAL_RULERS_ARE_QUIET_CONTROLS"
    "__METRIC_DEFORMATION_IS_RECOVERED_FROM_TYPED_PAIR_PLUS_CARRY"
    "__NO_PHYSICAL_CARRY_SELECTED"
)


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def close(a: float, b: float, scale: float = 1.0, tol: float = 3e-8) -> bool:
    return abs(a - b) <= tol * max(scale, abs(a), abs(b))


def scales(T: float) -> tuple[float, float, float]:
    return T ** (-1.0 / 3.0), T ** (2.0 / 3.0), T ** (2.0 / 3.0)


def carried_coordinates(
    T: float, rho: float, theta: float, lam: float
) -> tuple[float, float, float]:
    a = scales(T)
    initial = (
        math.sqrt(rho),
        math.sqrt(1.0 - rho) * math.cos(theta),
        math.sqrt(1.0 - rho) * math.sin(theta),
    )
    return tuple(initial[i] * a[i] ** (-lam) for i in range(3))


def spatial_dot(T: float, v: tuple[float, ...], w: tuple[float, ...]) -> float:
    a = scales(T)
    return sum(a[i] * a[i] * v[i] * w[i] for i in range(3))


def spacetime_dot(T: float, v: tuple[float, ...], w: tuple[float, ...]) -> float:
    return -v[0] * w[0] + spatial_dot(T, v[1:], w[1:])


def pair_from_metric(T: float, J: tuple[float, float, float], z: float) -> tuple[float, ...]:
    c, s = math.cosh(z), math.sinh(z)
    e0 = (c, s * J[0], s * J[1], s * J[2])
    e1 = (s, c * J[0], c * J[1], c * J[2])
    h00 = spacetime_dot(T, e0, e0)
    h01 = spacetime_dot(T, e0, e1)
    h11 = spacetime_dot(T, e1, e1)
    return h00, h01, h11, h00 * h11 - h01 * h01


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def trans(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def main() -> None:
    rng = random.Random(339031)
    checks: dict[str, bool] = {}
    random_cases = 1200
    regular_cases = 0

    # Rebuild the carry and pair directly from the four-dimensional metric.
    for index in range(random_cases):
        rho = (0.0, 1.0, 2.0 / 3.0)[index % 3] if index < 30 else rng.random()
        lam = (0.0, 1.0)[index % 2] if index < 30 else rng.random()
        theta = rng.uniform(-math.pi, math.pi)
        T = math.exp(rng.uniform(-2.0, 2.0))
        z = rng.uniform(-1.15, 1.15)
        J = carried_coordinates(T, rho, theta, lam)
        G_direct = spatial_dot(T, J, J)
        G_formula = (
            rho * T ** (-2.0 * (1.0 - lam) / 3.0)
            + (1.0 - rho) * T ** (4.0 * (1.0 - lam) / 3.0)
        )
        require(close(G_direct, G_formula), f"direct_metric_length_{index}", checks)

        h00, h01, h11, det = pair_from_metric(T, J, z)
        c, s = math.cosh(z), math.sinh(z)
        require(close(h00, -c * c + G_formula * s * s),
                f"direct_pair_h00_{index}", checks)
        require(close(h01, (G_formula - 1.0) * s * c),
                f"direct_pair_h01_{index}", checks)
        require(close(h11, -s * s + G_formula * c * c),
                f"direct_pair_h11_{index}", checks)
        require(close(det, -G_formula), f"direct_pair_det_{index}", checks)

        Delta = -h00
        if Delta > 1e-8:
            L2 = h11 - h01 * h01 / h00
            require(close(L2, G_formula / Delta), f"direct_w1_length_{index}", checks)
            require(close(Delta * L2 / G_formula, 1.0),
                    f"direct_w1_unit_determinant_{index}", checks)
            regular_cases += 1

        # Finite-difference the vector extension and metric to reconstruct
        # the Levi-Civita transport and the Lie-derivative subtraction.
        step = 2e-6 * T
        Jp = carried_coordinates(T + step, rho, theta, lam)
        Jm = carried_coordinates(T - step, rho, theta, lam)
        dJ = tuple((Jp[i] - Jm[i]) / (2.0 * step) for i in range(3))
        ap = scales(T + step)
        am = scales(T - step)
        a0 = scales(T)
        adot = tuple((ap[i] - am[i]) / (2.0 * step) for i in range(3))
        H = tuple(adot[i] / a0[i] for i in range(3))
        covariant = tuple(dJ[i] + H[i] * J[i] for i in range(3))
        expected_covariant = tuple((1.0 - lam) * H[i] * J[i] for i in range(3))
        for axis in range(3):
            require(close(covariant[axis], expected_covariant[axis], tol=2e-7),
                    f"direct_connection_carry_{index}_{axis}", checks)

        gp = spatial_dot(T + step, Jp, Jp)
        gm = spatial_dot(T - step, Jm, Jm)
        raw_derivative = (gp - gm) / (2.0 * step)
        geometric = sum(2.0 * a0[i] * adot[i] * J[i] * J[i] for i in range(3))
        bracket = sum(a0[i] * a0[i] * dJ[i] * J[i] for i in range(3))
        require(close(raw_derivative, geometric + 2.0 * bracket, tol=3e-7),
                f"direct_transport_subtraction_{index}", checks)

        if lam == 0.0:
            require(all(abs(x) < 2e-8 for x in dJ), f"direct_lie_bracket_{index}", checks)
        if lam == 1.0:
            require(close(G_direct, 1.0), f"direct_parallel_norm_{index}", checks)
            require(all(abs(x) < 2e-7 for x in covariant),
                    f"direct_parallel_connection_{index}", checks)

    # Exact-silent direction: strict turn-on for all nonparallel diagnostic carries.
    for index in range(120):
        lam = rng.uniform(0.0, 0.98)
        T = math.exp(rng.uniform(-3.0, 3.0))
        if abs(T - 1.0) < 1e-4:
            T *= 1.1
        y = T ** (2.0 * (1.0 - lam) / 3.0)
        G = (2.0 / 3.0) / y + (1.0 / 3.0) * y * y
        factor = (y - 1.0) ** 2 * (y + 2.0) / (3.0 * y)
        require(close(G - 1.0, factor, tol=2e-10), f"silent_factor_{index}", checks)
        require(G > 1.0, f"silent_strict_turn_on_{index}", checks)

    # Independently whiten representative Lorentzian pair matrices.
    for index in range(200):
        G = math.exp(rng.uniform(-3.0, 3.0))
        root = math.sqrt(G)
        z = rng.uniform(-1.3, 1.3)
        c, s = math.cosh(z), math.sinh(z)
        B = [[c, s], [s, c]]
        Binv = [[c, -s], [-s, c]]
        d = [[-1.0, 0.0], [0.0, G]]
        h = matmul(trans(B), matmul(d, B))
        change = matmul(Binv, [[1.0, 0.0], [0.0, 1.0 / root]])
        whitened = matmul(trans(change), matmul(h, change))
        require(close(whitened[0][0], -1.0), f"whiten_00_{index}", checks)
        require(close(whitened[0][1], 0.0), f"whiten_01_{index}", checks)
        require(close(whitened[1][0], 0.0), f"whiten_10_{index}", checks)
        require(close(whitened[1][1], 1.0), f"whiten_11_{index}", checks)

    # Fermi-Walker accelerated principal-axis controls, rebuilt in the local plane.
    principal = (-1.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0)
    for axis, exponent in enumerate(principal):
        for index in range(100):
            T = math.exp(rng.uniform(-2.0, 2.0))
            H = exponent / T
            z = rng.uniform(-1.5, 1.5)
            c, s = math.cosh(z), math.sinh(z)
            U, S = (c, s), (s, c)
            acceleration = (H * s * S[0], H * s * S[1])
            dS = (H * s * U[0], H * s * U[1])
            mdot = lambda v, w: -v[0] * w[0] + v[1] * w[1]
            require(close(mdot(U, U), -1.0), f"fermi_clock_{axis}_{index}", checks)
            require(close(mdot(S, S), 1.0), f"fermi_ruler_{axis}_{index}", checks)
            require(close(mdot(U, S), 0.0), f"fermi_cross_{axis}_{index}", checks)
            require(close(mdot(acceleration, U), 0.0),
                    f"fermi_acceleration_orthogonal_{axis}_{index}", checks)
            require(close(mdot(acceleration, S), H * s),
                    f"fermi_acceleration_component_{axis}_{index}", checks)
            require(close(mdot(acceleration, S) + mdot(U, dS), 0.0),
                    f"fermi_cross_derivative_{axis}_{index}", checks)

    # Carry-independent metric shape for the fixed normal congruence.
    for index in range(100):
        T = math.exp(rng.uniform(-4.0, 4.0))
        eig = (-1.0 / (3.0 * T), 2.0 / (3.0 * T), 2.0 / (3.0 * T))
        tr = sum(eig)
        tr2 = sum(x * x for x in eig)
        det = eig[0] * eig[1] * eig[2]
        require(close(tr2 / (tr * tr), 1.0), f"metric_trace_ratio_{index}", checks)
        require(close(det / (tr**3), -4.0 / 27.0),
                f"metric_det_ratio_{index}", checks)

    result = {
        "landing": LANDING,
        "grade": "INDEPENDENTLY_VERIFIED_DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW",
        "method": "direct 4D metric reconstruction; no production import or result read",
        "random_seed": 339031,
        "random_cases": random_cases,
        "regular_cases": regular_cases,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "all_passed": all(checks.values()),
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        Path(__file__).with_name("INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps({k: result[k] for k in (
        "landing", "grade", "method", "random_cases", "regular_cases",
        "checks_passed", "checks_total", "all_passed"
    )}, indent=2))


if __name__ == "__main__":
    main()
