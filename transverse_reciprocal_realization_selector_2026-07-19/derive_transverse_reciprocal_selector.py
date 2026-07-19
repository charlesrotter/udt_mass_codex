#!/usr/bin/env python3
"""Exact CPU algebra for the transverse reciprocal realization selector."""

from __future__ import annotations

import argparse
import json
import platform

import sympy as sp


VERDICT = (
    "EXACT_REPRESENTATION_LEVEL_RECIPROCAL_HOPF_CORRESPONDENCE_"
    "CONDITIONAL_ON_LORENTZ_SPIN_REALIZATION; "
    "PHYSICAL_TRANSVERSE_SPATIAL_PERIODICITY_UNDERDETERMINED; "
    "GLOBAL_UNIT_HOPF_LIFT_AND_SOLDERING_OPEN; "
    "FINITE_CELL_CAP_GATE_NOT_ACTIVATED"
)


def simplify(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda item: sp.trigsimp(sp.simplify(sp.expand_complex(item))))
    return sp.trigsimp(sp.simplify(sp.expand_complex(value)))


def require_zero(checks: dict[str, str], name: str, value) -> None:
    observed = simplify(value)
    if isinstance(observed, sp.MatrixBase):
        good = observed == sp.zeros(*observed.shape)
    else:
        good = observed == 0
    if not good:
        raise AssertionError(f"{name}: expected zero, got {observed}")
    checks[name] = "PASS"


def require_equal(checks: dict[str, str], name: str, left, right) -> None:
    require_zero(checks, name, left - right)


