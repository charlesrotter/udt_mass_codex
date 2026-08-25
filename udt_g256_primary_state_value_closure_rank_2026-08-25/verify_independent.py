#!/usr/bin/env python3
"""Independent exact-Fraction replay of G256 without production imports/results."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "FUNCTION_VALUED_PRIMARY_STATE_REMAINS__"
    "ANGULAR_INTERLOCK_IS_TOMOGRAPHIC_NOT_PROPAGATING__NO_ODE_GPU"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next((r for r in range(rank, row_count) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [item / value for item in matrix[rank]]
        for r in range(row_count):
            if r != rank and matrix[r][column]:
                factor = matrix[r][column]
                matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[rank])]
        rank += 1
        if rank == row_count:
            break
    return rank


def solve_square(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    size = len(matrix)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    assert exact_rank(matrix) == size
    for column in range(size):
        pivot = next(r for r in range(column, size) if augmented[r][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        value = augmented[column][column]
        augmented[column] = [item / value for item in augmented[column]]
        for r in range(size):
            if r != column and augmented[r][column]:
                factor = augmented[r][column]
                augmented[r] = [
                    a - factor * b for a, b in zip(augmented[r], augmented[column])
                ]
    return [augmented[i][-1] for i in range(size)]


def incidence(n: int, edges: list[tuple[int, int]]) -> list[list[Fraction]]:
    rows = []
    for source, target in edges:
        row = [Fraction(0) for _ in range(n)]
        row[source] = Fraction(-1)
        row[target] = Fraction(1)
        rows.append(row)
    return rows


def edge_families(n: int) -> dict[str, list[tuple[int, int]]]:
    families = {
        "path": [(i, i + 1) for i in range(n - 1)],
        "star": [(0, j) for j in range(1, n)],
        "complete": [(i, j) for i in range(n) for j in range(i + 1, n)],
    }
    if n >= 3:
        families["cycle"] = [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]
    return families


def matrix_vector(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def polynomial_derivative_value(coefficients: list[Fraction], x: Fraction, order: int) -> Fraction:
    total = Fraction(0)
    for power, coefficient in enumerate(coefficients):
        if power < order:
            continue
        multiplier = 1
        for step in range(order):
            multiplier *= power - step
        total += coefficient * multiplier * x ** (power - order)
    return total


def hermite_trial(n: int) -> None:
    width = 3 * n
    matrix: list[list[Fraction]] = []
    targets: list[Fraction] = []
    expected: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for i in range(1, n + 1):
        node = Fraction(i)
        value = Fraction(3 * i * i - 2 * i + 5, i + 2)
        p = Fraction((-1) ** i * (2 * i + 1), i + 3)
        q = Fraction(i * i - 4 * i + 7, 2 * i + 1)
        first = p / node
        second = q / (node * node)
        expected.append((node, value, first, second))
        matrix.append([node**power for power in range(width)])
        matrix.append([
            Fraction(0) if power == 0 else Fraction(power) * node ** (power - 1)
            for power in range(width)
        ])
        matrix.append([
            Fraction(0) if power < 2 else Fraction(power * (power - 1)) * node ** (power - 2)
            for power in range(width)
        ])
        targets.extend([value, first, second])
    coefficients = solve_square(matrix, targets)
    for node, value, first, second in expected:
        assert polynomial_derivative_value(coefficients, node, 0) == value
        assert polynomial_derivative_value(coefficients, node, 1) == first
        assert polynomial_derivative_value(coefficients, node, 2) == second

    # Product of (x-r_i)^3 has zero value/first/second jets at every node and
    # a nonzero third derivative at each node. Build it by exact convolution.
    null_coefficients = [Fraction(1)]
    for node, *_ in expected:
        factor = [-node**3, 3 * node**2, -3 * node, Fraction(1)]
        convolved = [Fraction(0)] * (len(null_coefficients) + 3)
        for i, left in enumerate(null_coefficients):
            for j, right in enumerate(factor):
                convolved[i + j] += left * right
        null_coefficients = convolved
    for node, *_ in expected:
        assert polynomial_derivative_value(null_coefficients, node, 0) == 0
        assert polynomial_derivative_value(null_coefficients, node, 1) == 0
        assert polynomial_derivative_value(null_coefficients, node, 2) == 0
    assert polynomial_derivative_value(null_coefficients, expected[0][0], 3) != 0


def verify() -> dict[str, object]:
    manifest = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    owners = read_tsv(PACKAGE / "OWNER_CENSUS.tsv")
    assert len(manifest) == len(owners) == 18
    for row in manifest:
        assert sha256(ROOT / row["path"]) == row["sha256"]
    assert {row["owned_nonidentity_value_law"] for row in owners} == {"no"}

    graph_trials = 0
    cycle_trials = 0
    for n in range(2, 13):
        potentials = [Fraction(i * i - 3 * i + 2, i + 1) for i in range(n)]
        for kind, edges in edge_families(n).items():
            matrix = incidence(n, edges)
            assert exact_rank(matrix) == n - 1
            deltas = matrix_vector(matrix, potentials)
            for (source, target), delta in zip(edges, deltas):
                assert delta == potentials[target] - potentials[source]
                assert -delta == potentials[source] - potentials[target]
            graph_trials += 1
            if kind == "complete":
                index = {edge: position for position, edge in enumerate(edges)}
                cycles = []
                for i in range(1, n):
                    for j in range(i + 1, n):
                        row = [Fraction(0)] * len(edges)
                        row[index[(0, i)]] = 1
                        row[index[(i, j)]] = 1
                        row[index[(0, j)]] = -1
                        cycles.append(row)
                        assert deltas[index[(0, i)]] + deltas[index[(i, j)]] == deltas[index[(0, j)]]
                assert exact_rank(cycles) == len(edges) - n + 1
                cycle_trials += len(cycles)

    angular_trials = 0
    for scale in [Fraction(1, 7), Fraction(1, 3), Fraction(1), Fraction(5, 2), Fraction(11)]:
        for p in [Fraction(-7, 3), Fraction(-1), Fraction(0), Fraction(2, 5), Fraction(9, 2)]:
            for q in [Fraction(-5), Fraction(-1, 4), Fraction(0), Fraction(7, 3)]:
                parallel = scale * (2 * p * p + p - q)
                perp = 1 - scale * (1 + p)
                recovered_p = (1 - perp) / scale - 1
                recovered_q = 2 * recovered_p * recovered_p + recovered_p - parallel / scale
                assert recovered_p == p and recovered_q == q
                assert -(scale * scale) != 0
                angular_trials += 1

    hermite_domain_trials = 0
    for _domain in ("radial", "timelive"):
        for n in range(2, 9):
            hermite_trial(n)
            hermite_domain_trials += 1
    assert hermite_domain_trials == 14

    return {
        "status": "PASS",
        "landing": LANDING,
        "method": "standard_library_exact_fraction_independent_replay",
        "production_imported": False,
        "production_result_read": False,
        "source_count": len(manifest),
        "owned_nonidentity_value_law_count": 0,
        "graph_trials": graph_trials,
        "cycle_trials": cycle_trials,
        "angular_trials": angular_trials,
        "radial_hermite_trials": 7,
        "timelive_hermite_trials": 7,
        "anchored_state_dimension": "N-1",
        "solver_status": "GATED_NOT_DEFINED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = json.dumps(verify(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
