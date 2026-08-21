#!/usr/bin/env python3
"""Independent exact-rational metric-jet replay for G199.

This implementation imports neither SymPy nor the production module.  It reconstructs the
Levi-Civita connection and Riemann tensor at equatorial points from exact first and second metric
jets and contracts both radial null signs.
"""

from fractions import Fraction as F
import json
import random


N = 4


def zeros(*shape):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def inverse_diagonal(g):
    out = zeros(N, N)
    for i in range(N):
        out[i][i] = F(1) / g[i][i]
    return out


def metric_jets(r, f, fp, fpp):
    # Coordinates: (x0,r,theta,varphi), evaluated at theta=pi/2.
    g = zeros(N, N)
    dg = zeros(N, N, N)
    ddg = zeros(N, N, N, N)
    g[0][0] = -f
    g[1][1] = F(1) / f
    g[2][2] = r * r
    g[3][3] = r * r

    dg[0][0][1] = -fp
    dg[1][1][1] = -fp / (f * f)
    dg[2][2][1] = 2 * r
    dg[3][3][1] = 2 * r

    ddg[0][0][1][1] = -fpp
    ddg[1][1][1][1] = 2 * fp * fp / (f**3) - fpp / (f * f)
    ddg[2][2][1][1] = F(2)
    ddg[3][3][1][1] = F(2)
    ddg[3][3][2][2] = -2 * r * r
    return g, dg, ddg


def connection_and_riemann(g, dg, ddg):
    gi = inverse_diagonal(g)
    dgi = zeros(N, N, N)
    for a in range(N):
        for b in range(N):
            for ell in range(N):
                dgi[a][b][ell] = -sum(
                    gi[a][e] * dg[e][q][ell] * gi[q][b]
                    for e in range(N) for q in range(N)
                )

    gamma = zeros(N, N, N)
    dgamma = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                gamma[a][b][c] = F(1, 2) * sum(
                    gi[a][d] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d])
                    for d in range(N)
                )
                for ell in range(N):
                    dgamma[a][b][c][ell] = F(1, 2) * sum(
                        dgi[a][d][ell] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d])
                        + gi[a][d] * (
                            ddg[d][c][b][ell]
                            + ddg[d][b][c][ell]
                            - ddg[b][c][d][ell]
                        )
                        for d in range(N)
                    )

    # R^a_{bcd}=partial_c Gamma^a_{db}-partial_d Gamma^a_{cb}+...
    riemann = zeros(N, N, N, N)
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    riemann[a][b][c][d] = (
                        dgamma[a][d][b][c]
                        - dgamma[a][c][b][d]
                        + sum(
                            gamma[a][c][e] * gamma[e][d][b]
                            - gamma[a][d][e] * gamma[e][c][b]
                            for e in range(N)
                        )
                    )
    return gi, gamma, riemann


def contract_tide(g, riemann, k, screens):
    tide = zeros(2, 2)
    for aa, sa in enumerate(screens):
        for bb, sb in enumerate(screens):
            tide[aa][bb] = sum(
                g[mu][nu] * sa[mu] * riemann[nu][alpha][beta][rho]
                * k[alpha] * sb[beta] * k[rho]
                for mu in range(N) for nu in range(N)
                for alpha in range(N) for beta in range(N) for rho in range(N)
            )
    return tide


def main():
    rng = random.Random(199)
    cases = 2000
    assertions = 0
    nonflat = 0
    sign_pairs = 0
    for _ in range(cases):
        r = F(rng.randint(2, 19), rng.randint(1, 7))
        f = F(rng.randint(1, 17), rng.randint(1, 9))
        fp = F(rng.randint(-13, 13), rng.randint(1, 11))
        fpp = F(rng.randint(-13, 13), rng.randint(1, 11))
        if fp == 0 and fpp == 0:
            fp = F(1, 3)
        energy = F(rng.randint(1, 11), rng.randint(1, 7))
        g, dg, ddg = metric_jets(r, f, fp, fpp)
        _, gamma, riemann = connection_and_riemann(g, dg, ddg)
        screens = ([F(0), F(0), F(1) / r, F(0)],
                   [F(0), F(0), F(0), F(1) / r])
        tides = []
        for sign in (1, -1):
            k = [energy / f, sign * energy, F(0), F(0)]
            null = sum(g[a][b] * k[a] * k[b] for a in range(N) for b in range(N))
            assert null == 0
            assertions += 1
            tide = contract_tide(g, riemann, k, screens)
            assert tide == [[F(0), F(0)], [F(0), F(0)]]
            assertions += 4
            tides.append(tide)
        assert tides[0] == tides[1]
        assertions += 4
        sign_pairs += 1

        # The zero optical tide is not a flat-metric shortcut.
        if any(riemann[a][b][c][d] != 0
               for a in range(N) for b in range(N)
               for c in range(N) for d in range(N)):
            nonflat += 1
        # Coordinate screen vectors are parallel along both radial signs.
        for sign in (1, -1):
            k = [energy / f, sign * energy, F(0), F(0)]
            for screen in screens:
                for a in range(N):
                    directional = -sign * energy / (r * r) if (
                        (a == 2 and screen[2] != 0) or (a == 3 and screen[3] != 0)
                    ) else F(0)
                    connection = sum(
                        gamma[a][b][c] * k[b] * screen[c]
                        for b in range(N) for c in range(N)
                    )
                    assert directional + connection == 0
                    assertions += 1

    assert nonflat == cases
    print(json.dumps({
        "all_pass": True,
        "cases": cases,
        "assertions": assertions,
        "nonflat_cases": nonflat,
        "opposite_sign_pairs": sign_pairs,
        "method": "independent exact-Fraction metric two-jet reconstruction",
        "production_imports": False,
        "production_artifacts_read": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
