#!/usr/bin/env python3
"""Hostile algebraic and semantic catches for G192."""

from __future__ import annotations

import ast
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import sympy as sp
from sympy.core.function import AppliedUndef


ROOT = Path(__file__).resolve().parent
SQRT2 = math.sqrt(2.0)


def fresh_production_output():
    env = os.environ.copy()
    env["G192_NO_WRITE"] = "1"
    result = subprocess.run(
        [sys.executable, str(ROOT / "derive_smooth_timelive_mixing.py")],
        cwd=ROOT.parent,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stdout + result.stderr)
    return json.loads(result.stdout)


def parsed_structure(production):
    eta = sp.symbols("eta", real=True)
    local = {
        "eta": eta,
        "a": sp.Function("a"),
        "mu": sp.Function("mu"),
        "I": sp.Function("I"),
        "J": sp.Function("J"),
        "exp": sp.exp,
        "sqrt": sp.sqrt,
    }

    def parse(value):
        return sp.sympify(value, locals=local)

    matrix = sp.Matrix([[parse(value) for value in row] for row in production["jacobi_original"]])
    f_plus = parse(production["jacobi_modes"]["f_plus"])
    f_minus = parse(production["jacobi_modes"]["f_minus"])
    plus_projector = sp.Matrix([[1, 1], [1, 1]]) / 2
    minus_projector = sp.Matrix([[1, -1], [-1, 1]]) / 2
    modal_matrix = f_plus * plus_projector + f_minus * minus_projector
    matrix_modal_residual = (matrix - modal_matrix).applyfunc(sp.simplify)
    determinant_residual = sp.simplify(matrix.det() - parse(production["jacobi_determinant"]))

    I_fun = local["I"](eta)
    J_fun = local["J"](eta)
    A_fun = sp.Function("A", real=True)(eta)
    y_plus = parse(production["jacobi_modes"]["y_plus"])
    factor_formula_residual = sp.simplify(y_plus - sp.exp(-2 * I_fun) * J_fun)
    factor_substitution = {
        sp.diff(I_fun, eta): A_fun,
        sp.diff(I_fun, eta, 2): sp.diff(A_fun, eta),
        sp.diff(J_fun, eta): sp.exp(4 * I_fun),
        sp.diff(J_fun, eta, 2): 4 * A_fun * sp.exp(4 * I_fun),
    }
    factorized_ode_residual = sp.simplify(
        (
            sp.diff(y_plus, eta, 2)
            + (2 * sp.diff(A_fun, eta) - 4 * A_fun**2) * y_plus
        ).subs(factor_substitution)
    )

    formula_values = [
        production["coframe"],
        production["coframe_determinant"],
        production["metric_determinant"],
        production["pair_pullback"],
        *production["affine_ray"],
        production["frequency"],
        production["frequency_derivative"],
        production["frequency_rhs"],
        production["isotropic_tide"],
        production["mixing_tide"],
        production["jacobi_modes"]["y_plus"],
        production["jacobi_modes"]["f_plus"],
        production["jacobi_modes"]["f_minus"],
        production["jacobi_determinant"],
    ]
    for block in (
        production["tidal_original"],
        production["tidal_rotated"],
        production["tracefree_tidal_original"],
        production["jacobi_original"],
    ):
        formula_values.extend(value for row in block for value in row)
    functional_atoms = sorted(
        {
            str(atom.func)
            for value in formula_values
            for atom in parse(value).atoms(AppliedUndef)
        }
    )
    allowed_functional_atoms = {"a", "mu", "I", "J"}

    source_tree = ast.parse((ROOT / "derive_smooth_timelive_mixing.py").read_text(encoding="utf-8"))
    executable_names = {node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)}
    executable_names.update(
        node.attr for node in ast.walk(source_tree) if isinstance(node, ast.Attribute)
    )
    banned_inputs = {
        "P1",
        "G116",
        "G189",
        "X_max",
        "Xmax",
        "luminosity",
        "radiative_transfer",
        "transparent",
    }
    banned_executable_names = sorted(executable_names & banned_inputs)

    evidence = {
        "matrix_shape": list(matrix.shape),
        "matrix_symmetric": matrix == matrix.T,
        "matrix_modal_residual_zero": matrix_modal_residual == sp.zeros(2),
        "matrix_determinant_residual": str(determinant_residual),
        "matrix_cross_term_nonzero": sp.simplify(matrix[0, 1]) != 0,
        "factor_formula_residual": str(factor_formula_residual),
        "factorized_ode_residual": str(factorized_ode_residual),
        "functional_atoms": functional_atoms,
        "functional_atoms_allowed": set(functional_atoms) <= allowed_functional_atoms,
        "banned_executable_names": banned_executable_names,
    }
    return evidence


