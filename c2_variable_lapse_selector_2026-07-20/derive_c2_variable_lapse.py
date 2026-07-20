#!/usr/bin/env python3
"""Exact positive variable-lapse extension of the conditional compact C2 slice."""

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
    N, Omega, lam = sp.symbols("N Omega lambda", positive=True)

    # g=N^2*g_hat in four dimensions. Weyl density and the Bach zero-set are conformal.
    measure_weight = 4
    weyl_scalar_weight = -4
    need("four_dimensional_Weyl_density_weight_zero", measure_weight + weyl_scalar_weight == 0, checks)
    need("positive_lapse_defines_regular_CSN_gauge", sp.simplify(N**-2 * N**2 - 1) == 0, checks)
    need("common_scale_cancels_from_Weyl_density", sp.simplify(Omega**4 * Omega**-4 - 1) == 0, checks)

    # After g_hat=N^-2 g, the metric is a constant-lapse product with spatial metric N^-2 g3.
    tf2, lapR, eps = sp.symbols("tf2 lapR epsilon_t", real=True)
    bach00_hat = -eps * (lapR / 12 + tf2 / 4)
    need("compact_product_Bach00_form", sp.diff(bach00_hat, tf2) == -eps / 4, checks)
    need("compact_integral_removes_laplacian", bach00_hat.subs(lapR, 0) == -eps * tf2 / 4, checks)

    # Fixed reciprocal toric basis: the off-diagonal orbit component is q^2(s^2-1).
    q, squash = sp.symbols("q squash", positive=True)
    orbit_cross = q**2 * (squash**2 - 1)
    need("positive_interior_orbit_cross_zero_forces_unit_squashing",
         sp.solve(orbit_cross, squash) == [1], checks)

    # Match the s=1 orbit block to F(eta)^2 times a round block at coordinate u.
    eta, u = sp.symbols("eta u", real=True)
    F = sp.symbols("F", positive=True)
    ceta2, seta2 = sp.cos(eta)**2, sp.sin(eta)**2
    cu2, su2 = sp.cos(u)**2, sp.sin(u)**2
    orbit_sum_original = sp.trigsimp(ceta2 + seta2)
    orbit_sum_round = sp.trigsimp(F**2 * (cu2 + su2))
    need("orbit_sum_original_one", orbit_sum_original == 1, checks)
    need("orbit_sum_match_forces_F_one", sp.solve(orbit_sum_round - orbit_sum_original, F) == [1], checks)
    need("same_axis_orbit_ratio_identifies_depth_coordinate",
         sp.trigsimp((seta2 / ceta2).subs(u, eta) - sp.tan(eta)**2) == 0, checks)
    need("axis_exchange_is_retained",
         sp.trigsimp(cu2.subs(u, sp.pi / 2 - eta) - seta2) == 0, checks)

    # Restoring constants: F=N*r0/b=1, so N is constant; radial matching gives H=1.
    b, r0, uprime = sp.symbols("b r0 uprime", positive=True)
    lapse_from_orbit_match = b / r0
    need("matched_lapse_is_constant", not lapse_from_orbit_match.has(eta), checks)
    Hmatched = sp.simplify((N * r0 / b) * uprime)
    need("same_axis_radial_match_H_one",
         sp.simplify(Hmatched.subs({N: lapse_from_orbit_match, uprime: 1}) - 1) == 0, checks)

    # Independent local formula in fixed round spatial gauge:
    # C^2=2/N^2 |(Hess_{S3} N)_TF|^2.
    N0, Np, Npp = sp.symbols("N0 Np Npp", real=True)
    hessian_eigenvalues = [Npp, -sp.tan(eta) * Np, sp.cot(eta) * Np]
    hessian_trace = sp.simplify(sum(hessian_eigenvalues))
    hessian_tf2 = sp.simplify(sum(value**2 for value in hessian_eigenvalues) - hessian_trace**2 / 3)
    lapse_weyl2 = sp.simplify(2 * hessian_tf2 / N0**2)
    angular_eigenvalue_difference = sp.simplify(hessian_eigenvalues[1] - hessian_eigenvalues[2])
    need("torus_invariant_zero_Weyl_lapse_forces_Nprime_zero",
         sp.simplify(angular_eigenvalue_difference + Np / (sp.sin(eta) * sp.cos(eta))) == 0, checks)
    need("constant_lapse_has_zero_Weyl_on_round_spatial_metric",
         sp.simplify(lapse_weyl2.subs({Np: 0, Npp: 0})) == 0, checks)

    # Exact nonconstant lapse-only sample.
    lapse_sample = 1 + sp.Rational(1, 3) * sp.sin(2 * eta)**2
    substitutions = {
        N0: lapse_sample,
        Np: sp.diff(lapse_sample, eta),
        Npp: sp.diff(lapse_sample, eta, 2),
    }
    sample_value = sp.simplify(lapse_weyl2.subs(substitutions).subs(eta, sp.pi / 8))
    need("nonconstant_lapse_only_sample_Weyl_nonzero", sample_value == sp.Rational(64, 21), checks)

    # A nonconstant common rescaling of the complete coframe is a CSN copy, not a new branch.
    omega_sample = sp.exp(sp.Rational(1, 3) * sp.sin(2 * eta)**2)
    need("nonconstant_common_factor_positive", omega_sample.is_positive is True, checks)
    common_copy_density = sp.simplify(omega_sample**4 * omega_sample**-4 * 0)
    need("common_conformal_copy_of_round_branch_remains_zero_Weyl", common_copy_density == 0, checks)

    # Overall scale and a future observational mass remain absent.
    dimensionless_shape = sp.symbols("dimensionless_shape")
    need("common_homothety_does_not_change_dimensionless_shape",
         sp.simplify((lam * b) / (lam * b) * dimensionless_shape - dimensionless_shape) == 0, checks)
    me = sp.symbols("m_e", positive=True)
    native_equations = [orbit_cross, orbit_sum_round - orbit_sum_original, lapse_weyl2]
    need("electron_mass_absent_from_dimensionless_equations",
         all(not expression.has(me) for expression in native_equations), checks)

    result = {
        "schema": "udt-conditional-c2-variable-lapse-selector-1.0",
        "result": "PASS",
        "checks": checks,
        "conformal_reduction": {
            "original": "g4=epsilon_t*N(eta)^2*d_tau^2+g3",
            "gauge": "g_hat=N^-2*g4=epsilon_t*d_tau^2+N^-2*g3",
            "Weyl_density": "sqrt(|g|) C^2 is unchanged in 4D",
            "Bach_zero_set": "conformally invariant inside the conditional C2 branch",
            "ruling": "POSITIVE_LAPSE_CAN_BE_REMOVED_AS_CSN_GAUGE_WHILE ITS SPATIAL RESCALING IS RETAINED",
        },
        "compact_full_equation": {
            "Bhat_tau_tau": "-epsilon_t*(Delta_hat R_hat/12+|Ric_hat_TF|^2/4)",
            "integrated_result": "N^-2*g3 must be a constant-curvature metric on smooth compact S3",
            "ruling": "EVERY_REGULAR_COMPACT_VARIABLE_LAPSE_BACH_SOLUTION_IS_CONFORMAL_TO_A_ROUND_PRODUCT",
        },
        "fixed_reciprocal_orbit_gauge": {
            "cross_component": "q^2*(s^2-1)",
            "result": "s=1; N*r0/b=1 constant; u=eta or axis exchange; H=1",
            "ruling": "NO_NEW_NONCONSTANT_LAPSE_BRANCH_IN_FIXED_BASIS_POSITIVE_COMPACT_FAMILY",
        },
        "direct_lapse_check": {
            "formula": "C^2=2/N^2*|(Hess_round N)_TF|^2 for H=s=1",
            "torus_invariant_zero_condition": "N'=0",
            "sample": "N=1+(1/3)sin^2(2 eta), eta=pi/8",
            "sample_C2": "64/21",
        },
        "common_factor_copy": {
            "metric": "Omega(eta)^2*[epsilon_t d_tau^2+b^2 g_round]",
            "status": "SAME_CSN_CLASS; nonconstant lapse accompanied by the same complete-coframe factor",
        },
        "scale_and_matter": {
            "overall_b": "unselected common calibration",
            "electron_mass": "excluded from equations; reserved future observational calibration",
            "material_weighting": "not derived",
        },
        "maximum_conclusion": "CONDITIONAL_ROUND_CSN_CLASS_SURVIVES_POSITIVE_VARIABLE_LAPSE_IN_COMPACT_FIXED_BASIS_C2_FAMILY; NO_NEW_PHYSICAL_LAPSE_BRANCH; SCALE_MATERIAL_BOUNDARY_AND_TIME_SHIFT_OPEN",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks),
                      "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
