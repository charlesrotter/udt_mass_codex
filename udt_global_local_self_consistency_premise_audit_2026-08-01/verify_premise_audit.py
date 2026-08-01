#!/usr/bin/env python3
"""Fail-closed verifier for the global/local premise audit."""

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


EXPECTED_INTERPRETATIONS = {
    "I01": "NOT_DERIVED_ONTOLOGY_IS_TRACE_RULE",
    "I02": "COMPLETE_SPECIFICATION_NOT_PHYSICAL_SELECTION",
    "I03": "DERIVED_PARTIAL_READOUT_NO_SELECTED_SECTION",
    "I04": "GRAPH_IS_NONSELECTION_EXACT",
    "I05": "FINITE_DOMAIN_NOT_BOUNDARY_OR_RETURN",
    "I06": "NATURALITY_GATE_NOT_LAW_GENERATOR",
    "I07": "PAIRING_SCOPED_NO_WHOLE_RELATION",
    "I08": "OPEN_NO_SELECTED_VARIATIONAL_RULE",
    "I09": "CONDITIONAL_STABILITY_IS_DOWNSTREAM",
    "I10": "CALIBRATION_OR_DISCRIMINATION_NOT_DERIVATION",
    "I11": "WORKING_SEMANTIC_POSIT_OPERATIONALLY_INCOMPLETE",
    "I12": "NO_OTHER_COMPLETE_ROUTE_IN_FROZEN_UNIVERSE",
}

EXPECTED_TYPES = {
    "T01": "NOT_DERIVED_MULTIPLE_SECTIONS",
    "T02": "NOT_DERIVED_READOUT_NONINJECTIVE",
    "T03": "OPEN_STRONGER_REALIZATION",
    "T04": "OPEN_REQUIRES_ACTION_AND_BOUNDARY",
    "T05": "OPEN_REQUIRES_BOUNDARY_EXTENSION_LAW",
    "T06": "OPEN_REQUIRES_OBSERVABLE_RESPONSE_PAIRING",
    "T07": "MINIMUM_ADDITIONAL_LOGICAL_TYPE_NOT_DERIVED",
    "T08": "OPEN_STRONGER_SELECTION_SEMANTICS",
}


def interpretations_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("candidate_id") for row in rows]
    if len(rows) != 12 or len(ids) != len(set(ids)) or set(ids) != set(EXPECTED_INTERPRETATIONS):
        return False
    by_id = {row["candidate_id"]: row for row in rows}
    return all(
        by_id[key].get("status") == value and by_id[key].get("basis") and by_id[key].get("ruling")
        for key, value in EXPECTED_INTERPRETATIONS.items()
    )


def types_ok(rows: list[dict[str, str]]) -> bool:
    ids = [row.get("type_id") for row in rows]
    if len(rows) != 8 or len(ids) != len(set(ids)) or set(ids) != set(EXPECTED_TYPES):
        return False
    by_id = {row["type_id"]: row for row in rows}
    return all(
        by_id[key].get("status") == value and by_id[key].get("relative_strength") and by_id[key].get("ruling")
        for key, value in EXPECTED_TYPES.items()
    ) and by_id["T07"]["relative_strength"] == "MINIMAL_OPERATIONAL_MUTUAL_DETERMINATION_TYPE" and sum(
        row.get("relative_strength") == "MINIMAL_OPERATIONAL_MUTUAL_DETERMINATION_TYPE" for row in rows
    ) == 1


def result_ok(data: dict) -> bool:
    return data == {
        "bootstrap_adopted_by_audit": False,
        "candidate_formula_constructed": False,
        "deductive_independence_proved": False,
        "frozen_record_derivation_found": False,
        "future_same_premise_metric_theorem_excluded": False,
        "gpu_used": False,
        "interpretations": 12,
        "interpretations_passing_derived_mutual_determination": 0,
        "minimum_extra_logical_type": "OBSERVER_NATURAL_RELATION_ON_INDEPENDENT_X_TIMES_O_WITH_NONTRIVIAL_DEPENDENCE_ON_BOTH_AND_NONEMPTY_PROPER_GRAPH_INTERSECTION",
        "minimum_type_derived": False,
        "outcome": "BOOTSTRAP_IS_DISTINCT_POSIT",
        "premises": 18,
        "return_types": 8,
        "solve_authorized": False,
        "source_anchors": 16,
        "source_paths_verified": 1424,
    }


