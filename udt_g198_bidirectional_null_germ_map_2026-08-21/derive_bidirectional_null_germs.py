#!/usr/bin/env python3
"""Exact same-metric reconstruction of both central null germs for G198."""

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


def directional(value, sign):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(
            lambda entry: simp(sp.diff(entry, eta) + sign * sp.diff(entry, z))
        )
    return simp(sp.diff(value, eta) + sign * sp.diff(value, z))


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


@lru_cache(maxsize=None)
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
        derivative = sum(
            direction[bb] * sp.diff(vector[aa], coords[bb]) for bb in range(dim)
        )
        connection = sum(
            gamma(aa, bb, cc) * direction[bb] * vector[cc]
            for bb in range(dim)
            for cc in range(dim)
        )
        result[aa] = central(derivative + connection)
    return result


def matrix_strings(matrix):
    return [[str(simp(matrix[ii, jj])) for jj in range(matrix.cols)] for ii in range(matrix.rows)]


def vector_strings(vector):
    return [str(simp(vector[ii])) for ii in range(vector.rows)]


def derive_germ(sign, metric, gamma, clock, screen):
    label = "plus" if sign == 1 else "minus"
    ray = sp.Matrix([a**-2, sign * a**-2, 0, 0])
    derivatives = [covariant_derivative(gamma, ray, vector) for vector in screen]
    connection_lambda = sp.zeros(2, 2)
    for ii, left in enumerate(screen):
        for jj, derivative in enumerate(derivatives):
            connection_lambda[ii, jj] = central(inner(metric, left, derivative))

    tide = sp.zeros(2, 2)
    curvature_columns = []
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
        curvature_columns.append(curvature_vector)
        for ii, left in enumerate(screen):
            tide[ii, jj] = central(inner(metric, left, curvature_vector))
    tide = tide.applyfunc(simp)

    y1 = sp.Function(f"y1_{label}", real=True)(eta, z)
    y2 = sp.Function(f"y2_{label}", real=True)(eta, z)
    jacobi_vector = sp.Matrix([0, 0, y1, y2])
    first_jacobi = covariant_derivative(gamma, ray, jacobi_vector)
    second_jacobi = covariant_derivative(gamma, ray, first_jacobi)
    curvature_jacobi = sp.zeros(dim, 1)
    for jj, component_y in enumerate((y1, y2)):
        curvature_jacobi += curvature_columns[jj] * (a * component_y)
    # curvature_columns use orthonormal screen vectors a^-1 partial_X.  The
    # coordinate vector component y^A partial_A therefore contributes a*y^A.
    direct_jacobi = (second_jacobi + curvature_jacobi).applyfunc(simp)

    geodesic = covariant_derivative(gamma, ray, ray)
    frequency = central(-inner(metric, clock, ray))
    screen_gram = sp.Matrix(
        [[central(inner(metric, left, right)) for right in screen] for left in screen]
    )
    connection_s = (a**2 * connection_lambda).applyfunc(simp)
    coordinate_operator = (a**4 * direct_jacobi[2:4, 0]).applyfunc(simp)

    return {
        "label": label,
        "sign": sign,
        "ray": ray,
        "frequency": frequency,
        "geodesic": geodesic,
        "screen_gram": screen_gram,
        "connection_lambda": connection_lambda,
        "connection_s": connection_s,
        "tide": tide,
        "direct_jacobi": direct_jacobi,
        "coordinate_operator": coordinate_operator,
        "first_jacobi": first_jacobi,
    }


