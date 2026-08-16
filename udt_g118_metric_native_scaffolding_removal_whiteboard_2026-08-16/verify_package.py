#!/usr/bin/env python3
"""Rerunnable package verifier for G118."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "f977b2e8"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> None:
    required = [
        "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "AUDIT_REPORT.md", "DEPENDENCY_MAP.tsv",
        "SCAFFOLDING_LEDGER.tsv", "CATEGORY_ERROR_LEDGER.tsv", "ROLE_SYNTHESIS.md",
        "NEXT_DERIVATION.md", "LAY_REPORT.md", "SOLVER_COMPLETENESS_MAP.md", "EVIDENCE_GATES.md",
        "STATUS.md", "VERIFICATION_RESULT.json", "verify_whiteboard.py", "BLIND_REVIEW.md",
        "CORRECTION_RECORD.md", "REPOSITORY_GATES.json",
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {
        row["path"]: digest(ROOT / row["path"]) == row["sha256"]
        for row in rows
    }
    saved = (HERE / "VERIFICATION_RESULT.json").read_bytes()
    replay = subprocess.run(
        [sys.executable, str(HERE / "verify_whiteboard.py")],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    reproduced = replay.stdout == saved
    checks = {
        "required_files": all((HERE / name).is_file() for name in required),
        "all_16_source_hashes": len(rows) == 16 and all(hashes.values()),
        "preregistration_is_ancestor": subprocess.run(
            ["git", "merge-base", "--is-ancestor", PREREG_COMMIT, "HEAD"],
            cwd=ROOT,
            check=False,
        ).returncode == 0,
        "whiteboard_replay_returns_zero": replay.returncode == 0,
        "whiteboard_output_exactly_reproduced": reproduced,
        "whiteboard_replay_reports_pass": json.loads(saved)["status"] == "PASS",
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_hashes": hashes,
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(output, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
