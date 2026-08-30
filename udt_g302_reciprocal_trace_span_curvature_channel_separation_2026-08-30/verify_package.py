#!/usr/bin/env python3
"""Mechanical package verifier for G302."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN"
    "__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION"
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    required = {
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION_ANCESTRY.md",
        "derive_trace_span_and_geometry.py", "verify_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "DOMAIN_CLASSIFICATION.tsv", "EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "SOURCE_MANIFEST.tsv", "COMMANDS.md",
        "RUN_RECORD.md",
    }
    missing = sorted(name for name in required if not (ROOT / name).is_file())
    assert not missing, missing

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catch = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["landing"] == LANDING
    assert production["status"] == "INTERNAL_PRODUCTION_DERIVATION_COMPLETE"
    assert production["gate_A"]["reciprocal_shape_rank"] == 9
    assert production["gate_A"]["complete_metric_rank"] == 10
    assert production["gate_B"]["complete_C2_solution"] == "-R0*r**2/12 + b/r + 1"
    assert production["gate_B"]["angular_parallel"] == "3*b/(2*r)"
    assert production["gate_B"]["angular_perpendicular"] == "-3*b/(2*r)"
    assert production["gate_B"]["smooth_areal_center_condition"] == "b=0"
    assert independent["status"] == "PASS"
    assert independent["imports_production_code"] is False
    assert (independent["shape_rank"], independent["complete_rank"]) == (9, 10)
    assert catch["status"] == "PASS" and catch["count"] == 11
    assert all(catch["caught"].values())

    with (ROOT / "DOMAIN_CLASSIFICATION.tsv").open(encoding="utf-8", newline="") as handle:
        domains = list(csv.DictReader(handle, delimiter="\t"))
    assert len(domains) == 8
    assert any(row["b_condition"] == "b=-4/(3*sqrt(R0))" for row in domains)
    assert any(row["positive_f_intervals"] == "(r_minus,r_plus)" for row in domains)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 7
    for row in sources:
        path = REPO / row["path"]
        assert path.is_file(), row["path"]
        assert digest(path) == row["sha256"], row["path"]

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for document in (exact, audit):
        assert "INTERNALLY_VERIFIED_BOUNDED_CLASSIFICATION_PENDING_FRESH_EXTERNAL_REVIEW" in document
    for document in (exact, lay, audit):
        assert "mass" in document.lower()
        assert "not" in document.lower()
    assert "physical query/plane population open" in exact
    assert "static, diagonal, areal-spherical" in exact

    physics = production["physics_changes"]
    assert not any(physics.values())

    output = {
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": len(sources),
        "domain_strata_verified": len(domains),
        "hostile_mutations_caught": catch["count"],
        "independent_verification": independent["status"],
        "fresh_external_review": "OPEN",
    }
    (ROOT / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G302 package verification PASS")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()

