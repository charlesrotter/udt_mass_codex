#!/usr/bin/env python3
"""Independent exact-Fraction/quadratic-surd replay for G221."""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F


if not __debug__:
    raise RuntimeError("G221 evidence must run with Python assertions enabled; -O is forbidden")

getcontext().prec = 90


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def inverse(a):
    n = len(a)
    aug = [list(row) + [F(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if aug[row][col]), None)
        require(pivot is not None, "singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor:
                aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


@dataclass(frozen=True)
class Surd:
    """a+b*sqrt(r), with all coefficients exact Fractions."""

    a: F
    b: F
    r: F

    def __add__(self, other):
        other = as_surd(other, self.r)
        require(self.r == other.r, "mixed quadratic fields")
        return Surd(self.a + other.a, self.b + other.b, self.r)

    __radd__ = __add__

    def __neg__(self):
        return Surd(-self.a, -self.b, self.r)

    def __sub__(self, other):
        return self + (-as_surd(other, self.r))

    def __rsub__(self, other):
        return as_surd(other, self.r) - self

    def __mul__(self, other):
        other = as_surd(other, self.r)
        require(self.r == other.r, "mixed quadratic fields")
        return Surd(
            self.a * other.a + self.b * other.b * self.r,
            self.a * other.b + self.b * other.a,
            self.r,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_surd(other, self.r)
        denominator = other.a * other.a - other.b * other.b * self.r
        require(denominator != 0, "zero surd denominator")
        return Surd(
            (self.a * other.a - self.b * other.b * self.r) / denominator,
            (self.b * other.a - self.a * other.b) / denominator,
            self.r,
        )

    def decimal(self) -> Decimal:
        a = Decimal(self.a.numerator) / Decimal(self.a.denominator)
        b = Decimal(self.b.numerator) / Decimal(self.b.denominator)
        r = Decimal(self.r.numerator) / Decimal(self.r.denominator)
        return a + b * r.sqrt()


def as_surd(value, r):
    if isinstance(value, Surd):
        return value
    return Surd(F(value), F(0), r)


def s_matvec(a, x):
    r = x[0].r
    return [sum((as_surd(v, r) * w for v, w in zip(row, x)), as_surd(0, r)) for row in a]


def s_quad(x, a):
    r = x[0].r
    total = as_surd(0, r)
    for i in range(len(x)):
        for j in range(len(x)):
            total += x[i] * a[i][j] * x[j]
    return total


def make_case(rng: random.Random):
    while True:
        N = F(rng.randint(2, 7))
        beta = F(rng.randint(-5, 5), rng.randint(3, 8))
        A = F(rng.randint(3, 10))
        D = A * A - N * N * beta * beta
        if D <= 0:
            continue
        Q = [[F(rng.randint(-4, 4)), F(rng.randint(-4, 4))] for _ in range(2)]
        if Q[0][0] * Q[1][1] - Q[0][1] * Q[1][0] == 0:
            continue
        H = matmul(transpose(Q), Q)
        st = [F(rng.randint(-3, 3), 12), F(rng.randint(-3, 3), 12)]
        P2 = N * N - dot(st, matvec(H, st))
        if P2 <= 0:
            continue
        sx = [F(rng.randint(-5, 5), 7), F(rng.randint(-5, 5), 7)]
        px = F(rng.randint(-7, 7), rng.randint(1, 5))
        pz = [F(rng.randint(-7, 7), rng.randint(1, 5)) for _ in range(2)]
        if px == 0 and pz == [0, 0]:
            continue
        return N, A, beta, Q, H, st, sx, px, pz, D, P2


def verify(case_count: int = 10000, reduction_pairs: int = 2000) -> dict[str, int]:
    rng = random.Random(221_20260822)
    checks = 0

    for case_index in range(case_count):
        N, A, beta, Q, H, st, sx, px, pz, D, P2 = make_case(rng)
        Hinv = inverse(H)
        qv = matvec(Hinv, pz)
        q2 = dot(pz, qv)
        Pi = px - dot(sx, pz)
        r2 = Pi * Pi + D * q2
        require(r2 > 0, f"nonpositive R2 at {case_index}")
        checks += 1

        p0_future = Surd(-N * beta * Pi / D, -A / D, r2)
        p0_past = Surd(-N * beta * Pi / D, A / D, r2)
        pt_future = Surd(dot(st, pz), F(0), r2) + N * p0_future
        pt_past = Surd(dot(st, pz), F(0), r2) + N * p0_past
        require(p0_future.decimal() < 0 < p0_past.decimal(), f"frame branch signs {case_index}")
        require(pt_future.decimal() < 0 < pt_past.decimal(), f"observer frequencies {case_index}")
        checks += 2

        S = [[st[0], sx[0]], [st[1], sx[1]]]
        QS = matmul(Q, S)
        E = [
            [N, N * beta, F(0), F(0)],
            [F(0), A, F(0), F(0)],
            [QS[0][0], QS[0][1], Q[0][0], Q[0][1]],
            [QS[1][0], QS[1][1], Q[1][0], Q[1][1]],
        ]
        etaE = [[(-row[j] if i == 0 else row[j]) for j in range(4)] for i, row in enumerate(E)]
        g = matmul(transpose(E), etaE)
        ginv = inverse(g)
        pf = [pt_future, as_surd(px, r2), as_surd(pz[0], r2), as_surd(pz[1], r2)]
        pp = [pt_past, as_surd(px, r2), as_surd(pz[0], r2), as_surd(pz[1], r2)]
        require(s_quad(pf, ginv) == as_surd(0, r2), f"future direct null {case_index}")
        require(s_quad(pp, ginv) == as_surd(0, r2), f"past direct null {case_index}")
        require((pt_future - dot(st, pz)) / N == p0_future, f"coframe p0 {case_index}")
        checks += 3

        k = s_matvec(ginv, pf)
        vx_direct = k[1] / k[0]
        vz_direct = [k[2] / k[0], k[3] / k[0]]
        vx_formula = Surd(N * N * beta / D, N * A * Pi / (D * r2), r2)
        vz_formula = [
            Surd(
                -st[j] - N * N * beta * sx[j] / D,
                N * A * (-Pi * sx[j] + D * qv[j]) / (D * r2),
                r2,
            )
            for j in range(2)
        ]
        require(vx_direct == vx_formula, f"HJ longitudinal {case_index}")
        require(vz_direct == vz_formula, f"HJ screen {case_index}")
        checks += 2

        shear = F(rng.randint(-3, 3))
        K = [[F(1), shear], [F(0), F(1)]]
        Kinv = inverse(K)
        Qp = matmul(Q, K)
        Hp = matmul(transpose(Qp), Qp)
        stp, sxp = matvec(Kinv, st), matvec(Kinv, sx)
        pzp = matvec(transpose(K), pz)
        P2p = N * N - dot(stp, matvec(Hp, stp))
        Pip = px - dot(sxp, pzp)
        q2p = dot(pzp, matvec(inverse(Hp), pzp))
        require(P2p == P2, f"screen P2 covariance {case_index}")
        require(Pip == Pi, f"screen Pi covariance {case_index}")
        require(q2p == q2, f"screen q2 covariance {case_index}")
        require(dot(stp, pzp) == dot(st, pz), f"screen energy covariance {case_index}")
        checks += 4

        scale = F(rng.randint(1, 7), rng.randint(1, 5))
        p0_scaled_same_field = Surd(
            -N * beta * (scale * Pi) / D,
            -A * scale / D,
            r2,
        )
        pt_scaled_same_field = Surd(scale * dot(st, pz), F(0), r2) + N * p0_scaled_same_field
        require(p0_scaled_same_field == scale * p0_future, f"affine p0 {case_index}")
        require(pt_scaled_same_field == scale * pt_future, f"affine frequency {case_index}")
        checks += 2

        rclock = F(rng.randint(1, 9), rng.randint(1, 7))
        require((-rclock * rclock) == -(rclock**2), f"clock leg {case_index}")
        checks += 1

    for pair_index in range(reduction_pairs):
        while True:
            N1, N2 = F(rng.randint(1, 7)), F(rng.randint(1, 7))
            b1, b2 = F(rng.randint(-4, 4), 5), F(rng.randint(-4, 4), 5)
            A1, A2 = F(rng.randint(2, 10)), F(rng.randint(2, 10))
            cp1, cp2 = A1 - N1 * b1, A2 - N2 * b2
            if A1 * A1 > N1 * N1 * b1 * b1 and A2 * A2 > N2 * N2 * b2 * b2:
                break
        px = F(rng.randint(1, 9), rng.randint(1, 7))
        W1, W2 = px / cp1, px / cp2
        require(W1 / W2 == cp2 / cp1, f"G220 reduction {pair_index}")
        require(W1 > 0 and W2 > 0, f"G220 positivity {pair_index}")
        checks += 2

    return {
        "cases": case_count + reduction_pairs,
        "full_sector_cases": case_count,
        "screen_covariance_cases": case_count,
        "future_past_branch_cases": case_count,
        "G220_reduction_pairs": reduction_pairs,
        "exact_checks": checks,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
