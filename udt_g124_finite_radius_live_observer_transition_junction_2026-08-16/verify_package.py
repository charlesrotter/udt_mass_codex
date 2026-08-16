#!/usr/bin/env python3
"""Verify G124 source hashes, exact outcomes, and evidence files."""

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
    checks = {"source_count_eight": len(rows) == 8}
    for row in rows:
        path = ROOT / row["path"]
        checks[f"source::{row['path']}"] = path.is_file() and digest(path) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    checks["production_22_of_22"] = (
        production.get("status") == "PASS"
        and len(production.get("checks", {})) == 22
        and all(production.get("checks", {}).values())
    )
    checks["independent_15_of_15"] = (
        independent.get("status") == "PASS"
        and len(independent.get("checks", {})) == 15
        and all(independent.get("checks", {}).values())
    )
    for name in (
        "PREREGISTRATION.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "REVIEW_REQUEST.md",
        "BLIND_REVIEW_RAW.md",
        "CORRECTION_RECORD.md",
        "BLIND_REVIEW_FOLLOWUP.md",
        "AUDIT_REPORT.md",
    ):
        checks[f"present::{name}"] = (HERE / name).is_file()

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_count": len(rows),
        "checks": checks,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
