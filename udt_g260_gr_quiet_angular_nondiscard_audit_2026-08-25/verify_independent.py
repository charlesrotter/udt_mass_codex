#!/usr/bin/env python3
"""Independent exact-rational G260 tensor replay; no production import/result read."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")


def zeros(*shape: int):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def diagonal_inverse(g):
    n = len(g)
    inverse = zeros(n, n)
    for i in range(n):
        assert g[i][i] != 0
        assert all(g[i][j] == 0 for j in range(n) if j != i)
        inverse[i][i] = 1 / g[i][i]
    return inverse


def einstein_from_metric_jets(g, dg, ddg):
    n = len(g)
    gi = diagonal_inverse(g)
    dgi = zeros(n, n, n)
    for a in range(n):
        for b in range(n):
            for e in range(n):
                dgi[a][b][e] = -sum(
                    gi[a][m] * dg[m][q][e] * gi[q][b]
                    for m in range(n)
                    for q in range(n)
                )

    gamma = zeros(n, n, n)
    dgamma = zeros(n, n, n, n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                first = [dg[d][c][b] + dg[d][b][c] - dg[b][c][d] for d in range(n)]
                gamma[a][b][c] = sum(gi[a][d] * first[d] for d in range(n)) / 2
                for e in range(n):
                    second = [
                        ddg[d][c][b][e] + ddg[d][b][c][e] - ddg[b][c][d][e]
                        for d in range(n)
                    ]
                    dgamma[a][b][c][e] = (
                        sum(dgi[a][d][e] * first[d] for d in range(n))
                        + sum(gi[a][d] * second[d] for d in range(n))
                    ) / 2

    ricci = zeros(n, n)
    for a in range(n):
        for b in range(n):
            ricci[a][b] = sum(
                dgamma[c][a][b][c]
                - dgamma[c][a][c][b]
                + sum(
                    gamma[c][c][d] * gamma[d][a][b]
                    - gamma[c][b][d] * gamma[d][a][c]
                    for d in range(n)
                )
                for c in range(n)
            )
    scalar = sum(gi[a][b] * ricci[a][b] for a in range(n) for b in range(n))
    einstein_cov = zeros(n, n)
    einstein_mix = zeros(n, n)
    for a in range(n):
        for b in range(n):
            einstein_cov[a][b] = ricci[a][b] - g[a][b] * scalar / 2
            einstein_mix[a][b] = sum(gi[a][c] * einstein_cov[c][b] for c in range(n))
    return ricci, einstein_mix, scalar


def four_metric_jets(r: F, f: F, fp: F, fpp: F, spherical: bool):
    n = 4
    g = zeros(n, n)
    dg = zeros(n, n, n)
    ddg = zeros(n, n, n, n)
    g[0][0] = -f
    g[1][1] = 1 / f
    g[2][2] = r**2
    g[3][3] = r**2
    dg[0][0][1] = -fp
    dg[1][1][1] = -fp / f**2
    dg[2][2][1] = 2 * r
    dg[3][3][1] = 2 * r
    ddg[0][0][1][1] = -fpp
    ddg[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    ddg[2][2][1][1] = 2
    ddg[3][3][1][1] = 2
    if spherical:
        # Equatorial value of d_theta^2(r^2 sin^2 theta).
        ddg[3][3][2][2] = -2 * r**2
    return g, dg, ddg


def two_metric_jets(f: F, fp: F, fpp: F):
    n = 2
    g = zeros(n, n)
    dg = zeros(n, n, n)
    ddg = zeros(n, n, n, n)
    g[0][0] = -f
    g[1][1] = 1 / f
    dg[0][0][1] = -fp
    dg[1][1][1] = -fp / f**2
    ddg[0][0][1][1] = -fpp
    ddg[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    return g, dg, ddg


def main() -> None:
    rng = random.Random(260)
    assertions = 0
    arbitrary_cases = 0
    for _ in range(700):
        r = F(rng.randint(2, 40), rng.randint(1, 7))
        f = F(rng.randint(1, 40), rng.randint(1, 9))
        fp = F(rng.randint(-20, 20), rng.randint(1, 9))
        fpp = F(rng.randint(-20, 20), rng.randint(1, 9))

        _, sphere_einstein, _ = einstein_from_metric_jets(*four_metric_jets(r, f, fp, fpp, True))
        expected_e0 = r * fp + f - 1
        expected_e1 = r * fp + r**2 * fpp / 2
        assert r**2 * sphere_einstein[0][0] == expected_e0
        assert r**2 * sphere_einstein[1][1] == expected_e0
        assert r**2 * sphere_einstein[2][2] == expected_e1
        assert r**2 * sphere_einstein[3][3] == expected_e1
        assert all(sphere_einstein[i][j] == 0 for i in range(4) for j in range(4) if i != j)
        assertions += 5

        a_parallel = (r**2 * fpp - r * fp) / 2
        a_perp = 1 - f + r * fp / 2
        assert a_parallel + a_perp == expected_e1 - expected_e0
        assertions += 1

        _, flat_einstein, _ = einstein_from_metric_jets(*four_metric_jets(r, f, fp, fpp, False))
        assert r**2 * flat_einstein[0][0] == r * fp + f
        assert r**2 * flat_einstein[1][1] == r * fp + f
        assertions += 2

        _, base_einstein, _ = einstein_from_metric_jets(*two_metric_jets(f, fp, fpp))
        assert all(base_einstein[i][j] == 0 for i in range(2) for j in range(2))
        assertions += 1
        arbitrary_cases += 1

    vacuum_cases = 0
    for _ in range(500):
        r = F(rng.randint(3, 60), rng.randint(1, 8))
        c = F(rng.randint(-20, 20), rng.randint(1, 8))
        if c == 0 or 1 + c / r <= 0:
            continue
        f = 1 + c / r
        fp = -c / r**2
        fpp = 2 * c / r**3
        ricci, einstein, _ = einstein_from_metric_jets(*four_metric_jets(r, f, fp, fpp, True))
        assert all(ricci[i][j] == 0 for i in range(4) for j in range(4))
        assert all(einstein[i][j] == 0 for i in range(4) for j in range(4))
        a_parallel = (r**2 * fpp - r * fp) / 2
        a_perp = 1 - f + r * fp / 2
        assert a_parallel == 3 * c / (2 * r)
        assert a_perp == -3 * c / (2 * r)
        assert a_parallel != 0 and a_perp != 0 and a_parallel + a_perp == 0
        _, flat_einstein, _ = einstein_from_metric_jets(*four_metric_jets(r, f, fp, fpp, False))
        assert r**2 * flat_einstein[0][0] == 1
        assertions += 6
        vacuum_cases += 1

    balanced_cases = 0
    for _ in range(500):
        r = F(rng.randint(2, 50), rng.randint(1, 8))
        a = F(rng.randint(-8, 8), rng.randint(1, 8))
        b = F(rng.randint(-8, 8), rng.randint(1, 8))
        f = 1 + a * r**2 + b / r
        if f <= 0:
            continue
        fp = 2 * a * r - b / r**2
        fpp = 2 * a + 2 * b / r**3
        e0 = r * fp + f - 1
        e1 = r * fp + r**2 * fpp / 2
        a_parallel = (r**2 * fpp - r * fp) / 2
        a_perp = 1 - f + r * fp / 2
        assert a_parallel + a_perp == 0
        assert e0 == 3 * a * r**2
        assert e1 == 3 * a * r**2
        if a != 0:
            assert e0 != 0
        assertions += 4
        balanced_cases += 1

    result = {
        "status": "PASS",
        "method": "independent exact-rational Christoffel-Ricci-Einstein reconstruction from metric two-jets at an equatorial event",
        "production_imported": False,
        "production_result_read": False,
        "arbitrary_metric_jet_cases": arbitrary_cases,
        "vacuum_family_cases": vacuum_cases,
        "balanced_trace_cases": balanced_cases,
        "assertions": assertions,
        "verified": [
            "full four-dimensional sphere residuals",
            "A_parallel+A_perp=E1-E0",
            "nonzero cancelling angular amplitudes on f=1+C/r",
            "isolated two-dimensional Einstein tensor is identically zero",
            "flat-screen corruption rejects the spherical vacuum family",
            "complete trace-balanced family f=1+a*r^2+b/r",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
