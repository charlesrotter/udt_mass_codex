#!/usr/bin/env python3
"""Verify the final R5 evidence manifest, censuses, and ownership landing."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def table(name: str):
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    manifest = table("R5_FINAL_EVIDENCE_MANIFEST.tsv")
    assert len(manifest) == 34
    assert len({row["artifact"] for row in manifest}) == len(manifest)
    for row in manifest:
        path = HERE / row["artifact"]
        assert path.stat().st_size == int(row["bytes"]), row["artifact"]
        assert digest(path) == row["sha256"], row["artifact"]

    output_manifest = table("R5_OUTPUT_MANIFEST.tsv")
    assert len(output_manifest) == 5
    for row in output_manifest:
        path = HERE / row["artifact"]
        assert path.stat().st_size == int(row["bytes"]), row["artifact"]
        assert digest(path) == row["sha256"], row["artifact"]

    status = json.loads((HERE / "R5_FINAL_STATUS.json").read_text())
    result = json.loads((HERE / "R5_RESULT.json").read_text())
    verification = json.loads((HERE / "R5_VERIFICATION_RESULT.json").read_text())
    catches = json.loads((HERE / "R5_VERIFIER_CATCH_PROOF_RESULT.json").read_text())
    repair = json.loads((HERE / "R5_EXTERNAL_REVIEW_REPAIR_RESULT.json").read_text())

    assert status["status"] == "PASS_WITH_CAVEATS"
    assert verification["status"] == catches["status"] == "PASS"
    assert repair["status"] == "PASS__EXTERNAL_FOLLOWUP_VERIFIED_WITH_CAVEATS"
    assert status["external_adversarial_landing"] == repair["external_followup_landing"] == "VERIFIED_WITH_CAVEATS"
    assert result["parent_curve_count"] == status["parent_curve_count"] == 2328
    assert result["relation_count"] == status["relation_count"] == 9286
    assert result["view_spectrum_row_count"] == verification["view_spectrum_row_count"] == status["view_spectrum_row_count"] == 2607
    assert result["ranked_overlap_row_count"] == verification["ranked_overlap_row_count"] == status["ranked_overlap_row_count"] == 3555
    assert result["covariance_subspace_row_count"] == verification["covariance_subspace_row_count"] == status["covariance_subspace_row_count"] == 275868
    assert result["covariance_summary_row_count"] == verification["covariance_summary_row_count"] == status["covariance_summary_row_count"] == 2850

    covariance = table("R5_COVARIANCE_SUBSPACE_ATLAS.tsv")
    assert len(covariance) == 275868
    range_counts = Counter(int(row["range_overlap_owned"]) for row in covariance)
    assert range_counts == Counter({0: 184300, 1: 91568})
    assert all(row["covariance_range_relative_gap_to_threshold"] != "" for row in covariance)
    assert all(row["covariance_range_owned"] in {"0", "1"} for row in covariance)
    assert all(row["global_subspace_owned"] in {"0", "1"} for row in covariance)

    summaries = table("R5_COVARIANCE_SUBSPACE_SUMMARY.tsv")
    assert len(summaries) == 2850
    summary_counts = Counter(row["ownership_status"] for row in summaries)
    assert summary_counts == Counter({
        "OWNED": 2369,
        "UNRESOLVED_NUMERICAL": 475,
        "NUMERICAL_BOOKKEEPING": 6,
    })

    assert status["resolved_range_overlap_row_count"] == verification["resolved_range_overlap_row_count"] == 91568
    assert status["unresolved_range_overlap_row_count"] == verification["unresolved_range_overlap_row_count"] == 184300
    assert catches["case_count"] == status["hostile_mutation_cases_passed"] == 5
    assert "no remaining blocking" in (HERE / "R5_EXTERNAL_FOLLOWUP_REVIEW.md").read_text().lower()
    assert "does not establish a reduced rank" in (HERE / "R5_OUTCOME_REPORT.md").read_text().lower()
    print("PASS: R5 final package (34 manifest rows; ownership caveats preserved)")


if __name__ == "__main__":
    main()
