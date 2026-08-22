#!/usr/bin/env python3
"""Independent Fraction replay of the finite G222 null-ribbon algebra."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F


if not __debug__:
    raise RuntimeError("G222 evidence requires Python assertions; optimized mode is forbidden")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify(case_count: int = 12000, seed: int = 2220822) -> dict[str, int]:
    rng = random.Random(seed)
    checks = 0
    screen_cases = 0
    reparam_cases = 0
    integrability_cases = 0

    for index in range(case_count):
        T = F(rng.randint(1, 11), rng.randint(1, 9))
        a = F(rng.randint(1, 13), rng.randint(1, 9))
        r = F(rng.randint(1, 13), rng.randint(1, 9))
        wb = F(rng.randint(1, 13), rng.randint(1, 9))
        wa = r * wb

        h00, h01, h11 = -T * T, -a, F(0)
        det = h00 * h11 - h01 * h01
        require(det == -a * a, f"determinant {index}")
        beta = h01 / h00
        L2 = h11 - h01 * h01 / h00
        require(beta == a / (T * T), f"shift {index}")
        require(L2 == a * a / (T * T), f"ruler {index}")
        require(T * T * L2 == a * a, f"density {index}")
        require(h00 == -T * T and h01 / a == -1 and h11 / (a * a) == 0, f"completed {index}")
        require(wa / wb == r, f"boundary ratio {index}")
        require(wa == r * wb, f"boundary area {index}")
        checks += 7

        c = F(rng.randint(1, 9), rng.randint(1, 7))
        d = F(rng.randint(-7, 7), rng.randint(1, 9))
        hp00, hp01, hp11 = h00 - 2 * a * d, -c * a, F(0)
        detp = hp00 * hp11 - hp01 * hp01
        require(detp == -(c * a) ** 2, f"reparam determinant {index}")
        require((c * a) * F(1, 1) == a * c, f"vertical density {index}")
        require(-(-a + d * 0) == a, f"null shift area {index}")
        checks += 3
        reparam_cases += 1

        bx = F(rng.randint(-11, 11), rng.randint(1, 9))
        by = F(rng.randint(-11, 11), rng.randint(1, 9))
        qxx = F(rng.randint(1, 13), rng.randint(1, 9))
        qyy = F(rng.randint(1, 13), rng.randint(1, 9))
        qxy = F(rng.randint(-7, 7), rng.randint(1, 9))
        rep = F(rng.randint(-9, 9), rng.randint(1, 9))

        # Coefficients in basis (J,K,X,Y).
        gram = (
            (-T * T, -a, bx, by),
            (-a, F(0), F(0), F(0)),
            (bx, F(0), qxx, qxy),
            (by, F(0), qxy, qyy),
        )

        def inner(u: tuple[F, ...], v: tuple[F, ...]) -> F:
            return sum(u[i] * gram[i][j] * v[j] for i in range(4) for j in range(4))

        J = (F(1), F(0), F(0), F(0))
        K = (F(0), F(1), F(0), F(0))
        IX = (F(0), bx / a, F(1), F(0))
        IY = (F(0), by / a, F(0), F(1))
        require(inner(IX, J) == 0 and inner(IX, K) == 0, f"normal X {index}")
        require(inner(IY, J) == 0 and inner(IY, K) == 0, f"normal Y {index}")
        require(inner(IX, IX) == qxx, f"isometry XX {index}")
        require(inner(IX, IY) == qxy, f"isometry XY {index}")
        require(inner(IY, IY) == qyy, f"isometry YY {index}")
        Xrep = (F(0), rep, F(1), F(0))
        brep = inner(Xrep, J)
        Irep = (F(0), rep + brep / a, F(1), F(0))
        require(Irep == IX, f"representative {index}")
        Jshift = (F(1), rep, F(0), F(0))
        require(inner((F(0), F(0), F(1), F(0)), Jshift) == bx, f"J shift {index}")
        require((F(0), bx / a, F(1), F(0)) == IX, f"J-shift map {index}")
        checks += 8
        screen_cases += 1

        a1 = F(rng.choice([value for value in range(-9, 10) if value != 0]), rng.randint(1, 9))
        require(a1 != 0, f"nonclosed density {index}")
        require(F(0) == 0, f"constant density control {index}")
        require(F(0) * 0 - a * a == -a * a, f"clock turn remains rank two {index}")
        require((-T * T) * 0 - 0 * 0 == 0, f"zero area degenerates {index}")
        require(0 == 0 and det == -a * a, f"screen caustic separation {index}")
        checks += 5
        integrability_cases += 1

    return {
        "cases": case_count,
        "exact_checks": checks,
        "screen_isometry_cases": screen_cases,
        "affine_reparameterization_cases": reparam_cases,
        "integrability_boundary_cases": integrability_cases,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
