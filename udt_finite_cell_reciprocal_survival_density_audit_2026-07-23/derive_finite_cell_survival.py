#!/usr/bin/env python3
"""Deterministic finite-cell reciprocal-survival and density-interface audit."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

COMPLETION_SOURCE = (
    ROOT
    / "udt_global_metric_assembly_atlas_2026-07-22"
    / "COMPLETION_CLASS_REGISTRY.tsv"
)
DENSITY_SOURCE = (
    ROOT
    / "udt_global_metric_assembly_atlas_2026-07-22"
    / "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv"
)

SOURCE_PATHS = [
    "LIVE.md",
    "HANDOFF.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/RESULT.json",
    "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
    "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/STAGE_GATE_LEDGER.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/AUDIT_REPORT.md",
    "udt_finite_cell_completion_atlas_2026-07-21/GLOBAL_INCIDENCE_ATLAS.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/CAUSAL_TIME_LIVE_ATLAS.tsv",
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md",
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv",
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


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def induced_two_form_map(endomorphism: sp.Matrix) -> sp.Matrix:
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    result = sp.zeros(6)
    for column, (a, b) in enumerate(pairs):
        for row, (i, j) in enumerate(pairs):
            result[row, column] = (
                endomorphism[i, a] * int(j == b)
                - endomorphism[j, a] * int(i == b)
                + endomorphism[j, b] * int(i == a)
                - endomorphism[i, b] * int(j == a)
            )
    return result


def local_exact_controls() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    eta_inv = eta.inv()
    identity4 = sp.eye(4)
    identity6 = sp.eye(6)

    controls: dict[str, object] = {}
    ranks: dict[str, dict[str, object]] = {}
    for name, alpha in {
        "timelike": sp.Matrix([1, 0, 0, 0]),
        "spacelike": sp.Matrix([0, 1, 0, 0]),
    }.items():
        raised = eta_inv * alpha
        norm = (alpha.T * raised)[0]
        projector = sp.simplify(raised * alpha.T / norm)
        induced = induced_two_form_map(projector)
        complement = identity6 - induced
        ranks[name] = {
            "norm": str(norm),
            "tangent_rank": projector.rank(),
            "two_form_parallel_rank": induced.rank(),
            "two_form_transverse_rank": complement.rank(),
            "tangent_idempotent": projector**2 == projector,
            "parallel_idempotent": induced**2 == induced,
            "transverse_idempotent": complement**2 == complement,
            "complementary": induced * complement == sp.zeros(6),
        }

    null_alpha = sp.Matrix([1, 1, 0, 0])
    null_raised = eta_inv * null_alpha
    null_map = null_raised * null_alpha.T
    null_induced = induced_two_form_map(null_map)
    zero_alpha = sp.zeros(4, 1)

    t, x = sp.symbols("t x", real=True)
    examples = {
        "boundary_spacelike_phi_x_norm": str(
            sp.simplify((sp.Matrix([0, 1, 0, 0]).T * eta_inv * sp.Matrix([0, 1, 0, 0]))[0])
        ),
        "boundary_timelike_phi_t_norm": str(
            sp.simplify((sp.Matrix([1, 0, 0, 0]).T * eta_inv * sp.Matrix([1, 0, 0, 0]))[0])
        ),
        "retained_boundary_critical_phi_x1mx_norm": str((1 - 2 * x) ** 2),
        "retained_boundary_critical_location": "x=1/2",
        "periodic_phi_sin_x_norm": str(sp.cos(x) ** 2),
        "periodic_critical_locations": "x=pi/2+k*pi",
        "even_mirror_phi_x2_norm": str(4 * x**2),
        "even_mirror_critical_location": "x=0",
        "odd_double_phi_x_norm": "1",
        "odd_double_descends_as_ordinary_scalar_to_reflection_quotient": False,
        "causal_transition_phi_tx_norm": str(sp.expand(t**2 - x**2)),
        "causal_transition_null_locus": "t=+/-x",
    }

    controls["ranks"] = ranks
    controls["null"] = {
        "norm": str((null_alpha.T * null_raised)[0]),
        "tangent_rank": null_map.rank(),
        "tangent_nonzero": null_map != sp.zeros(4),
        "tangent_nilpotent": null_map**2 == sp.zeros(4),
        "two_form_rank": null_induced.rank(),
        "two_form_nonzero": null_induced != sp.zeros(6),
        "two_form_nilpotent": null_induced**2 == sp.zeros(6),
    }
    controls["zero"] = {
        "covector_rank": zero_alpha.rank(),
        "normalized_projector_defined": False,
    }
    controls["examples"] = examples

    booleans: list[bool] = []
    for values in ranks.values():
        booleans.extend(value for value in values.values() if isinstance(value, bool))
    booleans.extend(
        value for value in controls["null"].values() if isinstance(value, bool)
    )
    if not all(booleans):
        raise AssertionError(f"local exact control failed: {controls}")
    return controls


BRANCH_RULINGS = {
    "FC01_BOUNDARY_BOUNDARY": {
        "static_spatial_phi": "POSSIBLE_IF_GLOBAL_SUBMERSION_NONNULL__NOT_FORCED",
        "time_live_phi": "POSSIBLE_IF_GLOBAL_NONNULL_GRADIENT__NOT_FORCED",
        "projector_survival": "CONDITIONAL_ON_UNSUPPLIED_G_PHI_PROFILE_AND_BOUNDARY_DATA",
        "hodge_exchange": "CONDITIONAL_ON_ORIENTATION_AND_NONNULL_DPHI",
        "global_behavior": "BOUNDARIES_DO_NOT_FORCE_A_CRITICAL_POINT_BUT_SUPPLY_NO_PROFILE",
    },
    "FC02_ONE_CAP_BOUNDARY": {
        "static_spatial_phi": "COHOMOGENEITY_ONE_SMOOTH_CAP_FORCES_CRITICAL_DPHI__GENERAL_STATIC_FIELD_OPEN",
        "time_live_phi": "TIME_COMPONENT_CAN_EVADE_CAP_CRITICALITY__NOT_FORCED",
        "projector_survival": "CONDITIONAL_AND_CAP_EXTENSION_PROFILE_DEPENDENT",
        "hodge_exchange": "CONDITIONAL_ON_ORIENTATION_CAP_REGULARITY_AND_NONNULL_DPHI",
        "global_behavior": "CAP_JETS_AND_FULL_FIELD_PROFILE_REQUIRED",
    },
    "FC03_TWO_CAP_P0": {
        "static_spatial_phi": "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT",
        "time_live_phi": "TIME_LIVE_NONNULL_GRADIENT_MAY_EVADE_STATIC_OBSTRUCTION__NOT_FORCED",
        "projector_survival": "OBSTRUCTED_FOR_STATIC_REAL_PHI__CONDITIONAL_TIME_LIVE",
        "hodge_exchange": "ORIENTABLE_CLASS_BUT_DPHI_DOMAIN_OPEN",
        "global_behavior": "STATIC_3PLUS3_CANNOT_SURVIVE_ENTIRE_COMPACT_SLICE",
    },
    "FC04_TWO_CAP_P1": {
        "static_spatial_phi": "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT",
        "time_live_phi": "TIME_LIVE_NONNULL_GRADIENT_MAY_EVADE_STATIC_OBSTRUCTION__NOT_FORCED",
        "projector_survival": "OBSTRUCTED_FOR_STATIC_REAL_PHI__CONDITIONAL_TIME_LIVE",
        "hodge_exchange": "ORIENTABLE_CLASS_BUT_DPHI_DOMAIN_OPEN",
        "global_behavior": "STATIC_3PLUS3_CANNOT_SURVIVE_ENTIRE_COMPACT_SLICE",
    },
    "FC05_TWO_CAP_P_GT1": {
        "static_spatial_phi": "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT",
        "time_live_phi": "TIME_LIVE_NONNULL_GRADIENT_MAY_EVADE_STATIC_OBSTRUCTION__NOT_FORCED",
        "projector_survival": "OBSTRUCTED_FOR_STATIC_REAL_PHI__CONDITIONAL_TIME_LIVE",
        "hodge_exchange": "ORIENTABLE_CLASS_BUT_DPHI_DOMAIN_OPEN",
        "global_behavior": "STATIC_3PLUS3_CANNOT_SURVIVE_ENTIRE_COMPACT_SLICE",
    },
    "FC06_NONPRIMITIVE_CAP": {
        "static_spatial_phi": "SINGULAR_OR_ORBIFOLD_STRATUM_REQUIRES_SEPARATE_EXTENSION_DATA",
        "time_live_phi": "TIME_DEPENDENCE_DOES_NOT_REPAIR_UNDEFINED_SINGULAR_GEOMETRY",
        "projector_survival": "DEFINED_ONLY_ON_REGULAR_NONNULL_DPHI_COMPLEMENT",
        "hodge_exchange": "UNDEFINED_AT_TRUE_METRIC_OR_MANIFOLD_SINGULARITY",
        "global_behavior": "NO_THROUGH_SINGULARITY_GLOBAL_CLAIM",
    },
    "FC07_PERIODIC_TORUS_BUNDLE": {
        "static_spatial_phi": "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT",
        "time_live_phi": "TIME_LIVE_NONNULL_GRADIENT_MAY_EVADE_STATIC_OBSTRUCTION__NOT_FORCED",
        "projector_survival": "OBSTRUCTED_FOR_STATIC_REAL_PHI__CONDITIONAL_TIME_LIVE",
        "hodge_exchange": "GL2Z_ORIENTATION_AND_DPHI_GLUE_DEPENDENT",
        "global_behavior": "PERIODIC_REAL_SCALAR_CANNOT_BE_MONOTONE_AROUND_BASE",
    },
    "FC08_MIRROR_DOUBLE": {
        "static_spatial_phi": "MIRROR_INVARIANT_SMOOTH_PHI_HAS_ZERO_NORMAL_DERIVATIVE_AT_FIXED_SEAM__COMPACT_DOUBLE_HAS_CRITICAL_POINT",
        "time_live_phi": "TIME_LIVE_COMPONENT_MAY_EVADE__MIRROR_LIFT_DEPENDENT",
        "projector_survival": "EVEN_STATIC_MIRROR_BRANCH_OBSTRUCTED__OTHER_LIFTS_CONDITIONAL",
        "hodge_exchange": "ANGULAR_AND_ORIENTATION_LIFT_DEPENDENT",
        "global_behavior": "ODD_PHI_CAN_BE_SMOOTH_ON_DOUBLE_BUT_NOT_DESCEND_AS_ORDINARY_QUOTIENT_SCALAR",
    },
    "FC09_NONORIENTABLE_GLUE": {
        "static_spatial_phi": "COMPACT_SUBCASES_FORCE_CRITICAL_POINT__BOUNDARY_SUBCASES_PROFILE_DEPENDENT",
        "time_live_phi": "POSSIBLE_IF_DPHI_DESCENDS_NONNULL__NOT_FORCED",
        "projector_survival": "REAL_3PLUS3_PROJECTORS_CAN_DESCEND_IF_DPHI_LINE_DESCENDS",
        "hodge_exchange": "ORDINARY_GLOBAL_HODGE_ENDOMORPHISM_FAILS__ORIENTATION_TWIST_REQUIRED",
        "global_behavior": "PROJECTOR_REDUCTION_AND_HODGE_RECIPROCITY_SEPARATE_GLOBALLY",
    },
    "FC10_STRATIFIED_PROJECTOR": {
        "static_spatial_phi": "REGISTERED_STRATIFICATION_DOES_NOT_FIX_DPHI_CAUSAL_STRATIFICATION",
        "time_live_phi": "REGISTERED_STRATIFICATION_DOES_NOT_FIX_DPHI_CAUSAL_STRATIFICATION",
        "projector_survival": "SURVIVES_OTHER_MOTIF_CHANGES_IFF_METRIC_REGULAR_AND_DPHI_NONNULL",
        "hodge_exchange": "CONDITIONAL_ON_ORIENTATION_METRIC_REGULARITY_AND_NONNULL_DPHI",
        "global_behavior": "OTHER_PROJECTOR_RANK_CHANGE_NEITHER_SELECTS_NOR_REFUTES_DPHI_SPLIT",
    },
    "FC11_NONINTEGRABLE_DISTRIBUTION": {
        "static_spatial_phi": "REGISTERED_ANHOLONOMIC_PLANE_IS_NOT_THE_EXACT_KERNEL_DPHI_DISTRIBUTION",
        "time_live_phi": "REGISTERED_ANHOLONOMIC_PLANE_IS_NOT_THE_EXACT_KERNEL_DPHI_DISTRIBUTION",
        "projector_survival": "CONDITIONAL_INDEPENDENT_OF_REGISTERED_NONINTEGRABLE_PLANE",
        "hodge_exchange": "CONDITIONAL_ON_ORIENTATION_AND_NONNULL_DPHI",
        "global_behavior": "NONINTEGRABILITY_OF_ANOTHER_DISTRIBUTION_IS_NOT_A_DPHI_OBSTRUCTION",
    },
    "FC12_RECIPROCAL_TORIC_DIAGONAL": {
        "static_spatial_phi": "OPEN_OR_BOUNDARY_DEPTH_PROFILE_CAN_SUPPORT_NONNULL_DPHI__CAP_EXTENSION_OPEN",
        "time_live_phi": "TIME_LIVE_PROFILE_NOT_SUPPLIED",
        "projector_survival": "EXACT_ON_OPEN_NONNULL_DPHI_PROFILE__GLOBAL_ENDPOINT_EXTENSION_OPEN",
        "hodge_exchange": "AVAILABLE_ON_ORIENTED_NONNULL_OPEN_CONTROL__GLOBAL_CAP_OR_GLUE_OPEN",
        "global_behavior": "CONDITIONAL_CONTROL_NOT_A_COMPLETE_SELECTED_FIELD_SOLUTION",
    },
}

GLOBAL_THEOREMS = [
    {
        "theorem_id": "G01_LOCAL_DOMAIN",
        "domain": "ANY_REGULAR_LORENTZIAN_POINT",
        "condition": "dphi_nonzero_and_g_inverse_dphi_dphi_nonzero",
        "ruling": "REAL_RANK3_PLUS_RANK3_PROJECTORS_EXIST",
        "scope_guard": "POINTWISE_NOT_GLOBAL_SELECTION",
    },
    {
        "theorem_id": "G02_CAUSAL_SIGN_CHANGE",
        "domain": "CONNECTED_CONTINUOUS_FIELD_PATH",
        "condition": "g_inverse_dphi_dphi_changes_sign",
        "ruling": "NULL_OR_ZERO_DEGENERATION_IS_CROSSED",
        "scope_guard": "NO_SEMISIMPLE_SPLIT_AT_CROSSING",
    },
    {
        "theorem_id": "G03_COMPACT_STATIC_REAL_SCALAR",
        "domain": "COMPACT_BOUNDARYLESS_SPATIAL_COMPLETION_WITH_STATIC_REAL_PHI",
        "condition": "phi_nonconstant_or_constant",
        "ruling": "DPHI_ZERO_AT_AN_EXTREMUM_OR_EVERYWHERE",
        "scope_guard": "DOES_NOT_APPLY_TO_UNCONSTRAINED_TIME_LIVE_PHI",
    },
    {
        "theorem_id": "G04_RETAINED_BOUNDARY",
        "domain": "FINITE_CELL_WITH_BOUNDARY",
        "condition": "global_real_phi_submersion_with_nonnull_gradient",
        "ruling": "GLOBAL_SPLIT_IS_MATHEMATICALLY_POSSIBLE",
        "scope_guard": "BOUNDARY_DOES_NOT_FORCE_OR_SELECT_PROFILE",
    },
    {
        "theorem_id": "G05_TIME_LIVE_ESCAPE",
        "domain": "R_TIME_CROSS_COMPACT_SPATIAL_COMPLETION",
        "condition": "time_live_phi_has_everywhere_nonnull_gradient",
        "ruling": "STATIC_EXTREME_VALUE_OBSTRUCTION_DOES_NOT_APPLY",
        "scope_guard": "NO_CURRENT_FIELD_EQUATION_FORCES_THIS_BRANCH",
    },
    {
        "theorem_id": "G06_COHOMOGENEITY_ONE_CAP",
        "domain": "SMOOTH_ROTATIONAL_CAP_WITH_PHI_ONLY_ORBIT_DEPTH",
        "condition": "ordinary_smooth_invariant_real_scalar",
        "ruling": "NORMAL_DPHI_VANISHES_AT_CAP",
        "scope_guard": "GENERAL_MULTI_COORDINATE_OR_TIME_LIVE_FIELD_REMAINS_OPEN",
    },
    {
        "theorem_id": "G07_EVEN_MIRROR",
        "domain": "SMOOTH_REFLECTION_FIXED_SEAM",
        "condition": "phi_is_mirror_invariant_ordinary_scalar",
        "ruling": "NORMAL_DPHI_VANISHES_AT_FIXED_SEAM",
        "scope_guard": "TANGENTIAL_OR_TIME_COMPONENT_COULD_REMAIN",
    },
    {
        "theorem_id": "G08_ODD_DOUBLE",
        "domain": "SMOOTH_DOUBLE_WITH_REFLECTION",
        "condition": "phi_is_odd_and_has_nonzero_normal_derivative",
        "ruling": "CAN_SURVIVE_ON_DOUBLE_BUT_NOT_DESCEND_AS_ORDINARY_QUOTIENT_SCALAR",
        "scope_guard": "SIGN_TWISTED_FIELD_WOULD_BE_AN_EXTRA_BUNDLE_PREMISE",
    },
    {
        "theorem_id": "G09_NONORIENTABLE",
        "domain": "NONORIENTABLE_REGULAR_COMPLETION",
        "condition": "dphi_line_descends_and_is_nonnull",
        "ruling": "REAL_PROJECTORS_MAY_DESCEND_BUT_ORDINARY_GLOBAL_HODGE_EXCHANGE_DOES_NOT",
        "scope_guard": "ORIENTATION_TWISTED_HODGE_MUST_BE_DISTINGUISHED",
    },
    {
        "theorem_id": "G10_SINGULAR_STRATUM",
        "domain": "TRUE_METRIC_OR_MANIFOLD_SINGULARITY",
        "condition": "inverse_metric_or_smooth_bundle_undefined",
        "ruling": "RECIPROCAL_PROJECTOR_CONSTRUCTION_UNDEFINED_AT_STRATUM",
        "scope_guard": "REGULAR_COMPLEMENT_CAN_STILL_BE_CLASSIFIED",
    },
    {
        "theorem_id": "G11_SEAL_VALUE",
        "domain": "PHI_EQUALS_ZERO_SEAL",
        "condition": "phi_zero_only",
        "ruling": "RECIPROCAL_WEIGHTS_COINCIDE_BUT_DPHI_DOMAIN_IS_UNDECIDED",
        "scope_guard": "PHI_ZERO_DOES_NOT_IMPLY_DPHI_ZERO",
    },
    {
        "theorem_id": "G12_OTHER_DISTRIBUTIONS",
        "domain": "REGISTERED_MOTIF_OR_ANHOLONOMIC_DISTRIBUTION_TRANSITION",
        "condition": "transition_not_proven_to_be_dphi_projector_transition",
        "ruling": "NEITHER_SELECTS_NOR_OBSTRUCTS_NONNULL_DPHI_SPLIT",
        "scope_guard": "DISTRIBUTIONS_MUST_NOT_BE_CONFLATED",
    },
]


def branch_atlas(completions: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in completions:
        completion_id = source["completion_id"]
        ruling = BRANCH_RULINGS[completion_id]
        data_level = (
            "CONDITIONAL_CONTROL_NO_COMPLETE_PROFILE_OR_ENDPOINT_SOLUTION"
            if completion_id == "FC12_RECIPROCAL_TORIC_DIAGONAL"
            else "PARAMETRIC_COMPLETION_TYPE_NO_COMPLETE_G_PHI_FIELD_WITNESS"
        )
        rows.append(
            {
                "completion_id": completion_id,
                "base_completion": source["base_completion"],
                "topology_family": source["topology_family"],
                "source_selection_status": source["selection_status"],
                "global_data_level": data_level,
                **ruling,
                "density_response": "UNDEFINED_NO_NATIVE_DENSITY_TO_BRANCH_INTERFACE",
                "selection_ruling": "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_THIS_AUDIT",
            }
        )
    return rows


def density_gate(density_rows: list[dict[str, str]]) -> tuple[dict[str, object], list[dict[str, str]]]:
    route_status = {row["route_id"]: row for row in density_rows}
    required = {
        "D01_OBSERVED_DENSITY_INPUT",
        "D02_CONDITIONAL_CARRIER_READOUT",
        "D03_NATIVE_SIMULTANEOUS_FIXED_POINT",
        "D04_DIMENSIONLESS_COMPACTNESS_LOOP",
        "D05_ASSEMBLY_ATLAS_CONTRIBUTION",
    }
    if set(route_status) != required:
        raise AssertionError("density route source changed")
    native = route_status["D03_NATIVE_SIMULTANEOUS_FIXED_POINT"]
    gate_pass = (
        native["mass_status"] == "NATIVE_OBJECT_AVAILABLE"
        and native["selection_authority"] == "ACTIVE_NATIVE_BRANCH_SELECTOR"
        and native["missing_object"] in {"", "-"}
    )
    bracket = [
        {
            "rho_tot_domain": "0",
            "interface_status": "NOT_AN_ARGUMENT_OF_CURRENT_GEOMETRY_BRANCH_SYSTEM",
            "branch_response": "IDENTICAL_UNCOUPLED_GEOMETRY_CLASSIFICATION",
            "interpretation": "FORMAL_ENDPOINT_NOT_A_VACUUM_FIELD_EQUATION_CLAIM",
        },
        {
            "rho_tot_domain": "ANY_FINITE_POSITIVE_VALUE",
            "interface_status": "NOT_AN_ARGUMENT_OF_CURRENT_GEOMETRY_BRANCH_SYSTEM",
            "branch_response": "IDENTICAL_UNCOUPLED_GEOMETRY_CLASSIFICATION",
            "interpretation": "NO_NORMALIZATION_OR_DENSITY_CENTER_INSERTED",
        },
        {
            "rho_tot_domain": "ARBITRARILY_LARGE_FINITE_VALUE",
            "interface_status": "NOT_AN_ARGUMENT_OF_CURRENT_GEOMETRY_BRANCH_SYSTEM",
            "branch_response": "IDENTICAL_UNCOUPLED_GEOMETRY_CLASSIFICATION",
            "interpretation": "NOT_A_CONTROLLED_INFINITE_DENSITY_PHYSICAL_LIMIT",
        },
        {
            "rho_tot_domain": "FORMAL_POSITIVE_EXTENDED_DOMAIN_[0,INFINITY)",
            "interface_status": "GATE_FAILED__NO_NUMERICAL_SWEEP_AUTHORIZED",
            "branch_response": "NO_APPEAR_DISAPPEAR_MERGE_OR_SINGULAR_EVENT_DEFINED_AS_RHO_RESPONSE",
            "interpretation": "MISSING_INTERFACE_NOT_EVIDENCE_OF_PHYSICAL_DENSITY_INDEPENDENCE",
        },
    ]
    gate = {
        "gate_pass": gate_pass,
        "source_route_count": len(density_rows),
        "native_route_status": native["mass_status"],
        "native_route_missing_object": native["missing_object"],
        "numeric_density_sweep_run": False,
        "formal_bracket": "rho_tot in [0,infinity)",
        "branch_map_dependence": "CONSTANT_ONLY_BECAUSE_RHO_TOT_IS_ABSENT_FROM_CURRENT_BRANCH_SYSTEM",
        "maximum_conclusion": "NO_DENSITY_DRIVEN_BRANCH_CHANGE_IS_DEFINED_IN_CURRENT_GEOMETRY_ONLY_SYSTEM",
    }
    if gate_pass:
        raise AssertionError("unexpected density gate activation requires a new preregistered schedule")
    return gate, bracket


def main() -> None:
    completions = read_tsv(COMPLETION_SOURCE)
    if len(completions) != 12:
        raise AssertionError(f"expected 12 completion rows, got {len(completions)}")
    if set(BRANCH_RULINGS) != {row["completion_id"] for row in completions}:
        raise AssertionError("completion ruling coverage mismatch")

    intrinsic = json.loads(
        (
            ROOT
            / "udt_complete_metric_intrinsic_object_audit_2026-07-23"
            / "RESULT.json"
        ).read_text(encoding="utf-8")
    )
    if not intrinsic["exact_checks"][
        "nonnull_gradient_induces_real_rank3_plus_rank3_two_form_split"
    ]:
        raise AssertionError("prior load-bearing reciprocal reduction did not replay")

    exact = local_exact_controls()
    branches = branch_atlas(completions)
    density_rows = read_tsv(DENSITY_SOURCE)
    density, bracket = density_gate(density_rows)

    source_rows = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise AssertionError(f"missing source {relative}")
        source_rows.append(
            {"path": relative, "sha256": sha256(path), "size": path.stat().st_size}
        )

    result = {
        "schema": "udt-finite-cell-reciprocal-survival-density-1.0",
        "sympy_version": sp.__version__,
        "base_commit": "67553529e79514aa79607dee859ae7d084ea37d6",
        "exact_controls": exact,
        "counts": {
            "registered_completion_families": len(branches),
            "complete_g_phi_field_witnesses": sum(
                row["global_data_level"] == "COMPLETE_G_PHI_FIELD_WITNESS"
                for row in branches
            ),
            "parametric_type_only": sum(
                row["global_data_level"]
                == "PARAMETRIC_COMPLETION_TYPE_NO_COMPLETE_G_PHI_FIELD_WITNESS"
                for row in branches
            ),
            "conditional_controls": sum(
                row["global_data_level"]
                == "CONDITIONAL_CONTROL_NO_COMPLETE_PROFILE_OR_ENDPOINT_SOLUTION"
                for row in branches
            ),
            "static_compact_completion_rows_obstructed": sum(
                "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT"
                in row["static_spatial_phi"]
                for row in branches
            ),
            "mirror_fixed_seam_rows_with_static_normal_obstruction": sum(
                "MIRROR_INVARIANT_SMOOTH_PHI_HAS_ZERO_NORMAL_DERIVATIVE"
                in row["static_spatial_phi"]
                for row in branches
            ),
            "global_theorems": len(GLOBAL_THEOREMS),
            "density_source_routes": len(density_rows),
            "density_numeric_runs": 0,
        },
        "geometry_stopping_gate": {
            "status": "REACHED",
            "reason": "REGISTERED_GLOBAL_ROWS_SUPPLY_COMPLETION_TYPES_BUT_NO_COMPLETE_G_PHI_FIELD_WITNESSES_OR_FIELD_EQUATIONS",
            "remaining_free_data": "GLOBAL_G_PHI_PROFILE__BOUNDARY_CAP_GLUE__STATIC_OR_TIME_LIVE_BRANCH__ACTION_AND_SOURCE",
        },
        "density_interface_gate": density,
        "maximum_conclusion": "FINITE_CELL_SURVIVAL_CRITERION_DERIVED_AND_COMPLETION_TYPES_CLASSIFIED__GEOMETRY_STOPS_AT_UNSUPPLIED_GLOBAL_FIELD_PROFILES__DENSITY_RESPONSE_UNDEFINED_WITHOUT_NATIVE_INTERFACE",
    }

    (OUT / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_tsv(
        OUT / "FINITE_CELL_BRANCH_ATLAS.tsv",
        [
            "completion_id",
            "base_completion",
            "topology_family",
            "source_selection_status",
            "global_data_level",
            "static_spatial_phi",
            "time_live_phi",
            "projector_survival",
            "hodge_exchange",
            "global_behavior",
            "density_response",
            "selection_ruling",
        ],
        branches,
    )
    write_tsv(
        OUT / "DENSITY_BRACKET.tsv",
        [
            "rho_tot_domain",
            "interface_status",
            "branch_response",
            "interpretation",
        ],
        bracket,
    )
    write_tsv(
        OUT / "GLOBAL_SURVIVAL_THEOREMS.tsv",
        ["theorem_id", "domain", "condition", "ruling", "scope_guard"],
        GLOBAL_THEOREMS,
    )
    write_tsv(
        OUT / "SOURCE_LINEAGE.tsv", ["path", "sha256", "size"], source_rows
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
