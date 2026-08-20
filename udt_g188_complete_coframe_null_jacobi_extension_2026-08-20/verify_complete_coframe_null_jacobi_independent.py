#!/usr/bin/env python3
"""Independent exact-Fraction metric-jet replay for G188.

No SymPy and no production imports are used. The verifier reconstructs the
connection and Riemann tensor at the central null geodesic for random symmetric
complete-coframe mixing matrices.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import factorial
import json
import random


DIM = 4
TRIALS = 10_000
SEED = 1880820


def zeros(shape):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(shape[1:]) for _ in range(shape[0])]


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def matadd(left, right):
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def matscale(scale, matrix):
    return [[scale * value for value in row] for row in matrix]


def metric_jet(mixing):
    """Metric two-jet at x=y=0 for theta^A=dz^A+M^A_B z^B du."""
    metric = zeros((DIM, DIM))
    inverse = zeros((DIM, DIM))
    metric[0][1] = metric[1][0] = F(-1)
    inverse[0][1] = inverse[1][0] = F(-1)
    metric[2][2] = metric[3][3] = F(1)
    inverse[2][2] = inverse[3][3] = F(1)

    first = zeros((DIM, DIM, DIM))
    second = zeros((DIM, DIM, DIM, DIM))
    for i in range(2):
        for j in range(2):
            first[0][2 + i][2 + j] = mixing[i][j]
            first[2 + i][0][2 + j] = mixing[i][j]
    mtm = matmul([[mixing[j][i] for j in range(2)] for i in range(2)], mixing)
    for i in range(2):
        for j in range(2):
            second[0][0][2 + i][2 + j] = 2 * mtm[i][j]
    return metric, inverse, first, second


def connection_and_curvature(metric, inverse, first, second):
    gamma = zeros((DIM, DIM, DIM))
    d_inverse = zeros((DIM, DIM, DIM))
    for a in range(DIM):
        for e in range(DIM):
            for c in range(DIM):
                d_inverse[a][e][c] = -sum(
                    inverse[a][m] * first[m][n][c] * inverse[n][e]
                    for m in range(DIM) for n in range(DIM)
                )
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                gamma[a][b][c] = F(1, 2) * sum(
                    inverse[a][e] * (
                        first[e][c][b] + first[e][b][c] - first[b][c][e]
                    ) for e in range(DIM)
                )

    d_gamma = zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            for d in range(DIM):
                for c in range(DIM):
                    d_gamma[a][b][d][c] = F(1, 2) * sum(
                        d_inverse[a][e][c]
                        * (first[e][d][b] + first[e][b][d] - first[b][d][e])
                        + inverse[a][e]
                        * (second[e][d][b][c] + second[e][b][d][c]
                           - second[b][d][e][c])
                        for e in range(DIM)
                    )

    riemann = zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    riemann[a][b][c][d] = (
                        d_gamma[a][d][b][c] - d_gamma[a][c][b][d]
                        + sum(gamma[a][c][e] * gamma[e][d][b]
                              - gamma[a][d][e] * gamma[e][c][b]
                              for e in range(DIM))
                    )
    return gamma, riemann


def inner(metric, left, right):
    return sum(metric[a][b] * left[a] * right[b]
               for a in range(DIM) for b in range(DIM))


def tidal(metric, riemann, left, ray, right):
    return sum(
        metric[mu][a] * left[mu] * riemann[a][b][c][d]
        * ray[b] * right[c] * ray[d]
        for mu in range(DIM) for a in range(DIM)
        for b in range(DIM) for c in range(DIM) for d in range(DIM)
    )


def projector(metric, observer, ruler):
    pair = [[observer[a], ruler[a]] for a in range(DIM)]
    pair_inverse = [[F(-1), F(0)], [F(0), F(1)]]
    correction = zeros((DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            correction[a][b] = sum(
                pair[a][i] * pair_inverse[i][j] * pair[c][j] * metric[c][b]
                for i in range(2) for j in range(2) for c in range(DIM)
            )
    return [[F(int(a == b)) - correction[a][b] for b in range(DIM)]
            for a in range(DIM)]


def matvec(matrix, vector):
    return [sum(matrix[a][b] * vector[b] for b in range(len(vector)))
            for a in range(len(matrix))]


def random_nonzero_fraction(rng):
    numerator = 0
    while numerator == 0:
        numerator = rng.randint(-5, 5)
    return F(numerator, rng.randint(1, 6))


def trial(rng):
    a = F(rng.randint(-5, 5), rng.randint(1, 6))
    b = random_nonzero_fraction(rng)
    d = F(rng.randint(-5, 5), rng.randint(1, 6))
    if a + d == 0:
        d += F(1, 7)
    mixing = [[a, b], [b, d]]
    metric, inverse, first, second = metric_jet(mixing)
    gamma, riemann = connection_and_curvature(metric, inverse, first, second)

    ray = [F(1), F(0), F(0), F(0)]
    observer = [F(1, 2), F(1), F(0), F(0)]
    ruler = [ray[i] - observer[i] for i in range(DIM)]
    screen = ([F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)])

    assert inner(metric, ray, ray) == 0
    assert inner(metric, observer, observer) == -1
    assert inner(metric, observer, ray) == -1
    assert inner(metric, ruler, ruler) == 1
    assert all(inner(metric, vector, ray) == 0 for vector in screen)
    assert all(inner(metric, left, right) == F(int(i == j))
               for i, left in enumerate(screen) for j, right in enumerate(screen))
    assert all(gamma[a_index][0][0] == 0 for a_index in range(DIM))
    assert all(gamma[a_index][0][j] == 0
               for a_index in range(DIM) for j in (2, 3))

    actual = [[tidal(metric, riemann, left, ray, right) for right in screen]
              for left in screen]
    squared = matmul(mixing, mixing)
    expected = matscale(F(-1), squared)
    assert actual == expected
    assert actual[0][1] == actual[1][0]
    assert actual[0][1] != 0

    alpha, beta = random_nonzero_fraction(rng), random_nonzero_fraction(rng)
    gauged = ([screen[0][i] + alpha * ray[i] for i in range(DIM)],
              [screen[1][i] + beta * ray[i] for i in range(DIM)])
    gauged_tidal = [[tidal(metric, riemann, left, ray, right) for right in gauged]
                    for left in gauged]
    assert gauged_tidal == actual

    proj = projector(metric, observer, ruler)
    assert matvec(proj, observer) == [F(0)] * DIM
    assert matvec(proj, ruler) == [F(0)] * DIM
    assert matvec(proj, screen[0]) == screen[0]
    assert matvec(proj, screen[1]) == screen[1]
    assert sum(proj[i][i] for i in range(DIM)) == 2

    # Formal finite-map coefficients C_n=(-T)^n/(2n+1)! obey the matrix ODE.
    minus_tidal = matscale(F(-1), actual)
    power = [[F(1), F(0)], [F(0), F(1)]]
    coefficients = []
    for n in range(6):
        coefficients.append(matscale(F(1, factorial(2 * n + 1)), power))
        power = matmul(power, minus_tidal)
    for n in range(5):
        residual = matadd(
            matscale(F((2 * n + 3) * (2 * n + 2)), coefficients[n + 1]),
            matmul(actual, coefficients[n]),
        )
        assert residual == [[F(0), F(0)], [F(0), F(0)]]
    assert coefficients[0] == [[F(1), F(0)], [F(0), F(1)]]
    assert coefficients[1][0][1] == squared[0][1] / 6
    return 24


def named_controls():
    mixing = [[F(1), F(1)], [F(1), F(1)]]
    metric, inverse, first, second = metric_jet(mixing)
    _, riemann = connection_and_curvature(metric, inverse, first, second)
    ray = [F(1), F(0), F(0), F(0)]
    screen = ([F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)])
    actual = [[tidal(metric, riemann, left, ray, right) for right in screen]
              for left in screen]
    assert actual == [[F(-2), F(-2)], [F(-2), F(-2)]]

    flat_metric, flat_inverse, flat_first, flat_second = metric_jet(
        [[F(0), F(0)], [F(0), F(0)]]
    )
    _, flat_riemann = connection_and_curvature(
        flat_metric, flat_inverse, flat_first, flat_second
    )
    flat = [[tidal(flat_metric, flat_riemann, left, ray, right) for right in screen]
            for left in screen]
    assert flat == [[F(0), F(0)], [F(0), F(0)]]
    return {
        "flat_tidal": [[str(value) for value in row] for row in flat],
        "mixing_matrix": [[str(value) for value in row] for row in mixing],
        "mixing_tidal": [[str(value) for value in row] for row in actual],
        "finite_cross_series_leading_coefficient": "1/3",
    }


def main():
    rng = random.Random(SEED)
    assertions = 0
    for _ in range(TRIALS):
        assertions += trial(rng)
    controls = named_controls()
    print(json.dumps({
        "assertions": assertions,
        "audit": "G188_INDEPENDENT_EXACT_FRACTION_METRIC_JET_REPLAY",
        "controls": controls,
        "seed": SEED,
        "status": "PASS",
        "trials": TRIALS,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
