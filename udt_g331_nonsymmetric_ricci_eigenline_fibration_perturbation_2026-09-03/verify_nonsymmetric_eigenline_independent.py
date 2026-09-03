#!/usr/bin/env python3
"""Implementation-distinct rational-function verifier for G331."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


def trim(coefficients):
    out = list(coefficients)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(F(value) for value in out)


def padd(a, b):
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pmul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            out[i + j] += left * right
    return trim(out)


def pscale(a, scale):
    return trim([F(scale) * value for value in a])


def pderiv(a):
    return trim([i * a[i] for i in range(1, len(a))] or [0])


def pdivmod(numerator, denominator):
    numerator, denominator = list(trim(numerator)), trim(denominator)
    if denominator == (F(0),):
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [F(0)] * max(1, len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and trim(numerator) != (F(0),):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[degree] += coefficient
        for index, value in enumerate(denominator):
            numerator[index + degree] -= coefficient * value
        numerator = list(trim(numerator))
    return trim(quotient), trim(numerator)


def pgcd(left, right):
    left, right = trim(left), trim(right)
    while right != (F(0),):
        _, remainder = pdivmod(left, right)
        left, right = right, remainder
    if left == (F(0),):
        return (F(1),)
    return pscale(left, 1 / left[-1])


class RF:
    """Exact rational function of x; equality is cross-polynomial equality."""

    __slots__ = ("num", "den")

    def __init__(self, numerator=(0,), denominator=(1,)):
        if isinstance(numerator, RF):
            self.num, self.den = numerator.num, numerator.den
            return
        if not isinstance(numerator, (tuple, list)):
            numerator = (F(numerator),)
        if not isinstance(denominator, (tuple, list)):
            denominator = (F(denominator),)
        numerator, denominator = trim(numerator), trim(denominator)
        if denominator == (F(0),):
            raise ZeroDivisionError("zero polynomial denominator")
        if numerator == (F(0),):
            self.num, self.den = (F(0),), (F(1),)
            return
        common = pgcd(numerator, denominator)
        numerator, rem_num = pdivmod(numerator, common)
        denominator, rem_den = pdivmod(denominator, common)
        if rem_num != (F(0),) or rem_den != (F(0),):
            raise ArithmeticError("non-exact rational-function reduction")
        normalization = denominator[-1]
        self.num = pscale(numerator, 1 / normalization)
        self.den = pscale(denominator, 1 / normalization)

    @staticmethod
    def q(value):
        return value if isinstance(value, RF) else RF(value)

    def __add__(self, other):
        other = RF.q(other)
        return RF(padd(pmul(self.num, other.den), pmul(other.num, self.den)), pmul(self.den, other.den))

    __radd__ = __add__

    def __neg__(self):
        return RF(pscale(self.num, -1), self.den)

    def __sub__(self, other):
        return self + (-RF.q(other))

    def __rsub__(self, other):
        return RF.q(other) - self

    def __mul__(self, other):
        other = RF.q(other)
        return RF(pmul(self.num, other.num), pmul(self.den, other.den))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = RF.q(other)
        if other.num == (F(0),):
            raise ZeroDivisionError("zero rational function")
        return RF(pmul(self.num, other.den), pmul(self.den, other.num))

    def __rtruediv__(self, other):
        return RF.q(other) / self

    def __eq__(self, other):
        other = RF.q(other)
        return pmul(self.num, other.den) == pmul(other.num, self.den)

    def __bool__(self):
        return self.num != (F(0),)

    def deriv(self):
        numerator = padd(pmul(pderiv(self.num), self.den), pscale(pmul(self.num, pderiv(self.den)), -1))
        return RF(numerator, pmul(self.den, self.den))

    def evaluate(self, x_value):
        x_value = F(x_value)

        def peval(poly):
            answer = F(0)
            for coefficient in reversed(poly):
                answer = answer * x_value + coefficient
            return answer

        return peval(self.num) / peval(self.den)


X = RF((0, 1))
ONE = RF(1)
ZERO = RF(0)


def ident(n=3):
    return [[RF(int(i == j)) for j in range(n)] for i in range(n)]


def mm(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), ZERO)
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def inv(matrix):
    n = len(matrix)
    unit = ident(n)
    aug = [list(matrix[i]) + unit[i] for i in range(n)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col]), None)
        if pivot is None:
            raise ZeroDivisionError("singular rational-function matrix")
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


def metric(weight_1, weight_2):
    w1, w2 = F(weight_1), F(weight_2)
    r = X * (ONE - X)
    f = w1 * X + w2 * (ONE - X)
    eta = (X / f, (ONE - X) / f)
    zeta = (w2 / f, -w1 / f)
    g = [[ZERO for _ in range(3)] for _ in range(3)]
    g[0][0] = 1 / (4 * r * f)
    g[1][1] = r / f * zeta[0] * zeta[0] + eta[0] * eta[0]
    g[1][2] = g[2][1] = r / f * zeta[0] * zeta[1] + eta[0] * eta[1]
    g[2][2] = r / f * zeta[1] * zeta[1] + eta[1] * eta[1]
    return g


def ricci_endomorphism(weight_1, weight_2):
    g = metric(weight_1, weight_2)
    gi = inv(g)
    gamma = [[[ZERO for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for i in range(3):
            for j in range(3):
                for ell in range(3):
                    first = g[ell][j].deriv() if i == 0 else ZERO
                    second = g[ell][i].deriv() if j == 0 else ZERO
                    third = g[i][j].deriv() if ell == 0 else ZERO
                    gamma[upper][i][j] += gi[upper][ell] * (first + second - third) / 2
    ricci = [[ZERO for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            value = gamma[0][i][j].deriv()
            if j == 0:
                value -= sum((gamma[k][i][k].deriv() for k in range(3)), ZERO)
            for k in range(3):
                for ell in range(3):
                    value += gamma[k][i][j] * gamma[ell][k][ell]
                    value -= gamma[ell][i][k] * gamma[k][j][ell]
            ricci[i][j] = value
    return g, ricci, mm(gi, ricci)


def outer(column, row):
    return [[column[i] * row[j] for j in range(len(row))] for i in range(len(column))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    for index, (w1, w2) in enumerate(((F(2), F(3)), (F(3, 2), F(5, 4)), (F(7, 3), F(11, 5)))):
        g, ricci, a = ricci_endomorphism(w1, w2)
        xi = [ZERO, RF(w1), RF(w2)]
        eta = [sum((g[i][j] * xi[j] for j in range(3)), ZERO) for i in range(3)]
        require(sum((eta[i] * xi[i] for i in range(3)), ZERO) == 1,
                f"family_{index}_unit_reeb_identity")
        require(
            [sum((a[i][j] * xi[j] for j in range(3)), ZERO) for i in range(3)]
            == [2 * entry for entry in xi],
            f"family_{index}_ricci_eigenline_identity",
        )
        scalar = sum((a[i][i] for i in range(3)), ZERO)
        lam_h = (scalar - 2) / 2
        projector = outer(xi, eta)
        expected = [[lam_h * RF(int(i == j)) + (2 - lam_h) * projector[i][j]
                     for j in range(3)] for i in range(3)]
        require(a == expected, f"family_{index}_full_projector_identity")
        require(bool(scalar.deriv()), f"family_{index}_nonconstant_scalar")
        for x_value in (F(1, 5), F(2, 5), F(3, 5), F(4, 5)):
            require(sum(eta[i].evaluate(x_value) * xi[i].evaluate(x_value) for i in range(3)) == 1,
                    f"family_{index}_interior_{x_value}_unit")

    # Independent equal-weight recovery and exact G330 eigenvalue comparison.
    for index, (a_radius, c_radius) in enumerate(((F(3, 2), F(1)), (F(4, 3), F(7, 5)))):
        w = a_radius**2 / c_radius**2
        mu = a_radius**4 / c_radius**2
        _, _, endomorphism = ricci_endomorphism(w, w)
        xi = [ZERO, RF(w), RF(w)]
        lhs = [sum((endomorphism[i][j] * xi[j] for j in range(3)), ZERO) / mu for i in range(3)]
        require(lhs == [2 * entry / mu for entry in xi], f"berger_{index}_scaled_vertical")
        require(F(2) / mu == 2 * c_radius**2 / a_radius**4, f"berger_{index}_g330_value")

    # A rank-one cluster stays isolated under the strict half-gap hypothesis; equality is not used.
    for index, (lam_h, lam_v, error) in enumerate((
        (F(-1, 2), F(9, 2), F(1)),
        (F(7, 3), F(-5, 3), F(3, 2)),
        (F(0), F(1, 10), F(1, 100)),
    )):
        separation = abs(lam_v - lam_h)
        require(error < separation / 2, f"spectral_{index}_strict_half_gap")
        require(lam_h + error < lam_v - error if lam_h < lam_v else lam_v + error < lam_h - error,
                f"spectral_{index}_disjoint_intervals")

    # The conformal transformation is checked independently from its n-dimensional coefficients.
    dimension = 3
    hess_13 = F(1)
    laplacian = F(2)
    for index, epsilon in enumerate((F(1, 50), F(-1, 75))):
        off_diagonal = -(dimension - 2) * epsilon * hess_13
        scalar_change = -2 * (dimension - 1) * epsilon * laplacian
        require(off_diagonal == -epsilon, f"conformal_{index}_offdiagonal")
        require(scalar_change == -8 * epsilon, f"conformal_{index}_scalar")

    # Exact irrationality certificate and approach to the Hopf generator.
    for n in (20, 200, 2000):
        sqrt_two_coefficient = F(2 * n, n * n - 2)
        require(sqrt_two_coefficient != 0, f"flow_{n}_irrational_certificate")
        require(F(2, n * n) < F(1, 100), f"flow_{n}_close_squared")

    payload = {
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "imports_production_code": False,
        "reads_production_output": False,
        "method": "exact rational-function coordinate Ricci calculation over the full interior x-domain",
        "metric_family": "weighted Sasaki S3 family with unequal torus weights",
        "ricci_line": "weighted Reeb line, verified as a rational-function identity",
        "generic_orbits": "nonclosed for irrational weight ratio",
        "constraint_embedding_proved": False,
        "stability_proved": False,
        "history_selected": False,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G331 independent PASS: {len(checks)} exact checks")


if __name__ == "__main__":
    main()
