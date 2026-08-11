#!/usr/bin/env python3
"""Verify the bounded G73 package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "REGULAR_SKY_RESPONSE_SOURCE_INVERTIBLE__"
    "ROBUST_KALEIDOSCOPE_REQUIRES_GLOBAL_BRANCHING_SINGULARITY_OR_SOURCE_RESTRICTION"
)
REQUIRED = (
    "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "derive_source_sensitivity.py",
    "verify_source_sensitivity_independent.py", "run_catch_proofs.py", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION_RESULT.json", "G68_SOURCE_SENSITIVITY_ATLAS.tsv",
    "RESPONSE_REGIME_ATLAS.tsv", "FALSIFICATION_CONTRACT.tsv", "TYPE_LEDGER.tsv",
    "OWNERSHIP_LEDGER.tsv", "CATCH_PROOF_RESULTS.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "RUN_RECORD.md",
)
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    ownership = {row["target"]: row["status"] for row in table(HERE / "OWNERSHIP_LEDGER.tsv")}
    checks = {
        "required_files": all((HERE / name).is_file() for name in REQUIRED),
        "source_count_and_hashes": len(sources) == 9 and all(digest(ROOT / row["path"]) == row["sha256"] for row in sources),
        "protected_excluded": not any(row["path"].startswith(PROTECTED_PREFIX) for row in sources),
        "landing": result["landing"] == LANDING,
        "exact_checks": all(value is True for value in result["exact_checks"].values() if isinstance(value, bool)),
        "g68_rows": result["g68_control"]["rows"] == len(table(HERE / "G68_SOURCE_SENSITIVITY_ATLAS.tsv")) == 21,
        "g68_strength": abs(result["g68_control"]["max_singular_value_ratio"] - 1.0046584288394136) < 2e-14,
        "independent": independent["status"] == "PASS" and independent["passed"] == independent["total"] == 11,
        "catches": catches["passed"] == catches["total"] == 9,
        "owners_open": ownership["CAUSTIC_OR_FOLD_BRANCH"] == "OPEN_NO_OWNER"
        and ownership["MULTIBRANCH_COMBINATION_RULE"] == "OPEN_NO_OWNER"
        and ownership["PHYSICAL_CMB_SOURCE_AND_OBSERVABLE"] == "OPEN_NO_OWNER",
    }
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        check=True, text=True, capture_output=True
    ).stdout.splitlines()
    checks["protected_metadata"] = len([line for line in status if line.startswith("?? " + PROTECTED_PREFIX)]) == 7
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g73-package-v1",
        "status": "PASS",
        "landing": LANDING,
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "protected_draft_read": False,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
