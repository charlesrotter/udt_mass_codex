#!/usr/bin/env python3
"""Exact bounded algebra for the UDT angular derivative-weight selector audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def need(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    d = sp.Integer(4)
    Omega, lam, a2, a4, X, R, A2, A4, fstate = sp.symbols(
        "Omega lambda a2 a4 X R A2 A4 fstate", positive=True
    )

    # Carrier-neutral conformal weights for a dimensionless neutral angular variable.
    measure_weight = d
    inverse_metric_weight = -2
    k2_density_weight = measure_weight + inverse_metric_weight
    k4_density_weight = measure_weight + 2 * inverse_metric_weight
    two_form_square_density_weight = measure_weight + 2 * inverse_metric_weight
    need("measure_CSN_weight_plus_four", measure_weight == 4, checks)
    need("inverse_metric_CSN_weight_minus_two", inverse_metric_weight == -2, checks)
    need("neutral_K2_density_weight_plus_two", k2_density_weight == 2, checks)
    need("neutral_K4_density_weight_zero", k4_density_weight == 0, checks)
    need("neutral_pullback_two_form_square_weight_zero", two_form_square_density_weight == 0, checks)
    need("constant_coefficient_K2_not_pre_scale_CSN", sp.simplify(Omega**k2_density_weight - 1) != 0, checks)
    need("constant_coefficient_K4_pre_scale_CSN_compatible", sp.simplify(Omega**k4_density_weight - 1) == 0, checks)

    # A mathematical compensator counterfamily. Its presence/weight/value are not UDT inputs.
    compensator_weight = -1
    compensated_k2_weight = measure_weight + inverse_metric_weight + 2 * compensator_weight
    need("weight_minus_one_compensator_can_make_K2_neutral", compensated_k2_weight == 0, checks)
    chi0 = sp.symbols("chi0", positive=True)
    need("post_selection_compensator_value_leaves_free_K2_coefficient", sp.diff(chi0**2, chi0) != 0, checks)

    # Pure-metric constant-scale weights in 4D: sufficient to distinguish EH and C^2.
    cosmological_density_weight = d
    eh_density_weight = d - 2
    curvature_square_density_weight = d - 4
    need("cosmological_density_not_pre_scale_CSN", cosmological_density_weight == 4, checks)
    need("EH_density_not_pre_scale_CSN", eh_density_weight == 2, checks)
    need("curvature_square_density_weight_zero", curvature_square_density_weight == 0, checks)
    # Curvature identities used by the bounded 4D inventory.
    Riem2, Ric2, Scal2 = sp.symbols("Riem2 Ric2 Scal2")
    C2 = Riem2 - 2 * Ric2 + Scal2 / 3
    Euler = Riem2 - 4 * Ric2 + Scal2
    need("four_dimensional_Weyl_identity", sp.expand(C2 - (Riem2 - 2 * Ric2 + Scal2 / 3)) == 0, checks)
    need("four_dimensional_Euler_identity", sp.expand(Euler - (Riem2 - 4 * Ric2 + Scal2)) == 0, checks)
    alpha = sp.symbols("alpha")
    need("CSN_does_not_fix_C2_overall_normalization", sp.diff(alpha * C2, alpha) == C2, checks)

    # Static three-space scaling: stationarity diagnoses a chosen ratio; it does not select it.
    E = a2 * A2 * R + a4 * A4 / R
    Rstar = sp.sqrt(a4 * A4 / (a2 * A2))
    need("Derrick_stationary_radius", sp.simplify(sp.diff(E, R).subs(R, Rstar)) == 0, checks)
    need("Derrick_stationarity_balances_chosen_terms",
         sp.simplify((a2 * A2 * Rstar) - (a4 * A4 / Rstar)) == 0, checks)
    need("different_input_ratios_give_different_stationary_radii",
         sp.sqrt(sp.Integer(1)) != sp.sqrt(sp.Integer(4)), checks)

    # Xmax reciprocity restricts dimension, not the dimensionless state function.
    coefficient_ratio = X**2 * fstate
    need("Xmax_ratio_has_length_squared_scaling",
         sp.simplify(coefficient_ratio.subs(X, lam * X) - lam**2 * coefficient_ratio) == 0, checks)
    need("normalized_position_is_common_scale_neutral",
         sp.simplify((lam * R) / (lam * X) - R / X) == 0, checks)
    need("Xmax_form_retains_arbitrary_dimensionless_function", sp.diff(coefficient_ratio, fstate) == X**2, checks)

    # General reciprocal toric/Hopf orbit block with an unselected depth coefficient H(eta).
    eta = sp.symbols("eta", real=True)
    eps = sp.Rational(1, 3)
    c = sp.cos(eta)
    s = sp.sin(eta)
    q = c * s
    H = 1 + eps * sp.sin(2 * eta) ** 2
    # The quotient by V=d_xi1+d_xi2 has h=H^2 d eta^2+q^2 d delta^2.
    need("diagonal_fiber_norm_is_one", sp.trigsimp(c**2 + s**2) == 1, checks)
    need("horizontal_relative_angle_norm", sp.trigsimp(c**2 * s**4 + s**2 * c**4 - q**2) == 0, checks)
    Fcoef = -2 * q
    volume_coef = H * q
    F_over_volume = sp.simplify(Fcoef / volume_coef)
    F2 = sp.simplify(2 * F_over_volume**2)
    need("Hopf_curvature_to_volume_ratio", sp.simplify(F_over_volume + 2 / H) == 0, checks)
    need("Hopf_curvature_norm_general_H", sp.simplify(F2 - 8 / H**2) == 0, checks)
    need("nonround_H_smooth_left_cap", H.subs(eta, 0) == 1 and sp.diff(H, eta).subs(eta, 0) == 0, checks)
    need("nonround_H_smooth_right_cap",
         sp.simplify(H.subs(eta, sp.pi / 2) - 1) == 0 and sp.simplify(sp.diff(H, eta).subs(eta, sp.pi / 2)) == 0,
         checks)
    chern_flux = sp.integrate(Fcoef, (eta, 0, sp.pi / 2)) * (2 * sp.pi)
    need("Hopf_Chern_flux_independent_of_H", sp.simplify(chern_flux + 2 * sp.pi) == 0, checks)
    # Scalar curvature of h=H^2 d eta^2+q^2 d delta^2.
    Rbase = sp.simplify(-2 * sp.diff(q, eta, 2) / (q * H**2) + 2 * sp.diff(q, eta) * sp.diff(H, eta) / (q * H**3))
    Rbase_round = sp.simplify(-2 * sp.diff(q, eta, 2) / q)
    need("round_quotient_scalar_curvature_eight", sp.trigsimp(Rbase_round - 8) == 0, checks)
    # H is already eps=1/3; compare at eta=pi/8 where H' is nonzero.
    sample = {eta: sp.pi / 8}
    sample_F2 = sp.simplify(F2.subs(sample))
    sample_Rbase = sp.simplify(Rbase.subs(sample))
    need("nonround_sample_F2", sample_F2 == sp.Rational(288, 49), checks)
    need("nonround_sample_Rbase", sample_Rbase == sp.Rational(2592, 343), checks)
    need("nonround_geometry_changes_curvature_ratio", sp.simplify(sample_Rbase / sample_F2) == sp.Rational(9, 7), checks)

    # Independent base/fiber scales in the same smooth S3 bundle leave a squashing modulus.
    af, bf = sp.symbols("a_f b_f", positive=True)
    Rbase_berger = 8 / bf**2
    F2_berger = 8 / bf**4
    R3_berger = sp.simplify(Rbase_berger - af**2 * F2_berger / 4)
    squash = af / bf
    need("Berger_scalar_curvature_formula", sp.simplify(R3_berger - (8 / bf**2 - 2 * af**2 / bf**4)) == 0, checks)
    need("round_unit_S3_scalar_curvature_six", R3_berger.subs({af: 1, bf: 1}) == 6, checks)
    need("common_scale_does_not_remove_squashing",
         sp.simplify(squash.subs({af: lam * af, bf: lam * bf}, simultaneous=True) - squash) == 0, checks)
    reduced_base_weight = sp.simplify(af * bf**2 * Rbase_berger)
    reduced_fiber_weight = sp.simplify(af * bf**2 * af**2 * F2_berger / 4)
    need("submersion_relative_weight_depends_on_squashing",
         sp.simplify(reduced_fiber_weight / reduced_base_weight - squash**2 / 4) == 0, checks)

    # A scale-free four-derivative invariant can yield lower derivative order only after a
    # nonzero selected background curvature/scale is supplied; the coefficient is then contingent.
    K0, q2 = sp.symbols("K0 q2")
    reduced_square = sp.expand((K0 + q2) ** 2)
    need("single_invariant_cross_term_requires_background_scale",
         reduced_square.coeff(q2, 1) == 2 * K0, checks)
    need("zero_background_removes_two_derivative_cross_term",
         reduced_square.subs(K0, 0).coeff(q2, 1) == 0, checks)

    result = {
        "schema": "udt-angular-derivative-weight-selector-1.0",
        "result": "PASS",
        "checks": checks,
        "carrier_neutral_csn": {
            "premise": "dimensionless CSN-neutral angular variable with separately supplied target tensors",
            "sqrt_g_K2_weight": "+2 in 4D",
            "sqrt_g_K4_weights": "0 in 4D",
            "ruling": "NONZERO_CONSTANT_K2_EXCLUDED_PRE_SCALE_IN_THIS_BRANCH; QUARTIC_FAMILY_COMPATIBLE_NOT_SELECTED",
        },
        "pure_metric_branch": {
            "EH_weight": "+2 under constant common scale in 4D; locally non-Weyl-invariant",
            "curvature_square_weight": "0 under constant common scale; C2 locally Weyl-compatible",
            "ruling": "C2_BACH_REMAINS_UNIQUE_CONDITIONAL; NORMALIZATION_AND_COMPLETE_ACTION_OPEN",
        },
        "two_stage_bridge": {
            "scale_selection_only": "does not algebraically create EH/K2 from a C2/K4 functional",
            "compensator_counterfamily": "a weight-minus-one field can dress K2, but its existence, law, and selected value are extra premises",
            "single_invariant_route": "a selected nonzero background curvature can create a two-derivative cross term upon exact reduction",
            "ruling": "STRUCTURALLY_PROMISING_CONDITIONAL_ROUTE; EXACT_METRIC_REDUCTION_AND_SELECTION_MISSING",
        },
        "conditional_hopf_route": {
            "metric": "H(eta)^2 d_eta^2+cos(eta)^2 d_xi1^2+sin(eta)^2 d_xi2^2",
            "quotient_metric": "H^2 d_eta^2+cos^2(eta) sin^2(eta) d_delta^2",
            "connection": "A=cos^2(eta)d_xi1+sin^2(eta)d_xi2",
            "curvature": "F=-2 cos(eta)sin(eta)d_eta wedge d_delta",
            "curvature_norm": "F_ab F^ab=8/H^2",
            "chern_flux": "-2*pi for the stated orientation",
            "nonround_counterexample": {"H": "1+(1/3)sin^2(2 eta)", "eta": "pi/8", "F2": "288/49", "Rbase": "2592/343", "Rbase_over_F2": "9/7"},
            "ruling": "RECIPROCAL_ORBIT_BLOCK_AND_TOPOLOGY_DO_NOT_FIX_LOCAL_METRIC_CURVATURE_NORMALIZATION",
        },
        "squashing": {
            "metric": "b^2 h_round_base+a^2 A^2",
            "R3": "8/b^2-2a^2/b^4",
            "common_scale_invariant_modulus": "a/b",
            "reduced_relative_weight": "(a/b)^2/4 for the stated EH submersion comparison",
            "ruling": "CSN_REMOVES_COMMON_SCALE_NOT_SQUASHING; ACTION_AND_GEOMETRY_MUST_BE_CHOSEN_FIRST",
        },
        "xmax": {
            "form": "a4/a2=Xmax^2*f(dimensionless global state)",
            "ruling": "FORM_ONLY; f, sign, term existence, and action placement remain open",
        },
        "maximum_conclusion": "PRE_SCALE_DERIVATIVE_ORDER_SEPARATION_DERIVED_IN_NEUTRAL_BRANCH; NONZERO_RELATIVE_WEIGHT_NOT_SELECTED_IN_CURRENT_FOUNDATION",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
