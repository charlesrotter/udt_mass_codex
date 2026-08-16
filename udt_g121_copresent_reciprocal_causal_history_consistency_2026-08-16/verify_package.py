#!/usr/bin/env python3
"""Fresh replay and source-integrity verifier for G121."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count_10"] = len(rows) == 10
    for row in rows:
        path = REPO / row["path"]
        checks[f"source::{row['path']}"] = path.is_file() and digest(path) == row["sha256"]

    production_before = digest(PACKAGE / "DERIVATION_RESULT.json")
    independent_before = digest(PACKAGE / "INDEPENDENT_VERIFICATION.json")

    with tempfile.TemporaryDirectory(prefix="g121_verify_", dir=REPO) as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("derive_history_consistency.py", "verify_history_consistency_independent.py"):
            shutil.copy2(PACKAGE / name, tmp / name)
        subprocess.run(["python3", str(tmp / "derive_history_consistency.py")], check=True, capture_output=True, text=True)
        subprocess.run(
            ["python3", str(tmp / "verify_history_consistency_independent.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        checks["fresh_production_byte_match"] = digest(tmp / "DERIVATION_RESULT.json") == production_before
        checks["fresh_independent_byte_match"] = digest(tmp / "INDEPENDENT_VERIFICATION.json") == independent_before

    checks["live_production_unchanged"] = digest(PACKAGE / "DERIVATION_RESULT.json") == production_before
    checks["live_independent_unchanged"] = digest(PACKAGE / "INDEPENDENT_VERIFICATION.json") == independent_before

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    checks["production_pass"] = production.get("status") == "PASS"
    checks["production_check_count_20"] = len(production.get("checks", {})) == 20
    checks["production_all_checks_true"] = all(production.get("checks", {}).values())
    checks["independent_pass"] = independent.get("status") == "PASS"
    checks["independent_check_count_10"] = len(independent.get("checks", {})) == 10
    checks["independent_all_checks_true"] = all(independent.get("checks", {}).values())

    required = (
        "PREREGISTRATION.md",
        "WITNESS_CONTRACT.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "PREMISE_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "NEXT_GATE.md",
        "STATUS.md",
        "REPOSITORY_GATES.json",
    )
    for name in required:
        checks[f"required::{name}"] = (PACKAGE / name).is_file()

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_count": len(rows),
        "production_hash": production_before,
        "independent_hash": independent_before,
    }
    (PACKAGE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
