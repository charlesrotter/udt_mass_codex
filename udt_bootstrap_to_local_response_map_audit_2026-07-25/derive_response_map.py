#!/usr/bin/env python3
"""Exact CPU algebra for the preregistered bootstrap-to-local response audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}

    # Density quotient rule.
    e = sp.symbols("e")
    M, V, dM, dV = sp.symbols("M V dM dV", nonzero=True)
    rho = M / V
    rho_e = (M + e * dM) / (V + e * dV)
    drho = sp.simplify(sp.diff(rho_e, e).subs(e, 0))
    expected_drho = sp.simplify((dM - rho * dV) / V)
    require("density_quotient_rule", sp.simplify(drho - expected_drho) == 0, checks)

    # Bulk volume variation for a general positive diagonal spatial metric.
    a, b, c = sp.symbols("a b c", positive=True)
    da, db, dc = sp.symbols("da db dc")
    h = sp.diag(a, b, c)
    dh = sp.diag(da, db, dc)
    sqrt_det = sp.sqrt((a + e * da) * (b + e * db) * (c + e * dc))
    d_sqrt_det = sp.simplify(sp.diff(sqrt_det, e).subs(e, 0))
    trace_formula = sp.simplify(sp.sqrt(h.det()) * sp.trace(h.inv() * dh) / 2)
    require("bulk_volume_first_variation", sp.simplify(d_sqrt_det - trace_formula) == 0, checks)

    # Two independent trace-free angular directions are invisible to volume.
    tau, sigma = sp.symbols("tau sigma")
    dh_tf_diag = sp.diag(0, b * tau, -c * tau)
    dh_tf_shear = sp.Matrix([[0, 0, 0], [0, 0, sigma], [0, sigma, 0]])
    require("diagonal_angular_direction_tracefree", sp.trace(h.inv() * dh_tf_diag) == 0, checks)
    require("shear_angular_direction_tracefree", sp.trace(h.inv() * dh_tf_shear) == 0, checks)
    det_tf_diag = (h + e * dh_tf_diag).det()
    det_tf_shear = (h + e * dh_tf_shear).det()
    require("diagonal_tracefree_volume_blind", sp.diff(sp.sqrt(det_tf_diag), e).subs(e, 0) == 0, checks)
    require("shear_tracefree_volume_blind", sp.diff(sp.sqrt(det_tf_shear), e).subs(e, 0) == 0, checks)

    # Any scalar density constraint inherits its angular response solely from native mass variation.
    Fp, eta, dM_tf = sp.symbols("Fprime eta dM_TF")
    alpha_density = sp.simplify(eta * Fp * drho)
    alpha_tf = sp.simplify(alpha_density.subs({dV: 0, dM: dM_tf}))
    require("density_constraint_response", sp.simplify(alpha_density - eta * Fp * (dM - rho * dV) / V) == 0, checks)
    require("tracefree_density_response_mass_only", sp.simplify(alpha_tf - eta * Fp * dM_tf / V) == 0, checks)
    require("no_mass_variation_no_angular_response", alpha_tf.subs(dM_tf, 0) == 0, checks)

    # Moving finite-cell boundary: even volume already has a boundary displacement channel.
    A, L, dA, dL = sp.symbols("A L dA dL")
    cell_volume = (A + e * dA) * (L + e * dL)
    d_cell_volume = sp.expand(sp.diff(cell_volume, e).subs(e, 0))
    require("moving_cell_volume_response", d_cell_volume == A * dL + L * dA, checks)
    require("fixed_boundary_drops_shape_channel", d_cell_volume.subs(dL, 0) == L * dA, checks)

    # A nonempty inequality window is not a stationarity equation in its interior.
    eps = sp.symbols("epsilon", positive=True)
    q_inside = eps / 2
    require("window_has_noncentral_interior_point", sp.simplify(abs(q_inside) < eps), checks)
    require("window_interior_not_root_equation", sp.simplify(q_inside) != 0, checks)

    # A zero set supplies at most a conormal line; normalization and off-shell extension are free.
    r, u, k = sp.symbols("r u k", real=True)
    B1 = r
    B2 = (1 + u**2) * r
    B3 = r + k**2 * r**3
    grad = lambda expr: sp.Matrix([sp.diff(expr, r), sp.diff(expr, u)])
    g1_on = grad(B1).subs(r, 0)
    g2_on = grad(B2).subs(r, 0)
    require("same_level_set_conormal_line", sp.simplify(g2_on[0] * g1_on[1] - g2_on[1] * g1_on[0]) == 0, checks)
    require("conormal_normalization_free", sp.simplify(g2_on[0] / g1_on[0] - (1 + u**2)) == 0, checks)
    require("positive_offshell_extension_same_real_zero", sp.factor(B3) == r * (k**2 * r**2 + 1), checks)
    require("offshell_extension_response_differs", sp.simplify(sp.diff(B3, r) - sp.diff(B1, r)) == 3 * k**2 * r**2, checks)

    # Even exact variational maps can share a realized root and differ off shell.
    q, s = sp.symbols("q s", real=True)
    lam = sp.Rational(1, 2)
    S1 = (q**2 + s**2) / 2
    S2 = S1 + lam * q * s
    alpha1 = sp.Matrix([sp.diff(S1, q), sp.diff(S1, s)])
    alpha2 = sp.Matrix([sp.diff(S2, q), sp.diff(S2, s)])
    J1 = alpha1.jacobian([q, s])
    J2 = alpha2.jacobian([q, s])
    require("counterfamily_one_unique_root", J1.det() != 0 and alpha1.subs({q: 0, s: 0}) == sp.zeros(2, 1), checks)
    require("counterfamily_two_unique_root", J2.det() != 0 and alpha2.subs({q: 0, s: 0}) == sp.zeros(2, 1), checks)
    require("same_root_different_offshell_responses", sp.simplify(alpha2 - alpha1) != sp.zeros(2, 1), checks)
    require("both_counterfamily_responses_integrable", J1 == J1.T and J2 == J2.T, checks)

    # A vector closure section produces a family of conormals until a dual covector is selected.
    x, y, l1, l2 = sp.symbols("x y lambda1 lambda2")
    closure = sp.Matrix([x + y, x - y])
    J = closure.jacobian([x, y])
    response_family = sp.simplify((sp.Matrix([[l1, l2]]) * J).T)
    require("vector_closure_jacobian_full_rank", J.det() != 0, checks)
    require("dual_covector_changes_response", response_family.subs({l1: 1, l2: 0}) != response_family.subs({l1: 0, l2: 1}), checks)

    # Multi-observable bootstrap: energy, density, and curvature enter through one chain rule.
    Eobs, Robs, Kobs = sp.symbols("E_obs rho_obs K_obs")
    lamE, lamR, lamK = sp.symbols("lambda_E lambda_rho lambda_K")
    observables = sp.Matrix([Eobs, Robs, Kobs])
    mix = sp.Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    residual = mix * observables
    residual_jacobian = residual.jacobian(observables)
    dual = sp.Matrix([[lamE, lamR, lamK]])
    observable_weights = sp.simplify((dual * residual_jacobian).T)
    require("multiobservable_chain_rule_weights", observable_weights == sp.Matrix([lamE + lamK, lamE + lamR, lamK + lamR]), checks)
    require("multiobservable_cross_jacobian_nontrivial", residual_jacobian.det() != 0, checks)

    # Complete chicken-and-egg closure has both a local branch equation and a
    # recomputation arrow. An observable-only chain rule omits the direct A_X term.
    a_x, a_o, r_x, lambda_a = sp.symbols("A_X A_O R_X lambda_A")
    dx, do = sp.symbols("delta_X delta_O")
    full_branch_differential = a_x * dx + a_o * do
    recomputation_differential = do - r_x * dx
    reduced_branch_differential = sp.expand(full_branch_differential.subs(do, r_x * dx))
    reduced_response = sp.expand(lambda_a * reduced_branch_differential)
    observable_only_response = sp.expand(lambda_a * a_o * r_x * dx)
    require("coupled_closure_full_differential",
            full_branch_differential == a_x * dx + a_o * do
            and recomputation_differential == do - r_x * dx, checks)
    require("coupled_closure_reduced_derivative",
            sp.simplify(reduced_response - lambda_a * (a_x + a_o * r_x) * dx) == 0, checks)
    require("observable_only_skeleton_omits_direct_local_arrow",
            sp.simplify(reduced_response - observable_only_response) == lambda_a * a_x * dx, checks)

    # A local sensitivity dX/dO additionally requires branch regularity.
    local_sensitivity = sp.simplify(-a_o / a_x)
    require("local_sensitivity_conditional_on_branch_invertibility",
            sp.simplify(a_x * local_sensitivity + a_o) == 0, checks)

    # The density-volume obstruction is projection-scoped: another native component may carry shear.
    k1, k2, e1, e2 = sp.symbols("k1 k2 e1 e2")
    angular_observable_jacobian = sp.Matrix([[e1, e2], [0, 0], [k1, k2]])
    angular_response = sp.simplify((dual * angular_observable_jacobian).T)
    require("non_density_component_can_carry_angular_response", angular_response == sp.Matrix([e1 * lamE + k1 * lamK, e2 * lamE + k2 * lamK]), checks)

    # Concrete mathematical curvature candidate, not a selected native UDT closure:
    # delta int sqrt(h) R has bulk coefficient (R h^ij/2 - Ric^ij) H_ij.
    # In an orthonormal Ricci eigenframe, a trace-free diagonal H=(1,-1,0)
    # gives -r1+r2, plus the separately required boundary flux.
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    scalar_r = r1 + r2 + r3
    ricci = sp.diag(r1, r2, r3)
    h_tf = sp.diag(1, -1, 0)
    curvature_bulk = sp.simplify(sum(
        (sp.Rational(1, 2) * scalar_r * int(i == j) - ricci[i, j]) * h_tf[i, j]
        for i in range(3) for j in range(3)
    ))
    require("curvature_integral_candidate_has_tracefree_bulk_response",
            curvature_bulk == -r1 + r2 and curvature_bulk.subs({r1: 2, r2: 3}) == 1, checks)

    # Invertible remixes have the same closure zero but alter a named dual response.
    remix = sp.Matrix([[1, 1], [0, 1]])
    base_residual = sp.Matrix([x, y])
    remixed_residual = remix * base_residual
    require("invertible_remix_same_zero_set", remix.det() != 0 and remixed_residual.subs({x: 0, y: 0}) == sp.zeros(2, 1), checks)
    base_named_response = sp.Matrix([[1, 0]]) * base_residual.jacobian([x, y])
    remixed_named_response = sp.Matrix([[1, 0]]) * remixed_residual.jacobian([x, y])
    require("named_dual_response_depends_on_residual_basis", base_named_response != remixed_named_response, checks)

    # The word self-consistent does not select a fixed-point operator.
    z = sp.symbols("z")
    F1 = sp.Integer(0) * z
    F2 = sp.Rational(1, 2) * z
    fixed_residual_1 = z - F1
    fixed_residual_2 = z - F2
    require("fixed_point_counterfamily_same_root", sp.solve(fixed_residual_1, z) == [0] and sp.solve(fixed_residual_2, z) == [0], checks)
    require("fixed_point_counterfamily_different_response", sp.diff(fixed_residual_1, z) != sp.diff(fixed_residual_2, z), checks)

    # Three-dimensional proper volume is not invariant under a local common rescaling.
    Omega = sp.symbols("Omega", positive=True)
    h_scaled = Omega**2 * h
    volume_ratio = sp.simplify(sp.sqrt(h_scaled.det()) / sp.sqrt(h.det()))
    require("three_volume_conformal_weight_three", volume_ratio == Omega**3, checks)

    # c and G alone cannot dimensionally select a length or a mass density.
    ac, bg = sp.symbols("a_c b_G")
    # c^a G^b dimensions: L^(a+3b) M^(-b) T^(-a-2b).
    length_solution = sp.solve(
        [sp.Eq(ac + 3 * bg, 1), sp.Eq(-bg, 0), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    density_solution = sp.solve(
        [sp.Eq(ac + 3 * bg, -3), sp.Eq(-bg, 1), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    require("c_and_G_do_not_select_length", length_solution == [], checks)
    require("c_and_G_do_not_select_density", density_solution == [], checks)

    result = {
        "schema": "udt-bootstrap-to-local-response-algebra-1.0",
        "sympy_version": sp.__version__,
        "checks": checks,
        "check_count": len(checks),
        "exact_objects": {
            "density_variation": str(expected_drho),
            "bulk_volume_variation_density": str(trace_formula),
            "tracefree_density_response": str(alpha_tf),
            "moving_cell_volume_variation": str(d_cell_volume),
            "level_set_conormal_1": [str(item) for item in g1_on],
            "level_set_conormal_2": [str(item) for item in g2_on],
            "offshell_counterfamily_alpha_1": [str(item) for item in alpha1],
            "offshell_counterfamily_alpha_2": [str(item) for item in alpha2],
            "vector_closure_response_family": [str(item) for item in response_family],
            "multiobservable_weights": [str(item) for item in observable_weights],
            "multiobservable_angular_response": [str(item) for item in angular_response],
            "curvature_integral_TF_bulk_candidate": str(curvature_bulk),
            "curvature_integral_boundary_flux": "n^i(nabla^j H_ij - nabla_i tr(H))",
            "coupled_closure_full_differentials": [
                str(full_branch_differential), str(recomputation_differential),
            ],
            "coupled_closure_reduced_response": str(reduced_response),
            "observable_only_missing_term": str(sp.simplify(reduced_response - observable_only_response)),
            "local_branch_sensitivity": str(local_sensitivity),
            "fixed_point_responses": [str(sp.diff(fixed_residual_1, z)), str(sp.diff(fixed_residual_2, z))],
            "conformal_volume_ratio": str(volume_ratio),
        },
        "structural_rulings": {
            "density_window": "ON_SHELL_ADMISSIBILITY_NO_INTERIOR_RESPONSE",
            "density_level_set": "CONDITIONAL_CONORMAL_LINE_NOT_SELECTED_ONE_FORM",
            "tracefree_angular_channel": "NATIVE_MASS_VARIATION_OR_OTHER_CLOSURE_COMPONENT_REQUIRED",
            "finite_cell": "VOLUME_HAS_SHAPE_CHANNEL_BUT_COMPLETE_MASS_BOUNDARY_RESPONSE_ABSENT",
            "metric_ontology": "CALIBRATED_METRIC_AND_CONFORMAL_CLASS_BRANCHES_INEQUIVALENT",
            "observed_anchors": "c_E_AND_G_obs_CALIBRATE_BUT_DO_NOT_SELECT_RESPONSE_FUNCTIONAL",
            "root_set": "DOES_NOT_SELECT_OFF_SHELL_RESPONSE_EVEN_WITH_INTEGRABILITY",
            "self_consistency": "DOES_NOT_SELECT_FIXED_POINT_OPERATOR_OR_LINEARIZATION",
            "minimum_missing_object": "DIFFERENTIABLE_COUPLED_GLOBAL_LOCAL_CLOSURE_SECTION_PLUS_NATIVE_DUAL_PAIRING_AND_BRANCH_REGULARITY",
            "multiobservable_bootstrap": "EXACT_COUPLED_TWO_ARROW_SKELETON_WITH_UNSELECTED_BRANCH_MAP_RECOMPUTATION_MAP_JACOBIAN_AND_DUAL_COVECTOR",
            "curvature_candidate": "TRACEFREE_BULK_RESPONSE_MATHEMATICALLY_AVAILABLE_BUT_NOT_SELECTED_NATIVE_CLOSURE_COMPONENT",
        },
    }
    (HERE / "ALGEBRA_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
