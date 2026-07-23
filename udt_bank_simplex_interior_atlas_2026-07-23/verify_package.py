#!/usr/bin/env python3
"""Fail-closed package verifier for the bank-simplex lattice atlas."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, mode="rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def load_signs(path):
    with gzip.open(path, "rb") as handle:
        return np.load(handle, allow_pickle=False)


def main():
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    groups = read_tsv(HERE / "GROUP_REGISTRY.tsv")
    census = read_tsv(HERE / "LATTICE_SHEET_CENSUS.tsv")
    interval = read_tsv(HERE / "COARSE_INTERVAL_CENSUS.tsv.gz")
    comparison = read_tsv(HERE / "CHART_COMPARISON.tsv")
    premises = read_tsv(HERE / "PREMISE_STATUS_LEDGER.tsv")
    status = read_tsv(HERE / "STATUS_LEDGER.tsv")
    anchors = read_tsv(HERE / "HIGH_PRECISION_FULL_MATRIX_ANCHORS.tsv")
    catches = []

    def check(label, condition):
        catches.append(
            {
                "catch_id": f"P{len(catches)+1:02d}",
                "check_type": "STATE_ASSERTION",
                "check": label,
                "status": "PASS" if condition else "FAIL",
            }
        )
        if not condition:
            raise AssertionError(label)

    check("384_unique_groups", len(groups) == 384 and len({row["group_id"] for row in groups}) == 384)
    check(
        "1536_unique_level_sheet_rows",
        len(census) == 1536
        and len({(row["level"], row["sheet_id"]) for row in census}) == 1536,
    )
    check("768_interval_rows", len(interval) == 768 and len({row["sheet_id"] for row in interval}) == 768)
    check("two_chart_comparison", len(comparison) >= 10)
    check("premise_ledger_present", len(premises) == 16)
    check("status_ledger_present", len(status) == 12)
    check("zero_numeric_zero_nodes", all(int(row["numerically_zero_nodes"]) == 0 for row in census))
    check(
        "all_resolution_classes_reproduced",
        all(row["cross_resolution_status"] == "QUALITATIVE_CLASS_REPRODUCED" for row in census),
    )
    l2 = [row for row in census if row["level"] == "L2"]
    counts = Counter(row["primary_class"] for row in l2)
    check(
        "balanced_l2_chart_classes",
        counts
        == {
            "ONE_OR_TWO_TRANSITION_FAMILIES__TWO_SAMPLED_NULL_COMPONENTS": 384,
            "ONE_TRANSITION_FAMILY__ONE_SAMPLED_NULL_COMPONENT": 384,
        },
    )
    j1 = [row for row in l2 if row["chart"].startswith("J1")]
    j2 = [row for row in l2 if row["chart"].startswith("J2")]
    check(
        "j1_pocket_component_identity",
        len(j1) == 384
        and all(
            int(row["base_negative_components"]) == 1
            and int(row["base_positive_components"]) == 1
            and int(row["transition_count_2_fibers"]) == int(row["base_negative_nodes"])
            and int(row["sampled_null_components"]) == 2
            and int(row["sampled_negative_components"]) == 2
            for row in j1
        ),
    )
    check(
        "j2_single_component_identity",
        len(j2) == 384
        and all(
            int(row["base_negative_nodes"]) == 0
            and int(row["base_positive_components"]) == 1
            and int(row["transition_count_1_fibers"]) == 2601
            and int(row["sampled_null_components"]) == 1
            and int(row["sampled_negative_components"]) == 1
            for row in j2
        ),
    )
    check(
        "raw_sign_hashes",
        all(
            digest(HERE / name) == expected
            for name, expected in result["raw_sign_files"].items()
        ),
    )
    raw_shapes = {
        name: load_signs(HERE / name).shape for name in result["raw_sign_files"]
    }
    check(
        "raw_sign_shapes",
        raw_shapes
        == {
            "RAW_SIGNS_L1_J1.npy.gz": (384, 26325),
            "RAW_SIGNS_L1_J2.npy.gz": (384, 26325),
            "RAW_SIGNS_L2_J1.npy.gz": (384, 335529),
            "RAW_SIGNS_L2_J2.npy.gz": (384, 335529),
        },
    )
    check(
        "coarse_unresolved_retained",
        result["coarse_derivative_indeterminate_boxes"] == 5_140_116
        and result["coarse_face_indeterminate_boxes"] == 342_811
        and result["coarse_vertex_indeterminate_boxes"] == 0,
    )
    check(
        "independent_all_nodes",
        independent["verdict"] == "PASS"
        and independent["node_signs_checked"] == 277_903_872
        and independent["node_sign_mismatches"] == 0
        and independent["transition_count_mismatches"] == 0
        and independent["nonnegative_metric_determinants"] == 0,
    )
    check(
        "independent_boundary_replay",
        independent["boundary_edge_replay"]["boundary_failures"] == 0
        and independent["boundary_edge_replay"]["prior_sheet_rows"] == 4608,
    )
    check(
        "high_precision_anchors",
        len(anchors) == 34
        and all(
            row["status"] == "HIGH_PRECISION_INTERVAL_SIGN_AND_DETERMINANT_AGREE"
            for row in anchors
        ),
    )
    check(
        "no_physical_filter",
        result["physical_regime_labels_used"] == 0
        and result["actions_or_eom_loaded"] == 0
        and result["carrier_interpretations_loaded"] == 0,
    )
    check(
        "maximum_conclusion_exact",
        result["maximum_conclusion"]
        == "BOUNDED_REGISTERED_COMPLETE_BANK-SIMPLEX_LATTICE_ATLAS_WITH_INTERVAL_AND_MATRIX_CHECKS",
    )
    check(
        "source_hashes_current",
        all(digest(ROOT / path) == expected for path, expected in result["source_hashes"].items()),
    )

    check(
        "independent_end_to_end_mutations",
        independent["mutation_catch_proofs"] >= 10
        and independent["all_checks_passed"]
        == independent["assertion_checks"] + independent["mutation_catch_proofs"],
    )

    write_tsv(
        HERE / "PACKAGE_ASSERTION_CHECKS.tsv", list(catches[0]), catches
    )
    output = {
        "schema": "udt-bank-simplex-package-verification-1.0",
        "status": "PASS_WITH_REGISTERED_LATTICE_SCOPE",
        "groups": len(groups),
        "lattice_rows": len(census),
        "l2_sheets": len(l2),
        "l2_class_counts": dict(counts),
        "numerically_zero_nodes": sum(
            int(row["numerically_zero_nodes"]) for row in census
        ),
        "resolution_agreement_rows": sum(
            row["cross_resolution_status"] == "QUALITATIVE_CLASS_REPRODUCED"
            for row in census
        ),
        "raw_sign_shapes": {key: list(value) for key, value in raw_shapes.items()},
        "independent_node_signs": independent["node_signs_checked"],
        "high_precision_anchors": len(anchors),
        "package_assertion_checks": len(catches),
        "package_assertion_checks_passed": sum(
            row["status"] == "PASS" for row in catches
        ),
        "maximum_conclusion": result["maximum_conclusion"],
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
