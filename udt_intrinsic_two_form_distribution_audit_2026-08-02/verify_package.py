#!/usr/bin/env python3
"""Fail closed on the final intrinsic two-form distribution evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {
    "PACKAGE_MANIFEST.sha256",
    "PACKAGE_VERIFICATION.json",
    "MANIFEST_STDOUT.txt",
    "MANIFEST_STDERR.txt",
    "PACKAGE_VERIFIER_STDOUT.txt",
    "PACKAGE_VERIFIER_STDERR.txt",
}


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

assert digest(HERE / "PREREGISTRATION.md") == "02011605b427dbfd8067aac68f9bae94b77531718a096e1b782550abe78384b2"
assert digest(HERE / "SOURCE_MANIFEST.tsv") == "48dcc11e79a0395e920c159a88346656011d8784118f11620f6996db040be122"

with (HERE / "CANDIDATE_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
    atlas = list(csv.DictReader(handle, delimiter="\t"))
assert len(atlas) == 18
assert sum(row["distribution_status"] == "ZERO" for row in atlas) == 9
assert sum(row["distribution_status"] == "MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI" for row in atlas) == 6
assert sum(row["distribution_status"] == "PROJECTOR_BLOCKED" for row in atlas) == 2
assert sum(row["distribution_status"] == "METRIC_DEGENERATE" for row in atlas) == 1

adjudication = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text(encoding="utf-8"))
production = json.loads((HERE / "DISTRIBUTION_RESULT.json").read_text(encoding="utf-8"))
semantic = json.loads((HERE / "SEMANTIC_VERIFICATION.json").read_text(encoding="utf-8"))
repository = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
cold = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text(encoding="utf-8"))

assert adjudication["status"] == "PASS_VERIFIED_BOUNDED_INTRINSIC_DISTRIBUTION_ATLAS"
assert adjudication["four_gates"] == "PASS_ALL_FOUR_FOR_BOUNDED_INTRINSIC_DISTRIBUTION_AND_DEGENERATION_ATLAS"
assert not adjudication["candidate_selected"] and not adjudication["physics_promoted"]
assert production["zero_locus"] == "q3=0 union C03 union C13 union C23"
assert production["nonzero_domain_components"] == 2
assert production["ruler_aligned_nonzero"] == "EMPTY_EXACT"
assert production["line_types_realized"] == ["SCREEN_CONTAINED", "GENERIC_MIXED"]
assert semantic["status"] == "PASS" and semantic["mutation_catches"] == 32
assert semantic["catch_classes"] == {
    "EXACT_OUTPUT_OR_ALGEBRA_GUARD": 26,
    "SEMANTIC_SCOPE_GUARD": 5,
    "EVIDENCE_BACKED_SEMANTIC_GUARD": 1,
}
assert cold["grade"] == "PASS" and cold["independent_exact_implementation"]
assert not cold["load_bearing_correction_required"]
assert repository["status"] == "PASS" and repository["tests"] == "70 passed, 1 xfailed"
assert repository["frozen_package_paths"] == 133 and repository["current_paths"] == 1114
assert repository["frontier_targets"] == 101

verification = {
    "status": adjudication["status"],
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "adjudication_result_sha256": digest(HERE / "ADJUDICATION_RESULT.json"),
    "candidate_atlas_sha256": digest(HERE / "CANDIDATE_ATLAS.tsv"),
    "headline": adjudication["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
