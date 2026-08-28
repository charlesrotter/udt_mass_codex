#!/usr/bin/env python3
"""Aggregate G289 evidence and provenance verification."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PACKAGE_VERIFICATION_RESULT.json"
LANDING = (
    "LOCAL_NULL_DIRECTION_EMBEDDING_EXISTS"
    "__FIXED_ROUND_S2_HOPFION_REQUIRES_SUPPLIED_FRAME_TARGET_AND_BOUNDARY"
    "__RAW_HOPF_CLASS_DOES_NOT_DESCEND_THROUGH_FULL_LOCAL_FRAME_GAUGE"
    "__CONFORMAL_HISTORY_TWINS_CARRY_THE_SAME_NULL_TEXTURE"
    "__STATIC_HOPFION_IS_CONDITIONALLY_COMPATIBLE_NOT_A_CURRENT_HISTORY_SELECTOR"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    required = {
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv", "COMMANDS.md", "STATUS_LEDGER.tsv", "EXACT_DERIVATION.md",
        "COMPATIBILITY_LEDGER.tsv", "HISTORY_SEPARATOR.tsv", "LAY_REPORT.md", "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md", "RUN_RECORD.md", "ADVERSARIAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
        "EXTERNAL_REPAIR_PREREGISTRATION.md", "REPAIR_RESULT.json",
        "REPAIR_FOLLOWUP_REQUEST.md", "build_repair_followup_intake.py",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md", "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
        "derive_compatibility.py", "verify_independent.py", "run_catch_proofs.py",
        "verify_repairs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "build_source_manifest.py", "verify_package.py",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    if missing:
        raise AssertionError(f"missing files: {missing}")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    if (
        production["status"] != "PASS"
        or production["landing"] != LANDING
        or production["check_count"] != 17
        or production["computed_check_count"] != 17
        or production["derived_conclusion_count"] != 6
        or production["total_claim_flags"] != 23
    ):
        raise AssertionError("production landing mismatch")
    if (
        not all(production["computed_checks"].values())
        or not all(production["derived_conclusions"].values())
        or production["imports_old_result_artifact"]
    ):
        raise AssertionError("production checks/provenance mismatch")
    if (
        independent["status"] != "PASS"
        or independent["assertions"] != 14537
        or independent["random_exact_cases"] != 1200
        or independent["hopf_connection_normalized_integral"] != "-1"
        or independent["hopf_integral_recomputed"] is not True
        or independent["compactification_basepoint_fixed"] is not True
        or independent["basepoint_adjoint_identity"] is not True
        or independent["imports_production_module"]
        or independent["reads_production_result"]
    ):
        raise AssertionError("independent replay mismatch")
    if (
        catches["status"] != "PASS"
        or catches["caught"] != 5
        or catches["total"] != 5
        or catches["recomputing_geometric_catches"] != 4
        or len(catches["recomputed_witnesses"]) != 5
    ):
        raise AssertionError("hostile catches mismatch")

    repairs = json.loads((HERE / "REPAIR_RESULT.json").read_text(encoding="utf-8"))
    if (
        repairs["status"] != "PASS"
        or repairs["repairs"] != ["R1", "R2", "R3", "R4"]
        or repairs["scientific_landing_changed"]
        or not all(repairs["checks"].values())
    ):
        raise AssertionError("external repair verification mismatch")

    manifest_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = ROOT / row["source"]
            if not source.is_file() or sha256(source) != row["sha256"]:
                raise AssertionError(f"source mismatch: {row['source']}")
            manifest_rows.append(row)
    if len(manifest_rows) != 13:
        raise AssertionError("source count mismatch")

    audit = "".join((HERE / "AUDIT_REPORT.md").read_text().split())
    if LANDING not in audit:
        raise AssertionError("audit landing mismatch")
    for token in (
        "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "EXTERNAL_REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED",
    ):
        if token not in (HERE / "AUDIT_REPORT.md").read_text():
            raise AssertionError(f"audit token missing: {token}")

    repair_followup = (HERE / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md").read_text(encoding="utf-8")
    if "REPAIRS_ACCEPTED" not in repair_followup or "Defects: none" not in repair_followup:
        raise AssertionError("external repair follow-up mismatch")

    result = {
        "status": "PASS",
        "required_files": len(required),
        "source_manifest_rows": len(manifest_rows),
        "production_computed_checks": production["computed_check_count"],
        "production_derived_conclusions": production["derived_conclusion_count"],
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["caught"],
        "landing": LANDING,
        "external_review": "ACCEPT_WITH_REPAIRS",
        "external_repair_followup": "REPAIRS_ACCEPTED",
        "aggregator_role": "integrity_and_provenance_only",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
