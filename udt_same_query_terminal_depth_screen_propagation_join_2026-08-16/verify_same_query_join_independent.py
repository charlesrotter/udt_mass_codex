#!/usr/bin/env python3
"""Independent numerical/Fraction verification of the bounded G109 join."""

from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]


def terminal(T: Fraction, L: Fraction, beta: Fraction) -> list[list[Fraction]]:
    return [[T, T * beta], [Fraction(0), L]]


def inverse_upper(b: list[list[Fraction]]) -> list[list[Fraction]]:
    a, c, d = b[0][0], b[0][1], b[1][1]
    return [[1 / a, -c / (a * d)], [Fraction(0), 1 / d]]


def delta(T0: Fraction, L0: Fraction, T1: Fraction, L1: Fraction) -> float:
    return 0.5 * math.log(float((L1 * T0) / (T1 * L0)))


def fraction_network_check() -> dict[str, float | bool]:
    states = [
        (Fraction(3, 2), Fraction(5, 4), Fraction(1, 7)),
        (Fraction(7, 5), Fraction(11, 6), Fraction(-2, 9)),
        (Fraction(13, 8), Fraction(17, 10), Fraction(3, 11)),
    ]
    B = [terminal(*state) for state in states]
    R10 = matmul(B[1], inverse_upper(B[0]))
    R21 = matmul(B[2], inverse_upper(B[1]))
    R20 = matmul(B[2], inverse_upper(B[0]))
    composed = matmul(R21, R10)
    d01 = delta(*states[0][:2], *states[1][:2])
    d12 = delta(*states[1][:2], *states[2][:2])
    d02 = delta(*states[0][:2], *states[2][:2])
    reverse = delta(*states[1][:2], *states[0][:2])
    character = -0.5 * math.log(float(R10[0][0] / R10[1][1]))
    return {
        "matrix_composition_exact": composed == R20,
        "scalar_composition_residual": abs(d01 + d12 - d02),
        "reversal_residual": abs(reverse + d01),
        "character_residual": abs(character - d01),
    }


