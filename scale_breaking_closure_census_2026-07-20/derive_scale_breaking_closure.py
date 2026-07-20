#!/usr/bin/env python3
"""Exact homothety, rank, density, Xmax-reciprocity, and local-CSN audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def need(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    lam, X, r, x, M, c, G, alpha, gamma, kV = sp.symbols(
        "lambda X r x M c G alpha gamma kV", positive=True
    )
    eta, epsilon = sp.symbols("eta epsilon", real=True)
    checks: dict[str, str] = {}

    def scaled(expr: sp.Expr) -> sp.Expr:
        return sp.simplify(expr.subs({X: lam * X, r: lam * r, x: lam * x, M: lam * M}, simultaneous=True))

    def has_weight(name: str, expr: sp.Expr, weight: int) -> None:
        need(name, sp.simplify(scaled(expr) - lam**weight * expr) == 0, checks)

    # Dimensionless positional structure, including the owner-requested Xmax reciprocity hypothesis.
    xi = x / X
    composition = (xi + eta) / (1 + xi * eta)
    has_weight("xmax_ratio_weight_zero", xi, 0)
    has_weight("xmax_fractional_composition_weight_zero", composition, 0)
    reverse = sp.simplify(composition.subs(eta, -eta))
    need("xmax_composition_remains_dimensionless_under_reversal", not reverse.has(lam), checks)

    # Recorded WR-L ratio/profile and exact metric scalars.
    A = 1 - r / X
    lapse = sp.sqrt(A)
    has_weight("WRL_profile_weight_zero", A, 0)
    has_weight("WRL_lapse_weight_zero", lapse, 0)
    ell = 2 * X
    area = 4 * sp.pi * X**2
    volume = sp.Rational(64, 15) * sp.pi * X**3
    ricci_wall = 6 / X**2
    kretschmann_wall = 8 / X**4
    surface_gravity = 1 / (2 * X)
    raw_flux = -2 * sp.pi * X
    has_weight("proper_reach_weight_one", ell, 1)
    has_weight("wall_area_weight_two", area, 2)
    has_weight("proper_volume_weight_three", volume, 3)
    has_weight("wall_Ricci_weight_minus_two", ricci_wall, -2)
    has_weight("wall_Kretschmann_weight_minus_four", kretschmann_wall, -4)
    has_weight("surface_gravity_weight_minus_one", surface_gravity, -1)
    has_weight("raw_flux_weight_one", raw_flux, 1)

    # Observed anchors calibrate mass per length, while current closure variables remain dimensionless.
    mass_per_length = c**2 / G
    compactness = G * M / (c**2 * X)
    rho = M / (kV * X**3)
    density_number = G * rho * X**2 / c**2
    has_weight("observed_mass_per_length_weight_zero", mass_per_length, 0)
    has_weight("compactness_weight_zero", compactness, 0)
    has_weight("total_density_weight_minus_two", rho, -2)
    has_weight("dimensionless_density_weight_zero", density_number, 0)
    need("dimensionless_density_is_dependent_compactness", sp.simplify(density_number - compactness / kV) == 0, checks)

    # General dimensional theorem for the presently accepted calibrated variables.
    # Columns are monomial exponents of (M, X, c, G); rows are dimensions (L, mass, T).
    dimension_matrix = sp.Matrix([
        [0, 1, 1, 3],
        [1, 0, 0, -1],
        [0, 0, -1, -2],
    ])
    dimensional_nullspace = dimension_matrix.nullspace()
    need("MXcG_has_one_dimensionless_group", len(dimensional_nullspace) == 1, checks)
    need("unique_group_is_compactness", dimensional_nullspace[0] == sp.Matrix([1, -1, -2, 1]), checks)
    a_c, a_G = sp.symbols("a_c a_G")
    length_system = sp.solve(
        [a_c + 3 * a_G - 1, -a_G, -a_c - 2 * a_G], [a_c, a_G], dict=True
    )
    mass_system = sp.solve(
        [a_c + 3 * a_G, -a_G - 1, -a_c - 2 * a_G], [a_c, a_G], dict=True
    )
    need("c_and_G_cannot_form_length", length_system == [], checks)
    need("c_and_G_cannot_form_mass", mass_system == [], checks)

    # The two proposed M-X relations are homogeneous and rank one when mutually consistent.
    e1 = X - alpha * G * M / c**2
    e2 = M - gamma * c**2 * X / G
    has_weight("X_from_mass_relation_weight_one", e1, 1)
    has_weight("mass_from_X_relation_weight_one", e2, 1)
    coefficient_matrix = sp.Matrix([[1, -alpha * G / c**2], [-gamma * c**2 / G, 1]])
    need("linear_pair_determinant", sp.simplify(coefficient_matrix.det() - (1 - alpha * gamma)) == 0, checks)
    consistent_matrix = coefficient_matrix.subs(gamma, 1 / alpha)
    need("consistent_pair_rank_one", consistent_matrix.rank() == 1, checks)
    null_vector = sp.Matrix([alpha * G / c**2, 1])
    need("consistent_pair_has_positive_scale_direction", sp.simplify(consistent_matrix * null_vector) == sp.zeros(2, 1), checks)
    log_pair = sp.Matrix([[1, -1], [-1, 1]])  # columns log X, log M
    need("log_pair_rank_one", log_pair.rank() == 1, checks)
    need("log_pair_homothety_null", log_pair * sp.Matrix([1, 1]) == sp.zeros(2, 1), checks)

    # An independently derived density center would add genuinely independent information.
    density_log_row = sp.Matrix([[-3, 1]])
    combined_density_rows = sp.Matrix.vstack(sp.Matrix([[1, -1]]), density_log_row)
    need("independent_density_row_rank_two", combined_density_rows.rank() == 2, checks)
    need("independent_density_row_determinant_nonzero", combined_density_rows.det() == -2, checks)
    rho_star = sp.symbols("rho_star", positive=True)
    X_from_density = sp.sqrt(gamma * c**2 / (kV * G * rho_star))
    need(
        "conditional_density_center_solution",
        sp.simplify((gamma * c**2 * X_from_density / G) / (kV * X_from_density**3) - rho_star) == 0,
        checks,
    )
    R_star, A_star = sp.symbols("R_star A_star", positive=True)
    need("conditional_curvature_target_solution", sp.simplify(6 / sp.sqrt(6 / R_star) ** 2 - R_star) == 0, checks)
    need("conditional_area_target_solution", sp.simplify(4 * sp.pi * sp.sqrt(A_star / (4 * sp.pi)) ** 2 - A_star) == 0, checks)

    # Clock-curvature residuals are homogeneous zero equations; they can select profile, not X.
    y = r / X
    trial_A = (1 - y) * (1 + epsilon * y * (1 - y))
    clock_residual = sp.simplify(sp.diff(trial_A, r, 2) + sp.diff(trial_A, r) / r + (1 - trial_A) / r**2)
    has_weight("clock_curvature_residual_weight_minus_two", clock_residual, -2)
    need("clock_curvature_trial_nonzero", sp.simplify(clock_residual.subs({epsilon: sp.Rational(1, 2), r: X / 2})) != 0, checks)

    # Dimensionless topology cannot break the common scale.
    Q = sp.symbols("Q", integer=True)
    has_weight("topological_integer_weight_zero", Q, 0)

    # A fixed global X does not fix the endpoint-flat local CSN representative.
    z = sp.symbols("z", real=True)
    bump = z**2 * (1 - z) ** 2
    need("local_CSN_bump_endpoint_values", bump.subs(z, 0) == 0 and bump.subs(z, 1) == 0, checks)
    need(
        "local_CSN_bump_endpoint_slopes",
        sp.diff(bump, z).subs(z, 0) == 0 and sp.diff(bump, z).subs(z, 1) == 0,
        checks,
    )
    Omega = sp.exp(epsilon * bump)
    need("local_CSN_bump_nontrivial_interior", Omega.subs(z, sp.Rational(1, 2)) == sp.exp(epsilon / 16), checks)
    volume_response = 12 * sp.pi * X**3 * sp.integrate(z**2 * bump / sp.sqrt(1 - z), (z, 0, 1))
    need("local_CSN_volume_response", sp.simplify(volume_response - 1024 * sp.pi * X**3 / 5005) == 0, checks)
    has_weight("local_CSN_volume_response_weight_three", volume_response, 3)

    result = {
        "schema": "udt-scale-breaking-closure-census-1.0",
        "result": "PASS",
        "checks": checks,
        "homothety": {
            "diagnostic": "X,r,x,M -> lambda*(X,r,x,M); measured c_E and G_obs fixed",
            "meaning": "tests scale rank of the recorded solution family; not an observer transformation",
            "available_log_rank": 1,
            "unknowns": ["log(Xmax)", "log(M_tot)"],
            "null_direction": [1, 1],
        },
        "xmax_reciprocity": {
            "status": "CONDITIONAL_HYPOTHESIS_RETAINED",
            "dimensionless_position": "xi=x/Xmax",
            "composition": "(xi+eta)/(1+xi*eta)",
            "scale_weight": 0,
            "ruling": "COMPATIBLE_WITH_ANY_COMMON_SCALE; DOES_NOT_SELECT_XMAX_VALUE",
        },
        "current_closure": {
            "mass_length_pair": "rank one when alpha*gamma=1; no isolated positive scale",
            "density_definition": "G*rho_tot*Xmax^2/c_E^2 = compactness/kV; no independent row",
            "boundary_scalars": "homogeneous powers of Xmax without independently derived target values",
            "topology": "dimensionless and scale blind",
            "noncircular_scale_breaker_found": False,
        },
        "dimensional_theorem": {
            "variables": ["M_tot", "Xmax", "c_E", "G_obs", "dimensionless metric/state data"],
            "dimension_matrix_rank": dimension_matrix.rank(),
            "dimensionless_nullspace": [1, -1, -2, 1],
            "unique_group": "G_obs*M_tot/(c_E^2*Xmax)",
            "c_E_and_G_obs_form_length": False,
            "c_E_and_G_obs_form_mass": False,
            "ruling": "ANY_CLOSURE_USING_ONLY_THESE_OBJECTS_CAN_SELECT_COMPACTNESS_NOT_ABSOLUTE_SCALE",
        },
        "conditional_future_routes": {
            "native_density_center": "would raise log rank to two if independently derived",
            "native_boundary_eigenvalue": "could select Xmax if its nonzero value is independently derived",
            "warning": "neither object exists in current foundation; examples are rank diagnostics, not proposals to insert values",
        },
        "local_representative": {
            "ruling": "GLOBAL_XMAX_SELECTION_WOULD_NOT_ALONE_FIX_COMPLETE_CSN_REPRESENTATIVE",
            "counterfamily": "Omega=exp(epsilon*y^2*(1-y)^2)",
            "volume_first_variation": "1024*pi*X^3/5005",
        },
        "maximum_conclusion": "NO_NONCIRCULAR_SCALE_BREAKER_FOUND_IN_AUDITED_CURRENT_FOUNDATION",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
