#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
exclude = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(name):
    with (here/name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

entries = {}
for line in (here/"PACKAGE_MANIFEST.sha256").read_text().splitlines():
    expected, name = line.split(None,1)
    relative = name.strip(); target = here/relative
    assert relative not in entries and target.is_file() and digest(target) == expected
    entries[relative] = expected
actual = {
    str(path.relative_to(here)) for path in here.rglob("*")
    if path.is_file() and path.name not in exclude and "__pycache__" not in path.parts
}
assert set(entries) == actual

assert digest(here/"PREREGISTRATION.md") == "020d44acf166ce3a0a0638485f1439dd4414c3f90655316cd2746044b14a2fc1"
assert digest(here/"SOURCE_MANIFEST.tsv") == "e486cdb7dd1147d0ce4d4fdb547e5c47726947b746e2cb33d471db54031defc8"
assert [(r["object_id"],r["object"]) for r in rows("OBJECT_STATUS.tsv")] == [(r["object_id"],r["object"]) for r in rows("OBJECT_UNIVERSE.tsv")]
assert [(r["premise_id"],r["choice_or_object"]) for r in rows("PREMISE_AUDIT.tsv")] == [(r["premise_id"],r["choice_or_object"]) for r in rows("PREMISE_LEDGER.tsv")]

production = json.loads((here/"TRANSPORT_RESULT.json").read_text())
independent = json.loads((here/"INDEPENDENT_VERIFICATION.json").read_text())
semantic = json.loads((here/"SEMANTIC_VERIFICATION.json").read_text())
cold = json.loads((here/"COLD_REVIEW_RESULT.json").read_text())
repository = json.loads((here/"REPOSITORY_GATES.json").read_text())
adjudication = json.loads((here/"ADJUDICATION_RESULT.json").read_text())

assert production["status"] == "PASS_EXACT_PRODUCTION"
assert production["line_w1"] == "ZERO_ON_ALL_H1_GENERATORS"
assert production["curvature_nonzero_certificates"] == 12
assert independent["status"] == "PASS_INDEPENDENT_HIGH_PRECISION" and independent["point_components_compared"] == 72
assert semantic["status"] == "PASS_FAIL_CLOSED" and semantic["mutation_catches"] == 36
assert cold["final_grade"] == "PASS_WITH_CAVEATS" and cold["algebra_failures"] == 0
assert repository["status"] == "PASS" and repository["tests"] == "70 passed, 1 xfailed"
assert repository["frozen_package_paths"] == 133 and repository["current_paths"] == 1114 and repository["frontier_targets"] == 101
assert adjudication["status"] == "VERIFIED_WITH_CAVEATS"
assert all(adjudication["four_gates"].values())
assert not adjudication["charge_carrier_substrate_or_physics_selected"]

verification = {
    "status": "PASS_PACKAGE_VERIFIED_WITH_CAVEATS",
    "entries": len(entries),
    "package_manifest_sha256": digest(here/"PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(here/"SOURCE_MANIFEST.tsv"),
    "adjudication_result_sha256": digest(here/"ADJUDICATION_RESULT.json"),
    "connection_points_sha256": digest(here/"CONNECTION_POINTS.tsv"),
    "object_status_sha256": digest(here/"OBJECT_STATUS.tsv"),
}
(here/"PACKAGE_VERIFICATION.json").write_text(json.dumps(verification, indent=2, sort_keys=True)+"\n", encoding="utf-8")
print(json.dumps(verification, sort_keys=True))