def algebra_ok(data: dict) -> bool:
    return (
        data.get("complete_state_count") == 4
        and data.get("readout_state_count") == 2
        and data.get("readout_graph_size") == 4
        and data.get("readout_graph_configuration_survivors") == 4
        and data.get("readout_fiber_sizes") == {"0": 2, "1": 2}
        and data.get("readout_is_surjective") is True
        and data.get("readout_is_injective") is False
        and data.get("right_inverse_section_count") == 4
        and data.get("distinct_section_image_count") == 4
        and data.get("section_fixed_set_sizes") == [2, 2, 2, 2]
        and data.get("finite_admissibility_predicate_count") == 16
        and data.get("observer_orbit_count") == 2
        and data.get("observer_saturated_relation_count") == 4
        and data.get("nonempty_proper_observer_saturated_relation_count") == 2
        and data.get("proper_saturated_relation_sizes") == [2, 2]
        and data.get("proper_saturated_relations_disjoint") is True
        and data.get("graph_subrelation_equivalent_to_X_predicate") is True
        and data.get("operational_independent_product_size") == 8
        and data.get("operational_relation_count_tested") == 2
        and data.get("operational_relations_depend_on_X") is True
        and data.get("operational_relations_depend_on_O") is True
        and data.get("operational_graph_intersection_sizes") == [2, 2]
        and data.get("transitive_control_observer_orbit_count") == 1
        and data.get("transitive_control_nonempty_proper_saturated_relation_count") == 0
    )


