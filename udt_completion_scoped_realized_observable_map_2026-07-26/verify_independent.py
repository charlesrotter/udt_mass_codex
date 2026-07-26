#!/usr/bin/env python3
"""Independent table/source reconstruction with exercised fail-closed mutations."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c1036fb498c8ed009733c82ee86cf96152a5ed6e"
PREREG = "c457bc4"
AMENDMENT = "b3325dd"
CORRECTION = "4a95a7b6f7231879ed1662d956603b1acb6326b8"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def table(items: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    result = {item[key]: item for item in items}
    if len(result) != len(items):
        raise ValueError(f"duplicate:{key}")
    return result


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def validate(state: dict[str, object]) -> list[str]:
    errors: list[str] = []
    try:
        completions = table(state["completions"], "completion_id")
        readouts = table(state["readouts"], "readout_id")
        gates = table(state["gates"], "gate_id")
        relations_u = table(state["relations_u"], "relation_id")
        matrix_list = state["matrix"]
        matrix = {(row["completion_id"], row["readout_id"]): row for row in matrix_list}
        relation = table(state["relation"], "relation_id")
        schema = table(state["schema"], "completion_id")
        bundle = table(state["bundle"], "completion_id")
        transport = table(state["transport"], "completion_id")
        registry = table(state["registry"], "completion_id")
        graph = state["graph"]
        selectors = state["selectors"]
    except (ValueError, KeyError, TypeError) as exc:
        return [f"structure:{exc}"]
    expected_completions = {
        "FC01_BOUNDARY_BOUNDARY", "FC02_ONE_CAP_BOUNDARY", "FC03_TWO_CAP_P0",
        "FC04_TWO_CAP_P1", "FC05_TWO_CAP_P_GT1", "FC06_NONPRIMITIVE_CAP",
        "FC07_PERIODIC_TORUS_BUNDLE", "FC08_MIRROR_DOUBLE", "FC09_NONORIENTABLE_GLUE",
        "FC10_STRATIFIED_PROJECTOR", "FC11_NONINTEGRABLE_DISTRIBUTION",
        "FC12_RECIPROCAL_TORIC_DIAGONAL",
    }
    if set(completions) != expected_completions:
        errors.append("completion_universe")
    if len(readouts) != 17 or set(readouts) != {f"R{i:02d}" for i in range(1, 18)}:
        errors.append("readout_universe")
    if len(gates) != 10 or set(gates) != {f"M{i:02d}" for i in range(1, 11)}:
        errors.append("gate_universe")
    if len(relations_u) != 10 or set(relations_u) != {f"Q{i:02d}" for i in range(1, 11)}:
        errors.append("relation_universe")
    expected_pairs = {(fc, rid) for fc in completions for rid in readouts}
    if len(matrix_list) != 204 or len(matrix) != 204 or set(matrix) != expected_pairs:
        errors.append("matrix_coverage")
        return errors
    if set(schema) != set(completions):
        errors.append("schema_coverage")
    for fc, row in schema.items():
        component_total = sum(int(row[name]) for name in (
            "local_formula_schema_entries", "conditional_or_parametric_schema_entries",
            "discrete_classification_schema_entries", "unavailable_schema_entries", "unselected_family_entries",
        ))
        subset_counts = Counter(item["availability"] for item in matrix_list if item["completion_id"] == fc)
        independently_counted = {
            "local_formula_schema_entries": sum(v for k, v in subset_counts.items() if "LOCAL" in k),
            "conditional_or_parametric_schema_entries": sum(v for k, v in subset_counts.items() if "CONDITIONAL" in k or "PARAMETRIC" in k),
            "discrete_classification_schema_entries": sum(v for k, v in subset_counts.items() if k.startswith("DISCRETE_")),
            "unavailable_schema_entries": subset_counts["UNAVAILABLE_ON_CLASS"] + subset_counts["OPEN_TYPE_ONLY"],
            "unselected_family_entries": subset_counts["UNSELECTED_FAMILY"],
        }
        if int(row["total_readout_entries"]) != 17 or component_total != 17 or any(
                int(row[name]) != value for name, value in independently_counted.items()):
            errors.append(f"schema_partition:{fc}")
    nodes = set(graph.get("nodes", []))
    edge_pairs = {(edge.get("from"), edge.get("to")) for edge in graph.get("edges", [])}
    required_edge_pairs = {
        ("complete_metric_or_coframe_profile", "R04"),
        ("complete_metric_or_coframe_profile", "R13"),
        ("boundary_cap_glue_and_moduli", "R06"),
        ("boundary_cap_glue_and_moduli", "R07"),
        ("boundary_cap_glue_and_moduli", "R08"),
        ("boundary_cap_glue_and_moduli", "R17"),
        ("integral_torus_bundle_and_lattice", "R09"),
        ("integral_torus_bundle_and_lattice", "R10"),
        ("integral_torus_bundle_and_lattice", "R11"),
        ("integral_torus_bundle_and_lattice", "R12"),
        ("torus_connection_S", "R09"),
        ("torus_connection_S", "R10"),
        ("normalized_angular_metric_H", "R12"),
        ("cap_cycles_or_GL2Z_glue", "R17"),
        ("complete_R_geom_A_of_X_O_target_normalization_and_pairing", "physical_bootstrap_closure"),
    }
    if (any(edge.get("from") not in nodes or edge.get("to") not in nodes for edge in graph.get("edges", []))
            or not required_edge_pairs <= edge_pairs):
        errors.append("dependency_graph_undeclared_endpoint")
    if any(row["M02"] != "ABSENT_NO_COMPLETE_METRIC_WITNESS" for row in matrix_list):
        errors.append("complete_witness_invented")
    if any(row["M10"] != "PASS_NO_PHYSICAL_CLOSURE_PROMOTION" for row in matrix_list):
        errors.append("authority_promotion")
    if any(row["M08"] == "COMPLETE_R_GEOM" for row in matrix_list):
        errors.append("complete_R_geom_invented")
    if any(matrix[(fc, "R01")]["M05"] != "LOCAL_ONLY_NOT_GLOBAL" for fc in completions):
        errors.append("local_called_global")

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
    # Exact source-table inheritance for four load-bearing readouts, plus an
    # independently typed open-path Levi-Civita ruling.
    for fc in completions:
        if fc not in bundle or fc not in transport or fc not in registry:
            errors.append("source_completion_coverage")
            break
        if matrix[(fc, "R07")]["completion_specific_ruling"] != bundle[fc]["levi_civita_tangent_holonomy"]:
            errors.append("LC_holonomy_source_mismatch")
        if matrix[(fc, "R08")]["completion_specific_ruling"] != bundle[fc]["projector_kato_transport"]:
            errors.append("Kato_source_mismatch")
        expected_r11 = ("NOT_APPLICABLE_NO_GLOBAL_INTEGRAL_LATTICE__SOURCE_REGISTERED_NONE_OR_OPEN"
                        if fc == "FC11_NONINTEGRABLE_DISTRIBUTION" else bundle[fc]["torus_lattice_or_cap_data"])
        if matrix[(fc, "R11")]["completion_specific_ruling"] != expected_r11:
            errors.append("lattice_source_mismatch")
        if matrix[(fc, "R12")]["completion_specific_ruling"] != transport[fc]["global_outcome"]:
            errors.append("systole_source_mismatch")
        if matrix[(fc, "R16")]["completion_specific_ruling"] != registry[fc]["topology_family"]:
            errors.append("topology_source_mismatch")
        if matrix[(fc, "R06")]["completion_specific_ruling"] != lc_path_ruling[fc]:
            errors.append("LC_path_source_mismatch")
        if matrix[(fc, "R10")]["completion_specific_ruling"] != t2_holonomy_ruling[fc]:
            errors.append("T2_holonomy_source_mismatch")
        if matrix[(fc, "R06")]["completion_specific_ruling"] == matrix[(fc, "R07")]["completion_specific_ruling"]:
            errors.append("path_called_holonomy")
        if matrix[(fc, "R10")]["completion_specific_ruling"] == matrix[(fc, "R11")]["completion_specific_ruling"]:
            errors.append("holonomy_monodromy_conflated")

    fc11 = "FC11_NONINTEGRABLE_DISTRIBUTION"
    if any(matrix[(fc11, rid)]["availability"] != "UNAVAILABLE_ON_CLASS" for rid in ("R09", "R10", "R11", "R12")):
        errors.append("FC11_toric_promotion")
    if any(matrix[(fc11, rid)][gate] != "NOT_APPLICABLE"
           for rid in ("R11", "R12") for gate in ("M07", "M09")):
        errors.append("FC11_unavailable_positive_gate")
    if any(matrix[(fc11, rid)]["M06"] != "NOT_APPLICABLE" for rid in ("R09", "R10", "R11", "R12")):
        errors.append("FC11_unavailable_scale_gate")
    if matrix[(fc11, "R11")]["M05"] != "NOT_APPLICABLE_NO_GLOBAL_INTEGRAL_LATTICE":
        errors.append("FC11_unavailable_descent_gate")
    if matrix[("FC10_STRATIFIED_PROJECTOR", "R11")]["availability"] != "CONDITIONAL_STRATIFIED_DISCRETE_SCHEMA":
        errors.append("FC10_discrete_schema_promoted")
    if any(matrix[(fc, "R11")]["availability"] != "DISCRETE_FAMILY_SCHEMA_ONLY"
           for fc in completions if fc not in {fc11, "FC10_STRATIFIED_PROJECTOR"}):
        errors.append("R11_schema_promoted_to_realized")
    if any(matrix[(fc, "R16")]["availability"] != "DISCRETE_CLASSIFICATION_AVAILABLE" for fc in completions):
        errors.append("R16_registered_label_lost")
    if matrix[("FC10_STRATIFIED_PROJECTOR", "R08")]["M04"] == "REGULAR_ALL_STRATA":
        errors.append("rank_stratum_smoothed")
    if matrix[("FC10_STRATIFIED_PROJECTOR", "R12")]["M07"] == "EVERYWHERE_SMOOTH":
        errors.append("systole_stratum_smoothed")
    if "null" not in matrix[("FC01_BOUNDARY_BOUNDARY", "R04")]["M03"].lower() and matrix[("FC01_BOUNDARY_BOUNDARY", "R04")]["M07"] == "COMPLETE":
        errors.append("null_boundary_promoted")
    if matrix[("FC01_BOUNDARY_BOUNDARY", "R14")]["availability"] == "UNIVERSAL_Dg":
        errors.append("temporal_phi_universalized")
    r15 = matrix[("FC01_BOUNDARY_BOUNDARY", "R15")]
    if "supremum" not in r15["completion_specific_ruling"] and "SUPREMUM" not in r15["completion_specific_ruling"]:
        errors.append("Xmax_called_maximum")
    if matrix[("FC04_TWO_CAP_P1", "R16")]["M07"] not in {"DISCRETE_LOCALLY_CONSTANT__NO_OFFSHELL_COVECTOR"}:
        errors.append("topology_covector")
    if matrix[("FC04_TWO_CAP_P1", "R17")]["availability"] == "NATIVE_UNCONDITIONAL":
        errors.append("Hopf_carrier_promoted")
    if matrix[("FC01_BOUNDARY_BOUNDARY", "R02")]["M07"] == "COMPLETE":
        errors.append("moving_boundary_omitted")
    if matrix[("FC12_RECIPROCAL_TORIC_DIAGONAL", "R12")]["M06"] == "PHYSICAL_SCALE_SELECTED":
        errors.append("common_scale_promoted")
    if len(relation) != 10 or set(relation) != set(relations_u):
        errors.append("relation_coverage")
    allowed_relation_classes = {
        "GEOMETRIC_IDENTITY", "COMPLETION_COMPATIBILITY", "DISCRETE_CLASSIFICATION_RULE",
        "CONDITIONAL_ON_COMPLETE_BRANCH", "SOURCE_GAP", "NOT_DERIVED", "PHYSICAL_CLOSURE_RELATION",
    }
    if {item["classification"] for item in relation.values()} - allowed_relation_classes:
        errors.append("relation_unregistered_class")
    if any(item["physical_closure"] != "NO" for item in relation.values()):
        errors.append("identity_called_closure")
    if relation["Q09"]["classification"] != "SOURCE_GAP":
        errors.append("source_gap_filled")
    if relation["Q10"]["classification"] != "NOT_DERIVED":
        errors.append("bootstrap_operator_invented")
    result = state["result"]
    if result.get("complete_metric_witness_count") != 0 or result.get("complete_R_geom_count") != 0:
        errors.append("result_complete_map_promotion")
    if result.get("physical_closure_relation_count") != 0:
        errors.append("result_closure_promotion")
    if result.get("density_status") != "NOT_USED__FUTURE_COMPARISON_BRACKET_DEFERRED":
        errors.append("forbidden_downstream_work")
    if state.get("unrelated_changed", False):
        errors.append("unrelated_path_changed")
    if not state.get("source_integrity", True):
        errors.append("source_identity_drift")
    selector_ids = {row["selector_id"] for row in selectors}
    selector_pairs = {(row["selector_id"], row["completion_id"]) for row in selectors}
    if len(selectors) != 84 or len(selector_ids) != 7 or selector_pairs != {
            (selector, fc) for selector in selector_ids for fc in completions}:
        errors.append("selector_coverage")
    return errors


def verify_frozen_file(commit: str, name: str) -> bool:
    git_path = f"{HERE.name}/{name}"
    frozen = subprocess.run(["git", "show", f"{commit}:{git_path}"], cwd=ROOT, check=True, capture_output=True).stdout
    return frozen == (HERE / name).read_bytes()


def main() -> None:
    checks: dict[str, str] = {}
    prereg_files = (
        "COMPLETION_UNIVERSE.tsv", "FALSIFICATION_CONTRACT.tsv", "MAP_GATE_UNIVERSE.tsv",
        "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "READOUT_UNIVERSE.tsv",
        "RELATION_UNIVERSE.tsv", "SOURCE_MANIFEST.tsv", "SOURCE_SCOPE.tsv", "build_source_manifest.py",
    )
    require("I01_preregistration_unchanged", all(verify_frozen_file(PREREG, name) for name in prereg_files), checks)
    require("I02_source_amendment_unchanged",
            all(verify_frozen_file(AMENDMENT, name) for name in ("PREREGISTRATION_SOURCE_AMENDMENT_01.md", "SOURCE_MANIFEST_AMENDMENT_01.tsv")), checks)
    require("I02b_source_correction_unchanged",
            all(verify_frozen_file(CORRECTION, name) for name in ("SOURCE_MANIFEST_CORRECTION_01.md", "SOURCE_MANIFEST_CORRECTION_01.tsv")), checks)

    source_rows = rows(HERE / "SOURCE_MANIFEST.tsv") + rows(HERE / "SOURCE_MANIFEST_AMENDMENT_01.tsv")
    correction_rows = rows(HERE / "SOURCE_MANIFEST_CORRECTION_01.tsv")
    corrections = {(row["source_id"], row["field"]): row["corrected_value"] for row in correction_rows}
    source_ok = len(source_rows) == 21 and len({row["source_id"] for row in source_rows}) == 21
    source_ok &= len(correction_rows) == 1 and set(corrections) == {("S17", "sha256")}
    for item in source_rows:
        path = ROOT / item["path"]
        frozen = subprocess.run(["git", "show", f"{BASE}:{item['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        expected_sha = corrections.get((item["source_id"], "sha256"), item["sha256"])
        source_ok &= path.is_file() and str(path.stat().st_size) == item["size_bytes"]
        source_ok &= digest(path.read_bytes()) == expected_sha == digest(frozen)
    require("I03_source_identities_21", source_ok, checks)

    # Independent determinant reconstruction.
    cap_rows = rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "CAP_PAIR_WITNESSES.tsv")
    cap_counts: Counter[str] = Counter()
    cap_ok = True
    for row in cap_rows:
        vm, vp = ast.literal_eval(row["v_minus"]), ast.literal_eval(row["v_plus"])
        det = vm[0] * vp[1] - vm[1] * vp[0]
        cap_ok &= det == int(row["signed_determinant"])
        cap_counts["P0" if abs(det) == 0 else "P1" if abs(det) == 1 else "P_GT1"] += 1
    require("I04_cap_determinants_and_counts",
            cap_ok and cap_counts == Counter({"P_GT1": 182, "P1": 58, "P0": 16}), checks)
    monodromy = rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "TORUS_MONODROMY_REGISTRY.tsv")
    mono_ok = True
    for row in monodromy:
        m = ast.literal_eval(row["matrix"])
        mono_ok &= m[0][0] * m[1][1] - m[0][1] * m[1][0] == int(row["determinant"])
    require("I05_monodromy_determinants", mono_ok and len(monodromy) == 8, checks)

    bundle_all = rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "BUNDLE_HOLONOMY_ATLAS.tsv")
    state: dict[str, object] = {
        "completions": rows(HERE / "COMPLETION_UNIVERSE.tsv"),
        "readouts": rows(HERE / "READOUT_UNIVERSE.tsv"),
        "gates": rows(HERE / "MAP_GATE_UNIVERSE.tsv"),
        "relations_u": rows(HERE / "RELATION_UNIVERSE.tsv"),
        "matrix": rows(HERE / "COMPLETION_READOUT_MATRIX.tsv"),
        "relation": rows(HERE / "RELATION_MATRIX.tsv"),
        "schema": rows(HERE / "R_GEOM_SCHEMA.tsv"),
        "bundle": [row for row in bundle_all if "::" not in row["completion_id"]],
        "transport": rows(ROOT / "udt_dual_systole_global_transport_audit_2026-07-24" / "GLOBAL_TRANSPORT_ATLAS.tsv"),
        "registry": rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "COMPLETION_CLASS_REGISTRY.tsv"),
        "graph": json.loads((HERE / "DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
        "selectors": rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22" / "SELECTOR_MATRIX.tsv"),
        "result": json.loads((HERE / "RESULT.json").read_text(encoding="utf-8")),
        "unrelated_changed": False,
        "source_integrity": True,
    }
    require("I06_complete_state_valid", validate(state) == [], checks)

    def matrix_row(s: dict[str, object], fc: str, rid: str) -> dict[str, str]:
        return next(row for row in s["matrix"] if row["completion_id"] == fc and row["readout_id"] == rid)

    mutations = [
        ("F01_missing_readout", lambda s: s["readouts"].pop()),
        ("F02_complete_witness", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R01").update(M02="PASS")),
        ("F03_local_called_global", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R01").update(M05="GLOBAL_INVARIANT")),
        ("F04_path_called_holonomy", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R06").update(completion_specific_ruling=s["bundle"][0]["levi_civita_tangent_holonomy"])),
        ("F05_holonomy_monodromy_conflated", lambda s: matrix_row(s, "FC07_PERIODIC_TORUS_BUNDLE", "R10").update(completion_specific_ruling=s["bundle"][6]["torus_lattice_or_cap_data"])),
        ("F06_FC11_toric", lambda s: matrix_row(s, "FC11_NONINTEGRABLE_DISTRIBUTION", "R12").update(availability="CONDITIONAL_STRATIFIED_MAP")),
        ("F07_stratum_smoothed", lambda s: matrix_row(s, "FC10_STRATIFIED_PROJECTOR", "R08").update(M04="REGULAR_ALL_STRATA")),
        ("F08_null_boundary_complete", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R04").update(M03="BOUNDARY", M07="COMPLETE")),
        ("F09_temporal_phi_universal", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R14").update(availability="UNIVERSAL_Dg")),
        ("F10_Xmax_maximum", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R15").update(completion_specific_ruling="ATTAINED_MAXIMUM")),
        ("F11_topology_covector", lambda s: matrix_row(s, "FC04_TWO_CAP_P1", "R16").update(M07="SMOOTH_COVECTOR")),
        ("F12_Hopf_native", lambda s: matrix_row(s, "FC04_TWO_CAP_P1", "R17").update(availability="NATIVE_UNCONDITIONAL")),
        ("F13_fixed_domain_complete", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R02").update(M07="COMPLETE")),
        ("F14_scale_selected", lambda s: matrix_row(s, "FC12_RECIPROCAL_TORIC_DIAGONAL", "R12").update(M06="PHYSICAL_SCALE_SELECTED")),
        ("F15_identity_closure", lambda s: next(row for row in s["relation"] if row["relation_id"] == "Q01").update(physical_closure="YES")),
        ("F16_partial_map_complete", lambda s: matrix_row(s, "FC01_BOUNDARY_BOUNDARY", "R02").update(M08="COMPLETE_R_GEOM")),
        ("F17_bootstrap_operator", lambda s: next(row for row in s["relation"] if row["relation_id"] == "Q10").update(classification="PHYSICAL_CLOSURE_RELATION")),
        ("F18_source_gap_filled", lambda s: next(row for row in s["relation"] if row["relation_id"] == "Q09").update(classification="GEOMETRIC_IDENTITY")),
        ("F19_density_used", lambda s: s["result"].update(density_status="USED")),
        ("F20_gpu_launched", lambda s: s["result"].update(density_status="GPU_RUN")),
        ("F21_source_drift", lambda s: s.update(source_integrity=False)),
        ("F22_unrelated_path", lambda s: s.update(unrelated_changed=True)),
    ]
    catch_rows = []
    for ident, mutate in mutations:
        trial = deepcopy(state)
        mutate(trial)
        detected = validate(trial)
        require(f"I07_{ident}", bool(detected), checks)
        catch_rows.append({"catch_id": ident, "result": "PASS_REJECTED", "detected_by": ";".join(detected)})
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "result", "detected_by"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)

    production = state["result"]
    require("I08_production_29_checks", production["check_count"] == 29 and set(production["checks"].values()) == {"PASS"}, checks)
    require("I09_production_conclusion",
            production["maximum_supported_conclusion"] == "COMPLETION_SCOPED_REDUNDANT_READOUT_SCHEMA_DERIVED__NO_REALIZED_COMPLETE_R_GEOM_OR_NONIDENTITY_PHYSICAL_CLOSURE", checks)
    result = {
        "schema": "udt-completion-scoped-realized-observable-independent-1.0",
        "method": "stdlib_source_table_reconstruction_no_production_import",
        "result": "PASS",
        "check_count": len(checks),
        "catch_count": len(catch_rows),
        "checks": checks,
        "maximum_supported_conclusion": production["maximum_supported_conclusion"],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
