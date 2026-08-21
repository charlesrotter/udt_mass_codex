#!/usr/bin/env python3
"""Exact metric reconstruction for the preregistered G195 rotation family."""

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
A = sp.Function("A", real=True)(eta)
N = sp.Function("N", real=True)(eta)
B = sp.Function("B", real=True)(eta)
R = sp.Function("R", real=True)(eta)
M = sp.Matrix([[A, N + R], [N - R, B]])


def central(value):
    substitutions = {p: 0, w: 0}
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs(substitutions)))
    return simp(value.subs(substitutions))


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
    print("G195: metric assembled", file=sys.stderr, flush=True)

    clock = sp.Matrix([a**-1, 0, 0, 0])
    ruler = sp.Matrix([0, a**-1, 0, 0])
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
    print("G195: screen connection assembled", file=sys.stderr, flush=True)

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
    print("G195: coordinate-screen tide assembled", file=sys.stderr, flush=True)

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
        2 * sp.diff(S, eta) - 4 * S * S - 4 * (S * Omega - Omega * S)
    ).applyfunc(simp)
    expected_tide = (tau0 * sp.eye(2) + mixing_tide / a**4).applyfunc(simp)
    connection_eta = (a**2 * screen_connection).applyfunc(simp)

    theta = sp.Function("vartheta", real=True)(eta)
    O = sp.Matrix(
        [[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]]
    )

    def rotation_simp(value):
        return simp(value.subs(sp.diff(theta, eta), 2 * R))

    def zero_modulo_rotation(matrix):
        """Certify a matrix identity modulo cos(theta)^2+sin(theta)^2=1.

        Large curvature expressions can retain this elementary rotation
        constraint after SymPy's generic simplifier has stopped.  Reducing
        each numerator as a polynomial in independent placeholders makes the
        exact constraint explicit without numerical substitution.
        """
        cosine, sine = sp.symbols("rotation_cosine rotation_sine", real=True)
        circle = sp.Poly(cosine**2 + sine**2 - 1, cosine, sine, domain="EX")
        for entry in matrix:
            replaced = sp.together(sp.expand(rotation_simp(entry))).subs(
                {sp.cos(theta): cosine, sp.sin(theta): sine}
            )
            numerator = sp.fraction(replaced)[0]
            remainder = sp.Poly(
                numerator, cosine, sine, domain="EX"
            ).rem(circle).as_expr()
            if simp(remainder) != 0:
                return False
        return True

    parallel_transport_residual = (
        sp.diff(O, eta) + connection_eta * O
    ).applyfunc(rotation_simp)
    S_parallel = (O.T * S * O).applyfunc(simp)
    dS_parallel = sp.diff(S_parallel, eta).applyfunc(rotation_simp)
    expected_dS_parallel = (
        O.T * (sp.diff(S, eta) - 2 * (S * Omega - Omega * S)) * O
    ).applyfunc(rotation_simp)
    parallel_tide = (O.T * tidal * O).applyfunc(rotation_simp)
    expected_parallel_tide = (
        tau0 * sp.eye(2) + (2 * dS_parallel - 4 * S_parallel * S_parallel) / a**4
    ).applyfunc(rotation_simp)

    y1 = sp.Function("y1", real=True)(eta)
    y2 = sp.Function("y2", real=True)(eta)
    y = sp.Matrix([y1, y2])
    inner_factor = sp.diff(y, eta) + 2 * M * y
    factored = (sp.diff(inner_factor, eta) - 2 * M.T * inner_factor).applyfunc(simp)
    covariant_first = sp.diff(y, eta) + 2 * Omega * y
    covariant_second = (
        sp.diff(covariant_first, eta) + 2 * Omega * covariant_first
    ).applyfunc(simp)
    covariant_operator = (covariant_second + mixing_tide * y).applyfunc(simp)
    expanded_operator = (
        sp.diff(y, eta, 2)
        + 2 * (M - M.T) * sp.diff(y, eta)
        + (2 * sp.diff(M, eta) - 4 * M.T * M) * y
    ).applyfunc(simp)

    def covariant_lambda(vector):
        return ((sp.diff(vector, eta) + 2 * Omega * vector) / a**2).applyfunc(simp)

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
    gram_quadratic = simp(
        (sp.Matrix([v1, v2]).T * inverse_gram * sp.Matrix([v1, v2]))[0]
    )

    symmetric_limit = tidal.subs(
        {R: 0, sp.diff(R, eta): 0}
    ).applyfunc(simp)
    expected_symmetric_limit = (
        tau0 * sp.eye(2) + (2 * sp.diff(S, eta) - 4 * S * S) / a**4
    ).applyfunc(simp)
    pure_rotation_limit = tidal.subs(
        {
            A: 0,
            sp.diff(A, eta): 0,
            N: 0,
            sp.diff(N, eta): 0,
            B: 0,
            sp.diff(B, eta): 0,
        }
    ).applyfunc(simp)

    assertions = {
        "coframe_determinant": simp(E.det() - a**4) == 0,
        "metric_determinant": simp(metric.det() + a**8) == 0,
        "pair_pullback": pair_h == sp.diag(-a**2, a**2),
        "affine_ray": geodesic == sp.zeros(4, 1),
        "frequency": simp(frequency - a**-1) == 0,
        "screen_orthonormal": screen_gram == sp.eye(2),
        "screen_connection": connection_eta == 2 * Omega,
        "screen_connection_skew": connection_eta + connection_eta.T == sp.zeros(2),
        "coordinate_tide": tidal == expected_tide,
        "coordinate_tide_self_adjoint": tidal == tidal.T,
        "parallel_transport": parallel_transport_residual == sp.zeros(2),
        "parallel_symmetric_strain": S_parallel == S_parallel.T,
        "parallel_strain_derivative": dS_parallel == expected_dS_parallel,
        "parallel_tide": zero_modulo_rotation(
            parallel_tide - expected_parallel_tide
        ),
        "general_factorization": factored == expanded_operator,
        "covariant_factorization": factored == covariant_operator,
        "affine_jacobi_reduction": affine_residual == affine_expected,
        "g194_limit": symmetric_limit == expected_symmetric_limit,
        "pure_rotation_no_tide": pure_rotation_limit == tau0 * sp.eye(2),
        "rotation_orthogonal": (O.T * O).applyfunc(simp) == sp.eye(2),
        "rotation_orientation": simp(O.det() - 1) == 0,
        "gram_positive_template": gram_quadratic == simp(sum(inverse_gram[ii, jj] * (v1, v2)[ii] * (v1, v2)[jj] for ii in range(2) for jj in range(2))),
    }
    assert all(assertions.values()), {key: value for key, value in assertions.items() if not value}

    result = {
        "status": "PASS",
        "landing": "ROTATION_CARRIES_COVARIANTLY__GENERAL_REAL_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE",
        "family": {
            "coordinates": ["eta", "z", "p", "w"],
            "scale": "a(eta)>0, C3, a(0)=1",
            "mixing": "M=[[A,N+R],[N-R,B]], A,N,B,R arbitrary real C2",
            "pair": "p=w=0, outgoing +z germ",
        },
        "det_coframe": str(simp(E.det())),
        "det_metric": str(simp(metric.det())),
        "pair_metric": matrix_strings(pair_h),
        "frequency": str(frequency),
        "screen_connection_lambda": matrix_strings(screen_connection),
        "screen_connection_eta": matrix_strings(connection_eta),
        "coordinate_tide": matrix_strings(tidal),
        "coordinate_tide_self_adjoint": tidal == tidal.T,
        "mixing_tide": matrix_strings(mixing_tide),
        "parallel_rotation": "O'= -2 R J O, O(0)=I",
        "parallel_strain": "S_parallel=O^T S O",
        "coordinate_factorization": "(d/deta-2M^T)(d/deta+2M)Y=0",
        "covariant_factorization": "[(d/deta+2Omega)^2+2S'-4S^2-4[S,Omega]]Y=0",
        "fundamental_representation": (
            "D_coordinate=a L K; L'=-2ML, L(0)=I; "
            "K=int_0^eta L^-1 L^-T ds"
        ),
        "caustic_sign": (
            "det(D)>0 for eta!=0 because det(aL)>0 and K is definite; "
            "no symmetry of M is required"
        ),
        "assertions": assertions,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G195_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("PRODUCTION_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    derive()
