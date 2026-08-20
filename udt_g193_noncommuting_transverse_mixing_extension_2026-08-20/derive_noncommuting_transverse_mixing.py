#!/usr/bin/env python3
"""Exact production derivation for the preregistered G193 family.

The calculation reconstructs the metric, Levi-Civita connection, curvature,
affine frequency, and full parallel-screen tide directly from the coframe.
No G192 tidal or Jacobi formula is imported.
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
mix_mu = sp.Function("mu", real=True)(eta_coord)
mix_nu = sp.Function("nu", real=True)(eta_coord)
mix_a = sp.sqrt(2) * mix_mu
mixing_matrix = sp.Matrix([[mix_a, mix_nu], [mix_nu, 0]])


def central(value):
    substitutions = {p_coord: 0, w_coord: 0}
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs(substitutions)))
    return simp(value.subs(substitutions))


def inner(metric, left, right):
    return simp((left.T * metric * right)[0])


def make_christoffel(metric, inverse):
    """Return a memoized exact component evaluator.

    Expressions remain unsimplified until after the central substitution.
    This preserves the full metric calculation while avoiding 64 expensive
    generic-coordinate simplifications that are irrelevant to the query.
    """

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
    """Return R^a_{b c d} in the G188--G192 convention."""
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
    """Derivative along the central affine ray: d/dlambda=a^-2 d/deta."""
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
    print("G193: metric and exact inverse assembled", file=sys.stderr, flush=True)

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
    print("G193: affine frame and frequency assembled", file=sys.stderr, flush=True)

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
    print("G193: central curvature tide reconstructed", file=sys.stderr, flush=True)

    conformal_hubble = sp.diff(scale, eta_coord) / scale
    isotropic_tide = simp(
        (conformal_hubble**2 - sp.diff(conformal_hubble, eta_coord)) / scale**4
    )
    expected_mixing_tide = (
        2 * sp.diff(mixing_matrix, eta_coord) - 4 * mixing_matrix * mixing_matrix
    ).applyfunc(lambda entry: simp(entry / scale**4))
    expected_tidal = (isotropic_tide * sp.eye(2) + expected_mixing_tide).applyfunc(simp)

    # Verify the matrix differential-operator order without assuming commutativity.
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

    # Check that the conformal rescaling f=a*y maps the eta-factorized
    # equation to the affine Jacobi equation with the full reconstructed tide.
    physical_amplitude = scale * y_vector
    affine_jacobi_residual = (
        lambda_derivative(lambda_derivative(physical_amplitude))
        + expected_tidal * physical_amplitude
    ).applyfunc(simp)
    expected_affine_residual = (expected_operator / scale**3).applyfunc(simp)
    affine_reduction_residual = (
        affine_jacobi_residual - expected_affine_residual
    ).applyfunc(simp)

    # The exact fundamental representation uses L'=-2 M L and
    # K'=L^-1 L^-T.  K' is positive definite because it is B B^T with
    # B=L^-1.  det(L) is positive from Liouville's formula.
    det_l_exponent_integrand = simp(-2 * sp.trace(mixing_matrix))
    commutator_probe_a, commutator_probe_b = sp.symbols("A_a A_b", real=True)
    nu_probe_a, nu_probe_b = sp.symbols("nu_a nu_b", real=True)
    matrix_a = sp.Matrix([[commutator_probe_a, nu_probe_a], [nu_probe_a, 0]])
    matrix_b = sp.Matrix([[commutator_probe_b, nu_probe_b], [nu_probe_b, 0]])
    commutator = (matrix_a * matrix_b - matrix_b * matrix_a).applyfunc(simp)

    # Regression limits are checked directly on the reconstructed tide.
    g192_limit = tidal.subs({mix_nu: 0, sp.diff(mix_nu, eta_coord): 0}).applyfunc(simp)
    expected_g192_limit = sp.diag(
        simp(
            isotropic_tide
            + (2 * sp.diff(mix_a, eta_coord) - 4 * mix_a**2) / scale**4
        ),
        isotropic_tide,
    )
    conformal_limit = tidal.subs(
        {
            mix_mu: 0,
            sp.diff(mix_mu, eta_coord): 0,
            mix_nu: 0,
            sp.diff(mix_nu, eta_coord): 0,
        }
    ).applyfunc(simp)

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
        "tidal_self_adjoint": tidal == tidal.T,
        "matrix_factorization": factorization_residual == sp.zeros(2, 1),
        "affine_jacobi_reduction": affine_reduction_residual == sp.zeros(2, 1),
        "g192_limit": g192_limit == expected_g192_limit,
        "g190_limit": conformal_limit == isotropic_tide * sp.eye(2),
        "commutator_antisymmetric": commutator + commutator.T == sp.zeros(2),
    }
    assert all(assertions.values()), {key: value for key, value in assertions.items() if not value}

    return {
        "status": "PASS",
        "family": {
            "coordinates": ["eta", "z", "p", "w"],
            "scale": "a(eta)>0, C3, a(0)=1",
            "mixing": "M=[[sqrt(2)mu,nu],[nu,0]], mu and nu real C2",
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
            "factorization": "(d/deta-2M)(d/deta+2M)y=0",
            "fundamental_representation": (
                "D=a L K; L'=-2ML, L(0)=I; "
                "K=int_0^eta L^-1 L^-T ds"
            ),
            "det_L_integrand": str(det_l_exponent_integrand),
            "commutator": matrix_strings(commutator),
            "caustic_sign": (
                "det(D)>0 for eta!=0 because det(aL)>0 and K is "
                "positive definite for eta>0, negative definite for eta<0"
            ),
        },
        "assertions": assertions,
        "scope": {
            "derived": (
                "displayed arbitrary positive a and real mu,nu family; supplied central pair"
            ),
            "open": (
                "third symmetric channel, antisymmetric rotation, arbitrary complete coframes, "
                "other germs, physical history, transfer, global completion, Xmax"
            ),
        },
    }


def main():
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G193_NO_WRITE") == "1":
        print(payload, end="")
        return
    destination = Path(__file__).with_name("PRODUCTION_RESULT.json")
    destination.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
