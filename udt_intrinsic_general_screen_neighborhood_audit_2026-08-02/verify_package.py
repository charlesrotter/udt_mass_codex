#!/usr/bin/env python3
"""Fail closed on the final intrinsic general-screen evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


entries = {}
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    relative = name.strip()
    target = HERE / relative
    assert relative not in entries and target.is_file() and digest(target) == expected
    entries[relative] = expected
actual = {
    str(path.relative_to(HERE))
    for path in HERE.rglob("*")
    if path.is_file() and path.name not in EXCLUDE and "__pycache__" not in path.parts
}
assert set(entries) == actual

assert digest(HERE / "PREREGISTRATION.md") == "16128a6cc0d9d7e78b7d07bf898c6cdca5ba2fa4d26f0b314976e02d4c8476b8"
assert digest(HERE / "CANDIDATE_UNIVERSE.tsv") == "a8c7c8f8c2c3992256e8b27d1e20bdd26b4f1e12d9ad5996b435531276ec2c9d"
assert digest(HERE / "SOURCE_MANIFEST.tsv") == "4117d443c5deb4742d6b11dceabc21460f5afda593c201ff84da9e2eda8eedad"
assert digest(HERE / "POINT_MANIFEST.sha256") == "61432ec911ca5b8fab9d51bac65235098609da88af4296b04e67ff7676aad7c4"

point_entries = []
for line in (HERE / "POINT_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    target = HERE / name.strip()
    assert target.is_file() and digest(target) == expected
    point_entries.append(name.strip())
assert len(point_entries) == len(set(point_entries)) == 34

with (HERE / "RESULT_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
    atlas = list(csv.DictReader(handle, delimiter="\t"))
assert len(atlas) == 18
assert sum(row["killing_line_status"].startswith("UNIQUE_") for row in atlas) == 16
assert sum(row["pair_projector_status"].startswith("METRIC_") for row in atlas) == 15
assert sum(row["intrinsic_contact_alternating_status"].startswith("NONZERO_SIMPLE") for row in atlas) == 6

adjudication = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text())
semantic = json.loads((HERE / "SEMANTIC_VERIFICATION.json").read_text())
repository = json.loads((HERE / "REPOSITORY_GATES.json").read_text())
cold = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text())
recheck = json.loads((HERE / "POST_REPAIR_RECHECK_RESULT.json").read_text())
parent = json.loads((HERE / "PARENT_REGRESSION.json").read_text())
killing = json.loads((HERE / "KILLING_LEMMA_CERTIFICATE.json").read_text())

assert adjudication["status"] == "PASS_VERIFIED_FRESH_COLD_REVIEW"
assert adjudication["four_gates"] == "PASS_ALL_FOUR_FOR_BOUNDED_CONFIGURATION_EXISTENCE"
assert adjudication["candidate_count"] == 18
assert adjudication["unique_killing_candidate_count"] == 16
assert adjudication["intrinsic_pair_candidate_count"] == 15
assert adjudication["intrinsic_pair_and_nonzero_count"] == 6
assert adjudication["full_screen_primary_intrinsic_nonzero_candidates"] == ["C08", "C09", "C10"]
assert adjudication["open_neighborhood_scope"] == "STATIONARY_BLOCK_SCREEN_SUBSPACE_RETAINING_K_ONLY"
assert not adjudication["universal_full_screen_claimed"]
assert not adjudication["on_shell_claimed"]
assert not adjudication["physics_promoted"]
assert not adjudication["full_GL2_or_time_live_exhausted"]

assert semantic["status"] == "PASS" and semantic["mutation_catches"] == 30
assert semantic["catch_classes"] == {
    "EXACT_OUTPUT_OR_ALGEBRA_GUARD": 19,
    "EVIDENCE_BACKED_SEMANTIC_GUARD": 2,
    "SEMANTIC_SCOPE_GUARD": 9,
}
assert cold["grade"] == "PASS_WITH_CAVEATS"
assert recheck["grade"] == "PASS" and recheck["blocking_corrections_remaining"] == 0
assert parent["status"] == "PASS_EXACT" and parent["parent_candidates"] == 3
assert killing["status"] == "PASS_EXACT" and killing["covers_time_dependent_candidate_coefficients"]
assert repository["status"] == "PASS" and repository["tests"] == "70 passed, 1 xfailed"
assert repository["frozen_package_paths"] == 133 and repository["current_paths"] == 1114
assert repository["frontier_targets"] == 101

verification = {
    "status": adjudication["status"],
    "entries": len(entries),
    "point_certificates": len(point_entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "point_manifest_sha256": digest(HERE / "POINT_MANIFEST.sha256"),
    "adjudication_result_sha256": digest(HERE / "ADJUDICATION_RESULT.json"),
    "result_atlas_sha256": digest(HERE / "RESULT_ATLAS.tsv"),
    "headline": adjudication["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(json.dumps(verification, sort_keys=True))