def derive():
    X = sp.Matrix([p, w])
    shift = M * X
    coframe = a * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [shift[0], shift[0], 1, 0],
            [shift[1], shift[1], 0, 1],
        ]
    )
    coframe_inverse = a**-1 * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-shift[0], -shift[0], 1, 0],
            [-shift[1], -shift[1], 0, 1],
        ]
    )
    metric = coframe.T * lorentz * coframe
    inverse = coframe_inverse * lorentz * coframe_inverse.T
    gamma = make_christoffel(metric, inverse)
    print("G198: full metric and Christoffels assembled", file=sys.stderr, flush=True)

    clock = sp.Matrix([a**-1, 0, 0, 0])
    screen = (
        sp.Matrix([0, 0, a**-1, 0]),
        sp.Matrix([0, 0, 0, a**-1]),
    )
    plus = derive_germ(1, metric, gamma, clock, screen)
    print("G198: outgoing direct contractions assembled", file=sys.stderr, flush=True)
    minus = derive_germ(-1, metric, gamma, clock, screen)
    print("G198: incoming direct contractions assembled", file=sys.stderr, flush=True)

    pair_metric = central(metric)[:2, :2]
    hubble = sp.diff(a, eta) / a
    tau0 = simp((hubble**2 - sp.diff(hubble, eta)) / a**4)
    S = sp.Matrix([[A, N], [N, B]])
    Omega = sp.Matrix([[0, R], [-R, 0]])
    expected_plus_tide = (
        tau0 * sp.eye(2)
        + (2 * directional(S, 1) - 4 * S * S - 4 * (S * Omega - Omega * S)) / a**4
    ).applyfunc(simp)

    y_minus = sp.Matrix(
        [
            sp.Function("y1_minus", real=True)(eta, z),
            sp.Function("y2_minus", real=True)(eta, z),
        ]
    )
    expected_minus_operator = directional(directional(y_minus, -1), -1)

    alias = (eta - z) ** 2 * (eta + z) ** 2
    alias_plus = simp(alias.subs(z, eta))
    alias_minus = simp(alias.subs(z, -eta))
    alias_dplus = simp(directional(alias, 1).subs(z, eta))
    alias_dminus = simp(directional(alias, -1).subs(z, -eta))
    alias_off_ray = simp(alias.subs({eta: sp.Rational(3, 10), z: sp.Rational(1, 10)}))

    assertions = {
        "coframe_determinant": simp(coframe.det() - a**4) == 0,
        "metric_determinant": simp(metric.det() + a**8) == 0,
        "pair_pullback": pair_metric == sp.diag(-a**2, a**2),
        "plus_null": central(inner(metric, plus["ray"], plus["ray"])) == 0,
        "minus_null": central(inner(metric, minus["ray"], minus["ray"])) == 0,
        "plus_affine": plus["geodesic"] == sp.zeros(4, 1),
        "minus_affine": minus["geodesic"] == sp.zeros(4, 1),
        "plus_frequency": simp(plus["frequency"] - a**-1) == 0,
        "minus_frequency": simp(minus["frequency"] - a**-1) == 0,
        "plus_screen_orthonormal": plus["screen_gram"] == sp.eye(2),
        "minus_screen_orthonormal": minus["screen_gram"] == sp.eye(2),
        "plus_connection_regression": plus["connection_s"] == 2 * Omega,
        "minus_connection_quiet": minus["connection_s"] == sp.zeros(2),
        "plus_tide_regression": plus["tide"] == expected_plus_tide,
        "minus_tide_control": minus["tide"] == tau0 * sp.eye(2),
        "plus_tide_self_adjoint": plus["tide"] == plus["tide"].T,
        "minus_tide_self_adjoint": minus["tide"] == minus["tide"].T,
        "plus_jacobi_screen_closed": plus["direct_jacobi"][:2, 0] == sp.zeros(2, 1),
        "minus_jacobi_screen_closed": minus["direct_jacobi"][:2, 0] == sp.zeros(2, 1),
        "minus_coordinate_jacobi": minus["coordinate_operator"] == expected_minus_operator,
        "two_ray_alias_values": alias_plus == 0 and alias_minus == 0,
        "two_ray_alias_first_jets": alias_dplus == 0 and alias_dminus == 0,
        "two_ray_alias_offray": alias_off_ray != 0,
    }
    if not all(assertions.values()):
        failed = {key: value for key, value in assertions.items() if not value}
        diagnostic = {
            "failed": failed,
            "minus_connection_s": matrix_strings(minus["connection_s"]),
            "minus_tide": matrix_strings(minus["tide"]),
            "minus_coordinate_operator": vector_strings(minus["coordinate_operator"]),
            "expected_minus_operator": vector_strings(expected_minus_operator),
        }
        raise AssertionError(diagnostic)

    result = {
        "status": "PASS",
        "landing": "OPPOSITE_GERM_NULL_CONTROL__ASYMMETRY_IS_METRIC_ENCODED",
        "scope": (
            "same full nonlinear G196 metric; central pair; supplied future plus-z and minus-z "
            "null germs; no mirror substitution or independent d_eta-d_z coframe channel"
        ),
        "coframe_one_form": "screen mixing is M(eta,z) X (deta+dz)",
        "det_coframe": str(simp(coframe.det())),
        "det_metric": str(simp(metric.det())),
        "pair_metric": matrix_strings(pair_metric),
        "tau0": str(tau0),
        "outgoing": {
            "directional_derivative": "D_plus=partial_eta+partial_z",
            "frequency": str(plus["frequency"]),
            "screen_connection_s": matrix_strings(plus["connection_s"]),
            "coordinate_tide": matrix_strings(plus["tide"]),
            "coordinate_operator": vector_strings(plus["coordinate_operator"]),
            "regression": "exact G196 formula recovered",
        },
        "incoming": {
            "directional_derivative": "D_minus=partial_eta-partial_z",
            "frequency": str(minus["frequency"]),
            "screen_connection_s": matrix_strings(minus["connection_s"]),
            "coordinate_tide": matrix_strings(minus["tide"]),
            "coordinate_operator": vector_strings(minus["coordinate_operator"]),
            "coordinate_jacobi": "D_minus^2 Y=0",
            "fundamental_solution": "Y(u)=Y0+u V0 in null coordinate u with d/du=D_minus",
            "coordinate_vertex_map": "Y_minus(u)=u I for Y(0)=0 and dY/du(0)=I",
            "physical_vertex_map": "D_minus(u)=a(u) u I in the orthonormal-screen amplitude",
            "caustic_sign": "det D_minus=a(u)^2 u^2>0 at every nonvertex point because a>0",
        },
        "two_ray_alias": {
            "difference": "(eta-z)^2(eta+z)^2 times any fixed real 2x2 coefficient",
            "value_on_plus_ray": str(alias_plus),
            "value_on_minus_ray": str(alias_minus),
            "first_directional_jet_on_plus_ray": str(alias_dplus),
            "first_directional_jet_on_minus_ray": str(alias_dminus),
            "offray_value_at_3_10_1_10": str(alias_off_ray),
        },
        "assertions": assertions,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G198_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("PRODUCTION_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    derive()
