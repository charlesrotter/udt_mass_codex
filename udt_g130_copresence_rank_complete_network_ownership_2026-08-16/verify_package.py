#!/usr/bin/env python3
"""Isolated package and source-manifest replay for G130."""

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


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = (
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_MANIFEST.tsv",
        "SOURCE_ENTAILMENT.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS.md",
        "REVIEW_REQUEST.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "REPAIR_ADJUDICATION.md",
        "FOLLOWUP_REVIEW.md",
        "derive_copresence_network_ownership.py",
        "verify_copresence_network_ownership_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
    )
    checks = {f"present::{name}": (HERE / name).is_file() for name in required}

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        checks[f"source::{row['path']}"] = sha(ROOT / row["path"]) == row["sha256"]

    saved = {
        name: (HERE / name).read_bytes()
        for name in ("DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "SOURCE_ENTAILMENT.tsv")
    }
    with tempfile.TemporaryDirectory(prefix="g130_verify_") as tmp:
        tmp_root = Path(tmp)
        tmp_package = tmp_root / HERE.name
        shutil.copytree(HERE, tmp_package, ignore=shutil.ignore_patterns("__pycache__"))
        for row in sources:
            destination = tmp_root / row["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / row["path"], destination)
        production = subprocess.run(
            [sys.executable, str(tmp_package / "derive_copresence_network_ownership.py")],
            cwd=tmp_package, capture_output=True, text=True, check=False,
        )
        independent = subprocess.run(
            [sys.executable, str(tmp_package / "verify_copresence_network_ownership_independent.py")],
            cwd=tmp_package, capture_output=True, text=True, check=False,
        )
        checks["fresh_production_exit"] = production.returncode == 0
        checks["fresh_independent_exit"] = independent.returncode == 0
        for name, prior in saved.items():
            checks[f"fresh::{name}"] = (tmp_package / name).read_bytes() == prior

    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    indep = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    checks["production_18_of_18"] = prod.get("production_check_count") == 18 and all(prod["checks"].values())
    checks["independent_10_of_10"] = indep.get("independent_check_count") == 10 and all(indep["checks"].values())
    checks["landings_agree"] = prod.get("landing") == indep.get("landing")
    checks["expected_landing"] = prod.get("landing") == (
        "COPRESENCE_DENOTES_EVENT_COMEMBERSHIP_IN_SUPPLIED_S__RECIPROCITY_OWNS_LAW_SCHEMA__RANK_COMPLETE_NETWORK_VALUES_OPEN"
    )
    checks["production_status_pass"] = prod.get("status") == "PASS"
    checks["independent_status_pass"] = indep.get("status") == "PASS"
    checks["source_count_nine"] = len(sources) == 9 and len({row["path"] for row in sources}) == 9
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    followup = (HERE / "FOLLOWUP_REVIEW.md").read_text(encoding="utf-8")
    checks["substantive_review_verdict"] = "PASS_WITH_REPAIRS" in review
    checks["followup_pass"] = "FOLLOWUP_PASS" in followup

    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "status": status,
        "verification_kind": "source_manifest_plus_fresh_standalone_exact_and_independent_replay",
        "source_count": len(sources),
        "checks": checks,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
