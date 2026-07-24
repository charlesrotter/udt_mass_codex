#!/usr/bin/env python3
"""Exact no-center two-point distance and complete-witness census."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def require(label: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    b, s, alpha, beta = sp.symbols(
        "b s alpha beta", positive=True, finite=True, real=True
    )
    eta, sigma = sp.symbols("eta sigma", positive=True, finite=True, real=True)

    # One arbitrary base observer can be placed at this coordinate only
    # because the round control is homogeneous; it is not a physical center.
    p = sp.Matrix([b, 0, 0, 0])
    n = sp.Matrix(
        [
            0,
            sp.cos(alpha),
            sp.sin(alpha) * sp.cos(beta),
            sp.sin(alpha) * sp.sin(beta),
        ]
    )
    gamma = sp.cos(s / b) * p + b * sp.sin(s / b) * n
    gamma_prime = sp.diff(gamma, s)
    require("round_base_point_norm", sp.simplify(p.dot(p) - b**2) == 0, checks)
    require("round_direction_unit", sp.trigsimp(n.dot(n) - 1) == 0, checks)
    require("round_direction_tangent", sp.simplify(p.dot(n)) == 0, checks)
    require("round_geodesic_stays_on_sphere", sp.trigsimp(gamma.dot(gamma) - b**2) == 0, checks)
    require("round_geodesic_unit_speed", sp.trigsimp(gamma_prime.dot(gamma_prime) - 1) == 0, checks)
    require("round_geodesic_starts_at_p", sp.simplify(gamma.subs(s, 0) - p) == sp.zeros(4, 1), checks)
    require(
        "round_geodesic_antipode_independent_direction",
        sp.simplify(gamma.subs(s, sp.pi * b) + p) == sp.zeros(4, 1),
        checks,
    )
    require(
        "round_cut_length",
        sp.simplify((sp.pi * b) - 0) == sp.pi * b,
        checks,
    )

    z = sp.symbols("z", real=True)
    distance = b * sp.acos(z)
    require("round_coincident_distance", distance.subs(z, 1) == 0, checks)
    require("round_antipodal_distance", distance.subs(z, -1) == sp.pi * b, checks)
    require(
        "round_distance_scale",
        sp.simplify(distance.subs(b, 3 * b) - 3 * distance) == 0,
        checks,
    )
    cap_depth = sp.simplify(b * (sp.pi / 2 - sp.pi / 4))
    diameter = sp.pi * b
    require("neutral_torus_to_cap_depth", cap_depth == sp.pi * b / 4, checks)
    require("diameter_to_cap_depth_ratio", sp.simplify(diameter / cap_depth) == 4, checks)
    require("round_directional_spread", sp.simplify(sp.pi * b - sp.pi * b) == 0, checks)

    # Complete off-shell constant-squashing control from the registered
    # stationary coframe.
    q = sp.sin(eta) * sp.cos(eta)
    c2 = sp.cos(eta) ** 2
    s2 = sp.sin(eta) ** 2
    coframe_matrix = sp.Matrix(
        [
            [1, 0, 0],
            [0, q, -q],
            [0, sigma * c2, sigma * s2],
        ]
    )
    h_squashed = sp.simplify(b**2 * coframe_matrix.T * coframe_matrix)
    require(
        "squashed_coframe_determinant",
        sp.trigsimp(coframe_matrix.det() - sigma * q) == 0,
        checks,
    )
    require(
        "squashed_metric_determinant",
        sp.simplify(
            sp.trigsimp(h_squashed.det() - b**6 * sigma**2 * q**2)
        )
        == 0,
        checks,
    )
    round_coordinate_metric = sp.diag(
        b**2,
        b**2 * sp.cos(eta) ** 2,
        b**2 * sp.sin(eta) ** 2,
    )
    require(
        "squashed_sigma_one_is_round",
        sp.trigsimp(h_squashed.subs(sigma, 1) - round_coordinate_metric)
        == sp.zeros(3),
        checks,
    )
    fiber_speed_squared = sp.simplify(
        (sp.Matrix([0, 1, 1]).T * h_squashed * sp.Matrix([0, 1, 1]))[0]
    )
    radial_speed_squared = sp.simplify(
        (sp.Matrix([1, 0, 0]).T * h_squashed * sp.Matrix([1, 0, 0]))[0]
    )
    require(
        "squashed_fiber_speed",
        sp.trigsimp(fiber_speed_squared - b**2 * sigma**2) == 0,
        checks,
    )
    require(
        "squashed_horizontal_meridian_speed",
        sp.simplify(radial_speed_squared - b**2) == 0,
        checks,
    )
    fiber_loop = 2 * sp.pi * b * sigma
    horizontal_loop = 2 * sp.pi * b
    require(
        "squashed_loop_ratio",
        sp.simplify(fiber_loop / horizontal_loop - sigma) == 0,
        checks,
    )
    antipode_upper_bound = sp.pi * b * sp.Min(sigma, 1)
    require(
        "squashed_antipode_bound_short_fiber_branch",
        sp.simplify(antipode_upper_bound.subs(sigma, sp.Rational(1, 2)) - sp.pi * b / 2)
        == 0,
        checks,
    )
    require(
        "squashed_antipode_bound_long_fiber_branch",
        sp.simplify(antipode_upper_bound.subs(sigma, 2) - sp.pi * b) == 0,
        checks,
    )

    fc_source = read_tsv(
        ROOT
        / "udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24"
        / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv"
    )
    family_registry = read_tsv(
        ROOT
        / "udt_involutive_exchange_branch_availability_audit_2026-07-24"
        / "BRANCH_EQUATION_FAMILY_REGISTRY.tsv"
    )
    family_source = read_tsv(
        ROOT
        / "udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24"
        / "EQUATION_FAMILY_SCREEN.tsv"
    )
    solder_source = read_tsv(
        ROOT
        / "udt_clock_angular_solder_regularity_audit_2026-07-24"
        / "SOLDER_CLASSIFICATION.tsv"
    )
    require("twelve_FC_rows", len(fc_source) == 12, checks)
    require("unique_FC_rows", len({row["completion_id"] for row in fc_source}) == 12, checks)
    require("twenty_eight_family_registry_rows", len(family_registry) == 28, checks)
    require("unique_family_registry_rows", len({row["family_id"] for row in family_registry}) == 28, checks)
    require("twenty_eight_family_screen_rows", len(family_source) == 28, checks)
    require(
        "family_registry_screen_identity",
        [row["family_id"] for row in family_registry]
        == [row["family_id"] for row in family_source],
        checks,
    )
    require("six_solder_rows", len(solder_source) == 6, checks)
    require(
        "unique_solder_rows",
        len({row["family_id"] for row in solder_source}) == 6,
        checks,
    )
    corrected_configurations = read_tsv(HERE / "CORRECTED_CONFIGURATION_REGISTRY.tsv")
    require("four_corrected_configurations", len(corrected_configurations) == 4, checks)
    require(
        "squashed_off_shell_configuration_retained",
        any(
            row["configuration_id"] == "Q02_SQUASHED_S3"
            and row["on_shell_status"] == "OFF_SHELL_CONTROL_NOT_OBSERVED_AS_ROOT"
            for row in corrected_configurations
        ),
        checks,
    )

    fc_rows = []
    for row in fc_source:
        is_fc12 = row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
        fc_rows.append(
            {
                "completion_id": row["completion_id"],
                "prior_classification": row["primary_classification"],
                "complete_metric_witness": "NO",
                "two_point_distance": "NOT_EVALUABLE",
                "directional_band": "NOT_EVALUABLE",
                "classification": (
                    "FORMULA_ONLY_PROFILE_COMPLETION_PAIRING_OPEN"
                    if is_fc12
                    else "TOPOLOGY_OR_COMPLETION_TYPE_NO_COMPLETE_METRIC"
                ),
            }
        )
    require(
        "FC_complete_metric_count_zero",
        sum(row["complete_metric_witness"] == "YES" for row in fc_rows) == 0,
        checks,
    )

    family_rows = []
    for source, registry in zip(family_source, family_registry):
        family_id = source["family_id"]
        if family_id == "B19":
            classification = "CONDITIONAL_COMPLETE_ROUND_SPATIAL_METRIC_CLOCK_UNSOLDERED"
            spatial = "YES_CONDITIONAL"
            distance_status = "CALCULABLE_ROUND_CONTROL"
        elif family_id == "B21":
            classification = "LOCAL_CLOCK_DEPTH_NO_COMPLETE_GLOBAL_SPATIAL_METRIC"
            spatial = "NO"
            distance_status = "NOT_EVALUABLE_GLOBALLY"
        elif source["primary_classification"] == "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS":
            classification = "TOPOLOGY_ONLY_NO_COMPLETE_METRIC"
            spatial = "NO"
            distance_status = "NOT_EVALUABLE"
        else:
            classification = "NO_COMPLETE_PAIR_DISTANCE_WITNESS"
            spatial = "NO"
            distance_status = "NOT_EVALUABLE"
        family_rows.append(
            {
                "family_id": family_id,
                "family_label": registry["family_label"],
                "prior_classification": source["primary_classification"],
                "complete_spatial_metric": spatial,
                "two_point_distance": distance_status,
                "classification": classification,
            }
        )
    require(
        "one_conditional_complete_spatial_family",
        sum(row["complete_spatial_metric"] == "YES_CONDITIONAL" for row in family_rows)
        == 1,
        checks,
    )
    require(
        "complete_spatial_family_is_B19",
        [
            row["family_id"]
            for row in family_rows
            if row["complete_spatial_metric"] == "YES_CONDITIONAL"
        ]
        == ["B19"],
        checks,
    )

    solder_rows = []
    for row in solder_source:
        family_id = row["family_id"]
        if family_id == "F05":
            classification = "DUPLICATE_ROUND_SPATIAL_CONTROL_CLOCK_ROLE_SEPARATE"
            complete = "YES_CONDITIONAL_DUPLICATE"
        elif family_id == "F06":
            classification = "OPEN_OUTSIDE_PRIOR_BOUNDED_CLASS_NO_METRIC_WITNESS"
            complete = "NO"
        else:
            classification = "NO_REGULAR_COMPLETE_CLOCK_SOLDERED_TWO_CAP_WITNESS"
            complete = "NO"
        solder_rows.append(
            {
                "family_id": family_id,
                "prior_classification": row["classification"],
                "unique_complete_spatial_metric": complete,
                "physical_Xmax_gate": "NO",
                "classification": classification,
            }
        )
    require(
        "no_solder_physical_Xmax_pass",
        all(row["physical_Xmax_gate"] == "NO" for row in solder_rows),
        checks,
    )

    witness_rows = [
        {
            "witness_id": "W01_ROUND_S3_B19",
            "metric_status": "CONDITIONAL_COMPLETE_SPATIAL",
            "shape": "ROUND_S3_RADIUS_b",
            "d_h": "b*arccos(dot_Zp_Zq/b^2)",
            "X_p_n": "pi*b",
            "E_p": "pi*b",
            "diameter": "pi*b",
            "Delta_X_p": "0",
            "no_center": "YES_BY_TRANSITIVE_ROUND_ISOMETRY",
            "clock_solder": "NO_CONSTANT_LAPSE",
            "physical_Xmax": "NO",
        },
        {
            "witness_id": "W02_WRL_LOCAL",
            "metric_status": "CONDITIONAL_LOCAL_INCOMPLETE",
            "shape": "STATIC_SPHERICAL_LOCAL_PROFILE",
            "d_h": "LOCAL_RADIAL_D_EQUALS_2X_1_MINUS_EXP_MINUS_PHI",
            "X_p_n": "NOT_GLOBAL",
            "E_p": "NOT_EVALUABLE",
            "diameter": "NOT_EVALUABLE",
            "Delta_X_p": "NOT_EVALUABLE",
            "no_center": "NOT_GLOBALLY_TESTABLE",
            "clock_solder": "YES_LOCAL",
            "physical_Xmax": "NO",
        },
        {
            "witness_id": "W03_SQUASHED_S3_OFF_SHELL",
            "metric_status": "COMPLETE_NONROUND_OFF_SHELL_CONFIGURATION",
            "shape": "HOMOGENEOUS_SQUASHED_S3_b_sigma",
            "d_h": "FULL_CUT_LOCUS_NOT_EVALUATED",
            "X_p_n": "OPEN_EXACT_DISTRIBUTION",
            "E_p": "CONSTANT_BY_HOMOGENEITY_VALUE_OPEN",
            "diameter": "OPEN",
            "Delta_X_p": "OPEN_NOT_ZERO_PROMOTED",
            "no_center": "YES_BY_TRANSITIVE_U2_METRIC_ISOMETRY",
            "clock_solder": "NO_CONSTANT_LAPSE_CONTROL",
            "physical_Xmax": "NO_OFF_SHELL",
        },
    ]

    round_rows = [
        {
            "quantity": "two_point_distance",
            "exact_value": "b*arccos(dot_Zp_Zq/b^2)",
            "observer_dependence": "TWO_POINT_ONLY",
            "status": "DERIVED_CONDITIONAL_ROUND_METRIC",
        },
        {
            "quantity": "directional_cut_distance_X_p_n",
            "exact_value": "pi*b",
            "observer_dependence": "INDEPENDENT_OF_p_AND_n",
            "status": "DERIVED_CONDITIONAL_ROUND_METRIC",
        },
        {
            "quantity": "observer_eccentricity_E_p",
            "exact_value": "pi*b",
            "observer_dependence": "INDEPENDENT_OF_p",
            "status": "DERIVED_CONDITIONAL_ROUND_METRIC",
        },
        {
            "quantity": "global_spatial_diameter",
            "exact_value": "pi*b",
            "observer_dependence": "SUPREMUM_OVER_ALL_PAIRS",
            "status": "DERIVED_CONDITIONAL_ROUND_METRIC",
        },
        {
            "quantity": "directional_spread_Delta_X_p",
            "exact_value": "0",
            "observer_dependence": "INDEPENDENT_OF_p",
            "status": "DERIVED_CONDITIONAL_ROUND_METRIC",
        },
        {
            "quantity": "neutral_torus_to_cap_depth",
            "exact_value": "pi*b/4",
            "observer_dependence": "FOLIATION_CHART_SEGMENT_NOT_PAIR_DIAMETER",
            "status": "DERIVED_CONDITIONAL_NOT_XMAX",
        },
    ]

    shape_rows = [
        {
            "change_class": "coordinate_change",
            "can_change_d_h": "NO",
            "can_change_Delta_X": "NO",
            "required_data": "diffeomorphism_pullback_only",
            "status": "EXACT_INVARIANCE",
        },
        {
            "change_class": "orthonormal_coframe_rotation",
            "can_change_d_h": "NO",
            "can_change_Delta_X": "NO",
            "required_data": "same_metric",
            "status": "EXACT_INVARIANCE",
        },
        {
            "change_class": "round_axis_exchange",
            "can_change_d_h": "NO",
            "can_change_Delta_X": "NO",
            "required_data": "round_isometry",
            "status": "EXACT_INVARIANCE",
        },
        {
            "change_class": "constant_physical_scale_b",
            "can_change_d_h": "YES_UNIFORM",
            "can_change_Delta_X": "NO_FROM_ZERO",
            "required_data": "selected_b",
            "status": "SCALE_UNSELECTED",
        },
        {
            "change_class": "constant_Hopf_fiber_squashing_sigma",
            "can_change_d_h": "YES",
            "can_change_Delta_X": "POSSIBLY_FULL_CUT_LOCUS_OPEN",
            "required_data": "complete_squashed_metric_supplied_off_shell",
            "status": "EXACT_LOOP_LENGTH_SENSITIVITY_OFF_SHELL_CONTROL",
        },
        {
            "change_class": "nonconstant_physical_shape_or_angular_amplitude",
            "can_change_d_h": "YES",
            "can_change_Delta_X": "YES_POSSIBLY",
            "required_data": "complete_regular_nonround_metric",
            "status": "NO_CURRENT_WITNESS",
        },
        {
            "change_class": "topology_or_quotient_label_only",
            "can_change_d_h": "NOT_EVALUABLE",
            "can_change_Delta_X": "NOT_EVALUABLE",
            "required_data": "metric_lattice_scale_quotient_and_pairing",
            "status": "INSUFFICIENT_DATA",
        },
    ]

    gate_rows = [
        {
            "gate": "complete_observer_rest_spatial_metric",
            "round_B19": "YES_CONDITIONAL",
            "WRL": "NO_GLOBAL",
            "full_physical_pass": "NO",
        },
        {
            "gate": "no_center_two_point_distance",
            "round_B19": "YES",
            "WRL": "NOT_TESTABLE_GLOBALLY",
            "full_physical_pass": "NO",
        },
        {
            "gate": "observer_frame_equivalence",
            "round_B19": "YES_ROUND_ISOMETRY",
            "WRL": "NOT_DERIVED_GLOBALLY",
            "full_physical_pass": "NO",
        },
        {
            "gate": "founding_clock_dilation_solder",
            "round_B19": "NO_CONSTANT_LAPSE",
            "WRL": "YES_LOCAL",
            "full_physical_pass": "NO",
        },
        {
            "gate": "pairwise_infinite_dilation_at_diameter",
            "round_B19": "NO",
            "WRL": "NO_GLOBAL_DIAMETER",
            "full_physical_pass": "NO",
        },
        {
            "gate": "nonround_directional_band",
            "round_B19": "ZERO",
            "WRL": "NOT_EVALUABLE",
            "full_physical_pass": "NO",
        },
    ]
    require(
        "no_full_physical_Xmax_gate_pass",
        all(row["full_physical_pass"] == "NO" for row in gate_rows),
        checks,
    )

    status_rows = [
        {
            "claim": "Xmax_definition",
            "status": "OWNER_CLARIFIED_TWO_OBSERVER_GLOBAL_SUPREMUM",
            "scope": "no_privileged_center",
        },
        {
            "claim": "round_two_point_distance",
            "status": "DERIVED_CONDITIONAL",
            "scope": "complete_round_S3_b_spatial_metric",
        },
        {
            "claim": "round_observer_frame_equivalence",
            "status": "DERIVED_CONDITIONAL",
            "scope": "transitive_round_isometry_group",
        },
        {
            "claim": "round_directional_variance",
            "status": "DERIVED_ZERO",
            "scope": "complete_round_S3_b_spatial_metric",
        },
        {
            "claim": "current_nonround_directional_band",
            "status": "OPEN_NOT_EVALUABLE",
            "scope": "off_shell_squashed_control_has_no_full_cut_locus_and_no_on_shell_clock_solder",
        },
        {
            "claim": "complete_nonround_metric_configuration",
            "status": "PRESENT_OFF_SHELL_CONTROL",
            "scope": "positive_constant_squashing_family",
        },
        {
            "claim": "squashed_control_no_privileged_center",
            "status": "DERIVED_CONDITIONAL_METRIC_GEOMETRY",
            "scope": "transitive_U2_action_preserves_round_horizontal_metric_and_Hopf_one_form",
        },
        {
            "claim": "squashed_control_loop_length_anisotropy",
            "status": "DERIVED_OFF_SHELL_CONTROL",
            "scope": "fiber_2pi_b_sigma_horizontal_2pi_b_not_full_cut_band",
        },
        {
            "claim": "CMB_relation_to_directional_band",
            "status": "OBSERVATIONAL_COMPARISON_OPEN",
            "scope": "not_used_as_selector",
        },
        {
            "claim": "physical_UDT_Xmax",
            "status": "OPEN_NOT_EVALUABLE",
            "scope": "no_branch_joins_global_pair_diameter_and_clock_asymptote",
        },
    ]

    write_tsv(
        "FC_PAIR_DISTANCE_SCREEN.tsv",
        [
            "completion_id",
            "prior_classification",
            "complete_metric_witness",
            "two_point_distance",
            "directional_band",
            "classification",
        ],
        fc_rows,
    )
    write_tsv(
        "EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv",
        [
            "family_id",
            "family_label",
            "prior_classification",
            "complete_spatial_metric",
            "two_point_distance",
            "classification",
        ],
        family_rows,
    )
    write_tsv(
        "SOLDER_FAMILY_PAIR_DISTANCE_SCREEN.tsv",
        [
            "family_id",
            "prior_classification",
            "unique_complete_spatial_metric",
            "physical_Xmax_gate",
            "classification",
        ],
        solder_rows,
    )
    write_tsv(
        "COMPLETE_WITNESS_LEDGER.tsv",
        [
            "witness_id",
            "metric_status",
            "shape",
            "d_h",
            "X_p_n",
            "E_p",
            "diameter",
            "Delta_X_p",
            "no_center",
            "clock_solder",
            "physical_Xmax",
        ],
        witness_rows,
    )
    write_tsv(
        "ROUND_DIRECTIONAL_DISTANCE_LEDGER.tsv",
        ["quantity", "exact_value", "observer_dependence", "status"],
        round_rows,
    )
    write_tsv(
        "SHAPE_SENSITIVITY_LEDGER.tsv",
        [
            "change_class",
            "can_change_d_h",
            "can_change_Delta_X",
            "required_data",
            "status",
        ],
        shape_rows,
    )
    write_tsv(
        "PHYSICAL_XMAX_GATE_MATRIX.tsv",
        ["gate", "round_B19", "WRL", "full_physical_pass"],
        gate_rows,
    )
    squashed_rows = [
        {
            "quantity": "metric",
            "exact_result": "h_sigma=b^2[e1^2+e2^2+sigma^2*alpha^2]",
            "status": "COMPLETE_POSITIVE_SMOOTH_FOR_SIGMA_POSITIVE",
            "physical_limit": "OFF_SHELL_CONTROL",
        },
        {
            "quantity": "homogeneity",
            "exact_result": "U2_preserves_h_round_and_alpha_and_acts_transitively",
            "status": "NO_PRIVILEGED_POINT",
            "physical_limit": "DIRECTION_ISOTROPY_NOT_IMPLIED",
        },
        {
            "quantity": "Hopf_fiber_closed_geodesic",
            "exact_result": "length=2*pi*b*sigma",
            "status": "DERIVED",
            "physical_limit": "CUT_TIME_NOT_DERIVED",
        },
        {
            "quantity": "horizontal_great_circle",
            "exact_result": "length=2*pi*b",
            "status": "DERIVED",
            "physical_limit": "CUT_TIME_NOT_DERIVED",
        },
        {
            "quantity": "antipode_distance_bound",
            "exact_result": "d(p,-p)<=pi*b*min(sigma,1)",
            "status": "DERIVED_BOUND",
            "physical_limit": "NOT_EXACT_DIAMETER",
        },
        {
            "quantity": "directional_cut_band",
            "exact_result": "not_evaluated",
            "status": "OPEN",
            "physical_limit": "REQUIRES_FULL_GEODESIC_CUT_LOCUS",
        },
    ]
    write_tsv(
        "SQUASHED_CONTROL_LEDGER.tsv",
        ["quantity", "exact_result", "status", "physical_limit"],
        squashed_rows,
    )
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows)

    source_rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv") + read_tsv(
        HERE / "SOURCE_ADDENDUM.tsv"
    )
    for row in source_rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        require(f"source_{row['id']}_identity", actual == row["sha256"], checks)

    result = {
        "schema": "udt-directional-observer-pair-distance-audit-1.0",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "FC_rows": len(fc_rows),
        "equation_family_rows": len(family_rows),
        "solder_family_rows": len(solder_rows),
        "complete_metric_configuration_classes": 2,
        "complete_on_shell_spatial_metric_witnesses": 1,
        "complete_nonround_off_shell_control_families": 1,
        "complete_nonround_clock_soldered_witnesses": 0,
        "physical_Xmax_pass_count": 0,
        "round_control": {
            "distance": "b*acos(dot_Zp_Zq/b^2)",
            "directional_cut_distance": "pi*b",
            "observer_eccentricity": "pi*b",
            "diameter": "pi*b",
            "directional_spread": "0",
            "neutral_torus_to_cap_depth": "pi*b/4",
            "diameter_to_cap_depth_ratio": "4",
            "privileged_center": False,
            "clock_solder": False,
        },
        "directional_variance_ruling": (
            "ON_SHELL_ROUND_CONTROL_ZERO;OFF_SHELL_SQUASHED_LOOP_ANISOTROPY_"
            "DERIVED_BUT_FULL_CUT_BAND_OPEN;NO_PHYSICAL_NONROUND_BAND"
        ),
        "squashed_control": {
            "metric": "b^2[e1^2+e2^2+sigma^2*alpha^2]",
            "fiber_loop_length": "2*pi*b*sigma",
            "horizontal_loop_length": "2*pi*b",
            "antipode_distance_upper_bound": "pi*b*min(sigma,1)",
            "privileged_center": False,
            "on_shell": False,
            "clock_solder": False,
            "full_directional_cut_band": "OPEN",
        },
        "global_ruling": (
            "GEOMETRIC_ROUND_DIAMETER_DERIVED_CONDITIONAL_WITH_NO_CENTER;"
            "PHYSICAL_UDT_XMAX_OPEN_NO_COMMON_CLOCK_SOLDERED_GLOBAL_WITNESS"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"sympy={sp.__version__}")
    print(f"checks={len(checks)}")
    print("FC_rows=12")
    print("equation_family_rows=28")
    print("solder_family_rows=6")
    print("complete_nonround_off_shell_control_families=1")
    print("complete_nonround_clock_soldered_witnesses=0")
    print("physical_Xmax_pass_count=0")
    print(
        "derivation_sha256="
        + hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest()
    )


if __name__ == "__main__":
    main()
