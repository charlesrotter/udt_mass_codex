#!/usr/bin/env python3
"""Constructive standard-library check of the R17 leaf normal geometry."""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class D:
    value: Q
    derivative: Q = Q(0)

    @staticmethod
    def make(value: "D | Q | int") -> "D":
        return value if isinstance(value, D) else D(Q(value))

    def __add__(self, other):
        other = D.make(other)
        return D(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return D(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-D.make(other))

    def __rsub__(self, other):
        return D.make(other) - self

    def __mul__(self, other):
        other = D.make(other)
        return D(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def reciprocal(self):
        return D(1 / self.value, -self.derivative / (self.value * self.value))

    def __truediv__(self, other):
        return self * D.make(other).reciprocal()

    def __rtruediv__(self, other):
        return D.make(other) / self


def matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), D(Q(0))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def inverse(a):
    n = len(a)
    augmented = [row[:] + [D(Q(int(i == j))) for j in range(n)] for i, row in enumerate(a)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column].value != 0)
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - factor * augmented[column][j] for j in range(2 * n)
            ]
    return [row[n:] for row in augmented]


def coframe_data(lam: Q, u0: Q, v0: Q, a0: Q, p_values: tuple[Q, Q, Q]):
    p1, p2, p3 = p_values
    # The Dual derivative is the e1 derivative.  Arbitrary second jets are
    # retained to make cancellation visible rather than assumed.
    u = D(u0, p1)
    v = D(v0, lam * v0 * p1 / u0)
    a = D(a0)
    second = (Q(7, 13), Q(-5, 17), Q(11, 19))
    p = (D(Q(0)), D(p1, second[0]), D(p2, second[1]), D(p3, second[2]))
    coframe = [
        [1 / u, a / u, D(0), D(0)],
        [D(0), u, D(0), D(0)],
        [D(0), D(0), v, D(0)],
        [D(0), D(0), D(0), v],
    ]
    log_v = (D(0), lam * p[1], lam * p[2], lam * p[3])
    derivatives = []
    for direction in range(4):
        derivatives.append(
            [
                [-p[direction] / u, -a * p[direction] / u, D(0), D(0)],
                [D(0), u * p[direction], D(0), D(0)],
                [D(0), D(0), v * log_v[direction], D(0)],
                [D(0), D(0), D(0), v * log_v[direction]],
            ]
        )
    return coframe, derivatives


def structure_constants(mc_sign: int):
    constants = [[[D(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    value = D(2 * mc_sign)
    for left, right, output in ((2, 3, 1), (3, 1, 2), (1, 2, 3)):
        constants[left][right][output] = value
        constants[right][left][output] = -value
    return constants


def frame_bracket(left, right, coframe, derivatives, constants):
    frame = inverse(coframe)
    d_frame = []
    for derivative in derivatives:
        product = matmul(matmul(frame, derivative), frame)
        d_frame.append([[-entry for entry in row] for row in product])
    base = []
    for output in range(4):
        value = D(0)
        for direction in range(4):
            value += frame[direction][left] * d_frame[direction][output][right]
            value -= frame[direction][right] * d_frame[direction][output][left]
        for first in range(4):
            for second in range(4):
                value += frame[first][left] * frame[second][right] * constants[first][second][output]
        base.append(value)
    return [
        sum((coframe[row][column] * base[column] for column in range(4)), D(0))
        for row in range(4)
    ]


def verify_witness(lam: Q, mc_sign: int) -> dict[str, bool]:
    u = Q(4)
    v = {
        Q(-2): Q(1, 16), Q(-1): Q(1, 4), Q(0): Q(1),
        Q(1, 2): Q(2), Q(1): Q(4), Q(2): Q(16),
    }[lam]
    a = Q(1, 64)
    p1, p2, p3 = Q(3, 50), Q(1, 50), Q(2, 50)
    coframe, derivatives = coframe_data(lam, u, v, a, (p1, p2, p3))
    constants = structure_constants(mc_sign)
    brackets = [[frame_bracket(i, j, coframe, derivatives, constants) for j in range(4)] for i in range(4)]
    eta = (-1, 1, 1, 1)

    def inner(vector, basis):
        return eta[basis] * vector[basis]

    def gamma(direction, vector, output):
        return (
            inner(brackets[direction][vector], output)
            - inner(brackets[vector][output], direction)
            + inner(brackets[output][direction], vector)
        ) / 2

    normal = [gamma(direction, 2, 3) for direction in range(4)]
    expected_A0 = Q(mc_sign) * a / (u * v * v)
    expected_A1 = Q(mc_sign) * (Q(2) / u - u / (v * v))
    pair = brackets[0][1]
    curvature = -normal[0].derivative - sum(
        (pair[index].value * normal[index].value for index in range(4)), Q(0)
    )
    expected_curvature = Q(mc_sign) * 2 * a * (1 + lam) * p1 / (u * u * v * v)
    A_T = normal[0].value / u
    A_Z = u * normal[1].value + a * normal[0].value / u
    expected_A_T = Q(mc_sign) * a / (u * u * v * v)
    expected_A_Z = Q(mc_sign) * (Q(2) - u * u / (v * v) + a * a / (u * u * v * v))
    return {
        "A_e0_constructive": normal[0].value == expected_A0,
        "A_e1_constructive": normal[1].value == expected_A1,
        "e1_of_A_e0_cancels_arbitrary_second_jets": normal[0].derivative == -(1 + 2 * lam) * p1 * expected_A0 / u,
        "curvature_constructive": curvature == expected_curvature,
        "global_leaf_components_constructive": A_T == expected_A_T and A_Z == expected_A_Z,
        "stratum_class_correct": (curvature == 0) == (lam == -1),
    }


def main() -> None:
    lambdas = [Q(-2), Q(-1), Q(0), Q(1, 2), Q(1), Q(2)]
    witnesses = []
    for index, lam in enumerate(lambdas, start=1):
        for mc_sign in (1, -1):
            checks = verify_witness(lam, mc_sign)
            if not all(checks.values()):
                raise SystemExit(f"FAIL C{index:02d}/{mc_sign}: {checks}")
            witnesses.append(
                {
                    "id": f"C{index:02d}_MC_{'PLUS' if mc_sign == 1 else 'MINUS'}",
                    "lambda": str(lam),
                    "checks": checks,
                }
            )
    result = {
        "schema": "udt-r17-normal-holonomy-independent-v1",
        "status": "PASS",
        "mode": "standard_library_fraction_dual_constructive",
        "imports_production_controller": False,
        "assigns_connection_or_curvature": False,
        "derives_frame_by_gauss_jordan": True,
        "derives_frame_derivative_by_inverse_identity": True,
        "derives_connection_by_koszul": True,
        "derives_curvature_by_exterior_derivative": True,
        "arbitrary_second_jets_exercised": True,
        "lambda_strata": 6,
        "maurer_cartan_sign_conventions": 2,
        "witnesses": witnesses,
        "checks_per_witness": 6,
        "passed_checks": 72,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS: 72/72 constructive Fraction/Dual checks; six lambda strata; both MC signs")


if __name__ == "__main__":
    main()
