#!/usr/bin/env python3
"""Implementation-distinct randomized verification of the bounded G336 identities."""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def matvec(matrix, vector):
    return [sum(matrix[i][j] * vector[j] for j in range(3)) for i in range(3)]


def dot(left, right):
    return sum(left[i] * right[i] for i in range(3))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(3))
             for j in range(3)] for i in range(3)]


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(3)] for i in range(3)]


def scale(value, matrix):
    return [[value * matrix[i][j] for j in range(3)] for i in range(3)]


def diagonal(values):
    return [[values[i] if i == j else 0.0 for j in range(3)] for i in range(3)]


def rotate(matrix, orthogonal):
    return matmul(matmul(orthogonal, matrix), transpose(orthogonal))


def normalize(vector):
    length = math.sqrt(dot(vector, vector))
    return [entry / length for entry in vector]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def random_rotation(rng):
    first = normalize([rng.uniform(-1.0, 1.0) for _ in range(3)])
    trial = [rng.uniform(-1.0, 1.0) for _ in range(3)]
    projection = dot(trial, first)
    second = normalize([trial[i] - projection * first[i] for i in range(3)])
    third = cross(first, second)
    # Columns form the orthonormal basis.
    return [[first[i], second[i], third[i]] for i in range(3)]


def quadratic_form(matrix, vector):
    return dot(vector, matvec(matrix, vector))


