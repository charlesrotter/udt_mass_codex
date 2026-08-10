#!/usr/bin/env python3
"""Git-free exact Fraction/second-jet reconstruction of the complete H connection."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 4


@dataclass(frozen=True)
class J1:
    value: Q
    gradient: tuple[Q, ...] = (Q(0),) * N

    @staticmethod
    def make(value: "J1 | Q | int") -> "J1":
        return value if isinstance(value, J1) else J1(Q(value))

    def __add__(self, other):
        other = J1.make(other)
        return J1(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self):
        return J1(-self.value, tuple(-x for x in self.gradient))

    def __sub__(self, other):
        return self + (-J1.make(other))

    def __rsub__(self, other):
        return J1.make(other) - self

    def __mul__(self, other):
        other = J1.make(other)
        return J1(
            self.value * other.value,
            tuple(a * other.value + self.value * b for a, b in zip(self.gradient, other.gradient)),
        )

    __rmul__ = __mul__

    def reciprocal(self):
        return J1(1 / self.value, tuple(-x / (self.value * self.value) for x in self.gradient))

    def __truediv__(self, other):
        return self * J1.make(other).reciprocal()

    def __rtruediv__(self, other):
        return J1.make(other) / self


@dataclass(frozen=True)
class J2:
    value: Q
    gradient: tuple[Q, ...] = (Q(0),) * N
    hessian: tuple[tuple[Q, ...], ...] = ((Q(0),) * N,) * N

    @staticmethod
    def make(value: "J2 | Q | int") -> "J2":
        return value if isinstance(value, J2) else J2(Q(value))

    def __add__(self, other):
        other = J2.make(other)
        return J2(
            self.value + other.value,
            tuple(a + b for a, b in zip(self.gradient, other.gradient)),
            tuple(tuple(a + b for a, b in zip(row_a, row_b)) for row_a, row_b in zip(self.hessian, other.hessian)),
        )

    __radd__ = __add__

    def __neg__(self):
        return J2(-self.value, tuple(-x for x in self.gradient), tuple(tuple(-x for x in row) for row in self.hessian))

    def __sub__(self, other):
        return self + (-J2.make(other))

    def __rsub__(self, other):
        return J2.make(other) - self

    def __mul__(self, other):
        other = J2.make(other)
        gradient = tuple(a * other.value + self.value * b for a, b in zip(self.gradient, other.gradient))
        hessian = tuple(
            tuple(
                self.hessian[i][j] * other.value
                + self.gradient[j] * other.gradient[i]
                + self.gradient[i] * other.gradient[j]
                + self.value * other.hessian[i][j]
                for j in range(N)
            )
            for i in range(N)
        )
        return J2(self.value * other.value, gradient, hessian)

    __rmul__ = __mul__

    def reciprocal(self):
        gradient = tuple(-x / (self.value * self.value) for x in self.gradient)
        hessian = tuple(
            tuple(
                -self.hessian[i][j] / (self.value * self.value)
                + 2 * self.gradient[i] * self.gradient[j] / (self.value * self.value * self.value)
                for j in range(N)
            )
            for i in range(N)
        )
        return J2(1 / self.value, gradient, hessian)

    def __truediv__(self, other):
        return self * J2.make(other).reciprocal()

    def __rtruediv__(self, other):
        return J2.make(other) / self


def first(value: J2) -> J1:
    return J1(value.value, value.gradient)


def derivative(value: J2, direction: int) -> J1:
    return J1(value.gradient[direction], tuple(value.hessian[i][direction] for i in range(N)))


def inverse(matrix):
    n = len(matrix)
    augmented = [row[:] + [J2.make(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column].value != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [augmented[row][j] - factor * augmented[column][j] for j in range(2 * n)]
    return [row[n:] for row in augmented]


def scalar_scale(value: Q, coefficient: Q, p, q):
    gradient = tuple(coefficient * value * p[i] for i in range(N))
    hessian = tuple(
        tuple(coefficient * value * (coefficient * p[i] * p[j] + q[i][j]) for j in range(N))
        for i in range(N)
    )
    return J2(value, gradient, hessian)


def witness(lam: Q, mc_sign: int) -> dict[str, bool]:
    u0 = Q(4)
    v0 = {Q(-2): Q(1, 16), Q(-1): Q(1, 4), Q(0): Q(1), Q(1, 2): Q(2), Q(1): Q(4), Q(2): Q(16)}[lam]
    a0 = Q(1, 64)
    p1, p2, p3 = Q(3, 50), Q(1, 50), Q(2, 50)
    q11, q21, q31, q22, q32, q33 = Q(7, 13), Q(-5, 17), Q(11, 19), Q(13, 23), Q(-17, 29), Q(19, 31)
    p = (Q(0), p1, p2, p3)
    eps = Q(mc_sign)
    q = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(0), q11, q21 + 2 * eps * p3, q31 - 2 * eps * p2),
        (Q(0), q21, q22, q32 + 2 * eps * p1),
        (Q(0), q31, q32, q33),
    )
    u = scalar_scale(u0, Q(1), p, q)
    v = scalar_scale(v0, lam, p, q)
    a = J2.make(a0)
    z = J2.make(0)
    coframe = [[1 / u, a / u, z, z], [z, u, z, z], [z, z, v, z], [z, z, z, v]]
    frame = inverse(coframe)
    constants = [[[Q(0) for _ in range(N)] for _ in range(N)] for _ in range(N)]
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = 2 * eps
        constants[right][left][output] = -2 * eps

    frame_first = [[first(entry) for entry in row] for row in frame]
    coframe_first = [[first(entry) for entry in row] for row in coframe]

    def bracket(left, right):
        base = []
        for output in range(N):
            value = J1.make(0)
            for direction in range(N):
                value += frame_first[direction][left] * derivative(frame[output][right], direction)
                value -= frame_first[direction][right] * derivative(frame[output][left], direction)
            for one in range(N):
                for two in range(N):
                    value += frame_first[one][left] * frame_first[two][right] * constants[one][two][output]
            base.append(value)
        return [sum((coframe_first[row][column] * base[column] for column in range(N)), J1.make(0)) for row in range(N)]

    brackets = [[bracket(i, j) for j in range(N)] for i in range(N)]
    eta = (-1, 1, 1, 1)

    def inner(vector, basis):
        return eta[basis] * vector[basis]

    def gamma(direction, vector, output):
        return (inner(brackets[direction][vector], output) - inner(brackets[vector][output], direction) + inner(brackets[output][direction], vector)) / 2

    connection = [gamma(direction, 2, 3) for direction in range(N)]
    curvature = {}
    for left in range(N):
        for right in range(left + 1, N):
            curvature[(left, right)] = (
                sum((frame[base][left].value * connection[right].gradient[base] for base in range(N)), Q(0))
                - sum((frame[base][right].value * connection[left].gradient[base] for base in range(N)), Q(0))
                - sum((brackets[left][right][index].value * connection[index].value for index in range(N)), Q(0))
            )

    expected_connection = (
        eps * a0 / (u0 * v0 * v0),
        eps * (2 / u0 - u0 / (v0 * v0)),
        -lam * p3 / v0,
        lam * p2 / v0,
    )
    expected_curvature = {
        (0, 1): 2 * eps * a0 * (1 + lam) * p1 / (u0 * u0 * v0 * v0),
        (0, 2): 2 * eps * a0 * (1 + lam) * p2 / (u0 * v0**3),
        (0, 3): 2 * eps * a0 * (1 + lam) * p3 / (u0 * v0**3),
        (1, 2): 2 * eps * (1 - lam) * p2 * u0 / v0**3 - lam * q31 / (u0 * v0),
        (1, 3): 2 * eps * (1 - lam) * p3 * u0 / v0**3 + lam * q21 / (u0 * v0),
        (2, 3): lam * (q22 + q33) / (v0 * v0) + 2 * u0 * u0 / v0**4 - 4 / (v0 * v0) - 2 * a0 * a0 / (u0 * u0 * v0**4),
    }
    metricity = [gamma(direction, 2, 2).value == 0 and gamma(direction, 3, 3).value == 0 and (gamma(direction, 2, 3) + gamma(direction, 3, 2)).value == 0 for direction in range(N)]
    commutators = [q[1][2] - q[2][1] == 2 * eps * p3, q[1][3] - q[3][1] == -2 * eps * p2, q[2][3] - q[3][2] == 2 * eps * p1]
    return {
        "connection_four_components": tuple(value.value for value in connection) == expected_connection,
        "curvature_six_components": curvature == expected_curvature,
        "metricity_four_directions": all(metricity),
        "scalar_jet_commutators_three": all(commutators),
    }


def main() -> None:
    lambdas = [Q(-2), Q(-1), Q(0), Q(1, 2), Q(1), Q(2)]
    rows = []
    for index, lam in enumerate(lambdas, start=1):
        for mc_sign in (1, -1):
            checks = witness(lam, mc_sign)
            if not all(checks.values()):
                raise SystemExit(f"FAIL C{index:02d}/{mc_sign}: {checks}")
            rows.append({"id": f"C{index:02d}_MC_{'PLUS' if mc_sign == 1 else 'MINUS'}", "lambda": str(lam), "checks": checks})
    result = {
        "schema": "udt-r17-path-connection-independent-v1",
        "status": "PASS",
        "mode": "standard_library_fraction_second_jet_constructive",
        "imports_production_controller": False,
        "imports_sympy": False,
        "assigns_connection_or_curvature": False,
        "derives_frame_by_gauss_jordan": True,
        "derives_brackets_from_noncoordinate_base": True,
        "derives_connection_by_koszul": True,
        "derives_all_curvature_planes_by_exterior_derivative": True,
        "compatible_noncommuting_second_jets": True,
        "lambda_strata": 6,
        "maurer_cartan_signs": 2,
        "witnesses": rows,
        "aggregate_atomic_checks": 300,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: 300 exact Fraction/second-jet checks; six lambdas; both MC signs")


if __name__ == "__main__":
    main()
