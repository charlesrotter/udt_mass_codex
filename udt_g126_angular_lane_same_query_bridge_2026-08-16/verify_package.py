#!/usr/bin/env python3
"""Verify G126 sources and replay both exact implementations in isolation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


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
    checks = {"source_count_ten": len(rows) == 10}
    for row in rows:
        path = ROOT / row["path"]
        checks[f"source::{row['path']}"] = path.is_file() and digest(path) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    checks["production_15_of_15"] = (
        production.get("status") == "PASS"
        and len(production.get("checks", {})) == 15
        and all(production.get("checks", {}).values())
    )
    checks["independent_12_of_12"] = (
        independent.get("status") == "PASS"
        and len(independent.get("checks", {})) == 12
        and all(independent.get("checks", {}).values())
    )

    with tempfile.TemporaryDirectory(prefix="udt_g126_replay_") as temp_name:
        temp = Path(temp_name)
        for name in ("derive_angular_bridge.py", "verify_angular_bridge_independent.py"):
            shutil.copy2(HERE / name, temp / name)
            replay = subprocess.run(
                [sys.executable, str(temp / name)],
                cwd=temp,
                text=True,
                capture_output=True,
                check=False,
            )
            checks[f"fresh_replay_exit::{name}"] = replay.returncode == 0
        checks["fresh_production_byte_identical"] = (
            (temp / "DERIVATION_RESULT.json").read_bytes()
            == (HERE / "DERIVATION_RESULT.json").read_bytes()
        )
        checks["fresh_independent_byte_identical"] = (
            (temp / "INDEPENDENT_VERIFICATION.json").read_bytes()
            == (HERE / "INDEPENDENT_VERIFICATION.json").read_bytes()
        )

    for name in (
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "REVIEW_REQUEST.md",
        "BLIND_REVIEW_RAW.md",
        "CORRECTION_RECORD.md",
        "BLIND_REVIEW_FOLLOWUP.md",
        "AUDIT_REPORT.md",
        "USER_FRAME_CORRECTION.md",
    ):
        checks[f"present::{name}"] = (HERE / name).is_file()

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "verification_kind": "source_manifest_plus_fresh_isolated_replay_and_byte_comparison",
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
