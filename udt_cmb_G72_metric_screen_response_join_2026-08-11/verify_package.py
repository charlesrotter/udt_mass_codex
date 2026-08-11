#!/usr/bin/env python3
"""Verify the bounded G72 package before repository banking."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = (
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST_CORRECTION_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_screen_response.py",
    "verify_screen_response_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_repository_gates.py",
    "build_review_manifest.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION_RESULT.json",
    "G68_RESPONSE_ATLAS.tsv",
    "TYPE_LEDGER.tsv",
    "RESPONSE_OWNERSHIP_LEDGER.tsv",
    "PREMISE_LEDGER.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "CATCH_PROOF_RESULTS.json",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "RUN_RECORD.md",
    "REPOSITORY_GATES.json",
    "EXTERNAL_REVIEW_DISPATCH.md",
    "REVIEW_MANIFEST.tsv",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    checks: dict[str, bool] = {}
    checks["required_files"] = all((HERE / name).is_file() for name in REQUIRED)

    source = table(HERE / "SOURCE_MANIFEST.tsv")
    checks["source_count"] = len(source) == 14
    checks["source_hashes"] = all(digest(ROOT / row["path"]) == row["sha256"] for row in source)
    checks["protected_excluded"] = all(
        not row["path"].startswith("udt_native_onshell_timelive_reset_owner_audit_2026-08-10/")
        for row in source
    )

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    checks["landing"] = result["landing"] == "METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN"
    checks["independent"] = independent["status"] == "PASS" and independent["trials"] == 1000
    checks["symbolic"] = all(result["symbolic_checks"].values())
    checks["gauge"] = (
        result["numerical_gauge_checks"]["trials"] == 512
        and result["numerical_gauge_checks"]["max_relative_angle_gauge_error"] < 1e-11
    )
    checks["g68"] = len(table(HERE / "G68_RESPONSE_ATLAS.tsv")) == 21
    checks["catches"] = catches["passed"] == catches["total"] == 14

    ownership = {row["target"]: row for row in table(HERE / "RESPONSE_OWNERSHIP_LEDGER.tsv")}
    checks["physical_owners_open"] = all(
        ownership[name]["status"] == "OPEN_NO_OWNER"
        for name in (
            "PHYSICAL_SCALAR_TT_RESPONSE",
            "PHYSICAL_POLARIZATION_RESPONSE",
            "SOURCE_POPULATION_AND_NORMALIZATION",
            "PHYSICAL_ENDPOINT_PROFILE_GLOBAL_SCALE",
        )
    )
    checks["response_conditional"] = ownership["RELATIVE_RESPONSE_OPERATOR"]["status"] == "DERIVED_CONDITIONAL_ON_COMMON_TYPED_QUERY"

    assert all(checks.values()), checks
    payload = {
        "schema": "udt-cmb-g72-package-verification-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "source_manifest_rows": len(source),
        "protected_draft_read": False,
        "landing": result["landing"],
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
