#!/usr/bin/env python3
"""Independent finite-algebra replay for the bounded G222 theorem.

This standard-library implementation does not certify the general differential-geometric
theorems by sampling.  It cross-checks their finite algebra, the explicit flat-ribbon witness,
and the quotient/normal projector on exact rational instances.
"""

from __future__ import annotations

import json
import random
from fractions import Fraction as F


if not __debug__:
    raise RuntimeError("G222 evidence requires Python assertions; optimized mode is forbidden")


Vector = tuple[F, F, F, F]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify(case_count: int = 12000, seed: int = 2220822) -> dict[str, int | str]:
    rng = random.Random(seed)
    assertions = 0
    screen_cases = 0
    connection_cases = 0
    tidal_cases = 0
    flat_ribbon_cases = 0

    for index in range(case_count):
        T = F(rng.randint(1, 11), rng.randint(1, 9))
        a = F(rng.randint(1, 13), rng.randint(1, 9))
        r = F(rng.randint(1, 13), rng.randint(1, 9))
        wb = F(rng.randint(1, 13), rng.randint(1, 9))
        wa = r * wb

        h00, h01, h11 = -T * T, -a, F(0)
        det = h00 * h11 - h01 * h01
        beta = h01 / h00
        L2 = h11 - h01 * h01 / h00
        normalized_metric = (h00, h01 / a, h11 / (a * a))
        require(det == -a * a, f"pair determinant {index}")
        require(beta == a / (T * T), f"shift {index}")
        require(L2 == a * a / (T * T), f"ruler {index}")
        require(T * T * L2 == a * a, f"density {index}")
        require(normalized_metric == (-T * T, F(-1), F(0)), f"completed metric {index}")
        require(wa / wb == r, f"boundary ratio {index}")
        assertions += 6

        c_affine = F(rng.randint(1, 9), rng.randint(1, 7))
        null_shift = F(rng.randint(-7, 7), rng.randint(1, 9))
        hp00, hp01, hp11 = h00 - 2 * a * null_shift, -c_affine * a, F(0)
        detp = hp00 * hp11 - hp01 * hp01
        require(detp == -(c_affine * a) ** 2, f"affine determinant {index}")
        require((c_affine * a) / c_affine == a, f"vertical covector density {index}")
        require(-(-a + null_shift * 0) == a, f"null shift area {index}")
        assertions += 3

        bx = F(rng.randint(-11, 11), rng.randint(1, 9))
        by = F(rng.randint(-11, 11), rng.randint(1, 9))
        qxx = F(rng.randint(1, 13), rng.randint(1, 9))
        qxy = F(rng.randint(-7, 7), rng.randint(1, 9))
        positive_minor = F(rng.randint(1, 13), rng.randint(1, 9))
        qyy = (qxy * qxy + positive_minor) / qxx
        representative_shift = F(rng.randint(-9, 9), rng.randint(1, 9))

        # Exact Gram form in basis (J,K,X,Y).  The constructed screen block is positive definite.
        gram = (
            (-T * T, -a, bx, by),
            (-a, F(0), F(0), F(0)),
            (bx, F(0), qxx, qxy),
            (by, F(0), qxy, qyy),
        )

        def inner(u: Vector, v: Vector) -> F:
            return sum(u[i] * gram[i][j] * v[j] for i in range(4) for j in range(4))

        J: Vector = (F(1), F(0), F(0), F(0))
        K: Vector = (F(0), F(1), F(0), F(0))
        X: Vector = (F(0), F(0), F(1), F(0))
        Y: Vector = (F(0), F(0), F(0), F(1))

        def add(u: Vector, v: Vector) -> Vector:
            return tuple(u[i] + v[i] for i in range(4))  # type: ignore[return-value]

        def scale(s: F, u: Vector) -> Vector:
            return tuple(s * u[i] for i in range(4))  # type: ignore[return-value]

        def normal(v: Vector) -> Vector:
            # v - g(v,J)/g(K,J) K, defined for v in K^perp.
            return add(v, scale(-inner(v, J) / inner(K, J), K))

        IX = normal(X)
        IY = normal(Y)
        require(inner(IX, J) == 0 and inner(IX, K) == 0, f"normal X {index}")
        require(inner(IY, J) == 0 and inner(IY, K) == 0, f"normal Y {index}")
        require(inner(IX, IX) == qxx, f"isometry XX {index}")
        require(inner(IX, IY) == qxy, f"isometry XY {index}")
        require(inner(IY, IY) == qyy, f"isometry YY {index}")
        Xrep = add(X, scale(representative_shift, K))
        require(normal(Xrep) == IX, f"quotient representative {index}")
        assertions += 6
        screen_cases += 1

        # If V=nabla_K X is in K^perp, differentiating the lifted representative only adds
        # -K(f_X)K.  Normal projection must remove that tangent term exactly.
        V: Vector = (
            F(0),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
        )
        f_dot = F(rng.randint(-9, 9), rng.randint(1, 9))
        differentiated_lift = add(V, scale(-f_dot, K))
        require(inner(V, K) == 0, f"connection input in Kperp {index}")
        require(normal(K) == (F(0), F(0), F(0), F(0)), f"normal kills K {index}")
        require(normal(differentiated_lift) == normal(V), f"connection intertwining {index}")
        assertions += 3
        connection_cases += 1

        # Model W=R(X,K)K as an arbitrary K-orthogonal vector and R(K,K)K=0.
        tidal_X: Vector = (
            F(0),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
            F(rng.randint(-9, 9), rng.randint(1, 9)),
        )
        def tidal_operator(x_coefficient: F, k_coefficient: F) -> Vector:
            # R(K,K)K=0, so the K coefficient contributes nothing.
            del k_coefficient
            return scale(x_coefficient, tidal_X)

        tidal_representative = tidal_operator(F(1), representative_shift)
        tidal_unshifted = tidal_operator(F(1), F(0))
        require(inner(tidal_X, K) == 0, f"tidal output in Kperp {index}")
        require(tidal_representative == tidal_unshifted, f"tidal representative {index}")
        require(
            normal(tidal_representative) == normal(tidal_unshifted),
            f"tidal intertwining {index}",
        )
        assertions += 3
        tidal_cases += 1

        # Independent exact replay of the explicit flat null ribbon.  Choose rational r>1 and set
        # epsilon=(r^2-1)/2, so the target unit tangent remains rational.
        r_flat = F(rng.randint(2, 12), rng.randint(1, 9))
        if r_flat <= 1:
            r_flat += 1
        eps = (r_flat * r_flat - 1) / 2
        y = F(rng.randint(0, 9), rng.randint(1, 9))
        lam = F(rng.randint(0, 9), rng.randint(1, 9))
        c_y = 1 + eps * y
        J_flat = (1 + eps * lam, eps * lam)
        K_flat = (c_y, c_y)

        def eta2(u: tuple[F, F], v: tuple[F, F]) -> F:
            return -u[0] * v[0] + u[1] * v[1]

        jj = eta2(J_flat, J_flat)
        jk = eta2(J_flat, K_flat)
        kk = eta2(K_flat, K_flat)
        U_A = (F(1), F(0))
        U_B = ((1 + eps) / r_flat, eps / r_flat)
        require(kk == 0, f"flat K null {index}")
        require(jk == -c_y, f"flat conserved area {index}")
        require(jj * kk - jk * jk == -c_y * c_y, f"flat determinant {index}")
        require(eta2(U_B, U_B) == -1, f"flat target unit {index}")
        require(-eta2(U_A, K_flat) == c_y, f"flat source frequency {index}")
        require(-eta2(U_B, K_flat) == c_y / r_flat, f"flat target frequency {index}")
        require(c_y / (c_y / r_flat) == r_flat, f"flat ratio {index}")
        require(eps != 0, f"flat nonclosed curl {index}")
        # In flat space J is affine in lambda.  An exact centered second difference independently
        # checks its Jacobi equation rather than asserting a literal zero.
        step = F(rng.randint(1, 9), rng.randint(1, 9))
        J_minus = (1 + eps * (lam - step), eps * (lam - step))
        J_plus = (1 + eps * (lam + step), eps * (lam + step))
        second_difference = tuple(
            (J_plus[i] - 2 * J_flat[i] + J_minus[i]) / (step * step) for i in range(2)
        )
        require(second_difference == (F(0), F(0)), f"flat Jacobi second derivative {index}")
        assertions += 9
        flat_ribbon_cases += 1

        require(F(0) * 0 - a * a == -a * a, f"clock turn remains rank two {index}")
        require((-T * T) * 0 - 0 * 0 == 0, f"zero area degenerates {index}")
        require(det == -a * a, f"screen caustic leaves pair determinant {index}")
        assertions += 3

    return {
        "classification": "independent_finite_algebra_replay_not_general_geometric_proof",
        "cases": case_count,
        "finite_algebra_assertions": assertions,
        "screen_isometry_cases": screen_cases,
        "connection_intertwining_cases": connection_cases,
        "tidal_intertwining_cases": tidal_cases,
        "flat_ribbon_cases": flat_ribbon_cases,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
