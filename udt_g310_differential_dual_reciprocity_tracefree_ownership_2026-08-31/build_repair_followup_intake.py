#!/usr/bin/env python3
"""Build the sealed G310 R1/R2 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "AUDIT_REPORT.md", "CATCH_PROOF_RESULT.json", "COMMANDS.md", "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md", "EXACT_DERIVATION.md", "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
    "EXTERNAL_REVIEW_REPAIR_REQUEST.md", "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md",
    "MAP.md", "PONDER.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md", "REPAIR_IMPLEMENTATION.md", "RUN_RECORD.md",
    "SOURCE_SCOPE.tsv", "STATUS_LEDGER.tsv", "derive_ddr_tracefree.py", "run_catch_proofs.py",
    "verify_ddr_independent.py", "verify_package.py",
)
SOURCE_FILES = (
    "founding.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXACT_DERIVATION.md",
    "udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/EXACT_DERIVATION.md",
    "udt_g309_strengthened_chain_history_selection_audit_2026-08-31/EXACT_DERIVATION.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    subprocess.run(
        [sys.executable, "-S", str(PACKAGE / "verify_package.py")],
        cwd=PACKAGE,
        check=True,
        capture_output=True,
        text=True,
    )
    intake = Path(tempfile.mkdtemp(prefix="udt_g310_repair_followup_", dir="/tmp"))
    package_target = intake / PACKAGE.name
    package_target.mkdir()
    payloads: list[Path] = []
    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise SystemExit(f"missing package file: {source}")
        target = package_target / name
        shutil.copy2(source, target)
        payloads.append(target)
    for relative in SOURCE_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"missing source file: {source}")
        target = intake / "frozen_sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target)

    scope = {
        "question": "read-only repair-only follow-up for preregistered G310 repairs R1 and R2",
        "package": PACKAGE.name,
        "payload_count_including_scope": len(payloads) + 1,
        "total_file_count_including_manifest_and_detached_seal": len(payloads) + 3,
        "permissions": {
            "verify_only_G310_repairs_R1_R2_and_unchanged_landing": True,
            "inspect_only_this_intake": True,
            "run_checks_only_in_writable_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research_or_change_question": False,
            "access_repository_or_protected_packages": False,
            "use_internet_or_unsealed_observations": False,
            "adopt_DDR_or_select_history_scale_Xmax": False,
        },
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads.append(scope_path)
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in sorted(payloads, key=lambda item: item.relative_to(intake).as_posix()):
            writer.writerow((path.relative_to(intake).as_posix(), digest(path), path.stat().st_size))
    seal_path = intake / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{digest(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    result = {
        "intake": str(intake),
        "file_count": sum(1 for path in intake.rglob("*") if path.is_file()),
        "manifest_payloads": len(payloads),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest_path),
        "detached_seal_sha256": digest(seal_path),
    }
    assert result["file_count"] == scope["total_file_count_including_manifest_and_detached_seal"]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
