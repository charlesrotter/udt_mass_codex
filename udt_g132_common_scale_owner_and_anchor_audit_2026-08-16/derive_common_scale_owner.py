#!/usr/bin/env python3
"""Exact symbolic derivation for the G132 common-scale ownership audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("DERIVATION_RESULT.json"))
    args = parser.parse_args()

    phi, phi_tilde = sp.symbols("phi phi_tilde", real=True)
    common, omega, c_e, radius = sp.symbols("A Omega c_E R", positive=True)
    K = sp.Matrix([[0, 1], [1, 0]])
    D = sp.diag(sp.exp(-phi), sp.exp(phi))
    P = common * D

    fixed_pairing = sp.simplify(P.T * K * P)
    base = sp.diag(-sp.exp(-2 * phi) * c_e**2, sp.exp(2 * phi))
    base_tilde = sp.diag(-sp.exp(-2 * phi_tilde) * c_e**2, sp.exp(2 * phi_tilde))
    scaled_base = omega**2 * base

    kappa, beta = sp.symbols("kappa beta", real=True)
    t2 = sp.exp(2 * (kappa - phi))
    l2 = sp.exp(2 * (kappa + phi))
    h = sp.Matrix([[-t2, -t2 * beta], [-t2 * beta, l2 - t2 * beta**2]])
    h_scaled = sp.simplify(omega**2 * h)

    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    h_generic = sp.Matrix([[h00, h01], [h01, h11]])
    beta_read = h01 / h00
    t2_read = -h00
    l2_read = h11 - h01**2 / h00
    reconstructed = sp.Matrix(
        [
            [-t2_read, -t2_read * beta_read],
            [-t2_read * beta_read, l2_read - t2_read * beta_read**2],
        ]
    )

    # Dimensional monomials c^a G^b X^d. Dimension order is (L,M,T).
    a, b, d = sp.symbols("a b d")
    ce_dim = sp.Matrix([1, 0, -1])
    g_dim = sp.Matrix([3, -1, -2])
    mass_dim = sp.Matrix([0, 1, 0])
    rho_dim = sp.Matrix([-3, 1, 0])
    energy_density_dim = sp.Matrix([-1, 1, -2])
    length_dim = sp.Matrix([1, 0, 0])

    ce_g_solution = sp.linsolve(
        [a * ce_dim[i] + b * g_dim[i] - length_dim[i] for i in range(3)], (a, b)
    )
    mass_solution = sp.linsolve(
        [a * ce_dim[i] + b * g_dim[i] + d * mass_dim[i] - length_dim[i] for i in range(3)],
        (a, b, d),
    )
    rho_solution = sp.linsolve(
        [a * ce_dim[i] + b * g_dim[i] + d * rho_dim[i] - length_dim[i] for i in range(3)],
        (a, b, d),
    )
    energy_solution = sp.linsolve(
        [a * ce_dim[i] + b * g_dim[i] + d * energy_density_dim[i] - length_dim[i] for i in range(3)],
        (a, b, d),
    )

    x, anchor_strength = sp.symbols("x anchor_strength", real=True)
    anchor_exponent = anchor_strength * x**2 * (x - 1) ** 2

    checks = {
        "fixed_pairing_scales_as_A_squared": sp.simplify(fixed_pairing - common**2 * K) == sp.zeros(2),
        "determinant_one_reciprocal_character": sp.simplify(D.det() - 1) == 0,
        "fixed_K_positive_common_factor_forced_to_one": sp.solve(
            sp.Eq(common**2, 1), common, domain=sp.S.Reals
        ) == [1],
        "founded_base_determinant_is_minus_cE_squared": sp.simplify(base.det() + c_e**2) == 0,
        "common_rescaling_changes_base_determinant_by_Omega_four": sp.simplify(
            scaled_base.det() - omega**4 * base.det()
        ) == 0,
        "same_founded_base_form_forces_Omega_four_one": sp.simplify(
            scaled_base.det() / base_tilde.det() - omega**4
        ) == 0,
        "positive_same_declared_base_determinant_solution_is_Omega_one": sp.solve(
            sp.Eq(omega**4, 1), omega, domain=sp.S.Reals
        ) == [1],
        "pair_determinant_is_minus_exp_four_kappa": sp.simplify(h.det() + sp.exp(4 * kappa)) == 0,
        "pair_terminal_ratio_is_exp_four_phi": sp.simplify((-h.det()) / h[0, 0] ** 2 - sp.exp(4 * phi)) == 0,
        "conformal_pair_determinant_weight_four": sp.simplify(h_scaled.det() - omega**4 * h.det()) == 0,
        "conformal_pair_terminal_ratio_weight_zero": sp.simplify(
            (-h_scaled.det()) / h_scaled[0, 0] ** 2 - (-h.det()) / h[0, 0] ** 2
        ) == 0,
        "conformal_pair_beta_weight_zero": sp.simplify(h_scaled[0, 1] / h_scaled[0, 0] - beta) == 0,
        "terminal_triplet_reconstructs_pair_metric": sp.simplify(reconstructed - h_generic) == sp.zeros(2),
        "spherical_orbit_area_weight_two": sp.simplify(4 * sp.pi * (omega * radius) ** 2 - omega**2 * 4 * sp.pi * radius**2) == 0,
        "four_volume_weight_four": sp.simplify(sp.sqrt(omega**8) - omega**4) == 0,
        "cE_and_G_alone_do_not_form_length": ce_g_solution == sp.EmptySet,
        "cE_G_mass_length_is_GM_over_cE_squared": mass_solution == sp.FiniteSet((-2, 1, 1)),
        "cE_G_density_length_is_cE_over_sqrt_G_rho": rho_solution == sp.FiniteSet((1, sp.Rational(-1, 2), sp.Rational(-1, 2))),
        "cE_G_energy_density_length_is_cE_squared_over_sqrt_G_epsilon": energy_solution
        == sp.FiniteSet((2, sp.Rational(-1, 2), sp.Rational(-1, 2))),
        "two_anchor_family_agrees_at_zero": sp.simplify(anchor_exponent.subs(x, 0)) == 0,
        "two_anchor_family_agrees_at_one": sp.simplify(anchor_exponent.subs(x, 1)) == 0,
        "two_anchor_family_remains_nonconstant": sp.simplify(anchor_exponent.subs(x, sp.Rational(1, 2)))
        == anchor_strength / 16,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passed": sum(bool(v) for v in checks.values()),
        "total": len(checks),
        "checks": checks,
        "exact": {
            "fixed_pairing": str(fixed_pairing),
            "base_determinant": str(base.det()),
            "pair_determinant": str(sp.factor(h.det())),
            "pair_terminal_ratio": str(sp.simplify((-h.det()) / h[0, 0] ** 2)),
            "cE_G_solution": str(ce_g_solution),
            "mass_solution": str(mass_solution),
            "density_solution": str(rho_solution),
            "energy_density_solution": str(energy_solution),
            "two_anchor_exponent_midpoint": str(anchor_exponent.subs(x, sp.Rational(1, 2))),
        },
        "landing": (
            "FIXED_K_RECIPROCAL_TRANSFORMATION_HAS_NO_INTERNAL_COMMON_FACTOR__"
            "COMPLETE_PAIR_EVALUATOR_RETAINS_SUPPLIED_COMMON_SCALE__"
            "NO_QUERY_INDEPENDENT_GENERAL_SCALE_OWNER_FOUND__"
            "GENERAL_HISTORY_AND_VALUE_LAW_OPEN"
        ),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {result['passed']}/{result['total']} exact G132 production checks" if result["status"] == "PASS" else json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
