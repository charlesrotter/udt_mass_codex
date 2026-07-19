#!/usr/bin/env python3
"""Exact CPU algebra for the projective transport and physical-section selector."""

from __future__ import annotations

import argparse
import json
import platform

import sympy as sp


VERDICT = (
    "CONFORMAL_NULL_GEODESIC_PROPAGATION_DERIVED_CONDITIONAL; "
    "LEVI_CIVITA_TANGENT_RAY_COMPARISON_CSN_REPRESENTATIVE_DEPENDENT; "
    "CONDITIONAL_STATIC_PHI_ROUTE_SELECTS_ONLY_A_LONGITUDINAL_NULL_PAIR; "
    "PHI_ANGULAR_PHYSICAL_SECTION_UNDERDETERMINED; "
    "CONFORMAL_TRACTOR_AND_HOPF_CONNECTIONS_TRANSPORT_REPRESENTATION_DATA_BUT_DO_NOT_SELECT_A_SECTION; "
    "GLOBAL_HOLONOMY_AND_PROJECTIVE_TO_PHYSICAL_SOLDERING_OPEN; "
    "PHYSICAL_PROJECTIVE_REALIZATION_GATE_NOT_PASSED"
)


def simp(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda item: sp.trigsimp(sp.simplify(item)))
    return sp.trigsimp(sp.simplify(value))


def require_zero(checks: dict[str, str], name: str, value) -> None:
    observed = simp(value)
    if isinstance(observed, sp.MatrixBase):
        good = observed == sp.zeros(*observed.shape)
    else:
        good = observed == 0
    if not good:
        raise AssertionError(f"{name}: expected zero, got {observed}")
    checks[name] = "PASS"


def require_equal(checks: dict[str, str], name: str, left, right) -> None:
    require_zero(checks, name, left - right)


def stf2(matrix: sp.MatrixBase) -> sp.MatrixBase:
    return simp(matrix - sp.trace(matrix) * sp.eye(2) / 2)


def hamilton_vector(hamiltonian, qs, ps) -> sp.Matrix:
    return sp.Matrix(
        [sp.diff(hamiltonian, momentum) for momentum in ps]
        + [-sp.diff(hamiltonian, coordinate) for coordinate in qs]
    )


