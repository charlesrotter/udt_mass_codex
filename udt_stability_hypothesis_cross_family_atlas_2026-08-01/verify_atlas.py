#!/usr/bin/env python3
"""Fail-closed verifier for the cross-family stability atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


EXPECTED_GRADES = {
    "F01": "CONDITIONAL_PRUNING_EVIDENCE",
    "F02": "CONDITIONAL_SECTOR_PRUNING_EVIDENCE",
    "F03": "CONTROL_NOT_SURVIVOR_EVIDENCE",
    "F04": "SETTLED_WITHIN_CONDITIONAL_PREMISES",
    "F05": "STRUCTURAL_EVIDENCE_ONLY",
    "F06": "EXACT_SCOPED_EMPTY_CONTROL",
    "F07": "FORMAL_COMPATIBILITY_NOT_STABILITY",
}

EXPECTED_LINEAGE = {
    "H01": "BANKED_MATH_PLUS_PONDER_INTERPRETATION",
    "H02": "SUPPORTED_CONDITIONALLY_NOT_DERIVED_UNIVERSALLY",
    "H03": "WORKING_MULTI_FAMILY_ARCHITECTURE_NOT_PARTICLE_THEOREM",
    "H04": "DERIVED_CONDITIONAL_REDUCED_CORE",
    "H05": "DERIVED_CONDITIONAL_SECTOR_DICHOTOMY",
    "H06": "BANKED_IDENTITIES_PONDER_CLOSURE_ANALOGY",
    "H07": "SETTLED_WITHIN_CONDITIONAL_PREMISES",
    "H08": "WORKING_DISTINCT_POSIT_NO_SELECTION_RULE",
}

EXPECTED_RESULT = {
    "Hopfion_removal_preserves_hypothesis_but_reduces_current_support_to_P4": True,
    "Hopfion_required_for_P4_algebra": False,
    "Hopfion_required_for_original_hypothesis_formulation": False,
    "P4_required_for_original_July31_algebraic_spine": True,
    "P4_threshold_is_continuous_region": True,
    "bootstrap_law_adopted": False,
    "bootstrap_selected_families": 0,
    "dependency_edges": 14,
    "discrete_species_catalog_derived": False,
    "families": 7,
    "family_overlap_after_correction": 0,
    "family_partition_rows": 7,
    "gpu_used": False,
    "grammar_cells": 70,
    "grammar_components": 10,
    "hypothesis_claims": 8,
    "isolated_multi_basin_spectrum_observed": False,
    "new_stability_solve_run": False,
    "non_hopf_load_bearing_stability_families": 2,
    "object_inequivalent_stability_support_streams": 2,
    "outcome": "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED",
    "premises": 18,
    "post_prereg_partition_correction": True,
    "post_prereg_source_admission_correction": True,
    "shared_metric_native_stability_operator_found": False,
    "source_anchors": 18,
    "source_paths_verified": 1469,
    "time_live_persistence_derived_families": 0,
}

CORRECTION_02_PATHS = {
    "PONDER_MATH_ELEGANCE_2026-07-31.md",
    "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md",
    "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv",
}


def sources_ok(rows: list[dict[str, str]]) -> bool:
    paths = [row.get("path", "") for row in rows]
    layer_counts = {
        name: sum(row.get("layer") == name for row in rows)
        for name in {
            "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE",
            "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE",
            "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02",
        }
    }
    additions = {
        row.get("path", "")
        for row in rows
        if row.get("layer") == "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    }
    return (
        len(rows) == 1469
        and paths == sorted(paths)
        and len(paths) == len(set(paths))
        and layer_counts
        == {
            "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE": 1424,
            "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE": 42,
            "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02": 3,
        }
        and additions == CORRECTION_02_PATHS
    )


def atlas_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("family_id") for row in rows]
    if ids != [f"F{i:02d}" for i in range(1, 8)] or len(ids) != len(set(ids)):
        return False
    by_id = {row["family_id"]: row for row in rows}
    if any(by_id[key].get("overall_grade") != grade for key, grade in EXPECTED_GRADES.items()):
        return False
    return (
        by_id["F01"].get("hopfion_dependency") == "NO_RESULT_TRANSFER_METHOD_SHAPE_ONLY"
        and by_id["F01"].get("carrier") == "NONE_SELECTED"
        and "empty" not in by_id["F01"].get("existence", "").lower()
        and by_id["F02"].get("hopfion_dependency") == "NONE"
        and "stable iff 64 E0^2 ell^4 <= g_p c_m pi^4" in by_id["F02"].get("stability_outcome", "")
        and "not isolated stable basins" in by_id["F03"].get("stability_outcome", "")
        and by_id["F04"].get("carrier") == "ROUND_S2_POSIT"
        and by_id["F04"].get("time_persistence") == "OPEN"
        and by_id["F05"].get("stability_test") == "NONE"
        and by_id["F06"].get("stability_test") == "NOT_APPLICABLE_EMPTY_DOMAIN"
        and by_id["F07"].get("stability_outcome") == "BLOCKED_BY_REALIZATION_JOIN"
    )


def lineage_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("claim_id") for row in rows]
    if ids != [f"H{i:02d}" for i in range(1, 9)] or len(ids) != len(set(ids)):
        return False
    by_id = {row["claim_id"]: row for row in rows}
    return all(by_id[key].get("status") == status for key, status in EXPECTED_LINEAGE.items()) and (
        by_id["H03"].get("hopfion_requirement") == "NO_FOR_FORMULATION__ITS_REMOVAL_REDUCES_CURRENT_SUPPORT_TO_P4"
        and "full certificate remains open" in by_id["H04"].get("ruling", "")
        and "not physical time stability" in by_id["H05"].get("ruling", "")
        and "not a selector" in by_id["H06"].get("ruling", "")
        and "no operational membership relation" in by_id["H08"].get("ruling", "")
    )


def partitions_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("family_id") for row in rows]
    keys = [row.get("effective_partition_key") for row in rows]
    return (
        ids == [f"F{i:02d}" for i in range(1, 8)]
        and len(keys) == len(set(keys)) == 7
        and "NONEMPTY_OR_CONDITIONAL" in keys[0]
        and "N1_CYCLIC_OR_DOUBLE_CREASE|EMPTY" in keys[5]
        and "-> F06" in rows[0].get("explicit_exclusion", "")
        and "-> F06" in rows[4].get("explicit_exclusion", "")
    )


def grammar_ok(rows: list[dict[str, str]]) -> bool:
    keys = [(row.get("family_id"), row.get("component_id")) for row in rows]
    expected = [(f"F{i:02d}", f"G{j:02d}") for i in range(1, 8) for j in range(1, 11)]
    if len(rows) != 70 or keys != expected or len(keys) != len(set(keys)):
        return False
    keyed = {(row["family_id"], row["component_id"]): row["status"] for row in rows}
    return (
        keyed[("F01", "G08")] == "OPEN_FULL_CERTIFICATE"
        and keyed[("F02", "G08")] == "PRESENT_SECTOR_ONLY"
        and keyed[("F03", "G08")] == "ABSENT_PSD_DEGENERATE"
        and keyed[("F04", "G08")] == "PRESENT_STATIC_FINITE_BOX_CONDITIONAL"
        and keyed[("F05", "G08")] == "NOT_TESTED"
        and keyed[("F06", "G08")] == "NOT_APPLICABLE"
        and keyed[("F07", "G08")] == "BLOCKED"
        and all(keyed[(f"F{i:02d}", "G10")] == "ABSENT" for i in range(1, 8))
        and all(keyed[(f"F{i:02d}", "G09")] in {"OPEN", "NOT_APPLICABLE"} for i in range(1, 8))
    )


def result_ok(data: dict) -> bool:
    return data == EXPECTED_RESULT


def deletion_ok(data: dict) -> bool:
    return data == {
        "all_evidence": {
            "object_inequivalent_stability_support_streams": 2,
            "original_P4_spine_components": 2,
        },
        "remove_Hopfion_F04_H07": {
            "P4_algebra_survives": True,
            "object_inequivalent_stability_support_streams": 1,
            "original_P4_spine_components": 2,
            "original_hypothesis_formulation_survives": True,
        },
        "remove_P4_F01_F02_H04_H05": {
            "conditional_Hopfion_exemplar_survives": True,
            "object_inequivalent_stability_support_streams": 1,
            "original_July31_algebraic_spine_survives": False,
            "original_P4_spine_components": 0,
        },
        "scope": "finite dependency deletion control; not counterfactual physics",
    }


def main() -> None:
    checks: list[tuple[str, bool]] = []
    inventory = tsv("SOURCE_INVENTORY.tsv")
    paths = [row["path"] for row in inventory]
    checks.append(("sources_1469_layers_exact", sources_ok(inventory)))
    checks.append(("sources_unique_sorted", paths == sorted(paths) and len(paths) == len(set(paths))))
    checks.append(("source_bytes_match", all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in inventory)))
    checks.append(("families_preregistered_7", len(tsv("FAMILY_UNIVERSE.tsv")) == 7))
    checks.append(("claims_preregistered_8", len(tsv("HYPOTHESIS_CLAIM_UNIVERSE.tsv")) == 8))
    checks.append(("premises_preregistered_18", len(tsv("PREMISE_LEDGER.tsv")) == 18))

    anchors = tsv("SOURCE_AUTHORITY_LEDGER.tsv")
    checks.append(("anchors_18", len(anchors) == 18 and len({row["anchor_id"] for row in anchors}) == 18))
    checks.append(("anchor_bytes", all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in anchors)))
    inventory_by_path = {row["path"]: row for row in inventory}
    checks.append(("anchors_admitted_to_source_freeze", all(
        row["path"] in inventory_by_path and inventory_by_path[row["path"]]["sha256"] == row["sha256"]
        for row in anchors
    )))
    checks.append(("source_git_blobs", all(
        subprocess.check_output(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True).strip()
        == row["git_blob"]
        for row in inventory
    )))
    source_text = {row["anchor_id"]: (ROOT / row["path"]).read_text(encoding="utf-8") for row in anchors}
    checks.append(("ponder_grade", "STATUS: PURE PONDER" in source_text["A01"] and "particle spectra =" in source_text["A01"]))
    checks.append(("p4_no_hopf_transfer", "no hopfion RESULT transferred" in source_text["A02"]))
    checks.append(("p4_threshold_source", "64 E0^2 l^4 <= g_p c_m" in source_text["A02"]))
    checks.append(("p4_cold_scope", "sector stability, not full dynamics" in source_text["A05"]))
    checks.append(("ring_scope", "all-definite ring is ENTIRELY massless" in source_text["A07"]))
    checks.append(("hopf_scope", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL" in source_text["A09"] and "Global/time-live persistence" in source_text["A09"]))
    checks.append(("foundations_separate", "P4/Hopfion" in source_text["A12"] or "P4\nsecond-variation" in source_text["A12"]))
    checks.append(("bootstrap_ceiling", "BOOTSTRAP_IS_DISTINCT_POSIT" in source_text["A16"] and "not a proof of deductive independence" in source_text["A16"]))

    generated = ["SOURCE_AUTHORITY_LEDGER.tsv", "FAMILY_ATLAS.tsv", "FAMILY_PARTITION_LEDGER.tsv", "LINEAGE_LEDGER.tsv", "COMMON_GRAMMAR_MATRIX.tsv", "DEPENDENCY_GRAPH.tsv", "DELETION_CONTROL.json", "STATUS_LEDGER.tsv", "RESULT.json"]
    before = {name: sha256(PKG / name) for name in generated}
    proc = subprocess.run([sys.executable, str(PKG / "derive_atlas.py")], cwd=ROOT, text=True, capture_output=True, timeout=60, check=False)
    after = {name: sha256(PKG / name) for name in generated}
    checks.append(("derive_exit_0", proc.returncode == 0))
    checks.append(("deterministic_replay", before == after))

    atlas = tsv("FAMILY_ATLAS.tsv")
    partitions = tsv("FAMILY_PARTITION_LEDGER.tsv")
    lineage = tsv("LINEAGE_LEDGER.tsv")
    grammar = tsv("COMMON_GRAMMAR_MATRIX.tsv")
    dependencies = tsv("DEPENDENCY_GRAPH.tsv")
    deletion = json.loads((PKG / "DELETION_CONTROL.json").read_text(encoding="utf-8"))
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    checks.append(("atlas_exact", atlas_ok(atlas)))
    checks.append(("partitions_exact_no_overlap", partitions_ok(partitions)))
    checks.append(("lineage_exact", lineage_ok(lineage)))
    checks.append(("grammar_exact", grammar_ok(grammar)))
    checks.append(("dependencies_14", len(dependencies) == 14 and [row["edge_id"] for row in dependencies] == [f"D{i:02d}" for i in range(1, 15)]))
    checks.append(("deletion_control_exact", deletion_ok(deletion)))
    checks.append(("result_exact", result_ok(result)))
    status = tsv("STATUS_LEDGER.tsv")
    checks.append(("status_overall", status[-1]["status"] == "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED"))
    checks.append(("no_species_catalog", next(row for row in status if row["claim"] == "discrete_species_catalog")["status"] == "NOT_DERIVED_OR_OBSERVED"))

    catches: list[tuple[str, bool]] = []
    catches.append(("missing_correction02_source", not sources_ok([
        row for row in inventory if row["path"] != "PONDER_MATH_ELEGANCE_2026-07-31.md"
    ])))
    extra_source = copy.deepcopy(inventory[0])
    extra_source["path"] = "EXTRA_NOT_PREREGISTERED.md"
    extra_source["layer"] = "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    catches.append(("extra_correction02_source", not sources_ok(sorted(inventory + [extra_source], key=lambda row: row["path"]))))
    wrong_layer = copy.deepcopy(inventory)
    next(row for row in wrong_layer if row["path"] == "PONDER_MATH_ELEGANCE_2026-07-31.md")["layer"] = "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE"
    catches.append(("hidden_source_admission_correction", not sources_ok(wrong_layer)))
    catches.append(("missing_family", not atlas_ok(atlas[:-1])))
    catches.append(("duplicate_family", not atlas_ok(atlas + [copy.deepcopy(atlas[0])])))
    mutated_partitions = copy.deepcopy(partitions)
    mutated_partitions[5]["effective_partition_key"] = mutated_partitions[0]["effective_partition_key"]
    catches.append(("duplicate_partition", not partitions_ok(mutated_partitions)))
    mutated_partitions = copy.deepcopy(partitions)
    mutated_partitions[0]["explicit_exclusion"] = "none"
    catches.append(("F01_F06_overlap", not partitions_ok(mutated_partitions)))
    atlas_mutations = [
        ("F01", "hopfion_dependency", "RESULT_TRANSFERRED", "Hopf_result_transfer"),
        ("F01", "overall_grade", "FULL_STABILITY_CERTIFIED", "P4_full_certificate"),
        ("F01", "existence", "double-crease and cyclic single-cell massive branches empty", "F01_F06_branch_overlap"),
        ("F02", "stability_outcome", "FULL_TIME_DYNAMICS_STABLE", "sector_to_time"),
        ("F03", "stability_outcome", "ISOLATED_STABLE_BASIN", "control_to_survivor"),
        ("F04", "carrier", "NATIVE_DERIVED_S2", "carrier_promotion"),
        ("F04", "time_persistence", "DERIVED", "Hopf_time_promotion"),
        ("F05", "stability_test", "FULL_STABILITY", "ring_stability_smuggle"),
        ("F06", "stability_test", "UNSTABLE", "empty_to_instability"),
        ("F07", "stability_outcome", "JOINT_REALIZED_STABLE", "formal_to_realized"),
    ]
    for family_id, field, value, name in atlas_mutations:
        mutated = copy.deepcopy(atlas)
        next(row for row in mutated if row["family_id"] == family_id)[field] = value
        catches.append((name, not atlas_ok(mutated)))
    lineage_mutations = [
        ("H03", "status", "DERIVED_PARTICLE_THEOREM", "taxonomy_promotion"),
        ("H04", "ruling", "full certificate closed", "parity_scope_drop"),
        ("H05", "ruling", "physical time stability", "threshold_scope_drop"),
        ("H06", "ruling", "derived selector", "sum_rule_selector"),
        ("H07", "status", "NATIVE_HOPFION_DERIVED", "Hopf_native_promotion"),
        ("H08", "status", "BOOTSTRAP_SELECTION_DERIVED", "bootstrap_promotion"),
    ]
    for claim_id, field, value, name in lineage_mutations:
        mutated = copy.deepcopy(lineage)
        next(row for row in mutated if row["claim_id"] == claim_id)[field] = value
        catches.append((name, not lineage_ok(mutated)))
    grammar_mutations = [
        ("F04", "G09", "PRESENT_DERIVED", "Hopf_time_grammar"),
        ("F05", "G08", "PRESENT", "ring_basin_grammar"),
        ("F06", "G08", "PRESENT", "empty_basin_grammar"),
        ("F01", "G10", "PRESENT", "bootstrap_selection_grammar"),
    ]
    for family_id, component_id, value, name in grammar_mutations:
        mutated = copy.deepcopy(grammar)
        next(row for row in mutated if row["family_id"] == family_id and row["component_id"] == component_id)["status"] = value
        catches.append((name, not grammar_ok(mutated)))
    deletion_mutations = [
        ("remove_Hopfion_F04_H07", "original_hypothesis_formulation_survives", False, "Hopf_deletion_kills_formulation"),
        ("remove_Hopfion_F04_H07", "original_P4_spine_components", 0, "Hopf_deletion_erases_P4"),
        ("remove_P4_F01_F02_H04_H05", "original_July31_algebraic_spine_survives", True, "P4_deletion_preserves_spine"),
    ]
    for section, field, value, name in deletion_mutations:
        mutated = copy.deepcopy(deletion)
        mutated[section][field] = value
        catches.append((name, not deletion_ok(mutated)))
    result_mutations = [
        ("Hopfion_required_for_original_hypothesis_formulation", True, "false_Hopf_dependency"),
        ("Hopfion_required_for_P4_algebra", True, "false_P4_transfer"),
        ("P4_required_for_original_July31_algebraic_spine", False, "erase_P4_spine"),
        ("P4_threshold_is_continuous_region", False, "threshold_discretized"),
        ("discrete_species_catalog_derived", True, "species_catalog_promotion"),
        ("isolated_multi_basin_spectrum_observed", True, "basin_spectrum_promotion"),
        ("family_overlap_after_correction", 1, "family_overlap_retained"),
        ("post_prereg_partition_correction", False, "correction_hidden"),
        ("shared_metric_native_stability_operator_found", True, "shared_operator_smuggle"),
        ("time_live_persistence_derived_families", 1, "time_promotion"),
        ("bootstrap_selected_families", 1, "bootstrap_selection"),
        ("bootstrap_law_adopted", True, "bootstrap_adoption"),
        ("new_stability_solve_run", True, "solve_smuggle"),
        ("gpu_used", True, "gpu_smuggle"),
        ("outcome", "HYPOTHESIS_HOPFION_DEPENDENT", "wrong_outcome"),
    ]
    for field, value, name in result_mutations:
        mutated = copy.deepcopy(result)
        mutated[field] = value
        catches.append((name, not result_ok(mutated)))
    checks.extend((f"catch_{name}", passed) for name, passed in catches)

    for name in ["AUDIT_REPORT.md", "EXACT_DERIVATION.md", "LAY_REPORT.md", "COMPLETENESS_MAP.md"]:
        checks.append((f"present_{name}", (PKG / name).is_file()))
    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks.append(("report_outcome", "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED" in report))
    checks.append(("report_no_operator", "No common metric-native stability operator" in report))
    checks.append(("report_Hopf_removal", "Remove Hopfion evidence" in report and "present support becomes P4-only" in report))
    checks.append(("report_P4_spine", "original algebraic spine is the P4" in report))
    checks.append(("report_no_ring_stability", "no stability test was performed" in report.lower()))
    checks.append(("report_no_bootstrap", "families selected by bootstrap: **0**" in report))

    failed = [name for name, passed in checks if not passed]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "checks_passed": sum(passed for _, passed in checks),
        "checks_total": len(checks),
        "catch_proofs_passed": sum(passed for _, passed in catches),
        "catch_proofs_total": len(catches),
        "failed": failed,
        "derive_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "derive_stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_rows = [
        {"catch_id": f"C{index:02d}", "failure_class": name, "result": "REJECTED" if passed else "MISSED"}
        for index, (name, passed) in enumerate(catches, 1)
    ]
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(write_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(write_rows)
    print(f"{'PASS' if not failed else 'FAIL'} atlas verification: {payload['checks_passed']}/{payload['checks_total']}; catches={payload['catch_proofs_passed']}/{payload['catch_proofs_total']}")
    if failed:
        print("failed=" + ",".join(failed), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