def nonlinear_check() -> dict[str, float | bool]:
    def phi(x: float) -> float:
        return x + x * x / 5.0

    def phi_dot(x: float) -> float:
        return 1.0 + 2.0 * x / 5.0

    def kappa(x: float) -> float:
        return x**3 / 10.0

    def beta(x: float) -> float:
        return x / 7.0 + x * x / 17.0

    def h(x: float) -> np.ndarray:
        T = math.exp(kappa(x) - phi(x))
        L = math.exp(kappa(x) + phi(x))
        b = beta(x)
        return np.array([[-T * T, -T * T * b], [-T * T * b, L * L - T * T * b * b]])

    def W(x: float) -> np.ndarray:
        u = 2.0 * x / 5.0 + x * x / 11.0
        v = -x / 6.0 + x**3 / 13.0
        angle = x * x / 9.0
        R = np.array(
            [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
        )
        return R @ np.diag([math.exp(u), math.exp(v)])

    max_phi = 0.0
    max_join = 0.0
    max_atlas = 0.0
    with (HERE / "CONTROL_ATLAS.tsv").open(newline="") as handle:
        atlas = {float(row["lambda"]): row for row in csv.DictReader(handle, delimiter="\t")}
    for x in (0.0, 0.2, 0.5, 0.8):
        hx = h(x)
        recovered = 0.25 * math.log((-np.linalg.det(hx)) / hx[0, 0] ** 2)
        max_phi = max(max_phi, abs(recovered - phi(x)))
        step = 1.0e-6
        log_area_plus = math.log(abs(np.linalg.det(W(x + step))))
        log_area_minus = math.log(abs(np.linalg.det(W(x - step))))
        joined = (log_area_plus - log_area_minus) / (4.0 * step * phi_dot(x))
        u_dot = 2.0 / 5.0 + 2.0 * x / 11.0
        v_dot = -1.0 / 6.0 + 3.0 * x * x / 13.0
        analytic = (u_dot + v_dot) / (2.0 * phi_dot(x))
        max_join = max(max_join, abs(joined - analytic))
        max_atlas = max(max_atlas, abs(analytic - float(atlas[x]["a_eff_joined"])))
    return {
        "maximum_phi_recovery_residual": max_phi,
        "maximum_finite_difference_join_residual": max_join,
        "maximum_independent_atlas_residual": max_atlas,
    }


def hostile_checks() -> dict[str, float | bool]:
    pA, p_in, p_out, pC = 0.2, 0.7, -0.1, 1.4
    dAB = p_in - pA
    dBC = pC - p_out
    dreset = p_out - p_in
    direct = pC - pA
    omitted = dAB + dBC
    restored = dAB + dreset + dBC
    rho = 0.63
    h = np.diag([-math.exp(-2.0 * rho), math.exp(2.0 * rho)])
    recovered = 0.25 * math.log((-np.linalg.det(h)) / h[0, 0] ** 2)
    step = 1.0e-6
    phi_turn = lambda x: x * x
    endpoint_delta = phi_turn(1.0) - phi_turn(0.0)
    phi_dot_at_turn = (phi_turn(step) - phi_turn(-step)) / (2.0 * step)
    screen_log_area_dot = (
        math.log(np.linalg.det(math.exp(step) * np.eye(2)))
        - math.log(np.linalg.det(math.exp(-step) * np.eye(2)))
    ) / (2.0 * step)
    zero_rate_rejected = abs(phi_dot_at_turn) < 1.0e-12 and abs(screen_log_area_dot) > 1.0
    noninjective_turning = abs(phi_turn(-1.0) - phi_turn(1.0)) < 1.0e-15
    caustic = np.zeros((2, 2))
    caustic_inverse_rejected = False
    try:
        np.linalg.inv(caustic)
    except np.linalg.LinAlgError:
        caustic_inverse_rejected = True
    return {
        "reset_restored_residual": abs(restored - direct),
        "omitted_reset_nonzero": abs(omitted - direct) > 0.1,
        "pure_reciprocal_residual": abs(recovered - rho),
        "zero_rate_endpoint_delta": endpoint_delta,
        "zero_rate_phi_dot_residual": abs(phi_dot_at_turn),
        "zero_rate_screen_log_area_dot": screen_log_area_dot,
        "zero_rate_local_parameter_rejected": zero_rate_rejected,
        "noninjective_turning_depth": noninjective_turning,
        "caustic_determinant": float(np.linalg.det(caustic)),
        "caustic_inverse_rejected": caustic_inverse_rejected,
    }


def main() -> None:
    network = fraction_network_check()
    nonlinear = nonlinear_check()
    hostile = hostile_checks()
    checks = {
        "matrix_composition": network["matrix_composition_exact"],
        "scalar_composition": network["scalar_composition_residual"] < 1.0e-14,
        "reversal": network["reversal_residual"] < 1.0e-14,
        "character": network["character_residual"] < 1.0e-14,
        "terminal_phi": nonlinear["maximum_phi_recovery_residual"] < 1.0e-13,
        "nonlinear_join": nonlinear["maximum_finite_difference_join_residual"] < 1.0e-9,
        "atlas_independence": nonlinear["maximum_independent_atlas_residual"] < 1.0e-13,
        "middle_reset": hostile["reset_restored_residual"] < 1.0e-14
        and hostile["omitted_reset_nonzero"],
        "pure_reciprocal": hostile["pure_reciprocal_residual"] < 1.0e-14,
        "zero_rate_typed": abs(hostile["zero_rate_endpoint_delta"] - 1.0) < 1.0e-15
        and hostile["zero_rate_phi_dot_residual"] < 1.0e-12
        and abs(hostile["zero_rate_screen_log_area_dot"] - 2.0) < 1.0e-9
        and hostile["zero_rate_local_parameter_rejected"],
        "turning_depth_noninjective": hostile["noninjective_turning_depth"],
        "caustic_typed": abs(hostile["caustic_determinant"]) < 1.0e-15
        and hostile["caustic_inverse_rejected"],
    }
    result = {
        "schema": "UDT_G109_INDEPENDENT_JOIN_VERIFICATION_V1",
        "network": network,
        "nonlinear": nonlinear,
        "hostile": hostile,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
