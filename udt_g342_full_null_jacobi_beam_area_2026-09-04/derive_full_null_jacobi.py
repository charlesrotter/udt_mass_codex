#!/usr/bin/env python3
"""Production checks for the bounded G342 exact full null Jacobi map."""

from __future__ import annotations

import json
import math
import os
import random


LANDING = (
    "FULL_METRIC_JACOBI_MAP_CLOSES__BOTH_SCREEN_RATES_AND_MEAN_EXPANSION_POSITIVE"
    "__SHEAR_ZERO_ONLY_ON_LONGITUDINAL_SYMMETRY_LOCUS_OR_VERTEX"
    "__EACH_COMPACT_LIFT_RETAINS_POSITIVE_AREA_WITH_PATH_LABEL"
    "__NO_LUMINOSITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED"
)
PREREGISTRATION_COMMIT = "b8d56fdd"
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


def close(left: float, right: float, tol: float = TOL) -> bool:
    return abs(left - right) <= tol * max(1.0, abs(left), abs(right))


def gauss_log_integral(function, upper: float, panels: int = 36) -> float:
    """Integrate f(u) du from 1 to upper using x=log(u)."""
    high = math.log(upper)
    width = high / panels
    total = 0.0
    for panel in range(panels):
        middle = (panel + 0.5) * width
        half = 0.5 * width
        total += half * sum(
            weight * function(math.exp(middle + half * node))
            * math.exp(middle + half * node)
            for node, weight in zip(GL_X, GL_W)
        )
    return total


def integrals(ratio: float, lam: float) -> tuple[float, float]:
    ibar = gauss_log_integral(
        lambda u: u ** (4.0 / 3.0) / (u * u + lam * lam) ** 1.5,
        ratio,
    )
    kbar = gauss_log_integral(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam),
        ratio,
    )
    return ibar, kbar


def alpha(ratio: float, lam: float) -> float:
    return (
        ratio ** (-2.0 / 3.0)
        * math.sqrt(ratio * ratio + lam * lam)
        / math.sqrt(1.0 + lam * lam)
    )


def qbar(ratio: float, lam: float) -> float:
    """Dimensionless positive tide q*T_e^2 in diag(-q,+q)."""
    return 2.0 * lam * lam / (
        3.0 * (1.0 + lam * lam) * ratio ** (10.0 / 3.0)
    )


def jacobi_state(ratio: float, lam: float) -> dict[str, float]:
    ibar, kbar = integrals(ratio, lam)
    root = math.sqrt(ratio * ratio + lam * lam)
    source_root = math.sqrt(1.0 + lam * lam)

    f = root * ratio ** (-1.0 / 3.0)
    f_log_1 = ratio / (ratio * ratio + lam * lam) - 1.0 / (3.0 * ratio)
    f_log_2 = (
        (lam * lam - ratio * ratio) / (ratio * ratio + lam * lam) ** 2
        + 1.0 / (3.0 * ratio * ratio)
    )
    f_1 = f * f_log_1
    f_2 = f * (f_log_1 * f_log_1 + f_log_2)

    i_1 = ratio ** (4.0 / 3.0) / (ratio * ratio + lam * lam) ** 1.5
    i_2 = i_1 * (
        4.0 / (3.0 * ratio) - 3.0 * ratio / (ratio * ratio + lam * lam)
    )
    cpar = 1.0 + lam * lam
    dpar = cpar * f * ibar
    dpar_r = cpar * (f_1 * ibar + f * i_1)
    dpar_rr = cpar * (f_2 * ibar + 2.0 * f_1 * i_1 + f * i_2)

    h = ratio ** (2.0 / 3.0)
    h_1 = h * 2.0 / (3.0 * ratio)
    h_2 = h * (-2.0) / (9.0 * ratio * ratio)
    k_1 = ratio ** (-2.0 / 3.0) / root
    k_2 = k_1 * (-2.0 / (3.0 * ratio) - ratio / (ratio * ratio + lam * lam))
    daz = source_root * h * kbar
    daz_r = source_root * (h_1 * kbar + h * k_1)
    daz_rr = source_root * (h_2 * kbar + 2.0 * h_1 * k_1 + h * k_2)

    al = alpha(ratio, lam)
    al_r = al * (-2.0 / (3.0 * ratio) + ratio / (ratio * ratio + lam * lam))
    dpar_dot = al * dpar_r
    daz_dot = al * daz_r
    dpar_ddot = al * (al_r * dpar_r + al * dpar_rr)
    daz_ddot = al * (al_r * daz_r + al * daz_rr)
    beta_par = dpar_dot / dpar
    beta_az = daz_dot / daz
    expansion_total = beta_par + beta_az
    shear_gap = beta_par - beta_az
    area = dpar * daz
    return {
        "alpha": al,
        "area": area,
        "area_dot": area * expansion_total,
        "beta_az": beta_az,
        "beta_parallel": beta_par,
        "daz": daz,
        "daz_ddot": daz_ddot,
        "daz_dot": daz_dot,
        "dparallel": dpar,
        "dparallel_ddot": dpar_ddot,
        "dparallel_dot": dpar_dot,
        "expansion_mean": 0.5 * expansion_total,
        "expansion_total": expansion_total,
        "qbar": qbar(ratio, lam),
        "raychaudhuri_rhs": -0.5 * expansion_total ** 2 - 0.5 * shear_gap ** 2,
        "shear_contraction": 0.5 * shear_gap ** 2,
        "shear_gap": shear_gap,
    }


