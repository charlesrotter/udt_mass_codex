#!/usr/bin/env python3
"""Exact full-metric reconstruction for the preregistered G196 family."""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp


def simp(value):
    return sp.factor(sp.simplify(sp.trigsimp(value)))


eta, z, p, w = sp.symbols("eta z p w", real=True)
coords = (eta, z, p, w)
dim = 4
lorentz = sp.diag(-1, 1, 1, 1)

a = sp.Function("a", positive=True)(eta)
A = sp.Function("A", real=True)(eta, z)
N = sp.Function("N", real=True)(eta, z)
B = sp.Function("B", real=True)(eta, z)
R = sp.Function("R", real=True)(eta, z)
M = sp.Matrix([[A, N + R], [N - R, B]])


def central(value):
    substitutions = {p: 0, w: 0}
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs(substitutions)))
    return simp(value.subs(substitutions))


def dplus(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(sp.diff(entry, eta) + sp.diff(entry, z)))
    return simp(sp.diff(value, eta) + sp.diff(value, z))


def inner(metric, left, right):
    return simp((left.T * metric * right)[0])


def make_christoffel(metric, inverse):
    @lru_cache(maxsize=None)
    def component(aa, bb, cc):
        return sp.Rational(1, 2) * sum(
            inverse[aa, dd]
            * (
                sp.diff(metric[dd, cc], coords[bb])
                + sp.diff(metric[dd, bb], coords[cc])
                - sp.diff(metric[bb, cc], coords[dd])
            )
            for dd in range(dim)
        )

    return component


def riemann_component(gamma, aa, bb, cc, dd):
    return simp(
        sp.diff(gamma(aa, dd, bb), coords[cc])
        - sp.diff(gamma(aa, cc, bb), coords[dd])
        + sum(
            gamma(aa, cc, ee) * gamma(ee, dd, bb)
            - gamma(aa, dd, ee) * gamma(ee, cc, bb)
            for ee in range(dim)
        )
    )


def covariant_derivative(gamma, direction, vector):
    result = sp.zeros(dim, 1)
    for aa in range(dim):
        directional = sum(direction[bb] * sp.diff(vector[aa], coords[bb]) for bb in range(dim))
        connection = sum(
            gamma(aa, bb, cc) * direction[bb] * vector[cc]
            for bb in range(dim)
            for cc in range(dim)
        )
        result[aa] = central(directional + connection)
    return result


def matrix_strings(matrix):
    return [[str(simp(matrix[ii, jj])) for jj in range(matrix.cols)] for ii in range(matrix.rows)]


