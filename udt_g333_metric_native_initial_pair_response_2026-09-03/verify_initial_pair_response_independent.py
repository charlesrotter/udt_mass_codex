#!/usr/bin/env python3
"""Implementation-distinct rotated-matrix verification of the G333 response."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def matvec(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(len(vector)))
            for i in range(len(matrix))]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def outer(left, right):
    return [[a * b for b in right] for a in left]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(3)] for i in range(3)]


def scale(value, matrix):
    return [[value * matrix[i][j] for j in range(3)] for i in range(3)]


def trace(matrix):
    return sum(matrix[i][i] for i in range(3))


def frobenius_squared(matrix):
    return sum(matrix[i][j] * matrix[i][j] for i in range(3) for j in range(3))


def close(left, right, tolerance=2e-12):
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()

    # Rational orthogonal matrix. Its third column hides the preferred direction from the basis.
    rotation = [
        [3 / 5, -4 / 5, 0.0],
        [16 / 25, 12 / 25, -3 / 5],
        [12 / 25, 9 / 25, 4 / 5],
    ]
    identity = [[float(i == j) for j in range(3)] for i in range(3)]
    rotated_identity = multiply(transpose(rotation), rotation)
    if any(not close(rotated_identity[i][j], identity[i][j])
           for i in range(3) for j in range(3)):
        raise AssertionError("independent rotation is not orthogonal")
    xi = [rotation[i][2] for i in range(3)]
    projector = outer(xi, xi)

    checks = ["rotation_orthogonal"]
    records = []
    directions = (
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [3 / 5, 4 / 5, 0.0],
        [4 / 5, 0.0, 3 / 5],
    )
    cases = (
        (12.0, -2.0, -20.0),
        (138 / 7, 3.0, 20.0),
        (28 / 3, 11.0, -20.0),
        (352 / 43, 3.0, 20.0),
        (6.0, 11.0, -20.0),
    )

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for case_index, (scalar_r, cosmological_lambda, constant_c) in enumerate(cases):
        q = 2 * (scalar_r + 2 * constant_c**2 - 2 * cosmological_lambda)
        require(q > 0, f"case_{case_index}_strict_radicand")
        for branch in (-1, 1):
            b = -constant_c + branch * math.sqrt(q)
            a = (constant_c - b) / 2
            k = add(scale(a, identity), scale(b, projector))
            h = scale(-1, k)

            tr_h = trace(h)
            mean = tr_h / 3
            shear = add(h, scale(-mean, identity))
            require(close(tr_h, (b - 3 * constant_c) / 2),
                    f"case_{case_index}_{branch}_trace")
            require(close(trace(shear), 0), f"case_{case_index}_{branch}_shear_trace")
            require(close(frobenius_squared(shear), 2 * b * b / 3),
                    f"case_{case_index}_{branch}_shear_norm")

            tau = trace(k)
            hamiltonian = scalar_r + tau * tau - frobenius_squared(k)
            require(close(hamiltonian, 2 * cosmological_lambda),
                    f"case_{case_index}_{branch}_hamiltonian")

            for direction_index, raw_v in enumerate(directions):
                norm = math.sqrt(dot(raw_v, raw_v))
                v = [entry / norm for entry in raw_v]
                mu = dot(v, xi) ** 2
                rate_matrix = dot(v, matvec(h, v))
                rate_scalar = (b - constant_c) / 2 - b * mu
                require(close(rate_matrix, rate_scalar),
                        f"case_{case_index}_{branch}_direction_{direction_index}")

                # Reconstruct from a centered first difference of gamma(t)=I+2tH.
                epsilon = 1e-7
                gamma_plus = add(identity, scale(2 * epsilon, h))
                gamma_minus = add(identity, scale(-2 * epsilon, h))
                length2_plus = dot(v, matvec(gamma_plus, v))
                length2_minus = dot(v, matvec(gamma_minus, v))
                finite_rate = (length2_plus - length2_minus) / (4 * epsilon)
                require(close(finite_rate, rate_matrix, 2e-8),
                        f"case_{case_index}_{branch}_finite_jet_{direction_index}")
                records.append({
                    "case": case_index,
                    "branch": branch,
                    "direction": direction_index,
                    "mu": mu,
                    "matrix_rate": rate_matrix,
                })

    payload = {
        "package": "G333",
        "verifier": "independent_rotated_matrix_and_centered_first_jet",
        "imports_production": False,
        "reads_production_result": False,
        "checks_passed": len(checks),
        "checks": checks,
        "records": records,
        "verdict": "PASS",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks_passed": len(checks), "verdict": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
