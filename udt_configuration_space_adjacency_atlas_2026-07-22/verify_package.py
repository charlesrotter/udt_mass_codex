#!/usr/bin/env python3
"""Fail-closed package verifier for the configuration-space adjacency atlas."""

from __future__ import annotations

import copy
import csv
import gzip
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"


def rows(path):
    opener = gzip.open if Path(path).suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def validate_state(state):
    require(state["endpoint_pairs"] == 2_304, "endpoint-pair count")
    require(state["endpoint_pair_unique"] == 2_304, "endpoint-pair uniqueness")
    require(state["matched_groups"] == 384, "matched-group count")
    require(state["endpoint_pair_types"] == {
        "CROSS_SECTOR": 1_152,
        "SAME_SIGN_CONTROL": 1_152,
    }, "endpoint-pair type census")
    require(state["sheets"] == 4_608, "sheet count")
    require(state["sheet_unique"] == 4_608, "sheet uniqueness")
    require(state["chart_counts"] == {
        "J1_GENERATOR_COEFFICIENT_JOIN": 2_304,
        "J2_EVALUATED_COFIELD_JOIN": 2_304,
    }, "chart census")
    require(state["sheet_classes"] == {
        "FORCED_SINGLE_REGULAR_NULL_GRAPH": 2_304,
        "UNIFORMLY_SPACELIKE_SHEET": 2_304,
    }, "sheet-class census")
    require(state["same_sign_certificates"] == 2_304, "same-sign certificates")
    require(state["same_sign_strict"] == 2_304, "same-sign strictness")
    require(state["null_graph_certificates"] == 2_304, "null-graph certificates")
    require(state["null_graph_complete"] == 2_304, "null-graph gates")
    require(state["null_graph_bounds_in_domain"] == 2_304, "null-domain bounds")
    require(state["unresolved_rows"] == 0, "unresolved rows")
    require(state["chart_comparisons"] == 1_152, "chart comparison count")
    require(state["chart_separator_agreement"] == 1_152, "chart separator agreement")
    require(state["high_precision_anchors"] == 12, "production high-precision anchors")
    require(state["independent_matrix_anchors"] == 12, "independent matrix anchors")
    require(state["independent_same_probes"] == 195_840, "independent same probes")
    require(state["independent_cross_roots"] == 11_520, "independent cross roots")
    require(state["independent_builder_imported"] is False, "independent builder import")
    require(state["independent_catches"] == 5, "independent catches")
    require(state["source_integrity"] is True, "source integrity")
    require(state["status_rows"] == 15, "status ledger")
    require(state["premise_rows"] == 20, "premise ledger")
    require(state["physical_labels"] == 0, "physical labels")
    require(state["actions_loaded"] == 0, "action import")
    require(state["matter_carriers_loaded"] == 0, "matter-carrier import")
    require(state["simplex_interiors"] == 0, "simplex overclaim")
    require(state["gpu_runs"] == 0, "GPU use")
    require(state["report_guards"] is True, "report scope guards")


def mutation_catches(state):
    mutations = (
        ("P01_MISSING_ENDPOINT_PAIR", lambda value: value.__setitem__("endpoint_pairs", 2_303)),
        ("P02_DUPLICATE_ENDPOINT_PAIR", lambda value: value.__setitem__("endpoint_pair_unique", 2_303)),
        ("P03_MISSING_GROUP", lambda value: value.__setitem__("matched_groups", 383)),
        ("P04_MISSING_SHEET", lambda value: value.__setitem__("sheets", 4_607)),
        ("P05_DUPLICATE_SHEET", lambda value: value.__setitem__("sheet_unique", 4_607)),
        ("P06_COUNT_CHARTS_AS_UNIVERSES", lambda value: value["chart_counts"].update({
            "J1_GENERATOR_COEFFICIENT_JOIN": 4_608
        })),
        ("P07_FLIP_SHEET_CLASS", lambda value: value["sheet_classes"].update({
            "FORCED_SINGLE_REGULAR_NULL_GRAPH": 2_303,
            "UNIFORMLY_SPACELIKE_SHEET": 2_305,
        })),
        ("P08_DROP_SAME_CERTIFICATE", lambda value: value.__setitem__("same_sign_certificates", 2_303)),
        ("P09_ENDPOINT_ONLY_SAME_SIGN", lambda value: value.__setitem__("same_sign_strict", 2_303)),
        ("P10_DROP_NULL_GRAPH", lambda value: value.__setitem__("null_graph_certificates", 2_303)),
        ("P11_HIDE_REGULARITY_FAILURE", lambda value: value.__setitem__("null_graph_complete", 2_303)),
        ("P12_OUT_OF_DOMAIN_BOUND", lambda value: value.__setitem__("null_graph_bounds_in_domain", 2_303)),
        ("P13_HIDE_UNRESOLVED", lambda value: value.__setitem__("unresolved_rows", 1)),
        ("P14_PROMOTE_CHART_SHAPE", lambda value: value.__setitem__("chart_separator_agreement", 1_151)),
        ("P15_DROP_MATRIX_ANCHOR", lambda value: value.__setitem__("independent_matrix_anchors", 11)),
        ("P16_IMPORT_PRODUCTION_BUILDER", lambda value: value.__setitem__("independent_builder_imported", True)),
        ("P17_MUTATE_SOURCE", lambda value: value.__setitem__("source_integrity", False)),
        ("P18_ASSIGN_PHYSICAL_LABEL", lambda value: value.__setitem__("physical_labels", 1)),
        ("P19_IMPORT_ACTION", lambda value: value.__setitem__("actions_loaded", 1)),
        ("P20_PROMOTE_TO_SIMPLEX", lambda value: value.__setitem__("simplex_interiors", 1)),
    )
    output = []
    for catch_id, mutate in mutations:
        corrupted = copy.deepcopy(state)
        mutate(corrupted)
        try:
            validate_state(corrupted)
        except AssertionError as exc:
            output.append({
                "catch_id": catch_id,
                "validator": "validate_state",
                "rejection": str(exc),
                "result": "MUTATION_REJECTED_AS_REQUIRED",
            })
        else:
            raise AssertionError(f"mutation escaped {catch_id}")
    return output


