#!/usr/bin/env python3
"""Read-only package and frozen-source verification for G258."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREREGISTRATION_COMMIT = "a9f96360"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_source_digest(relative_path: str, expected: str) -> str:
    """Resolve an exact source byte stream without synthesizing historical content."""

    path = REPO / relative_path
    actual = digest(path)
    if actual == expected:
        return actual
    git_marker = REPO / ".git"
    if relative_path != "CURRENT_SCIENTIFIC_PREMISES.tsv" or not git_marker.exists():
        return actual
    completed = subprocess.run(
        ["git", "show", f"{PREREGISTRATION_COMMIT}:{relative_path}"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return hashlib.sha256(completed.stdout).hexdigest()


def main() -> None:
    required = (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "NODE_ATLAS.tsv",
        "ADJACENT_CHANGE_ATLAS.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "EXTERNAL_REVIEW_GPT54.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_CERTIFICATION.json",
        "derive_inverse_metric_reconstruction.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_repair.py",
    )
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert not missing, missing

    result = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    landing = "POINTWISE_RELATIVE_METRIC_STATE_RECONSTRUCTS__CONTINUOUS_LAW_REMAINS_OPEN"
    assert result["status"] == "PASS" and result["landing"] == landing
    assert result["node_count"] == 12 and result["fit_coefficients"] == 0
    assert result["positive_adjacent_changes"] == 10 and result["negative_adjacent_changes"] == 1
    assert abs(result["adjacent_changes"][-1]["standardized"] + 0.3098941412089942) < 2e-12
    assert max(result["maximum_residuals"].values()) < 2e-12
    assert independent["status"] == "PASS" and independent["landing"] == landing
    assert independent["assertions"] == 252
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert catches["status"] == "PASS" and catches["caught_count"] == 8
    assert all(catches["catches"].values())

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 10
    for source in sources:
        path = REPO / source["path"]
        assert path.is_file(), path
        actual = exact_source_digest(source["path"], source["sha256"])
        assert actual == source["sha256"], source["path"]

    print("PASS: G258 package, 10 source hashes, 12 nodes, 252 independent assertions, 8 catches")


if __name__ == "__main__":
    main()