def main() -> None:
    checks: list[tuple[str, bool]] = []
    inventory = tsv("SOURCE_INVENTORY.tsv")
    checks.append(("source_count_1424", len(inventory) == 1424))
    checks.append(("source_unique_sorted", [row["path"] for row in inventory] == sorted({row["path"] for row in inventory})))
    checks.append(("source_bytes_match", all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in inventory)))
    checks.append(("premises_18", len(tsv("PREMISE_LEDGER.tsv")) == 18))

    anchors = tsv("SOURCE_AUTHORITY_LEDGER.tsv")
    checks.append(("anchors_16_unique", len(anchors) == len({row["anchor_id"] for row in anchors}) == 16))
    checks.append(("anchor_bytes_match", all(sha256(ROOT / row["path"]) == row["sha256"] for row in anchors)))
    checks.append(("term_definitions_10", len(tsv("TERM_DEFINITION_LEDGER.tsv")) == 10))

    generated = [
        "SOURCE_AUTHORITY_LEDGER.tsv",
        "TERM_DEFINITION_LEDGER.tsv",
        "INTERPRETATION_OUTCOMES.tsv",
        "RETURN_TYPE_OUTCOMES.tsv",
        "MINIMUM_LEVEL_LEDGER.tsv",
        "ALGEBRA_RESULT.json",
        "COUNTERMODEL_LEDGER.tsv",
        "IMPLICATION_LEDGER.tsv",
        "STATUS_LEDGER.tsv",
        "RESULT.json",
    ]
    before = {name: sha256(PKG / name) for name in generated}
    proc = subprocess.run(
        [sys.executable, str(PKG / "derive_premise_audit.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    after = {name: sha256(PKG / name) for name in generated}
    checks.append(("derivation_exit_0", proc.returncode == 0))
    checks.append(("deterministic_replay", before == after))

    interpretations = tsv("INTERPRETATION_OUTCOMES.tsv")
    return_types = tsv("RETURN_TYPE_OUTCOMES.tsv")
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    algebra = json.loads((PKG / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    checks.append(("interpretations_exact", interpretations_ok(interpretations)))
    checks.append(("return_types_exact", types_ok(return_types)))
    minimum_levels = tsv("MINIMUM_LEVEL_LEDGER.tsv")
    checks.append(("minimum_levels_7", len(minimum_levels) == 7 and [row["level_id"] for row in minimum_levels] == [f"M{i:02d}" for i in range(1, 8)]))
    checks.append(("graph_predicate_not_mutual_determination", next(row for row in minimum_levels if row["level_id"] == "M02")["status"] == "TYPE_IDENTIFIED_INSUFFICIENT_FOR_MUTUAL_DETERMINATION"))
    checks.append(("premise_minimum_separate", next(row for row in minimum_levels if row["level_id"] == "M03")["status"] == "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE"))
    checks.append(("response_not_premise_minimum", next(row for row in minimum_levels if row["level_id"] == "M05")["status"] == "OPEN_STRONGER_REQUIRED_FOR_LINEAR_RESPONSE_OR_ACTION_TEST"))
    checks.append(("result_exact", result_ok(result)))
    checks.append(("algebra_exact", algebra_ok(algebra)))
    checks.append(("countermodels_7", len(tsv("COUNTERMODEL_LEDGER.tsv")) == 7))
    implications = tsv("IMPLICATION_LEDGER.tsv")
    checks.append(("implications_12", len(implications) == 12 and len({row["implication_id"] for row in implications}) == 12))
    status = tsv("STATUS_LEDGER.tsv")
    checks.append(("status_ceiling", status[-1]["status"] == "BOOTSTRAP_IS_DISTINCT_POSIT" and status[-1]["remaining"].startswith("not adopted")))

    catches: list[tuple[str, bool]] = []
    catches.append(("missing_interpretation", not interpretations_ok(interpretations[:-1])))
    catches.append(("duplicate_interpretation", not interpretations_ok(interpretations + [copy.deepcopy(interpretations[0])])))
    interpretation_mutations = {
        "I01": "DERIVED_BOOTSTRAP_FROM_METRIC_ONTOLOGY",
        "I02": "COMPLETE_METRIC_IS_UNIQUE_REALIZED_UNIVERSE",
        "I03": "READOUT_SELECTS_UNIQUE_SECTION",
        "I04": "GRAPH_IS_FIXED_POINT",
        "I05": "FINITE_DOMAIN_DERIVES_BOUNDARY_LAW",
        "I06": "RECIPROCITY_DERIVES_RETURN",
        "I07": "PAIRING_IS_COMPLETE_RESPONSE",
        "I08": "NATIVE_ACTION_SELECTED",
        "I09": "STABILITY_CREATES_SOLUTION_LAW",
        "I10": "OBSERVATION_DERIVES_CLOSURE",
        "I11": "BOOTSTRAP_OPERATION_DERIVED",
        "I12": "OTHER_ROUTE_PASSES",
    }
    for candidate_id, false_status in interpretation_mutations.items():
        mutated = copy.deepcopy(interpretations)
        next(row for row in mutated if row["candidate_id"] == candidate_id)["status"] = false_status
        catches.append((f"promotion_{candidate_id}", not interpretations_ok(mutated)))
    mutated = copy.deepcopy(return_types)
    next(row for row in mutated if row["type_id"] == "T07")["status"] = "DERIVED_NATIVE_RELATION"
    catches.append(("minimum_type_promoted_to_derived", not types_ok(mutated)))
    mutated = copy.deepcopy(return_types)
    next(row for row in mutated if row["type_id"] == "T03")["relative_strength"] = "MINIMAL_OPERATIONAL_MUTUAL_DETERMINATION_TYPE"
    catches.append(("fixed_point_called_minimal", not types_ok(mutated)))
    mutated_levels = copy.deepcopy(minimum_levels)
    next(row for row in mutated_levels if row["level_id"] == "M05")["status"] = "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE"
    catches.append(("response_one_form_conflated_with_premise_minimum", sum(row["status"] == "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE" for row in mutated_levels) != 1))
    mutated_levels = copy.deepcopy(minimum_levels)
    next(row for row in mutated_levels if row["level_id"] == "M02")["status"] = "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE"
    catches.append(("X_predicate_conflated_with_mutual_determination", sum(row["status"] == "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE" for row in mutated_levels) != 1))
    for field, value, name in [
        ("minimum_type_derived", True, "false_type_derivation"),
        ("deductive_independence_proved", True, "false_independence_theorem"),
        ("future_same_premise_metric_theorem_excluded", True, "future_theorem_excluded"),
        ("frozen_record_derivation_found", True, "false_frozen_derivation"),
        ("bootstrap_adopted_by_audit", True, "unauthorized_adoption"),
        ("candidate_formula_constructed", True, "formula_smuggle"),
        ("solve_authorized", True, "unauthorized_solve"),
        ("interpretations_passing_derived_mutual_determination", 1, "false_derived_pass"),
    ]:
        mutated_result = copy.deepcopy(result)
        mutated_result[field] = value
        catches.append((name, not result_ok(mutated_result)))
    algebra_mutations = {
        "readout_graph_configuration_survivors": 2,
        "right_inverse_section_count": 1,
        "finite_admissibility_predicate_count": 1,
        "nonempty_proper_observer_saturated_relation_count": 1,
        "proper_saturated_relations_disjoint": False,
        "readout_is_injective": True,
        "graph_subrelation_equivalent_to_X_predicate": False,
        "operational_relations_depend_on_O": False,
        "transitive_control_nonempty_proper_saturated_relation_count": 1,
    }
    for field, value in algebra_mutations.items():
        mutated_algebra = copy.deepcopy(algebra)
        mutated_algebra[field] = value
        catches.append((f"algebra_{field}", not algebra_ok(mutated_algebra)))
    checks.extend((f"catch_{name}", passed) for name, passed in catches)

    for name in ["AUDIT_REPORT.md", "EXACT_DERIVATION.md", "COMPLETENESS_MAP.md", "LAY_REPORT.md"]:
        checks.append((f"present_{name}", (PKG / name).is_file()))
    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    checks.append(("report_outcome", "BOOTSTRAP_IS_DISTINCT_POSIT" in report))
    checks.append(("report_not_adopted", "not adopt, canonize, or define the relation" in report))
    checks.append(("report_minimum_type", "observer-natural relation on independent X and O" in report and "nontrivial dependence on both" in report))
    checks.append(("report_X_predicate_insufficient", "predicate on `X` alone" in report and "does not establish that global data feed back" in report))
    checks.append(("report_hard_stop", "Repeating those same readout, finiteness, and symmetry implications would be circular" in report))
    checks.append(("report_no_independence_overclaim", "not a proof of deductive independence" in report and "genuinely new metric theorem" in report))

    failed = [name for name, passed in checks if not passed]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "checks_passed": sum(passed for _, passed in checks),
        "checks_total": len(checks),
        "catch_proofs_passed": sum(passed for _, passed in catches),
        "catch_proofs_total": len(catches),
        "failed": failed,
        "derivation_stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
        "derivation_stderr_sha256": hashlib.sha256(proc.stderr.encode()).hexdigest(),
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "failure_class", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {"catch_id": f"C{index:02d}", "failure_class": name, "result": "REJECTED" if passed else "MISSED"}
            for index, (name, passed) in enumerate(catches, 1)
        )
    print(
        f"{'PASS' if not failed else 'FAIL'} premise audit verification: "
        f"{payload['checks_passed']}/{payload['checks_total']}; "
        f"catches={payload['catch_proofs_passed']}/{payload['catch_proofs_total']}"
    )
    if failed:
        print("failed=" + ",".join(failed), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
