#!/usr/bin/env python3
"""Implementation-distinct metric-curvature and ODE verification for G343."""

from __future__ import annotations

import json
import math
import os
import random


TOL = 2.0e-7


def zero_tensor(*shape: int):
    if len(shape) == 1:
        return [0.0 for _ in range(shape[0])]
    return [zero_tensor(*shape[1:]) for _ in range(shape[0])]


def metric_curvature(t: float, cx: float, cp: float):
    """Coordinate metric, connection, and Riemann built directly from the metric two-jet."""
    g = zero_tensor(4, 4)
    dg = zero_tensor(4, 4, 4)
    ddg = zero_tensor(4, 4, 4, 4)
    g[0][0] = -1.0
    g[1][1] = cx * cx * t ** (-2.0 / 3.0)
    g[2][2] = cp * cp * t ** (4.0 / 3.0)
    g[3][3] = g[2][2]
    for axis, power in ((1, -2.0 / 3.0), (2, 4.0 / 3.0), (3, 4.0 / 3.0)):
        dg[0][axis][axis] = power * g[axis][axis] / t
        ddg[0][0][axis][axis] = power * (power - 1.0) * g[axis][axis] / (t * t)

    inverse = zero_tensor(4, 4)
    for axis in range(4):
        inverse[axis][axis] = 1.0 / g[axis][axis]
    inverse_jet = zero_tensor(4, 4, 4)
    for derivative in range(4):
        for a in range(4):
            for d in range(4):
                inverse_jet[derivative][a][d] = -sum(
                    inverse[a][m] * dg[derivative][m][n] * inverse[n][d]
                    for m in range(4) for n in range(4)
                )

    gamma = zero_tensor(4, 4, 4)
    gamma_jet = zero_tensor(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                gamma[a][b][c] = 0.5 * sum(
                    inverse[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                    for d in range(4)
                )
                for derivative in range(4):
                    gamma_jet[derivative][a][b][c] = 0.5 * sum(
                        inverse_jet[derivative][a][d]
                        * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                        + inverse[a][d]
                        * (ddg[derivative][b][d][c]
                           + ddg[derivative][c][d][b]
                           - ddg[derivative][d][b][c])
                        for d in range(4)
                    )

    riemann = zero_tensor(4, 4, 4, 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    riemann[a][b][c][d] = (
                        gamma_jet[c][a][d][b] - gamma_jet[d][a][c][b]
                        + sum(
                            gamma[a][c][e] * gamma[e][d][b]
                            - gamma[a][d][e] * gamma[e][c][b]
                            for e in range(4)
                        )
                    )
    return g, riemann


def direct_screen_tide(
    t: float, rho: float, nu: float, t_reference: float, cx: float, cp: float
):
    g, riemann = metric_curvature(t, cx, cp)
    h = math.sqrt(rho * t * t + (1.0 - rho) * t_reference * t_reference)
    omega = nu * t_reference ** (-1.0 / 3.0) * t ** (-2.0 / 3.0) * h
    cosine = math.sqrt(rho) * t / h
    sine = math.sqrt(1.0 - rho) * t_reference / h
    a = cx * t ** (-1.0 / 3.0)
    b = cp * t ** (2.0 / 3.0)
    ray = (omega, omega * cosine / a, omega * sine / b, 0.0)
    screens = (
        (0.0, -sine / a, cosine / b, 0.0),
        (0.0, 0.0, 0.0, 1.0 / b),
    )

    def component(left, right):
        return sum(
            g[mu][aa] * left[mu] * riemann[aa][bb][cc][dd]
            * ray[bb] * right[cc] * ray[dd]
            for mu in range(4) for aa in range(4) for bb in range(4)
            for cc in range(4) for dd in range(4)
        )

    return tuple(component(left, right) for left in screens for right in screens)


def matrix_multiply(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def matrix_add(left, right, factor: float = 1.0):
    return [[left[i][j] + factor * right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def matrix_scale(matrix, factor: float):
    return [[factor * value for value in row] for row in matrix]


def matrix_transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def identity():
    return [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]


J = [
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, -1.0, 0.0, 0.0],
]


def relative_error(left, right) -> float:
    return max(
        abs(left[i][j] - right[i][j])
        / max(1.0, abs(left[i][j]), abs(right[i][j]))
        for i in range(len(left)) for j in range(len(left[0]))
    )


def ray_rate(t: float, rho: float, nu: float, t_reference: float) -> float:
    return (
        nu * t_reference ** (-1.0 / 3.0) * t ** (-2.0 / 3.0)
        * math.sqrt(rho * t * t + (1.0 - rho) * t_reference * t_reference)
    )


def q_value(t: float, rho: float, nu: float, t_reference: float) -> float:
    return (
        2.0 * nu * nu * t_reference ** (4.0 / 3.0) * (1.0 - rho)
        / (3.0 * t ** (10.0 / 3.0))
    )


def system_generator(t: float, rho: float, nu: float, t_reference: float):
    q = q_value(t, rho, nu, t_reference)
    return [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [q, 0.0, 0.0, 0.0],
        [0.0, -q, 0.0, 0.0],
    ]


def integrate_phase(t1: float, t0: float, rho: float, nu: float, t_reference: float):
    """RK4 in x=log(T), starting from the identity."""
    x0 = math.log(t0)
    x1 = math.log(t1)
    panels = max(600, int(280 * abs(x1 - x0)))
    step = (x1 - x0) / panels
    state = identity()

    def rhs(x, matrix):
        t = math.exp(x)
        factor = t / ray_rate(t, rho, nu, t_reference)
        return matrix_scale(
            matrix_multiply(system_generator(t, rho, nu, t_reference), matrix), factor
        )

    at = x0
    for _ in range(panels):
        k1 = rhs(at, state)
        k2 = rhs(at + 0.5 * step, matrix_add(state, k1, 0.5 * step))
        k3 = rhs(at + 0.5 * step, matrix_add(state, k2, 0.5 * step))
        k4 = rhs(at + step, matrix_add(state, k3, step))
        state = [
            [state[i][j] + step * (k1[i][j] + 2.0 * k2[i][j]
                                     + 2.0 * k3[i][j] + k4[i][j]) / 6.0
             for j in range(4)]
            for i in range(4)
        ]
        at += step
    return state


def simpson_log(function, low: float, high: float, panels: int = 1200) -> float:
    if panels % 2:
        panels += 1
    x0 = math.log(low)
    step = (math.log(high) - x0) / panels

    def transformed(x):
        t = math.exp(x)
        return function(t) * t

    total = transformed(x0) + transformed(x0 + panels * step)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * transformed(x0 + index * step)
    return total * step / 3.0


def two_inverse(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return ((matrix[1][1] / det, -matrix[0][1] / det),
            (-matrix[1][0] / det, matrix[0][0] / det))


def two_product(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def basis_matrix(
    t: float, integral_reference: float, rho: float, nu: float,
    ray_reference: float, channel: str
):
    h = math.sqrt(rho * t * t + (1.0 - rho) * ray_reference * ray_reference)
    if channel == "parallel":
        y = t ** (-1.0 / 3.0) * h
        dlog = rho * t / (h * h) - 1.0 / (3.0 * t)
        weight = lambda u: u ** (4.0 / 3.0) / (
            rho * u * u + (1.0 - rho) * ray_reference * ray_reference
        ) ** 1.5
    else:
        y = t ** (2.0 / 3.0)
        dlog = 2.0 / (3.0 * t)
        weight = lambda u: u ** (-2.0 / 3.0) / math.sqrt(
            rho * u * u + (1.0 - rho) * ray_reference * ray_reference
        )
    mu = ray_rate(t, rho, nu, ray_reference) * dlog
    integral = (
        ray_reference ** (1.0 / 3.0)
        * simpson_log(weight, integral_reference, t) / nu
    )
    second = y * integral
    return ((y, second), (mu * y, mu * second + 1.0 / y))


def fundamental_reference(
    t1: float, t0: float, rho: float, nu: float, ray_reference: float
):
    par = two_product(
        basis_matrix(t1, t0, rho, nu, ray_reference, "parallel"),
        two_inverse(basis_matrix(t0, t0, rho, nu, ray_reference, "parallel")),
    )
    az = two_product(
        basis_matrix(t1, t0, rho, nu, ray_reference, "azimuth"),
        two_inverse(basis_matrix(t0, t0, rho, nu, ray_reference, "azimuth")),
    )
    return [
        [par[0][0], 0.0, par[0][1], 0.0],
        [0.0, az[0][0], 0.0, az[0][1]],
        [par[1][0], 0.0, par[1][1], 0.0],
        [0.0, az[1][0], 0.0, az[1][1]],
    ]


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks: dict[str, bool] = {}
    maxima = {
        "composition_relative_error": 0.0,
        "curvature_relative_error": 0.0,
        "ode_fundamental_relative_error": 0.0,
        "reference_event_covariance_relative_error": 0.0,
        "reversal_relative_error": 0.0,
        "symplectic_relative_error": 0.0,
    }

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(343991)
    direction_controls = (0.0, 1.0, 1.0e-10, 1.0 - 1.0e-10)

    for index in range(180):
        t = 10.0 ** rng.uniform(-1.2, 1.2)
        t_reference = 10.0 ** rng.uniform(-1.2, 1.2)
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.8, 0.8)
        cx = 10.0 ** rng.uniform(-0.5, 0.5)
        cp = 10.0 ** rng.uniform(-0.5, 0.5)
        tide = direct_screen_tide(t, rho, nu, t_reference, cx, cp)
        expected = q_value(t, rho, nu, t_reference)
        error = max(abs(tide[0] + expected), abs(tide[3] - expected),
                    abs(tide[1]), abs(tide[2])) / max(1.0, abs(expected))
        maxima["curvature_relative_error"] = max(maxima["curvature_relative_error"], error)
        record(f"direct_metric_parallel_tide_{index}", abs(tide[0] + expected) < 2.0e-10 * max(1.0, abs(expected)))
        record(f"direct_metric_azimuth_tide_{index}", abs(tide[3] - expected) < 2.0e-10 * max(1.0, abs(expected)))
        record(f"direct_metric_zero_cross_tide_{index}", max(abs(tide[1]), abs(tide[2])) < 2.0e-10 * max(1.0, abs(expected)))
        record(f"direct_metric_tracefree_tide_{index}", abs(tide[0] + tide[3]) < 2.0e-10 * max(1.0, abs(expected)))

    for index in range(320):
        t_reference = 10.0 ** rng.uniform(-0.8, 0.8)
        t0 = t_reference * 10.0 ** rng.uniform(-0.35, 0.35)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-1.7, 0.55))
        t2 = t1 * (1.0 + 10.0 ** rng.uniform(-1.7, 0.55))
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-0.7, 0.7)

        ode10 = integrate_phase(t1, t0, rho, nu, t_reference)
        reference10 = fundamental_reference(t1, t0, rho, nu, t_reference)
        map_error = relative_error(ode10, reference10)
        maxima["ode_fundamental_relative_error"] = max(maxima["ode_fundamental_relative_error"], map_error)
        record(f"ode_matches_fundamental_{index}", map_error < TOL)

        symplectic_error = relative_error(
            matrix_multiply(matrix_multiply(matrix_transpose(ode10), J), ode10), J
        )
        maxima["symplectic_relative_error"] = max(maxima["symplectic_relative_error"], symplectic_error)
        record(f"ode_symplectic_{index}", symplectic_error < TOL)

        ode21 = integrate_phase(t2, t1, rho, nu, t_reference)
        ode20 = integrate_phase(t2, t0, rho, nu, t_reference)
        composition_error = relative_error(matrix_multiply(ode21, ode10), ode20)
        maxima["composition_relative_error"] = max(maxima["composition_relative_error"], composition_error)
        record(f"ode_composition_{index}", composition_error < TOL)

        reverse = integrate_phase(t0, t1, rho, nu, t_reference)
        reversal_error = relative_error(matrix_multiply(reverse, ode10), identity())
        maxima["reversal_relative_error"] = max(maxima["reversal_relative_error"], reversal_error)
        record(f"ode_reversal_{index}", reversal_error < TOL)

        record(f"future_bilocal_widths_positive_{index}", ode10[0][2] > 0.0 and ode10[1][3] > 0.0)
        record(f"independent_screen_decoupling_{index}",
               max(abs(ode10[0][1]), abs(ode10[0][3]), abs(ode10[1][0]),
                   abs(ode10[1][2]), abs(ode10[2][1]), abs(ode10[2][3]),
                   abs(ode10[3][0]), abs(ode10[3][2])) < 1.0e-13)

        new_reference = t_reference * 10.0 ** rng.uniform(-0.6, 0.6)
        if rho == 0.0:
            new_rho = 0.0
        elif rho == 1.0:
            new_rho = 1.0
        else:
            lam = t_reference * math.sqrt((1.0 - rho) / rho)
            new_rho = new_reference * new_reference / (
                new_reference * new_reference + lam * lam
            )
        new_nu = ray_rate(new_reference, rho, nu, t_reference)
        changed_reference = fundamental_reference(
            t1, t0, new_rho, new_nu, new_reference
        )
        covariance_error = relative_error(changed_reference, reference10)
        maxima["reference_event_covariance_relative_error"] = max(
            maxima["reference_event_covariance_relative_error"], covariance_error
        )
        record(f"independent_reference_event_covariance_{index}", covariance_error < TOL)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": "INDEPENDENT_DIRECT_METRIC_CURVATURE_RK_AND_FUNDAMENTAL_MATRIX_VERIFICATION",
        "maxima": maxima,
        "method": "generic coordinate metric two-jet curvature plus log-time RK4 and independently assembled unit-Wronskian basis",
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:16]))


if __name__ == "__main__":
    main()
