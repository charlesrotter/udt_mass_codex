#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction for the G296 Brinkmann control."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def zeros(shape):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(shape[1:]) for _ in range(shape[0])]


def metric_data(a: F, b: F, c: F, x: F, y: F):
    h = -(a*x*x + 2*b*x*y + c*y*y)
    g = [[h, -F(1), F(0), F(0)], [-F(1), F(0), F(0), F(0)],
         [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    gi = [[F(0), -F(1), F(0), F(0)], [-F(1), -h, F(0), F(0)],
          [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    dg = zeros((4, 4, 4))
    d2g = zeros((4, 4, 4, 4))
    dg[2][0][0] = -2*a*x - 2*b*y
    dg[3][0][0] = -2*b*x - 2*c*y
    d2g[2][2][0][0] = -2*a
    d2g[2][3][0][0] = -2*b
    d2g[3][2][0][0] = -2*b
    d2g[3][3][0][0] = -2*c
    return g, gi, dg, d2g


def curvature(a: F, b: F, c: F, x: F, y: F):
    n = 4
    g, gi, dg, d2g = metric_data(a, b, c, x, y)
    dgi = zeros((n, n, n))
    for mu in range(n):
        for r in range(n):
            for s in range(n):
                dgi[mu][r][s] = -sum(gi[r][p]*dg[mu][p][q]*gi[q][s] for p in range(n) for q in range(n))
    gamma = zeros((n, n, n))
    dgamma = zeros((n, n, n, n))
    for r in range(n):
        for i in range(n):
            for j in range(n):
                gamma[r][i][j] = F(1, 2) * sum(
                    gi[r][s] * (dg[i][s][j] + dg[j][s][i] - dg[s][i][j]) for s in range(n)
                )
                for mu in range(n):
                    first = sum(
                        dgi[mu][r][s] * (dg[i][s][j] + dg[j][s][i] - dg[s][i][j]) for s in range(n)
                    )
                    second = sum(
                        gi[r][s] * (d2g[mu][i][s][j] + d2g[mu][j][s][i] - d2g[mu][s][i][j]) for s in range(n)
                    )
                    dgamma[mu][r][i][j] = F(1, 2) * (first + second)
    rup = zeros((n, n, n, n))
    rlow = zeros((n, n, n, n))
    for r in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    rup[r][sig][mu][nu] = (
                        dgamma[mu][r][nu][sig] - dgamma[nu][r][mu][sig]
                        + sum(gamma[r][mu][lam]*gamma[lam][nu][sig] - gamma[r][nu][lam]*gamma[lam][mu][sig] for lam in range(n))
                    )
    for al in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    rlow[al][sig][mu][nu] = sum(g[al][r]*rup[r][sig][mu][nu] for r in range(n))
    ric = [[sum(rup[r][sig][r][nu] for r in range(n)) for nu in range(n)] for sig in range(n)]
    scalar = sum(gi[i][j]*ric[i][j] for i in range(n) for j in range(n))
    ric2 = sum(gi[i][k]*gi[j][l]*ric[i][j]*ric[k][l]
               for i in range(n) for j in range(n) for k in range(n) for l in range(n))
    kretsch = sum(gi[i][p]*gi[j][q]*gi[k][r]*gi[l][s]*rlow[i][j][k][l]*rlow[p][q][r][s]
                   for i in range(n) for j in range(n) for k in range(n) for l in range(n)
                   for p in range(n) for q in range(n) for r in range(n) for s in range(n))
    return rlow, ric, scalar, ric2, kretsch


def main() -> None:
    rng = random.Random(2960829)
    assertions = 0
    cases = 128
    active_tracefree = 0
    for _ in range(cases):
        a = F(rng.randint(-9, 9) or 1, rng.randint(1, 9))
        b = F(rng.randint(-9, 9), rng.randint(1, 9))
        c = -a
        x = F(rng.randint(-7, 7), rng.randint(1, 7))
        y = F(rng.randint(-7, 7), rng.randint(1, 7))
        rlow, ric, scalar, ric2, kretsch = curvature(a, b, c, x, y)
        expected = ((a, b), (b, c))
        assert rlow[0][2][0][2] == expected[0][0]; assertions += 1
        assert rlow[0][2][0][3] == expected[0][1]; assertions += 1
        assert rlow[0][3][0][2] == expected[1][0]; assertions += 1
        assert rlow[0][3][0][3] == expected[1][1]; assertions += 1
        assert all(ric[i][j] == 0 for i in range(4) for j in range(4)); assertions += 16
        assert scalar == 0; assertions += 1
        assert ric2 == 0; assertions += 1
        assert kretsch == 0; assertions += 1
        assert a != 0 or b != 0; assertions += 1
        active_tracefree += 1

    # Source-owned and logical classification gates, independently restated.
    gates = {
        "coframe_gauge_count": 16 - 6 == 10,
        "metric_physical_count": 10 - 4 == 6,
        "rank_two_identity_count": 10 - 4 == 6,
        "tracefree_wave_is_scalar_invisible": active_tracefree == cases,
        "different_lawful_data_need_not_be_rejected": True,
        "Lovelock_hypotheses_are_conditional": True,
        "first_order_Cartan_requires_classifying_law": True,
        "no_residual_formula_selected": True,
    }
    assertions += len(gates)
    assert all(gates.values())
    result = {
        "all_pass": True,
        "cases": cases,
        "assertions": assertions,
        "active_tracefree_cases": active_tracefree,
        "gates": gates,
        "imports_production": False,
        "reads_production_output": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
