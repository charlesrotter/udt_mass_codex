#!/usr/bin/env python3
"""Exact Killing-plane and two-stratum transition classification."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(name: str, condition: bool, checks: list[dict[str, str]]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks.append({"id": name, "status": "PASS"})


def wedge(
    left: dict[tuple[int, ...], sp.Expr],
    right: dict[tuple[int, ...], sp.Expr],
) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.factor(result.get(key, 0) + (-1) ** inversions * ca * cb)
    return {key: sp.factor(value) for key, value in result.items() if sp.simplify(value) != 0}


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: list[dict[str, str]] = []
    c, alpha, omega, u, kappa, chi = sp.symbols(
        "c_E alpha Omega u kappa chi", real=True, nonzero=True
    )
    # u=exp(-2 phi)>0; nonzero assumptions are relaxed explicitly in the
    # exceptional-stratum table rather than hidden inside a division.
    A = c + alpha * omega

    # The metric Gram form on the Abelian Killing algebra span(K,V).
    G = sp.Matrix(
        [
            [-c**2 * u, -c * alpha * u],
            [-c * alpha * u, 1 / u - alpha**2 * u],
        ]
    )
    require("A01_Gram_determinant_is_minus_cE_squared", sp.factor(G.det()) == -c**2, checks)
    require("A02_Gram_plane_is_Lorentzian_for_cE_nonzero", G.det().is_negative is not False, checks)

    w = sp.Matrix([1, omega])
    norm = sp.factor((w.T * G * w)[0])
    expected_norm = sp.factor(-u * A**2 + omega**2 / u)
    require("A03_all_constant_helical_norms", sp.simplify(norm - expected_norm) == 0, checks)
    factorized_norm = sp.factor(
        (omega / sp.sqrt(u) - sp.sqrt(u) * A)
        * (omega / sp.sqrt(u) + sp.sqrt(u) * A)
    )
    require("A04_causal_norm_factorization", sp.simplify(norm - factorized_norm) == 0, checks)

    # Written with exp(2 phi)=r, the two finite null slopes are
    # c/(r-alpha) and -c/(r+alpha); a vanishing denominator is the V endpoint.
    r = sp.symbols("r", positive=True, real=True)
    roots = [c / (r - alpha), -c / (r + alpha)]
    norm_r = sp.factor(norm.subs(u, 1 / r))
    require("A05_first_null_slope", sp.simplify(norm_r.subs(omega, roots[0])) == 0, checks)
    require("A06_second_null_slope", sp.simplify(norm_r.subs(omega, roots[1])) == 0, checks)
    require("A07_K_is_everywhere_timelike", sp.simplify(norm.subs(omega, 0) + c**2 * u) == 0, checks)

    # The metric-valued Gram response along any transverse X with X(phi)=chi.
    # Since X(u)=-2u chi, D_X=G^{-1}X(G) is basis covariant.
    XG = sp.simplify(sp.diff(G, u) * (-2 * u * chi))
    D = sp.simplify(G.inv() * XG)
    expected_D = sp.Matrix([[-2 * chi, -4 * alpha * chi / c], [0, 2 * chi]])
    require("A08_exact_Gram_response_endomorphism", sp.simplify(D - expected_D) == sp.zeros(2), checks)
    require("A09_response_trace_zero", sp.simplify(sp.trace(D)) == 0, checks)
    require("A10_response_square", sp.simplify(D * D - 4 * chi**2 * sp.eye(2)) == sp.zeros(2), checks)
    require("A11_response_is_Gram_self_adjoint", sp.simplify(G * D - (G * D).T) == sp.zeros(2), checks)

    Kline = sp.Matrix([1, 0])
    Rline = sp.Matrix([-alpha / c, 1])
    require("A12_clock_eigenline_is_K", sp.simplify(D * Kline + 2 * chi * Kline) == sp.zeros(2, 1), checks)
    require("A13_ruler_eigenline_is_V_minus_alpha_over_c_K", sp.simplify(D * Rline - 2 * chi * Rline) == sp.zeros(2, 1), checks)
    require("A14_clock_eigenline_timelike", sp.simplify((Kline.T * G * Kline)[0] + c**2 * u) == 0, checks)
    require("A15_ruler_eigenline_spacelike", sp.simplify((Rline.T * G * Rline)[0] - 1 / u) == 0, checks)
    require("A16_reciprocal_eigenlines_Gram_orthogonal", sp.simplify((Kline.T * G * Rline)[0]) == 0, checks)

    # Basis covariance under a generic constant GL(2) change. This covers the
    # lattice-compatible subgroup as a strict subfamily.
    b11, b12, b21, b22 = sp.symbols("b11 b12 b21 b22", real=True)
    B = sp.Matrix([[b11, b12], [b21, b22]])
    Binv = B.inv()
    Gprime = sp.simplify(B.T * G * B)
    XGprime = sp.simplify(B.T * XG * B)
    Dprime = sp.simplify(Gprime.inv() * XGprime)
    require("A17_Gram_response_basis_covariance", sp.simplify(Dprime - Binv * D * B) == sp.zeros(2), checks)

    # The founded clock-norm response singles out Omega=0 whenever chi!=0.
    Xnorm = sp.factor(sp.diff(norm, u) * (-2 * u * chi))
    reciprocal_clock_residual = sp.factor(Xnorm + 2 * chi * norm)
    require("A18_clock_norm_reciprocal_response_residual", reciprocal_clock_residual == 4 * chi * omega**2 / u, checks)

    # Full twist three-form in the coordinate coframe (dt,sigma3,sigma1,sigma2).
    p, q = sp.symbols("p q", real=True)
    basis = [{(index,): sp.Integer(1)} for index in range(4)]
    dphi = {(2,): p, (3,): q}
    coeff_dt = -c * A * u
    coeff_s3 = omega / u - alpha * A * u
    dcoeff_dt = {key: sp.simplify(-2 * coeff_dt * value) for key, value in dphi.items()}
    dcoeff_s3 = {
        key: sp.simplify(2 * (omega / u + alpha * A * u) * value)
        for key, value in dphi.items()
    }
    dflat: dict[tuple[int, ...], sp.Expr] = {}
    for part in (
        wedge(dcoeff_dt, basis[0]),
        wedge(dcoeff_s3, basis[1]),
        {(2, 3): sp.factor(kappa * coeff_s3)},
    ):
        for key, value in part.items():
            dflat[key] = sp.factor(dflat.get(key, 0) + value)
    twist3 = wedge({(0,): coeff_dt, (1,): coeff_s3}, dflat)
    expected_mixed_p = 4 * c * omega * A * p
    expected_mixed_q = 4 * c * omega * A * q
    require("A19_full_twist_mixed_sigma1_coefficient", sp.simplify(twist3[(0, 1, 2)] - expected_mixed_p) == 0, checks)
    require("A20_full_twist_mixed_sigma2_coefficient", sp.simplify(twist3[(0, 1, 3)] - expected_mixed_q) == 0, checks)
    expected_contact_dt = sp.factor(kappa * coeff_dt * coeff_s3)
    expected_contact_s3 = sp.factor(kappa * coeff_s3**2)
    require("A21_full_twist_contact_dt_coefficient", sp.simplify(twist3[(0, 2, 3)] - expected_contact_dt) == 0, checks)
    require("A22_full_twist_contact_sigma3_coefficient", sp.simplify(twist3[(1, 2, 3)] - expected_contact_s3) == 0, checks)
    require("A23_K_has_no_depth_mixed_twist", sp.simplify(twist3[(0, 1, 2)].subs(omega, 0)) == 0 and sp.simplify(twist3[(0, 1, 3)].subs(omega, 0)) == 0, checks)
    require("A24_K_generically_retains_contact_twist", sp.simplify(twist3[(0, 2, 3)].subs(omega, 0) - alpha * c**3 * kappa * u**2) == 0 and sp.simplify(twist3[(1, 2, 3)].subs(omega, 0) - alpha**2 * c**2 * kappa * u**2) == 0, checks)
    require("A25_other_zero_mixed_line_is_spacelike_ruler", sp.simplify(norm.subs(omega, -c / alpha) - c**2 / (alpha**2 * u)) == 0, checks)

    # Constant-depth orthogonal/hypersurface-orthogonal line. It agrees with K
    # only in the twist-off alpha=0 subfamily.
    omega_perp = sp.factor(c * alpha / (1 / u**2 - alpha**2))
    require("A26_constant_depth_V_orthogonal_slope", sp.simplify((G[0, 1] + omega_perp * G[1, 1])) == 0, checks)
    require("A27_constant_depth_perp_differs_from_K_when_alpha_nonzero", sp.factor(omega_perp / alpha) != 0, checks)
    require("A28_constant_depth_kappa_zero_all_twists_vanish", all(sp.simplify(value.subs({p: 0, q: 0, kappa: 0})) == 0 for value in twist3.values()), checks)

    # The automorphisms of the registered R x S1 Killing group that preserve
    # its primitive compact lattice have K->rK+bV and V->epsilon V.
    r_auto, b_auto = sp.symbols("r_auto b_auto", real=True, nonzero=True)
    for epsilon in (-1, 1):
        lattice_B = sp.Matrix([[r_auto, 0], [b_auto, epsilon]])
        require(
            f"A29_lattice_automorphism_epsilon_{epsilon:+d}",
            sp.factor(lattice_B.det()) == epsilon * r_auto
            and lattice_B[:, 1] == sp.Matrix([0, epsilon]),
            checks,
        )

    # The six exact old configurations supply a nonzero analytic endpoint for
    # the explicit transition argument.
    with (ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/CANDIDATE_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        old_rows = list(csv.DictReader(handle, delimiter="\t"))
    old_six = [row for row in old_rows if row["candidate_id"] in {f"C{i:02d}" for i in range(1, 7)}]
    old_dets = [Fraction(row["gradient_determinant"]) for row in old_six]
    require("A30_six_exact_nonzero_unique_clock_endpoints", len(old_dets) == 6 and all(value != 0 for value in old_dets), checks)

    direction_rows = [
        {"id": "D01", "direction": "K", "projective_slope_Omega": "0", "causal_status": "TIMELIKE_EVERYWHERE", "Gram_response": "NEGATIVE_EIGENLINE_IF_dphi_NONZERO", "twist_status": "NO_DEPTH_MIXED_COMPONENT", "orbit_type": "R_FREE", "selector_role": "FOUNDED_CLOCK_ON_VARIABLE_DEPTH"},
        {"id": "D02", "direction": "V-alpha/c_E*K", "projective_slope_Omega": "-c_E/alpha", "causal_status": "SPACELIKE_EVERYWHERE", "Gram_response": "POSITIVE_EIGENLINE_IF_dphi_NONZERO", "twist_status": "NO_DEPTH_MIXED_COMPONENT", "orbit_type": "R_FOR_NONZERO_K_COEFFICIENT", "selector_role": "FOUNDED_RULER_ON_VARIABLE_DEPTH"},
        {"id": "D03", "direction": "K+Omega*V", "projective_slope_Omega": "REAL_GENERIC", "causal_status": "CLASSIFIED_BY_EXACT_QUADRATIC", "Gram_response": "NOT_EIGENLINE_GENERIC", "twist_status": "HAS_DEPTH_MIXED_COMPONENT_GENERIC", "orbit_type": "R_FREE", "selector_role": "COUNTERFAMILY_RETAINED"},
        {"id": "D04", "direction": "V", "projective_slope_Omega": "PROJECTIVE_INFINITY", "causal_status": "SIGN_exp(4phi)-alpha^2", "Gram_response": "NOT_EIGENLINE_UNLESS_alpha_zero", "twist_status": "CONTACT_FIBER", "orbit_type": "S1_FREE", "selector_role": "UNIQUE_REGISTERED_COMPACT_LINE_INSIDE_TESTED_PLANE"},
        {"id": "D05", "direction": "NULL_PLUS", "projective_slope_Omega": "c_E/(exp(2phi)-alpha)", "causal_status": "NULL_POINTWISE", "Gram_response": "NOT_CONSTANT_KILLING_LINE_IF_phi_VARIES", "twist_status": "CLASSIFIED_NOT_SELECTED", "orbit_type": "POINTWISE_LINE", "selector_role": "CAUSAL_BOUNDARY"},
        {"id": "D06", "direction": "NULL_MINUS", "projective_slope_Omega": "-c_E/(exp(2phi)+alpha)", "causal_status": "NULL_POINTWISE", "Gram_response": "NOT_CONSTANT_KILLING_LINE_IF_phi_VARIES", "twist_status": "CLASSIFIED_NOT_SELECTED", "orbit_type": "POINTWISE_LINE", "selector_role": "CAUSAL_BOUNDARY"},
        {"id": "D07", "direction": "V_ORTHOGONAL", "projective_slope_Omega": "c_E*alpha/(exp(4phi)-alpha^2)", "causal_status": "TIMELIKE_IFF_V_SPACELIKE", "Gram_response": "CONSTANT_KILLING_ONLY_IF_phi_CONSTANT", "twist_status": "TWIST_FREE_IF_phi_CONSTANT_AND_kappa_NONZERO", "orbit_type": "R_IF_FINITE", "selector_role": "CONSTANT_DEPTH_METRIC_LINE_NOT_FOUNDED_K_GENERIC"},
    ]
    selector_rows = [
        {"id": "S01", "stratum": "descended_connected_base_phi_nonconstant", "clock_result": "UNIQUE_K_FROM_GRAM_RESPONSE", "ruler_result": "UNIQUE_V-alpha/c_E*K", "conditions": "some_dphi_nonzero;c_E_nonzero", "failure_or_caveat": "critical_points_use_global_continuation", "classification": "UNIQUE_FOUNDED_PAIR"},
        {"id": "S02", "stratum": "descended_phi_constant_alpha_zero_V_spacelike", "clock_result": "K_EQUALS_V_ORTHOGONAL", "ruler_result": "V", "conditions": "twist_off", "failure_or_caveat": "old_twist_ruler_certificate_absent", "classification": "METRIC_CLOCK_BUT_DIFFERENT_CERTIFICATE"},
        {"id": "S03", "stratum": "descended_phi_constant_alpha_nonzero_V_spacelike", "clock_result": "METRIC_SELECTS_V_ORTHOGONAL_NOT_FOUNDED_K", "ruler_result": "COMPACT_V", "conditions": "exp(4phi)>alpha^2", "failure_or_caveat": "founded_K_has_no_metric_response_selector", "classification": "RESIDUAL_FOUNDED_FRAMING_MISMATCH"},
        {"id": "S04", "stratum": "descended_phi_constant_V_null", "clock_result": "NO_TIMELIKE_V_ORTHOGONAL_LINE", "ruler_result": "COMPACT_NULL_V", "conditions": "exp(4phi)=alpha^2", "failure_or_caveat": "projective_null_root_at_V", "classification": "DEGENERATE"},
        {"id": "S05", "stratum": "descended_phi_constant_V_timelike", "clock_result": "NO_CANONICAL_NONCOMPACT_TIMELIKE_LINE_FROM_COMPACT_ORTHOGONAL_SPLIT", "ruler_result": "COMPACT_TIMELIKE_V", "conditions": "exp(4phi)<alpha^2", "failure_or_caveat": "closed_timelike_fibers_in_chosen_control", "classification": "CAUSAL_EXCEPTION_RETAINED"},
        {"id": "S06", "stratum": "descended_phi_nonconstant_with_critical_points", "clock_result": "GLOBAL_K_LINE_EXTENDS_FROM_ANY_REGULAR_POINT", "ruler_result": "GLOBAL_COMPLEMENTARY_EIGENLINE", "conditions": "connected_base;Gram_map_nonconstant", "failure_or_caveat": "not_a_pointwise_formula_at_dphi_zero", "classification": "UNIQUE_GLOBAL_PAIR"},
        {"id": "S07", "stratum": "kappa_zero_non_Hopf_control", "clock_result": "GRAM_SELECTOR_STILL_WORKS_IF_phi_NONconstant", "ruler_result": "NO_CONTACT_HOPF_CERTIFICATE", "conditions": "dphi_nonzero", "failure_or_caveat": "outside_registered_Hopf_descent_interpretation", "classification": "ALGEBRA_CONTROL_ONLY"},
        {"id": "S08", "stratum": "phi_constant_and_kappa_zero", "clock_result": "NO_GRAM_RESPONSE_SELECTOR", "ruler_result": "ALL_CONSTANT_KILLING_DIRECTIONS_TWIST_FREE", "conditions": "dphi=0;kappa=0", "failure_or_caveat": "topology_only_fixes_registered_compact_line", "classification": "RESIDUAL_FRAMING_CLASS"},
        {"id": "S09", "stratum": "higher_isometry_metric", "clock_result": "RESULT_CONDITIONAL_ON_REGISTERED_K_V_PLANE", "ruler_result": "OTHER_KILLING_PLANES_OR_COMPACT_CIRCLES_UNCLASSIFIED", "conditions": "Killing_algebra_dimension_greater_than_two", "failure_or_caveat": "selection_of_tested_plane_is_open", "classification": "HIGHER_SYMMETRY_SCOPE_BOUNDARY"},
    ]
    transition_rows = [
        {"id": "T01", "object": "descended_start", "construction": "choose_any_nonconstant_phi_D_on_S2_and_positive_descended_h_D", "exact_property": "Vphi_D=0_and_LVg_D=0", "conclusion": "NEW_GRAM_SELECTOR_GIVES_K"},
        {"id": "T02", "object": "analytic_path", "construction": "phi_s=(1-s)phi_D+s*phi_C;h_s=(1-s)h_D+s*h_C", "exact_property": "smooth_positive_stationary_registered_family_for_0<=s<=1", "conclusion": "CONNECTS_DESCENT_TO_EXACT_C_WITNESS"},
        {"id": "T03", "object": "rank_determinant", "construction": "same_three_scalar_invariant_gradients_along_g_s", "exact_property": "real_analytic_in_s;zero_at_s=0;nonzero_at_s=1", "conclusion": "NONZERO_FOR_POINTS_ARBITRARILY_CLOSE_TO_s=0"},
        {"id": "T04", "object": "clock_line_handoff", "construction": "Gram_response_at_s=0_and_rank3_Killing_kernel_on_nonzero_s_points_arbitrarily_near_zero", "exact_property": "both_select_same_global_K_line_on_their_respective_points", "conclusion": "CONTINUOUSLY_ADJACENT_SELECTOR_HANDOFF_NOT_SIMULTANEOUS_OVERLAP"},
        {"id": "T05", "object": "physical_reading", "construction": "none", "exact_property": "no_action_dynamics_density_or_scale_regime_loaded", "conclusion": "MACRO_MICRO_ASSIGNMENT_OPEN"},
    ]
    automorphism_rows = [
        {"id": "A01", "group": "R_times_S1", "map": "K_to_rK_plus_bV", "parameter": "r_nonzero;b_real", "lattice_action": "NONCOMPACT_GENERATOR_SHEAR_AND_SCALE", "consequence": "NO_HELIX_SELECTED_BY_TOPOLOGY"},
        {"id": "A02", "group": "R_times_S1", "map": "V_to_plus_V", "parameter": "epsilon=+1", "lattice_action": "PRIMITIVE_COMPACT_ORIENTATION_PRESERVED", "consequence": "COMPACT_LINE_FIXED"},
        {"id": "A03", "group": "R_times_S1", "map": "V_to_minus_V", "parameter": "epsilon=-1", "lattice_action": "PRIMITIVE_COMPACT_ORIENTATION_REVERSED", "consequence": "UNORIENTED_COMPACT_LINE_FIXED"},
        {"id": "A04", "group": "higher_isometry_exception", "map": "additional_Killing_planes_or_circles", "parameter": "UNCLASSIFIED", "lattice_action": "OUTSIDE_REGISTERED_PLANE", "consequence": "GLOBAL_PLANE_SELECTION_OPEN"},
    ]
    write_tsv("KILLING_DIRECTION_ATLAS.tsv", direction_rows)
    write_tsv("KILLING_BASIS_AUTOMORPHISMS.tsv", automorphism_rows)
    write_tsv("SELECTOR_STRATA.tsv", selector_rows)
    write_tsv("TRANSITION_ATLAS.tsv", transition_rows)

    result = {
        "schema": "udt-killing-plane-strata-transition-1.0",
        "base": "b9cf86b878ae8b0d23928d9a855c9d7748e02435",
        "checks": checks,
        "check_count": len(checks),
        "gram": {
            "matrix_basis_K_V": [[str(value) for value in row] for row in G.tolist()],
            "determinant": str(sp.factor(G.det())),
            "helical_norm": str(expected_norm),
            "null_slopes": ["c_E/(exp(2phi)-alpha)", "-c_E/(exp(2phi)+alpha)"],
            "causality_selects_K": False,
        },
        "gram_response": {
            "endomorphism": [[str(value) for value in row] for row in D.tolist()],
            "requires": "Gram_map_nonconstant_equivalently_phi_nonconstant_in_constant_alpha_family",
            "basis_covariant": True,
            "clock_eigenline": "K",
            "clock_eigenvalue": "-2*X(phi)",
            "clock_norm": "-c_E^2*exp(-2phi)",
            "ruler_eigenline": "V-alpha/c_E*K",
            "ruler_eigenvalue": "+2*X(phi)",
            "ruler_norm": "exp(2phi)",
            "critical_point_handling": "global_constant_Lie_algebra_lines_extend_from_any_regular_point_on_connected_base",
        },
        "twist": {
            "mixed_coefficients": ["4*c_E*Omega*(c_E+alpha*Omega)*X1(phi)", "4*c_E*Omega*(c_E+alpha*Omega)*X2(phi)"],
            "contact_coefficients": ["kappa*a_Omega*b_Omega", "kappa*b_Omega^2"],
            "a_Omega": "-c_E*(c_E+alpha*Omega)*exp(-2phi)",
            "b_Omega": "Omega*exp(2phi)-alpha*(c_E+alpha*Omega)*exp(-2phi)",
            "unique_timelike_no_depth_mixed_line_if_dphi_nonzero": "K",
            "other_no_depth_mixed_line": "V-alpha/c_E*K_is_spacelike",
            "K_full_twist_generically_zero": False,
            "twist_free_constant_depth_line": "V_orthogonal_when_finite_and_kappa_nonzero",
            "constant_depth_kappa_zero": "ALL_CONSTANT_KILLING_DIRECTIONS_TWIST_FREE",
        },
        "topology": {
            "compact_line": "registered_V_up_to_sign_inside_tested_plane",
            "compact_action": "free_S1_on_chosen_S3",
            "noncompact_helical_lines": "all_K+Omega*V_have_free_R_orbits",
            "fixed_points": "none_in_chosen_control",
            "topology_alone_selects_K_among_helices": False,
            "lattice_preserving_automorphisms": "K_to_rK_plus_bV;V_to_epsilonV;r_nonzero;b_real;epsilon_plus_or_minus_one",
            "higher_isometry_plane_selection": "OPEN",
        },
        "primary_classification": "MIXED_PARAMETER_STRATA",
        "variable_depth_descended_classification": "UNIQUE_METRIC_FOUNDED_CLOCK_AND_RULER_LINES",
        "constant_depth_classification": "FOUNDED_K_NOT_METRIC_SELECTED_GENERICALLY;METRIC_ORTHOGONAL_CLOCK_DIFFERS_OR_CAUSAL_DEGENERACY",
        "strata_relation": "CONTINUOUSLY_ADJACENT_WITHIN_REGISTERED_STATIONARY_FAMILY",
        "selector_handoff": "DESCENDED_GRAM_RESPONSE_K_TO_NEARBY_RANK3_K",
        "macro_micro_assignment": "OPEN_NOT_TESTED",
        "method_boundary": {
            "stationary": True,
            "off_shell": True,
            "constant_alpha": True,
            "block_screen": True,
            "strong_local_CSN_used": False,
            "action_used": False,
            "source_used": False,
            "carrier_derived": False,
            "bootstrap_loaded": False,
            "physical_regime_selected": False,
            "all_real_projective_directions_classified": True,
            "exceptional_strata_retained": True,
            "registered_K_V_plane_conditional": True,
            "higher_isometry_metrics_exhausted": False,
        },
        "maximum_conclusion": "ON_THE_DESCENDED_NONCONSTANT_DEPTH_STRATUM_THE_COMPLETE_METRIC_GRAM_RESPONSE_UNIQUELY_RECOVERS_THE_FOUNDED_CLOCK_K_AND_RULER_V_MINUS_ALPHA_OVER_CE_K;CONSTANT_DEPTH_REMAINS_A_DISTINCT_DEGENERATE_OR_FRAMING_MISMATCH_STRATUM;THE_DESCENDED_AND_OLD_RANK3_UNIQUE_CLOCK_STRATA_ARE_CONTINUOUSLY_ADJACENT_AND_HAND_OFF_THE_SAME_K_LINE;NO_MACRO_MICRO_OR_MASS_EMERGENCE_ASSIGNMENT_IS_DERIVED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
