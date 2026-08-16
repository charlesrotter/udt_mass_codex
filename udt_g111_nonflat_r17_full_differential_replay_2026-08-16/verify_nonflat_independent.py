#!/usr/bin/env python3
"""Independent finite-difference moving-frame replay of the G111 optical atlas."""

from __future__ import annotations

import csv
import json
import math
from itertools import product
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
LAMBDAS = (-2.0, -1.0, 0.0, 0.5, 1.0, 2.0)
BASE_UNITS = (
    np.array([0.0, 0.0, 0.0, 1.0]),  # Z=k
    np.array([0.0, 1.0, 0.0, 0.0]),  # X=i
    np.array([0.0, 0.0, 1.0, 0.0]),  # Y=j
)


def qmul(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    w, x, y, z = left
    a, b, c, d = right
    return np.array(
        [w * a - x * b - y * c - z * d,
         w * b + x * a + y * d - z * c,
         w * c - x * d + y * a + z * b,
         w * d + x * c - y * b + z * a]
    )


def move(q: np.ndarray, direction: np.ndarray, step: float) -> np.ndarray:
    norm = float(np.linalg.norm(direction[1:]))
    if norm == 0.0:
        return q.copy()
    unit = direction / norm
    rotor = np.concatenate(([math.cos(step * norm)], math.sin(step * norm) * unit[1:]))
    answer = qmul(q, rotor)
    return answer / np.linalg.norm(answer)


def frame(q: np.ndarray, epsilon: float, twist: float, lam: float) -> np.ndarray:
    phi = epsilon * q[0]
    u = math.exp(phi)
    v = math.exp(lam * phi)
    return np.array(
        [[u, -twist / u, 0.0, 0.0],
         [0.0, 1.0 / u, 0.0, 0.0],
         [0.0, 0.0, 1.0 / v, 0.0],
         [0.0, 0.0, 0.0, 1.0 / v]],
        dtype=float,
    )


def base_constants() -> np.ndarray:
    constants = np.zeros((4, 4, 4), dtype=float)
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left, right, output] = 2.0
        constants[right, left, output] = -2.0
    return constants


def frame_partials(q: np.ndarray, epsilon: float, twist: float, lam: float, step: float) -> np.ndarray:
    derivatives = np.zeros((4, 4, 4), dtype=float)
    for base_index, unit in enumerate(BASE_UNITS, start=1):
        plus = frame(move(q, unit, step), epsilon, twist, lam)
        minus = frame(move(q, unit, -step), epsilon, twist, lam)
        derivatives[base_index] = (plus - minus) / (2.0 * step)
    return derivatives


def brackets(q: np.ndarray, epsilon: float, twist: float, lam: float, step: float) -> np.ndarray:
    basis = frame(q, epsilon, twist, lam)
    inverse = np.linalg.inv(basis)
    derivatives = frame_partials(q, epsilon, twist, lam, step)
    constants = base_constants()
    result = np.zeros((4, 4, 4), dtype=float)
    for left, right in product(range(4), repeat=2):
        in_base = np.zeros(4)
        for output in range(4):
            for direction in range(4):
                in_base[output] += basis[direction, left] * derivatives[direction, output, right]
                in_base[output] -= basis[direction, right] * derivatives[direction, output, left]
            in_base[output] += np.einsum("i,j,ij", basis[:, left], basis[:, right], constants[:, :, output])
        result[left, right] = inverse @ in_base
    return result


def connection(q: np.ndarray, epsilon: float, twist: float, lam: float, inner_step: float) -> tuple[np.ndarray, np.ndarray]:
    structure = brackets(q, epsilon, twist, lam, inner_step)
    gamma = np.zeros((4, 4, 4), dtype=float)
    signature = np.diag(ETA)
    for direction, vector, output in product(range(4), repeat=3):
        lower = (
            signature[output] * structure[direction, vector, output]
            - signature[direction] * structure[vector, output, direction]
            + signature[vector] * structure[output, direction, vector]
        ) / 2.0
        gamma[direction, vector, output] = signature[output] * lower
    return gamma, structure


def riemann(q: np.ndarray, epsilon: float, twist: float, lam: float, outer_step: float, inner_step: float) -> tuple[np.ndarray, np.ndarray]:
    basis = frame(q, epsilon, twist, lam)
    gamma, structure = connection(q, epsilon, twist, lam, inner_step)
    base_derivative = np.zeros((4, 4, 4, 4), dtype=float)
    for base_index, unit in enumerate(BASE_UNITS, start=1):
        plus, _ = connection(move(q, unit, outer_step), epsilon, twist, lam, inner_step)
        minus, _ = connection(move(q, unit, -outer_step), epsilon, twist, lam, inner_step)
        base_derivative[base_index] = (plus - minus) / (2.0 * outer_step)
    frame_derivative = np.einsum("bi,bjkl->ijkl", basis, base_derivative)
    upper = np.zeros((4, 4, 4, 4), dtype=float)
    for left, right, vector, output in product(range(4), repeat=4):
        value = frame_derivative[left, right, vector, output] - frame_derivative[right, left, vector, output]
        value += sum(gamma[right, vector, middle] * gamma[left, middle, output] for middle in range(4))
        value -= sum(gamma[left, vector, middle] * gamma[right, middle, output] for middle in range(4))
        value -= sum(structure[left, right, middle] * gamma[middle, vector, output] for middle in range(4))
        upper[left, right, vector, output] = value
    return upper * np.diag(ETA)[None, None, None, :], gamma


