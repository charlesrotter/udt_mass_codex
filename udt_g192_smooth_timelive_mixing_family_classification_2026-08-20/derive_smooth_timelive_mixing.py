#!/usr/bin/env python3
"""Exact production derivation for the preregistered G192 function family.

The symbolic tensor reconstruction is performed in the constant screen-rotated
coordinates (eta, z, p=(x+y)/sqrt(2), w=(x-y)/sqrt(2)).  The reported Jacobi
map is rotated back to the original fixed (x,y) source screen.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def simp(value):
    return sp.factor(sp.simplify(sp.trigsimp(value)))


eta_coord, z_coord, p_coord, w_coord = sp.symbols("eta z p w", real=True)
coords = (eta_coord, z_coord, p_coord, w_coord)
DIM = 4
lorentz = sp.diag(-1, 1, 1, 1)

scale = sp.Function("a", positive=True)(eta_coord)
mix = sp.Function("mu", real=True)(eta_coord)
mix_plus = sp.sqrt(2) * mix


def central(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: simp(entry.subs(p_coord, 0)))
    return simp(value.subs(p_coord, 0))


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
    """Return R^a_{b c d} with the G188--G191 curvature convention."""
    return simp(
        sp.diff(gamma[aa][dd][bb], coords[cc])
        - sp.diff(gamma[aa][cc][bb], coords[dd])
        + sum(
            gamma[aa][cc][ee] * gamma[ee][dd][bb]
            - gamma[aa][dd][ee] * gamma[ee][cc][bb]
            for ee in range(DIM)
        )
    )


def lambda_derivative(expression):
    """Derivative along the central affine ray: d/dlambda=a^-2 d/deta."""
    return simp(sp.diff(expression, eta_coord) / scale**2)


def derive():
    # Constant O(2) screen rotation turns the two equal original mixing rows
    # into one active plus row and one passive minus row.
    coframe = scale * sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [mix_plus * p_coord, mix_plus * p_coord, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    metric = simp(coframe.T * lorentz * coframe)
    metric_central = central(metric)
    gamma = christoffel(metric)

    U = sp.Matrix([scale**-1, 0, 0, 0])
    N = sp.Matrix([0, scale**-1, 0, 0])
    ell = U + N
    ray = sp.Matrix([scale**-2, scale**-2, 0, 0])
    screen = (
        sp.Matrix([0, 0, scale**-1, 0]),
        sp.Matrix([0, 0, 0, scale**-1]),
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

    tidal_rotated = sp.zeros(2, 2)
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
            tidal_rotated[left_index, right_index] = central(inner(metric, left, rvector))
    tidal_rotated = tidal_rotated.applyfunc(simp)

    conformal_hubble = sp.diff(scale, eta_coord) / scale
    isotropic_tide = simp(
        (conformal_hubble**2 - sp.diff(conformal_hubble, eta_coord)) / scale**4
    )
    mixing_tide = simp(
        (2 * sp.diff(mix_plus, eta_coord) - 4 * mix_plus**2) / scale**4
    )
    expected_rotated = sp.diag(isotropic_tide + mixing_tide, isotropic_tide).applyfunc(simp)

    plus_projector = sp.Matrix([[1, 1], [1, 1]]) / 2
    minus_projector = sp.Matrix([[1, -1], [-1, 1]]) / 2
    tidal_original = (
        (isotropic_tide + mixing_tide) * plus_projector
        + isotropic_tide * minus_projector
    ).applyfunc(simp)
    tracefree_original = (
        tidal_original - sp.trace(tidal_original) * sp.eye(2) / 2
    ).applyfunc(simp)

    # The plus mode has an exact factorization.  I'=A and J'=exp(4I),
    # with I(0)=J(0)=0, give y_plus=exp(-2I)J.
    I_fun = sp.Function("I", real=True)(eta_coord)
    J_fun = sp.Function("J", real=True)(eta_coord)
    y_plus = sp.exp(-2 * I_fun) * J_fun
    substitution = {
        sp.diff(I_fun, eta_coord): mix_plus,
        sp.diff(I_fun, eta_coord, 2): sp.diff(mix_plus, eta_coord),
        sp.diff(J_fun, eta_coord): sp.exp(4 * I_fun),
        sp.diff(J_fun, eta_coord, 2): 4 * mix_plus * sp.exp(4 * I_fun),
    }
    y_plus_residual = simp(
        (
            sp.diff(y_plus, eta_coord, 2)
            + (2 * sp.diff(mix_plus, eta_coord) - 4 * mix_plus**2) * y_plus
        ).subs(substitution)
    )

    f_plus = scale * y_plus
    f_minus = scale * eta_coord
    plus_residual = simp(
        (
            lambda_derivative(lambda_derivative(f_plus))
            + (isotropic_tide + mixing_tide) * f_plus
        ).subs(substitution)
    )
    minus_residual = simp(
        lambda_derivative(lambda_derivative(f_minus)) + isotropic_tide * f_minus
    )

    jacobi_original = (f_plus * plus_projector + f_minus * minus_projector).applyfunc(simp)
    determinant = simp(jacobi_original.det())

    # Exact constant-control regressions.
    H_const, mu_const = sp.symbols("H mu", positive=True, real=True)
    constant_substitutions = {
        scale: sp.exp(H_const * eta_coord),
        sp.diff(scale, eta_coord): H_const * sp.exp(H_const * eta_coord),
        sp.diff(scale, eta_coord, 2): H_const**2 * sp.exp(H_const * eta_coord),
        mix: mu_const,
        sp.diff(mix, eta_coord): 0,
    }
    g191_rotated_tide = expected_rotated.subs(constant_substitutions).applyfunc(simp)
    expected_g191_rotated_tide = sp.diag(
        (H_const**2 - 8 * mu_const**2) * sp.exp(-4 * H_const * eta_coord),
        H_const**2 * sp.exp(-4 * H_const * eta_coord),
    )
    constant_y_plus = sp.sinh(2 * sp.sqrt(2) * mu_const * eta_coord) / (
        2 * sp.sqrt(2) * mu_const
    )

    assert simp(coframe.det() - scale**4) == 0
    assert simp(metric.det() + scale**8) == 0
    assert pair_h == sp.diag(-scale**2, scale**2)
    assert all(value == 0 for value in pair_frame.values())
    assert all(value == 0 for value in geodesic)
    assert all(value == 0 for row in parallel_screen for value in row)
    assert simp(omega - scale**-1) == 0
    assert simp(domega - frequency_rhs) == 0
    assert tidal_rotated == expected_rotated, (
        "tidal mismatch",
        tidal_rotated,
        expected_rotated,
        (tidal_rotated - expected_rotated).applyfunc(simp),
    )
    assert tidal_rotated == tidal_rotated.T
    assert tidal_original == tidal_original.T
    assert y_plus_residual == 0
    assert plus_residual == 0
    assert minus_residual == 0
    assert simp(determinant - f_plus * f_minus) == 0
    assert g191_rotated_tide == expected_g191_rotated_tide
    assert simp(constant_y_plus.limit(mu_const, 0) - eta_coord) == 0

    return {
        "family": {
            "coordinates": ["eta", "z", "p=(x+y)/sqrt(2)", "w=(x-y)/sqrt(2)"],
            "scale": "a(eta)>0, C3, a(0)=1",
            "mixing": "mu(eta) real, C2",
            "mixing_plus": "A(eta)=sqrt(2)*mu(eta)",
        },
        "coframe": str(coframe),
        "coframe_determinant": str(simp(coframe.det())),
        "metric_determinant": str(simp(metric.det())),
        "pair_pullback": str(pair_h),
        "pair_frame_residuals": {key: str(value) for key, value in pair_frame.items()},
        "affine_ray": [str(value) for value in ray],
        "affine_relation": "lambda(eta)=Integral(a(s)^2,(s,0,eta)); strictly increasing because a>0",
        "geodesic_residual": [str(value) for value in geodesic],
        "parallel_screen_residual": [[str(value) for value in row] for row in parallel_screen],
        "frequency": str(omega),
        "frequency_derivative": str(domega),
        "frequency_rhs": str(frequency_rhs),
        "frequency_residual": str(simp(domega - frequency_rhs)),
        "frequency_turn_condition": "a'(eta)=0; a' sign changes distinguish true turns from stalls",
        "tidal_rotated": [
            [str(tidal_rotated[ii, jj]) for jj in range(2)] for ii in range(2)
        ],
        "tidal_original": [
            [str(tidal_original[ii, jj]) for jj in range(2)] for ii in range(2)
        ],
        "tracefree_tidal_original": [
            [str(tracefree_original[ii, jj]) for jj in range(2)] for ii in range(2)
        ],
        "isotropic_tide": str(isotropic_tide),
        "mixing_tide": str(mixing_tide),
        "jacobi_modes": {
            "I": "I(eta)=Integral(A(s),(s,0,eta))",
            "J": "J(eta)=Integral(exp(4*I(s)),(s,0,eta))",
            "y_plus": str(y_plus),
            "f_plus": str(f_plus),
            "f_minus": str(f_minus),
            "y_plus_residual": str(y_plus_residual),
            "f_plus_residual": str(plus_residual),
            "f_minus_residual": str(minus_residual),
        },
        "jacobi_original": [
            [str(jacobi_original[ii, jj]) for jj in range(2)] for ii in range(2)
        ],
        "jacobi_determinant": str(determinant),
        "caustic_classification": {
            "eta_positive": "f_plus>0 and f_minus>0 for every eta>0 in the regular interval",
            "eta_negative": "f_plus<0 and f_minus<0 for every eta<0 in the regular interval",
            "nonvertex_zeros": 0,
            "scope": "displayed two-function coframe family only",
        },
        "descent_classification": {
            "native_output": "eta -> (lambda,Z,D,d_A)",
            "Z": "1/a(eta)",
            "dA_squared": "a(eta)^2*eta*exp(-2*I(eta))*J(eta)",
            "dA_of_Z": "local only where a'(eta)!=0; branch-labelled across frequency turns",
        },
        "regressions": {
            "G191_rotated_tide": [
                [str(g191_rotated_tide[ii, jj]) for jj in range(2)] for ii in range(2)
            ],
            "G191_constant_plus_mode": str(constant_y_plus),
            "G190_mu_zero": "y_plus=eta and D=a(eta)*eta*I2",
            "G188_static_constant_mu": "f_plus=sinh(2*sqrt(2)*mu*eta)/(2*sqrt(2)*mu), f_minus=eta",
        },
    }


def main():
    result = derive()
    if os.environ.get("G192_NO_WRITE") != "1":
        output = Path(__file__).with_name("PRODUCTION_RESULT.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
