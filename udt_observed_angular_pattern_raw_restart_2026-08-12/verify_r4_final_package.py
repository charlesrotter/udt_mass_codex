#!/usr/bin/env python3
"""Verify the final R4 closure manifest and headline status."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    with (HERE / "R4_FINAL_EVIDENCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 28
    assert len({row["artifact"] for row in rows}) == len(rows)
    for row in rows:
        path = HERE / row["artifact"]
        assert path.stat().st_size == int(row["bytes"]), row["artifact"]
        assert digest(path) == row["sha256"], row["artifact"]
    status = json.loads((HERE / "R4_FINAL_STATUS.json").read_text())
    verification = json.loads((HERE / "R4_VERIFICATION_RESULT.json").read_text())
    catches = json.loads((HERE / "R4_VERIFIER_CATCH_PROOF_RESULT.json").read_text())
    assert status["status"] == verification["status"] == catches["status"] == "PASS"
    assert status["relation_count"] == verification["relation_count"] == 9286
    assert status["cross_lag_entry_count"] == 9286 * (237 + 235)
    assert status["cap_covariance_record_count"] == verification["cap_covariance_record_count"] == 1164
    assert catches["case_count"] == 5
    assert status["external_adversarial_landing"] == "VERIFIED_WITH_CAVEATS"
    assert set(verification["max_range_projector_abs_difference_by_field"]) == {
        "range_fraction", "unresolved_fraction", "range_quadratic_per_rank"
    }
    assert "without_feature_selection" in (HERE / "R4_OUTCOME_REPORT.md").read_text().lower()
    print("PASS: R4 final package (28 manifest rows)")


if __name__ == "__main__":
    main()
