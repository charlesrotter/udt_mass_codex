#!/usr/bin/env python3
"""Final package consistency verifier for G86."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from verify_independent import validate


HERE = Path(__file__).resolve().parent
REQUIRED = {
    "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "FALSIFICATION_CONTRACT.tsv",
    "PREMISE_LEDGER.tsv", "derive_owner_atlas.py", "CONDITION_OWNER_ATLAS.tsv",
    "FAMILY_CONDITION_MATRIX.tsv", "CONDITIONAL_SELECTOR_ATLAS.tsv", "DERIVATION_RESULT.json",
    "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "STATUS_LEDGER.tsv", "RUN_RECORD.md",
    "verify_independent.py", "INDEPENDENT_VERIFICATION.json", "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json", "verify_repository_gates.py", "REPOSITORY_GATES.json",
}


def rows(path: str) -> list[dict[str, str]]:
    with (HERE / path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main() -> None:
    checks: dict[str, bool] = {}
    checks["required_files"] = all((HERE / path).is_file() for path in REQUIRED)
    checks["source_rows"] = len(rows("SOURCE_MANIFEST.tsv")) == 21
    checks["condition_rows"] = len(rows("CONDITION_OWNER_ATLAS.tsv")) == 14
    checks["matrix_rows"] = len(rows("FAMILY_CONDITION_MATRIX.tsv")) == 42
    checks["conditional_rows"] = len(rows("CONDITIONAL_SELECTOR_ATLAS.tsv")) == 4
    checks["independent_verifier"] = not validate()
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    repo = json.loads((HERE / "REPOSITORY_GATES.json").read_text())
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    checks["saved_independent"] = independent["verdict"] == "VERIFIED_WITH_CAVEATS" and not independent["errors"]
    checks["hostile_catches"] = catches["all_caught"] and catches["caught"] == catches["total"] == 12
    checks["repository_gates"] = repo["status"] == "PASS" and repo["pytest"] == "103 passed, 1 xfailed"
    checks["landing"] = result["primary_landing"] == "NO_EXISTING_OWNED_CONDITION_DISTINGUISHES_THE_THREE_G85_REGULAR_FAMILIES"
    checks["no_promotions"] = result["owned_nonidentity_selector_count"] == result["owned_exclusion_count"] == result["physical_promotions"] == 0
    payload = {
        "schema": "udt-cmb-g86-package-verification-v1",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_passed": all(checks.values()),
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(not payload["all_passed"])


if __name__ == "__main__":
    main()
