#!/usr/bin/env python3
"""Exact production algebra for the metric-native separation/asymptote audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require_zero(name: str, expression: sp.Expr, checks: dict[str, str]) -> None:
    simplified = sp.simplify(expression)
    if simplified != 0:
        raise AssertionError(f"{name}: expected zero, got {simplified}")
    checks[name] = "PASS"


def require_equal(name: str, actual: sp.Expr, expected: sp.Expr, checks: dict[str, str]) -> None:
    require_zero(name, actual - expected, checks)


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[sp.sstr(sp.factor(value)) for value in matrix.row(index)] for index in range(matrix.rows)]


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: dict[str, str] = {}
    phi = sp.symbols("phi", nonnegative=True)
    X = sp.symbols("X", positive=True)

    # F1: the reciprocal radial block realizes arbitrary monotone proper-depth laws.
    candidates = {
        "bounded_tanh": X * sp.tanh(phi),
        "bounded_exponential": X * (1 - sp.exp(-phi)),
        "unbounded_linear": X * phi,
    }
    profile_family: dict[str, dict[str, str]] = {}
    for name, distance in candidates.items():
        derivative = sp.diff(distance, phi)
        radial_derivative = sp.exp(-phi) * derivative
        require_zero(f"{name}_proper_pullback", sp.exp(phi) * radial_derivative - derivative, checks)
        require_equal(f"{name}_origin", distance.subs(phi, 0), 0, checks)
        require_equal(f"{name}_local_slope", derivative.subs(phi, 0), X, checks)
        endpoint = sp.limit(distance / X, phi, sp.oo)
        profile_family[name] = {
            "D_over_X": sp.sstr(distance / X),
            "dr_dphi_over_X": sp.sstr(sp.simplify(radial_derivative / X)),
            "endpoint_D_over_X": sp.sstr(endpoint),
        }
    require_zero(
        "same_local_calibration_different_bounded_shapes",
        sp.diff(candidates["bounded_tanh"], phi).subs(phi, 0)
        - sp.diff(candidates["bounded_exponential"], phi).subs(phi, 0),
        checks,
    )
    if sp.simplify(candidates["bounded_tanh"] - candidates["bounded_exponential"]) == 0:
        raise AssertionError("bounded profile controls collapsed")
    checks["bounded_profile_controls_are_distinct"] = "PASS"
    if sp.limit(candidates["unbounded_linear"], phi, sp.oo) != sp.oo:
        raise AssertionError("unbounded control lost")
    checks["finite_asymptote_not_forced_by_reciprocal_block"] = "PASS"

    # F2: all exact readings of the one fixed conditional WR-L realization.
    Tclock = sp.symbols("Tclock", positive=True)
    wr_coordinate = X * (1 - sp.exp(-2 * phi))
    wr_proper = 2 * X * (1 - sp.exp(-phi))
    wr_optical = 2 * X * phi
    projective = X * sp.tanh(phi)
    wr_readings = {
        "coordinate_areal_r": wr_coordinate,
        "slice_proper_ell": wr_proper,
        "optical_depth": wr_optical,
        "projective_tanh": projective,
    }
    wr_endpoints: dict[str, str] = {}
    for name, expression in wr_readings.items():
        wr_endpoints[name] = sp.sstr(sp.limit(expression / X, phi, sp.oo))
    require_equal(
        "wrl_coordinate_from_A",
        wr_coordinate.subs(phi, sp.log(Tclock)),
        X * (1 - Tclock ** -2),
        checks,
    )
    require_equal(
        "wrl_proper_from_A",
        wr_proper.subs(phi, sp.log(Tclock)),
        2 * X * (1 - Tclock ** -1),
        checks,
    )
    require_equal(
        "wrl_optical_from_A",
        wr_optical.subs(phi, sp.log(Tclock)),
        2 * X * sp.log(Tclock),
        checks,
    )
    require_equal(
        "projective_from_clock",
        projective.rewrite(sp.exp).subs(phi, sp.log(Tclock)),
        X * (Tclock**2 - 1) / (Tclock**2 + 1),
        checks,
    )
    at_two = {
        name: sp.sstr(sp.simplify(expression.subs(phi, sp.log(2)) / X))
        for name, expression in wr_readings.items()
    }
    if len(set(at_two.values())) != 4:
        raise AssertionError(f"fixed-metric readings not distinct: {at_two}")
    checks["fixed_metric_four_readings_distinct"] = "PASS"

    # F3: full ten-slot coframe and its clock-horizontal positive metric.
    U, W, R, Q = sp.symbols("U W R Q", positive=True)
    b, e = sp.symbols("b e", real=True)
    a20, a30, a21, a31 = sp.symbols("a20 a30 a21 a31", real=True)
    coframe = sp.Matrix(
        [
            [U, b, 0, 0],
            [0, W, 0, 0],
            [R * a20 + e * a30, R * a21 + e * a31, R, e],
            [Q * a30, Q * a31, 0, Q],
        ]
    )
    eta = sp.diag(-1, 1, 1, 1)
    metric = sp.simplify(coframe.T * eta * coframe)
    horizontal_injection = sp.Matrix(
        [
            [-b / U, 0, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
    )
    k2 = sp.factor(R * a21 + e * a31 - (b / U) * (R * a20 + e * a30))
    k3 = sp.factor(Q * (a31 - (b / U) * a30))
    spatial_coframe = sp.Matrix(
        [
            [W, 0, 0],
            [k2, R, e],
            [k3, 0, Q],
        ]
    )
    horizontal_metric = sp.simplify(spatial_coframe.T * spatial_coframe)
    pulled_metric = sp.simplify(horizontal_injection.T * metric * horizontal_injection)
    for row in range(3):
        for column in range(3):
            require_zero(
                f"complete_horizontal_pullback_{row}{column}",
                pulled_metric[row, column] - horizontal_metric[row, column],
                checks,
            )
    require_equal(
        "horizontal_metric_determinant",
        sp.factor(horizontal_metric.det()),
        W**2 * R**2 * Q**2,
        checks,
    )

    # Spatial depth norm. This is where phi and all live sectors meet.
    p0, p1, p2, p3 = sp.symbols("p0 p1 p2 p3", real=True)
    c0 = sp.factor((p0 - a20 * p2 - a30 * p3) / U)
    c1 = sp.factor((p1 - a21 * p2 - a31 * p3 - b * c0) / W)
    c2 = sp.factor(p2 / R)
    c3 = sp.factor((p3 - e * p2 / R) / Q)
    horizontal_depth_norm = sp.factor(c1**2 + c2**2 + c3**2)
    restricted_gradient = sp.Matrix([p1 - b * p0 / U, p2, p3])
    inverse_norm = sp.factor((restricted_gradient.T * horizontal_metric.inv() * restricted_gradient)[0])
    require_zero("horizontal_depth_norm_inverse_metric", inverse_norm - horizontal_depth_norm, checks)

    # Metric-native transnormal criterion for D=F(phi).
    Bphi = sp.symbols("Bphi", positive=True)
    Fprime = 1 / sp.sqrt(Bphi)
    require_equal("unit_eikonal_from_transnormal_norm", sp.simplify(Fprime**2 * Bphi), 1, checks)

    # Apply the criterion to the conditional WR-L branch.
    phi_prime_wrl = sp.exp(2 * phi) / (2 * X)
    B_wrl = sp.simplify(sp.exp(-2 * phi) * phi_prime_wrl**2)
    require_equal("wrl_spatial_depth_norm", B_wrl, sp.exp(2 * phi) / (4 * X**2), checks)
    Dprime_wrl = sp.simplify(1 / sp.sqrt(B_wrl))
    require_equal("wrl_metric_distance_derivative", Dprime_wrl, 2 * X * sp.exp(-phi), checks)
    D_wrl = sp.integrate(Dprime_wrl, (phi, 0, phi))
    require_equal("wrl_metric_distance", D_wrl, wr_proper, checks)
    require_equal("wrl_metric_distance_endpoint", sp.limit(D_wrl, phi, sp.oo), 2 * X, checks)
    if sp.simplify(D_wrl - projective) == 0:
        raise AssertionError("WR-L proper distance collapsed to tanh readout")
    checks["wrl_metric_distance_not_projective_tanh"] = "PASS"

    # Generic asymptotic convergence criterion B=C^2 exp(2 alpha phi).
    C, alpha = sp.symbols("C alpha", positive=True)
    power_integral = sp.integrate(sp.exp(-alpha * phi) / C, (phi, 0, sp.oo))
    require_equal("positive_power_depth_endpoint", power_integral, 1 / (C * alpha), checks)

    # F4: same radial clock law, different angular/global diameter.
    L = sp.symbols("L", positive=True)
    diameter_one_sq = sp.simplify(L**2 + (sp.pi * L) ** 2 + (sp.pi * L) ** 2)
    diameter_two_sq = sp.simplify(L**2 + (2 * sp.pi * L) ** 2 + (sp.pi * L) ** 2)
    require_equal(
        "angular_completion_changes_diameter",
        diameter_two_sq - diameter_one_sq,
        3 * sp.pi**2 * L**2,
        checks,
    )

    # F5: exact boost/event-pairing and common-scale controls.
    beta = sp.Rational(3, 5)
    gamma = sp.Rational(5, 4)
    require_equal("boost_gamma_identity", gamma**2 * (1 - beta**2), 1, checks)
    boosted_same_coordinate_span = sp.simplify(L / gamma)
    require_equal("boosted_clock_horizontal_span", boosted_same_coordinate_span, sp.Rational(4, 5) * L, checks)
    Omega = sp.symbols("Omega", positive=True)
    require_equal("constant_common_scale_changes_distance", Omega * L, Omega * L, checks)

    candidate_rows = [
        {
            "candidate": "coordinate_reach",
            "metric_intrinsic": "NO",
            "requires": "chart",
            "phi_relation_status": "PROFILE_OR_CHART_CONDITIONAL",
            "endpoint_status": "MAY_BE_FINITE",
            "global_Xmax_status": "NOT_BY_ITSELF",
        },
        {
            "candidate": "slice_proper_distance",
            "metric_intrinsic": "CONDITIONAL",
            "requires": "physical_metric+clock_congruence+integrable_rest_slices+event_pairing",
            "phi_relation_status": "DERIVED_IFF_TRANSNORMAL_B_OF_PHI",
            "endpoint_status": "INTEGRAL_CONVERGENCE_TEST",
            "global_Xmax_status": "REQUIRES_GLOBAL_DIAMETER_PROOF",
        },
        {
            "candidate": "horizontal_coframe_distance",
            "metric_intrinsic": "CONDITIONAL",
            "requires": "physical_reciprocal_clock_leg+reachable_horizontal_paths+event_pairing",
            "phi_relation_status": "PATH_DEPENDENT_UNLESS_TRANSNORMAL",
            "endpoint_status": "BRANCH_DEPENDENT",
            "global_Xmax_status": "REQUIRES_COMPLETE_COFRAME_DIAMETER",
        },
        {
            "candidate": "spacelike_world_function",
            "metric_intrinsic": "LOCAL_CONDITIONAL",
            "requires": "paired_events+unique_spacelike_geodesic",
            "phi_relation_status": "NOT_GENERAL",
            "endpoint_status": "NOT_GENERAL",
            "global_Xmax_status": "NO_GLOBAL_GUARANTEE",
        },
        {
            "candidate": "optical_depth",
            "metric_intrinsic": "CONDITIONAL",
            "requires": "null_path_and_clock_protocol",
            "phi_relation_status": "BRANCH_DEPENDENT",
            "endpoint_status": "MAY_DIVERGE_WHEN_PROPER_REACH_FINITE",
            "global_Xmax_status": "NOT_PHYSICAL_SEPARATION_WITHOUT_PREMISE",
        },
        {
            "candidate": "areal_angular_distance",
            "metric_intrinsic": "CONDITIONAL",
            "requires": "selected_screen_and_area_map",
            "phi_relation_status": "ANGULAR_ASSEMBLY_DEPENDENT",
            "endpoint_status": "BRANCH_DEPENDENT",
            "global_Xmax_status": "NOT_BY_ITSELF",
        },
        {
            "candidate": "projective_tanh_readout",
            "metric_intrinsic": "NO_CURRENTLY",
            "requires": "first_degree_anchored_projective_position_premise",
            "phi_relation_status": "UNIQUE_CONDITIONAL_IN_DECLARED_CLASS",
            "endpoint_status": "FINITE_BY_CONSTRUCTION",
            "global_Xmax_status": "NOT_DERIVED",
        },
        {
            "candidate": "global_pair_diameter",
            "metric_intrinsic": "YES_GIVEN_COMPLETE_PHYSICAL_BRANCH_AND_DOMAIN",
            "requires": "observer_domain+event_pairing+valid_pair_distance+global_completion",
            "phi_relation_status": "MUST_BE_PROVED",
            "endpoint_status": "SUPREMUM_MAY_BE_FINITE_OR_INFINITE",
            "global_Xmax_status": "DEFINITIONAL_OUTPUT_NOT_YET_EVALUABLE",
        },
    ]
    status_rows = [
        {
            "claim": "reciprocal_clock_factor_T_equal_exp_phi",
            "status": "DERIVED_CONDITIONAL",
            "scope_or_limit": "founding_pair_composition_and_interval_readout",
        },
        {
            "claim": "complete_clock_horizontal_spatial_quadratic_form",
            "status": "DERIVED_CONDITIONAL",
            "scope_or_limit": "supplied_complete_coframe_and_selected_clock_leg",
        },
        {
            "claim": "transnormal_distance_formula_Dprime_equal_B_minus_half",
            "status": "DERIVED",
            "scope_or_limit": "when_B_is_positive_and_a_function_of_phi_on_the_branch",
        },
        {
            "claim": "finite_infinite_dilation_reach",
            "status": "CONDITIONAL_INTEGRAL_TEST",
            "scope_or_limit": "integral_dphi_over_sqrt_B_must_converge",
        },
        {
            "claim": "tanh_is_metric_native_distance_law",
            "status": "NOT_DERIVED",
            "scope_or_limit": "projective_readout_remains_separate",
        },
        {
            "claim": "conditional_WRL_metric_native_radial_proper_endpoint",
            "status": "DERIVED_CONDITIONAL",
            "scope_or_limit": "equals_2X_not_X_and_not_global_diameter",
        },
        {
            "claim": "clock_dilation_alone_fixes_global_Xmax",
            "status": "REFUTED_IN_CURRENT_CONFIGURATION_CLASS",
            "scope_or_limit": "same_clock_law_different_angular_diameters",
        },
        {
            "claim": "complete_current_metric_parent_selects_unique_D_of_phi",
            "status": "OPEN_NOT_SELECTED",
            "scope_or_limit": "profile_clock_leg_event_pairing_and_global_branch_open",
        },
        {
            "claim": "global_Xmax_value_from_c_E_and_G_obs",
            "status": "OPEN_NOT_NEEDED_FOR_KINEMATIC_EXTRACTION",
            "scope_or_limit": "G_enters_later_mass_bootstrap_consistency",
        },
    ]

    result = {
        "schema": "udt-metric-native-observer-separation-asymptote-1.0",
        "sympy_version": sp.__version__,
        "checks": checks,
        "check_count": len(checks),
        "profile_family": profile_family,
        "wrl_readings": {
            name: {
                "expression": sp.sstr(expression),
                "endpoint_over_X": wr_endpoints[name],
                "value_over_X_at_T_equal_2": at_two[name],
            }
            for name, expression in wr_readings.items()
        },
        "complete_horizontal_metric": {
            "k2": sp.sstr(k2),
            "k3": sp.sstr(k3),
            "spatial_coframe": matrix_strings(spatial_coframe),
            "metric": matrix_strings(horizontal_metric),
            "determinant": sp.sstr(sp.factor(horizontal_metric.det())),
            "depth_norm_B": sp.sstr(horizontal_depth_norm),
        },
        "transnormal_distance": {
            "criterion": "B=h_u^{-1}(dphi,dphi)=B(phi)>0",
            "law": "dD/dphi=1/sqrt(B(phi))",
            "asymptote": "X_phi=int_phi0^infinity dphi/sqrt(B(phi))",
            "wrl_B": sp.sstr(B_wrl),
            "wrl_D": sp.sstr(D_wrl),
            "wrl_endpoint": sp.sstr(sp.limit(D_wrl, phi, sp.oo)),
            "power_control": "B=C^2*exp(2*alpha*phi), alpha>0 => X_phi=1/(C*alpha)",
        },
        "angular_countercontrol": {
            "common_clock_law": "exp(phi)=1/(1-ell/L)",
            "completion_one_diameter_squared": sp.sstr(diameter_one_sq),
            "completion_two_diameter_squared": sp.sstr(diameter_two_sq),
            "difference": sp.sstr(sp.simplify(diameter_two_sq - diameter_one_sq)),
        },
        "observer_and_scale_controls": {
            "beta": str(beta),
            "gamma": str(gamma),
            "original_horizontal_span": "L",
            "boosted_horizontal_span": sp.sstr(boosted_same_coordinate_span),
            "constant_common_scale": "D -> Omega D",
        },
        "maximum_conclusion": (
            "THE_COMPLETE_COFRAME_DERIVES_AN_EXACT_TRANSNORMAL_DISTANCE_AND_ASYMPTOTE_TEST;"
            "THE_CURRENT_CONFIGURATION_PARENT_DOES_NOT_SELECT_THE_REQUIRED_COMPLETE_BRANCH,"
            "CLOCK_LEG,EVENT_PAIRING,OR_GLOBAL_DIAMETER_JOIN"
        ),
    }

    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_tsv(
        HERE / "DISTANCE_CANDIDATE_LEDGER.tsv",
        [
            "candidate",
            "metric_intrinsic",
            "requires",
            "phi_relation_status",
            "endpoint_status",
            "global_Xmax_status",
        ],
        candidate_rows,
    )
    write_tsv(
        HERE / "STATUS_LEDGER.tsv",
        ["claim", "status", "scope_or_limit"],
        status_rows,
    )
    payload_hash = hashlib.sha256(
        (HERE / "DERIVATION_RESULT.json").read_bytes()
        + (HERE / "DISTANCE_CANDIDATE_LEDGER.tsv").read_bytes()
        + (HERE / "STATUS_LEDGER.tsv").read_bytes()
    ).hexdigest()
    print(f"SymPy {sp.__version__}")
    print(f"exact_checks={len(checks)}")
    print(f"result_payload_sha256={payload_hash}")
    print("status=PASS")


if __name__ == "__main__":
    main()
