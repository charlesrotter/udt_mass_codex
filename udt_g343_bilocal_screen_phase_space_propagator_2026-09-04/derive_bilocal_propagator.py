#!/usr/bin/env python3
"""Production checks for the bounded G343 bilocal screen propagator."""

from __future__ import annotations

import json
import math
import os
import random


LANDING = (
    "FULL_BILOCAL_PHASE_SPACE_PROPAGATOR_CLOSES__EXACT_COMPOSITION_SYMPLECTICITY"
    "__COMMON_AFFINE_INVERSE_AND_SOURCE_NORMALIZED_FREQUENCY_RECIPROCITY"
    "__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED"
    "__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "71db75f4"
TOL = 5.0e-9

GL_X = (
    -0.9602898564975363, -0.7966664774136267,
    -0.5255324099163290, -0.1834346424956498,
    0.1834346424956498, 0.5255324099163290,
    0.7966664774136267, 0.9602898564975363,
)
GL_W = (
    0.1012285362903763, 0.2223810344533745,
    0.3137066458778873, 0.3626837833783620,
    0.3626837833783620, 0.3137066458778873,
    0.2223810344533745, 0.1012285362903763,
)


def gauss_log(function, low: float, high: float, panels: int = 56) -> float:
    """Signed integral of function(T) dT on positive endpoints."""
    if low <= 0.0 or high <= 0.0:
        raise ValueError("positive-time domain required")
    left = math.log(low)
    width = (math.log(high) - left) / panels
    total = 0.0
    for panel in range(panels):
        middle = left + (panel + 0.5) * width
        half = 0.5 * width
        total += half * sum(
            weight * function(math.exp(middle + half * node))
            * math.exp(middle + half * node)
            for node, weight in zip(GL_X, GL_W)
        )
    return total


def hnorm(t: float, rho: float, t_reference: float) -> float:
    return math.sqrt(rho * t * t + (1.0 - rho) * t_reference * t_reference)


def alpha(t: float, rho: float, nu: float, t_reference: float) -> float:
    """dT/ds, with nu its value at the supplied reference event."""
    return (
        nu * t_reference ** (-1.0 / 3.0) * t ** (-2.0 / 3.0)
        * hnorm(t, rho, t_reference)
    )


def tide_q(t: float, rho: float, nu: float, t_reference: float) -> float:
    """Positive q in the metric-derived screen tide diag(-q,+q)."""
    return (
        2.0 * nu * nu * t_reference ** (4.0 / 3.0) * (1.0 - rho)
        / (3.0 * t ** (10.0 / 3.0))
    )


def channel_data(
    t: float, rho: float, nu: float, t_reference: float, channel: str
) -> tuple[float, float]:
    """Return a nonzero scalar Jacobi solution y and its affine log derivative."""
    h = hnorm(t, rho, t_reference)
    if channel == "parallel":
        y = t ** (-1.0 / 3.0) * h
        dlog_dt = rho * t / (h * h) - 1.0 / (3.0 * t)
    elif channel == "azimuth":
        y = t ** (2.0 / 3.0)
        dlog_dt = 2.0 / (3.0 * t)
    else:
        raise ValueError(channel)
    return y, alpha(t, rho, nu, t_reference) * dlog_dt


def bilocal_b(
    t1: float, t0: float, rho: float, nu: float, t_reference: float, channel: str
) -> float:
    y0, _ = channel_data(t0, rho, nu, t_reference, channel)
    y1, _ = channel_data(t1, rho, nu, t_reference, channel)
    if channel == "parallel":
        integral = gauss_log(
            lambda u: u ** (4.0 / 3.0) / hnorm(u, rho, t_reference) ** 3,
            t0, t1,
        )
    else:
        integral = gauss_log(
            lambda u: u ** (-2.0 / 3.0) / hnorm(u, rho, t_reference),
            t0, t1,
        )
    return y0 * y1 * t_reference ** (1.0 / 3.0) * integral / nu


def scalar_transfer(
    t1: float, t0: float, rho: float, nu: float, t_reference: float, channel: str
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Exact bilocal scalar fundamental map in the common affine gauge."""
    y0, mu0 = channel_data(t0, rho, nu, t_reference, channel)
    y1, mu1 = channel_data(t1, rho, nu, t_reference, channel)
    b = bilocal_b(t1, t0, rho, nu, t_reference, channel)
    ratio = y1 / y0
    a = ratio - mu0 * b
    d = 1.0 / ratio + mu1 * b
    c = mu1 * ratio - mu0 * d
    return ((a, b), (c, d))


def propagator(
    t1: float, t0: float, rho: float, nu: float, t_reference: float
) -> list[list[float]]:
    par = scalar_transfer(t1, t0, rho, nu, t_reference, "parallel")
    az = scalar_transfer(t1, t0, rho, nu, t_reference, "azimuth")
    return [
        [par[0][0], 0.0, par[0][1], 0.0],
        [0.0, az[0][0], 0.0, az[0][1]],
        [par[1][0], 0.0, par[1][1], 0.0],
        [0.0, az[1][0], 0.0, az[1][1]],
    ]


def identity(size: int = 4) -> list[list[float]]:
    return [[1.0 if row == col else 0.0 for col in range(size)] for row in range(size)]


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*matrix)]


def multiply(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def diagonal(values: tuple[float, ...]) -> list[list[float]]:
    return [[values[i] if i == j else 0.0 for j in range(len(values))]
            for i in range(len(values))]


def max_relative_error(left: list[list[float]], right: list[list[float]]) -> float:
    return max(
        abs(left[i][j] - right[i][j])
        / max(1.0, abs(left[i][j]), abs(right[i][j]))
        for i in range(len(left)) for j in range(len(left[0]))
    )


J = [
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, -1.0, 0.0, 0.0],
]


def unit_frequency_nu(t: float, rho: float, t_reference: float) -> float:
    """Affine gauge for unit normal-observer frequency at endpoint t."""
    return (
        t_reference ** (1.0 / 3.0) * t ** (2.0 / 3.0)
        / hnorm(t, rho, t_reference)
    )


def g342_mixed_widths(t1: float, t0: float, rho: float) -> tuple[float, float]:
    """G342 lambda-chart formulas, kept separate from the rho-chart production map."""
    if not 0.0 < rho < 1.0:
        raise ValueError("mixed direction required")
    lam = t0 * math.sqrt((1.0 - rho) / rho)
    i_value = gauss_log(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        t0, t1,
    )
    k_value = gauss_log(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        t0, t1,
    )
    return (
        (t0 * t0 + lam * lam) / t0
        * t1 ** (-1.0 / 3.0) * math.sqrt(t1 * t1 + lam * lam) * i_value,
        math.sqrt(t0 * t0 + lam * lam) * t1 ** (2.0 / 3.0) * k_value,
    )


def inverse_two(matrix: tuple[tuple[float, float], tuple[float, float]]):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def multiply_two(left, right):
    return tuple(tuple(sum(left[i][k] * right[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def transverse_power_transfer(
    t1: float, t0: float, transverse_constant: float, channel: str
):
    """Independent closed power-law basis at the transverse principal direction."""
    if channel == "parallel":
        def basis(t):
            return ((t ** (-1.0 / 3.0), t * t),
                    (-transverse_constant / (3.0 * t * t),
                     2.0 * transverse_constant * t ** (1.0 / 3.0)))
    else:
        def basis(t):
            return ((t ** (2.0 / 3.0), t),
                    (2.0 * transverse_constant / (3.0 * t),
                     transverse_constant * t ** (-2.0 / 3.0)))
    return multiply_two(basis(t1), inverse_two(basis(t0)))


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")

    checks: dict[str, bool] = {}
    maxima = {
        "composition_relative_error": 0.0,
        "g342_vertex_recovery_relative_error": 0.0,
        "gauge_covariance_relative_error": 0.0,
        "principal_limit_relative_error": 0.0,
        "reference_event_covariance_relative_error": 0.0,
        "reversal_relative_error": 0.0,
        "source_reciprocity_relative_error": 0.0,
        "symplectic_relative_error": 0.0,
        "wronskian_error": 0.0,
    }

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(343001)
    direction_controls = (0.0, 1.0, 1.0e-12, 1.0 - 1.0e-12)

    for index in range(800):
        t_reference = 10.0 ** rng.uniform(-1.0, 1.0)
        t0 = t_reference * 10.0 ** rng.uniform(-0.5, 0.5)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.8))
        t2 = t1 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.8))
        rho = direction_controls[index] if index < len(direction_controls) else rng.random()
        nu = 10.0 ** rng.uniform(-1.0, 1.0)

        m10 = propagator(t1, t0, rho, nu, t_reference)
        m21 = propagator(t2, t1, rho, nu, t_reference)
        m20 = propagator(t2, t0, rho, nu, t_reference)
        m01 = propagator(t0, t1, rho, nu, t_reference)

        composition_error = max_relative_error(multiply(m21, m10), m20)
        symplectic_error = max_relative_error(multiply(multiply(transpose(m10), J), m10), J)
        reversal_error = max_relative_error(multiply(m01, m10), identity())
        maxima["composition_relative_error"] = max(maxima["composition_relative_error"], composition_error)
        maxima["symplectic_relative_error"] = max(maxima["symplectic_relative_error"], symplectic_error)
        maxima["reversal_relative_error"] = max(maxima["reversal_relative_error"], reversal_error)
        record(f"composition_{index}", composition_error < TOL)
        record(f"symplectic_{index}", symplectic_error < TOL)
        record(f"reversal_inverse_{index}", reversal_error < TOL)

        b_antisymmetry = max(abs(m01[0][2] + m10[0][2]), abs(m01[1][3] + m10[1][3]))
        record(f"bilocal_B_antisymmetry_{index}", b_antisymmetry < TOL * max(1.0, abs(m10[0][2]), abs(m10[1][3])))

        par = scalar_transfer(t1, t0, rho, nu, t_reference, "parallel")
        az = scalar_transfer(t1, t0, rho, nu, t_reference, "azimuth")
        determinant_errors = (
            abs(par[0][0] * par[1][1] - par[0][1] * par[1][0] - 1.0),
            abs(az[0][0] * az[1][1] - az[0][1] * az[1][0] - 1.0),
        )
        maxima["wronskian_error"] = max(maxima["wronskian_error"], *determinant_errors)
        record(f"unit_channel_Wronskians_{index}", max(determinant_errors) < TOL)
        record(f"future_position_blocks_positive_{index}", m10[0][2] > 0.0 and m10[1][3] > 0.0)

        scale = 10.0 ** rng.uniform(-1.0, 1.0)
        scaled = propagator(t1, t0, rho, scale * nu, t_reference)
        change = diagonal((1.0, 1.0, scale, scale))
        change_inverse = diagonal((1.0, 1.0, 1.0 / scale, 1.0 / scale))
        expected_scaled = multiply(multiply(change, m10), change_inverse)
        gauge_error = max_relative_error(scaled, expected_scaled)
        maxima["gauge_covariance_relative_error"] = max(maxima["gauge_covariance_relative_error"], gauge_error)
        record(f"affine_gauge_covariance_{index}", gauge_error < TOL)

        nu0 = unit_frequency_nu(t0, rho, t_reference)
        nu1 = unit_frequency_nu(t1, rho, t_reference)
        forward_local = propagator(t1, t0, rho, nu0, t_reference)
        reverse_local = propagator(t0, t1, rho, nu1, t_reference)
        conversion = nu1 / nu0
        source_change = diagonal((1.0, 1.0, conversion, conversion))
        source_change_inverse = diagonal((1.0, 1.0, 1.0 / conversion, 1.0 / conversion))
        expected_reverse_local = multiply(
            multiply(source_change, propagator(t0, t1, rho, nu0, t_reference)),
            source_change_inverse,
        )
        source_error = max_relative_error(reverse_local, expected_reverse_local)
        maxima["source_reciprocity_relative_error"] = max(
            maxima["source_reciprocity_relative_error"], source_error
        )
        frequency_ratio = nu0 / nu1
        b_factor_error = max(
            abs(reverse_local[0][2] + frequency_ratio * forward_local[0][2]),
            abs(reverse_local[1][3] + frequency_ratio * forward_local[1][3]),
        ) / max(1.0, abs(reverse_local[0][2]), abs(reverse_local[1][3]))
        record(f"source_normalized_conjugation_{index}", source_error < TOL)
        record(f"source_normalized_B_frequency_factor_{index}", b_factor_error < TOL)

        new_reference = t_reference * 10.0 ** rng.uniform(-0.8, 0.8)
        if rho == 0.0:
            new_rho = 0.0
        elif rho == 1.0:
            new_rho = 1.0
        else:
            lam = t_reference * math.sqrt((1.0 - rho) / rho)
            new_rho = new_reference * new_reference / (new_reference * new_reference + lam * lam)
        new_nu = alpha(new_reference, rho, nu, t_reference)
        reference_changed = propagator(t1, t0, new_rho, new_nu, new_reference)
        reference_error = max_relative_error(reference_changed, m10)
        maxima["reference_event_covariance_relative_error"] = max(
            maxima["reference_event_covariance_relative_error"], reference_error
        )
        record(f"reference_event_covariance_{index}", reference_error < TOL)

    for index in range(200):
        t0 = 10.0 ** rng.uniform(-1.2, 1.2)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 1.0))
        rho = 10.0 ** rng.uniform(-4.0, -0.001)
        rho = min(rho, 1.0 - 1.0e-6)
        matrix = propagator(t1, t0, rho, 1.0, t0)
        old_parallel, old_azimuth = g342_mixed_widths(t1, t0, rho)
        error = max(
            abs(matrix[0][2] - old_parallel), abs(matrix[1][3] - old_azimuth)
        ) / max(1.0, abs(old_parallel), abs(old_azimuth))
        maxima["g342_vertex_recovery_relative_error"] = max(
            maxima["g342_vertex_recovery_relative_error"], error
        )
        record(f"g342_parallel_vertex_recovery_{index}", abs(matrix[0][2] - old_parallel) < TOL * max(1.0, abs(old_parallel)))
        record(f"g342_azimuth_vertex_recovery_{index}", abs(matrix[1][3] - old_azimuth) < TOL * max(1.0, abs(old_azimuth)))

    for index in range(120):
        t0 = 10.0 ** rng.uniform(-1.0, 1.0)
        t1 = t0 * (1.0 + 10.0 ** rng.uniform(-2.0, 0.8))
        t_reference = 10.0 ** rng.uniform(-1.0, 1.0)
        nu = 10.0 ** rng.uniform(-1.0, 1.0)
        affine_delta = (
            1.5 * t_reference ** (1.0 / 3.0)
            * (t1 ** (2.0 / 3.0) - t0 ** (2.0 / 3.0)) / nu
        )
        free = [
            [1.0, 0.0, affine_delta, 0.0],
            [0.0, 1.0, 0.0, affine_delta],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
        longitudinal = propagator(t1, t0, 1.0, nu, t_reference)
        long_error = max_relative_error(longitudinal, free)
        transverse = propagator(t1, t0, 0.0, nu, t_reference)
        transverse_constant = nu * t_reference ** (2.0 / 3.0)
        transverse_par = transverse_power_transfer(
            t1, t0, transverse_constant, "parallel"
        )
        transverse_az = transverse_power_transfer(
            t1, t0, transverse_constant, "azimuth"
        )
        transverse_expected = [
            [transverse_par[0][0], 0.0, transverse_par[0][1], 0.0],
            [0.0, transverse_az[0][0], 0.0, transverse_az[0][1]],
            [transverse_par[1][0], 0.0, transverse_par[1][1], 0.0],
            [0.0, transverse_az[1][0], 0.0, transverse_az[1][1]],
        ]
        transverse_error = max_relative_error(transverse, transverse_expected)
        maxima["principal_limit_relative_error"] = max(
            maxima["principal_limit_relative_error"], long_error, transverse_error
        )
        record(f"longitudinal_free_propagator_{index}", long_error < TOL)
        record(f"transverse_power_basis_propagator_{index}", transverse_error < TOL)
        record(f"principal_phase_space_rank_{index}",
               abs(transverse_par[0][0] * transverse_par[1][1] - transverse_par[0][1] * transverse_par[1][0] - 1.0) < TOL
               and abs(transverse_az[0][0] * transverse_az[1][1] - transverse_az[0][1] * transverse_az[1][0] - 1.0) < TOL)

    for index in range(64):
        t = 10.0 ** rng.uniform(-2.0, 2.0)
        rho = rng.random()
        t_reference = 10.0 ** rng.uniform(-2.0, 2.0)
        nu = 10.0 ** rng.uniform(-2.0, 2.0)
        coincident = propagator(t, t, rho, nu, t_reference)
        record(f"coincident_identity_{index}", max_relative_error(coincident, identity()) < 1.0e-13)
        labels = ((0, 0, 0), (1, 0, 0), (-1, 2, 0), (3, -1, 4))
        record(f"compact_path_labels_retained_{index}", tuple(labels) == labels)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": LANDING,
        "maxima": maxima,
        "method": "regular projective-direction chart plus exact bilocal reduction-of-order fundamental matrices",
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "selected_alternatives": ["A", "C1", "W1", "R1", "P1", "Q1"],
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:16]))


if __name__ == "__main__":
    main()
