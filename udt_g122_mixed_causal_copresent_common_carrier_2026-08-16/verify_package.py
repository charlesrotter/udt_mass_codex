#!/usr/bin/env python3
"""Verify G122 package-local results and frozen source hashes."""

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
    checks: dict[str, bool] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    checks["source_manifest_nonempty"] = len(rows) == 6
    for row in rows:
        path = ROOT / row["path"]
        checks[f"source::{row['path']}"] = path.is_file() and digest(path) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    checks["production_pass"] = production.get("status") == "PASS"
    checks["production_10_of_10"] = len(production.get("checks", {})) == 10 and all(
        production.get("checks", {}).values()
    )
    checks["independent_pass"] = independent.get("status") == "PASS"
    checks["independent_7_of_7"] = len(independent.get("checks", {})) == 7 and all(
        independent.get("checks", {}).values()
    )
    checks["preregistration_present"] = (HERE / "PREREGISTRATION.md").is_file()
    checks["next_gate_present"] = (HERE / "NEXT_GATE.md").is_file()

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
