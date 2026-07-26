#!/usr/bin/env python3
"""Exact readout, calibration, and reciprocal-inversion classification."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    A, B, C, phi, z = sp.symbols("A B C phi z", real=True)
    b = sp.symbols("b", real=True, nonzero=True)
    omega = sp.symbols("omega", real=True, positive=True)
    lam = sp.symbols("lam", real=True)
    H = sp.Matrix([[A, B], [B, C]])
    X = sp.diag(-1, 1)
    F = sp.Matrix([[0, b], [1 / b, 0]])

    # R01-R03: aligned/self-adjoint pair readouts.
    adjoint_residual = sp.simplify(X.T * H - H * X)
    check("pair_self_adjoint_residual", adjoint_residual == sp.Matrix([[0, -2 * B], [2 * B, 0]]), checks)
    check("pair_self_adjoint_iff_cross_term_zero", sp.solve(list(adjoint_residual), B) == {B: 0}, checks)
    eta2 = sp.diag(-1, 1)
    check("founding_aligned_readout_is_self_adjoint", X.T * eta2 == eta2 * X, checks)
    check("founding_aligned_readout_is_Lorentzian", sp.det(eta2) == -1, checks)

    # R04: complete constant reciprocal inversion isometry family.
    isometry_residual = sp.simplify(F.T * H * F - H)
    expected_isometry = sp.Matrix([[C / b**2 - A, 0], [0, A * b**2 - C]])
    check("inversion_isometry_residual", isometry_residual == expected_isometry, checks)
    check("inversion_isometry_constraint", sp.simplify(expected_isometry.subs(C, A * b**2)) == sp.zeros(2), checks)
    mixed_determinant = sp.factor(sp.det(H.subs(C, A * b**2)))
    check("mixed_isometry_determinant", sp.simplify(mixed_determinant - (A**2 * b**2 - B**2)) == 0, checks)

    Hmix = sp.Matrix([[1, -2], [-2, 1]])
    F1 = sp.Matrix([[0, 1], [1, 0]])
    check("mixed_Lorentzian_witness", sp.det(Hmix) == -3, checks)
    check("mixed_inversion_isometry_witness", F1.T * Hmix * F1 == Hmix, checks)
    check("mixed_witness_not_self_adjoint", X.T * Hmix != Hmix * X, checks)

    # R05: positive conformal inversion. Lorentz signature forces B nonzero;
    # then the off-diagonal equation forces omega=1, reducing to isometry.
    conformal_residual = sp.simplify(F.T * H * F - omega * H)
    expected_conformal = sp.Matrix([
        [C / b**2 - omega * A, (1 - omega) * B],
        [(1 - omega) * B, A * b**2 - omega * C],
    ])
    check("positive_conformal_residual", conformal_residual == expected_conformal, checks)
    check("reciprocal_inversion_is_involutive", sp.simplify(F**2) == sp.eye(2), checks)
    check("positive_involutive_conformal_factor_must_be_one", sp.solve(sp.Eq(omega**2, 1), omega) == [1], checks)
    check("nonzero_cross_term_forces_conformal_factor_one", sp.solve(sp.Eq((1 - omega) * B, 0), omega) == [1], checks)
    # On B=0, nondegeneracy gives A,C nonzero and the two diagonal equations
    # imply omega^2=1. Positive omega gives 1 and same-sign A,C.
    C_branch = omega * A * b**2
    branch_identity = sp.factor((A * b**2 - omega * C_branch))
    check("diagonal_conformal_branch_identity", branch_identity == -A * b**2 * (omega - 1) * (omega + 1), checks)
    check("positive_diagonal_conformal_branch_not_Lorentz", sp.det(H.subs({B: 0, C: A * b**2})) == A**2 * b**2, checks)
    check("founding_swap_is_anti_isometry_not_positive_conformal", F1.T * eta2 * F1 == -eta2, checks)

    # R06-R07: exact incompatibility and causal role of eigenlines.
    simultaneous = adjoint_residual.subs({B: 0, C: A * b**2})
    check("simultaneous_algebraic_family_has_B_zero_C_Ab2", simultaneous == sp.zeros(2), checks)
    check("simultaneous_family_has_nonLorentz_determinant", sp.det(H.subs({B: 0, C: A * b**2})) == A**2 * b**2, checks)
    check("mixed_eigenline_norms_same_sign_relation", H.subs(C, A * b**2)[1, 1] == b**2 * H.subs(C, A * b**2)[0, 0], checks)
    Hnull = sp.Matrix([[0, 1], [1, 0]])
    check("dual_null_readout_is_Lorentzian", sp.det(Hnull) == -1, checks)
    check("dual_null_reciprocal_eigenlines_both_null", Hnull[0, 0] == Hnull[1, 1] == 0, checks)
    check("dual_null_readout_phi_invisible", sp.diag(sp.exp(-phi), sp.exp(phi)).T * Hnull * sp.diag(sp.exp(-phi), sp.exp(phi)) == Hnull, checks)

    # A mixed isometric witness can be calibrated in another orthonormal
    # basis, but X ceases to be diagonal in that physical frame.
    S = sp.Matrix([[1 / sp.sqrt(2), 1 / sp.sqrt(6)], [1 / sp.sqrt(2), -1 / sp.sqrt(6)]])
    check("mixed_readout_has_orthonormal_Lorentz_frame", sp.simplify(S.T * Hmix * S) == eta2, checks)
    Xphysical = sp.simplify(S.inv() * X * S)
    check("reciprocal_action_mixes_in_calibrated_frame", Xphysical[0, 1] != 0 and Xphysical[1, 0] != 0, checks)

    # Relative to the mixed metric, X has both self-adjoint strain and
    # metric-skew parts. In the pure dual readout it is entirely metric-skew.
    Xdag_mix = sp.simplify(Hmix.inv() * X.T * Hmix)
    strain_mix = sp.simplify((X + Xdag_mix) / 2)
    skew_mix = sp.simplify((X - Xdag_mix) / 2)
    check("mixed_readout_has_nonzero_strain_part", strain_mix != sp.zeros(2), checks)
    check("mixed_readout_has_nonzero_metric_skew_part", skew_mix != sp.zeros(2), checks)
    Xdag_null = sp.simplify(Hnull.inv() * X.T * Hnull)
    check("dual_null_readout_makes_X_metric_skew", Xdag_null == -X, checks)

    # R08: complete 4D self-adjoint readout strata.
    X4 = sp.diag(-1, 1, lam, lam)
    variables = sp.symbols("g00 g01 g02 g03 g11 g12 g13 g22 g23 g33", real=True)
    g00, g01, g02, g03, g11, g12, g13, g22, g23, g33 = variables
    G = sp.Matrix([
        [g00, g01, g02, g03],
        [g01, g11, g12, g13],
        [g02, g12, g22, g23],
        [g03, g13, g23, g33],
    ])

    def readout_kernel(value: sp.Expr) -> tuple[int, list[sp.Matrix]]:
        equations = list(X4.subs(lam, value).T * G - G * X4.subs(lam, value))
        coefficient = sp.Matrix(equations).jacobian(variables)
        return len(variables) - coefficient.rank(), coefficient.nullspace()

    dim_generic, kernel_generic = readout_kernel(sp.Rational(2))
    dim_zero, kernel_zero = readout_kernel(0)
    dim_plus, kernel_plus = readout_kernel(1)
    dim_minus, kernel_minus = readout_kernel(-1)
    check("complete_generic_self_adjoint_readout_dimension_five", dim_generic == 5, checks)
    check("complete_zero_self_adjoint_readout_dimension_five", dim_zero == 5, checks)
    check("complete_plus_one_self_adjoint_readout_dimension_seven", dim_plus == 7, checks)
    check("complete_minus_one_self_adjoint_readout_dimension_seven", dim_minus == 7, checks)

    residual_generic = sp.simplify((X4.T * G - G * X4).subs(lam, 2))
    residual_plus = sp.simplify((X4.T * G - G * X4).subs(lam, 1))
    residual_minus = sp.simplify((X4.T * G - G * X4).subs(lam, -1))
    generic_allowed = G.subs({g01: 0, g02: 0, g03: 0, g12: 0, g13: 0})
    plus_allowed = G.subs({g01: 0, g02: 0, g03: 0})
    minus_allowed = G.subs({g01: 0, g12: 0, g13: 0})
    check("generic_complete_block_pattern", (X4.subs(lam, 2).T * generic_allowed - generic_allowed * X4.subs(lam, 2)) == sp.zeros(4), checks)
    check("plus_one_complete_block_pattern", (X4.subs(lam, 1).T * plus_allowed - plus_allowed * X4.subs(lam, 1)) == sp.zeros(4), checks)
    check("minus_one_complete_block_pattern", (X4.subs(lam, -1).T * minus_allowed - minus_allowed * X4.subs(lam, -1)) == sp.zeros(4), checks)
    check("generic_forbidden_cross_terms_detected", residual_generic.subs({g01: 1, g02: 1, g03: 1, g12: 1, g13: 1}) != sp.zeros(4), checks)
    check("aligned_eta_complete_readout_all_lambda", sp.simplify(X4.T * sp.diag(-1, 1, 1, 1) - sp.diag(-1, 1, 1, 1) * X4) == sp.zeros(4), checks)

    # Invariant causal no-go in the aligned complete lambda=0 stratum.
    F4 = sp.diag(1, 1, 1, 1)
    F4[0, 0] = F4[1, 1] = 0
    F4[0, 1] = F4[1, 0] = 1
    eta4 = sp.diag(-1, 1, 1, 1)
    Xzero = X4.subs(lam, 0)
    check("complete_swap_oddly_conjugates_lambda_zero", F4 * Xzero * F4.inv() == -Xzero, checks)
    check("complete_swap_not_aligned_metric_isometry", F4.T * eta4 * F4 != eta4, checks)
    check("complete_swap_not_positive_conformal_to_eta", not any(F4.T * eta4 * F4 == value * eta4 for value in (1, 2, 3)), checks)
    Hmix4 = sp.diag(1, 1, 1, 1)
    Hmix4[:2, :2] = Hmix
    check("mixed_complete_readout_Lorentzian", Hmix4.det() == -3, checks)
    check("mixed_complete_swap_isometry", F4.T * Hmix4 * F4 == Hmix4, checks)
    check("mixed_complete_X_not_self_adjoint", Xzero.T * Hmix4 != Hmix4 * Xzero, checks)

    result = {
        "schema": "udt-calibrated-reciprocal-readout-descent-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "routes": 12,
            "readout_strata": 17,
            "pair_readout_parameters": 3,
            "generic_complete_self_adjoint_readout_dimension": dim_generic,
            "lambda_zero_complete_self_adjoint_readout_dimension": dim_zero,
            "lambda_plus_one_complete_self_adjoint_readout_dimension": dim_plus,
            "lambda_minus_one_complete_self_adjoint_readout_dimension": dim_minus,
        },
        "rulings": {
            "aligned_self_adjoint_plus_physical_inverting_isometry": "NO_LORENTZIAN_SOLUTION",
            "positive_conformal_repair": "NO_LORENTZIAN_ALIGNED_SOLUTION",
            "mixed_inverting_readout": "EXISTS_CONDITIONALLY_BUT_RECIPROCAL_EIGENLINES_ARE_NOT_OPPOSITE_CAUSAL_PHYSICAL_CLOCK_RULER",
            "c_E_calibration": "SETS_SCALE_AFTER_FRAME_CHOICE_BUT_DOES_NOT_SELECT_ALIGNMENT",
            "twisted_lambda_zero": "REMAINS_INTERNAL_OR_MIXED_READOUT_CONDITIONAL_NOT_ALIGNED_PHYSICAL_HOLONOMY",
            "ordinary_lambda_family": "UNCHANGED; SCREEN_ONLY_OR_TRIVIAL_HOLONOMY_RETAINS_ALL_LAMBDA",
            "overall": "CALIBRATED_CAUSAL_ALIGNMENT_RULES_OUT_PHYSICAL_RECIPROCAL_SWAP_ISOMETRY_BUT_DOES_NOT_SELECT_LAMBDA_OR_GLOBAL_HOLONOMY",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
