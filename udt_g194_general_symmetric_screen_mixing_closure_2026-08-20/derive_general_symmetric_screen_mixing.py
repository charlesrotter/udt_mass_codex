#!/usr/bin/env python3
"""Exact production derivation for the preregistered G194 family.

The calculation reconstructs the metric, Levi-Civita connection, curvature,
affine frequency, and full parallel-screen tide directly from the coframe with
an arbitrary smooth symmetric 2 x 2 mixing matrix.  No G193 tide is imported.
"""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp


def simp(value):
    return sp.factor(sp.simplify(sp.trigsimp(value)))


eta_coord, z_coord, p_coord, w_coord = sp.symbols("eta z p w", real=True)
coords = (eta_coord, z_coord, p_coord, w_coord)
dim = 4
lorentz = sp.diag(-1, 1, 1, 1)

scale = sp.Function("a", positive=True)(eta_coord)
mix_a = sp.Function("A", real=True)(eta_coord)
mix_n = sp.Function("N", real=True)(eta_coord)
mix_b = sp.Function("B", real=True)(eta_coord)
mixing_matrix = sp.Matrix([[mix_a, mix_n], [mix_n, mix_b]])


def central(value):
    substitutions = {p_coord: 0, w_coord: 0}
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs(substitutions)))
    return simp(value.subs(substitutions))


def inner(metric, left, right):
    return simp((left.T * metric * right)[0])


def make_christoffel(metric, inverse):
    """Return a memoized exact component evaluator."""

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
    """Return R^a_{b c d} in the G188--G193 convention."""
    return simp(
        sp.diff(gamma(aa, dd, bb), coords[cc])
        - sp.diff(gamma(aa, cc, bb), coords[dd])
        + sum(
            gamma(aa, cc, ee) * gamma(ee, dd, bb)
            - gamma(aa, dd, ee) * gamma(ee, cc, bb)
            for ee in range(dim)
        )
    )


def lambda_derivative(expression):
    return simp(sp.diff(expression, eta_coord) / scale**2)


def matrix_strings(matrix):
    return [[str(simp(matrix[ii, jj])) for jj in range(matrix.cols)] for ii in range(matrix.rows)]


