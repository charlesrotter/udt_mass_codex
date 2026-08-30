#!/usr/bin/env python3
"""Mechanical verifier for the pre-external G305 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
LANDING = (
    "POSITIVE_STANDARD_GLOBAL_COMPLETION_NATIVELY_SUPPLIES_COMPACT_S3_HOPF_DOMAIN"
    "__STATIC_ZERO_IS_OBSERVER_HORIZON_NOT_MATERIAL_BOUNDARY"
    "__EXPLICIT_HOPF_CLASS_PERSISTS_KINEMATICALLY_AND_IS_SCALE_BLIND"
    "__TARGET_SECTION_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN"
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def frozen_registry_digest(path: Path) -> str:
    data = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(line for line in data if not line.startswith(b"G305\t"))).hexdigest()


def resolve_source(relative_path: str) -> Path:
    candidates = (
        REPO / relative_path,
        REPO / "frozen_sources" / relative_path,
    )
    matches = [path for path in candidates if path.is_file()]
    assert len(matches) == 1, {
        "relative_path": relative_path,
        "matches": [str(path) for path in matches],
    }
    return matches[0]


def main() -> None:
    required = {
        "MAP.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md", "PREMISE_LEDGER.tsv",
        "derive_global_hopf_bridge.py", "verify_global_hopf_bridge_independent.py",
        "run_global_hopf_catches.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md",
        "TOPOLOGY_CENSUS.tsv", "HOPF_REQUIREMENT_LEDGER.tsv", "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md", "SOURCE_SCOPE.tsv",
        "EXTERNAL_REVIEW_REQUEST.md", "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md", "build_review_intake.py", "verify_package.py",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    assert not missing, missing

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["landing"] == LANDING
    assert production["production_assertions"] == 77
    assert production["hopf_number_frozen_orientation"] == -1
    assert production["null_optical_tidal_all_signs"] == 0
    assert production["celestial_screen_euler_all_signs"] == 2
    rows = production["topology_census"]
    assert len(rows) == 3
    assert rows[0]["sector"] == "R0_positive" and rows[0]["compact_without_boundary"] is True
    assert all(row["compact_without_boundary"] is False for row in rows[1:])
    assert independent["status"] == "PASS" and independent["checks"] == 687
    assert independent["imports_production_code"] is False
    assert independent["finite_difference_cases"] == 24
    assert independent["max_finite_difference_metric_error"] < 3.6e-9
    assert independent["max_chart_overlap_error"] < 9.0e-16
    assert abs(independent["normalized_hopf_number"] + 1.0) < 2.0e-9
    assert independent["checks_by_category"] == {
        "ambient_constraints": 24,
        "hopf_and_scale_time": 157,
        "metric_coefficients": 384,
        "negative_global_relation": 36,
        "optical": 10,
        "positive_overlap": 54,
        "topology_witnesses": 22,
    }
    assert independent["topology_witnesses"]["positive"]["compact_without_boundary"] is True
    assert independent["topology_witnesses"]["zero"]["compact_without_boundary"] is False
    assert independent["topology_witnesses"]["negative_cover"]["compact_without_boundary"] is False
    assert catches["status"] == "PASS" and catches["caught"] == catches["total"] == 10
    assert catches["baseline_valid"] is True
    assert catches["corrupted_baseline_detected"] is True
    assert all(row["caught"] is True and row["violations"] for row in catches["catches"].values())

    with (HERE / "TOPOLOGY_CENSUS.tsv").open(newline="") as handle:
        topology = list(csv.DictReader(handle, delimiter="\t"))
    assert len(topology) == 3
    with (HERE / "HOPF_REQUIREMENT_LEDGER.tsv").open(newline="") as handle:
        requirements = list(csv.DictReader(handle, delimiter="\t"))
    assert len(requirements) == 11
    assert sum(row["status_after_G305"] == "OPEN" for row in requirements) == 7

    with (HERE / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 11
    for row in sources:
        source = resolve_source(row["path"])
        actual = frozen_registry_digest(source) if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv" else digest(source)
        assert actual == row["sha256"], row["path"]

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    audit = (HERE / "AUDIT_REPORT.md").read_text()
    lay = (HERE / "LAY_REPORT.md").read_text()
    assert LANDING in exact.replace("\n", "")
    assert LANDING in audit.replace("\n", "")
    for doc in (exact, audit, lay):
        low = doc.lower()
        for token in ("not", "history", "mass", "target", "action"):
            assert token in low, (doc[:20], token)
    assert "fc0ee889" in (HERE / "PREREGISTRATION_ANCESTRY.md").read_text()
    assert "Fresh external repair-only follow-up review remains required" in exact
    assert "PENDING" in (HERE / "EVIDENCE_GATES.md").read_text()

    result = {
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": len(sources),
        "topology_rows": len(topology),
        "requirement_rows": len(requirements),
        "production_assertions": production["production_assertions"],
        "independent_assertions": independent["checks"],
        "hostile_catches": catches["caught"],
        "external_review": "REPAIR_FOLLOWUP_PENDING",
        "external_fresh_verdict": "REPAIRABLE_DEFECTS",
        "repair_preregistration": "PRESENT",
        "corrupted_baseline_detected": catches["corrupted_baseline_detected"],
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