def screen(axis: int, sign: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = np.zeros(3)
    n[axis] = float(sign)
    if axis == 0:
        return n, np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, float(sign)])
    if axis == 1:
        return n, np.array([0.0, 0.0, 1.0]), np.array([float(sign), 0.0, 0.0])
    return n, np.array([1.0, 0.0, 0.0]), np.array([0.0, float(sign), 0.0])


def optical(tensor: np.ndarray, n: np.ndarray, first: np.ndarray, second: np.ndarray) -> np.ndarray:
    k = np.concatenate(([1.0], n))
    screens = (np.concatenate(([0.0], first)), np.concatenate(([0.0], second)))
    answer = np.empty((2, 2), dtype=float)
    for i, one in enumerate(screens):
        for j, two in enumerate(screens):
            answer[i, j] = np.einsum("a,b,c,d,abcd", one, k, k, two, tensor)
    return answer


def main() -> None:
    with (HERE / "CONTROL_ATLAS.tsv").open(newline="") as handle:
        production = list(csv.DictReader(handle, delimiter="\t"))
    by_key = {
        (row["epsilon"], row["twist_a"], row["lambda_R"], row["point_id"], row["sky_axis"]): row
        for row in production
    }
    points = tuple(np.array((0.5, *(0.5 * sign for sign in signs))) for signs in product((-1, 1), repeat=3))
    max_trace = 0.0
    max_det = 0.0
    max_norm = 0.0
    max_symmetry = 0.0
    max_phi_linear = 0.0
    max_pair_quadratic = 0.0
    max_pair_screen = 0.0
    comparisons = 0
    for epsilon, twist, lam, point_index in product((-0.2, 0.2), (-0.25, 0.25), LAMBDAS, range(8)):
        tensor, gamma = riemann(points[point_index], epsilon, twist, lam, outer_step=2.0e-5, inner_step=2.0e-6)
        for axis, sign in product(range(3), (-1, 1)):
            n, first, second = screen(axis, sign)
            tidal = optical(tensor, n, first, second)
            label = f"{'+' if sign > 0 else '-'}e{axis + 1}"
            key = (str(int(epsilon * 5)) + "/5", str(int(twist * 4)) + "/4", str(int(lam)) if lam.is_integer() else "1/2", f"P{point_index + 1:02d}", label)
            row = by_key[key]
            max_trace = max(max_trace, abs(float(row["tidal_trace"]) - float(np.trace(tidal))))
            max_det = max(max_det, abs(float(row["tidal_det"]) - float(np.linalg.det(tidal))))
            max_norm = max(max_norm, abs(float(row["tidal_frobenius"]) - float(np.linalg.norm(tidal))))
            max_symmetry = max(max_symmetry, float(np.max(np.abs(tidal - tidal.T))))
            observer = np.array([1.0, 0.0, 0.0, 0.0])
            null = np.concatenate(([1.0], n))
            metric = ETA
            initial = np.einsum("i,j,ijk->k", observer, null, gamma)
            curvature_covector = np.einsum("i,j,k,ijkl->l", observer, null, null, tensor)
            curvature_vector = np.diag(metric) * curvature_covector
            pair_quadratic_vector = -curvature_vector / 2.0
            h00_linear = 2.0 * observer @ metric @ initial
            h00_quadratic = initial @ metric @ initial + 2.0 * observer @ metric @ pair_quadratic_vector
            phi_linear = h00_linear / 2.0
            screen4 = (np.concatenate(([0.0], first)), np.concatenate(([0.0], second)))
            pair_screen = np.array([initial @ metric @ basis for basis in screen4])
            max_phi_linear = max(max_phi_linear, abs(float(row["phi_pair_linear"]) - float(phi_linear)))
            max_pair_quadratic = max(max_pair_quadratic, abs(float(row["pair_h00_quadratic"]) - float(h00_quadratic)))
            max_pair_screen = max(max_pair_screen, abs(float(row["pair_screen_leading_norm"]) - float(np.linalg.norm(pair_screen))))
            comparisons += 1
    tolerances = {"trace": 2.0e-5, "det": 2.0e-4, "norm": 2.0e-5, "symmetry": 2.0e-5, "pair": 2.0e-5}
    checks = {
        "all_1152_rows_compared": comparisons == 1152,
        "trace_agrees": max_trace < tolerances["trace"],
        "determinant_agrees": max_det < tolerances["det"],
        "norm_agrees": max_norm < tolerances["norm"],
        "optical_symmetry": max_symmetry < tolerances["symmetry"],
        "phi_pair_linear_agrees": max_phi_linear < tolerances["pair"],
        "pair_quadratic_agrees": max_pair_quadratic < tolerances["pair"],
        "pair_screen_agrees": max_pair_screen < tolerances["pair"],
        "does_not_import_production": True,
        "finite_difference_moving_frame_route": True,
    }
    result = {
        "schema": "UDT_G111_INDEPENDENT_MOVING_FRAME_V1",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "comparisons": comparisons,
        "maximum_absolute_residuals": {"trace": max_trace, "determinant": max_det, "frobenius": max_norm, "symmetry": max_symmetry, "phi_pair_linear": max_phi_linear, "pair_h00_quadratic": max_pair_quadratic, "pair_screen_norm": max_pair_screen},
        "tolerances": tolerances,
        "method": "numpy finite-difference quaternion-flow brackets and connection derivatives; no production import",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if not result["all_checks_pass"]:
        raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