def main():
    source = rows(HERE / "SOURCE_LEDGER.tsv")
    source_integrity = len(source) == 8
    for row in source:
        path = ROOT / row["path"]
        observed_blob = subprocess.check_output(
            ["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True
        ).strip()
        source_integrity &= (
            path.exists()
            and digest(path) == row["sha256"]
            and observed_blob == row["base_blob"]
        )

    endpoints = rows(HERE / "ENDPOINT_PAIR_REGISTRY.tsv")
    sheets = rows(HERE / "SHEET_CLASSIFICATION.tsv")
    same = rows(HERE / "SAME_SIGN_BOX_CERTIFICATES.tsv.gz")
    null = rows(HERE / "NULL_GRAPH_CERTIFICATES.tsv.gz")
    unresolved = rows(HERE / "UNRESOLVED_BOXES.tsv")
    comparisons = rows(HERE / "CHART_COMPARISON.tsv")
    anchors = rows(HERE / "HIGH_PRECISION_ANCHORS.tsv")
    status = rows(HERE / "STATUS_LEDGER.tsv")
    premises = rows(HERE / "PREMISE_STATUS_LEDGER.tsv")
    result = json.loads((HERE / "RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text()

    null_complete = sum(
        row["endpoint_signs"] == "CERTIFIED"
        and row["outer_region_signs"] == "CERTIFIED"
        and row["root_band_derivative"] == "STRICTLY_NEGATIVE"
        and row["root_band_dphi"] == "NONZERO_COMPONENT_CERTIFIED"
        and float(row["left_region_s_lower"]) > 0.0
        and float(row["right_region_s_upper"]) < 0.0
        and float(row["partial_lambda_s_upper"]) < 0.0
        for row in null
    )
    domain_bounds = sum(
        0.0 <= float(row["lambda_root_envelope_lo"])
        <= float(row["lambda_root_envelope_hi"]) <= 1.0
        for row in null
    )
    report_phrases = (
        "adjacent—not disconnected",
        "not 4,608 universes",
        "not a time evolution or a selected universe",
        "chart-dependent",
        "not measurements of a",
        "not canonization",
    )
    state = {
        "endpoint_pairs": len(endpoints),
        "endpoint_pair_unique": len({row["endpoint_pair_id"] for row in endpoints}),
        "matched_groups": len({(row["carrier_id"], row["mask_id"]) for row in endpoints}),
        "endpoint_pair_types": dict(sorted(Counter(row["pair_type"] for row in endpoints).items())),
        "sheets": len(sheets),
        "sheet_unique": len({row["sheet_id"] for row in sheets}),
        "chart_counts": dict(sorted(Counter(row["chart"] for row in sheets).items())),
        "sheet_classes": dict(sorted(Counter(row["primary_class"] for row in sheets).items())),
        "same_sign_certificates": len(same),
        "same_sign_strict": sum(
            row["certificate"] == "COMPLETE_SHEET_STRICTLY_SPACELIKE"
            and float(row["minimum_s_lower"]) > 0.0
            for row in same
        ),
        "null_graph_certificates": len(null),
        "null_graph_complete": null_complete,
        "null_graph_bounds_in_domain": domain_bounds,
        "unresolved_rows": len(unresolved),
        "chart_comparisons": len(comparisons),
        "chart_separator_agreement": sum(
            row["topological_separator_agreement"] == "YES"
            and row["shape_status"] == "CHART_DEPENDENT_ENVELOPES__EXISTENCE_INVARIANT"
            for row in comparisons
        ),
        "high_precision_anchors": sum(
            row["status"] == "HIGH_PRECISION_SIGN_AGREEMENT" for row in anchors
        ),
        "independent_matrix_anchors": independent["high_precision_matrix_anchor_count"],
        "independent_same_probes": independent["sampled_same_sign_matrix_values"],
        "independent_cross_roots": independent["sampled_cross_sector_matrix_roots"],
        "independent_builder_imported": independent["production_builder_imported"],
        "independent_catches": len(independent["mutation_catches"]),
        "source_integrity": source_integrity,
        "status_rows": len(status),
        "premise_rows": len(premises),
        "physical_labels": sum(row["physical_label"] != "NONE" for row in sheets),
        "actions_loaded": result["actions_loaded"],
        "matter_carriers_loaded": result["matter_carriers_loaded"],
        "simplex_interiors": result["simplex_interiors_covered"],
        "gpu_runs": result["gpu_runs"],
        "report_guards": all(phrase in report for phrase in report_phrases),
    }
    validate_state(state)
    catches = mutation_catches(state)
    with (HERE / "PACKAGE_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    package_result = {
        "status": "PASS_WITH_REGISTERED_SCOPE",
        "state": state,
        "package_catches_passed": len(catches),
        "independent_method": independent["method"],
        "independent_catches_passed": len(independent["mutation_catches"]),
        "maximum_conclusion": result["maximum_conclusion"],
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(package_result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(package_result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
