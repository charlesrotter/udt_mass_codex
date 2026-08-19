#!/usr/bin/env python3
"""Verify the complete bounded G166 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "AUDIT_REPORT.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "RUN_RECORD.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json",
        "CATCH_PROOF_RESULT.json",
        "SOURCE_CLASSIFICATION.tsv",
        "EVIDENCE_GATES.md",
    ]
    for name in required:
        assert (HERE / name).is_file(), name

    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    assert len(rows) == 13
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        assert actual == row["sha256"], row["path"]

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert derivation["checks_passed"] == derivation["checks_total"] == 22
    assert derivation["source_classes"] == 13
    assert independent["status"] == "PASS"
    assert independent["exact_fraction_trials"] == 1200
    assert catches["status"] == "PASS"
    assert catches["passed"] == catches["total"] == 9

    classes = list(csv.DictReader((HERE / "SOURCE_CLASSIFICATION.tsv").open(), delimiter="\t"))
    assert len(classes) == 13
    assert any(row["g166_class"] == "ALGEBRAIC_KERNEL_DESCENT" for row in classes)
    assert any(
        row["g166_class"] == "BROADER_ENVELOPE_CONTROL_NOT_FOUNDED_FREEDOM"
        for row in classes
    )

    report = (HERE / "AUDIT_REPORT.md").read_text()
    assert "PRIMARY_UDT_ORDERED_PAIR_KERNEL_DESCENDS_ALGEBRAICALLY" in report
    assert "G165 remains a valid control" in report
    assert "general `3+1` assembly" in report
    print("PASS: G166 package; 13 sources, 22 exact checks, 1200 trials, 9 catches")


if __name__ == "__main__":
    main()
