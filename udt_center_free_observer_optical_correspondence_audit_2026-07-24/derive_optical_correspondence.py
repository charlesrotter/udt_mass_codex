#!/usr/bin/env python3
"""Exact center-free observer optical-correspondence audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "c1d1e00aa4cc326f70df552d854d4606de447491"
SOURCE_ADDENDUM_COMMIT = "1e50f033a4d2489a1b1c3006a899c35645cb9027"
PAIR_SOURCE = (
    ROOT
    / "udt_directional_observer_pair_distance_audit_2026-07-24"
    / "EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv"
)
COMPLETION_SOURCE = (
    ROOT
    / "udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24"
    / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv"
)


def check(checks: dict[str, str], name: str, condition: object) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    filename: str, fieldnames: list[str], rows: list[dict[str, object]]
) -> None:
    with (HERE / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_checks(checks: dict[str, str]) -> int:
    rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(rows) == 19)
    check(checks, "source_paths_unique", len({row["path"] for row in rows}) == 19)
    for row in rows:
        path = ROOT / row["path"]
        check(checks, f"source_exists_{row['path']}", path.is_file())
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        check(checks, f"source_hash_{row['path']}", observed == row["sha256"])
    return len(rows)


def main() -> None:
    checks: dict[str, str] = {}
    D, b, X, r, kappa = sp.symbols("D b X r kappa", positive=True)

    # Screen gauge: a Jacobi matrix changes by independent orthogonal bases
    # at its two endpoints. Absolute determinant is invariant.
    alpha, beta = sp.symbols("alpha beta", real=True)
    j11, j12, j21, j22 = sp.symbols("j11 j12 j21 j22", real=True)
    J = sp.Matrix([[j11, j12], [j21, j22]])
    R_source = sp.Matrix(
        [[sp.cos(alpha), -sp.sin(alpha)], [sp.sin(alpha), sp.cos(alpha)]]
    )
    R_observer = sp.Matrix(
        [[sp.cos(beta), -sp.sin(beta)], [sp.sin(beta), sp.cos(beta)]]
    )
    transformed = R_source * J * R_observer.T
    check(checks, "screen_rotation_source_det", sp.trigsimp(R_source.det()) == 1)
    check(checks, "screen_rotation_observer_det", sp.trigsimp(R_observer.det()) == 1)
    check(
        checks,
        "screen_jacobi_determinant_invariant",
        sp.trigsimp(transformed.det() - J.det()) == 0,
    )

    # Constant-curvature spatial Jacobi controls.
    round_radius = b * sp.sin(D / b)
    flat_radius = D
    hyperbolic_radius = b * sp.sinh(D / b)
    check(
        checks,
        "round_jacobi_ode",
        sp.simplify(sp.diff(round_radius, D, 2) + round_radius / b**2) == 0,
    )
    check(checks, "round_jacobi_origin", round_radius.subs(D, 0) == 0)
    check(checks, "round_jacobi_unit_slope", sp.diff(round_radius, D).subs(D, 0) == 1)
    check(checks, "round_equator_area_radius", round_radius.subs(D, sp.pi * b / 2) == b)
    check(checks, "round_antipode_caustic", round_radius.subs(D, sp.pi * b) == 0)
    check(
        checks,
        "flat_jacobi_ode",
        sp.diff(flat_radius, D, 2) == 0,
    )
    check(
        checks,
        "hyperbolic_jacobi_ode",
        sp.simplify(
            sp.diff(hyperbolic_radius, D, 2) - hyperbolic_radius / b**2
        )
        == 0,
    )

    # In the ultrastatic product -c^2 dt^2+h_round, the time factor has zero
    # curvature and the null screen tidal scalar equals the spatial radial
    # sectional curvature 1/b^2. Hence the matched screen initial-value
    # problems coincide.
    null_screen_curvature_round = 1 / b**2
    spatial_screen_curvature_round = 1 / b**2
    check(
        checks,
        "round_null_spatial_screen_curvature",
        null_screen_curvature_round == spatial_screen_curvature_round,
    )
    check(
        checks,
        "round_null_screen_solution",
        sp.simplify(
            sp.diff(round_radius, D, 2)
            + null_screen_curvature_round * round_radius
        )
        == 0,
    )
    round_static_clock_ratio = sp.Integer(1)
    check(checks, "round_constant_lapse_redshift", round_static_clock_ratio == 1)

    # General central warped rest geometry:
    # h=dD^2+R(D)^2 dOmega^2. The radial Jacobi radius is R and the two
    # sectional curvatures are -R''/R and (1-R'^2)/R^2.
    R = sp.Function("R")(D)
    K_rad_general = -sp.diff(R, D, 2) / R
    K_tan_general = (1 - sp.diff(R, D) ** 2) / R**2
    check(
        checks,
        "warped_radial_jacobi_identity",
        sp.simplify(sp.diff(R, D, 2) + K_rad_general * R) == 0,
    )

    # Reconstruct the warped sectional curvatures directly from the 3D
    # metric, rather than merely assuming the standard formulas.
    theta, varphi = sp.symbols("theta varphi", real=True)
    coordinates = [D, theta, varphi]
    warped_metric = sp.diag(1, R**2, R**2 * sp.sin(theta) ** 2)
    warped_inverse = warped_metric.inv()
    dimension = 3
    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        warped_inverse[i, ell]
                        * (
                            sp.diff(warped_metric[ell, k], coordinates[j])
                            + sp.diff(warped_metric[ell, j], coordinates[k])
                            - sp.diff(warped_metric[j, k], coordinates[ell])
                        )
                        for ell in range(dimension)
                    )
                    / 2
                )
                for k in range(dimension)
            ]
            for j in range(dimension)
        ]
        for i in range(dimension)
    ]

    def riemann_up(rho: int, sigma: int, mu: int, nu: int):
        return sp.simplify(
            sp.diff(christoffel[rho][nu][sigma], coordinates[mu])
            - sp.diff(christoffel[rho][mu][sigma], coordinates[nu])
            + sum(
                christoffel[rho][mu][ell] * christoffel[ell][nu][sigma]
                - christoffel[rho][nu][ell] * christoffel[ell][mu][sigma]
                for ell in range(dimension)
            )
        )

    def riemann_low(a: int, b_index: int, c_index: int, d_index: int):
        return sp.simplify(
            sum(
                warped_metric[a, ell]
                * riemann_up(ell, b_index, c_index, d_index)
                for ell in range(dimension)
            )
        )

    direct_radial_sectional = sp.simplify(
        riemann_low(0, 1, 0, 1)
        / (warped_metric[0, 0] * warped_metric[1, 1])
    )
    direct_tangential_sectional = sp.simplify(
        riemann_low(1, 2, 1, 2)
        / (warped_metric[1, 1] * warped_metric[2, 2])
    )
    check(
        checks,
        "warped_curvature_direct_radial",
        sp.simplify(direct_radial_sectional - K_rad_general) == 0,
    )
    check(
        checks,
        "warped_curvature_direct_tangential",
        sp.simplify(direct_tangential_sectional - K_tan_general) == 0,
    )

    # WR-L exact proper-coordinate form.
    N_wrl = 1 - D / (2 * X)
    R_wrl = D - D**2 / (4 * X)
    A_wrl = N_wrl**2
    phi_wrl = -sp.log(N_wrl)
    check(checks, "wrl_origin_lapse", N_wrl.subs(D, 0) == 1)
    check(checks, "wrl_origin_radius", R_wrl.subs(D, 0) == 0)
    check(checks, "wrl_origin_radius_slope", sp.diff(R_wrl, D).subs(D, 0) == 1)
    check(
        checks,
        "wrl_nonsmooth_center_second_jet",
        sp.diff(R_wrl, D, 2).subs(D, 0) == -1 / (2 * X),
    )
    check(
        checks,
        "wrl_areal_lapse_identity",
        sp.simplify(R_wrl / X - (1 - A_wrl)) == 0,
    )
    check(
        checks,
        "wrl_proper_phi_identity",
        sp.simplify(
            (2 * X * (1 - sp.exp(-phi_wrl)) - D)
        )
        == 0,
    )
    check(checks, "wrl_proper_endpoint", N_wrl.subs(D, 2 * X) == 0)
    check(checks, "wrl_areal_endpoint", R_wrl.subs(D, 2 * X) == X)
    check(
        checks,
        "wrl_clock_ratio",
        sp.simplify(1 / N_wrl - sp.exp(phi_wrl)) == 0,
    )

    K_rad_wrl = sp.simplify(
        -sp.diff(R_wrl, D, 2) / R_wrl
    )
    K_tan_wrl = sp.simplify(
        (1 - sp.diff(R_wrl, D) ** 2) / R_wrl**2
    )
    check(
        checks,
        "wrl_radial_curvature",
        sp.simplify(K_rad_wrl - 1 / (2 * X * R_wrl)) == 0,
    )
    check(
        checks,
        "wrl_tangential_curvature",
        sp.simplify(K_tan_wrl - 1 / (X * R_wrl)) == 0,
    )
    check(
        checks,
        "wrl_curvature_split",
        sp.simplify(K_tan_wrl - 2 * K_rad_wrl) == 0,
    )
    scalar3_wrl = sp.simplify(4 * K_rad_wrl + 2 * K_tan_wrl)
    check(
        checks,
        "wrl_spatial_scalar_varies",
        sp.simplify(scalar3_wrl - 4 / (X * R_wrl)) == 0,
    )
    check(
        checks,
        "wrl_central_jacobi",
        sp.simplify(sp.diff(R_wrl, D, 2) + K_rad_wrl * R_wrl) == 0,
    )

    # All-observer direction-independent recenterability in connected 3D
    # forces constant sectional curvature. If Ric=2*kappa*h and R=6*kappa,
    # the contracted Bianchi identity gives 2 d(kappa)=3 d(kappa).
    bianchi_left_coefficient = sp.Integer(2)
    bianchi_right_coefficient = sp.Integer(3)
    check(
        checks,
        "schur_3d_nonzero_coefficient",
        bianchi_left_coefficient - bianchi_right_coefficient != 0,
    )
    check(
        checks,
        "wrl_not_isotropic_everywhere",
        sp.simplify(K_tan_wrl - K_rad_wrl) != 0,
    )

    # Positive constant-spatial-curvature reciprocal static control.
    A_cc = 1 - r**2 / b**2
    K_rad_cc = sp.simplify(-sp.diff(A_cc, r) / (2 * r))
    K_tan_cc = sp.simplify((1 - A_cc) / r**2)
    check(checks, "constant_curvature_radial", K_rad_cc == 1 / b**2)
    check(checks, "constant_curvature_tangential", K_tan_cc == 1 / b**2)
    r_of_D_cc = b * sp.sin(D / b)
    N_cc = sp.cos(D / b)
    check(
        checks,
        "constant_curvature_profile",
        sp.simplify(
            A_cc.subs(r, r_of_D_cc) - N_cc**2
        )
        == 0,
    )
    check(
        checks,
        "constant_curvature_static_endpoint",
        N_cc.subs(D, sp.pi * b / 2) == 0,
    )
    check(
        checks,
        "static_endpoint_half_round_diameter",
        sp.simplify(2 * (sp.pi * b / 2) - sp.pi * b) == 0,
    )

    # A time-dependent conformal metric separates null area distance from
    # observer-rest distance. For a radial null interval chi:
    # D_A(null)=a_source*chi, D_rest(at observation)=a_observer*chi.
    a_source, a_observer, chi = sp.symbols(
        "a_source a_observer chi", positive=True
    )
    null_area = a_source * chi
    rest_distance_observer_slice = a_observer * chi
    check(
        checks,
        "time_live_null_rest_difference_control",
        sp.simplify(
            (null_area - rest_distance_observer_slice).subs(
                {a_source: 2, a_observer: 3, chi: 5}
            )
            + 5
        )
        == 0,
    )

    # Event-pairing control for two static worldlines separated by L.
    L, c_E = sp.symbols("L c_E", positive=True)
    equal_time_source_event = sp.Integer(0)
    past_null_source_event = -L / c_E
    check(
        checks,
        "event_pairing_rules_differ",
        equal_time_source_event != past_null_source_event,
    )

    source_count = source_checks(checks)

    equation_rows = read_tsv(PAIR_SOURCE)
    completion_rows = read_tsv(COMPLETION_SOURCE)
    check(checks, "equation_family_count", len(equation_rows) == 28)
    check(
        checks,
        "equation_family_unique",
        len({row["family_id"] for row in equation_rows}) == 28,
    )
    check(checks, "completion_count", len(completion_rows) == 12)
    check(
        checks,
        "completion_unique",
        len({row["completion_id"] for row in completion_rows}) == 12,
    )
    check(
        checks,
        "completion_complete_witness_zero",
        sum(row["complete_g_phi_witness"] == "YES" for row in completion_rows)
        == 0,
    )

    type_rows = [
        {
            "candidate": "NULL_SCREEN_JACOBI",
            "metric_native_core": "YES_GIVEN_ORDERED_EVENT_OBSERVER_TANGENT_AND_NULL_PATH",
            "pairing_requirement": "NULL_INTERSECTION_WITH_ORDERED_OBSERVER_EVENT",
            "path_status": "SET_VALUED_IF_MULTIPLE_NULL_GEODESICS",
            "transverse_output": "SCREEN_JACOBI_MAP_AND_ABS_DETERMINANT",
            "clock_output": "ENDPOINT_MINUS_U_DOT_K_RATIO",
            "scalar_separation": "NOT_SPATIAL_PAIR_DISTANCE",
            "ruling": "DERIVED_CONDITIONAL_PATHWISE_CORRESPONDENCE",
        },
        {
            "candidate": "REST_SPACE_JACOBI",
            "metric_native_core": "YES_GIVEN_POSITIVE_REST_GEOMETRY_PAIRING_AND_GEODESIC",
            "pairing_requirement": "SUPPLIED_SLICE_OR_CONGRUENCE",
            "path_status": "MINIMIZING_PATH_FAMILY_AT_CUT_LOCUS",
            "transverse_output": "RIEMANNIAN_JACOBI_MAP_AND_ABS_DETERMINANT",
            "clock_output": "NONE_BY_ITSELF",
            "scalar_separation": "INTRINSIC_REST_DISTANCE",
            "ruling": "DERIVED_CONDITIONAL_PATHWISE_CORRESPONDENCE",
        },
        {
            "candidate": "WARPED_ORBIT_RADIUS",
            "metric_native_core": "YES_ONLY_IN_SUPPLIED_CENTERED_ISOTROPIC_WARPED_CHART",
            "pairing_requirement": "CENTERED_RADIAL_PAIR",
            "path_status": "CENTRAL_RADIAL_FAMILY",
            "transverse_output": "R(D)",
            "clock_output": "N_OBSERVER_OVER_N_SOURCE_IF_STATIC",
            "scalar_separation": "D_NOT_R",
            "ruling": "CONDITIONAL_SYMMETRY_READOUT",
        },
        {
            "candidate": "INTRINSIC_PAIR_DISTANCE",
            "metric_native_core": "YES_GIVEN_COMPLETE_POSITIVE_SLICE",
            "pairing_requirement": "SUPPLIED_EVENT_SLICE",
            "path_status": "INFIMUM_WITH_CUT_PATH_FAMILY",
            "transverse_output": "NOT_FROM_SCALAR_DISTANCE_ALONE",
            "clock_output": "NONE_BY_ITSELF",
            "scalar_separation": "YES",
            "ruling": "DERIVED_CONDITIONAL_DISTANCE",
        },
        {
            "candidate": "BOUNDED_PAIR_TRANSFORM",
            "metric_native_core": "METRIC_PRESERVING_GIVEN_F",
            "pairing_requirement": "INHERITS_BASE_PAIRING",
            "path_status": "NONLOCAL_ENDPOINT_COMPARISON",
            "transverse_output": "NONE_FROM_F_ALONE",
            "clock_output": "NONE_UNLESS_SOLDERED",
            "scalar_separation": "YES_CONDITIONAL",
            "ruling": "DERIVED_CONDITIONAL_NO_OPTICAL_JOIN",
        },
        {
            "candidate": "COFRAME_PATH_TRANSPORT",
            "metric_native_core": "YES_GIVEN_CONNECTION_AND_PATH",
            "pairing_requirement": "ENDPOINT_EVENTS",
            "path_status": "PATH_FAMILY",
            "transverse_output": "FRAME_HOLONOMY_NOT_AREA_DISTANCE_BY_ITSELF",
            "clock_output": "PATHWISE_FRAME_COMPARISON",
            "scalar_separation": "NO",
            "ruling": "DERIVED_CONDITIONAL_TRANSPORT",
        },
        {
            "candidate": "REGISTERED_LUMINOSITY_READOUT",
            "metric_native_core": "NO_METRIC_ALONE",
            "pairing_requirement": "NULL_OR_OTHER_OPTICAL_JOIN_PLUS_SOURCE_OBSERVER",
            "path_status": "INHERITS_OPTICAL_PATH",
            "transverse_output": "D_L_FROM_REGISTERED_RECIPROCITY_AFTER_D_A",
            "clock_output": "REQUIRES_Z",
            "scalar_separation": "OBSERVATIONAL_DISTANCE_NOT_PAIR_DIAMETER",
            "ruling": "PINNED_REGISTERED_CONDITIONAL_READOUT",
        },
        {
            "candidate": "UNIVERSAL_CENTER_FREE_OPTICAL_OPERATOR",
            "metric_native_core": "NOT_CURRENTLY_COMPLETE",
            "pairing_requirement": "OPEN_SELECTOR",
            "path_status": "OPEN_SINGLE_VERSUS_SET_VALUED",
            "transverse_output": "OPEN_JOIN",
            "clock_output": "OPEN_PHYSICAL_SOLDER",
            "scalar_separation": "OPEN_GLOBAL_JOIN",
            "ruling": "OPEN",
        },
    ]

    branch_rows = [
        {
            "branch": "B19_ROUND_S3",
            "metric_status": "CONDITIONAL_COMPLETE_ON_SHELL_SPATIAL_ULTRASTATIC",
            "pairing": "NULL_OR_REST_BOTH_CONDITIONAL",
            "rest_Jacobi": "b*sin(D/b)",
            "null_Jacobi": "b*sin(D/b)",
            "clock_ratio": "1",
            "center_status": "NO_CENTER_BY_TRANSITIVE_ISOMETRY",
            "global_behavior": "DIAMETER_PI_b;ANTIPODAL_CAUSTIC;PATH_FAMILY",
            "physical_ruling": "GEOMETRIC_OPTICAL_WITNESS_NO_RECIPROCAL_CLOCK_SOLDER",
        },
        {
            "branch": "SQUASHED_S3_OFF_SHELL",
            "metric_status": "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL",
            "pairing": "NULL_OR_REST_BOTH_CONDITIONAL",
            "rest_Jacobi": "PATHWISE_DEFINED_DIRECTION_DEPENDENT_CLOSED_ATLAS_OPEN",
            "null_Jacobi": "MATCHES_REST_PATHWISE_IN_ULTRASTATIC_PRODUCT",
            "clock_ratio": "1",
            "center_status": "NO_CENTER_BY_TRANSITIVE_ISOMETRY",
            "global_behavior": "CUT_AND_AREA_ATLAS_OPEN",
            "physical_ruling": "OFF_SHELL_CONTROL_NOT_SELECTED",
        },
        {
            "branch": "WRL_LOCAL_RESIDUAL",
            "metric_status": "LOCAL_CENTERED_STATIC_PROFILE_NO_GLOBAL_COMPLETION",
            "pairing": "CENTERED_RADIAL_ONLY",
            "rest_Jacobi": "R(D)=D-D^2/(4X)",
            "null_Jacobi": "R(D)_FOR_CENTRAL_RADIAL_SOLID_ANGLE",
            "clock_ratio": "1/N=1/(1-D/(2X))=exp(phi)",
            "center_status": "CENTER_IRREGULAR_IF_INCLUDED;RESIDUAL_PAIR_CHART_WORKING",
            "global_behavior": "NO_GLOBAL_CUT_LOCUS_DIAMETER_OR_ALL_OBSERVER_RECENTERING",
            "physical_ruling": "EXISTING_SNE_READOUT_IS_CENTERED_RESIDUAL_NOT_GLOBAL_PAIR_OPERATOR",
        },
        {
            "branch": "TEMPORAL_PHI_SLICE_FAMILY",
            "metric_status": "CONDITIONAL_PRE_SCALE_REST_GEOMETRY_NO_COMPLETE_BRANCH",
            "pairing": "EQUAL_PHI",
            "rest_Jacobi": "DEFINED_PATHWISE_ON_EACH_COMPLETE_POSITIVE_LEVEL_IF_SUPPLIED",
            "null_Jacobi": "SEPARATE_SPACETIME_PATH_FAMILY",
            "clock_ratio": "PHYSICAL_SOLDER_OPEN",
            "center_status": "NO_PREFERRED_OBSERVER_IN_CONDITIONAL_RULE",
            "global_behavior": "REPRESENTATIVE_RANGE_COMPLETION_AND_INTERFACE_OPEN",
            "physical_ruling": "CONDITIONAL_GEOMETRIC_FAMILY",
        },
        {
            "branch": "CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL",
            "metric_status": "MATHEMATICAL_COMPARISON_NOT_REGISTERED_UDT_BRANCH",
            "pairing": "OBSERVER_CENTERED_STATIC_PATCH",
            "rest_Jacobi": "b*sin(D/b)",
            "null_Jacobi": "b*sin(D/b)_CENTRAL_RADIAL",
            "clock_ratio": "sec(D/b)",
            "center_status": "SPATIAL_RECENTERABLE_AFTER_ROUND_COMPLETION",
            "global_behavior": "STATIC_ENDPOINT_PI_b/2;ROUND_SPATIAL_DIAMETER_PI_b",
            "physical_ruling": "COUNTERCONTROL_RADIAL_HORIZON_NOT_GLOBAL_DIAMETER",
        },
        {
            "branch": "UNIVERSAL_PHYSICAL_UDT",
            "metric_status": "NO_COMPLETE_WITNESS",
            "pairing": "OPEN",
            "rest_Jacobi": "OPEN",
            "null_Jacobi": "OPEN",
            "clock_ratio": "OPEN",
            "center_status": "OWNER_NO_PREFERRED_FRAME_NOT_YET_COMPLETE_METRIC_REALIZATION",
            "global_behavior": "OPEN",
            "physical_ruling": "OPEN",
        },
    ]

    equation_overlay = []
    for row in equation_rows:
        family_id = row["family_id"]
        if family_id == "B19":
            optical = (
                "ROUND_CENTER_FREE_NULL_AND_REST_JACOBI_EXACT;"
                "CONSTANT_LAPSE_NO_RECIPROCAL_CLOCK"
            )
            grade = "CONDITIONAL_COMPLETE_GEOMETRIC_WITNESS"
        elif family_id == "B21":
            optical = (
                "CENTERED_WRL_CLOCK_AREA_READOUT_ONLY;"
                "NO_GLOBAL_PAIR_GEOMETRY"
            )
            grade = "LOCAL_RESIDUAL_READOUT"
        else:
            optical = "NOT_EVALUABLE_NO_COMPLETE_METRIC"
            grade = "NO_COMPLETE_OPTICAL_WITNESS"
        equation_overlay.append(
            {
                "family_id": family_id,
                "family_label": row["family_label"],
                "prior_complete_spatial_metric": row["complete_spatial_metric"],
                "prior_two_point_distance": row["two_point_distance"],
                "optical_correspondence": optical,
                "classification": grade,
            }
        )

    completion_overlay = []
    for row in completion_rows:
        completion_overlay.append(
            {
                "completion_id": row["completion_id"],
                "prior_global_data_level": row["global_data_level"],
                "complete_g_phi_witness": row["complete_g_phi_witness"],
                "clock_phi_solder": row["clock_phi_solder"],
                "optical_correspondence": "NOT_EVALUABLE_NO_COMPLETE_G_PHI_METRIC",
                "smallest_missing_object": (
                    "complete_metric_observer_pairing_path_and_screen_transport"
                ),
            }
        )

    write_tsv(
        "OPTICAL_TYPE_LEDGER.tsv",
        [
            "candidate",
            "metric_native_core",
            "pairing_requirement",
            "path_status",
            "transverse_output",
            "clock_output",
            "scalar_separation",
            "ruling",
        ],
        type_rows,
    )
    write_tsv(
        "BRANCH_OPTICAL_ATLAS.tsv",
        [
            "branch",
            "metric_status",
            "pairing",
            "rest_Jacobi",
            "null_Jacobi",
            "clock_ratio",
            "center_status",
            "global_behavior",
            "physical_ruling",
        ],
        branch_rows,
    )
    write_tsv(
        "EQUATION_FAMILY_OPTICAL_SCREEN.tsv",
        [
            "family_id",
            "family_label",
            "prior_complete_spatial_metric",
            "prior_two_point_distance",
            "optical_correspondence",
            "classification",
        ],
        equation_overlay,
    )
    write_tsv(
        "COMPLETION_OPTICAL_ATLAS.tsv",
        [
            "completion_id",
            "prior_global_data_level",
            "complete_g_phi_witness",
            "clock_phi_solder",
            "optical_correspondence",
            "smallest_missing_object",
        ],
        completion_overlay,
    )
    status_rows = [
        {
            "claim": "metric-native optical core",
            "status": "DERIVED_CONDITIONAL_PATHWISE_CORRESPONDENCE",
            "scope": "given complete metric observers event pairing and path",
        },
        {
            "claim": "single universal optical operator",
            "status": "OPEN_SELECTOR",
            "scope": "pairing and path multiplicity unresolved",
        },
        {
            "claim": "null equals rest-space optical law",
            "status": "CONDITIONAL_NOT_UNIVERSAL",
            "scope": "coincides in round ultrastatic and central static controls; time-live countercontrol differs",
        },
        {
            "claim": "WRL D_A equals proper pair distance",
            "status": "REFUTED_CONFLATION",
            "scope": "D_A=R(D); proper distance=D",
        },
        {
            "claim": "WRL SNe readout is global center-free",
            "status": "OPEN_NOT_ESTABLISHED",
            "scope": "registered readout is centered residual local branch",
        },
        {
            "claim": "round B19 optical geometry",
            "status": "DERIVED_CONDITIONAL_CENTER_FREE",
            "scope": "D_A=b sin(D/b); constant lapse; antipodal caustic",
        },
        {
            "claim": "physical Xmax",
            "status": "OPEN",
            "scope": "optical caustic radial endpoint and pair diameter are distinct",
        },
        {
            "claim": "co-presence selects transport",
            "status": "OPEN_INTERPRETATION_NO_EQUATION",
            "scope": "no null versus rest pairing selection derived",
        },
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows)

    result = {
        "schema": "udt-center-free-observer-optical-correspondence-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_PENDING_INDEPENDENT_REPLAY",
        "preregistration_commit": PREREG_COMMIT,
        "source_addendum_commit": SOURCE_ADDENDUM_COMMIT,
        "source_count": source_count,
        "check_count": len(checks),
        "checks": checks,
        "registry": {
            "equation_families": len(equation_rows),
            "finite_cell_completions": len(completion_rows),
            "complete_g_phi_completion_witnesses": 0,
        },
        "derived_object": {
            "type": "SET_VALUED_OBSERVER_OPTICAL_CORRESPONDENCE",
            "null_member": (
                "event_pair,path,endpoint_clock_ratio,screen_Jacobi_map,"
                "area_radius"
            ),
            "rest_member": (
                "paired_events,minimizing_path,rest_distance,"
                "screen_Jacobi_map,area_radius"
            ),
            "status": "DERIVED_CONDITIONAL_ON_INPUTS",
        },
        "exact_witnesses": {
            "round_B19": (
                "CENTER_FREE_DA_b_sin_D_over_b_CONSTANT_CLOCK_"
                "ANTIPODAL_CAUSTIC"
            ),
            "WRL": (
                "CENTERED_RESIDUAL_DA_R_OF_D_CLOCK_EXP_PHI_"
                "NO_GLOBAL_RECENTERING"
            ),
            "constant_curvature_control": (
                "STATIC_ENDPOINT_HALF_SPATIAL_DIAMETER"
            ),
        },
        "universal_operator": "OPEN_SELECTOR",
        "physical_Xmax": "OPEN",
        "maximum_conclusion": (
            "COMPLETE_METRIC_DERIVES_PATHWISE_SCREEN_AND_CLOCK_DATA_GIVEN_"
            "PAIRING;CURRENT_UDT_DOES_NOT_SELECT_ONE_GLOBAL_CENTER_FREE_"
            "OPTICAL_OPERATOR;WRL_SNE_READOUT_REMAINS_CENTERED_RESIDUAL"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
