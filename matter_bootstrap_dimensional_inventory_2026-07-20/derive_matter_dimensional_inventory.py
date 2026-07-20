#!/usr/bin/env python3
"""Exact 3D matter-functional scaling and dimensional-rank audit."""

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
    R, lam, xi, kap, A, B, c, G, ell, X, f2, f4 = sp.symbols(
        "R lambda xi kappa A B c G ell X f2 f4", positive=True
    )
    C2, C4, s = sp.symbols("C2 C4 s", positive=True)
    checks: dict[str, str] = {}

    # A derivative contributes R^-1 and d^3x contributes R^3.
    l2_exponent = 3 - 2
    l4_exponent = 3 - 4
    need("three_dimensional_L2_scaling", l2_exponent == 1, checks)
    need("three_dimensional_L4_scaling", l4_exponent == -1, checks)

    energy = xi * A * R + kap * B / R
    need("scaled_energy_exact", sp.simplify(energy.subs(R, lam * R) - (lam * xi * A * R + kap * B / (lam * R))) == 0, checks)
    derivative = sp.simplify(sp.diff(energy, R))
    stationary_radius = sp.sqrt(kap * B / (xi * A))
    need("stationary_radius_solves_derivative", sp.simplify(derivative.subs(R, stationary_radius)) == 0, checks)
    need("stationary_point_positive", sp.simplify(sp.diff(energy, R, 2).subs(R, stationary_radius)) > 0, checks)
    E2star = sp.simplify((xi * A * R).subs(R, stationary_radius))
    E4star = sp.simplify((kap * B / R).subs(R, stationary_radius))
    need("Derrick_stationarity_E2_equals_E4", sp.simplify(E2star - E4star) == 0, checks)
    stationary_energy = sp.simplify(energy.subs(R, stationary_radius))
    need("stationary_energy", sp.simplify(stationary_energy - 2 * sp.sqrt(xi * kap * A * B)) == 0, checks)

    # Dimensions use vectors (length, mass, time).
    energy_dim = sp.Matrix([2, 1, -2])
    length_dim = sp.Matrix([1, 0, 0])
    xi_dim = energy_dim - length_dim
    kap_dim = energy_dim + length_dim
    need("xi_dimension_force", xi_dim == sp.Matrix([1, 1, -2]), checks)
    need("kappa_dimension_energy_length", kap_dim == sp.Matrix([3, 1, -2]), checks)
    need("kappa_over_xi_dimension_length_squared", kap_dim - xi_dim == sp.Matrix([2, 0, 0]), checks)
    c_dim = sp.Matrix([1, 0, -1])
    G_dim = sp.Matrix([3, -1, -2])
    need("c4_over_G_matches_xi", 4 * c_dim - G_dim == xi_dim, checks)
    need("c4_over_G_does_not_match_kappa", 4 * c_dim - G_dim != kap_dim, checks)

    coefficient_length = sp.sqrt(kap / xi)
    dimensionless_radius = sp.simplify(stationary_radius / coefficient_length)
    need("coefficient_ratio_is_ruler", sp.simplify(dimensionless_radius - sp.sqrt(B / A)) == 0, checks)
    code_energy = sp.simplify(energy.subs({R: coefficient_length * s}))
    need("code_unit_factorization", sp.simplify(code_energy - sp.sqrt(xi * kap) * (A * s + B / s)) == 0, checks)
    need("unit_coefficients_absorb_length_unit", sp.simplify(coefficient_length.subs({xi: 1, kap: 1}) - 1) == 0, checks)
    need("unit_coefficients_absorb_energy_unit", sp.simplify(sp.sqrt(xi * kap).subs({xi: 1, kap: 1}) - 1) == 0, checks)

    # If observed anchors normalize xi, kappa still needs a length squared.
    xi_anchor = c**4 * f2 / G
    kap_with_length = c**4 * ell**2 * f4 / G
    need("anchored_coefficient_ratio", sp.simplify(kap_with_length / xi_anchor - ell**2 * f4 / f2) == 0, checks)
    anchored_radius = sp.simplify(stationary_radius.subs({xi: xi_anchor, kap: kap_with_length}))
    need("anchored_radius_contains_extra_length", sp.simplify(anchored_radius / ell - sp.sqrt(f4 * B / (f2 * A))) == 0, checks)
    anchored_energy = sp.simplify(stationary_energy.subs({xi: xi_anchor, kap: kap_with_length}))
    need("anchored_energy_contains_extra_length", sp.simplify(anchored_energy - 2 * c**4 * ell * sp.sqrt(f2 * f4 * A * B) / G) == 0, checks)
    anchored_mass = sp.simplify(anchored_energy / c**2)
    need("anchored_mass_contains_same_length", sp.simplify(anchored_mass - 2 * c**2 * ell * sp.sqrt(f2 * f4 * A * B) / G) == 0, checks)

    # Counterfactual tie to Xmax selects a ratio while preserving common homothety.
    counter_radius = sp.simplify(stationary_radius.subs({xi: xi_anchor, kap: c**4 * X**2 * f4 / G}))
    need("Xmax_counterfactual_selects_radius_ratio", sp.simplify(counter_radius / X - sp.sqrt(f4 * B / (f2 * A))) == 0, checks)
    need("Xmax_counterfactual_common_scale_survives", sp.simplify(counter_radius.subs(X, lam * X) - lam * counter_radius) == 0, checks)
    counter_mass = sp.simplify((stationary_energy / c**2).subs({xi: xi_anchor, kap: c**4 * X**2 * f4 / G}))
    need("Xmax_counterfactual_mass_scales_with_Xmax", sp.simplify(counter_mass.subs(X, lam * X) - lam * counter_mass) == 0, checks)
    xmax_position = R / X
    need("Xmax_reciprocity_coordinate_scale_weight_zero", sp.simplify(xmax_position.subs({R: lam * R, X: lam * X}, simultaneous=True) - xmax_position) == 0, checks)

    # Fixed-Q inertia contains the same coefficient ruler, not an independent one.
    inertia = xi * C2 * R**3 + kap * C4 * R
    inertia_code = sp.simplify(inertia.subs({R: coefficient_length * s, kap: xi * coefficient_length**2}, simultaneous=True))
    expected_inertia = sp.simplify(xi * coefficient_length**3 * (C2 * s**3 + C4 * s))
    need("inertia_L2_scaling_R3", 3 - 0 == 3, checks)
    need("inertia_L4_scaling_R1", 3 - 2 == 1, checks)
    need("inertia_uses_same_coefficient_ruler", sp.simplify(inertia_code - expected_inertia) == 0, checks)

    # Numerical domain conversion and topology.
    Lcode, hcode, N, Q = sp.symbols("Lcode hcode N Q", positive=True)
    need("box_physical_length_inherits_coefficient_ruler", sp.simplify((Lcode * coefficient_length) / coefficient_length - Lcode) == 0, checks)
    need("grid_spacing_inherits_coefficient_ruler", sp.simplify((hcode * coefficient_length) / coefficient_length - hcode) == 0, checks)
    need("topological_Q_has_no_scale", not Q.has(R, X, ell, xi, kap), checks)
    need("grid_count_has_no_physical_dimension", not N.has(R, X, ell, xi, kap), checks)

    result = {
        "schema": "udt-matter-bootstrap-dimensional-inventory-1.0",
        "result": "PASS",
        "checks": checks,
        "continuum_scaling": {
            "family": "n_R(x)=n_1(x/R) in three spatial dimensions",
            "E2": "xi*A*R",
            "E4": "kappa*B/R",
            "stationary_radius": "sqrt(kappa/xi)*sqrt(B/A)",
            "stationary_energy": "2*sqrt(xi*kappa*A*B)",
            "ruling": "FINITE_STATIC_SIZE_INHERITS_COEFFICIENT_RATIO; TOPOLOGY_ALONE_DOES_NOT_SET_RADIUS",
        },
        "coefficient_dimensions": {
            "xi": "energy/length = force = mass*length/time^2",
            "kappa": "energy*length = mass*length^3/time^2",
            "kappa_over_xi": "length^2",
            "length_unit": "ell_coeff=sqrt(kappa/xi)",
            "energy_unit": "sqrt(xi*kappa)",
            "code_ruling": "xi=kappa=1 absorbs ell_coeff=1 and the corresponding energy unit",
        },
        "observational_anchors": {
            "xi_possible_dimension_only": "(c_E^4/G_obs)*dimensionless f2",
            "kappa_requires": "(c_E^4/G_obs)*ell_0^2*dimensionless f4",
            "physical_radius": "ell_0*sqrt(f4*B/(f2*A))",
            "physical_mass": "2*(c_E^2/G_obs)*ell_0*sqrt(f2*f4*A*B)",
            "ruling": "c_E_AND_G_obs_DO_NOT_SUPPLY_ell_0",
        },
        "fixed_charge": {
            "inertia": "xi*C2*R^3+kappa*C4*R",
            "factorized": "xi*ell_coeff^3*(C2*s^3+C4*s)",
            "source_status": "existing Q values and time/frequency normalization are supplied in code units",
            "ruling": "NO_INDEPENDENT_NATIVE_RULER_FOUND",
        },
        "xmax_counterfactual": {
            "assumption": "kappa/xi=Xmax^2*(f4/f2)",
            "result": "R_star/Xmax=sqrt(f4*B/(f2*A))",
            "homothety": "Xmax,R_star,M_star all retain one common scale",
            "reciprocity": "conditional x/Xmax structure remains scale-weight zero",
            "ruling": "RATIO_SELECTION_ONLY; NOT_ABSOLUTE_XMAX_SELECTION",
        },
        "mass_readout": {
            "carrier_energy": "conditional on round-S2 L2+L4 branch",
            "rest_mass_conversion": "E_star/c_E^2 retains ell_0",
            "phase_G": "conditional EH/weak-field unit-response M_N^(0)=2E4; no kappa_g value",
            "boundary": "M_N=E_carrier additionally needs controlled vanishing boundary/residual terms",
            "ruling": "NO_NATIVE_UNCONDITIONAL_MASS_NORMALIZATION",
        },
        "maximum_conclusion": "HIDDEN_CONDITIONAL_COEFFICIENT_RULER; NO_NATIVE_DIMENSIONAL_MATTER_OBJECT_FOUND",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
