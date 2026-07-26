#!/usr/bin/env python3
"""Build the preregistered UDT functional-DOF and constraint-rank ledgers."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def exact_dimensions() -> dict[str, int]:
    n = 4
    k = 2
    dims = {
        "spacetime_dimension": n,
        "symmetric_metric_components": n * (n + 1) // 2,
        "coframe_components": n * n,
        "local_lorentz_generators": n * (n - 1) // 2,
        "coordinate_presentation_functions": n,
        "metric_configuration_quotient": n * (n + 1) // 2 - n,
        "coframe_configuration_quotient": n * n - n * (n - 1) // 2 - n,
        "independent_scalar_components": 1,
        "symmetric_base_block": k * (k + 1) // 2,
        "symmetric_screen_block": k * (k + 1) // 2,
        "shift_block": k * (n - k),
        "rank_two_plane_components": k * (n - k),
        "conditional_local_conformal_generator": 1,
    }
    assert dims["symmetric_metric_components"] == 10
    assert dims["coframe_components"] == 16
    assert dims["local_lorentz_generators"] == 6
    assert dims["metric_configuration_quotient"] == 6
    assert dims["coframe_configuration_quotient"] == 6
    assert (
        dims["symmetric_base_block"]
        + dims["symmetric_screen_block"]
        + dims["shift_block"]
        == 10
    )
    assert dims["rank_two_plane_components"] == 4
    return dims


def verify_frozen_sources() -> None:
    for manifest in ("SOURCE_MANIFEST.tsv", "SOURCE_MANIFEST_CORRECTION.tsv"):
        for row in read_tsv(HERE / manifest):
            path = ROOT / row["path"]
            if not path.is_file() or str(path.stat().st_size) != row["bytes"] or sha256(path) != row["sha256"]:
                raise SystemExit(f"source manifest mismatch: {row['path']}")


def main() -> None:
    verify_frozen_sources()
    d = exact_dimensions()

    source_branches = read_tsv(
        ROOT / "udt_complete_metric_solution_space_map_2026-07-21/OFFSHELL_CONFIGURATION_BRANCHES.tsv"
    )
    branch_ids = [row["branch_id"] for row in source_branches]
    if branch_ids != [f"C0{i}" for i in range(1, 8)]:
        raise SystemExit(f"unexpected branch universe: {branch_ids}")

    completions = read_tsv(HERE / "COMPLETION_UNIVERSE.tsv")
    if len(completions) != 12 or len({row["completion_id"] for row in completions}) != 12:
        raise SystemExit("completion universe must contain twelve unique rows")

    presentation_rows = [
        {
            "id": "P01",
            "presentation": "symmetric_metric",
            "raw_signature": "F4[10]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM_PRESENTATION",
            "quotient_signature": "F4[6]",
            "status": "EXACT_LOCAL_CONFIGURATION_COUNT",
            "scope": "generic regular 4D Lorentz metric; not propagating modes",
        },
        {
            "id": "P02",
            "presentation": "coframe",
            "raw_signature": "F4[16]",
            "gauge_signature": "G4[6]_LOCAL_LORENTZ+G4[4]_DIFFEOMORPHISM",
            "quotient_signature": "F4[6]",
            "status": "EXACT_CROSSCHECK",
            "scope": "invertible coframe; metric and coframe are not additive inventories",
        },
        {
            "id": "P03",
            "presentation": "supplied_2plus2_base_screen_shift",
            "raw_signature": "F4[3]+F4[3]+F4[4]=F4[10]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM_PRESENTATION",
            "quotient_signature": "F4[6]",
            "status": "EXACT_WITH_SUPPLIED_SPLIT",
            "scope": "complete regular chart; split is not intrinsically selected",
        },
        {
            "id": "P04",
            "presentation": "generic_metric_plus_chosen_independent_scalar_control",
            "raw_signature": "F4[11]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM_PRESENTATION",
            "quotient_signature": "F4[7]",
            "status": "CHOSE_COMPARISON_CONFIGURATION",
            "scope": "exact enlarged-atlas count only; not native UDT field ownership",
        },
        {
            "id": "P05",
            "presentation": "generic_metric_arena_with_founded_reciprocal_phi_subgroup",
            "raw_signature": "F4[10]+F4[0]_FOUNDED_PHI",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM_PRESENTATION",
            "quotient_signature": "F4[6]_GENERIC_ARENA__UDT_REDUCED_RANK_OPEN",
            "status": "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN",
            "scope": "phi identity and pair action are derived; unique 4D extension and native reduced field rank remain open",
        },
        {
            "id": "P06",
            "presentation": "counterfactual_local_conformal_metric_class",
            "raw_signature": "F4[10]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM+G4[1]_LOCAL_CSN",
            "quotient_signature": "F4[5]",
            "status": "INACTIVE_COUNTERFACTUAL_REQUIRES_EXPLICIT_REAUTHORIZATION",
            "scope": "strong local CSN is CHALLENGED_OWNER_POSTULATE_NOT_DERIVED and cannot enter an active count",
        },
        {
            "id": "P07",
            "presentation": "counterfactual_conformal_metric_plus_chosen_scalar_control",
            "raw_signature": "F4[11]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM+G4[1]_LOCAL_CSN",
            "quotient_signature": "F4[6]",
            "status": "INACTIVE_COUNTERFACTUAL_PLUS_CHOSEN_COMPARISON",
            "scope": "neither strong local CSN nor independent native phi is current authority",
        },
        {
            "id": "P08",
            "presentation": "metric_plus_supplied_nondegenerate_rank2_projector",
            "raw_signature": "F4[10]+F4[4]",
            "gauge_signature": "G4[4]_DIFFEOMORPHISM_PRESENTATION",
            "quotient_signature": "F4[10]",
            "status": "EXACT_ON_C04_SUPPLIED_PROJECTOR_BRANCH",
            "scope": "four plane functions are extra only when the projector is supplied independently",
        },
        {
            "id": "P09",
            "presentation": "FC12_reciprocal_toric_diagonal_control",
            "raw_signature": "F1[2]_A_AND_OMEGA+Z[ENDPOINT_CLASS]+U[ENDPOINT_JETS]",
            "gauge_signature": "NONE_SUBTRACTED_FROM_PHYSICAL_PHI_PROFILE",
            "quotient_signature": "F1[2]+Z[ENDPOINT_CLASS]+U[ENDPOINT_JETS]",
            "status": "EXACT_INSIDE_SUPPLIED_ANSATZ_ONLY",
            "scope": "not the generic metric family and not a selected completion",
        },
    ]
    if d["metric_configuration_quotient"] != d["coframe_configuration_quotient"]:
        raise SystemExit("metric/coframe quotient cross-check failed")
    write_tsv(
        "LOCAL_PRESENTATION_RANK.tsv",
        ["id", "presentation", "raw_signature", "gauge_signature", "quotient_signature", "status", "scope"],
        presentation_rows,
    )

    branch_templates = {
        "C01": (
            "GENERIC_ARENA_F4[6]__NATIVE_RANK_OPEN",
            "INACTIVE_COUNTERFACTUAL_F4[5]",
            "founded_phi_adds_F4[0]__conformal_class_only_is_not_currently_selected",
            "complete founded extension; physical representative; variation domain; global smoothness",
        ),
        "C02": (
            "CHOSE_COMPARISON_F4[7]",
            "INACTIVE_COUNTERFACTUAL_COMPARISON_F4[6]",
            "chosen_independent_scalar_adds_F4[1]_only_in_enlarged_atlas",
            "not a candidate native ownership branch; retain only as comparison control",
        ),
        "C03": (
            "GENERIC_ARENA_F4[6]+U[FOUNDED_COMPLETE_EXTENSION]",
            "INACTIVE_COUNTERFACTUAL",
            "founded_pair_generator_fixed__triangular_extension_has_7_then_6_parameters_under_det1",
            "angular generator; mixing; Lorentz-independent descent; physical assignment; global lift",
        ),
        "C04": (
            "GENERIC_ARENA_F4[10]+U[FOUNDED_EXTENSION_THROUGH_SUPPLIED_PLANE]",
            "INACTIVE_COUNTERFACTUAL_F4[9]+U[FOUNDED_EXTENSION_THROUGH_SUPPLIED_PLANE]",
            "supplied_nondegenerate_rank2_plane_adds_F4[4]; founded_phi_adds_F4[0]",
            "projector selection; founded extension through plane; integrability; type change; transport authority",
        ),
        "C05": (
            "F4[6]+U[MULTIPLIERS_AND_CONSTRAINT_RANK]",
            "INACTIVE_COUNTERFACTUAL_F4[5]+U[MULTIPLIERS_AND_CONSTRAINT_RANK]",
            "field_and_constraint_count_not_supplied",
            "multiplier census; independent constraint rank; unrestricted variation; boundary terms",
        ),
        "C06": (
            "F4[6]+U[TWO_STAGE_MAP]",
            "INACTIVE_COUNTERFACTUAL_F4[5]+U[REPRESENTATIVE_SECTION_AND_BRIDGE]",
            "pre_scale_and_post_scale_counts_cannot_be_collapsed",
            "native representative map; scale origin; bridge; boundary variation",
        ),
        "C07": (
            "F4[6]+U[CONNECTION_OR_TORSION_BUNDLE]",
            "INACTIVE_COUNTERFACTUAL_F4[5]+U[CONNECTION_OR_TORSION_BUNDLE]",
            "connection_type_and_relation_to_metric_not_supplied",
            "field census; transition law; metric compatibility; torsion; response; boundary data",
        ),
    }
    branch_rows = []
    branch_roles = {
        "C01": "HISTORICAL_CONFIGURATION_CONTROL__CONFORMAL_CLASS_NOT_SELECTED",
        "C02": "CHOSE_COMPARISON_CONFIGURATION__NOT_NATIVE_OWNERSHIP",
        "C03": "CURRENT_FOUNDED_EXTENSION_CLASS__SELECTION_OPEN",
        "C04": "CONDITIONAL_DIAGNOSTIC_SUPPLIED_PROJECTOR",
        "C05": "OPEN_PROPOSED_MULTIPLIER_IMPLEMENTATION",
        "C06": "OPEN_PROPOSED_TWO_STAGE_IMPLEMENTATION",
        "C07": "OPEN_PROPOSED_CONNECTION_IMPLEMENTATION",
    }
    for source in source_branches:
        primary, conditional, addition, missing = branch_templates[source["branch_id"]]
        branch_rows.append(
            {
                "branch_id": source["branch_id"],
                "primary_variables": source["primary_variables"],
                "anchored_primary_signature": primary,
                "conditional_strong_local_CSN_signature": conditional,
                "branch_specific_addition": addition,
                "exact_status": branch_roles[source["branch_id"]],
                "missing_for_complete_rank": missing,
                "selected": "NO",
            }
        )
    write_tsv(
        "REALIZATION_BRANCH_RANK.tsv",
        [
            "branch_id",
            "primary_variables",
            "anchored_primary_signature",
            "conditional_strong_local_CSN_signature",
            "branch_specific_addition",
            "exact_status",
            "missing_for_complete_rank",
            "selected",
        ],
        branch_rows,
    )

    constraint_effects = {
        "K01": ("G4[4]", "PRESENTATION_GAUGE_EXACT", "removes coordinate descriptions not geometry"),
        "K02": ("G4[6]", "PRESENTATION_GAUGE_EXACT", "removes coframe Lorentz presentations only"),
        "K03": ("ZERO", "OPEN_CONDITION", "signature/positivity selects an open stratum"),
        "K04": ("ONE_INTERNAL_CHANNEL_RELATION__ZERO_EXTRA_PHI_FIELD", "DERIVED_FOUNDED_PAIR", "reciprocal pair has one additive logarithmic depth"),
        "K05": ("ZERO_ADDITIONAL_FIELD", "DERIVED_FOUNDED_ACTION", "phi acts as diag(exp(-phi),exp(phi)) on the founding pair"),
        "K06": ("U[PHYSICAL_PAIR_ASSIGNMENT_AND_COMPLETE_EXTENSION]", "OPEN_DOWNSTREAM_JOIN", "frame equivalence leaves physical observer/path assignment and 4D extension open without reopening phi identity"),
        "K07": ("INACTIVE_NO_RANK_SUBTRACTION", "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "counterfactual use requires explicit owner reauthorization"),
        "K08": ("AT_MOST_C[1]", "GLOBAL_ONLY", "constant rescaling is not a local gauge function"),
        "K09": ("ZERO_LOCAL+U[GLOBAL_DOMAIN]", "ONTOLOGY_NOT_EQUATION", "finite domain supplies no point-local field relation"),
        "K10": ("F3[1]_TRACE", "STATIC_BOUNDARY_ONLY", "does not remove bulk phi"),
        "K11": ("F3[1]_TANGENT_TRACE", "STATIC_VARIATION_DOMAIN_ONLY", "normal derivative and other variations remain"),
        "K12": ("U[COMPLETION_DEPENDENT]", "GLOBAL_OPEN", "no universal boundary/gluing rank"),
        "K13": ("ZERO_LOCAL_FUNCTIONAL_RANK", "OBSERVED_CALIBRATION", "c calibrates clock-distance scale"),
        "K14": ("ZERO_LOCAL_FUNCTIONAL_RANK", "OBSERVED_CALIBRATION", "G calibrates mass-length conversion"),
        "K15": ("ZERO_PRESENT_LOCAL_RANK", "ON_SHELL_WORKING_ONLY", "complete mass-volume-stability response absent"),
        "K16": ("ZERO_ADDITIONAL_FIELD", "DERIVED_DEFINITION", "F is not independent when F=dS"),
        "K17": ("ZERO_DYNAMICAL_RANK", "DERIVED_IDENTITY", "d squared equals zero and is not a sourced Maxwell equation"),
        "K18": ("ZERO_ADDITIONAL_FIELD", "DERIVED_EVALUATOR", "Levi-Civita connection is metric-derived"),
        "K19": ("ZERO_IF_DERIVED__F4[4]_IF_SUPPLIED", "BRANCH_DEPENDENT", "spectral and supplied projectors must be separated"),
        "K20": ("NO_CURRENT_RANK", "OPEN_ABSENT", "complete native response/EOM is the missing interface"),
    }
    constraint_rows = []
    for row in read_tsv(HERE / "CONSTRAINT_UNIVERSE.tsv"):
        effect, status, conclusion = constraint_effects[row["id"]]
        constraint_rows.append(
            {
                "id": row["id"],
                "constraint_or_equivalence": row["constraint_or_equivalence"],
                "domain": row["domain"],
                "registered_status": row["status"],
                "audited_rank_effect": effect,
                "rank_status": status,
                "conclusion": conclusion,
            }
        )
    write_tsv(
        "CONSTRAINT_RANK_LEDGER.tsv",
        [
            "id",
            "constraint_or_equivalence",
            "domain",
            "registered_status",
            "audited_rank_effect",
            "rank_status",
            "conclusion",
        ],
        constraint_rows,
    )

    completion_global = {
        "FC01_BOUNDARY_BOUNDARY": "U[TWO_BOUNDARY_EMBEDDINGS_POLARIZATIONS_JETS_CORNERS]",
        "FC02_ONE_CAP_BOUNDARY": "Z[PRIMITIVE_CAP]+U[CAP_JETS+BOUNDARY_DATA]",
        "FC03_TWO_CAP_P0": "Z[DEPENDENT_PRIMITIVE_PAIR]+U[TWO_CAP_PROFILE_JETS]",
        "FC04_TWO_CAP_P1": "Z[UNIMODULAR_PRIMITIVE_PAIR+ORIENTATION]+U[TWO_CAP_PROFILE_JETS]",
        "FC05_TWO_CAP_P_GT1": "Z[LENS_P_Q_AND_PRIMITIVE_PAIR]+U[TWO_CAP_PROFILE_JETS]",
        "FC06_NONPRIMITIVE_CAP": "Z[NONPRIMITIVE_VECTORS]+U[SINGULAR_STRATA_AND_JETS]",
        "FC07_PERIODIC_TORUS_BUNDLE": "Z[GL2Z_MONODROMY]+C[PERIOD_AND_HOLONOMY_MODULI]+U[PERIODIC_PROFILES]",
        "FC08_MIRROR_DOUBLE": "Z[INVOLUTION_LIFT]+U[FIXED_SET_EMBEDDING_PARITY_JETS]",
        "FC09_NONORIENTABLE_GLUE": "Z[DET_MINUS_ONE_MONODROMY+SIGN_HOLONOMY]+U[GLUE_PROFILES]",
        "FC10_STRATIFIED_PROJECTOR": "Z[STRATIFICATION]+U[TRANSITION_LOCI_COARSENING_INTERFACE]",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "U[DISTRIBUTION_CONNECTION_TORSION_HOLONOMY]",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "Z[ENDPOINT_CAP_GLUE_CLASS]+U[ENDPOINT_JETS]",
    }
    completion_rows = []
    for row in completions:
        fc12 = row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
        completion_rows.append(
            {
                "completion_id": row["completion_id"],
                "bulk_signature": "F1[2]_INSIDE_SUPPLIED_ANSATZ" if fc12 else "GENERIC_ARENA_F4[6]__FOUNDED_EXTENSION_NATIVE_RANK_OPEN",
                "global_freedom_signature": completion_global[row["completion_id"]],
                "local_rank_reduction_from_completion_alone": "NOT_APPLICABLE__SEPARATELY_SUPPLIED_ANSATZ" if fc12 else "ZERO",
                "selected": "NO",
                "closure_status": "CONDITIONAL_CONTROL_NOT_GENERIC" if fc12 else "GLOBAL_FUNCTIONAL_DATA_UNCOUNTED",
            }
        )
    write_tsv(
        "COMPLETION_DOF_ATLAS.tsv",
        [
            "completion_id",
            "bulk_signature",
            "global_freedom_signature",
            "local_rank_reduction_from_completion_alone",
            "selected",
            "closure_status",
        ],
        completion_rows,
    )

    derived_rows = [
        ("D01", "base_screen_shift_h_q_A", "metric_reparameterization", "F4[0]", "ten chart functions already equal the metric inventory"),
        ("D02", "Levi_Civita_connection", "metric_first_derivative", "F4[0]", "derived evaluator on regular metric branch"),
        ("D03", "Riemann_Ricci_Weyl_Cartan_curvature", "metric_two_jet", "F4[0]", "curvature is a readout not an extra field"),
        ("D04", "spectral_projectors_and_motifs", "metric_or_curvature_readout", "F4[0]", "adds F4[4] only on separately supplied C04 plane branch"),
        ("D05", "Kato_projector_transport", "metric_plus_projector_path_readout", "F4[0]", "transport law does not select projector or metric"),
        ("D06", "normalized_angular_metric_H", "angular_metric_block_readout", "F4[0]", "common normalization does not select physical scale"),
        ("D07", "torus_shift_connection_S", "metric_block_plus_supplied_torus_split", "F4[0]", "conditional connection schema not new matter field"),
        ("D08", "torus_curvature_F_equals_dS", "derived_from_S", "F4[0]", "F is not independent"),
        ("D09", "homogeneous_identity_dF_equals_zero", "exterior_calculus_identity", "F4[0]", "not the inhomogeneous Maxwell equation"),
        ("D10", "selected_circle_A_equals_wT_S", "S_plus_supplied_integral_character", "F4[0]+Z[w]", "U1 character selection remains conditional"),
        ("D11", "Maxwell_action_current_charge", "not_derived", "O[OPEN]", "historical/imported equations have zero native authority here"),
        ("D12", "Levi_Civita_Kato_torus_holonomies", "nonlocal_readouts", "F4[0]", "distinct readouts; none is independent field data"),
        ("D13", "Hopf_or_Chern_class", "conditional_global_invariant", "Z[class]_DERIVED_AFTER_GLOBAL_INPUTS", "not a carrier section action or source"),
        ("D14", "observer_pair_clock_cocycle", "founded_pair_plus_typed_path_readout", "F4[0]", "founded depth is derived; physical observer/path assignment and complete extension remain open"),
    ]
    write_tsv(
        "DERIVED_OBJECT_NO_DOUBLE_COUNT.tsv",
        ["id", "object", "parent", "additional_continuous_field_signature", "scope"],
        [dict(zip(["id", "object", "parent", "additional_continuous_field_signature", "scope"], row)) for row in derived_rows],
    )

    response_rows = [
        ("R01", "complete_founded_coframe_extension_and_variation_domain", "U[ANGULAR_GENERATOR+MIXING+DESCENT]", "OPEN_NOT_SELECTED", "select the full 4D realization of the derived founded pair before assigning native response rank"),
        ("R02", "generic_metric_comparison_variations", "F4[10]_RAW__F4[6]_MOD_COORDINATES", "ARENA_DEFINED__NATIVE_RESPONSE_ABSENT", "generic symmetric variations are a comparison arena, not yet the selected UDT variation domain"),
        ("R03", "chosen_independent_scalar_control_variations", "F4[1]", "COMPARISON_ONLY", "may test the enlarged atlas but cannot establish native scalar ownership"),
        ("R04", "supplied_projector_variations_C04", "F4[4]", "ABSENT", "conditional diagnostic branch cannot select its own projector"),
        ("R05", "multiplier_and_constraint_variations_C05", "U[MULTIPLIERS]", "FIELD_CENSUS_UNSPECIFIED", "constraint number and independence remain open"),
        ("R06", "representative_and_bridge_variations_C06", "U[SECTION_AND_MAP]", "ABSENT", "pre/post-scale bridge needs its own response"),
        ("R07", "independent_connection_variations_C07", "U[CONNECTION_BUNDLE]", "FIELD_CENSUS_UNSPECIFIED", "connection type metric relation and boundary response absent"),
        ("R08", "finite_cell_boundary_and_corner_variations", "U[BOUNDARY_COVECTORS]", "ABSENT", "static phi trace is not complete boundary polarization"),
        ("R09", "global_moduli_topology_and_period_variations", "Z+U[GLOBAL_MODULI]", "ABSENT_OR_DISCRETE", "global exactness and periods remain uncontrolled"),
        ("R10", "same_solution_mass_volume_density_feedback", "O[NOT_EVALUABLE]", "ABSENT", "native source and complete solution are prerequisites"),
    ]
    write_tsv(
        "RESPONSE_COVERAGE_TARGET.tsv",
        ["id", "variation_sector", "variation_signature", "current_response_status", "coverage_requirement"],
        [dict(zip(["id", "variation_sector", "variation_signature", "current_response_status", "coverage_requirement"], row)) for row in response_rows],
    )

    status_rows = [
        ("S01", "generic_metric_local_configuration_quotient", "DERIVED_F4_6", "four-dimensional regular metric modulo coordinate presentation; not dynamics"),
        ("S02", "coframe_metric_rank_agreement", "DERIVED_EXACT", "16 minus 6 local Lorentz minus 4 coordinate functions equals 10 minus 4 equals 6"),
        ("S03", "chosen_independent_scalar_control", "CHOSE_COMPARISON_F4_7_TOTAL", "exact enlarged-atlas count; not native UDT field ownership"),
        ("S04", "founded_phi_native_status", "DERIVED_FOUNDED_PHI_ADDS_ZERO__COMPLETE_EXTENSION_OPEN", "identity and pair action are derived; physical assignment and unique 4D extension remain open"),
        ("S05", "strong_local_CSN_counterfactual", "INACTIVE_CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "F4[5] is arithmetic for a separately reauthorized counterfactual, not a current UDT count"),
        ("S06", "metric_native_instrument_count", "MOSTLY_DERIVED_NOT_ADDITIVE", "curvature projectors connections holonomies clock and toric readouts do not enlarge field inventory"),
        ("S07", "supplied_rank2_projector_branch", "CONDITIONAL_ADDS_F4_4__FOUNDED_PHI_ADDS_ZERO", "nondegenerate two-plane Grassmannian dimension four; its relation to the founded complete extension remains open"),
        ("S08", "C05_C06_C07_extra_fields", "UNCOUNTED_OPEN", "multiplier bridge and independent-connection field censuses are not specified"),
        ("S09", "founded_bulk_constraint_rank", "ZERO_COMPLETE_NATIVE_COFRAME_RESPONSE_RANK", "founded phi kinematics do not by themselves select the complete extension variation domain or response"),
        ("S10", "static_seal_rank", "BOUNDARY_F3_1_ONLY", "phi trace and allowed variation fixed; normal jet and bulk scalar remain free"),
        ("S11", "completion_freedom", "TWELVE_CLASSES_ALL_GLOBAL_DATA_OPEN", "FC01-FC11 retain generic bulk freedom; FC12 is a separate two-profile control"),
        ("S12", "metric_native_Maxwell_content", "F_EQUALS_dS_AND_dF_EQUALS_ZERO_ONLY_CONDITIONAL_TORIC", "U1 selection action current charge and inhomogeneous equation remain open"),
        ("S13", "smallest_missing_closure_type", "FOUNDED_COMPLETE_EXTENSION_AND_VARIATION_DOMAIN_THEN_RESPONSE_AND_GLOBAL_BOUNDARY", "the response question is downstream of the still-unselected complete 4D realization"),
        ("S14", "propagating_physical_modes", "NOT_EVALUABLE", "requires selected response action constraints gauge evolution and initial-value problem"),
        ("S15", "overall", "CORRECTED_GENERIC_ARENA_RANK_CHARACTERIZED__NATIVE_FOUNDED_EXTENSION_RANK_OPEN", "generic algebra survives; native UDT field rank is neither six nor seven from this audit"),
    ]
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["id", "object", "status", "scope_or_limit"],
        [dict(zip(["id", "object", "status", "scope_or_limit"], row)) for row in status_rows],
    )

    result = {
        "status": "CORRECTED_GENERIC_ARENA_RANK_CHARACTERIZED__NATIVE_FOUNDED_EXTENSION_RANK_OPEN",
        "dimensions": d,
        "presentation_rows": len(presentation_rows),
        "realization_branches": len(branch_rows),
        "constraint_rows": len(constraint_rows),
        "completion_rows": len(completion_rows),
        "derived_no_double_count_rows": len(derived_rows),
        "response_sectors": len(response_rows),
        "generic_metric_quotient": "F4[6]",
        "chosen_comparison_metric_plus_independent_scalar": "F4[7]_NOT_NATIVE_OWNERSHIP",
        "founded_phi_additional_native_field_count": 0,
        "native_founded_complete_extension_rank": "OPEN",
        "counterfactual_strong_local_CSN_metric": "F4[5]_INACTIVE_WITHOUT_EXPLICIT_REAUTHORIZATION",
        "complete_native_bulk_response": "ABSENT",
        "smallest_missing_closure_type": "FOUNDED_COMPLETE_EXTENSION_AND_VARIATION_DOMAIN_THEN_RESPONSE_AND_GLOBAL_BOUNDARY",
        "propagating_modes": "NOT_EVALUABLE",
        "selected_completion": None,
    }
    (HERE / "AUDIT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
