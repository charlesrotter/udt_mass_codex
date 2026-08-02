#!/usr/bin/env python3
"""Fail-closed verification and exercised mutation catches for the census."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
VALID_DISPOSITIONS = {
    "SIX_GATE_SOURCE", "SUPPORTING_OR_INCOMPLETE_BRANCH_SOURCE",
    "SUPPORTING_LOCAL_OR_CONTEXT_SOURCE", "CONTEXT_ONLY_NOT_BRANCH_SOURCE",
    "MIXED__SEE_PATH_LEVEL_DISPOSITIONS", "REORGANIZATION_FORENSIC_RECORD",
    "PROVENANCE_OR_HISTORICAL_ONLY", "CONTROL_OR_TEST_SUPPORT",
    "SUPPORTING_REFERENCE_OR_REVIEW", "SUPPORTING_OR_PROVENANCE_NOT_STANDALONE_BRANCH",
    "CONTROL_CONTEXT", "SUPPORTING_OR_HISTORICAL_NOT_STANDALONE_BRANCH",
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique(data: list[dict[str, str]], key: str, count: int) -> None:
    values = [row[key] for row in data]
    assert len(data) == count
    assert len(set(values)) == count


def validate_reports(data: list[dict[str, str]]) -> None:
    unique(data, "path", 239)
    assert all(row["scientific_disposition"] in VALID_DISPOSITIONS for row in data)
    assert all(row["source_result_excerpt"] for row in data)
    assert sum(row["scientific_disposition"] == "SIX_GATE_SOURCE" for row in data) == 37


def validate_groups(data: list[dict[str, str]]) -> None:
    unique(data, "top_group", 280)
    assert all(row["scientific_disposition"] in VALID_DISPOSITIONS for row in data)
    assert all("PENDING" not in row["scientific_disposition"] for row in data)
    root = {row["top_group"]: row for row in data}["ROOT"]
    assert root["scientific_disposition"] == "MIXED__SEE_PATH_LEVEL_DISPOSITIONS"


def validate_hits(data: list[dict[str, str]]) -> None:
    unique(data, "path", 4461)
    assert all(row["path_disposition"] in VALID_DISPOSITIONS for row in data)
    assert all(row["disposition_evidence"] for row in data)
    assert sum(row["top_group"] == "ROOT" for row in data) == 283


def validate_cases(data: list[dict[str, str]], report_map: dict[str, dict[str, str]]) -> None:
    unique(data, "case_id", 18)
    assert {row["case_id"] for row in data} == {f"B{i:02d}" for i in range(1, 19)}
    valid_classes = {f"C{i:02d}" for i in range(1, 16)}
    for row in data:
        assert set(row["candidate_classes"].split(";")) <= valid_classes
        source = report_map[row["source_path"]]
        assert row["source_sha256"] == source["sha256"]
        assert row["source_group"] == source["top_group"]
        assert not any(word in row["ruling"] for word in ("CARRIER_DERIVED", "ACTION_SELECTED", "ON_SHELL_SELECTED"))
    by_id = {row["case_id"]: row for row in data}
    assert by_id["B01"]["gate6_relative_curvature"] == "PASS_NONZERO_AT_P00_ALL_6"
    assert "FAIL_AMBIENT_PARALLEL_HOLONOMY" in by_id["B01"]["gate4_transport_holonomy"]
    assert by_id["B02"]["gate6_relative_curvature"] == "PASS_SAME_NONZERO_RELATIVE_TERM_AS_B01"
    assert by_id["B03"]["gate6_relative_curvature"] == "FAIL_ZERO_DP"
    assert by_id["B06"]["gate1_intrinsic"] == "FAIL_SEMISIMPLE_PROJECTOR"
    assert by_id["B11"]["gate2_rank_uniqueness"] == "FAIL_UNIQUE_RAY"
    assert by_id["B12"]["gate1_intrinsic"] == "FAIL_METRIC_SELECTION__PLANE_SUPPLIED"
    assert by_id["B18"]["gate5_global_descent"] == "FAIL_MISSING_COMPLETE_G_PHI_WITNESS"


def validate_relative(data: list[dict[str, str]]) -> None:
    unique(data, "branch_id", 6)
    assert {row["branch_id"] for row in data} == {f"C{i:02d}" for i in range(1, 7)}
    assert all(row["nontrivial_somewhere"] == "YES" for row in data)
    assert all(row["relative_curvature_component_Q23_12"] not in {"0", "0/1"} for row in data)
    assert all(row["maximum_status"] == "DERIVED_CONDITIONAL_ON_REGISTERED_COMPLETE_CONFIGURATION" for row in data)


def expect_failure(name: str, callback, catches: list[dict[str, str]]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        catches.append({"catch_id": name, "status": "PASS"})
        return
    raise AssertionError(f"mutation accepted: {name}")


def main() -> int:
    report_universe = {row["path"]: row for row in rows("AUDIT_REPORT_UNIVERSE.tsv")}
    reports = rows("REPORT_DISPOSITIONS.tsv")
    groups = rows("GROUP_DISPOSITIONS.tsv")
    hits = rows("DISCOVERY_HIT_DISPOSITIONS.tsv")
    cases = rows("BRANCH_OBJECT_GATE_LEDGER.tsv")
    relative = rows("TWISTED_S3_RELATIVE_CURVATURE.tsv")
    validate_reports(reports)
    validate_groups(groups)
    validate_hits(hits)
    validate_cases(cases, report_universe)
    validate_relative(relative)

    source_manifest = rows("SIX_GATE_SOURCE_MANIFEST.tsv")
    unique(source_manifest, "path", 1270)
    for row in source_manifest:
        blob = subprocess.check_output(["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT)
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert derivation["status"] == independent["status"] == "PASS"
    assert derivation["twisted_s3_nonzero_relative_curvature_count"] == independent["branch_count"] == 6

    catches: list[dict[str, str]] = []
    expect_failure("F01_missing_report", lambda: validate_reports(reports[:-1]), catches)
    expect_failure("F02_duplicate_report", lambda: validate_reports(reports + [deepcopy(reports[0])]), catches)
    expect_failure("F03_missing_group", lambda: validate_groups(groups[:-1]), catches)
    expect_failure("F04_duplicate_group", lambda: validate_groups(groups + [deepcopy(groups[0])]), catches)
    expect_failure("F05_missing_hit", lambda: validate_hits(hits[:-1]), catches)
    expect_failure("F06_duplicate_hit", lambda: validate_hits(hits + [deepcopy(hits[0])]), catches)
    root_removed = [row for index, row in enumerate(hits) if not (row["top_group"] == "ROOT" and index == next(i for i, item in enumerate(hits) if item["top_group"] == "ROOT"))]
    expect_failure("F07_root_path_hidden", lambda: validate_hits(root_removed), catches)
    bad = deepcopy(cases); bad[0]["gate6_relative_curvature"] = "FAIL_ZERO"
    expect_failure("F08_zero_relative_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[0]["gate4_transport_holonomy"] = "PASS_AMBIENT_PARALLEL_HOLONOMY"
    expect_failure("F09_ambient_holonomy_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[-1]["gate5_global_descent"] = "PASS"
    expect_failure("F10_incomplete_completion_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[5]["gate1_intrinsic"] = "PASS_PROJECTOR"
    expect_failure("F11_null_projector_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[10]["gate2_rank_uniqueness"] = "PASS_UNIQUE_RAY"
    expect_failure("F12_celestial_fiber_section_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[11]["gate1_intrinsic"] = "PASS_METRIC_SELECTED"
    expect_failure("F13_supplied_plane_intrinsic_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[2]["gate6_relative_curvature"] = "PASS_NONZERO"
    expect_failure("F14_parallel_control_nonzero_promotion", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[0]["ruling"] = "CARRIER_DERIVED"
    expect_failure("F15_carrier_backfill", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[0]["ruling"] = "ACTION_SELECTED"
    expect_failure("F16_action_backfill", lambda: validate_cases(bad, report_universe), catches)
    bad = deepcopy(cases); bad[0]["source_sha256"] = "0" * 64
    expect_failure("F17_source_hash_mutation", lambda: validate_cases(bad, report_universe), catches)
    bad_relative = deepcopy(relative); bad_relative[0]["relative_curvature_component_Q23_12"] = "0"; bad_relative[0]["nontrivial_somewhere"] = "NO"
    expect_failure("F18_relative_witness_mutation", lambda: validate_relative(bad_relative), catches)
    bad_relative = relative[:-1]
    expect_failure("F19_missing_twisted_branch", lambda: validate_relative(bad_relative), catches)

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "status"], delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)
    assert len(catches) == 19 and all(row["status"] == "PASS" for row in catches)

    result = {
        "schema": "udt.branchwise_projector_holonomy_census.verification.v1",
        "status": "PASS",
        "reports": len(reports), "groups": len(groups), "hits": len(hits),
        "source_manifest_paths": len(source_manifest), "branch_object_cases": len(cases),
        "twisted_s3_relative_curvature_branches": len(relative), "catch_proofs": f"{len(catches)}/{len(catches)}",
        "frozen_blob_replay": "PASS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
