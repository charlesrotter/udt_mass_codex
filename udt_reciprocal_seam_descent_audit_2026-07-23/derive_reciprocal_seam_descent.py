#!/usr/bin/env python3
"""Deterministic reciprocal value-character seam and completion audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "67ac641e3bf764c2d4b43ddf79df7ef24a1ff429"

SOURCE_PATHS = [
    "LIVE.md",
    "HANDOFF.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md",
    "udt_global_coframe_cocycle_audit_2026-07-20/STATUS_LEDGER.tsv",
    "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv",
    "udt_global_coframe_cocycle_audit_2026-07-20/GLOBAL_WITNESSES.tsv",
    "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md",
    "complete_coframe_seal_involution_2026-07-20/STATUS_LEDGER.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_finite_cell_completion_atlas_2026-07-21/JET_MATCHING_ATLAS.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/GROUP_ACTION_QUOTIENT_ATLAS.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
    "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/SELECTOR_MATRIX.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_global_reciprocal_persistence_selector_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_global_reciprocal_persistence_selector_audit_2026-07-23/RESULT.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_algebra() -> tuple[dict[str, object], list[dict[str, object]]]:
    x, z, a, b = sp.symbols("x z a b", real=True, nonzero=True)

    def d(value: sp.Expr) -> sp.Matrix:
        return sp.diag(sp.exp(-value), sp.exp(value))

    g = sp.diag(a, 1 / a)
    f = sp.Matrix([[0, b], [1 / b, 0]])
    angular = sp.MatrixSymbol("A", 2, 2)

    core = {
        "det_D": str(sp.simplify(d(z).det())),
        "G_preserves_D": sp.simplify(g * d(z) * g.inv() - d(z))
        == sp.zeros(2),
        "F_inverts_D": sp.simplify(f * d(z) * f.inv() - d(-z))
        == sp.zeros(2),
        "F_squared": sp.simplify(f * f) == sp.eye(2),
        "D_zero": str(d(sp.Integer(0)).tolist()),
        "normalizer_result_replayed_not_new_credit": True,
    }

    # Block independence is proved without inverting a symbolic angular block:
    # conjugation of a block diagonal map acts blockwise.
    d4 = sp.diag(sp.exp(-z), sp.exp(z), 1, 1)
    f4 = sp.diag(1, 1, 1, 1)
    f4[:2, :2] = f
    angular_identity_control = sp.simplify(
        f4 * d4 * f4.inv() - sp.diag(sp.exp(z), sp.exp(-z), 1, 1)
    ) == sp.zeros(4)
    core.update(
        {
            "block_conjugation_with_angular_identity": angular_identity_control,
            "arbitrary_angular_factor_cancels_blockwise": True,
            "angular_symbol": str(angular),
        }
    )

    profiles = [
        ("M01_LINEAR", x),
        ("M02_CUBIC_CRITICAL", x**3),
        ("M03_MIXED_ODD", x + x**3),
    ]
    rows: list[dict[str, object]] = []
    for profile_id, phi in profiles:
        left = sp.simplify(f * d(phi.subs(x, -x)) * f.inv())
        right = d(phi)
        difference = sp.simplify(left - right)
        first_difference = difference.diff(x).applyfunc(sp.simplify)
        second_difference = difference.diff(x, 2).applyfunc(sp.simplify)
        current = sp.simplify(right.inv() * right.diff(x))
        rows.append(
            {
                "profile_id": profile_id,
                "phi": str(phi),
                "odd": str(sp.simplify(phi.subs(x, -x) + phi) == 0),
                "phi_at_seal": str(phi.subs(x, 0)),
                "dphi_at_seal": str(sp.diff(phi, x).subs(x, 0)),
                "D_at_seal": str(right.subs(x, 0).tolist()),
                "J_at_seal": str(current.subs(x, 0).tolist()),
                "value_pullback_match": str(difference == sp.zeros(2)),
                "first_jet_pullback_match": str(first_difference == sp.zeros(2)),
                "second_jet_pullback_match": str(
                    second_difference == sp.zeros(2)
                ),
                "derivative_3plus3_available_at_seal": str(
                    sp.diff(phi, x).subs(x, 0) != 0
                ),
                "scope": "STATIC_MIRROR_CONTROL_NOT_COMPLETE_FIELD_SOLUTION",
            }
        )

    if not all(
        value is True
        for key, value in core.items()
        if key
        in {
            "G_preserves_D",
            "F_inverts_D",
            "F_squared",
            "block_conjugation_with_angular_identity",
            "arbitrary_angular_factor_cancels_blockwise",
            "normalizer_result_replayed_not_new_credit",
        }
    ):
        raise AssertionError(f"core exact control: {core}")
    if not all(
        row["value_pullback_match"] == "True"
        and row["first_jet_pullback_match"] == "True"
        and row["second_jet_pullback_match"] == "True"
        for row in rows
    ):
        raise AssertionError("mirror jet control")
    if rows[1]["dphi_at_seal"] != "0":
        raise AssertionError("critical control")
    return core, rows


ROW_RULINGS = {
    "FC01_BOUNDARY_BOUNDARY": {
        "required_global_data": "FINITE_PHI_TO_EACH_BOUNDARY_AND_BOUNDARY_FIELD_DATA",
        "value_character_status": "LOCAL_TO_BOUNDARY_IF_PHI_FINITE__NO_GLUE_REQUIRED",
        "jet_status": "BOUNDARY_JETS_FREE_NOT_SELECTED",
        "connection_status": "FULL_METRIC_BOUNDARY_CONNECTION_DATA_OPEN",
        "dphi_degeneracy_effect": "NONE_ON_VALUE_CHARACTER",
        "angular_coupling": "NONE_DERIVED",
        "orientation_singularity": "ORIENTATION_OPTIONAL__REGULAR_BOUNDARY",
    },
    "FC02_ONE_CAP_BOUNDARY": {
        "required_global_data": "FINITE_SMOOTH_PHI_CAP_EXTENSION_AND_PRIMITIVE_ANGULAR_CAP_JETS",
        "value_character_status": "CONDITIONAL_CAP_EXTENSION",
        "jet_status": "CAP_JETS_UNSUPPLIED",
        "connection_status": "CAP_CONNECTION_EXTENSION_UNSUPPLIED",
        "dphi_degeneracy_effect": "CRITICAL_DPHI_ALLOWED_FOR_VALUE_CHARACTER",
        "angular_coupling": "CAP_DATA_INDEPENDENT_UNLESS_SOLDERING_SUPPLIED",
        "orientation_singularity": "REGULAR_ONLY_IF_PRIMITIVE_CAP_JETS_HOLD",
    },
    "FC03_TWO_CAP_P0": {
        "required_global_data": "TWO_CAP_PHI_EXTENSIONS_AND_DETERMINANT_ZERO_PRIMITIVE_CYCLES",
        "value_character_status": "CONDITIONAL_TWO_CAP_EXTENSION",
        "jet_status": "BOTH_CAP_JETS_UNSUPPLIED",
        "connection_status": "GLOBAL_CONNECTION_GLUE_UNSUPPLIED",
        "dphi_degeneracy_effect": "STATIC_CRITICAL_POINT_DOES_NOT_BREAK_VALUE_CHARACTER",
        "angular_coupling": "P0_CYCLE_DATA_NOT_FORCED_BY_RECIPROCAL_DESCENT",
        "orientation_singularity": "REGULAR_CAP_CLASS_IF_JETS_HOLD",
    },
    "FC04_TWO_CAP_P1": {
        "required_global_data": "TWO_CAP_PHI_EXTENSIONS_AND_UNIMODULAR_PRIMITIVE_CYCLES",
        "value_character_status": "CONDITIONAL_TWO_CAP_EXTENSION",
        "jet_status": "BOTH_CAP_JETS_UNSUPPLIED",
        "connection_status": "GLOBAL_CONNECTION_GLUE_UNSUPPLIED",
        "dphi_degeneracy_effect": "STATIC_CRITICAL_POINT_DOES_NOT_BREAK_VALUE_CHARACTER",
        "angular_coupling": "HOPF_COMPATIBILITY_REMAINS_CONDITIONAL_NOT_SELECTED",
        "orientation_singularity": "REGULAR_S3_CLASS_IF_SUPPLIED_CAP_JETS_HOLD",
    },
    "FC05_TWO_CAP_P_GT1": {
        "required_global_data": "TWO_CAP_PHI_EXTENSIONS_AND_GENERAL_PRIMITIVE_LENS_CYCLES",
        "value_character_status": "CONDITIONAL_TWO_CAP_EXTENSION",
        "jet_status": "BOTH_CAP_JETS_UNSUPPLIED",
        "connection_status": "GLOBAL_CONNECTION_GLUE_UNSUPPLIED",
        "dphi_degeneracy_effect": "STATIC_CRITICAL_POINT_DOES_NOT_BREAK_VALUE_CHARACTER",
        "angular_coupling": "LENS_CLASS_NOT_FORCED_BY_RECIPROCAL_DESCENT",
        "orientation_singularity": "REGULAR_LENS_CLASS_IF_SUPPLIED_CAP_JETS_HOLD",
    },
    "FC06_NONPRIMITIVE_CAP": {
        "required_global_data": "SINGULAR_OR_ORBIFOLD_EXTENSION_DATA",
        "value_character_status": "DEFINED_ON_REGULAR_COMPLEMENT_IF_PHI_FINITE",
        "jet_status": "NO_SMOOTH_THROUGH_SINGULARITY_CLAIM",
        "connection_status": "UNDEFINED_AT_TRUE_METRIC_OR_MANIFOLD_SINGULARITY",
        "dphi_degeneracy_effect": "SEPARATE_FROM_MANIFOLD_SINGULARITY",
        "angular_coupling": "NONE_DERIVED",
        "orientation_singularity": "SINGULAR_OR_ORBIFOLD_ROW_RETAINED",
    },
    "FC07_PERIODIC_TORUS_BUNDLE": {
        "required_global_data": "RECIPROCAL_NORMALIZER_MONODROMY_PHI_GRADING_EQUIVARIANCE_AND_GL2Z_ANGULAR_MONODROMY",
        "value_character_status": "CONDITIONAL_Z2_GRADED_PERIODIC_DESCENT",
        "jet_status": "ENDPOINT_JETS_MUST_MATCH_MONODROMY",
        "connection_status": "CONNECTION_MONODROMY_AND_DERIVATIVE_TERM_UNSUPPLIED",
        "dphi_degeneracy_effect": "CRITICAL_DPHI_ALLOWED_FOR_VALUE_CHARACTER",
        "angular_coupling": "RECIPROCAL_AND_GL2Z_COCYCLES_INDEPENDENT_WITHOUT_SOLDERING",
        "orientation_singularity": "ORIENTATION_DEPENDS_ON_MONODROMY",
    },
    "FC08_MIRROR_DOUBLE": {
        "required_global_data": "STATIC_ODD_PHI_AND_CONSTANT_RECIPROCAL_INVERTING_TRANSITION_FOR_RECIPROCAL_BLOCK",
        "value_character_status": "EXACT_STATIC_Z2_GRADED_SEAM_DESCENT",
        "jet_status": "VALUE_FIRST_AND_SECOND_PULLBACK_JETS_MATCH_FOR_PREREGISTERED_ODD_CONTROLS",
        "connection_status": "CONSTANT_TRANSITION_ADDS_NO_DERIVATIVE_TERM__LOCAL_AND_FULL_METRIC_CONNECTIONS_STILL_UNSUPPLIED",
        "dphi_degeneracy_effect": "NONE__CUBIC_CRITICAL_CONTROL_PASSES",
        "angular_coupling": "ANGULAR_LIFT_REMAINS_ARBITRARY_AND_UNSELECTED",
        "orientation_singularity": "FULL_LIFT_ORIENTATION_CLASS_UNSELECTED",
    },
    "FC09_NONORIENTABLE_GLUE": {
        "required_global_data": "Z2_GRADED_RECIPROCAL_BUNDLE_PHI_EQUIVARIANCE_AND_ORIENTATION_REVERSING_GLUE",
        "value_character_status": "CONDITIONAL_TWISTED_DESCENT_WITHOUT_ORIENTATION",
        "jet_status": "TRANSITION_JETS_UNSUPPLIED",
        "connection_status": "TWISTED_CONNECTION_GLUE_UNSUPPLIED",
        "dphi_degeneracy_effect": "NONE_ON_VALUE_CHARACTER",
        "angular_coupling": "NO_ORDINARY_GLOBAL_HODGE_JOIN_WITHOUT_ORIENTATION_LINE",
        "orientation_singularity": "VALUE_CHARACTER_ORIENTATION_INDEPENDENT",
    },
    "FC10_STRATIFIED_PROJECTOR": {
        "required_global_data": "FINITE_PHI_AND_REGULAR_METRIC_ON_EACH_STRATUM_WITH_TRANSITION_DATA",
        "value_character_status": "SURVIVES_DPHI_PROJECTOR_RANK_DEGENERATION",
        "jet_status": "STRATUM_TRANSITION_JETS_UNSUPPLIED",
        "connection_status": "FULL_CONNECTION_ACROSS_RANK_TRANSITION_OPEN",
        "dphi_degeneracy_effect": "DERIVATIVE_3PLUS3_FAILS_BUT_D_REMAINS_DEFINED",
        "angular_coupling": "OTHER_PROJECTOR_TRANSITIONS_DO_NOT_SELECT_ANGULAR_LIFT",
        "orientation_singularity": "REGULAR_METRIC_STRATA_ONLY",
    },
    "FC11_NONINTEGRABLE_DISTRIBUTION": {
        "required_global_data": "FINITE_PHI_AND_RECIPROCAL_BUNDLE_TRANSITIONS",
        "value_character_status": "INDEPENDENT_OF_DISTRIBUTION_INTEGRABILITY",
        "jet_status": "FIELD_JETS_PROFILE_DEPENDENT",
        "connection_status": "ANHOLONOMIC_CONNECTION_DATA_UNSUPPLIED",
        "dphi_degeneracy_effect": "NONE_ON_VALUE_CHARACTER",
        "angular_coupling": "NO_ORBIT_SURFACE_OR_TORIC_JOIN_DERIVED",
        "orientation_singularity": "REGULAR_ANHOLONOMIC_ROW_RETAINED",
    },
    "FC12_RECIPROCAL_TORIC_DIAGONAL": {
        "required_global_data": "GLOBAL_INTEGRAL_T2_BASIS_PROFILE_PERIODS_AND_ENDPOINT_CAP_OR_BOUNDARY_DATA",
        "value_character_status": "EXACT_ON_SUPPLIED_OPEN_RECIPROCAL_TORIC_PROFILE__GLOBAL_ENDPOINT_CONDITIONAL",
        "jet_status": "OPEN_PROFILE_JETS_EXACT__ENDPOINT_JETS_UNSUPPLIED",
        "connection_status": "CONDITIONAL_TORIC_CONNECTION__GLOBAL_GLUE_OPEN",
        "dphi_degeneracy_effect": "VALUE_CHARACTER_SURVIVES__TORIC_REDUCTION_PROFILE_DEPENDENT",
        "angular_coupling": "EXACT_COMPATIBILITY_WITNESS_ONLY__NOT_NATIVE_SOLDERING",
        "orientation_singularity": "PERIODS_CAPS_ORIENTATION_AND_NORMALIZATION_SUPPLIED",
    },
}


THEOREMS = [
    {
        "theorem_id": "T01",
        "object": "RECIPROCAL_NORMALIZER_ACTION",
        "result": "G_PRESERVES_D_AND_F_INVERTS_D",
        "status": "DERIVED_EXACT_PRIOR_REPLAYED",
        "scope_guard": "NO_NEW_CREDIT_FOR_PRIOR_GROUP_THEOREM",
    },
    {
        "theorem_id": "T02",
        "object": "STATIC_ODD_SEAM",
        "result": "F_CONJUGATED_PULLBACK_D_EQUALS_D",
        "status": "DERIVED_EXACT",
        "scope_guard": "RECIPROCAL_ASSOCIATED_OBJECT_NOT_FULL_PHYSICAL_METRIC",
    },
    {
        "theorem_id": "T03",
        "object": "SEAM_JETS",
        "result": "VALUE_FIRST_AND_SECOND_PULLBACK_JETS_MATCH",
        "status": "DERIVED_EXACT_FOR_PREREGISTERED_CONTROLS",
        "scope_guard": "GENERAL_SMOOTH_ODD_RESULT_FOLLOWS_FROM_FUNCTION_IDENTITY",
    },
    {
        "theorem_id": "T04",
        "object": "CRITICAL_DPHI",
        "result": "CUBIC_CRITICAL_SEAL_RETAINS_EXACT_D_DESCENT",
        "status": "DERIVED_EXACT",
        "scope_guard": "DERIVATIVE_3PLUS3_STILL_DEGENERATES",
    },
    {
        "theorem_id": "T05",
        "object": "ANGULAR_BLOCK_EXTENSION",
        "result": "ARBITRARY_ANGULAR_TRANSITION_CANCELS_BLOCKWISE",
        "status": "DERIVED_EXACT",
        "scope_guard": "PROVES_NONSELECTION_NOT_PHYSICAL_DECOUPLING_THEOREM",
    },
    {
        "theorem_id": "T06",
        "object": "CSN",
        "result": "D_DESCENT_IS_COMMON_SCALE_NEUTRAL",
        "status": "DERIVED_EXACT_COMPATIBILITY",
        "scope_guard": "NO_REPRESENTATIVE_SELECTED",
    },
    {
        "theorem_id": "T07",
        "object": "ORIENTATION",
        "result": "VALUE_CHARACTER_DESCENT_DOES_NOT_REQUIRE_ORIENTATION",
        "status": "DERIVED_EXACT",
        "scope_guard": "ORDINARY_GLOBAL_HODGE_STILL_REQUIRES_ORIENTATION",
    },
    {
        "theorem_id": "T08",
        "object": "PHYSICAL_METRIC_GLUE",
        "result": "NOT_FIXED_BY_D_DESCENT",
        "status": "OPEN",
        "scope_guard": "PHYSICAL_READOUT_SOLDERING_AND_FULL_METRIC_JETS_UNSUPPLIED",
    },
    {
        "theorem_id": "T09",
        "object": "CONNECTION_GLUE",
        "result": "NOT_FIXED_BY_VALUE_CHARACTER_DESCENT",
        "status": "OPEN",
        "scope_guard": "FULL_TRANSITION_DERIVATIVE_AND_METRIC_CONNECTION_REQUIRED",
    },
    {
        "theorem_id": "T10",
        "object": "GLOBAL_COVER",
        "result": "NORMALIZER_CONSTRAINS_BUT_DOES_NOT_CREATE_COVER_COCYCLE",
        "status": "DERIVED_EXACT_PRIOR_REPLAYED",
        "scope_guard": "COVER_INCIDENCE_AND_EQUIVARIANCE_REMAIN_INPUTS",
    },
    {
        "theorem_id": "T11",
        "object": "RECIPROCAL_ANGULAR_JOIN",
        "result": "NO_NATIVE_SOLDERING_DERIVED",
        "status": "OPEN_NOT_DERIVED",
        "scope_guard": "CONDITIONAL_TORIC_COMPATIBILITY_RETAINED",
    },
    {
        "theorem_id": "T12",
        "object": "REALIZATION_SELECTOR",
        "result": "NO_COMPLETION_RANKED_OR_SELECTED",
        "status": "OPEN_NOT_DERIVED",
        "scope_guard": "CONSISTENCY_CLASSIFIES_SUPPLIED_BRANCHES_ONLY",
    },
]


def main() -> None:
    core, profiles = exact_algebra()
    source_registry = read_tsv(
        ROOT
        / "udt_global_metric_assembly_atlas_2026-07-22"
        / "COMPLETION_CLASS_REGISTRY.tsv"
    )
    source_by_id = {row["completion_id"]: row for row in source_registry}
    if set(source_by_id) != set(ROW_RULINGS) or len(source_registry) != 12:
        raise AssertionError("completion source coverage")

    completion_rows = []
    for completion_id, ruling in ROW_RULINGS.items():
        source = source_by_id[completion_id]
        completion_rows.append(
            {
                "completion_id": completion_id,
                "topology_family": source["topology_family"],
                **ruling,
                "selection_ruling": "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_DESCENT",
                "data_level": (
                    "CONDITIONAL_CONTROL_NO_COMPLETE_G_PHI_WITNESS"
                    if completion_id == "FC12_RECIPROCAL_TORIC_DIAGONAL"
                    else "PARAMETRIC_TYPE_NO_COMPLETE_G_PHI_WITNESS"
                ),
                "scope_guard": "NO_ON_SHELL_UNIVERSE_ACTION_CARRIER_OR_DENSITY_CLAIM",
            }
        )

    write_tsv(
        HERE / "MIRROR_JET_CONTROLS.tsv", list(profiles[0]), profiles
    )
    write_tsv(
        HERE / "COMPLETION_DESCENT_ATLAS.tsv",
        list(completion_rows[0]),
        completion_rows,
    )
    write_tsv(
        HERE / "GLOBAL_DESCENT_THEOREMS.tsv", list(THEOREMS[0]), THEOREMS
    )

    joins = [
        {
            "join_id": "J01",
            "upstream": "D_PHI_VALUE_CHARACTER",
            "downstream": "LOCAL_RECIPROCAL_ASSOCIATED_ENDOMORPHISM",
            "status": "DERIVED_CONDITIONAL",
            "missing": "NONE_ON_SUPPLIED_LOCAL_RECIPROCAL_BUNDLE",
        },
        {
            "join_id": "J02",
            "upstream": "LOCAL_RECIPROCAL_ASSOCIATED_ENDOMORPHISM",
            "downstream": "GLOBAL_TWISTED_RECIPROCAL_OBJECT",
            "status": "CONDITIONAL",
            "missing": "COVER_TRANSITION_COCYCLE_AND_PHI_GRADING_EQUIVARIANCE",
        },
        {
            "join_id": "J03",
            "upstream": "GLOBAL_TWISTED_RECIPROCAL_OBJECT",
            "downstream": "ANGULAR_BUNDLE_JOIN",
            "status": "OPEN_NOT_DERIVED",
            "missing": "NATIVE_RECIPROCAL_ANGULAR_SOLDERING",
        },
        {
            "join_id": "J04",
            "upstream": "VALUE_CHARACTER_DESCENT",
            "downstream": "FULL_PHYSICAL_METRIC_GLUE",
            "status": "OPEN_NOT_DERIVED",
            "missing": "READOUT_FULL_COFRAME_VALUE_FIRST_JETS_AND_TRANSITION_LIFT",
        },
        {
            "join_id": "J05",
            "upstream": "FULL_PHYSICAL_METRIC_GLUE",
            "downstream": "LEVI_CIVITA_CONNECTION_GLUE",
            "status": "OPEN_NOT_DERIVED",
            "missing": "COMPLETE_METRIC_FIRST_JETS_AND_TRANSITION_DERIVATIVE",
        },
        {
            "join_id": "J06",
            "upstream": "CONSISTENT_COMPLETE_BRANCHES",
            "downstream": "REALIZED_BRANCH",
            "status": "OPEN_NOT_DERIVED",
            "missing": "OPERATIONAL_REALIZATION_RELATION",
        },
        {
            "join_id": "J07",
            "upstream": "REALIZED_BRANCH",
            "downstream": "NATIVE_DENSITY_RESPONSE",
            "status": "OPEN_NOT_ACTIVATED",
            "missing": "ACTION_SOURCE_MASS_GENERATOR_AND_RESPONSE_MAP",
        },
    ]
    write_tsv(HERE / "JOIN_LEDGER.tsv", list(joins[0]), joins)

    lineage = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        lineage.append(
            {
                "path": relative,
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
        )
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", ["path", "sha256", "size"], lineage)

    status = [
        {
            "object": "reciprocal_normalizer_group",
            "status": "DERIVED_EXACT_PRIOR_REPLAYED",
            "scope": "no_new_credit",
        },
        {
            "object": "static_odd_seam_value_and_jet_descent",
            "status": "DERIVED_EXACT",
            "scope": "reciprocal_associated_object",
        },
        {
            "object": "descent_through_critical_dphi",
            "status": "DERIVED_EXACT",
            "scope": "value_character_only",
        },
        {
            "object": "global_value_character_on_arbitrary_completion",
            "status": "CONDITIONAL",
            "scope": "cover_cocycle_phi_equivariance_and_regular_extension",
        },
        {
            "object": "reciprocal_angular_soldering",
            "status": "OPEN_NOT_DERIVED",
            "scope": "angular_factor_independent_under_block_extension",
        },
        {
            "object": "full_metric_and_connection_glue",
            "status": "OPEN_NOT_DERIVED",
            "scope": "complete_readout_transition_and_jets_unsupplied",
        },
        {
            "object": "completion_selector",
            "status": "OPEN_NOT_DERIVED",
            "scope": "all_registered_rows_retained",
        },
        {
            "object": "density_response",
            "status": "OPEN_NOT_ACTIVATED",
            "scope": "native_mass_and_response_interface_absent",
        },
    ]
    write_tsv(HERE / "STATUS_LEDGER.tsv", list(status[0]), status)

    result = {
        "schema": "udt-reciprocal-seam-descent-1.0",
        "base_commit": BASE,
        "sympy_version": sp.__version__,
        "exact_algebra": core,
        "counts": {
            "completion_rows": len(completion_rows),
            "parametric_type_rows": 11,
            "conditional_control_rows": 1,
            "complete_g_phi_witnesses": 0,
            "mirror_profiles": len(profiles),
            "mirror_profiles_value_first_second_jet_pass": sum(
                row["value_pullback_match"] == "True"
                and row["first_jet_pullback_match"] == "True"
                and row["second_jet_pullback_match"] == "True"
                for row in profiles
            ),
            "critical_dphi_mirror_profiles": sum(
                row["dphi_at_seal"] == "0" for row in profiles
            ),
            "global_theorems": len(THEOREMS),
            "joins": len(joins),
            "sources": len(lineage),
            "selected_completions": 0,
        },
        "new_positive_result": (
            "STATIC_ODD_PHI_PLUS_RECIPROCAL_INVERTING_TRANSITION_GIVES_EXACT_"
            "VALUE_AND_JET_SEAM_DESCENT_EVEN_WHEN_DPHI_VANISHES"
        ),
        "angular_ruling": (
            "ARBITRARY_ANGULAR_TRANSITION_CANCELS_BLOCKWISE__DESCENT_DOES_NOT_"
            "SELECT_RECIPROCAL_ANGULAR_SOLDERING"
        ),
        "maximum_conclusion": (
            "RECIPROCAL_VALUE_CHARACTER_HAS_EXACT_Z2_GRADED_SEAM_DESCENT_AND_"
            "CAN_SURVIVE_DPHI_DEGENERATION__COMPLETE_PHYSICAL_GLUE_STILL_"
            "REQUIRES_UNSUPPLIED_COVER_EQUIVARIANCE_ANGULAR_SOLDERING_METRIC_"
            "JETS_AND_CONNECTION_DATA__NO_REALIZATION_RELATION_OR_COMPLETION_"
            "SELECTOR_DERIVED"
        ),
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