def derive():
    screen_position = sp.Matrix([p_coord, w_coord])
    screen_shift = mixing_matrix * screen_position
    coframe = scale * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [screen_shift[0], screen_shift[0], 1, 0],
            [screen_shift[1], screen_shift[1], 0, 1],
        ]
    )
    inverse_coframe = scale**-1 * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-screen_shift[0], -screen_shift[0], 1, 0],
            [-screen_shift[1], -screen_shift[1], 0, 1],
        ]
    )
    metric = coframe.T * lorentz * coframe
    inverse_metric = inverse_coframe * lorentz * inverse_coframe.T
    metric_central = central(metric)
    gamma = make_christoffel(metric, inverse_metric)
    print("G194: metric and exact inverse assembled", file=sys.stderr, flush=True)

    clock = sp.Matrix([scale**-1, 0, 0, 0])
    ruler = sp.Matrix([0, scale**-1, 0, 0])
    null_germ = clock + ruler
    ray = sp.Matrix([scale**-2, scale**-2, 0, 0])
    screen = (
        sp.Matrix([0, 0, scale**-1, 0]),
        sp.Matrix([0, 0, 0, scale**-1]),
    )

    pair_h = metric_central[:2, :2]
    frame_residuals = {
        "clock_norm_plus_1": central(inner(metric, clock, clock) + 1),
        "ruler_norm_minus_1": central(inner(metric, ruler, ruler) - 1),
        "clock_ruler": central(inner(metric, clock, ruler)),
        "null_germ": central(inner(metric, null_germ, null_germ)),
        "source_frequency_minus_1": central(-inner(metric, clock, null_germ) - 1),
    }

    geodesic_residual = []
    for aa in range(dim):
        directional = sum(ray[bb] * sp.diff(ray[aa], coords[bb]) for bb in range(dim))
        connection = sum(
            gamma(aa, bb, cc) * ray[bb] * ray[cc]
            for bb in range(dim)
            for cc in range(dim)
        )
        geodesic_residual.append(central(directional + connection))

    screen_gram = sp.zeros(2, 2)
    parallel_screen_residual = []
    for ii, left in enumerate(screen):
        for jj, right in enumerate(screen):
            screen_gram[ii, jj] = central(inner(metric, left, right))
        vector_residual = []
        for aa in range(dim):
            directional = sum(ray[bb] * sp.diff(left[aa], coords[bb]) for bb in range(dim))
            connection = sum(
                gamma(aa, bb, cc) * ray[bb] * left[cc]
                for bb in range(dim)
                for cc in range(dim)
            )
            vector_residual.append(central(directional + connection))
        parallel_screen_residual.append(vector_residual)

    frequency = central(-inner(metric, clock, ray))
    frequency_derivative = central(
        sum(ray[aa] * sp.diff(frequency, coords[aa]) for aa in range(dim))
    )
    clock_covector = metric * clock
    frequency_contraction = sp.S.Zero
    for aa in range(dim):
        for bb in range(dim):
            nabla_clock = sp.diff(clock_covector[bb], coords[aa]) - sum(
                gamma(cc, aa, bb) * clock_covector[cc] for cc in range(dim)
            )
            frequency_contraction -= ray[aa] * ray[bb] * nabla_clock
    frequency_contraction = central(frequency_contraction)
    print("G194: affine frame and frequency assembled", file=sys.stderr, flush=True)

    tidal = sp.zeros(2, 2)
    for left_index, left in enumerate(screen):
        for right_index, right in enumerate(screen):
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
            tidal[left_index, right_index] = central(inner(metric, left, curvature_vector))
    tidal = tidal.applyfunc(simp)
    print("G194: central curvature tide reconstructed", file=sys.stderr, flush=True)

    conformal_hubble = sp.diff(scale, eta_coord) / scale
    isotropic_tide = simp(
        (conformal_hubble**2 - sp.diff(conformal_hubble, eta_coord)) / scale**4
    )
    expected_mixing_tide = (
        2 * sp.diff(mixing_matrix, eta_coord) - 4 * mixing_matrix * mixing_matrix
    ).applyfunc(lambda entry: simp(entry / scale**4))
    expected_tidal = (isotropic_tide * sp.eye(2) + expected_mixing_tide).applyfunc(simp)

    y1 = sp.Function("y1", real=True)(eta_coord)
    y2 = sp.Function("y2", real=True)(eta_coord)
    y_vector = sp.Matrix([y1, y2])
    first_factor = sp.diff(y_vector, eta_coord) + 2 * mixing_matrix * y_vector
    factored_operator = (
        sp.diff(first_factor, eta_coord) - 2 * mixing_matrix * first_factor
    ).applyfunc(simp)
    expected_operator = (
        sp.diff(y_vector, eta_coord, 2)
        + (2 * sp.diff(mixing_matrix, eta_coord) - 4 * mixing_matrix * mixing_matrix)
        * y_vector
    ).applyfunc(simp)
    factorization_residual = (factored_operator - expected_operator).applyfunc(simp)

    physical_amplitude = scale * y_vector
    affine_jacobi_residual = (
        lambda_derivative(lambda_derivative(physical_amplitude))
        + expected_tidal * physical_amplitude
    ).applyfunc(simp)
    expected_affine_residual = (expected_operator / scale**3).applyfunc(simp)
    affine_reduction_residual = (
        affine_jacobi_residual - expected_affine_residual
    ).applyfunc(simp)

    det_l_exponent_integrand = simp(-2 * sp.trace(mixing_matrix))
    v1, v2 = sp.symbols("v1 v2", real=True)
    g11, g12, g22 = sp.symbols("g11 g12 g22", real=True)
    gram = sp.Matrix([[g11, g12], [g12, g22]])
    gram_quadratic = simp((sp.Matrix([v1, v2]).T * gram * sp.Matrix([v1, v2]))[0])

    a1, n1, b1, a2, n2, b2 = sp.symbols("A1 N1 B1 A2 N2 B2", real=True)
    matrix_1 = sp.Matrix([[a1, n1], [n1, b1]])
    matrix_2 = sp.Matrix([[a2, n2], [n2, b2]])
    commutator = (matrix_1 * matrix_2 - matrix_2 * matrix_1).applyfunc(simp)

    g193_limit = tidal.subs({mix_b: 0, sp.diff(mix_b, eta_coord): 0}).applyfunc(simp)
    expected_g193_limit = (
        isotropic_tide * sp.eye(2)
        + (
            2 * sp.diff(sp.Matrix([[mix_a, mix_n], [mix_n, 0]]), eta_coord)
            - 4 * sp.Matrix([[mix_a, mix_n], [mix_n, 0]]) ** 2
        )
        / scale**4
    ).applyfunc(simp)
    g192_limit = tidal.subs(
        {
            mix_b: 0,
            sp.diff(mix_b, eta_coord): 0,
            mix_n: 0,
            sp.diff(mix_n, eta_coord): 0,
        }
    ).applyfunc(simp)
    expected_g192_limit = sp.diag(
        simp(isotropic_tide + (2 * sp.diff(mix_a, eta_coord) - 4 * mix_a**2) / scale**4),
        isotropic_tide,
    )
    conformal_limit = tidal.subs(
        {
            mix_a: 0,
            sp.diff(mix_a, eta_coord): 0,
            mix_n: 0,
            sp.diff(mix_n, eta_coord): 0,
            mix_b: 0,
            sp.diff(mix_b, eta_coord): 0,
        }
    ).applyfunc(simp)

    explicit_component_tide = sp.Matrix(
        [
            [
                2 * sp.diff(mix_a, eta_coord) - 4 * mix_a**2 - 4 * mix_n**2,
                2 * sp.diff(mix_n, eta_coord) - 4 * mix_n * (mix_a + mix_b),
            ],
            [
                2 * sp.diff(mix_n, eta_coord) - 4 * mix_n * (mix_a + mix_b),
                2 * sp.diff(mix_b, eta_coord) - 4 * mix_b**2 - 4 * mix_n**2,
            ],
        ]
    ).applyfunc(lambda entry: simp(entry / scale**4))

    assertions = {
        "coframe_determinant": simp(coframe.det() - scale**4) == 0,
        "metric_determinant": simp(metric.det() + scale**8) == 0,
        "pair_pullback": pair_h == sp.diag(-scale**2, scale**2),
        "completed_frame": all(value == 0 for value in frame_residuals.values()),
        "affine_ray": all(value == 0 for value in geodesic_residual),
        "screen_orthonormal": screen_gram == sp.eye(2),
        "screen_parallel": all(
            value == 0 for row in parallel_screen_residual for value in row
        ),
        "frequency": simp(frequency - scale**-1) == 0,
        "frequency_contraction": simp(frequency_derivative - frequency_contraction) == 0,
        "tidal_matrix": tidal == expected_tidal,
        "tidal_components": expected_mixing_tide == explicit_component_tide,
        "tidal_self_adjoint": tidal == tidal.T,
        "matrix_factorization": factorization_residual == sp.zeros(2, 1),
        "affine_jacobi_reduction": affine_reduction_residual == sp.zeros(2, 1),
        "g193_limit": g193_limit == expected_g193_limit,
        "g192_limit": g192_limit == expected_g192_limit,
        "g190_limit": conformal_limit == isotropic_tide * sp.eye(2),
        "commutator_antisymmetric": commutator + commutator.T == sp.zeros(2),
        "gram_quadratic_form": gram_quadratic == g11 * v1**2 + 2 * g12 * v1 * v2 + g22 * v2**2,
    }
    assert all(assertions.values()), {key: value for key, value in assertions.items() if not value}

    return {
        "status": "PASS",
        "landing": "GENERAL_SYMMETRIC_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE",
        "family": {
            "coordinates": ["eta", "z", "p", "w"],
            "scale": "a(eta)>0, C3, a(0)=1",
            "mixing": "M=[[A,N],[N,B]], A,N,B arbitrary real C2",
            "pair": "p=w=0, outgoing +z germ",
        },
        "exact": {
            "det_coframe": str(simp(coframe.det())),
            "det_metric": str(simp(metric.det())),
            "pair_metric": matrix_strings(pair_h),
            "affine_relation": "dlambda/deta=a(eta)^2",
            "frequency": str(frequency),
            "frequency_derivative": str(frequency_derivative),
            "tidal_matrix": matrix_strings(tidal),
            "mixing_tide": matrix_strings(expected_mixing_tide),
            "factorization": "(d/deta-2M)(d/deta+2M)Y=0",
            "fundamental_representation": (
                "D=a L K; L'=-2ML, L(0)=I; K=int_0^eta L^-1 L^-T ds"
            ),
            "det_L_integrand": str(det_l_exponent_integrand),
            "commutator": matrix_strings(commutator),
            "gram_quadratic_template": str(gram_quadratic),
            "caustic_sign": (
                "det(D)>0 for eta!=0 because det(aL)>0 and K is positive definite "
                "for eta>0, negative definite for eta<0"
            ),
        },
        "assertions": assertions,
        "scope": {
            "derived": (
                "displayed arbitrary positive a and arbitrary real symmetric 2x2 M; "
                "supplied central pair"
            ),
            "open": (
                "antisymmetric rotation, arbitrary complete coframes, other germs, physical "
                "history, transfer, global completion, Xmax"
            ),
        },
    }


def main():
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G194_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("PRODUCTION_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