def rk4_plus(endpoint, L, Lp, Lpp, mu, mup, *, keep_mup=True, keep_mu2=True, curvature_sign=1.0, steps=6000):
    step = endpoint / steps
    state = [0.0, 1.0]

    def rhs(eta, values):
        f, velocity = values
        a = math.exp(L(eta))
        iso = (Lp(eta) ** 2 - Lpp(eta)) / a**4
        mix = 0.0
        if keep_mup:
            mix += 2.0 * SQRT2 * mup(eta) / a**4
        if keep_mu2:
            mix -= 8.0 * mu(eta) ** 2 / a**4
        return [a * a * velocity, -a * a * curvature_sign * (iso + mix) * f]

    def shifted(values, slope, scale):
        return [value + scale * change for value, change in zip(values, slope)]

    eta = 0.0
    for _ in range(steps):
        k1 = rhs(eta, state)
        k2 = rhs(eta + step / 2.0, shifted(state, k1, step / 2.0))
        k3 = rhs(eta + step / 2.0, shifted(state, k2, step / 2.0))
        k4 = rhs(eta + step, shifted(state, k3, step))
        state = [
            value + step * (one + 2.0 * two + 2.0 * three + four) / 6.0
            for value, one, two, three, four in zip(state, k1, k2, k3, k4)
        ]
        eta += step
    return state[0]


def simpson(function, endpoint, steps=20000):
    step = endpoint / steps
    total = function(0.0) + function(endpoint)
    for index in range(1, steps):
        total += (4.0 if index % 2 else 2.0) * function(index * step)
    return total * step / 3.0


def c03_area_squared(endpoint):
    L = lambda e: 0.55 * e - 0.55 * e * e
    I = lambda e: SQRT2 * (0.15 * e + 0.04 * (1.0 - math.cos(2.0 * e)))
    J = simpson(lambda value: math.exp(4.0 * I(value)), endpoint)
    plus = math.exp(L(endpoint) - 2.0 * I(endpoint)) * J
    minus = math.exp(L(endpoint)) * endpoint
    return plus * minus


