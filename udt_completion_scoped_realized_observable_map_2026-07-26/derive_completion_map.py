#!/usr/bin/env python3
"""Deterministic completion-by-readout atlas and exact discrete controls."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c1036fb498c8ed009733c82ee86cf96152a5ed6e"
PREREG = "c457bc4"
AMENDMENT = "b3325dd"
CORRECTION = "4a95a7b6f7231879ed1662d956603b1acb6326b8"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def keyed(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    result = {row[key]: row for row in rows}
    if len(result) != len(rows):
        raise AssertionError(f"duplicate {key}")
    return result


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frozen_file_matches(commit: str, name: str) -> bool:
    path = f"{HERE.name}/{name}"
    frozen = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True,
                            capture_output=True).stdout
    return frozen == (HERE / name).read_bytes()


def main() -> None:
    checks: dict[str, str] = {}
    completions = read_tsv(HERE / "COMPLETION_UNIVERSE.tsv")
    readouts = read_tsv(HERE / "READOUT_UNIVERSE.tsv")
    gates = read_tsv(HERE / "MAP_GATE_UNIVERSE.tsv")
    relations = read_tsv(HERE / "RELATION_UNIVERSE.tsv")
    completion_ids = {f"FC{i:02d}_{name}" for i, name in enumerate((
        "BOUNDARY_BOUNDARY", "ONE_CAP_BOUNDARY", "TWO_CAP_P0", "TWO_CAP_P1",
        "TWO_CAP_P_GT1", "NONPRIMITIVE_CAP", "PERIODIC_TORUS_BUNDLE", "MIRROR_DOUBLE",
        "NONORIENTABLE_GLUE", "STRATIFIED_PROJECTOR", "NONINTEGRABLE_DISTRIBUTION",
        "RECIPROCAL_TORIC_DIAGONAL",
    ), start=1)}
    require("A01_completion_universe_exact", len(completions) == 12 and
            set(keyed(completions, "completion_id")) == completion_ids, checks)
    require("A02_readout_universe_exact", len(readouts) == 17 and
            set(keyed(readouts, "readout_id")) == {f"R{i:02d}" for i in range(1, 18)}, checks)
    require("A03_gate_universe_exact", len(gates) == 10 and
            set(keyed(gates, "gate_id")) == {f"M{i:02d}" for i in range(1, 11)}, checks)
    require("A04_relation_universe_exact", len(relations) == 10 and
            set(keyed(relations, "relation_id")) == {f"Q{i:02d}" for i in range(1, 11)}, checks)

    falsification = read_tsv(HERE / "FALSIFICATION_CONTRACT.tsv")
    require("A05_falsification_universe_exact", len(falsification) == 22 and
            set(keyed(falsification, "contract_id")) == {f"F{i:02d}" for i in range(1, 23)}, checks)
    prereg_files = (
        "COMPLETION_UNIVERSE.tsv", "FALSIFICATION_CONTRACT.tsv", "MAP_GATE_UNIVERSE.tsv",
        "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "READOUT_UNIVERSE.tsv",
        "RELATION_UNIVERSE.tsv", "SOURCE_MANIFEST.tsv", "SOURCE_SCOPE.tsv", "build_source_manifest.py",
    )
    require("A06_preregistration_unchanged", all(frozen_file_matches(PREREG, name) for name in prereg_files), checks)
    require("A07_source_amendment_unchanged", all(frozen_file_matches(AMENDMENT, name) for name in
            ("PREREGISTRATION_SOURCE_AMENDMENT_01.md", "SOURCE_MANIFEST_AMENDMENT_01.tsv")), checks)
    require("A08_source_correction_unchanged", all(frozen_file_matches(CORRECTION, name) for name in
            ("SOURCE_MANIFEST_CORRECTION_01.md", "SOURCE_MANIFEST_CORRECTION_01.tsv")), checks)

    source_rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv") + read_tsv(HERE / "SOURCE_MANIFEST_AMENDMENT_01.tsv")
    source_by_id = keyed(source_rows, "source_id")
    correction_rows = read_tsv(HERE / "SOURCE_MANIFEST_CORRECTION_01.tsv")
    corrections = {(row["source_id"], row["field"]): row["corrected_value"] for row in correction_rows}
    require("A09_source_universe_and_overlay_exact", len(source_rows) == 21 and
            set(source_by_id) == {f"S{i:02d}" for i in range(1, 22)} and
            len(correction_rows) == 1 and set(corrections) == {("S17", "sha256")}, checks)
    source_scope = keyed(read_tsv(HERE / "SOURCE_SCOPE.tsv"), "source_id")
    require("A10_source_scope_exact", set(source_scope) == {f"S{i:02d}" for i in range(1, 17)} and
            all(source_scope[sid]["path"] == source_by_id[sid]["path"] and
                source_scope[sid]["role"] == source_by_id[sid]["role"] for sid in source_scope), checks)
    source_integrity = True
    for item in source_rows:
        path = ROOT / item["path"]
        expected_sha = corrections.get((item["source_id"], "sha256"), item["sha256"])
        source_integrity &= re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None and path.is_file()
        if not path.is_file():
            continue
        frozen = subprocess.run(["git", "show", f"{BASE}:{item['path']}"], cwd=ROOT, check=True,
                                capture_output=True).stdout
        source_integrity &= path.stat().st_size == int(item["size_bytes"])
        source_integrity &= digest(path.read_bytes()) == expected_sha == digest(frozen)
    require("A11_source_identities_21", source_integrity, checks)

    completion_registry = keyed(read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "COMPLETION_CLASS_REGISTRY.tsv"), "completion_id")
    bundle_all = read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "BUNDLE_HOLONOMY_ATLAS.tsv")
    bundle = keyed([row for row in bundle_all if "::" not in row["completion_id"]], "completion_id")
    transport = keyed(read_tsv(ROOT / "udt_dual_systole_global_transport_audit_2026-07-24" / "GLOBAL_TRANSPORT_ATLAS.tsv"), "completion_id")
    selectors = read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "SELECTOR_MATRIX.tsv")
    require("A12_completion_registry_exact_coverage", set(completion_registry) == completion_ids, checks)
    require("A13_bundle_main_exact_coverage", set(bundle) == set(completion_registry), checks)
    require("A14_systole_transport_exact_coverage", set(transport) == set(completion_registry), checks)
    selector_ids = {row["selector_id"] for row in selectors}
    selector_pairs = {(row["selector_id"], row["completion_id"]) for row in selectors}
    require("A15_all_registered_selector_rows_nonselecting",
            len(selectors) == 84 and len(selector_ids) == 7 and
            selector_pairs == {(selector, fc) for selector in selector_ids for fc in completion_ids} and
            {row["selection_power"] for row in selectors} == {"NONSELECTING_IN_CURRENT_REGISTRY"}, checks)

    # Exact cap determinant family controls.
    cap_rows = read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "CAP_PAIR_WITNESSES.tsv")
    cap_counts: Counter[str] = Counter()
    cap_identities_ok = True
    for row in cap_rows:
        vm = ast.literal_eval(row["v_minus"])
        vp = ast.literal_eval(row["v_plus"])
        det = vm[0] * vp[1] - vm[1] * vp[0]
        cap_identities_ok &= det == int(row["signed_determinant"])
        p = abs(det)
        cap_counts["P0" if p == 0 else "P1" if p == 1 else "P_GT1"] += 1
    require("A16_cap_determinants_256", cap_identities_ok and len(cap_rows) == 256, checks)
    require("A17_cap_witness_counts", cap_counts == Counter({"P_GT1": 182, "P1": 58, "P0": 16}), checks)

    monodromy_rows = read_tsv(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "TORUS_MONODROMY_REGISTRY.tsv")
    monodromy_identities_ok = True
    for row in monodromy_rows:
        matrix = ast.literal_eval(row["matrix"])
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        monodromy_identities_ok &= det == int(row["determinant"]) and abs(det) == 1
    require("A18_monodromy_determinants", monodromy_identities_ok, checks)
    require("A19_monodromy_control_count", len(monodromy_rows) == 8, checks)

    regularity = {ident: completion_registry[ident]["regularity"] for ident in completion_registry}
    boundary_desc = {
        "FC01_BOUNDARY_BOUNDARY": "TWO_PHYSICAL_BOUNDARIES_REQUIRE_EMBEDDING_AND_BOUNDARY_DATA",
        "FC02_ONE_CAP_BOUNDARY": "ONE_REGULAR_CAP_PLUS_PHYSICAL_BOUNDARY_REQUIRE_JETS_AND_BOUNDARY_DATA",
        "FC03_TWO_CAP_P0": "TWO_DEPENDENT_CAPS_REQUIRE_REGULAR_CAP_JETS",
        "FC04_TWO_CAP_P1": "TWO_UNIMODULAR_CAPS_REQUIRE_REGULAR_CAP_JETS",
        "FC05_TWO_CAP_P_GT1": "TWO_CAPS_AND_LENS_QUOTIENT_REQUIRE_REGULAR_JETS_AND_QUOTIENT_DATA",
        "FC06_NONPRIMITIVE_CAP": "ORBIFOLD_OR_SINGULAR_CAP_REQUIRES_STRATIFIED_MEASURE",
        "FC07_PERIODIC_TORUS_BUNDLE": "NO_PHYSICAL_BOUNDARY__PERIODIC_GLUE_AND_MONODROMY_REQUIRED",
        "FC08_MIRROR_DOUBLE": "MIRROR_FIXED_SET_AND_LIFT_JETS_REQUIRED",
        "FC09_NONORIENTABLE_GLUE": "NO_PHYSICAL_BOUNDARY__ORIENTATION_REVERSING_GLUE_REQUIRED",
        "FC10_STRATIFIED_PROJECTOR": "RANK_STRATA_AND_MATCHING_DATA_REQUIRED",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "BOUNDARY_STATUS_DEPENDS_ON_FINITE_OR_PERIODIC_BASE__NO_ORBIT_SURFACE",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "ENDPOINT_BOUNDARY_OR_CAP_SUBCASE_DATA_REQUIRED",
    }
    lc_path_ruling = {
        "FC01_BOUNDARY_BOUNDARY": "OPEN_PATH_LC_MAP_REQUIRES_COMPLETE_METRIC_AND_ENDPOINT_FRAMES",
        "FC02_ONE_CAP_BOUNDARY": "OPEN_PATH_LC_MAP_REQUIRES_SMOOTH_CAP_EXTENSION_OR_PATH_AVOIDANCE",
        "FC03_TWO_CAP_P0": "OPEN_PATH_LC_MAP_REQUIRES_SMOOTH_CAP_EXTENSIONS_OR_PATH_AVOIDANCE",
        "FC04_TWO_CAP_P1": "OPEN_PATH_LC_MAP_REQUIRES_SMOOTH_CAP_EXTENSIONS_OR_PATH_AVOIDANCE",
        "FC05_TWO_CAP_P_GT1": "OPEN_PATH_LC_MAP_REQUIRES_QUOTIENT_LIFT_AND_SMOOTH_CAP_EXTENSIONS",
        "FC06_NONPRIMITIVE_CAP": "OPEN_PATH_LC_MAP_ONLY_WITHIN_REGULAR_STRATUM_UNLESS_SINGULAR_MATCHING_SUPPLIED",
        "FC07_PERIODIC_TORUS_BUNDLE": "OPEN_PATH_LC_MAP_REQUIRES_GLUE_TRANSITION_WHEN_PATH_CROSSES_PERIODIC_SEAM",
        "FC08_MIRROR_DOUBLE": "OPEN_PATH_LC_MAP_REQUIRES_DECLARED_MIRROR_LIFT_WHEN_PATH_CROSSES_FIXED_SET",
        "FC09_NONORIENTABLE_GLUE": "OPEN_PATH_LC_MAP_REQUIRES_ORIENTATION_REVERSING_TANGENT_TRANSITION_AT_GLUE",
        "FC10_STRATIFIED_PROJECTOR": "AMBIENT_LC_PATH_MAP_CROSSES_PROJECTOR_TRANSITION_IF_METRIC_REGULAR__COMPLETE_METRIC_PROFILE_REQUIRED",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "AMBIENT_TANGENT_LC_PATH_MAP_REMAINS_PROFILE_DEPENDENT__NOT_DISTRIBUTION_TRANSPORT",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "DEPTH_PATH_LC_MAP_REQUIRES_COMPLETE_PROFILE__KATO_ZERO_DOES_NOT_IMPLY_LC_ZERO",
    }
    t2_holonomy_ruling = {
        "FC01_BOUNDARY_BOUNDARY": "FIXED_CLOSED_LOOP_IN_REGULAR_TORIC_REGION_ONLY__BOUNDARY_CROSSING_NOT_DEFINED",
        "FC02_ONE_CAP_BOUNDARY": "FIXED_CLOSED_LOOP_IN_REGULAR_TORIC_REGION__CAP_EXTENSION_REQUIRES_DEGENERATING_CYCLE_RULE",
        "FC03_TWO_CAP_P0": "REGULAR_LOCUS_T2_HOLONOMY_ONLY__BOTH_CAP_EXTENSIONS_REQUIRE_CYCLE_RULES",
        "FC04_TWO_CAP_P1": "REGULAR_LOCUS_T2_HOLONOMY_ONLY__BOTH_CAP_EXTENSIONS_REQUIRE_CYCLE_RULES",
        "FC05_TWO_CAP_P_GT1": "REGULAR_LOCUS_T2_HOLONOMY_ONLY__CAP_AND_LENS_QUOTIENT_LIFTS_REQUIRED",
        "FC06_NONPRIMITIVE_CAP": "REGULAR_STRATUM_T2_HOLONOMY_ONLY__SINGULAR_ISOTROPY_MATCHING_NOT_SUPPLIED",
        "FC07_PERIODIC_TORUS_BUNDLE": "PERIODIC_LOOP_REQUIRES_MONODROMY_COMPATIBLE_T2_CONNECTION_AND_ENDPOINT_GLUE",
        "FC08_MIRROR_DOUBLE": "MIRROR_CROSSING_LOOP_REQUIRES_DECLARED_Z2_LIFT_OF_T2_CONNECTION",
        "FC09_NONORIENTABLE_GLUE": "GLUE_CROSSING_LOOP_REQUIRES_DET_MINUS_ONE_LATTICE_ACTION_ON_T2_HOLONOMY",
        "FC10_STRATIFIED_PROJECTOR": "T2_HOLONOMY_ONLY_ON_FIXED_RANK_TORIC_STRATUM__CROSS_STRATUM_RULE_ABSENT",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "NO_GLOBAL_T2_CONNECTION_HOLONOMY_OBJECT",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "FIXED_LOOP_T2_HOLONOMY_CONDITIONAL_ON_COMPLETE_S_PROFILE__NO_PRINCIPAL_CIRCLE_PROJECTION_ASSUMED",
    }

    source_by_readout = {
        "R01": "S13", "R02": "S01;S09", "R03": "S01;S09", "R04": "S05;S09",
        "R05": "S01;S14", "R06": "S04;S17", "R07": "S04;S17", "R08": "S04;S06;S17",
        "R09": "S12;S17", "R10": "S05;S12;S17", "R11": "S05;S17;S19;S20",
        "R12": "S07;S08;S21", "R13": "S05", "R14": "S10", "R15": "S11",
        "R16": "S05;S19;S20", "R17": "S04;S15;S17",
    }

    matrix_rows: list[dict[str, str]] = []
    for completion in completions:
        fc = completion["completion_id"]
        reg = regularity[fc]
        toric = transport[fc]["torus_lattice"]
        for readout in readouts:
            rid = readout["readout_id"]
            row = {
                "completion_id": fc,
                "readout_id": rid,
                "M01": "CONDITIONAL_DEFINITION",
                "M02": "ABSENT_NO_COMPLETE_METRIC_WITNESS",
                "M03": "DOMAIN_DATA_REQUIRED",
                "M04": reg,
                "M05": "GLOBAL_COMPLETION_DATA_REQUIRED",
                "M06": "OPEN_PHYSICAL_REPRESENTATIVE_AND_SCALE",
                "M07": "INCOMPLETE_GLOBAL_VARIATION",
                "M08": "TYPE_OR_CONDITIONAL_SCHEMA_ONLY",
                "M09": "INVARIANCE_TYPED_CONDITIONALLY",
                "M10": "PASS_NO_PHYSICAL_CLOSURE_PROMOTION",
                "availability": "CONDITIONAL_COMPONENT_SCHEMA",
                "dependency_tags": "complete_metric_profile",
                "completion_specific_ruling": "NO_COMPLETE_PROFILE_VALUES_AVAILABLE",
                "source_basis": source_by_readout[rid],
            }
            if rid == "R01":
                row.update(M01="PASS_LOCAL_GEOMETRIC_DEFINITION", M03="LOCAL_CHART_OR_COFRAME",
                           M05="LOCAL_ONLY_NOT_GLOBAL", M06="OPEN_REPRESENTATIVE",
                           M07="LOCAL_LINEARIZATION_NOT_PHYSICAL_RESPONSE", M08="FORMULA_AVAILABLE_VALUES_REQUIRE_PROFILE",
                           M09="TENSORIAL_OR_FRAME_COMPONENT_TYPE_EXPLICIT", availability="LOCAL_FORMULA_AVAILABLE",
                           dependency_tags="metric_or_coframe;Levi_Civita_connection",
                           completion_specific_ruling="STRATUMWISE_WHERE_METRIC_REGULAR" if fc in {"FC06_NONPRIMITIVE_CAP", "FC10_STRATIFIED_PROJECTOR"} else "LOCAL_ON_REGULAR_METRIC_REGION")
            elif rid == "R02":
                row.update(M03="SPACETIME_REGION_AND_TIME_DOMAIN_REQUIRED", M05=boundary_desc[fc],
                           M07="FIXED_REGION_FORMULA__MOVING_BOUNDARY_GLUE_MODULUS_INCOMPLETE",
                           dependency_tags="metric_representative;spacetime_region;boundary_or_glue",
                           completion_specific_ruling="V4_COMPONENT_CONDITIONAL_NOT_EVALUABLE")
            elif rid == "R03":
                row.update(M03="PHYSICAL_SPATIAL_SLICE_AND_REGION_REQUIRED", M05=boundary_desc[fc],
                           M07="FIXED_SLICE_FORMULA__MOVING_BOUNDARY_GLUE_MODULUS_INCOMPLETE",
                           dependency_tags="metric_representative;spatial_slice;boundary_or_glue",
                           completion_specific_ruling="V3_COMPONENT_CONDITIONAL_NOT_EVALUABLE")
            elif rid == "R04":
                row.update(M03="TYPED_NONNULL_EMBEDDING_CAP_STRATUM_CORNER_OR_JOINT_REQUIRED", M05=boundary_desc[fc],
                           M07="FIXED_EMBEDDING_FORMULA__SHAPE_CORNER_NULL_CHANNELS_INCOMPLETE",
                           dependency_tags="metric_representative;embedding;normal_or_null_structure;corner_data",
                           completion_specific_ruling="BOUNDARY_CAP_STRATUM_SCHEMA_ONLY")
            elif rid == "R05":
                row.update(M01="UNSELECTED_FUNCTIONAL_FAMILY", M03="FUNCTIONAL_SLICE_REGION_AND_BOUNDARY_REQUIRED",
                           M05=boundary_desc[fc], M07="BULK_EXAMPLES_EXIST__COMPLETE_BOUNDARY_GLOBAL_VARIATION_ABSENT",
                           M08="NOT_SELECTED_AS_R_GEOM_COMPONENT", M09="SCALAR_ONLY_AFTER_DOMAIN_AND_BOUNDARY_CHOICE",
                           availability="UNSELECTED_FAMILY", dependency_tags="metric;functional_choice;domain;boundary_functional",
                           completion_specific_ruling="COUNTERFAMILY_PREVENTS_NATIVE_COMPONENT_SELECTION")
            elif rid == "R06":
                row.update(M03="PATH_AND_ENDPOINT_FRAMES_REQUIRED", M05="OPEN_PATH_NEEDS_NO_LOOP_DESCENT__CROSS_STRATUM_PATH_MAY_FAIL",
                           M07="FIXED_PATH_CONNECTION_VARIATION_ONLY", M08="ENDPOINT_MAP_REQUIRES_COMPLETE_PROFILE",
                           M09="ENDPOINT_FRAME_COVARIANCE_TYPED", dependency_tags="metric_profile;path;endpoint_frames",
                           completion_specific_ruling=lc_path_ruling[fc])
            elif rid == "R07":
                row.update(M03="BASED_LOOP_AND_BASE_FRAME_OR_CONJUGACY_RULE_REQUIRED",
                           M05="LOOP_EXISTENCE_AND_GLOBAL_PROFILE_REQUIRED", M07="LOOP_AND_CONNECTION_VARIATION_NOT_COMPLETED",
                           M08="HOLONOMY_NOT_COMPUTED_WITHOUT_COMPLETE_PROFILE", M09="CONJUGACY_CLASS_REMOVES_BASE_FRAME_ONLY",
                           dependency_tags="metric_profile;closed_loop;basepoint_or_conjugacy",
                           completion_specific_ruling=bundle[fc]["levi_civita_tangent_holonomy"])
            elif rid == "R08":
                row.update(M01="PASS_CONDITIONAL_PROJECTOR_BUNDLE", M03="SMOOTH_PROJECTOR_FAMILY_AND_PATH_REQUIRED",
                           M05="GLOBAL_PROJECTOR_SUBBUNDLE_OR_STRATUM_REQUIRED", M06="METRIC_COMPATIBLE",
                           M07="EXACT_KATO_TRANSPORT_ON_SMOOTH_FIXED_RANK_PATH", M08="CONDITIONAL_PATH_MAP_NOT_COMPLETE_BRANCH_READOUT",
                           M09="PROJECTOR_BUNDLE_COVARIANT", availability="CONDITIONAL_TRANSPORT_MAP",
                           dependency_tags="metric;projector_family;path;fixed_rank_stratum",
                           completion_specific_ruling=bundle[fc]["projector_kato_transport"])
            elif rid == "R09":
                if fc == "FC11_NONINTEGRABLE_DISTRIBUTION":
                    row.update(M01="UNAVAILABLE_NO_GLOBAL_TORIC_LATTICE", M03="ABSENT_TORIC_ORBIT_CHART", M05="FROBENIUS_OBSTRUCTION",
                               M06="NOT_APPLICABLE", M07="NOT_APPLICABLE", M08="UNAVAILABLE", M09="NOT_APPLICABLE", availability="UNAVAILABLE_ON_CLASS",
                               dependency_tags="missing_integral_torus_bundle", completion_specific_ruling="NO_GLOBAL_TORUS_CONNECTION_OBJECT")
                else:
                    row.update(M01="PASS_LOCAL_ON_TORIC_REGION", M03="TORIC_CHART_AND_CONNECTION_REQUIRED",
                               M05="GLOBAL_DESCENT_" + toric, M06="NORMALIZED_TORIC_OBJECT__PHYSICAL_SCALE_OPEN",
                               M07="LOCAL_CONNECTION_CURVATURE_VARIATION_ONLY", M08="LOCAL_FORMULA_VALUES_REQUIRE_PROFILE",
                               M09="TORUS_GAUGE_CURVATURE_COVARIANT", availability="LOCAL_TORIC_FORMULA_AVAILABLE",
                               dependency_tags="integral_torus_region;connection_S", completion_specific_ruling="F=dS_" + toric)
            elif rid == "R10":
                if fc == "FC11_NONINTEGRABLE_DISTRIBUTION":
                    row.update(M01="UNAVAILABLE_NO_GLOBAL_TORIC_LATTICE", M03="ABSENT_TORUS_LOOP_OBJECT", M05="FROBENIUS_OBSTRUCTION",
                               M06="NOT_APPLICABLE", M07="NOT_APPLICABLE", M08="UNAVAILABLE", M09="NOT_APPLICABLE", availability="UNAVAILABLE_ON_CLASS",
                               dependency_tags="missing_integral_torus_bundle", completion_specific_ruling=t2_holonomy_ruling[fc])
                else:
                    row.update(M03="CLOSED_BASE_LOOP_T2_CONNECTION_AND_LATTICE_TRIVIALIZATION_REQUIRED", M05=t2_holonomy_ruling[fc],
                               M06="PERIOD_AND_COMMON_SCALE_TYPED_SEPARATELY", M07="CONTINUOUS_FIXED_LOOP_VARIATION__GLOBAL_LIFT_INCOMPLETE",
                               M08="CONDITIONAL_T2_LOOP_MAP_NOT_NUMERIC", M09="T2_GAUGE_CLASS_WITH_MONODROMY_ACTION_TYPED",
                               dependency_tags="R09;closed_loop;integral_lattice;global_lift",
                               completion_specific_ruling=t2_holonomy_ruling[fc])
            elif rid == "R11":
                lattice_data = bundle[fc]["torus_lattice_or_cap_data"]
                unavailable = fc == "FC11_NONINTEGRABLE_DISTRIBUTION"
                stratified = fc == "FC10_STRATIFIED_PROJECTOR"
                row.update(M01="UNAVAILABLE_NO_INTEGRAL_LATTICE" if unavailable else
                           "CONDITIONAL_STRATIFIED_DISCRETE_SCHEMA" if stratified else "PASS_DISCRETE_FAMILY_SCHEMA",
                           M03="ABSENT_NO_GLOBAL_INTEGRAL_TORUS_LATTICE" if unavailable else "COMPLETION_GLUE_CAP_OR_MONODROMY_PARAMETERS",
                           M05="NOT_APPLICABLE_NO_GLOBAL_INTEGRAL_LATTICE" if unavailable else lattice_data,
                           M06="NOT_APPLICABLE" if unavailable else "DIMENSIONLESS_INTEGRAL_DATA",
                           M07="NOT_APPLICABLE" if unavailable else "DISCRETE_LOCALLY_CONSTANT__NO_OFFSHELL_COVECTOR",
                           M08="UNAVAILABLE" if unavailable else
                           "CONDITIONAL_STRATUM_SCHEMA_NOT_REALIZED" if stratified else
                           "DISCRETE_FAMILY_SCHEMA_EVALUABLE_NOT_REALIZED_WITNESS",
                           M09="NOT_APPLICABLE" if unavailable else "GL2Z_EQUIVALENCE_AND_ORIENTATION_TYPED",
                           availability="UNAVAILABLE_ON_CLASS" if unavailable else
                           "CONDITIONAL_STRATIFIED_DISCRETE_SCHEMA" if stratified else "DISCRETE_FAMILY_SCHEMA_ONLY",
                           dependency_tags="integral_lattice;cap_cycles_or_glue_matrix",
                           completion_specific_ruling="NOT_APPLICABLE_NO_GLOBAL_INTEGRAL_LATTICE__SOURCE_REGISTERED_NONE_OR_OPEN" if unavailable else lattice_data)
            elif rid == "R12":
                unavailable = fc == "FC11_NONINTEGRABLE_DISTRIBUTION"
                row.update(M01="UNAVAILABLE_NO_GLOBAL_DEFINITION" if unavailable else "PASS_SET_VALUED_TORIC_DEFINITION",
                           M03="ABSENT_NO_GLOBAL_NORMALIZED_H_OR_INTEGRAL_CHARACTER_LATTICE" if unavailable else "NORMALIZED_H_AND_INTEGRAL_CHARACTER_LATTICE",
                           M05=transport[fc]["global_outcome"],
                           M06="NOT_APPLICABLE" if unavailable else "NORMALIZED_SHAPE_AVAILABLE__PHYSICAL_LENGTH_NEEDS_COMMON_SCALE_AND_PERIODS",
                           M07="NOT_APPLICABLE" if unavailable else "STRATIFIED_CHAMBER_DERIVATIVE_AND_SET_VALUED_TIE_RULE",
                           M08="UNAVAILABLE" if unavailable else "CONDITIONAL_SET_VALUED_MAP_REQUIRES_PROFILE",
                           M09="NOT_APPLICABLE" if unavailable else "GL2Z_COVARIANT_SET",
                           availability="UNAVAILABLE_ON_CLASS" if unavailable else "CONDITIONAL_STRATIFIED_MAP",
                           dependency_tags="normalized_angular_metric_H;integral_lattice;common_scale_for_length",
                           completion_specific_ruling=transport[fc]["global_outcome"])
            elif rid == "R13":
                row.update(M01="PASS_PARAMETRIC_COMPLETION_MODULI", M03="COMPLETE_PROFILE_AND_EQUIVALENCE_RULE_REQUIRED",
                           M05=boundary_desc[fc], M07="MODULUS_AND_MOVING_DOMAIN_VARIATION_INCOMPLETE",
                           M08="PARAMETRIC_MODULI_SCHEMA_NOT_REALIZED_VALUES", M09="QUOTIENT_BY_COORDINATE_AND_LATTICE_EQUIVALENCE_REQUIRED",
                           availability="PARAMETRIC_MODULI_SCHEMA", dependency_tags="completion_parameters;metric_profile;equivalence_rule",
                           completion_specific_ruling=completion_registry[fc]["infinite_family_rule"])
            elif rid == "R14":
                row.update(M01="PASS_CONDITIONAL_TEMPORAL_PHI_DEFINITION", M03="EVERYWHERE_TIMELIKE_NONZERO_DPHI_AND_COMPLETE_CONNECTED_LEVELS",
                           M05="GLOBAL_LEVEL_SET_DESCENT_NOT_SUPPLIED", M06="CANONICAL_PRE_SCALE_H0__PHYSICAL_RULER_OPEN",
                           M07="DISTANCE_VARIATION_NONSMOOTH_AT_CUT_LOCUS", M08="NO_REGISTERED_COMPLETE_TEMPORAL_PHI_BRANCH",
                           M09="CHART_COFRAME_INVARIANT_ON_CONDITIONAL_BRANCH", availability="CONDITIONAL_BRANCH_SCHEMA",
                           dependency_tags="metric;phi;timelike_dphi;complete_levels;physical_ruler",
                           completion_specific_ruling="NOT_APPLICABLE_TO_STATIC_SPATIAL_PHI_CONTROL" if fc == "FC12_RECIPROCAL_TORIC_DIAGONAL" else "CAUSAL_BRANCH_NOT_SPECIFIED_BY_COMPLETION_CLASS")
            elif rid == "R15":
                row.update(M01="TYPE_ONLY_OPEN", M03="OBSERVER_DOMAIN_EVENT_COMPARISON_AND_NATIVE_Dg_ABSENT",
                           M05="GLOBAL_FINITE_COMPLETE_DOMAIN_AND_ATTAINMENT_OPEN", M06="PHYSICAL_RULER_OPEN",
                           M07="NO_VARIATION__NONATTAINMENT_CUT_AND_MULTIMAX_BRANCHES_OPEN", M08="UNAVAILABLE",
                           M09="RELATIONAL_INVARIANCE_REQUIREMENT_ONLY", availability="OPEN_TYPE_ONLY",
                           dependency_tags="observer_domain;event_pairing;native_Dg;complete_branch",
                           completion_specific_ruling="Xmax_SUPREMUM_NOT_COMPUTABLE")
            elif rid == "R16":
                row.update(M01="PASS_DISCRETE_COMPLETION_FAMILY_LABEL", M03="CAP_GLUE_OR_STRATUM_PARAMETERS",
                           M05=completion_registry[fc]["topology_family"], M06="DIMENSIONLESS_DISCRETE_DATA",
                           M07="DISCRETE_LOCALLY_CONSTANT__NO_OFFSHELL_COVECTOR", M08="DISCRETE_FAMILY_LABEL_EVALUABLE",
                           M09="HOMEOMORPHISM_OR_ORBIFOLD_EQUIVALENCE_CLASS", availability="DISCRETE_CLASSIFICATION_AVAILABLE",
                           dependency_tags="completion_gluing_and_discrete_parameters",
                           completion_specific_ruling=completion_registry[fc]["topology_family"])
            elif rid == "R17":
                host = fc in {"FC04_TWO_CAP_P1", "FC12_RECIPROCAL_TORIC_DIAGONAL"}
                row.update(M01="CONDITIONAL_MAP_OR_BUNDLE_REQUIRED", M03="CARRIER_MAP_PHASE_PERIOD_OR_FREE_ACTION_AND_BOUNDARY_CLASS_REQUIRED",
                           M05="HOST_S3_SUBCASE_AVAILABLE__MAP_NOT_SUPPLIED" if host else "TOPOLOGICAL_MAP_AND_GLOBAL_EXTENSION_NOT_SUPPLIED",
                           M06="DIMENSIONLESS_LABEL__NORMALIZATION_AND_ORIENTATION_CONDITIONAL",
                           M07="DISCRETE_WITHIN_FIXED_MAP_SECTOR__BOUNDARY_ESCAPE_AND_SINGULARITY_OPEN", M08="CONDITIONAL_ONLY_NOT_NATIVE_R_GEOM",
                           M09="MAP_HOMOTOPY_OR_BUNDLE_CLASS_AFTER_SUPPLIED_STRUCTURE", availability="CONDITIONAL_TOPOLOGICAL_SCHEMA",
                           dependency_tags="carrier_or_bundle_map;periods;orientation;boundary_class",
                           completion_specific_ruling=bundle[fc]["principal_circle_characteristic_data"])
            matrix_rows.append(row)

    require("A20_matrix_12_by_17", len(matrix_rows) == 204, checks)
    require("A21_matrix_unique_pairs", len({(row["completion_id"], row["readout_id"]) for row in matrix_rows}) == 204, checks)
    require("A22_no_complete_metric_witness", {row["M02"] for row in matrix_rows} == {"ABSENT_NO_COMPLETE_METRIC_WITNESS"}, checks)
    fc11_toric = [row for row in matrix_rows if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION" and row["readout_id"] in {"R09", "R10", "R11", "R12"}]
    require("A23_FC11_toric_objects_fail_closed", len(fc11_toric) == 4 and
            all(row["availability"] == "UNAVAILABLE_ON_CLASS" for row in fc11_toric) and
            all(row[gate] == "NOT_APPLICABLE" for row in fc11_toric for gate in ("M07", "M09")), checks)
    require("A24_no_complete_R_geom_component", all(row["M08"] != "COMPLETE_R_GEOM" for row in matrix_rows), checks)
    require("A25_no_physical_closure_promotion", {row["M10"] for row in matrix_rows} == {"PASS_NO_PHYSICAL_CLOSURE_PROMOTION"}, checks)

    fields = ["completion_id", "readout_id"] + [f"M{i:02d}" for i in range(1, 11)] + ["availability", "dependency_tags", "completion_specific_ruling", "source_basis"]
    write_tsv("COMPLETION_READOUT_MATRIX.tsv", fields, matrix_rows)

    schema_rows: list[dict[str, str]] = []
    for completion in completions:
        fc = completion["completion_id"]
        subset = [row for row in matrix_rows if row["completion_id"] == fc]
        counts = Counter(row["availability"] for row in subset)
        schema_rows.append({
            "completion_id": fc,
            "local_formula_schema_entries": str(sum(v for k, v in counts.items() if "LOCAL" in k)),
            "conditional_or_parametric_schema_entries": str(sum(v for k, v in counts.items() if "CONDITIONAL" in k or "PARAMETRIC" in k)),
            "discrete_classification_schema_entries": str(sum(v for k, v in counts.items() if k.startswith("DISCRETE_"))),
            "unavailable_schema_entries": str(counts["UNAVAILABLE_ON_CLASS"] + counts["OPEN_TYPE_ONLY"]),
            "unselected_family_entries": str(counts["UNSELECTED_FAMILY"]),
            "total_readout_entries": str(len(subset)),
            "complete_metric_witnesses": "0",
            "complete_R_geom_status": "NOT_AVAILABLE_NO_COMPLETE_METRIC_WITNESS",
            "selection_status": completion_registry[fc]["selection_status"],
        })
    write_tsv("R_GEOM_SCHEMA.tsv", list(schema_rows[0]), schema_rows)
    require("A26_schema_exact_partition", len(schema_rows) == 12 and
            {row["completion_id"] for row in schema_rows} == set(completion_registry) and
            all(sum(int(row[name]) for name in (
                "local_formula_schema_entries", "conditional_or_parametric_schema_entries",
                "discrete_classification_schema_entries", "unavailable_schema_entries",
                "unselected_family_entries")) == int(row["total_readout_entries"]) == 17
                for row in schema_rows), checks)

    relation_status = {
        "Q01": ("GEOMETRIC_IDENTITY", "local_coframe_and_connection", "does_not_select_global_readouts_or_physical_response", "S13"),
        "Q02": ("GEOMETRIC_IDENTITY", "local_curvature_and_covariant_derivative", "does_not_supply_dynamics_or_bootstrap", "S13;S14"),
        "Q03": ("COMPLETION_COMPATIBILITY", "toric_connection_loop_and_global_lift", "local_F_does_not_determine_holonomy_without_global_profile", "S12;S17"),
        "Q04": ("DISCRETE_CLASSIFICATION_RULE", "primitive_cap_pair", "p_abs_det_classifies_family_but_does_not_select_caps", "S05;S20"),
        "Q05": ("DISCRETE_CLASSIFICATION_RULE", "GL2Z_glue_matrix", "monodromy_defines_bundle_data_but_does_not_select_matrix", "S19"),
        "Q06": ("COMPLETION_COMPATIBILITY", "reciprocal_exchange_and_declared_lift", "symmetry_compatibility_leaves_all_twelve_classes_nonselected", "S18"),
        "Q07": ("GEOMETRIC_IDENTITY", "constant_common_rescaling_or_normalized_H", "ontology_scale_weights_and_invariants_do_not_select_physical_representative", "S01;S12;S18"),
        "Q08": ("COMPLETION_COMPATIBILITY", "toric_lattice_profile_and_completion", "stratified_wall_crossing_constrains_transport_but_selects_no_line_or_completion", "S07;S08;S21"),
        "Q09": ("SOURCE_GAP", "not_defined_in_frozen_sources", "no_imported_index_theorem_used_to_fill_gap", "NONE"),
        "Q10": ("NOT_DERIVED", "complete_physical_state_vector_and_two_bootstrap_arrows_absent", "self_consistency_word_does_not_define_fixed_point_operator", "S01;S14"),
    }
    relation_rows = []
    for relation in relations:
        status, domain, consequence, source = relation_status[relation["relation_id"]]
        relation_rows.append({"relation_id": relation["relation_id"], "classification": status,
                              "domain_or_inputs": domain, "exact_consequence": consequence,
                              "physical_closure": "NO", "source_basis": source})
    write_tsv("RELATION_MATRIX.tsv", list(relation_rows[0]), relation_rows)
    allowed_relation_classes = {
        "GEOMETRIC_IDENTITY", "COMPLETION_COMPATIBILITY", "DISCRETE_CLASSIFICATION_RULE",
        "CONDITIONAL_ON_COMPLETE_BRANCH", "SOURCE_GAP", "NOT_DERIVED", "PHYSICAL_CLOSURE_RELATION",
    }
    require("A27_relation_exact_coverage_and_labels", len(relation_rows) == 10 and
            set(keyed(relation_rows, "relation_id")) == {f"Q{i:02d}" for i in range(1, 11)} and
            {row["classification"] for row in relation_rows} <= allowed_relation_classes, checks)
    require("A28_zero_physical_closure_relations", {row["physical_closure"] for row in relation_rows} == {"NO"}, checks)

    linkage_rows = [
        {"linkage_id": "K01", "upstream_object": "complete_metric_or_coframe_profile", "downstream_readouts": "R01;R02;R03;R04;R05;R06;R07;R09;R10;R12;R13;R14;R15", "link_type": "REQUIRED_FOR_COMPLETE_REALIZATION", "current_status": "PROFILE_ABSENT_IN_ALL_12_CLASSES"},
        {"linkage_id": "K02", "upstream_object": "boundary_cap_glue_and_moduli", "downstream_readouts": "R02;R03;R04;R05;R06;R07;R08;R13;R16;R17", "link_type": "DOMAIN_DESCENT_AND_MOVING_VARIATION", "current_status": "TYPE_DATA_PRESENT__COMPLETE_GEOMETRY_AND_VARIATION_ABSENT"},
        {"linkage_id": "K03", "upstream_object": "smooth_projector_bundle_and_metric", "downstream_readouts": "R08", "link_type": "PATH_TRANSPORT", "current_status": "CONDITIONAL_EXACT_ON_SMOOTH_FIXED_RANK_PATHS"},
        {"linkage_id": "K04", "upstream_object": "integral_torus_bundle_and_lattice", "downstream_readouts": "R09;R10;R11;R12", "link_type": "TORIC_GLOBAL_DOMAIN", "current_status": "COMPLETION_DEPENDENT__ABSENT_GLOBALLY_IN_FC11"},
        {"linkage_id": "K05", "upstream_object": "cap_cycles_or_GL2Z_glue", "downstream_readouts": "R10;R11;R12;R16;R17", "link_type": "GLOBAL_CONSTRAINT", "current_status": "DISCRETE_RULES_AVAILABLE__NO_SELECTION"},
        {"linkage_id": "K06", "upstream_object": "torus_connection_S", "downstream_readouts": "R09;R10", "link_type": "CONTINUOUS_CONNECTION_DATA", "current_status": "LOCAL_SCHEMA_PRESENT__COMPLETE_PROFILE_AND_GLOBAL_LIFT_ABSENT"},
        {"linkage_id": "K07", "upstream_object": "normalized_angular_metric_H", "downstream_readouts": "R12", "link_type": "ANGULAR_NORM_DATA", "current_status": "CONDITIONAL_PROFILE__PHYSICAL_SCALE_OPEN"},
        {"linkage_id": "K08", "upstream_object": "metric_phi_timelike_nonzero_dphi_and_complete_levels", "downstream_readouts": "R14", "link_type": "CAUSAL_BRANCH_CONDITION", "current_status": "CONDITIONAL_DEFINITION__NO_COMPLETE_BRANCH"},
        {"linkage_id": "K09", "upstream_object": "observer_domain_event_pairing_and_native_Dg", "downstream_readouts": "R15", "link_type": "RELATIONAL_PROTOCOL", "current_status": "OPEN_TYPE_GAP"},
        {"linkage_id": "K10", "upstream_object": "carrier_or_bundle_map_and_boundary_class", "downstream_readouts": "R17", "link_type": "CONDITIONAL_TOPOLOGICAL_DATA", "current_status": "POSIT_OR_SUPPLIED_ONLY"},
        {"linkage_id": "K11", "upstream_object": "complete_R_geom_A_of_X_O_target_normalization_and_pairing", "downstream_readouts": "physical_bootstrap_closure", "link_type": "MISSING_CLOSURE_INPUTS_AND_OPERATOR", "current_status": "NOT_DERIVED_BY_ANY_REGISTERED_LINKAGE"},
    ]
    write_tsv("LOCK_LINKAGE_LEDGER.tsv", list(linkage_rows[0]), linkage_rows)

    graph_nodes = ({row["upstream_object"] for row in linkage_rows}
                   | {row["readout_id"] for row in readouts}
                   | {target for row in linkage_rows for target in row["downstream_readouts"].split(";")})
    graph_edges = [
        {"from": row["upstream_object"], "to": target, "type": row["link_type"], "status": row["current_status"]}
        for row in linkage_rows for target in row["downstream_readouts"].split(";")
    ]
    require("A29_dependency_graph_endpoints_declared",
            all(edge["from"] in graph_nodes and edge["to"] in graph_nodes for edge in graph_edges), checks)
    graph = {
        "schema": "udt-completion-readout-dependency-graph-1.0",
        "nodes": sorted(graph_nodes),
        "edges": graph_edges,
        "physical_closure_edges": 0,
    }
    (HERE / "DEPENDENCY_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    availability_counts = Counter(row["availability"] for row in matrix_rows)
    result = {
        "schema": "udt-completion-scoped-realized-observable-map-1.0",
        "checks": checks,
        "check_count": len(checks),
        "completion_count": 12,
        "readout_count": 17,
        "matrix_rows": 204,
        "relation_count": 10,
        "availability_counts": dict(sorted(availability_counts.items())),
        "complete_metric_witness_count": 0,
        "complete_R_geom_count": 0,
        "physical_closure_relation_count": 0,
        "maximum_supported_conclusion": "COMPLETION_SCOPED_REDUNDANT_READOUT_SCHEMA_DERIVED__NO_REALIZED_COMPLETE_R_GEOM_OR_NONIDENTITY_PHYSICAL_CLOSURE",
        "density_status": "NOT_USED__FUTURE_COMPARISON_BRACKET_DEFERRED",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
