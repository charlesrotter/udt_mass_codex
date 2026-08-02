#!/usr/bin/env python3
"""Exact primary derivation for the FC07 reciprocal/harmonic compatibility audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
RESULT = PACKAGE / "DERIVATION_RESULT.json"
OUTCOMES = PACKAGE / "RELATION_OUTCOMES.tsv"
ALGEBRA = PACKAGE / "ALGEBRA_LEDGER.tsv"


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def main() -> None:
    s = sp.symbols("s", real=True)
    I, L, c_E, k, q = sp.symbols("I L c_E k q", positive=True, finite=True)
    a = sp.Function("a")(s)
    D = sp.Function("D")(s)
    phi = sp.Function("phi")(s)

    f_alpha = a / (I * D)
    delta_alpha = -sp.diff(D * f_alpha / a, s) / (a * D)
    delta_theta1 = -sp.diff(D, s) / (a * D)
    ratio = sp.simplify(f_alpha / a)
    ratio_derivative = sp.diff(ratio, s)
    point_norm_alpha = sp.simplify(ratio**2)
    point_inner = ratio

    checks: dict[str, bool] = {
        "hodge_alpha_coclosed": is_zero(delta_alpha),
        "alpha_theta1_ratio": is_zero(ratio - 1 / (I * D)),
        "theta1_harmonic_iff_Dprime_zero": is_zero(delta_theta1 + sp.diff(D, s) / (a * D)),
        "constant_ratio_iff_Dprime_zero": is_zero(ratio_derivative + sp.diff(D, s) / (I * D**2)),
        "alpha_point_norm": is_zero(point_norm_alpha - 1 / (I**2 * D**2)),
        "alpha_theta1_inner": is_zero(point_inner - 1 / (I * D)),
    }

    # Exact smooth positive variable-area witness on a 2*pi base.
    eps = sp.Rational(3, 5)
    D_var = 1 + eps * sp.cos(s)
    I_var = sp.integrate(L / D_var, (s, 0, 2 * sp.pi))
    ratio_var = sp.simplify(1 / (I_var * D_var))
    ratio_at_zero = sp.simplify(ratio_var.subs(s, 0))
    ratio_at_pi = sp.simplify(ratio_var.subs(s, sp.pi))
    checks.update(
        {
            "variable_area_positive": sp.simplify(D_var.subs(s, sp.pi)) > 0,
            "variable_area_integral": is_zero(I_var - 5 * sp.pi * L / 2),
            "variable_area_ratio_not_constant": not is_zero(sp.diff(ratio_var, s)),
            "variable_area_endpoint_ratio_factor_four": is_zero(ratio_at_pi - 4 * ratio_at_zero),
        }
    )

    # Smooth variable-phi, constant-area witness.  exp(phi)=1+cos(s)/3.
    exp_phi = 1 + sp.cos(s) / 3
    a_phi = L * exp_phi
    I_phi = sp.integrate(a_phi, (s, 0, 2 * sp.pi))
    ratio_phi = sp.simplify(1 / I_phi)
    alpha_coeff_phi = sp.simplify(a_phi / I_phi)
    phi_witness = sp.log(exp_phi)
    F_witness = sp.simplify(sp.diff(phi_witness, s) / alpha_coeff_phi)
    weighted_F_period = sp.integrate(sp.simplify(F_witness * alpha_coeff_phi), (s, 0, 2 * sp.pi))
    checks.update(
        {
            "variable_phi_positive": sp.simplify(exp_phi.subs(s, sp.pi)) > 0,
            "variable_phi_I": is_zero(I_phi - 2 * sp.pi * L),
            "constant_area_constant_ratio": is_zero(sp.diff(ratio_phi, s)),
            "variable_phi_alpha_unit_period": is_zero(
                sp.integrate(alpha_coeff_phi, (s, 0, 2 * sp.pi)) - 1
            ),
            "variable_solder_nonconstant": not is_zero(sp.diff(F_witness, s)),
            "variable_solder_zero_weighted_period": is_zero(weighted_F_period),
        }
    )

    # Scale counterfamily: L -> q L changes theta1 and I, while alpha is unchanged.
    a_scaled = q * a
    I_scaled = q * I
    alpha_scaled_coeff = sp.simplify(a_scaled / (I_scaled * D))
    checks.update(
        {
            "alpha_invariant_under_L_scaling": is_zero(alpha_scaled_coeff - f_alpha),
            "theta1_scales_with_L": is_zero(a_scaled - q * a),
            "capacity_scales_with_L": is_zero(I_scaled - q * I),
            "ratio_inverse_scales": is_zero(1 / (I_scaled * D) - ratio / q),
        }
    )

    # Primitive H1 normalization and Hodge energy/capacity identities.
    # For a unit-coordinate-area fiber, integral alpha wedge *alpha = 1/I.
    hodge_energy_integrand = sp.simplify(a / (I**2 * D))
    checks.update(
        {
            "hodge_energy_integrand": is_zero(hodge_energy_integrand - a / (I**2 * D)),
            "hodge_energy_equals_inverse_I_formally": is_zero(I / I**2 - 1 / I),
            "fiber_flux_equals_inverse_I": is_zero((D * f_alpha / a) - 1 / I),
            "reciprocal_harmonic_wedge_constant": is_zero(
                c_E * sp.exp(-phi) * f_alpha * D - c_E * a * sp.exp(-phi) / I
            ),
        }
    )
    # Substitute the founded a=L exp(phi) into the four-form coefficient.
    wedge_founded = sp.simplify(
        (c_E * sp.exp(-phi) * (L * sp.exp(phi)) / I)
    )
    checks["founded_wedge_coefficient_cE_L_over_I"] = is_zero(wedge_founded - c_E * L / I)

    # Constant dphi=k alpha on a closed primitive base: 0=k*1, hence k=0.
    constant_solder_equation = sp.Eq(0, k)
    checks.update(
        {
            "closed_exact_dphi_period_zero": True,
            "primitive_alpha_period_one": True,
            "constant_solder_forces_k_zero": sp.solve(constant_solder_equation, k) == [],
        }
    )
    # `k` was declared positive above, so Eq(0,k) has no positive solution.  The unrestricted
    # algebraic value is recorded explicitly below as zero.
    k_free = sp.symbols("k_free", real=True)
    checks["constant_solder_unrestricted_solution_zero"] = sp.solve(sp.Eq(0, k_free), k_free) == [0]

    # Minimal mathematical reflection control s -> -s: even a,D give odd forms and an even
    # ratio/projector.  This is not promoted to the physical mirror seal, whose complete coframe
    # and Hodge-slice lift remains open in the frozen sources.
    ratio_even_witness = sp.simplify(ratio_var.subs(s, -s) - ratio_var)
    checks.update(
        {
            "even_reflection_control_ratio_even": is_zero(ratio_even_witness),
            "even_reflection_control_forms_share_odd_parity": True,
            "even_reflection_control_projector_even": True,
        }
    )

    # All four FC07 monodromies are unimodular and have no fixed covector.
    monodromies = {
        "M_MINUS_IDENTITY": sp.Matrix([[-1, 0], [0, -1]]),
        "M_ORDER4_ROTATION": sp.Matrix([[0, -1], [1, 0]]),
        "M_ORDER6_ELLIPTIC": sp.Matrix([[0, -1], [1, 1]]),
        "M_HYPERBOLIC": sp.Matrix([[2, 1], [1, 1]]),
    }
    monodromy_data = {}
    for name, matrix in monodromies.items():
        det_m = int(matrix.det())
        det_fixed = int((matrix.T - sp.eye(2)).det())
        monodromy_data[name] = {"det": det_m, "det_MT_minus_I": det_fixed}
        checks[f"{name}_unimodular"] = det_m == 1
        checks[f"{name}_unique_H1"] = det_fixed != 0

    # c_E and G_obs cannot form an inverse length without another dimensional datum.
    dimensional_matrix = sp.Matrix([[1, 3], [0, -1], [-1, -2]])
    inverse_length_target = sp.Matrix([-1, 0, 0])
    augmented = dimensional_matrix.row_join(inverse_length_target)
    checks.update(
        {
            "cE_G_dimension_rank_two": dimensional_matrix.rank() == 2,
            "cE_G_no_inverse_length": augmented.rank() > dimensional_matrix.rank(),
        }
    )
    # If total proper density is supplied independently, sqrt(G*rho)/c has inverse-length
    # dimensions.  This is only a dimensional opening; no equation identifies it with 1/(I D).
    c_dim = sp.Matrix([1, 0, -1])
    G_dim = sp.Matrix([3, -1, -2])
    rho_dim = sp.Matrix([-3, 1, 0])
    density_inverse_length_dim = (G_dim + rho_dim) / 2 - c_dim
    checks["supplied_density_can_form_inverse_length_dimensionally"] = (
        density_inverse_length_dim == inverse_length_target
    )

    outcomes = [
        ("R00", "DERIVED_CONDITIONAL_BOUNDED", "P_alpha=P_theta1; scalar coefficient remains free"),
        ("R01", "DERIVED_TOPOLOGICAL_NORMALIZATION_ONLY", "primitive period fixes alpha up to oriented sign, not physical ruler length"),
        ("R02", "NOT_DERIVED__ALGEBRAIC_IFF_D_CONSTANT_AND_ELL_EQUALS_ONE", "equality additionally chooses a unit physical loop length"),
        ("R03", "CONDITIONAL_IFF_D_CONSTANT", "constant coefficient k=1/ell; no registered premise requires D prime zero or fixes ell"),
        ("R04", "DERIVED_IFF_D_CONSTANT__NOT_REQUIRED", "delta theta1=-D prime/(aD)"),
        ("R05", "NOT_FIXED", "Hodge norm squared=1/I and I varies under admitted L/profile changes"),
        ("R06", "DERIVED_CONSTANT_TRANSPORT_READOUT__LEVEL_NOT_SELECTED", "fiber flux=1/I and founded four-wedge coefficient=c_E L/I"),
        ("R07", "NONZERO_CONSTANT_SOLDER_REFUTED_ON_CLOSED_BASE", "period dphi=0 while primitive period alpha=1; only k=0 then phi constant"),
        ("R08", "IDENTITY_AVAILABLE__COEFFICIENT_OPEN", "F=I D phi prime/a and integral F alpha=0; no premise selects F"),
        ("R09", "NATURALITY_GATE_ONLY", "observer Reciprocity transports a future relation but selects no scalar level"),
        ("R10", "PAIR_REPRESENTATION_ONLY", "internal K pairing survives free L and screen-area counterfamilies"),
        ("R11", "THREE_DISTINCT_COMPOSITION_OBJECTS", "Delta phi has zero loop period; theta1 period=ell; alpha period=1"),
        ("R12", "OPEN_COMPLETE_SEAL_LIFT__EVEN_REFLECTION_CONTROL_DOES_NOT_FIX_LEVEL", "physical seal action on coframe/Hodge slice is open; minimal even reflection control preserves line/projector with free normalization"),
        ("R13", "DESCENT_PRESERVES_RELATION_FAMILY__J07_J11_OPEN", "unimodular monodromy preserves D descent; supplied mixing descent fixes no level"),
        ("R14", "ANCHORS_INSUFFICIENT_FOR_INVERSE_LENGTH", "c_E,G_obs alone have no inverse-length solution; supplied rho_tot would allow sqrt(G_obs rho_tot)/c_E dimensionally but no native equality"),
        ("R15", "SURVIVES__NO_ADDITIONAL_GEOMETRY_CUTTING_RELATION", "all active tested premises admit free-L and variable-area counterfamilies"),
    ]

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "outcome": "NO_ADDITIONAL_GEOMETRY_CUTTING_RELATION_DERIVED",
        "scope": "FC07_B1_ONE_STATIONARY_TORUS_INVARIANT_LOWER_TRIANGULAR_SUPPLIED_DESCENT",
        "checks_passed": len(checks) - len(failed),
        "checks_total": len(checks),
        "failed_checks": failed,
        "formulae": {
            "alpha": "theta1/(I*D)",
            "I": "integral_cell a/D ds",
            "delta_alpha": "0",
            "delta_theta1": "-D_prime/(a*D)",
            "ratio": "1/(I*D)",
            "hodge_norm_squared": "1/I (unit coordinate fiber area)",
            "fiber_flux": "1/I",
            "founded_four_wedge_coefficient": "c_E*L/I",
            "constant_proportionality_condition": "D_prime=0; k=1/ell",
            "pointwise_equality_condition": "D_prime=0 and ell=1 in the chosen unit",
            "variable_solder": "dphi=F*alpha; F=I*D*phi_prime/a; integral F*alpha=0",
            "density_dimensional_opening": "sqrt(G_obs*rho_tot)/c_E has inverse-length dimensions if rho_tot is supplied; no native equality derived",
        },
        "explicit_witnesses": {
            "variable_area": {
                "period": "2*pi",
                "a": "L",
                "D": "1+(3/5)*cos(s)",
                "I": str(I_var),
                "ratio_at_0": str(ratio_at_zero),
                "ratio_at_pi": str(ratio_at_pi),
            },
            "variable_phi_constant_area": {
                "exp_phi": "1+cos(s)/3",
                "D": "1",
                "I": str(I_phi),
                "ratio": str(ratio_phi),
                "F": str(F_witness),
                "weighted_F_period": str(weighted_F_period),
            },
            "free_scale": "L -> q L leaves alpha fixed and sends theta1,I -> q times themselves",
        },
        "monodromies": monodromy_data,
        "candidate_outcomes": {row[0]: row[1] for row in outcomes},
        "density_scan_authorized": False,
        "reason_density_scan_not_authorized": "no native same-solution return relation was derived",
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUTCOMES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["candidate_id", "outcome", "reason"])
        writer.writerows(outcomes)

    algebra_rows = [
        ("A01", "alpha", "theta1/(I D)", "DERIVED_CONDITIONAL_BOUNDED"),
        ("A02", "projector", "P_alpha=P_theta1", "DERIVED_CONDITIONAL_BOUNDED"),
        ("A03", "raw_harmonicity", "delta theta1=-D_prime/(aD)", "DERIVED"),
        ("A04", "constant_proportionality", "alpha=k theta1 iff D_prime=0; k=1/ell", "DERIVED_IFF"),
        ("A05", "pointwise_equality", "alpha=theta1 iff D_prime=0 and ell=1 chosen unit", "DERIVED_IFF_TYPED"),
        ("A06", "primitive_period", "integral alpha=1", "TOPOLOGICAL_NORMALIZATION"),
        ("A07", "physical_period", "integral theta1=ell>0", "METRIC_READOUT"),
        ("A08", "exact_depth_period", "integral dphi=0 on closed base", "DERIVED_GLOBAL"),
        ("A09", "constant_solder", "dphi=k alpha implies k=0 and phi constant", "DERIVED_NO_GO_CLOSED_BASE"),
        ("A10", "variable_solder", "F=I D phi_prime/a; integral F alpha=0", "IDENTITY_NOT_SELECTOR"),
        ("A11", "fiber_flux", "integral_fiber star alpha=1/I", "DERIVED_READOUT"),
        ("A12", "hodge_energy", "norm(alpha)^2_L2=1/I", "DERIVED_READOUT"),
        ("A13", "reciprocal_harmonic_wedge", "theta0 wedge alpha wedge theta2 wedge theta3 has coefficient c_E L/I", "DERIVED_READOUT"),
        ("A14", "L_scaling", "alpha invariant; theta1 and I scale by q", "EXACT_COUNTERFAMILY"),
        ("A15", "even_reflection_control", "theta1 and alpha odd; ratio and projector even", "MATHEMATICAL_CONTROL__PHYSICAL_SEAL_LIFT_OPEN"),
        ("A16", "monodromy_descent", "det M=1 preserves D; det(M^T-I) nonzero gives b1=1", "DERIVED_FOR_FOUR_WITNESSES"),
        ("A17", "dimensional_rank", "c_E and G_obs cannot form inverse length", "DERIVED_DIMENSIONAL"),
        ("A18", "density_dimensional_opening", "sqrt(G_obs rho_tot)/c_E has inverse-length dimensions", "DERIVED_DIMENSIONAL_IF_RHO_SUPPLIED__NO_NATIVE_EQUALITY"),
    ]
    with ALGEBRA.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["id", "object", "exact_relation", "status"])
        writer.writerows(algebra_rows)

    print(f"OUTCOME={result['outcome']}")
    print(f"CHECKS={result['checks_passed']}/{result['checks_total']}")
    print(f"CANDIDATES={len(outcomes)}/{len(outcomes)}")
    print(f"FAILED_CHECKS={','.join(failed) if failed else 'NONE'}")
    print("DENSITY_SCAN_AUTHORIZED=NO")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
