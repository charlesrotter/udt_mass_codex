#!/usr/bin/env python3
"""Fail-closed structural verifier for the foundations-to-CMB consultation package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    checks: list[str] = []

    manifest_path = PKG / "SOURCE_MANIFEST.tsv"
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(rows) == 20, f"expected 20 source rows, found {len(rows)}")
    require(len({row["path"] for row in rows}) == 20, "duplicate source path")
    require(len({row["role"] for row in rows}) == 20, "duplicate source role")
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing source: {row['path']}")
        require(sha256(path) == row["sha256"], f"source hash mismatch: {row['path']}")
        require("udt_native_onshell_timelive_reset_owner_audit" not in row["path"],
                "protected stopped draft entered source manifest")
    checks.append("20_source_hashes_and_roles")

    required_files = {
        "PREREGISTRATION.md",
        "AUDIT_REPORT.md",
        "SOURCE_MANIFEST.tsv",
        "WHITEBOARD_DEBATE.md",
        "CHAIR_ADJUDICATION.md",
        "TYPE_DEPENDENCY_LEDGER.tsv",
        "PROGRAM_OPTIONS.tsv",
        "path.md",
        "verify_consultation.py",
        "verify_repository_gates.py",
        "REPOSITORY_GATES.json",
    }
    actual_files = {path.name for path in PKG.iterdir() if path.is_file()}
    require(required_files <= actual_files, f"missing package files: {sorted(required_files-actual_files)}")
    checks.append("required_package_files")

    path_text = (PKG / "path.md").read_text(encoding="utf-8")
    required_headings = [
        "## 2. Founding implication chain",
        "## 3. What phi is, and what it is not",
        "## 4. The complete-coframe broadening",
        "## 5. The corrected observer-pair object",
        "## 7. Xmax: controlling meaning and current gap",
        "## 8. The SNe compatibility anchor",
        "## 9. The CMB arc before the current AM excavation",
        "## 10. G83--G86: the current conditional excavation",
        "## 12. Is the work linear or circular?",
        "## 13. The whiteboard's proposed object",
        "## 15. Cold external-review task",
    ]
    for heading in required_headings:
        require(heading in path_text, f"missing path.md heading: {heading}")
    for guard in [
        "not a route or history selector",
        "not silently a local signal velocity",
        "not yet a derived separation operator",
        "not physical profiles",
        "not on-shell solutions",
        "Do not revive strong local CSN",
    ]:
        require(guard in path_text, f"missing semantic guard: {guard}")
    checks.append("cold_brief_sections_and_guards")

    with (PKG / "TYPE_DEPENDENCY_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        dependency_rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(dependency_rows) == 21, f"expected 21 dependency rows, found {len(dependency_rows)}")
    require(len({row["id"] for row in dependency_rows}) == 21, "duplicate dependency id")
    require(any(row["id"] == "D04" and "physical_map_to_delta" in row["open_gate"]
                for row in dependency_rows), "missing founding-depth open gate")
    require(any(row["id"] == "D06" and
                row["status"] == "DEFINED_COMPLETE_CONFIGURATION_CHART__FINITE_JET_OPEN_ON_DECLARED_COMPONENT"
                for row in dependency_rows), "complete coframe chart improperly promoted")
    require(any(row["id"] == "D21" and row["status"] == "PROPOSED_TYPE_REFRAME"
                for row in dependency_rows), "typed total space improperly promoted")
    checks.append("dependency_ledger_types")

    with (PKG / "PROGRAM_OPTIONS.tsv").open(newline="", encoding="utf-8") as handle:
        option_rows = list(csv.DictReader(handle, delimiter="\t"))
    require(len(option_rows) == 6, f"expected 6 program rows, found {len(option_rows)}")
    require(sum(row["current_recommendation"] == "DO_FIRST_NO_SOLVE" for row in option_rows) == 1,
            "program ranking must have exactly one first action")
    require(any(row["current_recommendation"] == "PAUSE" for row in option_rows),
            "missing paused-program control")
    checks.append("program_options_fail_closed")

    result = {
        "status": "VERIFIED_STRUCTURAL_CONSULTATION_PACKAGE",
        "checks": checks,
        "source_rows": len(rows),
        "dependency_rows": len(dependency_rows),
        "program_rows": len(option_rows),
        "maximum_conclusion": "CONCEPTUAL_DIAGNOSIS_NO_NEW_PHYSICAL_SELECTOR",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