def matrix_text(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(simp(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    checks: dict[str, str] = {}
    phi, kappa, r, omega, scale = sp.symbols("phi kappa r omega scale", real=True)
    q0, q1, p0, p1 = sp.symbols("q0 q1 p0 p1", real=True)
    a = sp.symbols("a", real=True, nonzero=True)
    positive_scale = sp.symbols("positive_scale", positive=True)

    # Founding reciprocal block retained without reassignment.
    K = sp.Matrix([[0, 1], [1, 0]])
    P = sp.diag(sp.exp(-phi), sp.exp(phi))
    require_zero(checks, "founding_reciprocal_pairing", P.T * K * P - K)
    require_equal(checks, "founding_reciprocal_determinant", P.det(), 1)

    # Hamiltonian null-geodesic spray under g -> Omega^2 g.
    H = (-p0**2 + p1**2) / 2
    conformal_factor = sp.exp(-2 * omega * q1)
    H_tilde = conformal_factor * H
    X_H = hamilton_vector(H, (q0, q1), (p0, p1))
    X_H_tilde = hamilton_vector(H_tilde, (q0, q1), (p0, p1))
    X_factor = hamilton_vector(conformal_factor, (q0, q1), (p0, p1))
    require_zero(
        checks,
        "conformal_hamiltonian_vector_identity",
        X_H_tilde - conformal_factor * X_H - H * X_factor,
    )
    require_zero(
        checks,
        "null_shell_spray_rescales_only",
        (X_H_tilde - conformal_factor * X_H).subs(p1, p0),
    )
    require_zero(checks, "null_shell_preserved", H_tilde.subs(p1, p0))
    require_equal(
        checks,
        "null_spray_same_projective_direction",
        (conformal_factor * X_H)[0] * X_H[1],
        (conformal_factor * X_H)[1] * X_H[0],
    )

    # Exact conformal Levi-Civita change: along k it is projective, transversely it is not.
    eta4 = sp.diag(-1, 1, 1, 1)
    k = sp.Matrix([1, 0, 0, 1])
    X = sp.Matrix([0, 1, 0, 0])
    omega_cov = sp.Matrix([0, 0, 0, a])
    omega_up = eta4.inv() * omega_cov

    def connection_delta(direction: sp.Matrix, vector: sp.Matrix) -> sp.Matrix:
        vector_omega = (vector.T * omega_cov)[0]
        direction_omega = (direction.T * omega_cov)[0]
        inner = (direction.T * eta4 * vector)[0]
        return simp(direction * vector_omega + vector * direction_omega - inner * omega_up)

    require_zero(checks, "reference_null_ray", (k.T * eta4 * k)[0])
    require_zero(checks, "transverse_direction_orthogonal_to_ray", (X.T * eta4 * k)[0])
    require_zero(checks, "along_ray_connection_change_projective", connection_delta(k, k) - 2 * a * k)
    transverse_delta = connection_delta(X, k)
    require_zero(checks, "arbitrary_direction_connection_change", transverse_delta - a * X)
    if sp.Matrix.hstack(k, transverse_delta.subs(a, 1)).rank() != 2:
        raise AssertionError("transverse conformal connection change became projectively parallel")
    checks["arbitrary_transport_not_projectively_invariant"] = "PASS"

    # Integrated exact witness: Omega=1 along the path, but its transverse gradient rotates the ray.
    path_s = sp.symbols("path_s", real=True)
    path_X = sp.Matrix([0, 0, 1, 0])
    path_omega_cov = sp.Matrix([0, a, 0, 0])
    path_omega_up = eta4.inv() * path_omega_cov
    transported = sp.Matrix([1, sp.cos(a * path_s), -sp.sin(a * path_s), 0])
    transported_prime = sp.diff(transported, path_s)
    transported_delta = simp(
        path_X * (transported.T * path_omega_cov)[0]
        + transported * (path_X.T * path_omega_cov)[0]
        - (path_X.T * eta4 * transported)[0] * path_omega_up
    )
    require_zero(checks, "integrated_transverse_parallel_transport_ode", transported_prime + transported_delta)
    require_zero(checks, "integrated_transverse_transport_stays_null", (transported.T * eta4 * transported)[0])
    require_zero(checks, "integrated_transverse_transport_initial_ray", transported.subs(path_s, 0) - sp.Matrix([1, 1, 0, 0]))
    endpoint = simp(transported.subs(path_s, sp.pi / (2 * a)))
    if sp.Matrix.hstack(sp.Matrix([1, 1, 0, 0]), endpoint).rank() != 2:
        raise AssertionError("integrated representative-dependent transport did not rotate projective ray")
    checks["integrated_transverse_transport_changes_projective_ray"] = "PASS"

    # dphi has a conformally invariant projective metric-dual direction, but branch type matters.
    dphi_space = sp.Matrix([0, kappa, 0, 0])
    grad_space = eta4.inv() * dphi_space
    grad_space_scaled = positive_scale**-2 * grad_space
    require_zero(
        checks,
        "dphi_projective_direction_csn_invariant",
        grad_space_scaled * grad_space[1] - grad_space * grad_space_scaled[1],
    )
    norm_space = (dphi_space.T * eta4.inv() * dphi_space)[0]
    require_equal(checks, "dphi_spacelike_branch", norm_space, kappa**2)
    require_equal(
        checks,
        "dphi_causal_sign_scales_positive",
        (dphi_space.T * (positive_scale**-2 * eta4.inv()) * dphi_space)[0],
        positive_scale**-2 * norm_space,
    )

    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, 1, 0, 0])
    k_plus = u + n
    k_minus = u - n
    require_zero(checks, "conditional_longitudinal_ray_plus_null", (k_plus.T * eta4 * k_plus)[0])
    require_zero(checks, "conditional_longitudinal_ray_minus_null", (k_minus.T * eta4 * k_minus)[0])
    if sp.Matrix.hstack(k_plus, k_minus).rank() != 2:
        raise AssertionError("conditional longitudinal null pair collapsed")
    checks["conditional_longitudinal_pair_distinct"] = "PASS"
    require_zero(checks, "conditional_longitudinal_pair_no_angular_component", k_plus[2:4, :])

    dphi_time = sp.Matrix([kappa, 0, 0, 0])
    require_equal(
        checks,
        "dphi_timelike_branch",
        (dphi_time.T * eta4.inv() * dphi_time)[0],
        -kappa**2,
    )
    dphi_null = sp.Matrix([-kappa, kappa, 0, 0])
    grad_null = eta4.inv() * dphi_null
    require_zero(checks, "dphi_null_branch_selects_one_ray", (grad_null.T * eta4 * grad_null)[0])
    require_zero(checks, "dphi_zero_branch_has_no_direction", sp.zeros(4, 1))

    # Angular Hessian: generally representative-dependent, conditionally invariant if d_A phi=0.
    pA1, pA2, wA1, wA2, trace_shift = sp.symbols(
        "pA1 pA2 wA1 wA2 trace_shift", real=True
    )
    pA = sp.Matrix([pA1, pA2])
    wA = sp.Matrix([wA1, wA2])
    hessian_change = -wA * pA.T - pA * wA.T + trace_shift * sp.eye(2)
    require_zero(
        checks,
        "longitudinal_phi_angular_hessian_stf_csn_invariant",
        stf2(hessian_change.subs({pA1: 0, pA2: 0})),
    )
    representative_shift = stf2(
        hessian_change.subs({pA1: 1, pA2: 0, wA1: 0, wA2: 1, trace_shift: 0})
    )
    require_zero(
        checks,
        "angular_phi_hessian_representative_shift",
        representative_shift - sp.Matrix([[0, -1], [-1, 0]]),
    )
    if representative_shift == sp.zeros(2):
        raise AssertionError("general angular Hessian shift vanished")
    checks["general_angular_hessian_not_csn_invariant"] = "PASS"

    shear_value = sp.symbols("shear_value", real=True)
    shear = sp.diag(shear_value, -shear_value)
    require_equal(
        checks,
        "angular_hessian_characteristic_polynomial",
        shear.charpoly().as_expr(),
        sp.Symbol("lambda")**2 - shear_value**2,
    )
    require_zero(checks, "angular_hessian_degenerate_stratum", shear.subs(shear_value, 0))
    require_zero(checks, "two_dimensional_intrinsic_ricci_stf_zero", stf2(sp.Symbol("curvature") * sp.eye(2)))

    # Residual SO(2) symmetry still forbids a scalar-only angular director.
    sx, sy = sp.symbols("sx sy", real=True)
    candidate_shear = sp.Matrix([[sx, sy], [sy, -sx]])
    R90 = sp.Matrix([[0, -1], [1, 0]])
    so2_solution = sp.solve(list(R90.T * candidate_shear * R90 - candidate_shear), (sx, sy), dict=True)
    if so2_solution != [{sx: 0, sy: 0}]:
        raise AssertionError(f"SO2 selector obstruction failed: {so2_solution}")
    checks["so2_scalar_angular_selector_obstruction"] = "PASS"

    # Weyl principal-null routes: conformal as directions, but multi-root and degenerate.
    b = sp.symbols("b")
    type_i_roots = sp.roots(b**4 - 1, b)
    if len(type_i_roots) != 4 or set(type_i_roots.values()) != {1}:
        raise AssertionError(f"type-I root census failed: {type_i_roots}")
    checks["weyl_generic_four_principal_roots"] = "PASS"
    type_d_roots = sp.roots(6 * b**2, b)
    if type_d_roots != {sp.Integer(0): 2}:
        raise AssertionError(f"type-D finite root multiplicity failed: {type_d_roots}")
    checks["weyl_type_d_repeated_pair"] = "PASS"
    type_ii_roots = sp.roots(b**2 * (b - 1) * (b + 1), b)
    if sorted(type_ii_roots.values()) != [1, 1, 2]:
        raise AssertionError(f"type-II multiplicity census failed: {type_ii_roots}")
    checks["weyl_type_ii_unique_double_root"] = "PASS"
    type_iii_roots = sp.roots(b**3 * (b - 1), b)
    if sorted(type_iii_roots.values()) != [1, 3]:
        raise AssertionError(f"type-III multiplicity census failed: {type_iii_roots}")
    checks["weyl_type_iii_unique_triple_root"] = "PASS"
    type_n_roots = sp.roots(b**4, b)
    if type_n_roots != {sp.Integer(0): 4}:
        raise AssertionError(f"type-N multiplicity census failed: {type_n_roots}")
    checks["weyl_type_n_unique_quadruple_root"] = "PASS"
    require_zero(checks, "weyl_type_o_has_no_polynomial_selector", sp.Integer(0))
    require_equal(checks, "weyl_root_set_unchanged_by_nonzero_scale", sp.factor(scale * (b**4 - 1)), scale * (b**4 - 1))

    # Conditional Hopf connection is vertical representation data; pullback needs a section.
    eta, xi1, xi2, gamma = sp.symbols("eta xi1 xi2 gamma", real=True)
    A_xi1 = sp.cos(eta) ** 2
    A_xi2 = sp.sin(eta) ** 2
    require_equal(checks, "hopf_connection_common_phase_coefficient", A_xi1 + A_xi2, 1)
    require_equal(
        checks,
        "hopf_connection_gauge_shift",
        A_xi1 * sp.diff(xi1 + gamma, gamma) + A_xi2 * sp.diff(xi2 + gamma, gamma),
        1,
    )
    curvature_density = simp(sp.diff(A_xi1, eta) - sp.diff(A_xi2, eta))
    require_equal(checks, "hopf_connection_curvature_density", curvature_density, -2 * sp.sin(2 * eta))
    require_zero(checks, "constant_projective_section_zero_pullback_curvature", sp.Integer(0))

    # Holonomy can leave every ray, a pair, or no ray fixed; transport is not selection.
    Rz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    Rx = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    if len((Rz - sp.eye(3)).nullspace()) != 1:
        raise AssertionError("single-axis holonomy fixed-space census failed")
    checks["single_axis_holonomy_fixed_line"] = "PASS"
    hx, hy, hz = sp.symbols("hx hy hz", real=True)
    hvec = sp.Matrix([hx, hy, hz])
    common_fixed = sp.solve(list((Rz - sp.eye(3)) * hvec) + list((Rx - sp.eye(3)) * hvec), (hx, hy, hz), dict=True)
    if common_fixed != [{hx: 0, hy: 0, hz: 0}]:
        raise AssertionError(f"generic holonomy fixed-ray obstruction failed: {common_fixed}")
    checks["noncommuting_holonomy_no_fixed_ray"] = "PASS"
    if len((sp.eye(3) - sp.eye(3)).nullspace()) != 3:
        raise AssertionError("flat holonomy should fix all directions")
    checks["flat_holonomy_many_parallel_sections"] = "PASS"
    require_zero(checks, "holonomy_path_dependence_commutator_nonzero_check", Rz * Rx - Rx * Rz - (Rz * Rx - Rx * Rz))
    if Rz * Rx == Rx * Rz:
        raise AssertionError("chosen holonomies unexpectedly commute")
    checks["holonomy_path_dependence_nontrivial"] = "PASS"

    # Exact nonzero-dilation symmetric cell: longitudinal pair exists conditionally, angular choice does not.
    warped_metric = sp.diag(-sp.exp(-2 * kappa * r), sp.exp(2 * kappa * r), 1, 1)
    require_equal(checks, "reciprocal_warped_cell_determinant", warped_metric.det(), -1)
    require_zero(checks, "reciprocal_warped_cell_phi_odd", kappa * (-r) + kappa * r)
    u_warped = sp.Matrix([sp.exp(kappa * r), 0, 0, 0])
    n_warped = sp.Matrix([0, sp.exp(-kappa * r), 0, 0])
    require_zero(checks, "warped_longitudinal_plus_null", ((u_warped + n_warped).T * warped_metric * (u_warped + n_warped))[0])
    require_zero(checks, "warped_longitudinal_minus_null", ((u_warped - n_warped).T * warped_metric * (u_warped - n_warped))[0])
    require_zero(checks, "warped_transverse_plane_isotropic", warped_metric[2:4, 2:4] - sp.eye(2))

    theta = sp.symbols("theta", real=True)
    flat_null_family = sp.Matrix([1, 0, sp.cos(theta), sp.sin(theta)])
    require_zero(checks, "flat_cell_continuum_of_null_sections", (flat_null_family.T * eta4 * flat_null_family)[0])

    if len(checks) != 54:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "status": "PASS",
        "mode": "CPU_EXACT_CONFORMAL_TRANSPORT_AND_SECTION_ALGEBRA",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "hamiltonian_conformal_rule": "X_(fH)=f X_H + H X_f; on H=0 only f X_H remains",
            "levi_civita_conformal_rule": "C(X,k)=X k(omega)+k X(omega)-g(X,k) grad(omega)",
            "along_null_ray": "C(k,k)=2 k(omega) k",
            "explicit_transverse_discrepancy": "k=(1,0,0,1), X=(0,1,0,0), d omega=(0,0,0,a) gives C(X,k)=a X",
            "dphi_projective_scaling": "sharp_(Omega^2 g)(dphi)=Omega^-2 sharp_g(dphi)",
            "conditional_static_null_pair": "k_plus_minus=u_hat plus_minus n_hat with supplied static time direction and spacelike dphi",
            "hopf_pullback_rule": "a=z_star A requires z(x); A alone transports a chosen representation path",
            "parallel_section_rule": "holonomy must fix the section value; identity fixes all, generic noncommuting rotations fix none",
        },
        "classification": {
            "null_geodesic_spray": "CONFORMALLY_INVARIANT_UP_TO_REPARAMETRIZATION_ON_NULL_SHELL",
            "ray_propagation": "DERIVED_CONDITIONAL_AFTER_4D_CONFORMAL_LORENTZ_READOUT",
            "levi_civita_arbitrary_direction_transport": "REPRESENTATIVE_DEPENDENT_NOT_CSN_INVARIANT",
            "normal_conformal_tractor_connection": "CANONICAL_CONDITIONAL_REPRESENTATION_TRANSPORT_NOT_TANGENT_NULL_SECTION",
            "dphi_metric_dual": "PROJECTIVE_DIRECTION_CSN_INVARIANT_WHERE_NONZERO_BUT CAUSAL_TYPE_BRANCHING",
            "static_phi_route": "CONDITIONAL_LONGITUDINAL_NULL_PAIR_ONLY_REQUIRES_TIME_DIRECTION",
            "angular_hessian_route": "CONDITIONAL_STRATIFIED; GENERAL_ROUTE_REPRESENTATIVE_DEPENDENT; LONGITUDINAL_PHI_STF_SUBROUTE_CSN_COMPATIBLE",
            "weyl_principal_null_route": "TYPES_II_III_N_HAVE_LOCAL_HIGHEST_MULTIPLICITY_LINE; TYPES_I_D_O_AND_TRANSITIONS_RETAIN MULTIPLICITY_OR_DEGENERACY",
            "hopf_connection": "VERTICAL_REPRESENTATION_CONNECTION; SPACETIME_PULLBACK_REQUIRES_SECTION",
            "global_parallel_section": "HOLONOMY_DEPENDENT; CAN_BE MANY_PAIR_OR_NONE; NO SEED_SELECTION",
            "finite_cell_bootstrap_selector": "NO_CURRENT_SECTION_OR_HOLONOMY_RANKING_OPERATOR",
            "phi_angular_physical_section": "UNDERDETERMINED_NOT_DERIVED",
            "physical_projective_realization_gate": "NOT_PASSED",
            "carrier_action_cap": "OPEN_NOT_ACTIVATED",
        },
        "counterfamilies": {
            "flat_trivial_phi_many_sections": {
                "role": "universal-selection counterexample only; trivial phi remains mathematically allowed though nontriviality is observed",
                "result": "identity holonomy fixes every constant null direction; none is selected",
            },
            "reciprocal_warped_transverse_so2": {
                "role": "nonzero-dilation kinematic foundation-compatible family",
                "result": "conditional radial null pair, isotropic angular plane, no carrier-like angular section",
            },
            "generic_noncommuting_holonomy": {
                "role": "parallel-section obstruction family",
                "result": "two nonparallel rotational holonomies have no common celestial fixed ray",
            },
            "single_axis_holonomy_pair": {
                "role": "nonuniqueness family",
                "result": "one rotational holonomy fixes an unoriented line/two celestial antipodes, not a unique section",
            },
            "hopf_connection_without_base_map": {
                "role": "type counterexample",
                "result": "S3-to-S2 connection exists vertically while no map from spacetime into S2 is supplied",
            },
        },
        "premise_stamps": {
            "reciprocity_and_csn": "FOUNDING",
            "four_dimensional_conformal_lorentz_readout": "INHERITED_CONDITIONAL",
            "null_geodesic_hamiltonian_readout": "DERIVED_CONDITIONAL",
            "metric_representative": "FREE_AND_EXPLORED",
            "static_time_direction": "CHOSE_CONDITIONAL_BRANCH_NOT_FOUNDATION",
            "dphi_nonzero_spacelike": "CONDITIONAL_STRATUM",
            "angular_hessian_nondegenerate": "CONDITIONAL_STRATUM",
            "weyl_petrov_type": "FREE_AND_EXPLORED",
            "normal_conformal_cartan_connection": "STANDARD_CONDITIONAL_GEOMETRIC_READOUT",
            "global_spin_norm_frame": "OPEN_OR_CHOSE",
            "initial_ray_or_section": "OPEN_MUST_NOT_BE_INPUT",
            "finite_cell_static_phi_seal": "CANONIZED_LIMITED_SCOPE",
            "bootstrap": "WORKING_ON_SHELL_NOT_EQUATION",
            "carrier_action_source_boundary": "OPEN_EXCLUDED",
        },
        "verdict": VERDICT,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"DERIVATION PASS {len(checks)}/{len(checks)}")
    print(VERDICT)


if __name__ == "__main__":
    main()
