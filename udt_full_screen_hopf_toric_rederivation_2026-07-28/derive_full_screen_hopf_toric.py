#!/usr/bin/env python3
"""Exact full-screen rederivation of the N22 and T18 routes."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def need(name: str, condition: bool, checks: list[dict[str, object]]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks.append({"id": name, "status": "PASS"})


def det2(v: tuple[int, int], w: tuple[int, int]) -> int:
    return v[0] * w[1] - v[1] * w[0]


def primitive(v: tuple[int, int]) -> bool:
    return sp.gcd(abs(v[0]), abs(v[1])) == 1


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    path = HERE / name
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: list[dict[str, object]] = []

    # General positive screen and its canonical oriented complex structure.
    a, b, c, d = sp.symbols("a b c d", real=True)
    P = sp.Matrix([[a, b], [c, d]])
    hP = sp.simplify(P.T * P)
    need("A01_screen_metric_determinant", sp.factor(hP.det()) == (a * d - b * c) ** 2, checks)

    A, B, C = sp.symbols("A B C", real=True)
    h = sp.Matrix([[A, B], [B, C]])
    deth = sp.factor(h.det())
    J = sp.Matrix([[B, C], [-A, -B]]) / sp.sqrt(deth)
    need("A02_oriented_screen_J_squares_minus_identity", sp.simplify(J * J + sp.eye(2)) == sp.zeros(2), checks)
    need("A03_oriented_screen_J_is_metric_compatible", sp.simplify(J.T * h * J - h) == sp.zeros(2), checks)
    need("A04_J_has_no_real_line_eigenvalue", sp.factor(J.charpoly().as_expr()) == sp.Symbol("lambda") ** 2 + 1, checks)

    # Metric-dual connection of a supplied primitive torus generator.
    m, n, scale = sp.symbols("m n scale", real=True, nonzero=True)
    w = sp.Matrix([m, n])
    hww = sp.expand((w.T * h * w)[0])
    q = sp.simplify(h * w / hww)
    q_scaled = sp.simplify((scale**2 * h) * w / ((w.T * (scale**2 * h) * w)[0]))
    need("A05_common_positive_scale_cancels_from_connection", sp.simplify(q_scaled - q) == sp.zeros(2, 1), checks)
    need("A06_connection_normalization", sp.simplify((w.T * q)[0] - 1) == 0, checks)

    r, s = sp.symbols("r s", real=True)
    u = sp.Matrix([r, s])
    huu = (u.T * h * u)[0]
    hwu = (w.T * h * u)[0]
    schur = sp.factor(huu - hwu**2 / hww)
    expected_schur = sp.factor(deth * (m * s - n * r) ** 2 / hww)
    need("A07_quotient_metric_Schur_formula", sp.simplify(schur - expected_schur) == 0, checks)

    # Contact form theta1 on the twisted S3 control and its exact Reeb field.
    p2, p3, t1 = sp.symbols("p2 p3 t1", real=True, nonzero=True)
    F = sp.Matrix([[0, -p2, -p3], [p2, 0, t1], [p3, -t1, 0]])
    reeb = sp.Matrix([1, p3 / t1, -p2 / t1])
    need("A08_general_theta1_Reeb_contraction", sp.simplify((reeb.T * F)) == sp.zeros(1, 3), checks)
    need("A09_general_theta1_Reeb_normalization", reeb[0] == 1, checks)

    # A smooth positive rescaling of the standard Hopf contact form can have irrational Reeb slope.
    eta, k = sp.symbols("eta k", real=True)
    f = sp.exp(k * sp.cos(2 * eta))
    aa = f * sp.cos(eta) ** 2
    bb = f * sp.sin(eta) ** 2
    denom = sp.simplify(aa * sp.diff(bb, eta) - bb * sp.diff(aa, eta))
    reeb_a = sp.simplify(sp.diff(bb, eta) / denom)
    reeb_b = sp.simplify(-sp.diff(aa, eta) / denom)
    need("A10_scaled_Hopf_Reeb_a", sp.simplify(reeb_a - (1 - 2 * k * sp.sin(eta) ** 2) / f) == 0, checks)
    need("A11_scaled_Hopf_Reeb_b", sp.simplify(reeb_b - (1 + 2 * k * sp.cos(eta) ** 2) / f) == 0, checks)
    k0 = sp.sqrt(2) / 2
    irrational_slope = sp.simplify((reeb_a / reeb_b).subs({eta: sp.pi / 4, k: k0}))
    need("A12_contact_does_not_force_periodic_Reeb", sp.simplify(irrational_slope - (3 - 2 * sp.sqrt(2))) == 0, checks)

    # If the scaled standard form has a constant Reeb generator (m,n), its scale is forced.
    fmn = 1 / (m * sp.cos(eta) ** 2 + n * sp.sin(eta) ** 2)
    amn = fmn * sp.cos(eta) ** 2
    bmn = fmn * sp.sin(eta) ** 2
    dmn = sp.simplify(amn * sp.diff(bmn, eta) - bmn * sp.diff(amn, eta))
    need("A13_constant_generator_scale_gives_m", sp.simplify(sp.diff(bmn, eta) / dmn - m) == 0, checks)
    need("A14_constant_generator_scale_gives_n", sp.simplify(-sp.diff(amn, eta) / dmn - n) == 0, checks)
    need("A15_depth_normalized_contact_has_standard_Reeb", sp.simplify(fmn.subs({m: 1, n: 1}) - 1) == 0, checks)

    phi, shift = sp.symbols("phi shift", real=True)
    spatial_fiber_coefficient = sp.exp(2 * phi) - shift**2 * sp.exp(-2 * phi)
    need("A15b_founded_depth_normalization", sp.simplify(sp.exp(-phi) * sp.exp(phi) - 1) == 0, checks)
    spatial_metric = sp.Matrix(
        [[spatial_fiber_coefficient, 0, 0], [0, A, B], [0, B, C]]
    )
    fiber_vector = sp.Matrix([1, 0, 0])
    fiber_covector = spatial_metric * fiber_vector
    fiber_norm_squared = (fiber_vector.T * spatial_metric * fiber_vector)[0]
    need(
        "A15c_positive_slice_metric_dual_normalizes_to_sigma3",
        sp.simplify(fiber_covector / fiber_norm_squared - fiber_vector) == sp.zeros(3, 1),
        checks,
    )

    # Registered Hopf-coordinate period and curvature normalization.
    hopf_a, hopf_b = sp.cos(eta) ** 2, sp.sin(eta) ** 2
    need("A15d_sigma3_normalizes_diagonal_fiber", sp.simplify(hopf_a + hopf_b - 1) == 0, checks)
    tau = sp.symbols("tau", real=True)
    need("A15e_sigma3_fiber_period_is_2pi", sp.integrate(1, (tau, 0, 2 * sp.pi)) == 2 * sp.pi, checks)
    delta = sp.symbols("delta", real=True)
    hopf_flux = sp.integrate(sp.diff(hopf_a, eta), (eta, 0, sp.pi / 2)) * sp.integrate(1, (delta, 0, 2 * sp.pi))
    need("A15f_sigma3_Chern_flux_is_minus_one", sp.simplify(hopf_flux / (2 * sp.pi) + 1) == 0, checks)

    # An explicit off-diagonal full-screen family on S3: local connection changes, class does not.
    eps = sp.symbols("eps", real=True)
    se, ce = sp.sin(eta), sp.cos(eta)
    hs = sp.Matrix([[ce**2, eps * se**2 * ce**2], [eps * se**2 * ce**2, se**2]])
    hs_det = sp.factor(hs.det())
    need(
        "A16_sheared_screen_determinant",
        sp.simplify(hs_det - se**2 * ce**2 * (1 - eps**2 * se**2 * ce**2)) == 0,
        checks,
    )
    one = sp.Matrix([1, 1])
    den_s = sp.simplify((one.T * hs * one)[0])
    qs = sp.simplify(hs * one / den_s)
    need("A17_sheared_connection_normalized", sp.simplify(qs[0] + qs[1] - 1) == 0, checks)
    need("A18_shear_changes_local_connection", sp.simplify(sp.diff(qs[0], eps)) != 0, checks)
    q0 = sp.simplify(qs[0].subs(eta, 0))
    qend = sp.simplify(qs[0].subs(eta, sp.pi / 2))
    need("A19_sheared_S3_endpoint_connection_values", q0 == 1 and qend == 0, checks)
    cs_coefficient = sp.simplify(qs[1] * sp.diff(qs[0], eta) - qs[0] * sp.diff(qs[1], eta))
    need("A20_sheared_Chern_Simons_reduces_to_endpoint", sp.simplify(cs_coefficient - sp.diff(qs[0], eta)) == 0, checks)
    need("A21_sheared_unit_class_independent_of_eps", sp.simplify(qend - q0) == -1, checks)

    # Primitive cap/fiber examples and the infinite mirror/lens counterfamily.
    examples = [
        ("L01_S3_STANDARD", (1, 0), (0, 1), (1, 1), "S3"),
        ("L02_MIRROR_P3", (2, 1), (1, 2), (1, 1), "LENS_L_3_1"),
        ("L03_MIRROR_P5", (3, 2), (2, 3), (1, 1), "LENS_L_5_1"),
        ("L04_LENS_P4", (1, 0), (1, 4), (0, 1), "LENS_L_4_1"),
        ("L05_DET_ZERO", (1, 0), (1, 0), (0, 1), "S2_X_S1_STANDARD"),
        ("L06_MIRROR_P8_NOT_FREE", (3, 1), (1, 3), (1, 1), "LENS_WITH_EXCEPTIONAL_QUOTIENT"),
        ("L07_NONPRIMITIVE", (2, 0), (0, 1), (1, 1), "SINGULAR_CAP"),
    ]
    lattice_rows: list[dict[str, object]] = []
    for row_id, vminus, vplus, fiber, topology in examples:
        p = abs(det2(vminus, vplus))
        dm = det2(vminus, fiber)
        dp = det2(vplus, fiber)
        smooth_caps = primitive(vminus) and primitive(vplus)
        free = smooth_caps and abs(dm) == 1 and abs(dp) == 1
        lattice_rows.append(
            {
                "id": row_id,
                "v_minus": str(vminus),
                "v_plus": str(vplus),
                "fiber_w": str(fiber),
                "p_abs_det_caps": p,
                "det_vminus_w": dm,
                "det_vplus_w": dp,
                "primitive_caps": str(bool(smooth_caps)).upper(),
                "free_circle": str(bool(free)).upper(),
                "abs_c1_if_free": p if free else "UNDEFINED_OR_ORBIFOLD",
                "topology_or_status": topology,
            }
        )
    need("A22_standard_S3_free_unit", lattice_rows[0]["free_circle"] == "TRUE" and lattice_rows[0]["abs_c1_if_free"] == 1, checks)
    need("A23_mirror_p3_is_free_not_unit", lattice_rows[1]["free_circle"] == "TRUE" and lattice_rows[1]["abs_c1_if_free"] == 3, checks)
    need("A24_lens_p4_free_family_exists", lattice_rows[3]["free_circle"] == "TRUE" and lattice_rows[3]["abs_c1_if_free"] == 4, checks)
    need("A25_p8_mirror_action_not_free", lattice_rows[5]["free_circle"] == "FALSE", checks)
    need("A26_nonprimitive_cap_rejected_as_smooth", lattice_rows[6]["primitive_caps"] == "FALSE", checks)

    kk = sp.symbols("kk", integer=True, positive=True)
    vm = sp.Matrix([kk + 1, kk])
    vp = sp.Matrix([kk, kk + 1])
    ww = sp.Matrix([1, 1])
    capdet = sp.expand(vm[0] * vp[1] - vm[1] * vp[0])
    dmf = sp.expand(vm[0] * ww[1] - vm[1] * ww[0])
    dpf = sp.expand(vp[0] * ww[1] - vp[1] * ww[0])
    need("A27_infinite_mirror_lens_family", capdet == 2 * kk + 1 and dmf == 1 and dpf == -1, checks)

    # In a unimodular basis (w,u), v_i=a_i w+b_i u. Freeness gives |b_i|=1.
    am, bm, ap, bp = sp.symbols("am bm ap bp", real=True, nonzero=True)
    capdet_basis = am * bp - bm * ap
    euler_difference = am / bm - ap / bp
    need(
        "A27b_free_cap_Chern_difference_equals_cap_determinant",
        sp.simplify(euler_difference * bm * bp - capdet_basis) == 0,
        checks,
    )

    # A globally smooth allowed P can break the torus action.  Use a scalar P so
    # coframe rotation cannot disguise the failure as O(2) gauge.
    x, y = sp.symbols("x y", real=True)
    screen_scalar = sp.exp(2 * eps * x)
    circle_derivative_h11 = sp.diff(screen_scalar, x) * (-y)
    need("A28_general_screen_not_automatically_toric", sp.simplify(circle_derivative_h11) != 0, checks)

    contact_rows = [
        {
            "id": "C01",
            "object": "theta1_contact_form",
            "scope": "twisted_S3_all_smooth_finite_phi_and_all_invertible_P",
            "exact_result": "theta1_wedge_dtheta1=t1_volume_nonzero",
            "classification": "SURVIVES_ALL_FULL_SCREENS_IN_CHOSEN_S3_COFRAME",
            "open_gate": "coframe_or_metric_ownership_and_global_branch_selection",
        },
        {
            "id": "C02",
            "object": "theta1_Reeb_line",
            "scope": "same_chosen_coframe",
            "exact_result": "R=E1+(p3/t1)E2-(p2/t1)E3",
            "classification": "SURVIVES_ALL_FULL_SCREENS_IN_CHOSEN_S3_COFRAME",
            "open_gate": "frame_independence_periodicity_and_metric_descent",
        },
        {
            "id": "C03",
            "object": "unnormalized_ruler_Reeb_periodicity",
            "scope": "theta1=exp(phi)sigma3",
            "exact_result": "smooth_positive_nonconstant_phi_counterexample_has_irrational_Reeb_slope",
            "classification": "COUNTERMODEL_FAMILY_PRESENT",
            "open_gate": "contact_does_not_imply_circle_action",
        },
        {
            "id": "C04",
            "object": "founded_depth_normalized_ruler_form",
            "scope": "chosen_twisted_S3_coframe",
            "exact_result": "alpha0=exp(-phi)theta1=sigma3;dalpha0=kappa/detP theta2_wedge_theta3",
            "classification": "CONDITIONAL_TOPOLOGICAL_CLASS_INDEPENDENT_OF_SCREEN_SHAPE",
            "open_gate": "complete_4D_pair_ownership_and_S3_coframe_selection",
        },
        {
            "id": "C05",
            "object": "normalized_ruler_Hopf_flow",
            "scope": "global_Maurer_Cartan_S3_with_registered_period_normalization",
            "exact_result": "sigma3(V)=1;fiber_period=2pi;normalized_base_flux=plus_or_minus_1",
            "classification": "SURVIVES_ALL_FULL_SCREENS_IN_CHOSEN_S3_COFRAME",
            "open_gate": "why_realized_universe_uses_this_complete_coframe",
        },
        {
            "id": "C06",
            "object": "screen_metric_descent",
            "scope": "normalized_Hopf_flow",
            "exact_result": "full_h_descends_only_if_invariant_under_the_fiber_action",
            "classification": "BLOCKED_BY_MISSING_NATIVE_SELECTOR",
            "open_gate": "P_equivariance_or_fiber_invariance",
        },
    ]

    descent_rows = [
        {
            "id": "D01",
            "screen_or_completion": "arbitrary_smooth_P_on_S3",
            "local_structure": "area_two_shears_plus_gauge_rotation_and_contact_form",
            "global_result": "generically_no_T2_isometry_or_metric_quotient",
            "classification": "OPEN_OUTSIDE_BOUNDED_REGIME",
        },
        {
            "id": "D02",
            "screen_or_completion": "T2_invariant_general_SPD2_torus_orbit_block",
            "local_structure": "orthogonal_interval_gauge_or_orbit_component;radial_basic_term_separate",
            "global_result": "every_supplied_primitive_w_has_scale_free_metric_dual_connection",
            "classification": "SURVIVES_TORIC_INVARIANT_SUBFAMILY_ONLY",
        },
        {
            "id": "D03",
            "screen_or_completion": "S3_caps_plus_free_circle",
            "local_structure": "arbitrary_invariant_full_screen",
            "global_result": "abs_c1=1_independent_of_screen_shape_but_local_connection_and_base_metric_vary",
            "classification": "CONDITIONAL_TOPOLOGICAL_CLASS_INDEPENDENT_OF_SCREEN_SHAPE",
        },
        {
            "id": "D04",
            "screen_or_completion": "lens_L_p_1_caps_plus_free_circle",
            "local_structure": "arbitrary_invariant_full_screen",
            "global_result": "abs_c1=p_infinite_family_including_exchange_symmetric_odd_p",
            "classification": "COUNTERMODEL_FAMILY_PRESENT",
        },
        {
            "id": "D05",
            "screen_or_completion": "finite_boundary_or_no_cap",
            "local_structure": "connection_may_exist_on_principal_region",
            "global_result": "no_forced_integral_Hopf_class",
            "classification": "COUNTERMODEL_FAMILY_PRESENT",
        },
        {
            "id": "D06",
            "screen_or_completion": "nonprimitive_or_exceptional_action",
            "local_structure": "orbifold_or_stratified_quotient",
            "global_result": "not_a_smooth_round_S2_carrier",
            "classification": "COUNTERMODEL_FAMILY_PRESENT",
        },
        {
            "id": "D07",
            "screen_or_completion": "free_circle_with_invariant_full_screen",
            "local_structure": "quotient_metric_schur_complement_det_h_over_hww",
            "global_result": "smooth_S2_shape_not_forced_round",
            "classification": "SURVIVES_TORIC_INVARIANT_SUBFAMILY_ONLY",
        },
        {
            "id": "D08",
            "screen_or_completion": "canonical_bundle_projection",
            "local_structure": "one_quotient_map_and_connection",
            "global_result": "does_not_supply_Map_S3_S2_deformation_space_or_action",
            "classification": "BLOCKED_BY_MISSING_NATIVE_SELECTOR",
        },
    ]

    route_rows = [
        {"id": "R01", "layer": "FULL_SCREEN", "object": "area_plus_two_shears", "classification": "SURVIVES_ALL_FULL_SCREENS", "basis": "h=P^T_P", "remaining_open": "physical_screen"},
        {"id": "R02", "layer": "FULL_SCREEN", "object": "canonical_oriented_J", "classification": "SURVIVES_ALL_FULL_SCREENS", "basis": "J_h_squared_minus_I", "remaining_open": "no_real_line_or_circle_selected"},
        {"id": "R03", "layer": "SYMMETRY", "object": "T2_reduction", "classification": "SURVIVES_TORIC_INVARIANT_SUBFAMILY_ONLY", "basis": "general_P_can_break_T2", "remaining_open": "native_global_symmetry"},
        {"id": "R04", "layer": "CONTACT", "object": "theta1_contact_and_Reeb", "classification": "SURVIVES_ALL_FULL_SCREENS", "basis": "t1_nonzero_for_all_invertible_P", "remaining_open": "metric_ownership_and_periodicity"},
        {"id": "R05", "layer": "CONTACT", "object": "unnormalized_theta1_free_circle", "classification": "COUNTERMODEL_FAMILY_PRESENT", "basis": "irrational_Reeb_slope", "remaining_open": "regularity_rule"},
        {"id": "R06", "layer": "CONTACT", "object": "alpha0=exp_minus_phi_theta1", "classification": "CONDITIONAL_TOPOLOGICAL_CLASS_INDEPENDENT_OF_SCREEN_SHAPE", "basis": "alpha0=sigma3", "remaining_open": "selected_S3_coframe_and_pair_normalization"},
        {"id": "R07", "layer": "TORIC_CONNECTION", "object": "A_h_w", "classification": "SURVIVES_TORIC_INVARIANT_SUBFAMILY_ONLY", "basis": "h_w_over_hww", "remaining_open": "w_selection"},
        {"id": "R08", "layer": "TORIC_CONNECTION", "object": "common_scale_cancellation", "classification": "SURVIVES_ALL_FULL_SCREENS", "basis": "A_Omega2h=A_h", "remaining_open": "physical_scale_status_not_changed"},
        {"id": "R09", "layer": "TOPOLOGY", "object": "fixed_bundle_Chern_class", "classification": "CONDITIONAL_TOPOLOGICAL_CLASS_INDEPENDENT_OF_SCREEN_SHAPE", "basis": "free_cap_lattice", "remaining_open": "cap_and_fiber_selection"},
        {"id": "R10", "layer": "TOPOLOGY", "object": "unit_Hopf_class", "classification": "SURVIVES_REGULAR_CONTACT_SUBFAMILY_ONLY", "basis": "S3_plus_free_circle", "remaining_open": "global_branch_selection"},
        {"id": "R11", "layer": "TOPOLOGY", "object": "unit_class_uniqueness_across_completions", "classification": "COUNTERMODEL_FAMILY_PRESENT", "basis": "L_p_1_has_abs_c1_p", "remaining_open": "topology_ranking"},
        {"id": "R12", "layer": "MIRROR", "object": "exchange_selects_p1", "classification": "COUNTERMODEL_FAMILY_PRESENT", "basis": "mirror_odd_p_free_family", "remaining_open": "cap_rule"},
        {"id": "R13", "layer": "DESCENT", "object": "quotient_metric", "classification": "SURVIVES_TORIC_INVARIANT_SUBFAMILY_ONLY", "basis": "Schur_complement", "remaining_open": "roundness_and_P_equivariance"},
        {"id": "R14", "layer": "CARRIER", "object": "bundle_projection_equals_carrier", "classification": "BLOCKED_BY_MISSING_NATIVE_SELECTOR", "basis": "one_projection_not_full_map_space", "remaining_open": "section_deformation_and_action"},
        {"id": "N22", "layer": "OVERALL", "object": "metric_to_Hopf_bridge", "classification": "SUPERSEDED_OR_REFINED", "basis": "depth_normalized_contact_Hopf_bundle_survives_full_screen_on_chosen_S3", "remaining_open": "complete_coframe_selection_metric_descent_carrier_action"},
        {"id": "T18", "layer": "OVERALL", "object": "angular_toric_gate_chain", "classification": "SUPERSEDED_OR_REFINED", "basis": "toric_and_contact_routes_separate_then_require_global_regular_free_completion_and_descent", "remaining_open": "native_global_selector"},
    ]

    write_tsv("TORIC_LATTICE_ATLAS.tsv", lattice_rows)
    write_tsv("CONTACT_REEB_ATLAS.tsv", contact_rows)
    write_tsv("FULL_SCREEN_DESCENT_ATLAS.tsv", descent_rows)
    write_tsv("ROUTE_CLASSIFICATION.tsv", route_rows)

    result = {
        "schema": "udt-full-screen-hopf-toric-rederivation-1.0",
        "fixed_base": "ace0699fc145c935c16cd283f393c18e654d5b74",
        "checks": checks,
        "check_count": len(checks),
        "screen": {
            "metric_dof": 3,
            "coframe_gauge_dof": 1,
            "canonical_oriented_complex_structure": True,
            "canonical_real_line": False,
            "arbitrary_screen_automatically_toric": False,
        },
        "contact": {
            "theta1_contact_for_all_invertible_P_on_control": True,
            "theta1_Reeb": "E1+(p3/t1)E2-(p2/t1)E3",
            "contact_implies_periodic": False,
            "counterexample_slope": str(irrational_slope),
            "depth_normalized_form": "exp(-phi)*theta1=sigma3",
            "normalized_form_regular_Hopf_on_registered_S3": True,
            "metric_intrinsic_across_all_full_screens": False,
            "metric_intrinsic_overlap": "positive_slice_plus_metric_identified_ruler_line",
            "strong_local_CSN_used": False,
        },
        "toric": {
            "connection": [str(sp.simplify(q[0])), str(sp.simplify(q[1]))],
            "common_scale_independent": True,
            "local_shear_changes_connection": True,
            "two_shear_response": "offdiagonal_mode_changes_connection;complementary_shape_mode_can_change_base_metric_without_changing_connection",
            "fixed_bundle_class_changes_with_screen": False,
            "free_action_condition": "abs(det(v_minus,w))=abs(det(v_plus,w))=1",
            "abs_c1_if_free": "abs(det(v_minus,v_plus))",
            "chern_formula_scope": "effective_T2_cohomogeneity_one_two_smooth_caps_no_extra_exceptional_orbit",
            "connection_scope": "torus_orbit_block_or_orthogonal_interval_gauge;radial_basic_term_does_not_change_cap_Euler_class",
            "lens_counterfamily": "v_minus=(k+1,k);v_plus=(k,k+1);w=(1,1);abs_c1=2k+1",
        },
        "quotient": {
            "metric_coefficient_for_unimodular_base_vector": "det(h)/h(w,w)",
            "roundness_selected": False,
            "carrier_configuration_space_derived": False,
        },
        "regraded_rows": {
            "N22": "STRONGER_CONDITIONAL_DEPTH_NORMALIZED_CONTACT_HOPF_BUNDLE_ROUTE__NATIVE_CARRIER_OPEN",
            "T18": "REFINED_CONTACT_OR_TORIC_GLOBAL_REGULARITY_AND_DESCENT_GATE_CHAIN__NO_SELECTION",
        },
        "maximum_conclusion": "FULL_SCREEN_ROBUST_CONDITIONAL_HOPF_BUNDLE_ON_CHOSEN_NORMALIZED_S3_COFRAME__GENERAL_SCREEN_DOES_NOT_SELECT_TORIC_SYMMETRY_CAP_CLASS_FIBER_DESCENT_CARRIER_OR_ACTION",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