def main():
    production = fresh_production_output()
    structural = parsed_structure(production)

    L = lambda e: 0.15 * e
    Lp = lambda e: 0.15
    Lpp = lambda e: 0.0
    mu = lambda e: 0.25 * e / SQRT2
    mup = lambda e: 0.25 / SQRT2
    endpoint = 1.2
    correct = rk4_plus(endpoint, L, Lp, Lpp, mu, mup)
    without_mup = rk4_plus(endpoint, L, Lp, Lpp, mu, mup, keep_mup=False)
    without_mu2 = rk4_plus(endpoint, L, Lp, Lpp, mu, mup, keep_mu2=False)
    sign_reversed = rk4_plus(endpoint, L, Lp, Lpp, mu, mup, curvature_sign=-1.0)
    minus_mode = math.exp(L(endpoint)) * endpoint

    # Same Z at eta=.2 and eta=.8 in the preregistered single-turn history,
    # but the screen areas differ: one global d_A(Z) would erase a branch.
    z_left = math.exp(-(0.55 * 0.2 - 0.55 * 0.2**2))
    z_right = math.exp(-(0.55 * 0.8 - 0.55 * 0.8**2))
    area_left = c03_area_squared(0.2)
    area_right = c03_area_squared(0.8)

    # C08 has A' = 2 A^2, hence nonzero coframe mixing but zero central
    # trace-free tide and exactly zero cross response.
    eta_c08 = 0.7
    mu_c08 = -1.0 / (SQRT2 * (2.0 * eta_c08 + 3.0))
    mup_c08 = SQRT2 / (2.0 * eta_c08 + 3.0) ** 2
    tracefree_c08 = SQRT2 * mup_c08 - 4.0 * mu_c08**2

    # C03 and C09 supply fixed counterexamples to forced monotonicity and
    # forced positive cross response.
    c03_lp_left = 0.55 - 1.10 * 0.2
    c03_lp_right = 0.55 - 1.10 * 0.8
    c09_cross = 0.5 * (correct - minus_mode)

    # The constant-mu G191 formula is deliberately misapplied to C09.
    fake_constant_mu = mu(endpoint)
    fake_g191_plus = math.exp(L(endpoint)) * math.sinh(2.0 * SQRT2 * fake_constant_mu * endpoint) / (
        2.0 * SQRT2 * fake_constant_mu
    )

    catches = {
        "mu_prime_deletion_goes_red": abs(without_mup - correct) > 1.0e-4,
        "mu_squared_deletion_goes_red": abs(without_mu2 - correct) > 1.0e-4,
        "curvature_sign_reversal_goes_red": abs(sign_reversed - correct) > 1.0e-4,
        "screen_scalarization_goes_red": abs(c09_cross) > 1.0e-4,
        "forced_positive_cross_goes_red": c09_cross < 0.0,
        "nonzero_mix_need_not_have_tracefree_tide": mu_c08 != 0.0 and abs(tracefree_c08) < 1.0e-14,
        "forced_monotone_frequency_goes_red": c03_lp_left * c03_lp_right < 0.0,
        "frequency_sign_reversal_goes_red": abs(math.exp(-L(endpoint)) - math.exp(L(endpoint))) > 1.0e-3,
        "global_dA_of_Z_across_turn_goes_red": abs(z_left - z_right) < 1.0e-14 and abs(area_left - area_right) > 1.0e-3,
        "constant_G191_substitution_goes_red": abs(fake_g191_plus - correct) > 1.0e-3,
        "matrix_response_retained": (
            structural["matrix_shape"] == [2, 2]
            and structural["matrix_symmetric"]
            and structural["matrix_modal_residual_zero"]
            and structural["matrix_determinant_residual"] == "0"
            and structural["matrix_cross_term_nonzero"]
        ),
        "factorized_positive_mode_retained": (
            structural["factor_formula_residual"] == "0"
            and structural["factorized_ode_residual"] == "0"
        ),
        "P1_not_a_production_input": (
            structural["functional_atoms_allowed"]
            and "P1" not in structural["banned_executable_names"]
        ),
        "G116_not_a_production_input": "G116" not in structural["banned_executable_names"],
        "G189_not_a_production_input": "G189" not in structural["banned_executable_names"],
        "Xmax_not_a_production_input": not {
            "X_max", "Xmax"
        } & set(structural["banned_executable_names"]),
        "radiative_transfer_not_promoted": not {
            "luminosity", "radiative_transfer", "transparent"
        } & set(structural["banned_executable_names"]),
        "turns_are_characterized_not_filtered": (
            c03_lp_left * c03_lp_right < 0.0
            and abs(z_left - z_right) < 1.0e-14
            and abs(area_left - area_right) > 1.0e-3
        ),
    }
    assert all(catches.values()), catches
    result = {
        "status": "PASS",
        "caught": len(catches),
        "catches": catches,
        "control_differences": {
            "delete_mu_prime": abs(without_mup - correct),
            "delete_mu_squared": abs(without_mu2 - correct),
            "reverse_curvature_sign": abs(sign_reversed - correct),
            "forced_constant_G191": abs(fake_g191_plus - correct),
            "same_Z_area_difference": abs(area_left - area_right),
        },
        "structural_evidence": structural,
    }
    if os.environ.get("G192_NO_WRITE") != "1":
        output = ROOT / "CATCH_PROOF_RESULT.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
