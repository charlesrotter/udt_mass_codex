#!/usr/bin/env python3
"""Exact production derivation for the preregistered G191 witness."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def simp(value):
    return sp.simplify(sp.trigsimp(value))


eta_coord, z_coord, x_coord, y_coord = sp.symbols("eta z x y", real=True)
H, mu, lam = sp.symbols("H mu lambda", positive=True, real=True)
coords = (eta_coord, z_coord, x_coord, y_coord)
DIM = 4
lorentz = sp.diag(-1, 1, 1, 1)


def central(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs({x_coord: 0, y_coord: 0})))
    return simp(value.subs({x_coord: 0, y_coord: 0}))


def inner(metric, left, right):
    return simp((left.T * metric * right)[0])


def christoffel(metric):
    inverse = simp(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for aa in range(DIM):
        for bb in range(DIM):
            for cc in range(DIM):
                gamma[aa][bb][cc] = simp(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[aa, dd]
                        * (
                            sp.diff(metric[dd, cc], coords[bb])
                            + sp.diff(metric[dd, bb], coords[cc])
                            - sp.diff(metric[bb, cc], coords[dd])
                        )
                        for dd in range(DIM)
                    )
                )
    return gamma


def riemann_component(gamma, aa, bb, cc, dd):
    """R^a_{b c d}; slots are Z=b, X=c, Y=d."""
    return simp(
        sp.diff(gamma[aa][dd][bb], coords[cc])
        - sp.diff(gamma[aa][cc][bb], coords[dd])
        + sum(
            gamma[aa][cc][ee] * gamma[ee][dd][bb]
            - gamma[aa][dd][ee] * gamma[ee][cc][bb]
            for ee in range(DIM)
        )
    )


def derive():
    a = sp.exp(H * eta_coord)
    mix = mu * (x_coord + y_coord) / sp.sqrt(2)
    coframe = a * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [mix, mix, 1, 0],
            [mix, mix, 0, 1],
        ]
    )
    metric = simp(coframe.T * lorentz * coframe)
    metric_central = central(metric)
    gamma = christoffel(metric)

    U = sp.Matrix([a**-1, 0, 0, 0])
    N = sp.Matrix([0, a**-1, 0, 0])
    ell = U + N
    ray = sp.Matrix([a**-2, a**-2, 0, 0])
    screen = (
        sp.Matrix([0, 0, a**-1, 0]),
        sp.Matrix([0, 0, 0, a**-1]),
    )

    pair_h = metric_central[:2, :2]
    pair_frame = {
        "UU_plus_1": central(inner(metric, U, U) + 1),
        "NN_minus_1": central(inner(metric, N, N) - 1),
        "UN": central(inner(metric, U, N)),
        "ell_null": central(inner(metric, ell, ell)),
        "ell_frequency_minus_1": central(-inner(metric, U, ell) - 1),
    }

    geodesic = []
    for aa in range(DIM):
        directional = sum(ray[bb] * sp.diff(ray[aa], coords[bb]) for bb in range(DIM))
        connection = sum(
            gamma[aa][bb][cc] * ray[bb] * ray[cc]
            for bb in range(DIM)
            for cc in range(DIM)
        )
        geodesic.append(central(directional + connection))

    parallel_screen = []
    for vector in screen:
        residual = []
        for aa in range(DIM):
            directional = sum(ray[bb] * sp.diff(vector[aa], coords[bb]) for bb in range(DIM))
            connection = sum(
                gamma[aa][bb][cc] * ray[bb] * vector[cc]
                for bb in range(DIM)
                for cc in range(DIM)
            )
            residual.append(central(directional + connection))
        parallel_screen.append(residual)

    omega = central(-inner(metric, U, ray))
    domega = central(sum(ray[aa] * sp.diff(omega, coords[aa]) for aa in range(DIM)))
    U_cov = metric * U
    frequency_rhs = sp.S.Zero
    for aa in range(DIM):
        for bb in range(DIM):
            nabla_u = sp.diff(U_cov[bb], coords[aa]) - sum(
                gamma[cc][aa][bb] * U_cov[cc] for cc in range(DIM)
            )
            frequency_rhs -= ray[aa] * ray[bb] * nabla_u
    frequency_rhs = central(frequency_rhs)

    tidal = sp.zeros(2, 2)
    for left_index, left in enumerate(screen):
        for right_index, right in enumerate(screen):
            rvector = sp.zeros(DIM, 1)
            for aa in range(DIM):
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
                rvector[aa] = central(component)
            tidal[left_index, right_index] = central(inner(metric, left, rvector))
    tidal = tidal.applyfunc(simp)
    scaled_tidal = tidal.applyfunc(lambda entry: simp(entry * a**4))

    # Exact affine elimination.  Along the central branch
    # q=1+2H lambda=a^2 and Z=q^(-1/2).
    q_lam = 1 + 2 * H * lam
    constant_tide = sp.Matrix(
        [
            [H**2 - 4 * mu**2, -4 * mu**2],
            [-4 * mu**2, H**2 - 4 * mu**2],
        ]
    )
    tidal_lam = constant_tide / q_lam**2
    symmetric_projector = sp.Matrix([[1, 1], [1, 1]]) / 2
    antisymmetric_projector = sp.Matrix([[1, -1], [-1, 1]]) / 2
    f_symmetric = (
        sp.sqrt(q_lam)
        * sp.sinh(sp.sqrt(2) * mu * sp.log(q_lam) / H)
        / (2 * sp.sqrt(2) * mu)
    )
    f_antisymmetric = sp.sqrt(q_lam) * sp.log(q_lam) / (2 * H)
    jacobi = (f_symmetric * symmetric_projector + f_antisymmetric * antisymmetric_projector).applyfunc(simp)
    jacobi_residual = (sp.diff(jacobi, lam, 2) + tidal_lam * jacobi).applyfunc(simp)
    vertex_jacobi = jacobi.subs(lam, 0).applyfunc(simp)
    vertex_derivative = sp.diff(jacobi, lam).subs(lam, 0).applyfunc(simp)
    determinant = simp(jacobi.det())
    expected_determinant = simp(f_symmetric * f_antisymmetric)
    tracefree_tide = (
        tidal_lam - sp.trace(tidal_lam) * sp.eye(2) / 2
    ).applyfunc(simp)

    Zsym = sp.symbols("Z", positive=True, real=True)
    Z_lam = q_lam ** sp.Rational(-1, 2)
    dZ_dlam = simp(sp.diff(Z_lam, lam))
    f_antisymmetric_Z = -sp.log(Zsym) / (H * Zsym)
    f_symmetric_Z = (
        sp.sinh(-2 * sp.sqrt(2) * mu * sp.log(Zsym) / H)
        / (2 * sp.sqrt(2) * mu * Zsym)
    )
    dA_squared_Z = simp(f_symmetric_Z * f_antisymmetric_Z)

    mu_zero_jacobi = jacobi.applyfunc(lambda entry: simp(sp.limit(entry, mu, 0)))
    expected_mu_zero = sp.eye(2) * f_antisymmetric
    H_zero_jacobi = jacobi.applyfunc(lambda entry: simp(sp.limit(entry, H, 0, dir="+")))
    H_zero_symmetric = sp.sinh(2 * sp.sqrt(2) * mu * lam) / (2 * sp.sqrt(2) * mu)
    expected_H_zero = (
        H_zero_symmetric * symmetric_projector + lam * antisymmetric_projector
    ).applyfunc(simp)

    assert simp(coframe.det() - a**4) == 0
    assert simp(metric.det() + a**8) == 0
    assert pair_h == sp.diag(-a**2, a**2)
    assert all(value == 0 for value in pair_frame.values())
    assert all(value == 0 for value in geodesic)
    assert all(value == 0 for row in parallel_screen for value in row)
    assert simp(domega - frequency_rhs) == 0
    assert tidal == tidal.T
    assert scaled_tidal == constant_tide
    assert jacobi_residual == sp.zeros(2)
    assert vertex_jacobi == sp.zeros(2)
    assert vertex_derivative == sp.eye(2)
    assert simp(determinant - expected_determinant) == 0
    assert mu_zero_jacobi == expected_mu_zero
    assert H_zero_jacobi == expected_H_zero
    assert tracefree_tide[0, 1] == -4 * mu**2 / q_lam**2

    return {
        "coframe": str(coframe),
        "coframe_determinant": str(simp(coframe.det())),
        "metric": str(metric),
        "metric_determinant": str(simp(metric.det())),
        "central_metric": str(metric_central),
        "pair_pullback": str(pair_h),
        "pair_frame_residuals": {key: str(value) for key, value in pair_frame.items()},
        "affine_ray": [str(value) for value in ray],
        "geodesic_residual": [str(value) for value in geodesic],
        "parallel_screen_residual": [[str(value) for value in row] for row in parallel_screen],
        "omega": str(omega),
        "domega_dlambda": str(domega),
        "frequency_rhs": str(frequency_rhs),
        "frequency_residual": str(simp(domega - frequency_rhs)),
        "tidal": [[str(tidal[ii, jj]) for jj in range(2)] for ii in range(2)],
        "scaled_tidal": [[str(scaled_tidal[ii, jj]) for jj in range(2)] for ii in range(2)],
        "affine_elimination": {
            "q": str(q_lam),
            "eta_of_lambda": "log(2*H*lambda + 1)/(2*H)",
            "Z_of_lambda": str(Z_lam),
            "dZ_dlambda": str(dZ_dlam),
        },
        "tidal_of_lambda": [[str(tidal_lam[ii, jj]) for jj in range(2)] for ii in range(2)],
        "tracefree_tidal": [[str(tracefree_tide[ii, jj]) for jj in range(2)] for ii in range(2)],
        "jacobi": [[str(jacobi[ii, jj]) for jj in range(2)] for ii in range(2)],
        "jacobi_eigenmodes": {
            "symmetric": str(f_symmetric),
            "antisymmetric": str(f_antisymmetric),
        },
        "jacobi_residual": [[str(jacobi_residual[ii, jj]) for jj in range(2)] for ii in range(2)],
        "vertex_jacobi": [[str(vertex_jacobi[ii, jj]) for jj in range(2)] for ii in range(2)],
        "vertex_derivative": [[str(vertex_derivative[ii, jj]) for jj in range(2)] for ii in range(2)],
        "determinant": str(determinant),
        "dA_squared_of_Z": str(dA_squared_Z),
        "mu_zero_jacobi": [[str(mu_zero_jacobi[ii, jj]) for jj in range(2)] for ii in range(2)],
        "H_zero_jacobi": [[str(H_zero_jacobi[ii, jj]) for jj in range(2)] for ii in range(2)],
        "branch_classification": {
            "domain": "H>0, mu>0, lambda>=0",
            "frequency": "strictly_decreasing_for_lambda>=0",
            "frequency_turns": 0,
            "post_vertex_caustics": 0,
            "cross_response": "strictly_positive_for_lambda>0",
            "dA_of_Z": "single_valued_on_0<Z<=1_for_this_control",
        },
    }


def main():
    result = derive()
    if os.environ.get("G191_NO_WRITE") != "1":
        output = Path(__file__).with_name("PRODUCTION_RESULT.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
