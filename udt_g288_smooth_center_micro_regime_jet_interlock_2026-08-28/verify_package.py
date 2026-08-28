#!/usr/bin/env python3
"""Aggregate G288 artifact and source-integrity verification."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PACKAGE_VERIFICATION_RESULT.json"
LANDING = (
    "PARTIAL_CENTER_INTERLOCK_ONLY"
    "__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE"
    "__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET"
    "__NO_PLANCK_SCALE_OR_HISTORY_SELECTED"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    required = {
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md", "STATUS_LEDGER.tsv", "derive_micro_center.py",
        "verify_independent.py", "run_catch_proofs.py", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    if missing:
        raise AssertionError(f"missing files: {missing}")

    prod = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    indep = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    if prod["landing_candidate"] != LANDING or prod["check_count"] != 22 or not all(prod["checks"].values()):
        raise AssertionError("production result mismatch")
    if indep["status"] != "PASS" or indep["assertions"] != 18117:
        raise AssertionError("independent result mismatch")
    if indep["imports_production_module"] or indep["reads_production_result"]:
        raise AssertionError("independence declaration failed")
    if catches["status"] != "PASS" or catches["caught"] != catches["total"] or catches["total"] != 9:
        raise AssertionError("hostile catch mismatch")

    prod_source = (HERE / "derive_micro_center.py").read_text()
    independent_source = (HERE / "verify_independent.py").read_text()
    forbidden_import_markers = ("udt_g201_", "udt_g204_", "udt_g262_", "udt_g264_")
    if any(marker in prod_source for marker in forbidden_import_markers):
        raise AssertionError("production source imports or reads an earlier/result artifact")
    if "sympy" in independent_source or "DERIVATION_RESULT.json" in independent_source:
        raise AssertionError("independent implementation is not dependency/artifact distinct")

    manifest_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["source"]
            if not path.is_file() or sha256(path) != row["sha256"]:
                raise AssertionError(f"source mismatch: {row['source']}")
            manifest_rows.append(row)
    if len(manifest_rows) != 9:
        raise AssertionError("source count mismatch")

    audit = (HERE / "AUDIT_REPORT.md").read_text()
    compact_audit = "".join(audit.split())
    if LANDING not in compact_audit:
        raise AssertionError("audit landing mismatch")
    for required_phrase in (
        "geometric mass-aspect",
        "does not select the Planck scale",
        "EXTERNAL_REVIEW_OPEN",
    ):
        if required_phrase.lower() not in audit.lower():
            raise AssertionError(f"audit phrase missing: {required_phrase}")

    result = {
        "status": "PASS",
        "required_files": len(required),
        "source_manifest_rows": len(manifest_rows),
        "production_checks": prod["check_count"],
        "independent_assertions": indep["assertions"],
        "hostile_catches": catches["caught"],
        "landing": LANDING,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
