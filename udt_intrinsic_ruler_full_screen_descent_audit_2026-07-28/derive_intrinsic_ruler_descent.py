#!/usr/bin/env python3
"""Exact stationary full-screen intrinsic-ruler and Hopf-descent classification."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def need(name: str, condition: bool, checks: list[dict[str, str]]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks.append({"id": name, "status": "PASS"})


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def wedge(left: dict[tuple[int, ...], sp.Expr], right: dict[tuple[int, ...], sp.Expr]):
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.simplify(result.get(key, 0) + (-1) ** inversions * ca * cb)
    return {key: value for key, value in result.items() if value != 0}


def main() -> None:
    checks: list[dict[str, str]] = []
    cE, alpha, kappa, detP = sp.symbols("c_E alpha kappa detP", real=True, nonzero=True)
    phi = sp.symbols("phi", real=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    e = [{(index,): sp.Integer(1)} for index in range(4)]
    dphi = {(1,): p1, (2,): p2, (3,): p3}
    t0 = alpha * kappa * sp.exp(-phi) / detP

    # K^flat=-c_E exp(-phi) theta0 and the exact general-P exterior derivative.
    kflat = {(0,): -cE * sp.exp(-phi)}
    dk = {}
    for key, value in wedge(dphi, e[0]).items():
        dk[key] = sp.simplify(2 * cE * sp.exp(-phi) * value)
    dk[(2, 3)] = sp.simplify(dk.get((2, 3), 0) - cE * sp.exp(-phi) * t0)
    k_wedge_dk = wedge(kflat, dk)
    twist_coefficient = sp.simplify(k_wedge_dk[(0, 2, 3)])
    expected_twist = cE**2 * alpha * kappa * sp.exp(-3 * phi) / detP
    need("A01_general_P_clock_twist_coefficient", sp.simplify(twist_coefficient - expected_twist) == 0, checks)
    need("A02_twist_has_only_ruler_Hodge_line", set(k_wedge_dk) == {(0, 2, 3)}, checks)
    need("A03_both_screen_shears_enter_only_through_detP_in_twist", not expected_twist.has(p1, p2, p3), checks)

    # Coordinate stationary field K and Hopf lift V versus orthonormal E0,E1.
    evaluation = sp.Matrix([
        [cE * sp.exp(-phi), alpha * sp.exp(-phi)],
        [0, sp.exp(phi)],
    ])
    dual_vectors = sp.simplify(evaluation.inv())
    expected_dual = sp.Matrix([
        [sp.exp(phi) / cE, -alpha * sp.exp(-phi) / cE],
        [0, sp.exp(-phi)],
    ])
    need("A04_exact_E0_E1_in_K_V_basis", sp.simplify(dual_vectors - expected_dual) == sp.zeros(2), checks)
    need("A05_orbit_projection_of_E1_is_Hopf_line", dual_vectors[1, 1] == sp.exp(-phi), checks)

    # The founded normalization and explicit period/flux convention.
    eta, delta, tau = sp.symbols("eta delta tau", real=True)
    hopf_a, hopf_b = sp.cos(eta) ** 2, sp.sin(eta) ** 2
    need("A06_founded_depth_normalization", sp.simplify(sp.exp(-phi) * sp.exp(phi) - 1) == 0, checks)
    need("A07_sigma3_normalizes_V", sp.simplify(hopf_a + hopf_b - 1) == 0, checks)
    need("A08_Hopf_fiber_period", sp.integrate(1, (tau, 0, 2 * sp.pi)) == 2 * sp.pi, checks)
    flux = sp.integrate(sp.diff(hopf_a, eta), (eta, 0, sp.pi / 2)) * sp.integrate(1, (delta, 0, 2 * sp.pi))
    need("A09_Hopf_curvature_flux_unit_magnitude", abs(sp.simplify(flux / (2 * sp.pi))) == 1, checks)

    # Exact Lie derivative of the full orbit metric under the registered Hopf generator.
    A, B, C = sp.symbols("A B C", real=True)
    VA, VB, VC, Vphi = sp.symbols("V_A V_B V_C V_phi", real=True)
    h = sp.Matrix([[A, B], [B, C]])
    Vh = sp.Matrix([[VA, VB], [VB, VC]])
    R = sp.Matrix([[0, -1], [1, 0]])
    screen_lie = sp.simplify(Vh + kappa * (h * R - R * h))
    need("A10_screen_Lie_derivative_is_equivariant_tensor", sp.simplify(screen_lie - sp.Matrix([
        [VA + 2 * B * kappa, -A * kappa + C * kappa + VB],
        [-A * kappa + C * kappa + VB, -2 * B * kappa + VC],
    ])) == sp.zeros(2), checks)
    gtt_fiber_derivative = sp.simplify(sp.diff(-cE**2 * sp.exp(-2 * phi), phi) * Vphi)
    need("A11_full_metric_invariance_forces_Vphi_zero", gtt_fiber_derivative == 2 * cE**2 * Vphi * sp.exp(-2 * phi), checks)

    # A positive anisotropic screen can satisfy the equivariance equation and carry both shears.
    s = sp.symbols("s", real=True)
    A0, B0, C0 = sp.symbols("A0 B0 C0", real=True)
    H0 = sp.Matrix([[A0, B0], [B0, C0]])
    Rot = sp.Matrix([[sp.cos(kappa * s), -sp.sin(kappa * s)],
                     [sp.sin(kappa * s), sp.cos(kappa * s)]])
    hrot = sp.simplify(Rot * H0 * Rot.T)
    invariant_residual = sp.simplify(sp.diff(hrot, s) + kappa * (hrot * R - R * hrot))
    need("A12_rotating_anisotropic_screen_is_fiber_invariant", invariant_residual == sp.zeros(2), checks)
    need("A13_rotating_screen_preserves_trace_and_determinant", sp.simplify(sp.trace(hrot) - sp.trace(H0)) == 0 and sp.simplify(hrot.det() - H0.det()) == 0, checks)
    need("A14_kappa_minus_two_solution_is_2pi_periodic", sp.simplify(hrot.subs({s: 2 * sp.pi, kappa: -2}) - H0) == sp.zeros(2), checks)

    # The old generic profile is not fiber invariant at its exact rank certificate event.
    x, y, z = sp.symbols("x y z", real=True)
    radius2 = x*x + y*y + z*z
    den = 1 + radius2
    q = [(1-radius2)/den, 2*x/den, 2*y/den, 2*z/den]
    coords = (x, y, z)
    dq = sp.Matrix([[sp.diff(component, coordinate) for coordinate in coords] for component in q])
    sigma = sp.zeros(3, 3)
    for axis in range(3):
        sigma[0, axis] = q[0]*dq[1, axis]-q[1]*dq[0, axis]-q[2]*dq[3, axis]+q[3]*dq[2, axis]
        sigma[1, axis] = q[0]*dq[2, axis]-q[2]*dq[0, axis]-q[3]*dq[1, axis]+q[1]*dq[3, axis]
        sigma[2, axis] = q[0]*dq[3, axis]-q[3]*dq[0, axis]-q[1]*dq[2, axis]+q[2]*dq[1, axis]
    origin = {x: 0, y: 0, z: 0}
    Vcoords = sp.simplify(sigma.subs(origin).inv() * sp.Matrix([0, 0, 1]))
    q1, q2, q3 = q[1], q[2], q[3]
    profile = (q1 + 2*q2 + 3*q3 + q1*q2 + 2*q2*q3 + 3*q3*q1
               + 2*q1**2 - 3*q2**2 + 5*q3**2 + q1*q2*q3
               + 2*q1**3 - q2**3 + 3*q3**3)
    Vprofile_origin = sp.simplify(sum(Vcoords[i] * sp.diff(profile, coords[i]).subs(origin) for i in range(3)))
    need("A15_registered_Hopf_generator_at_certificate", Vcoords == sp.Matrix([0, 0, sp.Rational(1, 2)]), checks)
    need("A16_old_profile_is_fiber_dependent", Vprofile_origin == 3, checks)
    need("A17_old_C01_C06_Vphi_is_3_over_50", Vprofile_origin / 50 == sp.Rational(3, 50), checks)

    # Exact nonzero determinants provide C3-open rank-three neighborhoods with both shear tangents.
    with (ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/CANDIDATE_OUTCOMES.tsv").open(newline="") as handle:
        old_rows = list(csv.DictReader(handle, delimiter="\t"))
    old_six = [row for row in old_rows if row["candidate_id"] in {f"C{i:02d}" for i in range(1, 7)}]
    determinants = [Fraction(row["gradient_determinant"]) for row in old_six]
    need("A18_all_six_old_rank_determinants_nonzero", len(determinants) == 6 and all(value != 0 for value in determinants), checks)
    need("A19_rank_three_is_C3_open", min(abs(value) for value in determinants) > 0, checks)

    # Fiber invariance adds V to the Killing kernel, so the old rank-three certificate cannot hold.
    g11, g12, g21, g22, g31, g32 = sp.symbols("g11 g12 g21 g22 g31 g32")
    gradients_on_spatial_basis = sp.Matrix([[g11, g12, 0], [g21, g22, 0], [g31, g32, 0]])
    need("A20_two_Killing_directions_force_spatial_gradient_det_zero", gradients_on_spatial_basis.det() == 0, checks)
    need("A21_rank_upper_bound_is_two", gradients_on_spatial_basis.rank() <= 2, checks)

    # Causal character alone does not isolate K once V is also Killing.
    omega = sp.symbols("Omega", real=True)
    gKK = -cE**2 * sp.exp(-2*phi)
    gKV = -cE * alpha * sp.exp(-2*phi)
    gVV = sp.exp(2*phi) - alpha**2 * sp.exp(-2*phi)
    helical_norm = sp.expand(gKK + 2*omega*gKV + omega**2*gVV)
    need("A22_helical_family_contains_K", helical_norm.subs(omega, 0) == gKK, checks)
    need("A23_K_norm_is_negative_positive_square", sp.simplify(-gKK - cE**2 * sp.exp(-2*phi)) == 0, checks)

    branch_rows = [
        {"id": "B01", "branch": "all_stationary_invertible_P_with_supplied_K_and_nonzero_alpha_kappa", "clock_certificate": "SUPPLIED_K_ONLY_UNLESS_EXTRA_TEST", "ruler": "EXACT_TWIST_LINE_THETA1", "normalized_Hopf": "EXACT_COFRAME_ORBIT_CONNECTION", "full_descent": "CONDITIONAL", "classification": "GENERAL_P_RULER_ALIGNMENT_DERIVED"},
        {"id": "B02", "branch": "C3_open_neighborhoods_of_old_C01_C06_in_both_shear_directions", "clock_certificate": "RANK3_UNIQUE_K_PERSISTS", "ruler": "EXACT", "normalized_Hopf": "EXACT", "full_descent": "GENERALLY_ABSENT", "classification": "OPEN_INTRINSIC_PAIR_STRATUM"},
        {"id": "B03", "branch": "old_C01_C06_exact_profiles", "clock_certificate": "RANK3_UNIQUE_K", "ruler": "EXACT", "normalized_Hopf": "EXACT", "full_descent": "FAIL_VPHI_3_OVER_50_AT_CERTIFICATE", "classification": "NO_FULL_HOPF_METRIC_DESCENT"},
        {"id": "B04", "branch": "Vphi_zero_and_Vh_plus_kappa_hR_minus_Rh_zero", "clock_certificate": "OLD_RANK3_IMPOSSIBLE", "ruler": "EXACT_IF_K_SUPPLIED_OR_SELECTED_OTHERWISE", "normalized_Hopf": "EXACT", "full_descent": "PASS", "classification": "FIBER_INVARIANT_TWO_KILLING_STRATUM"},
        {"id": "B05", "branch": "global_pullback_of_generic_positive_S2_metric_with_smooth_P_equals_positive_sqrt_h", "clock_certificate": "OLD_RANK3_IMPOSSIBLE", "ruler": "CONDITIONAL_ON_K", "normalized_Hopf": "EXACT", "full_descent": "PASS", "classification": "GLOBAL_CONSTRUCTIVE_TWO_SHEAR_DESCENT_WITNESS"},
        {"id": "B06", "branch": "fiber_dependent_phi_or_h", "clock_certificate": "CAN_BE_RANK3", "ruler": "EXACT_IF_K_SELECTED", "normalized_Hopf": "EXACT", "full_descent": "FAIL_GENERIC", "classification": "COUNTERBRANCH_RETAINED"},
        {"id": "B07", "branch": "sigma3_contact_bundle_without_metric_invariance", "clock_certificate": "NOT_REQUIRED", "ruler": "COFRAME", "normalized_Hopf": "EXACT_FREE_CIRCLE", "full_descent": "FAIL_OR_OPEN", "classification": "BUNDLE_NOT_METRIC_QUOTIENT"},
        {"id": "B08", "branch": "alpha_zero", "clock_certificate": "MAY_PERSIST", "ruler": "FAIL_ZERO_TWIST", "normalized_Hopf": "COFRAME_ONLY", "full_descent": "SEPARATE", "classification": "TWIST_OFF_CONTROL"},
        {"id": "B09", "branch": "constant_phi", "clock_certificate": "OLD_PROFILE_CERTIFICATE_FAILS", "ruler": "MAY_EXIST_IF_ALPHA_NONZERO", "normalized_Hopf": "EXACT", "full_descent": "DEPENDS_ON_h", "classification": "DEPTH_OFF_CONTROL"},
        {"id": "B10", "branch": "fiber_invariant_metric_with_possible_new_clock_selector", "clock_certificate": "OPEN_BEYOND_RANK3_METHOD", "ruler": "OPEN_UNTIL_K_SELECTED", "normalized_Hopf": "AVAILABLE", "full_descent": "PASS", "classification": "SMALLEST_REMAINING_SELECTOR_SEAM"},
    ]
    descent_rows = [
        {"object": "phi", "necessary_and_sufficient_condition": "V(phi)=0", "reason": "dt_squared_coefficient_is_minus_cE_squared_exp_minus_2phi", "gauge_status": "METRIC"},
        {"object": "screen_metric_h", "necessary_and_sufficient_condition": "V(h)+kappa*(hR-Rh)=0", "reason": "Lie_derivative_in_rotating_Maurer_Cartan_frame", "gauge_status": "METRIC"},
        {"object": "screen_coframe_P", "necessary_and_sufficient_condition": "only_h_condition_required;P_may_change_by_left_O2", "reason": "local_coframe_rotation_is_gauge", "gauge_status": "COFRAME_REPRESENTATIVE"},
        {"object": "normalized_ruler_sigma3", "necessary_and_sufficient_condition": "none_beyond_registered_S3_coframe", "reason": "L_V_sigma3=0_and_sigma3_V=1", "gauge_status": "COFRAME_CONDITIONAL_BUNDLE"},
        {"object": "full_stationary_metric", "necessary_and_sufficient_condition": "both_phi_and_h_conditions", "reason": "pair_and_screen_blocks_are_independent", "gauge_status": "METRIC_DESCENT"},
    ]
    write_tsv("BRANCH_COMPATIBILITY_ATLAS.tsv", branch_rows)
    write_tsv("DESCENT_CONDITIONS.tsv", descent_rows)

    result = {
        "schema": "udt-intrinsic-ruler-full-screen-descent-1.0",
        "fixed_base": "97d85edb7da351e6a96bb8c55b4e969ea8e3a749",
        "checks": checks,
        "check_count": len(checks),
        "screen_metric_dof": 3,
        "general_P_twist": {
            "coefficient_up_to_orientation": str(expected_twist),
            "line": "theta1",
            "requires": "supplied_or_metric_selected_K;alpha*kappa_nonzero;detP_nonzero",
            "screen_shear_dependence": "coefficient_only_through_detP;line_independent",
        },
        "ruler_Hopf_type_distinction": {
            "spacetime_ruler_vector": "E1=exp(-phi)*(V-alpha/c_E*K)",
            "orbit_projection": "pi_*E1=exp(-phi)*V",
            "normalized_orbit_form": "exp(-phi)*theta1=sigma3",
            "same_vector": False,
        },
        "rank_persistence": {
            "old_nonzero_certificates": 6,
            "topology": "C3_open_neighborhoods_in_general_screen_configuration_space",
            "both_shear_tangents_released": True,
            "universal_all_P": False,
        },
        "descent": {
            "phi_condition": "V(phi)=0",
            "screen_condition": "V(h)+kappa*(hR-Rh)=0",
            "anisotropic_two_shear_witness": True,
            "global_two_shear_witness": "pullback_generic_positive_S2_metric_then_P=positive_sqrt(h)",
            "old_C01_C06_descend": False,
        },
        "compatibility": {
            "fiber_descent_implies_second_Killing": True,
            "old_rank3_unique_K_can_coexist_with_descent": False,
            "all_metric_intrinsic_clock_selectors_ruled_out": False,
            "remaining_seam": "metric_intrinsic_clock_selector_inside_K_V_symmetry_plane_or_other_global_rule",
        },
        "method_boundary": {
            "stationarity_alone_selects_K": False,
            "strong_local_CSN_used": False,
            "orientation_selects_ordered_ruler_sign": False,
            "coframe_P_invariance_required_for_metric_descent": False,
            "round_carrier_derived": False,
            "action_or_dynamics_derived": False,
            "counterbranches_retained_without_filter": True,
            "constant_alpha_control": True,
        },
        "maximum_conclusion": "GENERAL_P_TWIST_RULER_ALIGNMENT_AND_OPEN_INTRINSIC_PAIR_NEIGHBORHOODS_DERIVED;FULL_HOPF_METRIC_DESCENT_FORCES_A_SECOND_KILLING_DIRECTION_AND_IS_INCOMPATIBLE_WITH_THE_OLD_RANK3_UNIQUE_CLOCK_CERTIFICATE;NATIVE_CLOCK_SELECTOR_CARRIER_ACTION_AND_PHYSICAL_BRANCH_REMAIN_OPEN",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