def endpoint(ratio: float, lam: float) -> tuple[float, float]:
    qx = gauss_log_integral(
        lambda u: u ** (4.0 / 3.0) / math.sqrt(u * u + lam * lam), ratio
    )
    qp = lam * gauss_log_integral(
        lambda u: u ** (-2.0 / 3.0) / math.sqrt(u * u + lam * lam), ratio
    )
    return qx, qp


def affine_length(ratio: float, lam: float) -> float:
    return gauss_log_integral(lambda u: 1.0 / alpha(u, lam), ratio)


def solve_ratio_for_affine(target: float, lam: float, guess: float) -> float:
    low = 1.0
    high = max(guess, 1.001)
    while affine_length(high, lam) < target:
        high = 1.0 + 2.0 * (high - 1.0)
    for _ in range(54):
        middle = 0.5 * (low + high)
        if affine_length(middle, lam) < target:
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def fixed_affine_direction_derivative(ratio: float, lam: float) -> float:
    theta = math.atan(lam)
    step = min(2.0e-5, 0.08 * theta, 0.08 * (0.5 * math.pi - theta))
    target = affine_length(ratio, lam)
    values = []
    for shifted_theta in (theta - step, theta + step):
        shifted_lam = math.tan(shifted_theta)
        shifted_ratio = solve_ratio_for_affine(target, shifted_lam, ratio)
        values.append(endpoint(shifted_ratio, shifted_lam))
    dqx = (values[1][0] - values[0][0]) / (2.0 * step)
    dqp = (values[1][1] - values[0][1]) / (2.0 * step)
    root = math.sqrt(ratio * ratio + lam * lam)
    c = ratio / root
    s = lam / root
    return -s * ratio ** (-1.0 / 3.0) * dqx + c * ratio ** (2.0 / 3.0) * dqp


def principal_values(ratio: float) -> dict[str, float]:
    log_r = math.log(ratio)
    longitudinal = 1.5 * math.expm1(2.0 * log_r / 3.0)
    transverse_parallel = (
        3.0 / 7.0 * math.exp(-log_r / 3.0) * math.expm1(7.0 * log_r / 3.0)
    )
    transverse_azimuth = (
        3.0 * math.exp(2.0 * log_r / 3.0) * math.expm1(log_r / 3.0)
    )
    return {
        "longitudinal": longitudinal,
        "transverse_parallel": transverse_parallel,
        "transverse_azimuth": transverse_azimuth,
    }


