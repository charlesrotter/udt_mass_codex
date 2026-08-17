#!/usr/bin/env python3
"""Isolated source, production, and independent replay for G129."""

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


def main() -> None:
    checks: dict[str, bool] = {}

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count_eight"] = len(sources) == 8
    for row in sources:
        path = ROOT / row["path"]
        checks[f"source::{row['path']}"] = (
            path.is_file()
            and hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        )

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    checks["production_pass"] = production["status"] == "PASS"
    checks["production_18_of_18"] = (
        production["production_check_count"] == 18
        and all(production["checks"].values())
    )
    checks["production_landing"] = (
        production["landing"] == "FAITHFUL_IFF_PAIR_PLANE_SPAN_HAS_RANK_TEN"
    )
    checks["independent_pass"] = independent["status"] == "PASS"
    checks["independent_12_of_12"] = (
        independent["independent_check_count"] == 12
        and all(independent["checks"].values())
    )
    checks["independent_landing"] = independent["landing"] == production["landing"]

    with tempfile.TemporaryDirectory(prefix=".g129_replay_", dir=ROOT) as temp_name:
        temp = Path(temp_name)
        for source in HERE.iterdir():
            if source.is_file():
                shutil.copy2(source, temp / source.name)

        production_run = subprocess.run(
            [sys.executable, str(temp / "derive_network_faithfulness.py")],
            cwd=temp,
            text=True,
            capture_output=True,
            check=False,
        )
        independent_run = subprocess.run(
            [sys.executable, str(temp / "verify_network_faithfulness_independent.py")],
            cwd=temp,
            text=True,
            capture_output=True,
            check=False,
        )
        checks["fresh_production_exit"] = production_run.returncode == 0
        checks["fresh_independent_exit"] = independent_run.returncode == 0
        for name in (
            "DERIVATION_RESULT.json",
            "INDEPENDENT_VERIFICATION.json",
            "NETWORK_RANK_ATLAS.tsv",
        ):
            checks[f"fresh::{name}"] = (
                (temp / name).is_file()
                and (temp / name).read_bytes() == (HERE / name).read_bytes()
            )

    for name in (
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "SECOND_ADVERSARIAL_REVIEW.md",
        "REPAIR_ADJUDICATION.md",
        "FOLLOWUP_REVIEW.md",
    ):
        checks[f"present::{name}"] = (HERE / name).is_file()

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_count": len(sources),
        "verification_kind": "source_manifest_plus_fresh_isolated_exact_and_independent_replay",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
