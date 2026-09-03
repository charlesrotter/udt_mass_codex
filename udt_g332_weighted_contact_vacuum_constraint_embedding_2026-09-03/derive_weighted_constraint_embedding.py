#!/usr/bin/env python3
"""Exact rational-coordinate checks for the preregistered G332 witness."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class Jet2:
    """Value and first two derivatives of a one-variable rational function."""

    __slots__ = ("v", "d1", "d2")

    def __init__(self, value=0, first=0, second=0):
        self.v = F(value)
        self.d1 = F(first)
        self.d2 = F(second)

    @staticmethod
    def q(value):
        return value if isinstance(value, Jet2) else Jet2(value)

    def __add__(self, other):
        other = Jet2.q(other)
        return Jet2(self.v + other.v, self.d1 + other.d1, self.d2 + other.d2)

    __radd__ = __add__

    def __neg__(self):
        return Jet2(-self.v, -self.d1, -self.d2)

    def __sub__(self, other):
        return self + (-Jet2.q(other))

    def __rsub__(self, other):
        return Jet2.q(other) - self

    def __mul__(self, other):
        other = Jet2.q(other)
        return Jet2(
            self.v * other.v,
            self.d1 * other.v + self.v * other.d1,
            self.d2 * other.v + 2 * self.d1 * other.d1 + self.v * other.d2,
        )

    __rmul__ = __mul__

    def inverse(self):
        if not self.v:
            raise ZeroDivisionError("zero jet")
        return Jet2(
            1 / self.v,
            -self.d1 / self.v**2,
            2 * self.d1**2 / self.v**3 - self.d2 / self.v**2,
        )

    def __truediv__(self, other):
        return self * Jet2.q(other).inverse()

    def __rtruediv__(self, other):
        return Jet2.q(other) * self.inverse()


class Quadratic:
    """Exact a+b*s arithmetic at a point, with s^2=q>0."""

    __slots__ = ("a", "b", "q")

    def __init__(self, a, b, q):
        self.a = F(a)
        self.b = F(b)
        self.q = F(q)

    @classmethod
    def lift(cls, value, q):
        if isinstance(value, cls):
            if value.q != q:
                raise ValueError("quadratic generators differ")
            return value
        return cls(value, 0, q)

    def __add__(self, other):
        other = self.lift(other, self.q)
        return Quadratic(self.a + other.a, self.b + other.b, self.q)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b, self.q)

    def __sub__(self, other):
        return self + (-self.lift(other, self.q))

    def __rsub__(self, other):
        return self.lift(other, self.q) - self

    def __mul__(self, other):
        other = self.lift(other, self.q)
        return Quadratic(
            self.a * other.a + self.b * other.b * self.q,
            self.a * other.b + self.b * other.a,
            self.q,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = F(other)
        return Quadratic(self.a / other, self.b / other, self.q)

    def is_zero(self):
        return self.a == 0 and self.b == 0

    def as_pair(self):
        return [str(self.a), str(self.b)]


def identity(n=3):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def matmul(left, right):
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def inverse_fraction(matrix):
    n = len(matrix)
    aug = [list(matrix[i]) + identity(n)[i] for i in range(n)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col]), None)
        if pivot is None:
            raise ZeroDivisionError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [entry / scale for entry in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [aug[row][j] - factor * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def weighted_metric_jets(x_value, weight_1, weight_2):
    """G331 metric in (x,phi1,phi2), with exact x derivatives."""
    x = Jet2(x_value, 1, 0)
    one = Jet2(1)
    radial = x * (one - x)
    f = weight_1 * x + weight_2 * (one - x)
    eta = (x / f, (one - x) / f)
    zeta = (Jet2(weight_2) / f, Jet2(-weight_1) / f)
    g = [[Jet2(0) for _ in range(3)] for _ in range(3)]
    g[0][0] = 1 / (4 * radial * f)
    g[1][1] = radial / f * zeta[0] * zeta[0] + eta[0] * eta[0]
    g[1][2] = g[2][1] = radial / f * zeta[0] * zeta[1] + eta[0] * eta[1]
    g[2][2] = radial / f * zeta[1] * zeta[1] + eta[1] * eta[1]
    return (
        [[g[i][j].v for j in range(3)] for i in range(3)],
        [[g[i][j].d1 for j in range(3)] for i in range(3)],
        [[g[i][j].d2 for j in range(3)] for i in range(3)],
    )


def coordinate_geometry(x_value, weight_1, weight_2):
    """Direct metric inverse, connection, Ricci tensor, and scalar curvature."""
    g, dg, ddg = weighted_metric_jets(x_value, weight_1, weight_2)
    gi = inverse_fraction(g)
    dgi = [[-sum(gi[i][a] * dg[a][b] * gi[b][j] for a in range(3) for b in range(3))
            for j in range(3)] for i in range(3)]
    gamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    dgamma = [[[F(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    first = (dg[ell][j] if i == 0 else 0)
                    first += dg[ell][i] if j == 0 else 0
                    first -= dg[i][j] if ell == 0 else 0
                    second = (ddg[ell][j] if i == 0 else 0)
                    second += ddg[ell][i] if j == 0 else 0
                    second -= ddg[i][j] if ell == 0 else 0
                    gamma[upper][i][j] += gi[upper][ell] * first / 2
                    dgamma[upper][i][j] += (
                        dgi[upper][ell] * first + gi[upper][ell] * second
                    ) / 2
    ricci = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = dgamma[0][i][j]
            if j == 0:
                value -= sum(dgamma[k][i][k] for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += gamma[k][i][j] * gamma[ell][k][ell]
                    value -= gamma[ell][i][k] * gamma[k][j][ell]
            ricci[i][j] = value
    scalar = sum(gi[i][j] * ricci[i][j] for i in range(3) for j in range(3))
    return g, dg, gi, dgi, gamma, ricci, scalar


def quadratic_matmul(left, right, q):
    rows, middle, cols = len(left), len(right), len(right[0])
    output = [[Quadratic(0, 0, q) for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            for k in range(middle):
                output[i][j] += Quadratic.lift(left[i][k], q) * right[k][j]
    return output


def run_case(x, w1, w2, constant_c, cosmological_lambda, sign):
    g, dg, gi, dgi, gamma, _, scalar = coordinate_geometry(x, w1, w2)
    xi = [F(0), F(w1), F(w2)]
    eta = [sum(g[i][j] * xi[j] for j in range(3)) for i in range(3)]
    xi_norm = sum(eta[i] * xi[i] for i in range(3))

    divergence_xi = sum(gamma[i][i][k] * xi[k] for i in range(3) for k in range(3))
    acceleration = [
        sum(gamma[i][j][k] * xi[j] * xi[k] for j in range(3) for k in range(3))
        for i in range(3)
    ]

    radicand = 2 * (scalar + 2 * constant_c**2 - 2 * cosmological_lambda)
    if radicand <= 0:
        raise ValueError("registered exact sample requires positive radicand")
    root = Quadratic(0, sign, radicand)
    b = -constant_c + root
    kh = constant_c - root / 2

    k_cov = [[
        kh * g[i][j] + b * eta[i] * eta[j]
        for j in range(3)
    ] for i in range(3)]
    k_mixed = quadratic_matmul(gi, k_cov, radicand)
    tau = trace(k_mixed)
    k_square = trace(quadratic_matmul(k_mixed, k_mixed, radicand))
    hamiltonian = Quadratic.lift(scalar, radicand) + tau * tau - k_square

    p_contra = [[
        Quadratic.lift(-constant_c * gi[i][j], radicand) + b * xi[i] * xi[j]
        for j in range(3)
    ] for i in range(3)]
    divergence_p = []
    for i in range(3):
        value = Quadratic.lift(-constant_c * dgi[i][0], radicand)
        for j in range(3):
            for k in range(3):
                value += gamma[i][j][k] * p_contra[k][j]
                value += gamma[j][j][k] * p_contra[i][k]
        divergence_p.append(value)

    p_from_k = [[
        k_cov[i][j] - tau * g[i][j]
        for j in range(3)
    ] for i in range(3)]
    p_expected = [[
        Quadratic.lift(-constant_c * g[i][j], radicand) + b * eta[i] * eta[j]
        for j in range(3)
    ] for i in range(3)]

    return {
        "metric_positive": g[0][0] > 0 and determinant3(g) > 0,
        "unit_xi": xi_norm == 1,
        "divergence_xi_zero": divergence_xi == 0,
        "acceleration_xi_zero": all(value == 0 for value in acceleration),
        "p_trace_inversion": all(
            (p_from_k[i][j] - p_expected[i][j]).is_zero()
            for i in range(3) for j in range(3)
        ),
        "momentum_zero": all(value.is_zero() for value in divergence_p),
        "hamiltonian_equals_2lambda": (
            hamiltonian - 2 * cosmological_lambda
        ).is_zero(),
        "non_pure_trace": not b.is_zero(),
        "scalar": scalar,
        "radicand": radicand,
        "tau": tau.as_pair(),
        "b": b.as_pair(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()

    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    samples = (
        (F(1, 3), F(2), F(3)),
        (F(2, 3), F(2), F(3)),
        (F(2, 5), F(3, 2), F(5, 4)),
        (F(3, 7), F(5, 4), F(7, 4)),
        (F(1, 2), F(1), F(1)),
    )
    case_records = []
    for sample_index, (x, w1, w2) in enumerate(samples):
        for lam in (F(-2), F(0), F(3), F(11)):
            for constant_c in (F(-20), F(20)):
                for sign in (-1, 1):
                    result = run_case(x, w1, w2, constant_c, lam, sign)
                    for gate in (
                        "metric_positive",
                        "unit_xi",
                        "divergence_xi_zero",
                        "acceleration_xi_zero",
                        "p_trace_inversion",
                        "momentum_zero",
                        "hamiltonian_equals_2lambda",
                        "non_pure_trace",
                    ):
                        require(result[gate], f"case_{sample_index}_{lam}_{constant_c}_{sign}_{gate}")
                    case_records.append({
                        "x": str(x),
                        "w1": str(w1),
                        "w2": str(w2),
                        "Lambda": str(lam),
                        "C": str(constant_c),
                        "branch": sign,
                        "R": str(result["scalar"]),
                        "radicand": str(result["radicand"]),
                    })

    r_left = coordinate_geometry(F(1, 3), F(2), F(3))[-1]
    r_right = coordinate_geometry(F(2, 3), F(2), F(3))[-1]
    require(r_left != r_right, "unequal_weight_scalar_is_nonconstant")
    r_round_left = coordinate_geometry(F(1, 3), F(1), F(1))[-1]
    r_round_right = coordinate_geometry(F(2, 3), F(1), F(1))[-1]
    require(r_round_left == r_round_right, "equal_weight_constant_scalar_control")

    payload = {
        "package": "G332",
        "landing": (
            "EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST"
            "__INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY"
            "__EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY"
        ),
        "grade": "DERIVED_CONDITIONAL_BOUNDED",
        "analytic_family": {
            "P": "-C*gamma+b*xi_flat*xi_flat",
            "b": "-C +/- sqrt(2*(R+2*C^2-2*Lambda))",
            "tau": "(3*C-b)/2",
            "K": "((C-b)/2)*gamma+b*xi_flat*xi_flat",
            "uniform_condition": "C^2 > Lambda - min(R)/2",
        },
        "scope": {
            "spatial_metrics": "complete positive-weight G331 weighted-contact S3 family",
            "extrinsic_curvature": "one exact witness inside unrestricted symmetric K space",
            "irregular_flow": "irrational positive weight ratio",
            "evolution": "open",
            "stability": "open",
            "occupancy": "open",
            "scale": "open",
            "X_max": "open",
        },
        "checks_passed": len(checks),
        "checks": checks,
        "sample_count": len(case_records),
        "sample_records": case_records,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "checks_passed": len(checks),
        "landing": payload["landing"],
        "sample_count": len(case_records),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