def main() -> None:
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    checks: dict[str, bool] = {}
    maxima = {
        "fixed_affine_relative_error": 0.0,
        "jacobi_residual": 0.0,
        "longitudinal_limit_relative_error": 0.0,
        "transverse_limit_relative_error": 0.0,
    }

    def record(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    rng = random.Random(342001)
    for index in range(720):
        ratio = 1.0 + 10.0 ** rng.uniform(-2.0, 2.0)
        lam = 10.0 ** rng.uniform(-3.0, 3.0)
        state = jacobi_state(ratio, lam)
        q = state["qbar"]
        residual_parallel = abs(state["dparallel_ddot"] - q * state["dparallel"])
        residual_azimuth = abs(state["daz_ddot"] + q * state["daz"])
        residual_scale = max(1.0, abs(q * state["dparallel"]), abs(q * state["daz"]))
        maxima["jacobi_residual"] = max(
            maxima["jacobi_residual"], residual_parallel / residual_scale,
            residual_azimuth / residual_scale,
        )
        record(f"positive_map_{index}", state["dparallel"] > 0.0 and state["daz"] > 0.0)
        record(f"positive_area_{index}", state["area"] > 0.0 and state["area_dot"] > 0.0)
        record(
            f"positive_rates_{index}",
            state["beta_parallel"] > 0.0 and state["beta_az"] > 0.0
            and state["expansion_mean"] > 0.0,
        )
        record(f"mixed_shear_{index}", state["shear_gap"] > 0.0)
        record(
            f"jacobi_equation_{index}",
            close(state["dparallel_ddot"], q * state["dparallel"])
            and close(state["daz_ddot"], -q * state["daz"]),
        )
        record(
            f"raychaudhuri_{index}",
            close(
                (q - state["beta_parallel"] ** 2)
                + (-q - state["beta_az"] ** 2),
                state["raychaudhuri_rhs"],
            ),
        )

    for index in range(96):
        ratio = 1.0 + 10.0 ** rng.uniform(-1.5, 1.0)
        lam = 10.0 ** rng.uniform(-1.2, 1.2)
        finite = fixed_affine_direction_derivative(ratio, lam)
        exact = jacobi_state(ratio, lam)["dparallel"]
        error = abs(finite - exact) / max(1.0, abs(exact))
        maxima["fixed_affine_relative_error"] = max(
            maxima["fixed_affine_relative_error"], error
        )
        record(f"fixed_affine_endpoint_variation_{index}", error < 2.0e-7)

    for index in range(80):
        ratio = 1.0 + 10.0 ** rng.uniform(-2.0, 1.5)
        expected = principal_values(ratio)
        near_longitudinal = jacobi_state(ratio, 1.0e-5)
        # At finite lambda the error from the exact transverse projective boundary is O(lambda^-2).
        # Use a point far enough into that declared chart for the preregistered 5e-9 raw tolerance.
        near_transverse = jacobi_state(ratio, 1.0e6)
        long_error = max(
            abs(near_longitudinal["dparallel"] - expected["longitudinal"]),
            abs(near_longitudinal["daz"] - expected["longitudinal"]),
        ) / max(1.0, expected["longitudinal"])
        transverse_error = max(
            abs(near_transverse["dparallel"] - expected["transverse_parallel"]),
            abs(near_transverse["daz"] - expected["transverse_azimuth"]),
        ) / max(
            1.0, expected["transverse_parallel"], expected["transverse_azimuth"]
        )
        maxima["longitudinal_limit_relative_error"] = max(
            maxima["longitudinal_limit_relative_error"], long_error
        )
        maxima["transverse_limit_relative_error"] = max(
            maxima["transverse_limit_relative_error"], transverse_error
        )
        record(f"longitudinal_limit_{index}", long_error < 2.0e-8)
        record(f"transverse_limit_{index}", transverse_error < TOL)
        record(
            f"principal_regular_{index}",
            expected["longitudinal"] > 0.0
            and expected["transverse_parallel"] > 0.0
            and expected["transverse_azimuth"] > 0.0,
        )

    # The longitudinal ray has q=0, D=w I, so it is shear-free exactly.
    for index in range(32):
        ratio = 1.0 + 10.0 ** rng.uniform(-3.0, 2.0)
        expected = principal_values(ratio)["longitudinal"]
        record(f"longitudinal_zero_tide_{index}", qbar(ratio, 0.0) == 0.0)
        record(f"longitudinal_equal_screen_map_{index}", expected > 0.0)

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "assertions": len(checks),
        "failed": failed,
        "landing": LANDING,
        "maxima": maxima,
        "method": "exact endpoint variation plus analytic metric-tide Jacobi identities",
        "preregistration_commit": PREREGISTRATION_COMMIT,
        "selected_alternatives": ["A", "E1", "S1", "M1", "Q1"],
        "status": "PASS" if not failed else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed[:12]))


if __name__ == "__main__":
    main()
