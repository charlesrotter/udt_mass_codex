#!/usr/bin/env python3
"""Independent exact G332 replay using truncated series and adjugate inversion."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


class Series:
    """Second-order Taylor coefficients, normalized by powers rather than derivatives."""

    __slots__ = ("c",)

    def __init__(self, *coefficients):
        data = [F(value) for value in coefficients]
        self.c = tuple((data + [F(0), F(0), F(0)])[:3])

    @staticmethod
    def lift(value):
        return value if isinstance(value, Series) else Series(value)

    def __add__(self, other):
        other = self.lift(other)
        return Series(*(self.c[i] + other.c[i] for i in range(3)))

    __radd__ = __add__

    def __neg__(self):
        return Series(*(-value for value in self.c))

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Series(*(
            sum(self.c[j] * other.c[i - j] for j in range(i + 1))
            for i in range(3)
        ))

    __rmul__ = __mul__

    def reciprocal(self):
        if not self.c[0]:
            raise ZeroDivisionError("zero series")
        d0 = 1 / self.c[0]
        d1 = -self.c[1] * d0 / self.c[0]
        d2 = -(self.c[1] * d1 + self.c[2] * d0) / self.c[0]
        return Series(d0, d1, d2)

    def __truediv__(self, other):
        return self * self.lift(other).reciprocal()

    def __rtruediv__(self, other):
        return self.lift(other) * self.reciprocal()

    def derivative_at_zero(self):
        return self.c[1]


class Surd:
    """Exact a+b*s at one point, with s^2=q."""

    __slots__ = ("a", "b", "q")

    def __init__(self, a, b, q):
        self.a, self.b, self.q = F(a), F(b), F(q)

    def lift(self, other):
        if isinstance(other, Surd):
            if other.q != self.q:
                raise ValueError("incompatible surds")
            return other
        return Surd(other, 0, self.q)

    def __add__(self, other):
        other = self.lift(other)
        return Surd(self.a + other.a, self.b + other.b, self.q)

    __radd__ = __add__

    def __neg__(self):
        return Surd(-self.a, -self.b, self.q)

    def __sub__(self, other):
        return self + (-self.lift(other))

    def __rsub__(self, other):
        return self.lift(other) - self

    def __mul__(self, other):
        other = self.lift(other)
        return Surd(
            self.a * other.a + self.b * other.b * self.q,
            self.a * other.b + self.b * other.a,
            self.q,
        )

    __rmul__ = __mul__

    def __truediv__(self, value):
        value = F(value)
        return Surd(self.a / value, self.b / value, self.q)

    def zero(self):
        return self.a == 0 and self.b == 0


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def inverse3(m):
    cof = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows = [r for r in range(3) if r != i]
            cols = [c for c in range(3) if c != j]
            minor = m[rows[0]][cols[0]] * m[rows[1]][cols[1]]
            minor -= m[rows[0]][cols[1]] * m[rows[1]][cols[0]]
            cof[i][j] = minor if (i + j) % 2 == 0 else -minor
    determinant = sum(m[0][j] * cof[0][j] for j in range(3))
    return [[cof[j][i] / determinant for j in range(3)] for i in range(3)]


def weighted_series(x0, w1, w2):
    x = Series(x0, 1)
    one = Series(1)
    radial = x * (one - x)
    weight = w1 * x + w2 * (one - x)
    eta = [x / weight, (one - x) / weight]
    zeta = [Series(w2) / weight, Series(-w1) / weight]
    g = [[Series(0) for _ in range(3)] for _ in range(3)]
    g[0][0] = 1 / (4 * radial * weight)
    g[1][1] = radial / weight * zeta[0] * zeta[0] + eta[0] * eta[0]
    g[1][2] = g[2][1] = radial / weight * zeta[0] * zeta[1] + eta[0] * eta[1]
    g[2][2] = radial / weight * zeta[1] * zeta[1] + eta[1] * eta[1]
    return g


def geometry(x0, w1, w2):
    g = weighted_series(x0, w1, w2)
    gi = inverse3(g)
    connection = [[[Series(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                total = Series(0)
                for ell in range(3):
                    term = Series(0)
                    if i == 0:
                        term += Series(g[ell][j].c[1], 2 * g[ell][j].c[2])
                    if j == 0:
                        term += Series(g[ell][i].c[1], 2 * g[ell][i].c[2])
                    if ell == 0:
                        term -= Series(g[i][j].c[1], 2 * g[i][j].c[2])
                    total += gi[upper][ell] * term / 2
                connection[upper][i][j] = total

    ricci = [[F(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = connection[0][i][j].derivative_at_zero()
            if j == 0:
                value -= sum(connection[k][i][k].derivative_at_zero() for k in range(3))
            for k in range(3):
                for ell in range(3):
                    value += connection[k][i][j].c[0] * connection[ell][k][ell].c[0]
                    value -= connection[ell][i][k].c[0] * connection[k][j][ell].c[0]
            ricci[i][j] = value
    scalar = sum(
        gi[i][j].c[0] * ricci[i][j]
        for i in range(3) for j in range(3)
    )
    return g, gi, connection, scalar


def matrix_product(left, right, q):
    out = [[Surd(0, 0, q) for _ in range(len(right[0]))] for _ in range(len(left))]
    for i in range(len(left)):
        for j in range(len(right[0])):
            for k in range(len(right)):
                lhs = left[i][k] if isinstance(left[i][k], Surd) else Surd(left[i][k], 0, q)
                out[i][j] += lhs * right[k][j]
    return out


def check_case(x, w1, w2, c0, lam, branch):
    g_series, gi_series, connection, scalar = geometry(x, w1, w2)
    g = [[g_series[i][j].c[0] for j in range(3)] for i in range(3)]
    gi = [[gi_series[i][j].c[0] for j in range(3)] for i in range(3)]
    xi = [F(0), F(w1), F(w2)]
    eta = [sum(g[i][j] * xi[j] for j in range(3)) for i in range(3)]
    q = 2 * (scalar + 2 * c0 * c0 - 2 * lam)
    if q <= 0:
        raise AssertionError("independent sample radicand")
    s = Surd(0, branch, q)
    b = -c0 + s
    horizontal = c0 - s / 2
    k_cov = [[horizontal * g[i][j] + b * eta[i] * eta[j] for j in range(3)] for i in range(3)]
    k_mixed = matrix_product(gi, k_cov, q)
    tau = sum(k_mixed[i][i] for i in range(3))
    norm = sum(
        k_mixed[i][j] * k_mixed[j][i]
        for i in range(3) for j in range(3)
    )
    ham = Surd(scalar, 0, q) + tau * tau - norm - 2 * lam

    p = [[Surd(-c0 * gi[i][j], 0, q) + b * xi[i] * xi[j] for j in range(3)] for i in range(3)]
    momentum = []
    for i in range(3):
        value = Surd(-c0 * gi_series[i][0].c[1], 0, q)
        for j in range(3):
            for k in range(3):
                value += connection[i][j][k].c[0] * p[k][j]
                value += connection[j][j][k].c[0] * p[i][k]
        momentum.append(value)

    norm_xi = sum(eta[i] * xi[i] for i in range(3))
    div_xi = sum(
        connection[i][i][k].c[0] * xi[k]
        for i in range(3) for k in range(3)
    )
    accel = [sum(
        connection[i][j][k].c[0] * xi[j] * xi[k]
        for j in range(3) for k in range(3)
    ) for i in range(3)]
    return scalar, q, (
        det3(g) > 0
        and norm_xi == 1
        and div_xi == 0
        and all(value == 0 for value in accel)
        and ham.zero()
        and all(value.zero() for value in momentum)
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()

    checks = []
    records = []
    samples = (
        (F(1, 4), F(2), F(3)),
        (F(3, 5), F(2), F(3)),
        (F(2, 7), F(4, 3), F(5, 3)),
        (F(1, 2), F(1), F(1)),
    )
    for index, (x, w1, w2) in enumerate(samples):
        for lam in (F(-5), F(0), F(3), F(13)):
            for c0 in (F(-25), F(25)):
                for branch in (-1, 1):
                    scalar, radicand, passed = check_case(x, w1, w2, c0, lam, branch)
                    if not passed:
                        raise AssertionError(f"independent_case_{index}_{lam}_{c0}_{branch}")
                    checks.append(f"independent_case_{index}_{lam}_{c0}_{branch}")
                    records.append({
                        "x": str(x), "w1": str(w1), "w2": str(w2),
                        "Lambda": str(lam), "C": str(c0), "branch": branch,
                        "R": str(scalar), "radicand": str(radicand),
                    })

    left = geometry(F(1, 4), F(2), F(3))[-1]
    right = geometry(F(3, 5), F(2), F(3))[-1]
    if left == right:
        raise AssertionError("independent_nonconstant_scalar")
    checks.append("independent_nonconstant_scalar")

    payload = {
        "package": "G332",
        "verifier": "independent_truncated_series_adjugate_coordinate_reconstruction",
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
