#!/usr/bin/env python3
"""Direct coordinate-curvature derivation for the preregistered G127 theorem."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    t, r, theta, psi = sp.symbols("t r theta psi", real=True)
    phi = sp.Function("phi")(r)
    coords = (t, r, theta, psi)
    g = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), r**2, r**2 * sp.sin(theta) ** 2)
    ginv = sp.simplify(g.inv())
    dim = 4

    Gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for rho in range(dim):
        for mu in range(dim):
            for nu in range(dim):
                Gamma[rho][mu][nu] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        ginv[rho, sigma]
                        * (
                            sp.diff(g[sigma, nu], coords[mu])
                            + sp.diff(g[sigma, mu], coords[nu])
                            - sp.diff(g[mu, nu], coords[sigma])
                        )
                        for sigma in range(dim)
                    )
                )

    @lru_cache(maxsize=None)
    def rup(rho: int, sigma: int, mu: int, nu: int):
        # R^rho_{ sigma mu nu} = (R(d_mu,d_nu)d_sigma)^rho.
        return sp.simplify(
            sp.diff(Gamma[rho][nu][sigma], coords[mu])
            - sp.diff(Gamma[rho][mu][sigma], coords[nu])
            + sum(
                Gamma[rho][mu][ell] * Gamma[ell][nu][sigma]
                - Gamma[rho][nu][ell] * Gamma[ell][mu][sigma]
                for ell in range(dim)
            )
        )

    def R4(X, Y, Z, W):
        # R(X,Y,Z,W) = g(R(X,Y)Z,W).
        value = sp.S.Zero
        for mu in range(dim):
            if X[mu] == 0:
                continue
            for nu in range(dim):
                if Y[nu] == 0:
                    continue
                for sigma in range(dim):
                    if Z[sigma] == 0:
                        continue
                    for rho in range(dim):
                        component = rup(rho, sigma, mu, nu)
                        if component == 0:
                            continue
                        for delta in range(dim):
                            if W[delta] != 0 and g[delta, rho] != 0:
                                value += (
                                    X[mu]
                                    * Y[nu]
                                    * Z[sigma]
                                    * W[delta]
                                    * g[delta, rho]
                                    * component
                                )
        return sp.simplify(value.subs(theta, sp.pi / 2))

    et = sp.Matrix([sp.exp(phi), 0, 0, 0])
    er = sp.Matrix([0, sp.exp(-phi), 0, 0])
    eth = sp.Matrix([0, 0, 1 / r, 0])
    eps = sp.Matrix([0, 0, 0, 1 / (r * sp.sin(theta))])

    # Spherical orthonormal curvature scalars in the preregistered convention.
    T = sp.simplify(R4(er, et, et, er))
    U = sp.simplify(R4(eth, et, et, eth))
    V = sp.simplify(R4(eth, er, er, eth))
    W = sp.simplify(R4(eps, eth, eth, eps))
    Xi = sp.simplify(T - U + V - W)

    k_rad = et + er
    radial = sp.Matrix(
        [
            [R4(eth, k_rad, k_rad, eth), R4(eth, k_rad, k_rad, eps)],
            [R4(eps, k_rad, k_rad, eth), R4(eps, k_rad, k_rad, eps)],
        ]
    ).applyfunc(sp.simplify)

    # Keep the tilt genuinely generic.  The rational 3-4-5 direction below is
    # used only as a finite exact witness after the symbolic identity passes.
    alpha = sp.symbols("alpha", real=True)
    c = sp.cos(alpha)
    s = sp.sin(alpha)
    v = c * er + s * eth
    k_tilt = et + v
    s1 = -s * er + c * eth
    s2 = eps
    tilted = sp.Matrix(
        [
            [R4(s1, k_tilt, k_tilt, s1), R4(s1, k_tilt, k_tilt, s2)],
            [R4(s2, k_tilt, k_tilt, s1), R4(s2, k_tilt, k_tilt, s2)],
        ]
    ).applyfunc(lambda value: sp.trigsimp(sp.simplify(value)))
    tilted_expected = sp.Matrix(
        [
            [s**2 * T + c**2 * U + V, 0],
            [0, U + c**2 * V + s**2 * W],
        ]
    ).applyfunc(lambda value: sp.trigsimp(sp.simplify(value)))

    phi_prime = sp.diff(phi, r)
    phi_second = sp.diff(phi, r, 2)
    expected_scalars = {
        "T": sp.exp(-2 * phi) * (2 * phi_prime**2 - phi_second),
        "U": -sp.exp(-2 * phi) * phi_prime / r,
        "V": sp.exp(-2 * phi) * phi_prime / r,
        "W": (1 - sp.exp(-2 * phi)) / r**2,
    }
    expected_xi = sp.simplify(
        expected_scalars["T"]
        - expected_scalars["U"]
        + expected_scalars["V"]
        - expected_scalars["W"]
    )

    q = sp.symbols("q", positive=True)
    witness_phi = sp.log(1 + q * r**2) / 2
    xi_witness = sp.factor(Xi.subs(phi, witness_phi).doit())
    xi_witness_expected = q**2 * r**2 * (3 - q * r**2) / (1 + q * r**2) ** 3
    xi_at_one = sp.simplify(xi_witness.subs({q: 1, r: 1}))

    jacobi_cubic_radial = radial.applyfunc(lambda value: sp.simplify(-value / 6))
    jacobi_cubic_tilted = tilted.applyfunc(lambda value: sp.simplify(-value / 6))
    tilted_tf = sp.simplify(
        tilted - sp.trace(tilted) * sp.eye(2) / 2
    )

    # The optical deformation is B=D'D^{-1}, not D itself.  From the Jacobi
    # jet D=lambda I-lambda^3 R/6+O(lambda^4), the inverse jet is
    # lambda^-1(I+lambda^2 R/6), so B=I/lambda-lambda R/3+O(lambda^2).
    lam = sp.symbols("lambda", positive=True)
    Dprime_jet = sp.eye(2) - lam**2 * tilted / 2
    Dinverse_jet = sp.eye(2) / lam + lam * tilted / 6
    optical_product = sp.expand(Dprime_jet * Dinverse_jet)
    optical_leading = sp.eye(2) / lam - lam * tilted / 3
    optical_tf_leading = -lam * tilted_tf / 3
    optical_product_linear = optical_product.applyfunc(
        lambda value: sp.expand(value).coeff(lam, 1)
    )
    optical_product_linear_tf = sp.simplify(
        optical_product_linear
        - sp.trace(optical_product_linear) * sp.eye(2) / 2
    )

    def inner(X, Y):
        return sp.simplify((X.T * g * Y)[0].subs(theta, sp.pi / 2))

    P = sp.Matrix(
        [
            [sp.Rational(5, 13), sp.Rational(-12, 13)],
            [sp.Rational(12, 13), sp.Rational(5, 13)],
        ]
    )
    tilted_rebased = sp.simplify(P.T * tilted * P)
    tilted_tf_rebased = sp.simplify(
        tilted_rebased - sp.trace(tilted_rebased) * sp.eye(2) / 2
    )

    def expr_zero(value):
        return sp.trigsimp(sp.simplify(value)) == 0

    def matrix_zero(value):
        return all(expr_zero(entry) for entry in value)

    cw = sp.Rational(3, 5)
    sw = sp.Rational(4, 5)
    tilted_witness = sp.Matrix(
        [
            [sw**2 * T + cw**2 * U + V, 0],
            [0, U + cw**2 * V + sw**2 * W],
        ]
    )

    scalar_checks = {
        name: sp.simplify(value - expected_scalars[name]) == 0
        for name, value in {"T": T, "U": U, "V": V, "W": W}.items()
    }
    checks = {
        **{f"direct_scalar_{name}": passed for name, passed in scalar_checks.items()},
        "reciprocal_radial_focusing_cancels": sp.simplify(U + V) == 0,
        "radial_screen_isotropic": radial == sp.zeros(2),
        "generic_alpha_direct_equals_spherical_formula": matrix_zero(
            tilted - tilted_expected
        ),
        "generic_alpha_offdiagonal_zero": expr_zero(tilted[0, 1])
        and expr_zero(tilted[1, 0]),
        "radial_query_is_null_and_screen_orthonormal": (
            inner(k_rad, k_rad) == 0
            and inner(eth, eth) == 1
            and inner(eps, eps) == 1
            and inner(k_rad, eth) == 0
            and inner(k_rad, eps) == 0
        ),
        "tilted_query_is_null_and_screen_orthonormal": (
            inner(k_tilt, k_tilt) == 0
            and inner(s1, s1) == 1
            and inner(s2, s2) == 1
            and inner(k_tilt, s1) == 0
            and inner(k_tilt, s2) == 0
            and inner(s1, s2) == 0
        ),
        "generic_alpha_tidal_eigenvalue_contrast_is_sin2_Xi": expr_zero(
            tilted[0, 0] - tilted[1, 1] - s**2 * Xi
        ),
        "xi_matches_direct_scalars": sp.simplify(Xi - expected_xi) == 0,
        "flat_phi_zero_has_no_adapted_curvature_contrast": sp.simplify(
            Xi.subs(phi, 0).doit()
        )
        == 0,
        "regular_nonlinear_witness_formula": sp.simplify(
            xi_witness - xi_witness_expected
        )
        == 0,
        "regular_nonlinear_witness_nonzero": xi_at_one == sp.Rational(1, 4),
        "regular_nonlinear_witness_center_limit": sp.limit(
            xi_witness_expected, r, 0, dir="+"
        )
        == 0,
        "tilted_tracefree_curvature_nonzero_on_witness": tilted_witness.subs(
            phi, witness_phi
        ).doit().subs({q: 1, r: 1}) - sp.trace(
            tilted_witness.subs(phi, witness_phi).doit().subs({q: 1, r: 1})
        ) * sp.eye(2) / 2 != sp.zeros(2),
        "jacobi_radial_cubic_isotropic": jacobi_cubic_radial == sp.zeros(2),
        "jacobi_tilted_cubic_eigenvalue_contrast": expr_zero(
            jacobi_cubic_tilted[0, 0] - jacobi_cubic_tilted[1, 1]
            + s**2 * Xi / 6
        ),
        "generic_tilt_reversal_even": matrix_zero(
            tilted.subs(alpha, -alpha) - tilted
        ),
        "optical_matrix_leading_coefficient": matrix_zero(
            optical_product_linear + tilted / 3
        ),
        "optical_shear_tracefree_leading": matrix_zero(
            optical_product_linear_tf + tilted_tf / 3
        ),
        "optical_shear_eigenvalue_contrast": expr_zero(
            optical_product_linear_tf[0, 0]
            - optical_product_linear_tf[1, 1]
            + s**2 * Xi / 3
        ),
        "screen_basis_trace_covariant": sp.simplify(
            sp.trace(tilted_rebased) - sp.trace(tilted)
        )
        == 0,
        "screen_basis_determinant_covariant": sp.simplify(
            tilted_rebased.det() - tilted.det()
        )
        == 0,
        "screen_basis_tidal_tracefree_norm_covariant": sp.simplify(
            sp.trace(tilted_tf_rebased * tilted_tf_rebased)
            - sp.trace(tilted_tf * tilted_tf)
        )
        == 0,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact": {
            "T": str(T),
            "U": str(U),
            "V": str(V),
            "W": str(W),
            "Xi": str(sp.factor(Xi)),
            "radial_Rperp": str(radial),
            "tilted_difference": str(sp.factor(tilted[0, 0] - tilted[1, 1])),
            "witness_phi": "log(1+q*r**2)/2",
            "witness_Xi": str(xi_witness),
            "witness_Xi_q1_r1": str(xi_at_one),
            "jacobi_jet": "D(lambda)=lambda I-lambda^3 Rperp(0)/6+O(lambda^4)",
            "optical_jet": "B(lambda)=D'D^{-1}=I/lambda-lambda Rperp(0)/3+O(lambda^2)",
        },
        "landing": (
            "SAME_HISTORY_RADIAL_AND_TILTED_SCREEN_EMERGENCE_DERIVED_LOCALLY__"
            "SYMMETRY_RADIAL_SCREEN_AT_THE_SHARED_FINITE_RADIUS_VERTEX_IS_ISOTROPIC__"
            "TILTED_QUERY_TIDAL_CONTRAST_IS_SIN2_ALPHA_TIMES_SPHERICALLY_ADAPTED_"
            "CURVATURE_CONTRAST_XI__OPTICAL_SHEAR_FOLLOWS_FROM_JACOBI_PROPAGATION__"
            "NO_APPENDED_ANGULAR_RESPONSE_OR_SECOND_HISTORY__"
            "PHYSICAL_HISTORY_GLOBAL_QUERY_AND_OBSERVATIONS_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
