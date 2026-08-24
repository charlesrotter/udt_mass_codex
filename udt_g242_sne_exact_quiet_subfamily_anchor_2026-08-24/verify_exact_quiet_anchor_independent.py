#!/usr/bin/env python3
"""Independent 80-digit G242 replay without importing production code."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
STATE_PATH = ROOT / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
OUTPUT_PATH = PACKAGE / "INDEPENDENT_VERIFICATION.json"


def number(value: object) -> mp.mpf:
    return mp.mpf(str(value))


def cholesky(matrix: list[list[mp.mpf]]) -> list[list[mp.mpf]]:
    size = len(matrix)
    lower = [[mp.mpf("0") for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1):
            value = matrix[i][j] - mp.fsum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value <= 0:
                    raise RuntimeError("covariance is not positive definite")
                lower[i][j] = mp.sqrt(value)
            else:
                lower[i][j] = value / lower[j][j]
    return lower


def cholesky_solve(lower: list[list[mp.mpf]], rhs: list[mp.mpf]) -> list[mp.mpf]:
    size = len(rhs)
    forward = [mp.mpf("0") for _ in range(size)]
    for i in range(size):
        forward[i] = (rhs[i] - mp.fsum(lower[i][j] * forward[j] for j in range(i))) / lower[i][i]
    solution = [mp.mpf("0") for _ in range(size)]
    for i in range(size - 1, -1, -1):
        solution[i] = (
            forward[i] - mp.fsum(lower[j][i] * solution[j] for j in range(i + 1, size))
        ) / lower[i][i]
    return solution


def chi_square_quantile(probability: mp.mpf, dof: int) -> mp.mpf:
    shape = mp.mpf(dof) / 2

    def cdf(value: mp.mpf) -> mp.mpf:
        return mp.gammainc(shape, 0, value / 2, regularized=True)

    low = mp.mpf("0")
    high = mp.mpf(max(1, dof))
    while cdf(high) < probability:
        high *= 2
    for _ in range(300):
        middle = (low + high) / 2
        if cdf(middle) < probability:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def evaluate() -> dict[str, object]:
    mp.mp.dps = 80
    document = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    state = document["state"]
    knots = [number(value) for value in state["knots"]]
    observed = [number(value) for value in state["theta"]]
    covariance = [[number(value) for value in row] for row in state["theta_covariance"]]
    phi_anchor = knots[0]
    denominator = 1 - mp.exp(-2 * phi_anchor)
    predicted = [
        mp.mpf("2.5") * mp.log10((1 - mp.exp(-2 * phi)) / denominator) for phi in knots[1:]
    ]
    residual = [left - right for left, right in zip(observed, predicted)]
    lower = cholesky(covariance)
    solved = cholesky_solve(lower, residual)
    chi2 = mp.fsum(left * right for left, right in zip(residual, solved))
    ceiling = chi_square_quantile(mp.mpf("0.999"), len(observed))

    maximum_abs_j = mp.mpf("0")
    minimum_s_prime = mp.inf
    maximum_q_identity_error = mp.mpf("0")
    count = 4097
    for index in range(count):
        phi = knots[0] + (knots[-1] - knots[0]) * mp.mpf(index) / (count - 1)
        p = mp.exp(2 * phi) - 1
        s_prime = 1 / p
        s_second = -2 * mp.exp(2 * phi) / (p * p)
        q = -(s_second + s_prime * s_prime) / (s_prime**3)
        tidal = mp.exp(-2 * phi) * (2 * p * p - q + 2 * p) - (1 - mp.exp(-2 * phi))
        minimum_s_prime = min(minimum_s_prime, s_prime)
        maximum_abs_j = max(maximum_abs_j, abs(tidal))
        maximum_q_identity_error = max(maximum_q_identity_error, abs(q - (2 * p * p + p)))

    classification = (
        "EXACT_QUIET_SUBFAMILY_COMPATIBLE_WITH_FROZEN_SNE_STATE"
        if chi2 <= ceiling
        else "EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN"
    )
    return {
        "classification": classification,
        "chi2": mp.nstr(chi2, 60),
        "dof": len(observed),
        "chi2_ceiling_0p999": mp.nstr(ceiling, 60),
        "predicted_theta": [mp.nstr(value, 60) for value in predicted],
        "minimum_s_prime": mp.nstr(minimum_s_prime, 60),
        "maximum_abs_J": mp.nstr(maximum_abs_j, 20),
        "maximum_abs_q_identity_error": mp.nstr(maximum_q_identity_error, 20),
        "precision_digits": mp.mp.dps,
        "boss_outcomes": "CLOSED_AND_UNREAD",
        "independence": "NO_PRODUCTION_IMPORT_OR_OUTPUT_READ",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
