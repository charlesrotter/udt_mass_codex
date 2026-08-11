#!/usr/bin/env python3
"""Independent Fraction/dual-number verification with no SymPy or production import."""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 10


@dataclass(frozen=True)
class Dual:
    value: F
    grad: tuple[F, ...]

    @classmethod
    def basis(cls, value: int, index: int) -> "Dual":
        return cls(F(value), tuple(F(int(i == index)) for i in range(N)))

    def __add__(self, other: object) -> "Dual":
        rhs = other if isinstance(other, Dual) else Dual(F(other), (F(0),) * N)
        return Dual(self.value + rhs.value, tuple(a + b for a, b in zip(self.grad, rhs.grad)))

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value, tuple(-a for a in self.grad))

    def __sub__(self, other: object) -> "Dual":
        return self + (-other if isinstance(other, Dual) else -F(other))

    def __rsub__(self, other: object) -> "Dual":
        return (-self) + other

    def __mul__(self, other: object) -> "Dual":
        rhs = other if isinstance(other, Dual) else Dual(F(other), (F(0),) * N)
        return Dual(
            self.value * rhs.value,
            tuple(self.value * b + rhs.value * a for a, b in zip(self.grad, rhs.grad)),
        )

    __rmul__ = __mul__


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant(matrix: list[list[F]]) -> F:
    work = [row[:] for row in matrix]
    result = F(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            ratio = work[row][column] / value
            for j in range(column, len(work)):
                work[row][j] -= ratio * work[column][j]
    return result


def inv2(matrix):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return [[matrix[1][1] / det, -matrix[0][1] / det],
            [-matrix[1][0] / det, matrix[0][0] / det]]


def metric_map(values):
    T, L, beta, u, v, w, s00, s01, s10, s11 = values
    zero = T * 0
    B = [[T, T * beta], [zero, L]]
    Q = [[u, zero], [v, w]]
    S = [[s00, s01], [s10, s11]]
    QS = matmul(Q, S)
    E = [B[0] + [zero, zero], B[1] + [zero, zero], QS[0] + Q[0], QS[1] + Q[1]]
    eta_E = [[(-1 if i == 0 else 1) * E[i][j] for j in range(4)] for i in range(4)]
    g = matmul(transpose(E), eta_E)
    return g


def selected(g):
    return [g[0][0], g[0][1], g[1][1], g[0][2], g[0][3],
            g[1][2], g[1][3], g[2][2], g[2][3], g[3][3]]


def sub2(left, right):
    return [[left[i][j] - right[i][j] for j in range(2)] for i in range(2)]


def verify(seed: int = 20260810, trials: int = 300) -> dict[str, object]:
    rng = random.Random(seed)
    for _ in range(trials):
        raw = [rng.randint(1, 5), rng.randint(1, 5), rng.randint(-3, 3),
               rng.randint(1, 5), rng.randint(-3, 3), rng.randint(1, 5),
               *[rng.randint(-3, 3) for _ in range(4)]]
        duals = [Dual.basis(value, i) for i, value in enumerate(raw)]
        outputs = selected(metric_map(duals))
        jacobian = [list(output.grad) for output in outputs]
        T, L, _, u, _, w, *_ = map(F, raw)
        assert determinant(jacobian) == 16 * L * T**3 * u**5 * w**6

        g = metric_map(list(map(F, raw)))
        H = [[g[2][2], g[2][3]], [g[3][2], g[3][3]]]
        C = [[g[0][2], g[0][3]], [g[1][2], g[1][3]]]
        base = [[g[0][0], g[0][1]], [g[1][0], g[1][1]]]
        schur = sub2(base, matmul(matmul(C, inv2(H)), transpose(C)))
        T0, L0, beta0, u0, v0, w0, s00, s01, s10, s11 = map(F, raw)
        det_h = H[0][0] * H[1][1] - H[0][1] ** 2
        det_a = schur[0][0] * schur[1][1] - schur[0][1] ** 2
        assert -schur[0][0] == T0**2
        assert schur[0][1] / schur[0][0] == beta0
        assert det_a / schur[0][0] == L0**2
        assert H[1][1] == w0**2
        assert H[0][1] / w0 == v0
        assert det_h / H[1][1] == u0**2
        assert matmul(inv2(H), transpose(C)) == [[s00, s01], [s10, s11]]

    for _ in range(trials):
        f0, f1, f2 = (F(rng.randint(-20, 20), rng.randint(1, 9)) for _ in range(3))
        assert (f1 - f0) + (f2 - f1) == f2 - f0

    for _ in range(trials):
        t = F(rng.randint(0, 100), 100)
        epsilon = F(rng.randint(-10, 10), 20)
        chi = t**2 * (1 - t)**2
        spatial = 1 + epsilon * chi
        assert spatial > 0
        assert (t not in (0, 1)) or spatial == 1

    return {
        "status": "PASS",
        "implementation": "independent_standard_library_fraction_dual_numbers_no_sympy_no_production_import",
        "exact_jacobian_and_inverse_trials": trials,
        "endpoint_cocycle_trials": trials,
        "boundary_preserving_interior_trials": trials,
        "total_exact_trials": 3 * trials,
        "genuine_owned_history_restrictions": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    result = verify()
    if not args.read_only:
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
