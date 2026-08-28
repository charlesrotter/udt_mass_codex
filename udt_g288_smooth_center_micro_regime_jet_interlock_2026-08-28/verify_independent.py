#!/usr/bin/env python3
"""Implementation-distinct exact-Fraction verification for G288.

This file imports no production module or result.  It reconstructs metric,
inverse-metric derivatives, connection derivatives, curvature, null screens,
and the regular-center polynomial maps at an equatorial event.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
D = 4
Z = F(0)
H = F(1, 2)


def zeros(*shape: int):
    if len(shape) == 1:
        return [Z for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def geometry(r: F, f: F, fp: F, fpp: F):
    # Metric and its first/second coordinate derivatives at theta=pi/2.
    g = zeros(D, D)
    g[0][0], g[1][1], g[2][2], g[3][3] = -f, 1 / f, r * r, r * r
    gi = zeros(D, D)
    gi[0][0], gi[1][1], gi[2][2], gi[3][3] = -1 / f, f, 1 / (r * r), 1 / (r * r)

    dg = zeros(D, D, D)  # dg[p][a][b]
    dg[1][0][0] = -fp
    dg[1][1][1] = -fp / (f * f)
    dg[1][2][2] = 2 * r
    dg[1][3][3] = 2 * r
    # theta derivative of r^2 sin^2(theta) vanishes at the equator.

    ddg = zeros(D, D, D, D)  # ddg[p][q][a][b]
    ddg[1][1][0][0] = -fpp
    ddg[1][1][1][1] = 2 * fp * fp / (f**3) - fpp / (f * f)
    ddg[1][1][2][2] = 2
    ddg[1][1][3][3] = 2
    ddg[2][2][3][3] = -2 * r * r

    dgi = zeros(D, D, D)
    for p in range(D):
        for a in range(D):
            for b in range(D):
                dgi[p][a][b] = -sum(
                    gi[a][e] * dg[p][e][h] * gi[h][b]
                    for e in range(D) for h in range(D)
                )

    Gamma = zeros(D, D, D)
    for a in range(D):
        for b in range(D):
            for c in range(D):
                Gamma[a][b][c] = H * sum(
                    gi[a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                    for d in range(D)
                )

    dGamma = zeros(D, D, D, D)  # derivative p of Gamma[a][b][c]
    for p in range(D):
        for a in range(D):
            for b in range(D):
                for c in range(D):
                    dGamma[p][a][b][c] = H * sum(
                        dgi[p][a][d] * (dg[b][d][c] + dg[c][d][b] - dg[d][b][c])
                        + gi[a][d]
                        * (
                            ddg[p][b][d][c]
                            + ddg[p][c][d][b]
                            - ddg[p][d][b][c]
                        )
                        for d in range(D)
                    )

    Riem = zeros(D, D, D, D)
    for a in range(D):
        for b in range(D):
            for c in range(D):
                for d in range(D):
                    Riem[a][b][c][d] = (
                        dGamma[c][a][d][b]
                        - dGamma[d][a][c][b]
                        + sum(
                            Gamma[a][c][e] * Gamma[e][d][b]
                            - Gamma[a][d][e] * Gamma[e][c][b]
                            for e in range(D)
                        )
                    )

    Rlow = zeros(D, D, D, D)
    for a in range(D):
        for b in range(D):
            for c in range(D):
                for d in range(D):
                    Rlow[a][b][c][d] = sum(g[a][e] * Riem[e][b][c][d] for e in range(D))

    Ric = zeros(D, D)
    for b in range(D):
        for d in range(D):
            Ric[b][d] = sum(Riem[a][b][a][d] for a in range(D))
    scalar = sum(gi[a][b] * Ric[a][b] for a in range(D) for b in range(D))
    ricci_sq = sum(
        gi[a][a] * gi[b][b] * Ric[a][b] * Ric[a][b]
        for a in range(D) for b in range(D)
    )
    riemann_sq = sum(
        gi[a][a] * gi[b][b] * gi[c][c] * gi[d][d] * Rlow[a][b][c][d] ** 2
        for a in range(D) for b in range(D) for c in range(D) for d in range(D)
    )
    weyl_sq = riemann_sq - 2 * ricci_sq + scalar * scalar / 3
    return g, gi, Gamma, Rlow, Ric, scalar, riemann_sq, weyl_sq


def dot4(g, u, v):
    return sum(g[a][b] * u[a] * v[b] for a in range(D) for b in range(D))


def tidal(Rlow, left, kvec, right):
    return sum(
        Rlow[a][b][c][d] * left[a] * kvec[b] * right[c] * kvec[d]
        for a in range(D) for b in range(D) for c in range(D) for d in range(D)
    )


def eval_poly(coeffs: dict[int, F], r: F, derivative: int = 0) -> F:
    total = Z
    for power, coeff in coeffs.items():
        if power < derivative:
            continue
        multiplier = 1
        for j in range(derivative):
            multiplier *= power - j
        total += coeff * multiplier * r ** (power - derivative)
    return total


def polynomial_maps():
    # Mechanical coefficient-map derivation from differentiation and linear
    # polynomial operations; no production artifact is read.
    maps = {}
    for k in range(1, 5):
        power = 2 * k
        f = {0: F(1), power: F(1)}
        fp = {p - 1: F(p) * c for p, c in f.items() if p >= 1}
        fpp = {p - 1: F(p) * c for p, c in fp.items() if p >= 1}
        apar = {}
        aperp = {0: F(1)}
        scalar_numerator = {0: F(-2)}
        for p, c in fpp.items():
            apar[p + 2] = apar.get(p + 2, Z) + H * c
            scalar_numerator[p + 2] = scalar_numerator.get(p + 2, Z) + c
        for p, c in fp.items():
            apar[p + 1] = apar.get(p + 1, Z) - H * c
            aperp[p + 1] = aperp.get(p + 1, Z) + H * c
            scalar_numerator[p + 1] = scalar_numerator.get(p + 1, Z) + 4 * c
        for p, c in f.items():
            aperp[p] = aperp.get(p, Z) - c
            scalar_numerator[p] = scalar_numerator.get(p, Z) + 2 * c
        maps[k] = {
            "apar": {p: c for p, c in apar.items() if c},
            "aperp": {p: c for p, c in aperp.items() if c},
            "scalar_numerator": {p: c for p, c in scalar_numerator.items() if c},
        }
    return maps


def main() -> None:
    rng = random.Random(28820260828)
    assertions = 0
    cases = 1000
    signs = set()

    maps = polynomial_maps()
    expected = {
        1: (Z, Z, F(12)),
        2: (F(4), F(1), F(30)),
        3: (F(12), F(2), F(56)),
        4: (F(24), F(3), F(90)),
    }
    for k, (ap, at, sc) in expected.items():
        power = 2 * k
        assert maps[k]["apar"].get(power, Z) == ap
        assert maps[k]["aperp"].get(power, Z) == at
        # Scalar numerator is divided by r^2 and negated.
        assert maps[k]["scalar_numerator"].get(power, Z) == sc
        assert maps[k]["scalar_numerator"].get(0, Z) == 0
        assertions += 4

    ca, sa = F(3, 5), F(4, 5)
    for i in range(cases):
        r = F(rng.randint(1, 7), rng.randint(1, 7))
        c2 = F(rng.choice((-1, 1)) * rng.randint(1, 9), rng.randint(5, 17))
        c4 = F(rng.randint(-9, 9), rng.randint(5, 19))
        c6 = F(rng.randint(-7, 7), rng.randint(5, 19))
        # Force the metric value at the test event to a positive rational square
        # while leaving the center coefficients otherwise nondegenerate.
        rootf = F(rng.randint(2, 11), rng.randint(2, 9))
        c8 = (rootf * rootf - 1 - c2 * r**2 - c4 * r**4 - c6 * r**6) / r**8
        coeffs = {0: F(1), 2: c2, 4: c4, 6: c6, 8: c8}
        f = eval_poly(coeffs, r)
        fp = eval_poly(coeffs, r, 1)
        fpp = eval_poly(coeffs, r, 2)
        assert f == rootf * rootf and f > 0
        assertions += 1
        signs.add(1 if c2 > 0 else -1)

        g, gi, Gamma, Rlow, Ric, scalar, riemann_sq, weyl_sq = geometry(r, f, fp, fpp)
        U = (1 / rootf, Z, Z, Z)
        er = (Z, rootf, Z, Z)
        etheta = (Z, Z, 1 / r, Z)
        evarphi = (Z, Z, Z, 1 / r)
        kvec = tuple(U[j] + ca * er[j] + sa * evarphi[j] for j in range(D))
        spar = tuple(-sa * er[j] + ca * evarphi[j] for j in range(D))
        sperp = etheta

        assert dot4(g, kvec, kvec) == 0
        assert dot4(g, spar, spar) == 1
        assert dot4(g, sperp, sperp) == 1
        assert dot4(g, spar, kvec) == 0
        assert dot4(g, sperp, kvec) == 0
        assertions += 5

        tpar = tidal(Rlow, spar, kvec, spar)
        tperp = tidal(Rlow, sperp, kvec, sperp)
        toff = tidal(Rlow, spar, kvec, sperp)
        apar_tensor = r * r * tpar / (sa * sa)
        aperp_tensor = r * r * tperp / (sa * sa)
        apar_poly = sum(2 * k * (k - 1) * coeffs[2 * k] * r ** (2 * k) for k in range(1, 5))
        aperp_poly = sum((k - 1) * coeffs[2 * k] * r ** (2 * k) for k in range(1, 5))
        scalar_poly = -sum(
            2 * (2 * k + 1) * (k + 1) * coeffs[2 * k] * r ** (2 * k - 2)
            for k in range(1, 5)
        )
        assert apar_tensor == apar_poly
        assert aperp_tensor == aperp_poly
        assert toff == 0
        assert scalar == scalar_poly
        assertions += 4

        # Acceleration is obtained from the rebuilt connection, not assumed.
        acc_r = Gamma[1][0][0] / f
        acc_hat = acc_r / rootf
        assert acc_hat == fp / (2 * rootf)
        mu = r * (1 - f) / 2
        assert f == 1 - 2 * mu / r
        # Radial null vector U+er has dr/dx0=f and normalized speed one.
        krad = tuple(U[j] + er[j] for j in range(D))
        assert dot4(g, krad, krad) == 0
        assert krad[1] / krad[0] == f
        assert (krad[1] / rootf) / (rootf * krad[0]) == 1
        assertions += 5

        # Invariant formula reconstructed from the full tensor contraction.
        bracket = r * r * fpp - 2 * r * fp + 2 * f - 2
        assert weyl_sq == bracket * bracket / (3 * r**4)
        assertions += 1

    assert signs == {-1, 1}
    assertions += 1

    # Exact quadratic controls, independently rebuilt from the metric tensor.
    quadratic_cases = 100
    for _ in range(quadratic_cases):
        r = F(rng.randint(1, 9), rng.randint(1, 9))
        rootf = F(rng.randint(2, 13), rng.randint(2, 7))
        C = (rootf * rootf - 1) / (r * r)
        f, fp, fpp = 1 + C * r * r, 2 * C * r, 2 * C
        g, gi, Gamma, Rlow, Ric, scalar, riemann_sq, weyl_sq = geometry(r, f, fp, fpp)
        U = (1 / rootf, Z, Z, Z)
        er = (Z, rootf, Z, Z)
        etheta = (Z, Z, 1 / r, Z)
        evarphi = (Z, Z, Z, 1 / r)
        kvec = tuple(U[j] + ca * er[j] + sa * evarphi[j] for j in range(D))
        spar = tuple(-sa * er[j] + ca * evarphi[j] for j in range(D))
        assert tidal(Rlow, spar, kvec, spar) == 0
        assert tidal(Rlow, etheta, kvec, etheta) == 0
        assert scalar == -12 * C
        assert riemann_sq == 24 * C * C
        assert weyl_sq == 0
        for a in range(D):
            for b in range(D):
                assert Ric[a][b] == -3 * C * g[a][b]
                assertions += 1
        assertions += 5

    result = {
        "status": "PASS",
        "implementation": "standard-library Fraction metric-two-jet connection-curvature-screen rebuild",
        "imports_production_module": False,
        "reads_production_result": False,
        "general_cases": cases,
        "quadratic_controls": quadratic_cases,
        "assertions": assertions,
        "c2_signs_covered": sorted(signs),
        "polynomial_maps": {
            str(k): {name: {str(p): str(c) for p, c in values.items()} for name, values in maps[k].items()}
            for k in maps
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