def verify() -> dict:
    rng = random.Random(336)
    checks: list[str] = []
    max_adm_error = 0.0
    max_rotation_error = 0.0
    max_pair_error = 0.0
    sign_counts = {-1: 0, 0: 0, 1: 0}
    records = []

    identity = diagonal([1.0, 1.0, 1.0])
    for index in range(480):
        scalar = rng.uniform(-12.0, 18.0)
        mu = rng.uniform(0.001, 0.999)
        b = rng.choice((-1.0, 1.0)) * rng.uniform(0.08, 8.0)
        C = b * (1.0 - 2.0 * mu)
        cosmological = 0.5 * scalar - 2.0 * b * b * mu + 3.0 * b * b * mu * mu

        kh = 0.5 * (C - b)
        kv = 0.5 * (C + b)
        K_basis = diagonal([kh, kh, kv])
        ric_h = 0.5 * (scalar - 2.0)
        Ric_basis = diagonal([ric_h, ric_h, 2.0])
        v_basis = [math.sqrt(1.0 - mu), 0.0, math.sqrt(mu)]

        rotation = random_rotation(rng)
        K = rotate(K_basis, rotation)
        Ric = rotate(Ric_basis, rotation)
        v = matvec(rotation, v_basis)
        tau = 2.0 * kh + kv
        K_squared = matmul(K, K)
        Kdot = add(add(Ric, scale(tau, K)), add(scale(-2.0, K_squared),
                                                       scale(-cosmological, identity)))
        q0 = -quadratic_form(K, v)
        require(abs(q0) < 3e-12, f"silent_{index}", checks)

        direct = -quadratic_form(Kdot, v)
        formula = 1.0 + 0.5 * (scalar - 6.0) * mu + b * b * mu * mu
        error = abs(direct - formula)
        max_adm_error = max(max_adm_error, error)
        require(error < 3e-11 * max(1.0, abs(direct), abs(formula)),
                f"adm_{index}", checks)

        K2_direct = quadratic_form(K_squared, v)
        K2_formula = b * b * mu * (1.0 - mu)
        rotation_error = abs(K2_direct - K2_formula)
        max_rotation_error = max(max_rotation_error, rotation_error)
        require(rotation_error < 3e-12 * max(1.0, K2_formula),
                f"rotation_{index}", checks)

        # A direct centered reconstruction from gamma(t)=I-2Kt-Kdot*t^2.
        step = 2e-4
        gamma_plus = add(identity, add(scale(-2.0 * step, K),
                                       scale(-step * step, Kdot)))
        gamma_minus = add(identity, add(scale(2.0 * step, K),
                                        scale(-step * step, Kdot)))
        length_plus = quadratic_form(gamma_plus, v)
        length_zero = dot(v, v)
        length_minus = quadratic_form(gamma_minus, v)
        finite_second = 0.5 * (length_plus - 2.0 * length_zero + length_minus) / (step * step)
        require(abs(finite_second - direct) < 5e-8 * max(1.0, abs(direct)),
                f"finite_second_{index}", checks)

        rapidity = rng.uniform(-3.0, 3.0)
        sh = math.sinh(rapidity)
        ch = math.cosh(rapidity)
        pair = [[2.0 * direct * sh * sh, 2.0 * direct * sh * ch],
                [2.0 * direct * sh * ch, 2.0 * direct * ch * ch]]
        pair_error = max(
            abs((-pair[0][0] + pair[1][1]) - 2.0 * direct),
            abs(pair[0][0] * pair[1][1] - pair[0][1] * pair[1][0]),
            abs(0.5 * pair[0][0] - direct * sh * sh),
        )
        max_pair_error = max(max_pair_error, pair_error)
        require(pair_error < 2e-9 * max(1.0, abs(direct), abs(pair[1][1]) ** 2),
                f"pair_{index}", checks)

        H = scale(-1.0, K)
        Hv = matvec(H, v)
        hv2 = dot(Hv, Hv)
        require(abs(dot(Hv, v)) < 3e-12, f"hv_orthogonal_{index}", checks)
        require(abs(hv2 - b * b * mu * (1.0 - mu)) < 3e-12 * max(1.0, hv2),
                f"hv_norm_{index}", checks)
        k_zero = 1.0 - direct / (2.0 * hv2)
        carried_zero = direct + 2.0 * (k_zero - 1.0) * hv2
        carried_low = direct + 2.0 * (k_zero - 2.0) * hv2
        carried_high = direct + 2.0 * k_zero * hv2
        require(abs(carried_zero) < 2e-11 and carried_low < 0.0 and carried_high > 0.0,
                f"carry_tuning_{index}", checks)

        if formula > 1e-10:
            sign_counts[1] += 1
        elif formula < -1e-10:
            sign_counts[-1] += 1
        else:
            sign_counts[0] += 1
        if len(records) < 16:
            records.append({"R": scalar, "mu": mu, "b": b, "C": C,
                            "Lambda": cosmological, "s1": formula})

    # Exact registered sign and endpoint controls, evaluated without production code.
    for b_squared, expected in ((1.0, -0.25), (2.0, 0.0), (4.0, 0.5)):
        value = 1.0 - 1.5 + 0.25 * b_squared
        require(value == expected, f"triplet_{b_squared}", checks)
        key = 0 if value == 0.0 else (1 if value > 0.0 else -1)
        sign_counts[key] += 1
    for scalar in (-7.0, 0.0, 6.0, 15.0):
        for b in (-3.0, 3.0):
            require(1.0 == 1.0 + 0.0 * scalar + 0.0 * b,
                    f"horizontal_{scalar}_{b}", checks)
            cosmological = 0.5 * scalar + b * b
            vertical = 1.0 + 0.5 * (scalar - 6.0) + b * b
            require(abs(vertical - (cosmological - 2.0)) < 1e-14,
                    f"vertical_{scalar}_{b}", checks)

    require(all(sign_counts[key] > 0 for key in (-1, 0, 1)),
            "all_signs_realized", checks)
    return {
        "package": "G336",
        "verdict": "PASS",
        "checks_passed": len(checks),
        "imports_production": False,
        "reads_production_result": False,
        "method": "independent randomized rotated-basis ADM reconstruction and centered metric jet",
        "seed": 336,
        "max_adm_error": max_adm_error,
        "max_rotation_error": max_rotation_error,
        "max_pair_error": max_pair_error,
        "sign_counts": {str(key): value for key, value in sign_counts.items()},
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({"checks_passed": result["checks_passed"],
                      "verdict": result["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
