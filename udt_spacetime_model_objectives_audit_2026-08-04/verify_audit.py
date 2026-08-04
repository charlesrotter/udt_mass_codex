#!/usr/bin/env python3
"""Fail-closed verifier for the UDT spacetime-model objectives audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parent

ALLOWED_CLASSES = {
    "FOUNDING_CONSTRAINT",
    "METRIC_DERIVED_STRUCTURE",
    "GLOBAL_COMPLETION_JOINT",
    "DYNAMICAL_CLOSURE_JOINT",
    "WORKING_BOOTSTRAP_HYPOTHESIS",
    "CONDITIONAL_MATTER_BRANCH",
    "OBSERVATIONAL_READOUT_OR_ANCHOR",
    "CERTIFICATE_SIDE_LEMMA",
    "DEFERRED_NONBLOCKING",
}
ALLOWED_PRIORITIES = {"NOW", "NEXT", "AFTER_LAW", "DOWNSTREAM", "PAUSED", "COMPARISON_ONLY"}
EXPECTED_OBJECTS = {
    "K01", "K02", "K03", "K04", "G01", "G02", "G03", "G04", "G05", "G06",
    "J01", "J02", "J03", "J04", "J05", "D01", "M01", "M02", "O01", "S01", "S02",
}
EXPECTED_TASKS = {
    "R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", "R11", "R12", "R13",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique_ids(rows: list[dict[str, str]], field: str, expected: set[str]) -> None:
    ids = [row[field] for row in rows]
    assert len(ids) == len(set(ids)), f"duplicate {field}"
    assert set(ids) == expected, f"{field} coverage mismatch"


def git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
    ).strip()


def validate_dependency(rows: list[dict[str, str]]) -> None:
    unique_ids(rows, "object_id", EXPECTED_OBJECTS)
    for row in rows:
        assert row["classification"] in ALLOWED_CLASSES
        assert row["priority"] in ALLOWED_PRIORITIES
        assert row["runtime_is_scientific_evidence"] == "NO"
        assert (ROOT / row["controlling_source"]).is_file()
    by_id = {row["object_id"]: row for row in rows}
    assert by_id["K01"]["classification"] == "FOUNDING_CONSTRAINT"
    assert by_id["K04"]["classification"] == "OBSERVATIONAL_READOUT_OR_ANCHOR"
    assert by_id["J02"]["classification"] == "DYNAMICAL_CLOSURE_JOINT"
    assert by_id["J04"]["classification"] == "WORKING_BOOTSTRAP_HYPOTHESIS"
    assert by_id["M02"]["classification"] == "CONDITIONAL_MATTER_BRANCH"
    assert by_id["S01"]["classification"] == "CERTIFICATE_SIDE_LEMMA"
    assert by_id["S01"]["priority"] == "PAUSED"
    assert by_id["D01"]["priority"] == "AFTER_LAW"


def validate_regrading(rows: list[dict[str, str]]) -> None:
    unique_ids(rows, "task_id", EXPECTED_TASKS)
    for row in rows:
        assert row["corrected_classification"] in ALLOWED_CLASSES
        assert row["new_priority"] in ALLOWED_PRIORITIES
        assert (ROOT / row["controlling_source"]).is_file()
    by_id = {row["task_id"]: row for row in rows}
    assert by_id["R01"]["new_priority"] == "NOW"
    assert by_id["R02"]["new_priority"] == "NEXT"
    assert by_id["R06"]["new_priority"] == "AFTER_LAW"
    assert by_id["R08"]["new_priority"] == "PAUSED"
    assert by_id["R11"]["new_priority"] == "DOWNSTREAM"


def validate_manifest() -> None:
    rows = read_tsv(AUDIT / "SOURCE_MANIFEST.tsv")
    listed = [line.strip() for line in (AUDIT / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    assert [row["path"] for row in rows] == listed
    assert len(listed) == len(set(listed))
    for row in rows:
        path = ROOT / row["path"]
        data = path.read_bytes()
        assert str(len(data)) == row["bytes"]
        assert sha(data) == row["sha256"]
        assert git_blob(row["path"]) == row["git_blob"]


def catch_proofs(dep: list[dict[str, str]], reg: list[dict[str, str]]) -> dict[str, str]:
    checks: dict[str, str] = {}

    def must_fail(name: str, fn) -> None:
        try:
            fn()
        except (AssertionError, KeyError):
            checks[name] = "PASS"
        else:
            raise AssertionError(f"catch proof did not fail: {name}")

    must_fail("missing_dependency_identity", lambda: validate_dependency(dep[:-1]))
    must_fail("duplicate_dependency_identity", lambda: validate_dependency(dep + [dict(dep[0])]))
    bad = [dict(row) for row in dep]
    bad[0]["classification"] = "DERIVED_ACTION"
    must_fail("invalid_classification", lambda: validate_dependency(bad))
    bad = [dict(row) for row in dep]
    bad[0]["runtime_is_scientific_evidence"] = "YES"
    must_fail("runtime_promoted_to_evidence", lambda: validate_dependency(bad))
    bad = [dict(row) for row in dep]
    next(row for row in bad if row["object_id"] == "S01")["priority"] = "NOW"
    must_fail("c08_promoted_to_blocker", lambda: validate_dependency(bad))
    bad = [dict(row) for row in dep]
    next(row for row in bad if row["object_id"] == "D01")["priority"] = "NOW"
    must_fail("time_live_before_native_law", lambda: validate_dependency(bad))
    bad = [dict(row) for row in dep]
    next(row for row in bad if row["object_id"] == "M02")["classification"] = "METRIC_DERIVED_STRUCTURE"
    must_fail("carrier_branch_promoted_to_metric_derived", lambda: validate_dependency(bad))
    bad = [dict(row) for row in dep]
    next(row for row in bad if row["object_id"] == "J04")["classification"] = "FOUNDING_CONSTRAINT"
    must_fail("bootstrap_promoted_to_founding", lambda: validate_dependency(bad))
    bad = [dict(row) for row in reg]
    next(row for row in bad if row["task_id"] == "R08")["new_priority"] = "NOW"
    must_fail("elimination_side_lemma_promoted", lambda: validate_regrading(bad))
    bad = [dict(row) for row in reg]
    next(row for row in bad if row["task_id"] == "R11")["new_priority"] = "NOW"
    must_fail("matter_moved_ahead_of_law", lambda: validate_regrading(bad))
    bad = [dict(row) for row in reg]
    bad.pop()
    must_fail("missing_regrading_identity", lambda: validate_regrading(bad))
    bad = [dict(row) for row in dep]
    bad[0]["controlling_source"] = "does/not/exist.md"
    must_fail("missing_controlling_source", lambda: validate_dependency(bad))
    return checks


def main() -> None:
    required = [
        "SPACETIME_MODEL_OBJECTIVES.md", "DEPENDENCY_LEDGER.tsv", "LOAD_BEARING_REGRADING.tsv",
        "RAM_AWARE_EXPLORATION_PROGRAM.md", "AUDIT_REPORT.md", "SOURCE_MANIFEST.tsv",
    ]
    for name in required:
        assert (AUDIT / name).is_file(), f"missing deliverable: {name}"
    dep = read_tsv(AUDIT / "DEPENDENCY_LEDGER.tsv")
    reg = read_tsv(AUDIT / "LOAD_BEARING_REGRADING.tsv")
    validate_dependency(dep)
    validate_regrading(reg)
    validate_manifest()
    proofs = catch_proofs(dep, reg)
    result = {
        "status": "PASS",
        "dependency_rows": len(dep),
        "regrading_rows": len(reg),
        "source_manifest_rows": len(read_tsv(AUDIT / "SOURCE_MANIFEST.tsv")),
        "catch_proofs": proofs,
        "deliverable_sha256": {
            name: sha((AUDIT / name).read_bytes()) for name in required
        },
    }
    (AUDIT / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
