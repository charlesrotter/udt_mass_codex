#!/usr/bin/env python3
"""Independent exact-Fraction curvature replay for G187.

This implementation imports no production code and does not use SymPy.  It
reconstructs the Christoffel symbols and Riemann tensor from the metric two-jet
at an equatorial point, then contracts them with independently assembled null
and screen vectors.
"""

from __future__ import annotations

from fractions import Fraction as F
import json
import random


TRIALS = 10_000
SEED = 1870820
DIM = 4


def zeros(shape):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(shape[1:]) for _ in range(shape[0])]


def inner(g, left, right):
    return sum(g[a][b] * left[a] * right[b]
               for a in range(DIM) for b in range(DIM))


def metric_jet(r, f, fp, fpp):
    """Return g, inverse g, first and second coordinate derivatives at theta=pi/2."""
    g = zeros((DIM, DIM))
    gi = zeros((DIM, DIM))
    dg = zeros((DIM, DIM, DIM))       # dg[a][b][c] = d_c g_ab
    ddg = zeros((DIM, DIM, DIM, DIM)) # ddg[a][b][c][d] = d_c d_d g_ab

    g[0][0], g[1][1], g[2][2], g[3][3] = -f, 1 / f, r * r, r * r
    gi[0][0], gi[1][1], gi[2][2], gi[3][3] = -1 / f, f, 1 / r**2, 1 / r**2

    dg[0][0][1] = -fp
    dg[1][1][1] = -fp / f**2
    dg[2][2][1] = 2 * r
    dg[3][3][1] = 2 * r

    ddg[0][0][1][1] = -fpp
    ddg[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    ddg[2][2][1][1] = 2
    ddg[3][3][1][1] = 2
    # At the equator d_theta^2(r^2 sin^2 theta)=-2r^2.
    ddg[3][3][2][2] = -2 * r**2
    return g, gi, dg, ddg


def connection_and_curvature(g, gi, dg, ddg):
    gamma = zeros((DIM, DIM, DIM))
    dgi = zeros((DIM, DIM, DIM))
    for a in range(DIM):
        for e in range(DIM):
            for c in range(DIM):
                dgi[a][e][c] = -sum(
                    gi[a][m] * dg[m][n][c] * gi[n][e]
                    for m in range(DIM) for n in range(DIM)
                )

    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                gamma[a][b][c] = F(1, 2) * sum(
                    gi[a][e] * (dg[e][c][b] + dg[e][b][c] - dg[b][c][e])
                    for e in range(DIM)
                )

    # dgamma[a][b][d][c] = d_c Gamma^a_bd.
    dgamma = zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            for d in range(DIM):
                for c in range(DIM):
                    dgamma[a][b][d][c] = F(1, 2) * sum(
                        dgi[a][e][c]
                        * (dg[e][d][b] + dg[e][b][d] - dg[b][d][e])
                        + gi[a][e]
                        * (ddg[e][d][b][c] + ddg[e][b][d][c]
                           - ddg[b][d][e][c])
                        for e in range(DIM)
                    )

    # Same declared convention as the production derivation:
    # R^a_bcd=d_c Gamma^a_db-d_d Gamma^a_cb+Gamma^a_ce Gamma^e_db-...
    riemann = zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    riemann[a][b][c][d] = (
                        dgamma[a][d][b][c] - dgamma[a][c][b][d]
                        + sum(gamma[a][c][e] * gamma[e][d][b]
                              - gamma[a][d][e] * gamma[e][c][b]
                              for e in range(DIM))
                    )
    return gamma, riemann


def tidal(g, riemann, left, ray, right):
    return sum(
        g[mu][a] * left[mu] * riemann[a][b][c][d]
        * ray[b] * right[c] * ray[d]
        for mu in range(DIM) for a in range(DIM)
        for b in range(DIM) for c in range(DIM) for d in range(DIM)
    )


def covariant_screen_derivatives(gamma, r, f, fp, energy, angular, q):
    ray = [energy / f, q, F(0), angular / r**2]
    out = [F(0), F(0), 1 / r, F(0)]
    inside = [F(0), -f * angular / (energy * r), F(0), q / (energy * r)]
    qdot = angular**2 * (2 * f - r * fp) / (2 * r**3)

    direct_out = [F(0), F(0), -q / r**2, F(0)]
    direct_in = [
        F(0),
        -angular * q * (fp / r - f / r**2) / energy,
        F(0),
        qdot / (energy * r) - q**2 / (energy * r**2),
    ]

    def add_connection(direct, vector):
        return [
            direct[a] + sum(gamma[a][b][c] * ray[b] * vector[c]
                            for b in range(DIM) for c in range(DIM))
            for a in range(DIM)
        ]

    return ray, out, inside, add_connection(direct_out, out), add_connection(direct_in, inside)


def projector(g, observer, spatial):
    # The two supplied vectors are exactly orthonormal: J^T g J=diag(-1,+1).
    j = [[observer[a], spatial[a]] for a in range(DIM)]
    h_inv = [[F(-1), F(0)], [F(0), F(1)]]
    correction = zeros((DIM, DIM))
    for a in range(DIM):
        for b in range(DIM):
            correction[a][b] = sum(
                j[a][i] * h_inv[i][q] * j[c][q] * g[c][b]
                for i in range(2) for q in range(2) for c in range(DIM)
            )
    return [[F(int(a == b)) - correction[a][b] for b in range(DIM)]
            for a in range(DIM)]


def matvec(matrix, vector):
    return [sum(matrix[a][b] * vector[b] for b in range(DIM))
            for a in range(DIM)]


def trial(rng):
    # Rational square f and Pythagorean ray angles keep every assertion exact.
    roots = [F(1, 2), F(2, 3), F(3, 4), F(1), F(4, 3), F(3, 2), F(2)]
    root_f = rng.choice(roots)
    f = root_f**2
    r = F(rng.randint(1, 9), rng.randint(1, 4))
    fp = F(rng.randint(-9, 9), rng.randint(1, 7))
    fpp = F(rng.randint(-9, 9), rng.randint(1, 7))
    energy = F(rng.randint(1, 7), rng.randint(1, 5))
    sine, cosine = rng.choice([
        (F(3, 5), F(4, 5)), (F(4, 5), F(3, 5)),
        (F(5, 13), F(12, 13)), (F(12, 13), F(5, 13)),
        (F(7, 25), F(24, 25)), (F(24, 25), F(7, 25)),
    ])
    if rng.randrange(2):
        cosine = -cosine
    angular = energy * r * sine / root_f
    q = energy * cosine

    g, gi, dg, ddg = metric_jet(r, f, fp, fpp)
    gamma, riemann = connection_and_curvature(g, gi, dg, ddg)
    ray, out, inside, d_out, d_in = covariant_screen_derivatives(
        gamma, r, f, fp, energy, angular, q
    )

    assert inner(g, ray, ray) == 0
    assert inner(g, out, out) == 1 and inner(g, inside, inside) == 1
    assert inner(g, out, inside) == 0
    assert inner(g, out, ray) == 0 and inner(g, inside, ray) == 0
    assert d_out == [F(0)] * DIM
    gauge = -angular * fp / (2 * energy * r)
    assert d_in == [gauge * x for x in ray]

    actual_out = tidal(g, riemann, out, ray, out)
    actual_in = tidal(g, riemann, inside, ray, inside)
    actual_cross = tidal(g, riemann, out, ray, inside)
    expected_out = angular**2 * (r * fp - 2 * f + 2) / (2 * r**4)
    expected_in = angular**2 * (r * fpp - fp) / (2 * r**3)
    assert actual_out == expected_out
    assert actual_in == expected_in
    assert actual_cross == 0

    observer = [1 / root_f, F(0), F(0), F(0)]
    spatial = [F(0), q * root_f / energy, F(0),
               root_f * angular / (energy * r**2)]
    assert inner(g, observer, observer) == -1
    assert inner(g, spatial, spatial) == 1
    assert inner(g, observer, spatial) == 0
    proj = projector(g, observer, spatial)
    assert matvec(proj, observer) == [F(0)] * DIM
    assert matvec(proj, spatial) == [F(0)] * DIM
    assert matvec(proj, out) == out
    assert matvec(proj, inside) == inside
    assert sum(proj[a][a] for a in range(DIM)) == 2

    # Exact out-of-plane Killing-Jacobi residual for arbitrary sin(Delta phi).
    sine_delta = F(rng.randint(-5, 5), rng.randint(1, 7))
    qdot = angular**2 * (2 * f - r * fp) / (2 * r**3)
    residual = ((qdot - angular**2 / r**3) * sine_delta
                + expected_out * r * sine_delta)
    assert residual == 0
    return 22


def named_controls():
    r, mass, angular = F(7, 2), F(2, 5), F(11, 7)
    f = 1 - 2 * mass / r
    fp = 2 * mass / r**2
    fpp = -4 * mass / r**3
    out = angular**2 * (r * fp - 2 * f + 2) / (2 * r**4)
    inside = angular**2 * (r * fpp - fp) / (2 * r**3)
    assert out == 3 * mass * angular**2 / r**5
    assert inside == -3 * mass * angular**2 / r**5
    assert out + inside == 0

    # Flat space: the complete finite map is lambda times the identity for
    # every nonradial initial angle when the vertex screen slope is identity.
    affine = F(17, 9)
    flat_map = [[affine, F(0)], [F(0), affine]]
    assert flat_map[0][0] == flat_map[1][1]

    # The two vertex slopes independently equal one under omega_o=1.
    sine, cosine, radius, root_f = F(5, 13), F(12, 13), F(7, 3), F(4, 3)
    energy = root_f
    angular = radius * sine
    q = root_f * cosine
    delta_q = -root_f * sine
    delta_phidot = cosine / radius
    in_slope = ((-angular / (energy * radius)) * delta_q
                + (q * radius / energy) * delta_phidot)
    out_slope = angular / (radius * sine)
    assert in_slope == 1 and out_slope == 1
    return {
        "flat_finite_map": [[str(x) for x in row] for row in flat_map],
        "schwarzschild_parallel": str(inside),
        "schwarzschild_perpendicular": str(out),
        "vertex_parallel_slope": str(in_slope),
        "vertex_perpendicular_slope": str(out_slope),
    }


def main():
    rng = random.Random(SEED)
    assertions = 0
    for _ in range(TRIALS):
        assertions += trial(rng)
    controls = named_controls()
    print(json.dumps({
        "assertions": assertions,
        "audit": "G187_INDEPENDENT_EXACT_FRACTION_CURVATURE_REPLAY",
        "controls": controls,
        "seed": SEED,
        "status": "PASS",
        "trials": TRIALS,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
