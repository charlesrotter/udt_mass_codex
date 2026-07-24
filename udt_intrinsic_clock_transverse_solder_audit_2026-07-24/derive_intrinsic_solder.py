#!/usr/bin/env python3
"""Exact intrinsic clock/transverse solder audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_BASE = "2e98f4cc91a0accbfe8a5e96d180ef3f297d8da0"
PREREG_COMMIT = "4ceac0f880edf3e3ffe1c8caa8805a00a826595b"


def check(checks: dict[str, str], name: str, condition: object) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    name: str, fields: list[str], rows: list[dict[str, object]]
) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_checks(checks: dict[str, str]) -> int:
    rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(rows) == 21)
    check(checks, "source_unique", len({row["path"] for row in rows}) == 21)
    for row in rows:
        path = ROOT / row["path"]
        check(checks, f"source_exists_{row['role']}", path.is_file())
        if row["role"] == "frontier_scope_at_base":
            data = subprocess.run(
                ["git", "show", f"{SOURCE_BASE}:{row['path']}"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout
        else:
            data = path.read_bytes()
        check(
            checks,
            f"source_hash_{row['role']}",
            hashlib.sha256(data).hexdigest() == row["sha256"],
        )
    return len(rows)


def exterior_derivation(endomorphism: sp.Matrix) -> sp.Matrix:
    """Induced derivation on Lambda^2 in lexicographic pair basis."""
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    index = {pair: i for i, pair in enumerate(pairs)}
    result = sp.zeros(6)

    def add_wedge(column: int, coefficient: sp.Expr, i: int, j: int) -> None:
        if i == j or coefficient == 0:
            return
        if i < j:
            result[index[(i, j)], column] += coefficient
        else:
            result[index[(j, i)], column] -= coefficient

    for column, (i, j) in enumerate(pairs):
        for a in range(4):
            add_wedge(column, endomorphism[a, i], a, j)
            add_wedge(column, endomorphism[a, j], i, a)
    return result


def cross(vector: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Matrix:
    x, y, z = vector
    return sp.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])


def main() -> None:
    checks: dict[str, str] = {}
    I2, I3 = sp.eye(2), sp.eye(3)
    Z3 = sp.zeros(3)

    # Universal oriented Lorentzian Hodge control on Lambda^2, ordered as
    # three longitudinal/electric bivectors followed by their transverse
    # Hodge partners.
    star = sp.zeros(6)
    star[:3, 3:] = -I3
    star[3:, :3] = I3
    check(checks, "hodge_square_minus_identity", star * star == -sp.eye(6))
    check(checks, "hodge_invertible", star.det() == 1)
    normal_area = sp.Matrix([1, 0, 0, 0, 0, 0])
    screen_area = sp.Matrix([0, 0, 0, 1, 0, 0])
    check(checks, "hodge_maps_normal_area_to_screen_area", star * normal_area == screen_area)

    delta, theta = sp.symbols("delta theta", real=True)
    reciprocal = sp.diag(sp.exp(-delta), sp.exp(delta))
    rotation = sp.Matrix(
        [[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]]
    )
    check(checks, "reciprocal_area_character_trivial", reciprocal.det() == 1)
    check(checks, "screen_area_character_trivial", sp.trigsimp(rotation.det()) == 1)

    # Independent endpoint screen gauge forbids a nonzero linear map from a
    # screen-scalar reciprocal space to screen vectors or phase space.
    J2 = sp.Matrix([[0, -1], [1, 0]])
    J4 = sp.diag(1, 1, 1, 1)
    J4[:2, :2], J4[2:, 2:] = J2, J2
    check(checks, "screen_generator_invertible", J4.det() == 1)
    check(checks, "clock_to_phase_equivariant_map_dimension", len(J4.nullspace()) == 0)
    check(checks, "phase_to_clock_cross_pairing_dimension", len(J4.T.nullspace()) == 0)

    # Exact invariant screen-line condition for Jacobi phase space.
    k1, k12, k2 = sp.symbols("k1 k12 k2", real=True)
    tidal = sp.Matrix([[k1, k12], [k12, k2]])
    P = sp.diag(1, 0)
    P4 = sp.diag(1, 0, 1, 0)
    A4 = sp.zeros(4)
    A4[:2, 2:] = I2
    A4[2:, :2] = -tidal
    commutator = sp.simplify(A4 * P4 - P4 * A4)
    check(
        checks,
        "phase_line_commutator_equals_tidal_commutator",
        commutator[2:, :2] == -(tidal * P - P * tidal)
        and commutator[:2, :2] == sp.zeros(2)
        and commutator[:2, 2:] == sp.zeros(2)
        and commutator[2:, 2:] == sp.zeros(2),
    )
    check(
        checks,
        "fixed_line_invariant_iff_offdiagonal_tidal_zero",
        all(sp.simplify(entry.subs(k12, 0)) == 0 for entry in commutator)
        and any(entry != 0 for entry in commutator),
    )

    # Scalar Jacobi versus reciprocal infinitesimal generator.
    K, a, lam = sp.symbols("K a lam", real=True)
    jacobi_generator = sp.Matrix([[0, 1], [-K, 0]])
    reciprocal_generator = sp.diag(-a, a)
    check(
        checks,
        "jacobi_characteristic_polynomial",
        jacobi_generator.charpoly().all_coeffs() == [1, 0, K],
    )
    check(
        checks,
        "reciprocal_characteristic_polynomial",
        reciprocal_generator.charpoly().all_coeffs() == [1, 0, -a**2],
    )
    check(
        checks,
        "generator_determinant_match_condition",
        sp.simplify(jacobi_generator.det() - reciprocal_generator.det())
        == K + a**2,
    )
    matched_jacobi = jacobi_generator.subs(K, -a**2)
    intertwiner = sp.Matrix([[1, 1], [-a, a]])
    check(
        checks,
        "negative_curvature_intertwiner",
        matched_jacobi * intertwiner == intertwiner * reciprocal_generator,
    )
    check(checks, "negative_curvature_intertwiner_rank_nonzero_a", intertwiner.det() == 2 * a)
    flat_jacobi = jacobi_generator.subs(K, 0)
    check(checks, "zero_clock_flat_jacobi_nonzero", flat_jacobi != sp.zeros(2))
    check(checks, "zero_clock_flat_jacobi_nilpotent", flat_jacobi**2 == sp.zeros(2))

    # B19 and WR-L exact obstructions.
    b, length, D, X = sp.symbols("b length D X", positive=True)
    round_M = sp.Matrix(
        [
            [sp.cos(length / b), b * sp.sin(length / b)],
            [-sp.sin(length / b) / b, sp.cos(length / b)],
        ]
    )
    check(
        checks,
        "b19_quarter_diameter_not_identity",
        round_M.subs(length, sp.pi * b / 2) != sp.eye(2),
    )
    check(
        checks,
        "b19_positive_screen_curvature",
        1 / b**2 > 0,
    )
    N = 1 - D / (2 * X)
    R = D - D**2 / (4 * X)
    K_wrl = sp.simplify(1 / (2 * X * R))
    a_wrl = sp.simplify(-sp.diff(sp.log(N), D))
    check(
        checks,
        "wrl_clock_rate",
        sp.simplify(a_wrl - 1 / (2 * X * N)) == 0,
    )
    check(
        checks,
        "wrl_generator_mismatch_nonzero",
        sp.factor(K_wrl + a_wrl**2) != 0,
    )
    check(
        checks,
        "wrl_scalar_profile_relation",
        sp.simplify(R - X * (1 - N**2)) == 0,
    )
    Q = sp.symbols("Q", positive=True)
    check(
        checks,
        "wrl_Q_profile_relation",
        sp.simplify((R - X * (1 - Q**-2)).subs(Q, 1 / N)) == 0,
    )

    # The complete induced two-form connection commutes with Hodge while
    # its off-stabilizer block can still mix the dphi 3+3 sectors.
    rx, ry, rz, bx = sp.symbols("rx ry rz bx", real=True, nonzero=True)
    rot3 = cross((rx, ry, rz))
    boost3 = cross((bx, 0, 0))
    connection6 = sp.zeros(6)
    connection6[:3, :3] = rot3
    connection6[:3, 3:] = boost3
    connection6[3:, :3] = -boost3
    connection6[3:, 3:] = rot3
    check(checks, "connection_commutes_with_hodge", connection6 * star == star * connection6)
    Pi_parallel = sp.diag(1, 1, 1, 0, 0, 0)
    split_mixing = connection6 * Pi_parallel - Pi_parallel * connection6
    check(checks, "generic_offstabilizer_mixing_rank_four", split_mixing.rank() == 4)
    check(
        checks,
        "zero_offstabilizer_preserves_split",
        split_mixing.subs(bx, 0) == sp.zeros(6),
    )

    # dphi reciprocal 3+3 and null degeneration controls.
    phi = sp.symbols("phi", real=True)
    Dphi = sp.diag(
        sp.exp(phi),
        sp.exp(phi),
        sp.exp(phi),
        sp.exp(-phi),
        sp.exp(-phi),
        sp.exp(-phi),
    )
    check(
        checks,
        "hodge_exchanges_dphi_reciprocal_sectors",
        all(
            sp.powsimp(entry, force=True) == 0
            for entry in (star * Dphi * star.inv() - Dphi.inv())
        ),
    )
    metric_inverse = sp.diag(-1, 1, 1, 1)
    alpha_null = sp.Matrix([[1, 1, 0, 0]])
    vector_null = metric_inverse * alpha_null.T
    null_map = vector_null * alpha_null
    null_lift = exterior_derivation(null_map)
    check(checks, "null_line_map_rank_one", null_map.rank() == 1)
    check(checks, "null_line_map_nilpotent", null_map**2 == sp.zeros(4))
    check(checks, "null_twoform_lift_rank_two", null_lift.rank() == 2)
    check(checks, "null_twoform_lift_nilpotent", null_lift**2 == sp.zeros(6))

    completions_source = read_tsv(
        ROOT
        / "udt_finite_cell_cartan_transport_atlas_2026-07-23"
        / "FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv"
    )
    prior_solder = {
        row["completion_id"]: row
        for row in read_tsv(
            ROOT
            / "udt_reciprocal_angular_intertwiner_audit_2026-07-23"
            / "COMPLETION_SOLDERING_ATLAS.tsv"
        )
    }
    equations = read_tsv(
        ROOT
        / "udt_center_free_observer_optical_correspondence_audit_2026-07-24"
        / "EQUATION_FAMILY_OPTICAL_SCREEN.tsv"
    )
    check(checks, "completion_count", len(completions_source) == 12)
    check(
        checks,
        "completion_unique",
        len({row["completion_id"] for row in completions_source}) == 12,
    )
    check(checks, "prior_solder_completion_count", len(prior_solder) == 12)
    check(checks, "equation_family_count", len(equations) == 28)
    check(
        checks,
        "equation_family_unique",
        len({row["family_id"] for row in equations}) == 28,
    )
    source_count = source_checks(checks)

    candidates = [
        {
            "candidate": "OBSERVER_PATH_2PLUS2_REDUCTION",
            "type": "TANGENT_BUNDLE_REDUCTION",
            "derived_content": "NORMAL_PLANE_PLUS_SCREEN_GIVEN_G_U_K",
            "solder_ruling": "CONDITIONAL_REDUCTION_NOT_CLOCK_SCREEN_IDENTIFICATION",
        },
        {
            "candidate": "HODGE_NORMAL_SCREEN_AREA_DUALITY",
            "type": "SPACETIME_TWOFORM_MAP",
            "derived_content": "STAR_NORMAL_AREA_EQUALS_SCREEN_AREA_UP_TO_ORIENTATION_SIGN",
            "solder_ruling": "DERIVED_UNIVERSAL_CONTROL_TYPE_MISMATCH_TO_JACOBI_PHASE",
        },
        {
            "candidate": "SO2_EQUIVARIANT_LINEAR_CLOCK_TO_PHASE_MAP",
            "type": "BUNDLE_HOMOMORPHISM",
            "derived_content": "ZERO_ONLY_WITHOUT_SCREEN_DIRECTION",
            "solder_ruling": "OBSTRUCTED_BY_ENDPOINT_SCREEN_GAUGE",
        },
        {
            "candidate": "SO2_INVARIANT_CLOCK_PHASE_CROSS_PAIRING",
            "type": "BILINEAR_CROSS_BLOCK",
            "derived_content": "ZERO_ONLY_WITHOUT_SCREEN_DIRECTION",
            "solder_ruling": "OBSTRUCTED_BY_ENDPOINT_SCREEN_GAUGE",
        },
        {
            "candidate": "PARALLEL_TIDAL_INVARIANT_SCREEN_LINE",
            "type": "RANK2_PHASE_SUBBUNDLE",
            "derived_content": "EXISTS_IFF_DP_EQUALS_ZERO_AND_T_COMMUTES_WITH_P",
            "solder_ruling": "CONDITIONAL_NOT_SELECTED",
        },
        {
            "candidate": "SCALAR_JACOBI_RECIPROCAL_GENERATOR_MATCH",
            "type": "REAL_INTERTWINER",
            "derived_content": "POINTWISE_NATURAL_FRAME_NONTRIVIAL_MATCH_IFF_K_EQUALS_MINUS_A_SQUARED",
            "solder_ruling": "UNIQUE_CONDITION_CHARACTERIZED_NO_REGISTERED_COMPLETE_WITNESS",
        },
        {
            "candidate": "WRL_SCALAR_PROFILE_RELATION",
            "type": "BRANCH_SPECIFIC_SCALAR_IDENTITY",
            "derived_content": "R_EQUALS_X_TIMES_ONE_MINUS_Q_INVERSE_SQUARED",
            "solder_ruling": "DERIVED_LOCAL_PROFILE_RELATION_NOT_TRANSPORT_SOLDER",
        },
        {
            "candidate": "FULL_COFRAME_CONNECTION",
            "type": "SPACETIME_FRAME_TRANSPORT",
            "derived_content": "HODGE_PARALLEL_BUT_OFFSTABILIZER_BLOCK_MIXES_SPLIT",
            "solder_ruling": "DERIVED_PER_METRIC_NOT_RECIPROCAL_JACOBI_IDENTIFICATION",
        },
        {
            "candidate": "DPHI_3PLUS3_TWOFORM_REDUCTION",
            "type": "FIELD_ASSISTED_LAMBDA2_REDUCTION",
            "derived_content": "REAL_HODGE_EXCHANGED_SECTORS_ON_NONNULL_DPHI",
            "solder_ruling": "DERIVED_ON_DOMAIN_NO_CANONICAL_RANK2_JACOBI_SUBBUNDLE",
        },
        {
            "candidate": "PRIOR_MATCHED_ANGULAR_INTERTWINER",
            "type": "CONDITIONAL_REPRESENTATION_THEOREM",
            "derived_content": "FULL_RANK_IFF_ANGULAR_GENERATOR_SIMILAR_TO_RECIPROCAL_GENERATOR",
            "solder_ruling": "CONDITIONAL_INPUT_NOT_SELECTED",
        },
        {
            "candidate": "CURVATURE_OR_HOLONOMY_SELECTED_PLANE",
            "type": "SPECTRAL_OR_GLOBAL_REDUCTION",
            "derived_content": "ZERO_ISOLATED_REAL_SIMPLE_EIGENBIVECTOR_PLANES_IN_REGISTERED_6144_TWOJETS",
            "solder_ruling": "BOUNDED_NEGATIVE_REUSED_GLOBAL_REDUCTION_OPEN",
        },
        {
            "candidate": "DIRECT_SUM_CLOCK_PLUS_JACOBI",
            "type": "REDUCIBLE_PATH_COCYCLE",
            "derived_content": "EXACT_COMPOSITION_GIVEN_COMMON_TYPED_PATH_DATA",
            "solder_ruling": "DERIVED_AND_REMAINS_STRONGEST_UNCONDITIONAL_ASSEMBLY",
        },
    ]
    write_tsv(
        "SOLDER_TYPE_LEDGER.tsv",
        ["candidate", "type", "derived_content", "solder_ruling"],
        candidates,
    )

    generator_rows = [
        {
            "control": "GENERAL_SCALAR_MODE",
            "clock_rate_a": "a",
            "screen_curvature_K": "K",
            "phase_type": "ELLIPTIC_IF_K_POSITIVE_HYPERBOLIC_IF_K_NEGATIVE",
            "match_condition": "a_NONZERO_AND_K_EQUALS_MINUS_a_SQUARED",
            "ruling": "UNIQUE_CONDITION_CHARACTERIZED",
        },
        {
            "control": "MATCHED_NEGATIVE_CURVATURE",
            "clock_rate_a": "a_NONZERO",
            "screen_curvature_K": "-a^2",
            "phase_type": "HYPERBOLIC",
            "match_condition": "EXACT_INTERTWINER_COLUMNS_1_MINUS_a_AND_1_PLUS_a",
            "ruling": "CONSTRUCTIVE_MATHEMATICAL_WITNESS_NOT_SELECTED_UDT_BRANCH",
        },
        {
            "control": "B19_ROUND",
            "clock_rate_a": "0",
            "screen_curvature_K": "+1/b^2",
            "phase_type": "ELLIPTIC",
            "match_condition": "FAIL",
            "ruling": "COMPLETE_TRANSVERSE_NO_NONTRIVIAL_CLOCK_SOLDER",
        },
        {
            "control": "WRL_LOCAL_RADIAL",
            "clock_rate_a": "1/(2XN)",
            "screen_curvature_K": "+1/(2XR)",
            "phase_type": "ELLIPTIC_INFINITESIMALLY",
            "match_condition": "FAIL_K_PLUS_a_SQUARED_POSITIVE",
            "ruling": "LOCAL_PROFILE_RELATION_WITHOUT_LINEAR_TRANSPORT_SOLDER",
        },
        {
            "control": "FLAT_ZERO_CLOCK",
            "clock_rate_a": "0",
            "screen_curvature_K": "0",
            "phase_type": "NONZERO_NILPOTENT_FREE_DRIFT",
            "match_condition": "FAIL_ZERO_GENERATOR_NOT_SIMILAR_TO_NONZERO_NILPOTENT",
            "ruling": "NO_GENERATOR_SOLDER",
        },
    ]
    write_tsv(
        "GENERATOR_MATCH_ATLAS.tsv",
        [
            "control",
            "clock_rate_a",
            "screen_curvature_K",
            "phase_type",
            "match_condition",
            "ruling",
        ],
        generator_rows,
    )

    branches = [
        {
            "branch": "B19_ROUND_S3",
            "metric_status": "CONDITIONAL_COMPLETE_ON_SHELL_SPATIAL_ULTRASTATIC",
            "area_duality": "YES_GIVEN_ORIENTATION_AND_PATH_SPLIT",
            "linear_solder": "NO_Q_IDENTITY_VERSUS_ELLIPTIC_TRANSVERSE_GENERATOR",
            "global_status": "COMPLETE_SET_VALUED_PATH_FAMILY",
            "ruling": "TRANSVERSE_COCYCLE_WITHOUT_NONTRIVIAL_CLOCK_SOLDER",
        },
        {
            "branch": "SQUASHED_S3_OFF_SHELL",
            "metric_status": "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL",
            "area_duality": "YES_GIVEN_ORIENTATION_AND_PATH_SPLIT",
            "linear_solder": "NO_SELECTED_PARALLEL_SCREEN_LINE_OR_MATCHED_MODE;Q_IDENTITY",
            "global_status": "OFF_SHELL_CUT_ATLAS_OPEN",
            "ruling": "NO_SELECTED_SOLDER",
        },
        {
            "branch": "WRL_LOCAL_RESIDUAL",
            "metric_status": "LOCAL_CENTERED_STATIC_PROFILE_NO_GLOBAL_COMPLETION",
            "area_duality": "YES_ON_REGULAR_RADIAL_2PLUS2_REGION",
            "linear_solder": "NO_POINTWISE_NATURAL_FRAME_SIMILARITY_POSITIVE_K_VERSUS_HYPERBOLIC_CLOCK",
            "global_status": "NO_ALL_OBSERVER_RECENTERING",
            "ruling": "SCALAR_PROFILE_JOIN_DERIVED_TRANSPORT_SOLDER_OBSTRUCTED",
        },
        {
            "branch": "TEMPORAL_PHI_SLICE_FAMILY",
            "metric_status": "CONDITIONAL_PRE_SCALE_REST_GEOMETRY_NO_COMPLETE_BRANCH",
            "area_duality": "CONDITIONAL_GIVEN_PATH_SPLIT_AND_ORIENTATION",
            "linear_solder": "OPEN_CLOCK_SOLDER_AND_SCREEN_MODE_NOT_SELECTED",
            "global_status": "OPEN",
            "ruling": "CONDITIONAL_REDUCTION_NO_WITNESS",
        },
        {
            "branch": "CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL",
            "metric_status": "MATHEMATICAL_COMPARISON_NOT_REGISTERED_UDT_BRANCH",
            "area_duality": "YES_IN_STATIC_PATCH",
            "linear_solder": "NO_POSITIVE_SCREEN_K_VERSUS_HYPERBOLIC_CLOCK",
            "global_status": "CLOCK_PATCH_ENDS_BEFORE_SPATIAL_DIAMETER",
            "ruling": "COUNTERCONTROL_NO_GLOBAL_SOLDER",
        },
        {
            "branch": "UNIVERSAL_PHYSICAL_UDT",
            "metric_status": "NO_COMPLETE_WITNESS",
            "area_duality": "LOCAL_UNIVERSAL_CONTROL_WHERE_ORIENTED_SPLIT_SUPPLIED",
            "linear_solder": "OPEN",
            "global_status": "OPEN",
            "ruling": "NO_COMPLETE_NONTRIVIAL_ALL_OBSERVER_SOLDER",
        },
    ]
    write_tsv(
        "BRANCH_SOLDER_ATLAS.tsv",
        [
            "branch",
            "metric_status",
            "area_duality",
            "linear_solder",
            "global_status",
            "ruling",
        ],
        branches,
    )

    causal_rows = [
        {
            "dphi_class": "TIMELIKE_NONNULL",
            "intrinsic_object": "REAL_BOOST3_PLUS_ROTATION3_TWOFORMS",
            "connection": "LC_PRESERVES_IFF_OFFSTABILIZER_BLOCK_ZERO;KATO_AVAILABLE",
            "clock_jacobi_solder": "NO_CANONICAL_RANK2_SCREEN_PHASE_SUBBUNDLE",
            "ruling": "LOCAL_REDUCTION_DERIVED_SOLDER_OPEN",
        },
        {
            "dphi_class": "SPACELIKE_NONNULL",
            "intrinsic_object": "REAL_3PLUS3_SO_PLUS_1_2_SYMMETRIC_PAIR",
            "connection": "LC_PRESERVES_IFF_COMPLEMENTARY_BLOCK_ZERO;KATO_AVAILABLE",
            "clock_jacobi_solder": "NO_OBSERVER_SCREEN_OR_CANONICAL_RANK2_SUBBUNDLE",
            "ruling": "LOCAL_REDUCTION_DERIVED_NO_OBSERVER_SOLDER",
        },
        {
            "dphi_class": "NULL_NONNULL",
            "intrinsic_object": "RANK2_NILPOTENT_TWOFORMS_FILTRATION",
            "connection": "SEMISIMPLE_PROJECTOR_UNDEFINED",
            "clock_jacobi_solder": "NO_SEMISIMPLE_RECIPROCAL_SPLIT",
            "ruling": "DEGENERATE",
        },
        {
            "dphi_class": "ZERO",
            "intrinsic_object": "NO_DPHI_LINE",
            "connection": "APPROACH_DIRECTION_DEPENDENT",
            "clock_jacobi_solder": "NO_FIELD_ASSISTED_SOLDER",
            "ruling": "DEGENERATE",
        },
        {
            "dphi_class": "TYPE_CHANGING",
            "intrinsic_object": "PIECEWISE_NONNULL_REDUCTIONS",
            "connection": "MUST_CROSS_NULL_OR_ZERO_DEGENERATION",
            "clock_jacobi_solder": "NO_UNIVERSAL_INTERFACE_RULE",
            "ruling": "OPEN_INTERFACE",
        },
    ]
    write_tsv(
        "CAUSAL_SOLDER_ATLAS.tsv",
        ["dphi_class", "intrinsic_object", "connection", "clock_jacobi_solder", "ruling"],
        causal_rows,
    )

    completion_rows = []
    for row in completions_source:
        old = prior_solder[row["completion_id"]]
        completion_rows.append(
            {
                "completion_id": row["completion_id"],
                "topology_family": row["topology_family"],
                "dphi_reduction": row["parent_projector_survival"],
                "hodge_globality": row["Hodge_status"],
                "angular_representation": old["angular_representation_status"],
                "complete_g_phi_witness": old["complete_g_phi_witness"],
                "solder_ruling": "NO_COMPLETE_ONSHELL_SOLDER_WITNESS;NO_BRANCH_SELECTED",
            }
        )
    write_tsv(
        "COMPLETION_SOLDER_ATLAS.tsv",
        [
            "completion_id",
            "topology_family",
            "dphi_reduction",
            "hodge_globality",
            "angular_representation",
            "complete_g_phi_witness",
            "solder_ruling",
        ],
        completion_rows,
    )

    statuses = [
        {
            "claim": "oriented normal-screen area Hodge duality",
            "status": "DERIVED_GIVEN_TYPED_2PLUS2_SPLIT",
            "scope": "universal Lorentzian area relation not UDT-specific phase transport",
        },
        {
            "claim": "Hodge area duality is clock-Jacobi solder",
            "status": "FALSE_TYPE",
            "scope": "spacetime two-forms differ from Jacobi phase states and boost area loses delta",
        },
        {
            "claim": "screen-gauge-equivariant linear clock-to-phase map",
            "status": "OBSTRUCTED_WITHOUT_SCREEN_REDUCTION",
            "scope": "independent endpoint SO2 gauge has no fixed vector",
        },
        {
            "claim": "parallel tidal-invariant screen line criterion",
            "status": "DERIVED_IFF",
            "scope": "DP=0 and tidal operator commutes with P",
        },
        {
            "claim": "scalar Jacobi-reciprocal generator criterion",
            "status": "UNIQUE_CONDITION_CHARACTERIZED",
            "scope": "for nonzero rate real similarity iff K=-a^2",
        },
        {
            "claim": "WRL clock-transverse scalar profile relation",
            "status": "DERIVED_LOCAL",
            "scope": "R=X(1-Q^-2) centered residual",
        },
        {
            "claim": "WRL pointwise natural-frame clock-transverse generator solder",
            "status": "NO_POINTWISE_SIMILARITY_IN_EXACT_LOCAL_RADIAL_CONTROL",
            "scope": "positive screen K versus hyperbolic nonzero clock generator; arbitrary path-dependent H not excluded or selected",
        },
        {
            "claim": "dphi 3plus3 clock-to-Jacobi solder",
            "status": "OPEN_NOT_DERIVED",
            "scope": "two-form sectors do not select rank2 screen phase subbundle",
        },
        {
            "claim": "prior matched reciprocal-angular intertwiner",
            "status": "CONDITIONAL_RETAINED",
            "scope": "matched angular representation mirror and relative normalization remain inputs",
        },
        {
            "claim": "intrinsic irreducible clock-transverse solder",
            "status": "OPEN_NO_REGISTERED_WITNESS",
            "scope": "complete registered linear and connection-level candidate set",
        },
        {
            "claim": "direct-sum common-path cocycle",
            "status": "DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY",
            "scope": "reducible typed path data",
        },
        {
            "claim": "complete nontrivial all-observer realization",
            "status": "OPEN",
            "scope": "no complete branch satisfies all gates",
        },
        {
            "claim": "action source carrier density bootstrap physical Xmax",
            "status": "OPEN_EXCLUDED",
            "scope": "not used or derived",
        },
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], statuses)

    result = {
        "result": "PASS",
        "preregistration_commit": PREREG_COMMIT,
        "check_count": len(checks),
        "checks": checks,
        "source_count": source_count,
        "candidate_count": len(candidates),
        "generator_control_count": len(generator_rows),
        "branch_count": len(branches),
        "causal_class_count": len(causal_rows),
        "completion_count": len(completion_rows),
        "equation_family_count": len(equations),
        "derived_positive": [
            "ORIENTED_NORMAL_SCREEN_AREA_HODGE_DUALITY_GIVEN_TYPED_SPLIT",
            "PARALLEL_TIDAL_INVARIANT_SCREEN_LINE_IFF_CRITERION",
            "POINTWISE_NATURAL_FRAME_NONTRIVIAL_SCALAR_GENERATOR_MATCH_IFF_K_EQUALS_MINUS_A_SQUARED",
            "WRL_CENTERED_SCALAR_PROFILE_RELATION_R_EQUALS_X_ONE_MINUS_Q_INVERSE_SQUARED",
        ],
        "intrinsic_irreducible_solder": "OPEN_NO_REGISTERED_WITNESS",
        "direct_sum_cocycle": "DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY",
        "cross_branch_splice": "FORBIDDEN_NOT_USED",
        "physical_Xmax": "OPEN",
        "maximum_scope": "REGISTERED_LOCAL_LINEAR_AND_CONNECTION_LEVEL_CANDIDATES",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
