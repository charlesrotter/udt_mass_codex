#!/usr/bin/env python3
"""Verify G123 source hashes and package-local results."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    checks = {"source_count_seven": len(rows) == 7}
    for row in rows:
        path = ROOT / row["path"]
        checks[f"source::{row['path']}"] = path.is_file() and digest(path) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    checks["production_16_of_16"] = production.get("status") == "PASS" and len(
        production.get("checks", {})
    ) == 16 and all(production.get("checks", {}).values())
    checks["independent_12_of_12"] = independent.get("status") == "PASS" and len(
        independent.get("checks", {})
    ) == 12 and all(independent.get("checks", {}).values())
    checks["preregistration_present"] = (HERE / "PREREGISTRATION.md").is_file()
    checks["next_gate_present"] = (HERE / "NEXT_GATE.md").is_file()
    checks["audit_report_present"] = (HERE / "AUDIT_REPORT.md").is_file()
    checks["blind_review_and_correction_present"] = all(
        (HERE / name).is_file()
        for name in (
            "BLIND_REVIEW_RAW.md",
            "CORRECTION_RECORD.md",
            "BLIND_REVIEW_FOLLOWUP.md",
        )
    )

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_count": len(rows),
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