def derive():
    X = sp.Matrix([p, w])
    shift = M * X
    E = a * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [shift[0], shift[0], 1, 0],
            [shift[1], shift[1], 0, 1],
        ]
    )
    E_inv = a**-1 * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-shift[0], -shift[0], 1, 0],
            [-shift[1], -shift[1], 0, 1],
        ]
    )
    metric = E.T * lorentz * E
    inverse = E_inv * lorentz * E_inv.T
    gamma = make_christoffel(metric, inverse)
    print("G196: metric assembled", file=sys.stderr, flush=True)

    clock = sp.Matrix([a**-1, 0, 0, 0])
    ray = sp.Matrix([a**-2, a**-2, 0, 0])
    screen = (
        sp.Matrix([0, 0, a**-1, 0]),
        sp.Matrix([0, 0, 0, a**-1]),
    )

    screen_derivatives = [covariant_derivative(gamma, ray, vector) for vector in screen]
    screen_connection = sp.zeros(2, 2)
    for ii, left in enumerate(screen):
        for jj, derivative in enumerate(screen_derivatives):
            screen_connection[ii, jj] = central(inner(metric, left, derivative))
    print("G196: screen connection assembled", file=sys.stderr, flush=True)

    tidal = sp.zeros(2, 2)
    for ii, left in enumerate(screen):
        for jj, right in enumerate(screen):
            curvature_vector = sp.zeros(dim, 1)
            for aa in range(dim):
                component = sp.S.Zero
                for bb in (0, 1):
                    for cc in (2, 3):
                        for dd in (0, 1):
                            component += (
                                riemann_component(gamma, aa, bb, cc, dd)
                                * ray[bb]
                                * right[cc]
                                * ray[dd]
                            )
                curvature_vector[aa] = central(component)
            tidal[ii, jj] = central(inner(metric, left, curvature_vector))
    tidal = tidal.applyfunc(simp)
    print("G196: coordinate-screen tide assembled", file=sys.stderr, flush=True)

    pair_h = central(metric)[:2, :2]
    screen_gram = sp.Matrix(
        [[central(inner(metric, left, right)) for right in screen] for left in screen]
    )
    frequency = central(-inner(metric, clock, ray))
    geodesic = covariant_derivative(gamma, ray, ray)

    S = sp.Matrix([[A, N], [N, B]])
    J = sp.Matrix([[0, 1], [-1, 0]])
    Omega = R * J
    hubble = sp.diff(a, eta) / a
    tau0 = simp((hubble**2 - sp.diff(hubble, eta)) / a**4)
    mixing_tide = (
        2 * dplus(S) - 4 * S * S - 4 * (S * Omega - Omega * S)
    ).applyfunc(simp)
    expected_tide = (tau0 * sp.eye(2) + mixing_tide / a**4).applyfunc(simp)
    connection_s = (a**2 * screen_connection).applyfunc(simp)

    y1 = sp.Function("y1", real=True)(eta, z)
    y2 = sp.Function("y2", real=True)(eta, z)
    y = sp.Matrix([y1, y2])
    dy = dplus(y)
    inner_factor = dy + 2 * M * y
    factored = (dplus(inner_factor) - 2 * M.T * inner_factor).applyfunc(simp)
    expanded_operator = (
        dplus(dy)
        + 2 * (M - M.T) * dy
        + (2 * dplus(M) - 4 * M.T * M) * y
    ).applyfunc(simp)
    covariant_first = dy + 2 * Omega * y
    covariant_second = (dplus(covariant_first) + 2 * Omega * covariant_first).applyfunc(simp)
    covariant_operator = (covariant_second + mixing_tide * y).applyfunc(simp)

    def covariant_lambda(vector):
        return ((dplus(vector) + 2 * Omega * vector) / a**2).applyfunc(simp)

    physical_amplitude = a * y
    affine_residual = (
        covariant_lambda(covariant_lambda(physical_amplitude))
        + expected_tide * physical_amplitude
    ).applyfunc(simp)
    affine_expected = (factored / a**3).applyfunc(simp)

    l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22", real=True)
    L = sp.Matrix([[l11, l12], [l21, l22]])
    inverse_gram = (L.inv() * L.inv().T).applyfunc(simp)
    v1, v2 = sp.symbols("v1 v2", real=True)
    vector = sp.Matrix([v1, v2])
    gram_quadratic = simp((vector.T * inverse_gram * vector)[0])
    gram_template = simp(sum((L.inv().T * vector)[ii] ** 2 for ii in range(2)))

    z_derivatives = {
        sp.diff(function, z): 0
        for function in (A, N, B, R)
    }
    g195_limit = tidal.subs(z_derivatives).applyfunc(simp)
    expected_g195_limit = (
        tau0 * sp.eye(2)
        + (
            2 * sp.diff(S, eta)
            - 4 * S * S
            - 4 * (S * Omega - Omega * S)
        )
        / a**4
    ).applyfunc(simp)
    pure_rotation_subs = {}
    for function in (A, N, B):
        pure_rotation_subs[function] = 0
        pure_rotation_subs[sp.diff(function, eta)] = 0
        pure_rotation_subs[sp.diff(function, z)] = 0
    pure_rotation_limit = tidal.subs(pure_rotation_subs).applyfunc(simp)

    assertions = {
        "coframe_determinant": simp(E.det() - a**4) == 0,
        "metric_determinant": simp(metric.det() + a**8) == 0,
        "pair_pullback": pair_h == sp.diag(-a**2, a**2),
        "affine_ray": geodesic == sp.zeros(4, 1),
        "frequency": simp(frequency - a**-1) == 0,
        "screen_orthonormal": screen_gram == sp.eye(2),
        "screen_connection": connection_s == 2 * Omega,
        "screen_connection_skew": connection_s + connection_s.T == sp.zeros(2),
        "coordinate_tide": tidal == expected_tide,
        "coordinate_tide_self_adjoint": tidal == tidal.T,
        "null_directional_derivative": all(
            simp(tidal[ii, jj] - expected_tide[ii, jj]) == 0
            for ii in range(2) for jj in range(2)
        ),
        "general_factorization": factored == expanded_operator,
        "covariant_factorization": factored == covariant_operator,
        "affine_jacobi_reduction": affine_residual == affine_expected,
        "g195_limit": g195_limit == expected_g195_limit,
        "pure_rotation_no_tide": pure_rotation_limit == tau0 * sp.eye(2),
        "gram_positive_template": simp(gram_quadratic - gram_template) == 0,
    }
    assert all(assertions.values()), {key: value for key, value in assertions.items() if not value}

    result = {
        "status": "PASS",
        "landing": "NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE",
        "family": {
            "coordinates": ["eta", "z", "p", "w"],
            "scale": "a(eta)>0, C3, a(0)=1",
            "mixing": "M(eta,z) arbitrary real 2x2 C2",
            "pair": "p=w=0, outgoing +z germ; gamma(s)=(s,s,0,0)",
        },
        "null_derivative": "D_plus=partial_eta+partial_z",
        "det_coframe": str(simp(E.det())),
        "det_metric": str(simp(metric.det())),
        "pair_metric": matrix_strings(pair_h),
        "frequency": str(frequency),
        "screen_connection_lambda": matrix_strings(screen_connection),
        "screen_connection_s": matrix_strings(connection_s),
        "coordinate_tide": matrix_strings(tidal),
        "mixing_tide": matrix_strings(mixing_tide),
        "coordinate_factorization": "(D_plus-2M^T)(D_plus+2M)Y=0",
        "fundamental_representation": (
            "On each outgoing ray, M_bar(s)=M(s+eta0,s+z0); "
            "D=a L K, L'=-2 M_bar L, K=int L^-1 L^-T ds"
        ),
        "caustic_sign": (
            "det(D)>0 off the vertex on every connected regular outgoing-ray interval; "
            "the proof uses the positive Gram integrand and det(L)>0"
        ),
        "assertions": assertions,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G196_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("PRODUCTION_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    derive()