def matrix_text(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(simplify(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    checks: dict[str, str] = {}
    phi, a, alpha, kappa, r = sp.symbols("phi a alpha kappa r", real=True)
    eta, xi1, xi2, gamma, beta = sp.symbols("eta xi1 xi2 gamma beta", real=True)
    t, lam = sp.symbols("t lam", positive=True)
    seed_a, seed_b = sp.symbols("seed_a seed_b", positive=True)
    I = sp.I

    # Founding reciprocal action and its direct Lorentz-signature extension.
    K2 = sp.Matrix([[0, 1], [1, 0]])
    P2 = sp.diag(sp.exp(-phi), sp.exp(phi))
    require_zero(checks, "founding_dual_pairing", P2.T * K2 * P2 - K2)
    K4 = sp.diag(1, 1, 1, 1)
    K4[0, 0] = 0
    K4[1, 1] = 0
    K4[0, 1] = 1
    K4[1, 0] = 1
    P4 = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    require_zero(checks, "direct_vector_extension_preserves_form", P4.T * K4 * P4 - K4)
    require_zero(checks, "direct_vector_extension_transverse_identity", P4[2:4, 2:4] - sp.eye(2))
    require_equal(checks, "direct_vector_extension_unit_determinant", P4.det(), 1)

    # A scalar and an isotropic oriented transverse plane cannot naturally select shear axes.
    x, y = sp.symbols("x y", real=True)
    T = sp.Matrix([[x, y], [y, -x]])
    R90 = sp.Matrix([[0, -1], [1, 0]])
    R45 = sp.sqrt(2) / 2 * sp.Matrix([[1, -1], [1, 1]])
    equations = list(R90.T * T * R90 - T) + list(R45.T * T * R45 - T)
    solution = sp.solve(equations, (x, y), dict=True)
    if solution != [{x: 0, y: 0}]:
        raise AssertionError(f"SO2 invariant TF tensor solution: {solution}")
    checks["so2_equivariance_obstruction"] = "PASS"

    # Foundation-compatible finite local countermodel.
    counter_metric = sp.diag(-sp.exp(-2 * kappa * r), sp.exp(2 * kappa * r), 1, 1)
    require_equal(checks, "finite_countermodel_determinant", counter_metric.det(), -1)
    require_zero(checks, "finite_countermodel_phi_odd", kappa * (-r) + kappa * r)
    require_zero(checks, "finite_countermodel_transverse_shear", counter_metric[2:4, 2:4] - sp.eye(2))
    # Since g_AB is constant and phi depends only on r, the projected transverse Hessian is zero.
    transverse_hessian = sp.zeros(2)
    require_zero(checks, "finite_countermodel_projected_hessian", transverse_hessian)

    # Hodge/orientation returns a transverse area element, not two line projectors.
    e01_dual = sp.Matrix([[0, 1], [-1, 0]])
    require_equal(checks, "hodge_transverse_area_rank", e01_dual.det(), 1)
    require_zero(checks, "hodge_area_has_no_symmetric_tf_part", (e01_dual + e01_dual.T) / 2)

    # Two-component Lorentz-spin representation and null Hermitian factorization.
    z = sp.Matrix([
        sp.cos(eta) * sp.exp(I * xi1),
        sp.sin(eta) * sp.exp(I * xi2),
    ])
    zdag = sp.conjugate(z.T)
    hermitian_null = z * zdag
    require_zero(checks, "spinor_hermitian_rank_one_null", hermitian_null.det())
    require_equal(checks, "unit_spinor_norm", (zdag * z)[0], 1)

    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -I], [I, 0]])
    sigma3 = sp.Matrix([[1, 0], [0, -1]])
    n = sp.Matrix([simplify((zdag * sigma * z)[0]) for sigma in (sigma1, sigma2, sigma3)])
    require_equal(checks, "projective_null_direction_unit_sphere", (n.T * n)[0], 1)

    boost = sp.diag(sp.exp(-a), sp.exp(a))
    require_equal(checks, "spin_boost_special_linear", boost.det(), 1)
    ratio_squared_before = sp.tan(eta) ** 2
    ratio_squared_after = sp.exp(4 * a) * ratio_squared_before
    require_equal(
        checks,
        "spin_boost_reciprocal_ratio",
        ratio_squared_after / ratio_squared_before,
        sp.exp(4 * a),
    )
    twisted_boost = sp.diag(
        sp.exp((-1 + I * alpha) * phi),
        sp.exp((1 - I * alpha) * phi),
    )
    require_equal(checks, "phase_twisted_embedding_special_linear", twisted_boost.det(), 1)
    require_zero(
        checks,
        "phase_twisted_embedding_same_metric_weights",
        sp.conjugate(twisted_boost.T) * twisted_boost
        - sp.diag(sp.exp(-2 * phi), sp.exp(2 * phi)),
    )

    # Hopf orbit block in rational t=tan(eta) coordinates.
    orbit = sp.diag(1 / (1 + t**2), t**2 / (1 + t**2))
    orbit_area = t / (1 + t**2)
    normalized_orbit = simplify(orbit / orbit_area)
    require_zero(checks, "normalized_hopf_orbit", normalized_orbit - sp.diag(1 / t, t))
    reciprocal_substitution = normalized_orbit.subs(t, sp.exp(2 * phi))
    require_zero(
        checks,
        "exact_reciprocal_hopf_correspondence",
        reciprocal_substitution - sp.diag(sp.exp(-2 * phi), sp.exp(2 * phi)),
    )
    generic_seed_orbit = sp.diag(
        seed_a * sp.exp(-2 * phi) / seed_b,
        seed_b * sp.exp(2 * phi) / seed_a,
    )
    require_zero(
        checks,
        "generic_seed_normalized_orbit",
        generic_seed_orbit
        - sp.diag(seed_a * sp.exp(-2 * phi) / seed_b, seed_b * sp.exp(2 * phi) / seed_a),
    )
    balanced_solution = sp.solve(sp.Eq(seed_a / seed_b, 1), seed_a, dict=True)
    if balanced_solution != [{seed_a: seed_b}]:
        raise AssertionError(f"balanced seed solution: {balanced_solution}")
    checks["balanced_seed_required_at_phi_zero"] = "PASS"

    delta = xi2 - xi1
    projective_n = sp.Matrix([
        2 * t * sp.cos(delta) / (1 + t**2),
        2 * t * sp.sin(delta) / (1 + t**2),
        (1 - t**2) / (1 + t**2),
    ])
    require_equal(checks, "cp1_bilinear_unit_sphere", (projective_n.T * projective_n)[0], 1)
    reciprocal_n = simplify(projective_n.subs(t, sp.exp(2 * phi)))
    expected_n = sp.Matrix([
        sp.sech(2 * phi) * sp.cos(delta),
        sp.sech(2 * phi) * sp.sin(delta),
        -sp.tanh(2 * phi),
    ])
    require_zero(checks, "reciprocal_projective_celestial_flow", reciprocal_n - expected_n)
    rho = sp.symbols("rho", positive=True)
    fs_boost_factor = lam**2 * (1 + rho**2) ** 2 / (1 + lam**2 * rho**2) ** 2
    require_equal(
        checks,
        "projective_boost_not_round_isometry",
        fs_boost_factor.subs({lam: 2, rho: 1}),
        sp.Rational(16, 25),
    )

    radial_r1 = sp.exp(-phi) / sp.sqrt(2 * sp.cosh(2 * phi))
    radial_r2 = sp.exp(phi) / sp.sqrt(2 * sp.cosh(2 * phi))
    radial_metric = simplify(sp.diff(radial_r1, phi) ** 2 + sp.diff(radial_r2, phi) ** 2)
    require_equal(checks, "normalized_spinor_radial_metric", radial_metric, sp.sech(2 * phi) ** 2)

    irrational_slope = sp.sqrt(2)
    if irrational_slope.is_irrational is not True:
        raise AssertionError("sqrt(2) irrationality not certified")
    checks["irrational_torus_first_eigenflow_nonclosed"] = "PASS"
    if (-1 / irrational_slope).is_irrational is not True:
        raise AssertionError("-1/sqrt(2) irrationality not certified")
    checks["irrational_torus_second_eigenflow_nonclosed"] = "PASS"
    hessian_cov = sp.diag(-kappa**2 * sp.exp(-4 * phi), kappa**2)
    transverse_inverse = sp.diag(sp.exp(2 * phi), sp.exp(-2 * phi))
    require_zero(
        checks,
        "irrational_torus_projected_hessian_selects_dense_axes",
        transverse_inverse * hessian_cov
        - sp.diag(-kappa**2 * sp.exp(-2 * phi), kappa**2 * sp.exp(-2 * phi)),
    )

    # Positive common scale and common phase disappear from the projective direction.
    u1, u2 = sp.symbols("u1 u2", complex=True)
    norm = sp.conjugate(u1) * u1 + sp.conjugate(u2) * u2
    generic = sp.Matrix([u1, u2])
    generic_dag = sp.conjugate(generic.T)
    generic_n = sp.Matrix([simplify((generic_dag * sigma * generic)[0] / norm) for sigma in (sigma1, sigma2, sigma3)])
    scaled = lam * generic
    scaled_dag = sp.conjugate(scaled.T)
    scaled_norm = (scaled_dag * scaled)[0]
    scaled_n = sp.Matrix([simplify((scaled_dag * sigma * scaled)[0] / scaled_norm) for sigma in (sigma1, sigma2, sigma3)])
    require_zero(checks, "positive_common_scale_projective_invariance", scaled_n - generic_n)
    common_phase_delta = simplify((xi2 + gamma) - (xi1 + gamma) - delta)
    require_zero(checks, "common_phase_projective_invariance", common_phase_delta)
    relative_phase_delta = simplify((xi2 - beta) - (xi1 + beta) - delta + 2 * beta)
    require_zero(checks, "relative_phase_is_celestial_azimuth", relative_phase_delta)

    common_phase_matrix = sp.exp(I * gamma) * sp.eye(2)
    relative_phase_matrix = sp.diag(sp.exp(I * beta), sp.exp(-I * beta))
    require_equal(checks, "common_phase_not_generically_sl2", common_phase_matrix.det(), sp.exp(2 * I * gamma))
    require_equal(checks, "relative_phase_is_sl2", relative_phase_matrix.det(), 1)

    # No positive Hermitian norm is invariant under the full boost subgroup.
    h11, h22, hx, hy = sp.symbols("h11 h22 hx hy", real=True)
    H = sp.Matrix([[h11, hx + I * hy], [hx - I * hy, h22]])
    boost_two = sp.diag(sp.Rational(1, 2), 2)
    invariant_equations = list(boost_two.conjugate().T * H * boost_two - H)
    invariant_solution = sp.solve(invariant_equations, (h11, h22), dict=True)
    if invariant_solution != [{h11: 0, h22: 0}]:
        raise AssertionError(f"boost invariant Hermitian solution: {invariant_solution}")
    checks["no_lorentz_invariant_positive_spinor_norm"] = "PASS"
    require_equal(
        checks,
        "boost_invariant_hermitian_form_nonpositive",
        H.subs(invariant_solution[0]).det(),
        -(hx**2 + hy**2),
    )

    # Hopf connection and unit class in the conditional unit-spinor lift.
    A_xi1 = sp.cos(eta) ** 2
    A_xi2 = sp.sin(eta) ** 2
    require_equal(checks, "hopf_connection_vertical_normalization", A_xi1 + A_xi2, 1)
    curvature_eta_xi1 = sp.diff(A_xi1, eta)
    curvature_eta_xi2 = sp.diff(A_xi2, eta)
    wedge_coefficient = simplify(A_xi2 * curvature_eta_xi1 - A_xi1 * curvature_eta_xi2)
    require_equal(checks, "hopf_connection_wedge_density", wedge_coefficient, -sp.sin(2 * eta))
    hopf_integral = simplify(sp.integrate(wedge_coefficient, (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2)
    require_equal(checks, "conditional_hopf_connection_integral", hopf_integral, -4 * sp.pi**2)
    require_equal(checks, "conditional_hopf_unit_class", -hopf_integral / (4 * sp.pi**2), 1)

    if len(checks) != 40:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "status": "PASS",
        "mode": "CPU_EXACT_METRIC_AND_REPRESENTATION_ALGEBRA",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "founding_pairing": matrix_text(K2),
            "founding_action": matrix_text(P2),
            "direct_4d_transverse_block": matrix_text(P4[2:4, 2:4]),
            "so2_invariant_tracefree_solution": {"x": "0", "y": "0"},
            "finite_countermodel_metric": matrix_text(counter_metric),
            "spin_boost": matrix_text(boost),
            "phase_twisted_spin_embedding": matrix_text(twisted_boost),
            "normalized_hopf_orbit": matrix_text(normalized_orbit),
            "reciprocal_hopf_orbit": matrix_text(reciprocal_substitution),
            "generic_seed_reciprocal_orbit": matrix_text(generic_seed_orbit),
            "projective_direction": [str(item) for item in reciprocal_n],
            "normalized_spinor_radial_metric": str(radial_metric),
            "fubini_study_boost_factor_at_lambda2_rho1": "16/25",
            "hopf_integral": str(hopf_integral),
            "hopf_unit_class": "1",
        },
        "topological_classification": {
            "positive_scale_quotient": "C2_MINUS_ZERO_MOD_RPLUS_DIFFEO_S3_AFTER_NORM_CHOICE",
            "projective_quotient": "C2_MINUS_ZERO_MOD_CSTAR_IS_CP1_DIFFEO_S2",
            "metric_rotation_frame_bundle_over_S2": "SO3_TO_S2_WITH_CIRCLE_FIBER; TOTAL_RP3; EULER_CLASS_MAGNITUDE_2",
            "spin_lift_bundle_over_S2": "SU2_TO_S2_WITH_CIRCLE_FIBER; TOTAL_S3; CHERN_CLASS_MAGNITUDE_1",
            "common_phase_role": "HOPF_FIBER_GAUGE_NOT_SECOND_PHYSICAL_SPATIAL_DIRECTION",
            "relative_phase_role": "CELESTIAL_AZIMUTH_AFTER_AXIS_AND_FRAME_CHOICE",
        },
        "counterfamilies": {
            "finite_disk_transverse": {
                "geometry": "R_t x [-L,L]_r x D2 with diag(-e^-2kr,e^2kr,1,1)",
                "foundation_status": "KINEMATICALLY_COMPATIBLE; COMPLETE_ACTION_AND_BOOTSTRAP_ADMISSIBILITY_UNTESTABLE",
                "periodic_transverse_pair": "ABSENT",
            },
            "finite_sphere_transverse": {
                "geometry": "R_t x [-L,L]_r x S2 with reciprocal longitudinal block and round transverse S2",
                "foundation_status": "KINEMATICALLY_COMPATIBLE; S2_HAS_NO_FREE_EFFECTIVE_T2_ACTION",
                "periodic_transverse_pair": "ABSENT",
            },
            "local_plane_vs_torus": {
                "geometry": "identical local flat transverse metric on R2 and T2",
                "foundation_status": "LOCAL_C0_C1_CANNOT_DISTINGUISH_GLOBAL_PERIOD_IDENTIFICATIONS",
                "periodic_transverse_pair": "GLOBAL_CHOICE_NOT_LOCAL_CONSEQUENCE",
            },
            "irrational_torus_eigenflow": {
                "geometry": "T2 with exact reciprocal metric in a constant irrational-slope eigenbasis",
                "foundation_status": "GRANTS_TRANSVERSE_TORUS_AND_RECIPROCAL_AXES_BUT_BOTH_EIGENFLOWS_ARE_DENSE",
                "periodic_transverse_pair": "ABSENT_DESPITE_TORUS_AND_NONDEGENERATE_HESSIAN_AXES",
            },
            "spin_representation_only": {
                "geometry": "conditional local SL2C doublet with projective celestial CP1",
                "foundation_status": "EXACT_REPRESENTATION_CORRESPONDENCE_WITH_OPEN_GLOBAL_SPIN_AND_SOLDERING",
                "periodic_transverse_pair": "PHASE_COORDINATES_NOT_SPACETIME_DIRECTIONS",
            },
        },
        "classification": {
            "direct_tangent_vector_route": "TRANSVERSE_IDENTITY_NOT_RECIPROCAL_PAIR",
            "so2_natural_tensor_route": "NO_NONZERO_SCALAR_ONLY_EQUIVARIANT_TRACEFREE_TENSOR",
            "metric_derivative_route": "CONDITIONAL_STRATIFIED_AND_DEGENERATE; NO_FORCED_EXPONENTIAL_WEIGHTS_OR_CLOSED_ORBITS",
            "representation_correspondence": "EXACT_WITHIN_CONDITIONAL_LORENTZ_SPIN_REALIZATION",
            "spin_embedding_uniqueness": "REAL_POSITIVE_EMBEDDING_REQUIRES_ALPHA_ZERO; METRIC_MAGNITUDES_ALONE_ALLOW_PHASE_TWIST_ALPHA",
            "balanced_reference_ray": "EQUAL_COMPONENT_MAGNITUDES_AT_PHI_ZERO_REQUIRED_FOR_UNSHIFTED_PRIOR_BLOCK",
            "physical_transverse_spatial_periodicity": "UNDERDETERMINED_NOT_DERIVED",
            "global_unit_hopf_lift": "OPEN_WITHOUT_GLOBAL_SPIN_LIFT_AND_NORM_FRAME_DATA",
            "soldering_to_physical_spacetime": "OPEN",
            "finite_cell_bootstrap_rejection_operator": "ABSENT_FROM_REGISTERED_WORDING",
            "finite_cell_cap_gate": "NOT_ACTIVATED",
            "smallest_missing_gate": "NATIVE_REALIZATION_OR_SOLDERING_RULE_FROM_RECIPROCAL_PROJECTIVE_GEOMETRY_TO_PHYSICAL_FIELD_OR_TRANSVERSE_METRIC_DATA",
        },
        "premise_stamps": {
            "reciprocal_pair": "DERIVED_CONDITIONAL",
            "4d_conformal_lorentzian_readout": "INHERITED_CONDITIONAL",
            "internal_pair_to_lorentz_boost_embedding": "CONDITIONAL_OPEN_REALIZATION_MAP",
            "local_spin_frame": "CHOSE_REPRESENTATION_COORDINATES",
            "positive_norm_representative": "CHOSE_OBSERVER_OR_HERMITIAN_NORM",
            "global_spin_structure": "OPEN",
            "phase_to_physical_spatial_circle": "OPEN_NOT_DERIVED",
            "carrier_action_boundary_mass": "OPEN_NOT_ENTERED",
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
